import streamlit as st
import io
import sys
import pandas as pd
import re
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from match_index import MATCH_INDEX


from sideline_ai_v01 import (
    run_pipeline,
    OUTPUT_MODE_BEGINNER,
    OUTPUT_MODE_ANALYST,
)

# Base Visuals
from visuals import (
    make_pitch,
    render_tactical_polygons,
    render_line_breakers,
    render_pressing_trap,
    add_visual_legend,
    
)

# Advanced Visuals (V0.2.1)
from visuals_v2 import (
    make_dark_pitch,
    render_rest_defence,
    render_isolation_island,
    render_transition_tracer,
    add_advanced_legend,
    get_game_state_split,
    render_game_state_shift
)

@st.cache_data
def load_events(mid: int) -> pd.DataFrame:
    from statsbombpy import sb
    return sb.events(match_id=mid)

st.set_page_config(page_title="Sideline AI", layout="wide")

st.markdown("""
    <style>
    .verdict-box {
        background-color: #EFE9FF;
        color: #2D1A54;
        padding: 20px;
        border-radius: 10px;
        font-size: 1.1em;
        margin-bottom: 25px;
        border-left: 5px solid #5A32A8;
    }
    .timeline-card {
        background-color: #F8F8F8;
        padding: 14px 18px;
        border-radius: 8px;
        margin-bottom: 12px;
        border-left: 4px solid #5A32A8;
    }
    .period-label {
        font-size: 0.8em;
        font-weight: 600;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 4px;
    }
    .shift-type {
        font-size: 0.85em;
        font-weight: 600;
        color: #5A32A8;
    }
    .shift-desc {
        font-size: 0.95em;
        color: #2D1A54;
        line-height: 1.5;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Sideline AI")
st.caption("2022 FIFA World Cup — Tactical Reasoning Engine")

with st.sidebar:
    st.markdown("### Step 1 — Select a match")
    stage = st.selectbox("Stage", list(MATCH_INDEX.keys()))
    match_options = MATCH_INDEX[stage]
    selected = st.selectbox("Match", match_options, format_func=lambda x: x[1])
    match_id, match_label = selected[0], selected[1]

    st.markdown("### Step 2 — Analysis depth")
    mode = st.radio("Mode", ["Beginner", "Analyst"])
    output_mode = OUTPUT_MODE_BEGINNER if mode == "Beginner" else OUTPUT_MODE_ANALYST

    st.markdown("### Step 3 — Text Template")
    template = st.radio("Template", ["The Game Flow", "The Exploit Finder", "The Press Autopsy", "The Danger Map"])
    
    st.markdown("### Step 4 — Base Pitch Visuals")
    show_net    = st.checkbox("Show Defensive Net",  value=True)
    show_danger = st.checkbox("Show Danger Zone",    value=True)
    show_laser  = st.checkbox("Show Line-Breakers",  value=True)
    show_trap   = st.checkbox("Show Pressing Traps", value=True)

    st.markdown("### Step 5 — Advanced Visuals")
    show_rest_def   = st.checkbox("Rest-Defence Snapshot",    value=False)
    show_isolation  = st.checkbox("Isolation Island",          value=False)
    show_transition = st.checkbox("Transition Tracer",         value=False)

    st.markdown("### Step 6 — Advanced Templates")
    show_game_state = st.checkbox("Game State Split",          value=False)

    run = st.button("Run analysis", type="primary", use_container_width=True)

if run:
    if "cache_key" not in st.session_state or st.session_state.cache_key != f"{match_id}_{output_mode}":
        with st.spinner(f"Running pipeline for {match_label}..."):
            old_stdout = sys.stdout
            sys.stdout = buffer = io.StringIO()
            results = run_pipeline(match_id=match_id, output_mode=output_mode)
            sys.stdout = old_stdout
            st.session_state.pipeline_output = buffer.getvalue()
            st.session_state.results = results
            st.session_state.cache_key = f"{match_id}_{output_mode}"
            st.session_state.match_label = match_label

if "results" in st.session_state:
    results = st.session_state.results
    match_label = st.session_state.match_label
    
    raw_output = st.session_state.pipeline_output
    clean_output = re.sub(r'=+', '', raw_output)
    clean_output = re.sub(r'\[\d/5\].*', '', clean_output)
    clean_output = re.sub(r'✓.*', '', clean_output)
    clean_output = clean_output.replace("Mode: BEGINNER", "").replace("Mode: ANALYST", "")
    clean_output = re.sub(r'\n\s*\n', '\n\n', clean_output).strip()

    st.subheader(match_label)
    st.divider()

    if template == "The Game Flow":
        momentum_df = results.get("momentum_df", pd.DataFrame())
        st.markdown("### 📈 TACTICAL MOMENTUM")
        if not momentum_df.empty:
            st.line_chart(momentum_df.set_index('Minute'))
            st.info("🧠 **Engine Analysis:** The graph above maps the average defensive line height minute-by-minute.")
        
        shape_shifts = results.get("shift_summary", pd.DataFrame())
        if not shape_shifts.empty:
            st.markdown("**TACTICAL TIMELINE**")
            for _, row in shape_shifts.iterrows():
                is_major = row.get("severity") == "major"
                st.markdown(f'''
                    <div class="{'timeline-card major' if is_major else 'timeline-card'}">
                        <div class="period-label">{row.get("from_period")} → {row.get("to_period")}</div>
                        <div class="shift-type">{"🔴" if is_major else "🟡"} {row.get("shift_type")} — {row.get("team")}</div>
                        <div class="shift-desc">{row.get("description")}</div>
                    </div>
                ''', unsafe_allow_html=True)

    elif template == "The Exploit Finder":
        comp_df = results.get("compactness_summary", pd.DataFrame())
        for _, team_data in comp_df.iterrows():
            team_name = team_data["team"]
            c_v_m = round(float(team_data.get("c_v", 0)) * 0.875, 1)
            comp_class = team_data.get("classification", "Neutral")
            
            st.markdown(f'<div class="verdict-box"><strong>VERDICT — {team_name.upper()}</strong><br><strong>Shape:</strong> {team_data.get("horizontal_state")} & {comp_class}<br><br>{team_data.get("risk_desc")}</div>', unsafe_allow_html=True)
            
            fig, ax = plt.subplots(figsize=(5, 4))
            fig.patch.set_alpha(0.0)
            ax.set_facecolor('none')
            ax.axis('off')
            ax.plot([0, 0], [0, 100], color='#374151', linewidth=2, linestyle='--')
            ax.plot([100, 100], [0, 100], color='#374151', linewidth=2, linestyle='--')
            
            base_y = 20
            midfield_y = base_y + c_v_m 
            
            ax.plot([0, 100], [base_y, base_y], color='#38BDF8', linewidth=4)
            ax.plot([0, 100], [midfield_y, midfield_y], color='#38BDF8', linewidth=4)
            glow_hex = '#EF4444' if comp_class == "Gapped" else '#22C55E'
            ax.add_patch(patches.Rectangle((0, base_y), 100, c_v_m, linewidth=0, facecolor=glow_hex, alpha=0.25))
            ax.set_xlim(-10, 110); ax.set_ylim(0, max(midfield_y + 20, 80))
            st.pyplot(fig, transparent=True)

    elif template == "The Press Autopsy":
        st.markdown("### 🛑 THE PRESS AUTOPSY")
        ppda_df = results.get("ppda_summary", pd.DataFrame())
        if not ppda_df.empty:
            st.bar_chart(ppda_df, x="team", y="ppda")
        for _, row in ppda_df.iterrows():
            st.markdown(f'<div class="verdict-box"><strong>VERDICT — {row["team"].upper()}</strong><br><br>{row.get("verdict_desc")}<br></div>', unsafe_allow_html=True)

    elif template == "The Danger Map":
        prog_df = results.get("progression_summary", pd.DataFrame())
        for _, row in prog_df.iterrows():
            total_prog = int(row["progressive_pass_count"])
            conv_rate = (row["danger_corridor_count"] / total_prog) if total_prog > 0 else 0.0
            danger_pct = int(conv_rate * 100)
            st.markdown(f'<div class="verdict-box"><strong>VERDICT — {row["team"].upper()}</strong><br>Threat Conversion: {danger_pct}%</div>', unsafe_allow_html=True)
            st.progress(conv_rate)

    if "pipeline_output" in st.session_state:
        raw_events = load_events(match_id)
        available_teams = sorted(raw_events["team"].dropna().unique().tolist())
        
        st.markdown("---")
        st.markdown("### 🏟️ SPATIAL TACTICS ENGINE")
        
        visual_team = st.selectbox("Select Team to Analyze", options=available_teams, key="visual_team_selector")
        opponent_team = [t for t in available_teams if t != visual_team]
        opponent_team = opponent_team[0] if opponent_team else visual_team

        # BASE PITCH
        any_visual_active = show_net or show_danger or show_laser or show_trap
        if any_visual_active:
            pitch, fig, ax = make_dark_pitch()
            render_tactical_polygons(ax, raw_events, team=visual_team, opponent=opponent_team, show_net=show_net, show_danger=show_danger)
            if show_laser: render_line_breakers(ax, raw_events, team=visual_team)
            if show_trap: render_pressing_trap(ax, raw_events, team=visual_team)
            add_visual_legend(ax, show_net, show_danger, show_laser, show_trap)
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)   

        # ADVANCED PITCH
        any_advanced = show_rest_def or show_isolation or show_transition
        if any_advanced:
            st.markdown("---")
            st.markdown("**Advanced Tactical View**")
            pitch, fig, ax = make_dark_pitch()
            if show_rest_def: render_rest_defence(ax, raw_events, visual_team, match_id)
            if show_isolation: render_isolation_island(ax, raw_events, visual_team)
            if show_transition: render_transition_tracer(ax, raw_events, visual_team)
            add_advanced_legend(ax, show_rest_def, show_isolation, show_transition)
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

        # GAME STATE SPLIT
        if show_game_state:
            st.markdown("---")
            st.markdown("## The Game State Split")
            split = get_game_state_split(raw_events, visual_team)
            if split.get("error"):
                st.info(split["error"])
            else:
                goal_min, goal_team = split["goal_minute"], split["goal_team"]
                before, after = split["before"], split["after"]
                
                st.markdown(f'<div class="verdict-box"><strong>SPLIT POINT</strong><br>First goal: minute {goal_min}\' ({goal_team})</div>', unsafe_allow_html=True)
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Before minute {goal_min}'**")
                    st.metric("PPDA", str(before["ppda"]))
                    st.metric("Defensive Line Height", f"{round((before['avg_x'] or 0) * 0.875, 1)}m")
                with col2:
                    st.markdown(f"**After minute {goal_min}'**")
                    st.metric("PPDA", str(after["ppda"]), delta=str(round(split["ppda_delta"], 2)), delta_color="inverse")
                    st.metric("Defensive Line Height", f"{round((after['avg_x'] or 0) * 0.875, 1)}m", delta=f"{split['x_delta_m']}m", delta_color="normal")
                
                st.divider()
                st.write(split["ppda_narrative"])
                st.write(split["x_narrative"])

                # ── Line Shift Graphic ───────────────────────────────
            st.markdown("**The Line Shift**")

            from mplsoccer import Pitch as _Pitch
            import matplotlib.pyplot as _plt

            _pitch = _Pitch(
                pitch_type="statsbomb",
                pitch_color="#0d1117",
                line_color="#3d4451",
                linewidth=1.0,
            )
            _fig, _ax = _pitch.draw(figsize=(10, 6))
            _fig.patch.set_facecolor("#0d1117")

            render_game_state_shift(_ax, raw_events, visual_team, split)

            st.pyplot(_fig, use_container_width=True)
            _plt.close(_fig)
    if mode == "Analyst":
        with st.expander("Technical Engine Receipts", expanded=False):
            st.code(clean_output, language="yaml")
else:
    st.info("Select a match and click **Run analysis**.")