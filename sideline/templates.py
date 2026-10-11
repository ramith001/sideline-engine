"""
The five analysis templates: each builds its per-team numbers, verdict and
pitch visual and returns the /analyze response dict.
"""

from mplsoccer import Pitch
import matplotlib.pyplot as plt
import pandas as pd

from sideline.metrics import (
    METERS,
    PPDA_AGGRESSIVE_MAX,
    PPDA_MODERATE_MAX,
    _classify_horizontal,
    _classify_vertical,
    _danger_map_for_team,
    _exploit_finder_for_team,
    _get_press_breaking_passes,
    _progress_trap_for_team,
    classify_ppda,
    compute_ppda,
    euclidean_to_goal,
    get_defensive_events,
    get_teams,
)
from sideline.models import AnalysisRequest
from sideline.story import generate_auto_story
from sideline.verdicts import _danger_map_verdict, _exploit_verdict, _progress_trap_verdict
from sideline.visuals import (
    _render_danger_pitch,
    _render_exploit_pitch,
    _render_progress_trap_pitch,
    fig_to_b64,
    make_pitch,
)


def _game_flow(df: pd.DataFrame, request: AnalysisRequest) -> dict:
    teams  = get_teams(df)
    team_a = teams[0]
    team_b = teams[1] if len(teams) > 1 else teams[0]

    # Period colours: dim = P1, bright = P2
    # Team A = cyan family, Team B = purple family
    period_colors = {
        team_a: {"p1": "#1a4a52", "p2": "#00e5ff"},   # dim teal / bright cyan
        team_b: {"p1": "#3b2a4a", "p2": "#a78bfa"},   # dim purple / bright purple
    }

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.patch.set_facecolor("#111827")
    fig.subplots_adjust(wspace=0.06)

    metrics_by_team = {}

    for i, (ax, team) in enumerate(zip(axes, teams[:2])):
        cols = period_colors[team]

        pitch = Pitch(pitch_type="statsbomb", pitch_color="#111827",
                      line_color="#4B5563", linewidth=1.0)
        pitch.draw(ax=ax)

        passes = df[(df["team"] == team) & (df["type"] == "Pass")
                    & (df["period"].isin([1, 2]))].copy()
        passes = passes.dropna(subset=["location", "pass_end_location"])
        passes = passes[passes["pass_outcome"].isna()]
        passes["x1"] = passes["location"].apply(lambda l: float(l[0]))
        passes["y1"] = passes["location"].apply(lambda l: float(l[1]))
        passes["x2"] = passes["pass_end_location"].apply(lambda l: float(l[0]))
        passes["y2"] = passes["pass_end_location"].apply(lambda l: float(l[1]))
        passes["d_start"] = passes.apply(lambda r: euclidean_to_goal(r["x1"], r["y1"]), axis=1)
        passes["d_end"]   = passes.apply(lambda r: euclidean_to_goal(r["x2"], r["y2"]), axis=1)
        passes["delta_d"] = passes["d_start"] - passes["d_end"]

        def _is_prog(row):
            x1, x2, dd = row["x1"], row["x2"], row["delta_d"]
            if x1 <= 60 and x2 <= 60: return dd > 30
            if x1 <= 60 and x2 > 60:  return dd > 15
            if x1 > 60:                return dd > 10
            return False

        passes["is_progressive"] = passes.apply(_is_prog, axis=1)
        prog = passes[passes["is_progressive"]].copy()

        p1 = prog[prog["period"] == 1]
        p2 = prog[prog["period"] == 2]

        # Period 1 — dim
        if not p1.empty:
            pitch.arrows(
                p1["x1"].tolist(), p1["y1"].tolist(),
                p1["x2"].tolist(), p1["y2"].tolist(),
                width=1.2, headwidth=7, headlength=7,
                color=cols["p1"], ax=ax, alpha=0.55, zorder=2,
            )

        # Period 2 — bright
        if not p2.empty:
            pitch.arrows(
                p2["x1"].tolist(), p2["y1"].tolist(),
                p2["x2"].tolist(), p2["y2"].tolist(),
                width=2.2, headwidth=10, headlength=10,
                color=cols["p2"], ax=ax, alpha=0.90, zorder=3,
            )

        rate1 = len(p1)
        rate2 = len(p2)
        delta = rate2 - rate1
        direction = "↑" if delta > 0 else "↓"

        total      = len(prog)
        ppda       = compute_ppda(df, team)
        press_cls  = classify_ppda(ppda)
        def_events  = get_defensive_events(df, team)
        
        # --- NEW SPLIT LOGIC ---
        p1_def = def_events[def_events["period"] == 1]
        p2_def = def_events[def_events["period"] == 2]
        
        avg_def_x_u = float(def_events["loc_x"].mean()) if not def_events.empty else 52.0
        avg_def_x_m = round(avg_def_x_u * METERS, 1)
        
        p1_x_u = float(p1_def["loc_x"].mean()) if not p1_def.empty else avg_def_x_u
        p2_x_u = float(p2_def["loc_x"].mean()) if not p2_def.empty else avg_def_x_u
        
        first_half_def_x_m = round(p1_x_u * METERS, 1)
        second_half_def_x_m = round(p2_x_u * METERS, 1)
        # -----------------------

        v_state     = _classify_vertical(avg_def_x_u)
        h_state     = _classify_horizontal(
            float((def_events["loc_y"] - 40.0).abs().mean()) if not def_events.empty else 20.0
        )

        ax.set_title(
            f"{team}  —  {rate1} prog passes (1st half)  →  {rate2} (2nd half)  {direction}{abs(delta)}",
            color=cols["p2"], fontsize=8, fontweight="bold", pad=6,
        )
        ax.text(2, 4, f"Line {avg_def_x_m}m",
                color="#9ca3af", fontsize=6.5, alpha=0.75)

        metrics_by_team[team] = {
            "avg_defensive_x_m":         avg_def_x_m,
            "first_half_defensive_x_m":  first_half_def_x_m,  # Added
            "second_half_defensive_x_m": second_half_def_x_m, # Added
            "vertical_state":            v_state,
            "horizontal_state":          h_state,
            "ppda":                      ppda,
            "press_class":               press_cls,
            "progressive_passes":        total,
            "prog_p1":                   rate1,
            "prog_p2":                   rate2,
            "prog_delta":                delta,
        }
    # Legend
    import matplotlib.patches as mp
    handles = [
        mp.Patch(facecolor="#1a4a52", alpha=0.8, label="1st half progressive passes"),
        mp.Patch(facecolor="#00e5ff", alpha=0.9, label=f"{teams[0]} — 2nd half progressive passes"),
        mp.Patch(facecolor="#3b2a4a", alpha=0.8, label="1st half progressive passes"),
        mp.Patch(facecolor="#a78bfa", alpha=0.9, label=f"{teams[1]} — 2nd half progressive passes"),
    ]
    fig.legend(handles=handles, loc="lower center", ncol=4, fontsize=6.5,
               framealpha=0.20, facecolor="#111827", edgecolor="#374151",
               labelcolor="white", bbox_to_anchor=(0.5, -0.06))
    fig.tight_layout()

    ma = metrics_by_team.get(team_a, {})
    mb = metrics_by_team.get(team_b, {})

    a_pp = ma.get("progressive_passes", 0)
    b_pp = mb.get("progressive_passes", 0)
    a_d  = ma.get("prog_delta", 0)
    b_d  = mb.get("prog_delta", 0)
    a_p1 = ma.get("prog_p1", 0)
    a_p2 = ma.get("prog_p2", 0)
    b_p1 = mb.get("prog_p1", 0)
    b_p2 = mb.get("prog_p2", 0)

    # Dynamic verdict based on momentum shift patterns
    biggest_shift_team = team_a if abs(a_d) >= abs(b_d) else team_b
    biggest_shift_val  = a_d if biggest_shift_team == team_a else b_d
    other_team         = team_b if biggest_shift_team == team_a else team_a
    other_d            = b_d if biggest_shift_team == team_a else a_d

    if abs(biggest_shift_val) >= 8:
        direction_word = "surged" if biggest_shift_val > 0 else "fell sharply"
        verdict = (
            f"The momentum story is clear. {biggest_shift_team}'s progressive passing "
            f"{direction_word} by {abs(biggest_shift_val)} between halves — from "
            f"{a_p1 if biggest_shift_team == team_a else b_p1} in the first half to "
            f"{a_p2 if biggest_shift_team == team_a else b_p2} in the second. "
            f"{other_team} shifted by {'+' if other_d > 0 else ''}{other_d} in comparison. "
            f"The half-time tactical adjustment was the defining moment of this match."
        )
    elif abs(a_d) >= 4 or abs(b_d) >= 4:
        verdict = (
            f"{team_a}: {a_p1} progressive passes in the first half, {a_p2} in the second "
            f"({'+' if a_d > 0 else ''}{a_d}). "
            f"{team_b}: {b_p1} in the first half, {b_p2} in the second "
            f"({'+' if b_d > 0 else ''}{b_d}). "
            f"The brighter arrows on each pitch show where the second-half momentum was concentrated."
        )
    else:
        verdict = (
            f"Both teams maintained relatively consistent progression across both halves. "
            f"{team_a}: {a_p1} → {a_p2} progressive passes. "
            f"{team_b}: {b_p1} → {b_p2}. "
            f"No major momentum shift detected — this was a match decided by execution, not tactical adjustment."
        )

    teams_list = get_teams(df)
    auto_story = generate_auto_story(df, teams_list)

    return {
        "match_id":      request.match_id,
        "mode":          request.mode,
        "team":          team_a,
        "pipeline_text": f"Game Flow complete. Both teams analysed across both halves.",
        "auto_story":    auto_story,
        "graphic_b64":   fig_to_b64(fig),
        "metrics": {
            **ma,
            "verdict_label": verdict,
            "teams_data_flow": [
                {"team": t, **metrics_by_team.get(t, {})} for t in teams[:2]
            ],
        },
    }


def _press_autopsy(df: pd.DataFrame, request: AnalysisRequest) -> dict:
    teams  = get_teams(df)
    team_a = teams[0]
    team_b = teams[1] if len(teams) > 1 else teams[0]

    team_colors = ["#00e5ff", "#a78bfa"]

    pitch, fig, ax = make_pitch()
    metrics_by_team = {}

    for i, team in enumerate(teams[:2]):
        col  = team_colors[i]
        ppda = compute_ppda(df, team)
        press_class = classify_ppda(ppda)
        pb   = _get_press_breaking_passes(df, team)

        total_under = len(df[
            (df["team"] == team) & (df["type"] == "Pass") &
            (df["period"] != 5) & (df["under_pressure"] == True)
        ])
        pb_count   = len(pb)
        exit_rate  = round((pb_count / total_under) * 100) if total_under > 0 else 0
        avg_gain_m = round(float(pb["delta_d"].mean()) * METERS, 1) if not pb.empty else 0.0

        def_events  = get_defensive_events(df, team)
        avg_def_x_u = float(def_events["loc_x"].mean()) if not def_events.empty else 52.57
        avg_def_x_m = round(avg_def_x_u * METERS, 1)

        if not pb.empty:
            # Mirror team B so they attack left
            if i == 1:
                pb = pb.copy()
                pb["x1"] = 120 - pb["x1"]
                pb["y1"] = 80  - pb["y1"]
                pb["x2"] = 120 - pb["x2"]
                pb["y2"] = 80  - pb["y2"]

            pitch.arrows(
                pb["x1"].tolist(), pb["y1"].tolist(),
                pb["x2"].tolist(), pb["y2"].tolist(),
                width=2, headwidth=10, headlength=10,
                color=col, ax=ax, alpha=0.80, zorder=2 + i,
            )
            pitch.scatter(
                pb["x1"].tolist(), pb["y1"].tolist(),
                color="#111827", edgecolors=col,
                s=100, linewidth=1.8, ax=ax, zorder=4 + i,
            )

        line_style = "--" if i == 0 else "-."
        ax.axvline(x=avg_def_x_u, color=col, linewidth=1.6,
                   linestyle=line_style, alpha=0.65, zorder=5)
        ly = 74 if i == 0 else 6
        ax.text(avg_def_x_u + 0.8, ly,
                f"{team[:3].upper()}  µ={avg_def_x_m}m",
                color=col, fontsize=6.5, alpha=0.85, fontweight="bold")

        metrics_by_team[team] = {
            "ppda":                   ppda,
            "press_class":            press_class,
            "avg_defensive_x_m":      avg_def_x_m,
            "press_breaking_count":   pb_count,
            "total_under_pressure":   total_under,
            "press_exit_rate_pct":    exit_rate,
            "avg_press_break_gain_m": avg_gain_m,
        }

    # Dynamic two-team verdict
    ma = metrics_by_team.get(team_a, {})
    mb = metrics_by_team.get(team_b, {})
    a_ppda = ma.get("ppda", 99)
    b_ppda = mb.get("ppda", 99)
    a_exit = ma.get("press_exit_rate_pct", 0)
    b_exit = mb.get("press_exit_rate_pct", 0)
    a_cls  = ma.get("press_class", "")
    b_cls  = mb.get("press_class", "")

    # Which team pressed harder?
    harder_presser = team_a if a_ppda <= b_ppda else team_b
    softer_presser = team_b if harder_presser == team_a else team_a
    hp_ppda = min(a_ppda, b_ppda)
    sp_ppda = max(a_ppda, b_ppda)
    hp_exit = a_exit if harder_presser == team_a else b_exit
    sp_exit = b_exit if harder_presser == team_a else a_exit

    if hp_ppda < PPDA_AGGRESSIVE_MAX and sp_exit >= 35:
        verdict = (
            f"{harder_presser} pressed with serious intensity (PPDA {hp_ppda}) but {softer_presser} "
            f"found a way through — {sp_exit}% of passes under pressure escaped. "
            f"A high press that wasn't suffocating enough."
        )
    elif hp_ppda < PPDA_AGGRESSIVE_MAX and sp_exit < 25:
        verdict = (
            f"{harder_presser}'s press was working (PPDA {hp_ppda}) — {softer_presser} "
            f"could only escape {sp_exit}% of the time. "
            f"{softer_presser}'s {sp_ppda} PPDA was passive by comparison, "
            f"but their deeper block ({mb.get('avg_defensive_x_m','—') if softer_presser==team_b else ma.get('avg_defensive_x_m','—')}m) "
            f"absorbed much of {harder_presser}'s forward momentum."
        )
    elif abs(a_exit - b_exit) >= 15:
        better_escape = team_a if a_exit >= b_exit else team_b
        worse_escape  = team_b if better_escape == team_a else team_a
        be_exit = max(a_exit, b_exit)
        we_exit = min(a_exit, b_exit)
        verdict = (
            f"{better_escape} were far more effective under pressure — {be_exit}% exit rate "
            f"vs {we_exit}% for {worse_escape}. "
            f"PPDA: {team_a} {a_ppda} vs {team_b} {b_ppda}. "
            f"The difference in press resistance was the clearest tactical gap of the match."
        )
    else:
        verdict = (
            f"Both teams pressed with similar intent — {team_a} PPDA {a_ppda} ({a_cls}), "
            f"{team_b} PPDA {b_ppda} ({b_cls}). "
            f"Press-breaking exit rates were comparable: {a_exit}% vs {b_exit}%. "
            f"Neither press dominated decisively."
        )

    import matplotlib.patches as mp
    handles = [
        mp.Patch(facecolor="#00e5ff", alpha=0.8, label=f"{teams[0]} — press-breaking pass"),
        mp.Patch(facecolor="#a78bfa", alpha=0.8, label=f"{teams[1]} — press-breaking pass"),
        plt.Line2D([0], [0], color="#00e5ff", linewidth=1.5, linestyle="--",
                   label=f"{teams[0]} avg defensive line"),
        plt.Line2D([0], [0], color="#a78bfa", linewidth=1.5, linestyle="-.",
                   label=f"{teams[1]} avg defensive line"),
    ]
    fig.legend(handles=handles, loc="lower center", ncol=4, fontsize=6.5,
               framealpha=0.20, facecolor="#111827", edgecolor="#374151",
               labelcolor="white", bbox_to_anchor=(0.5, -0.06))
    fig.tight_layout()

    receipt_lines = ["PRESS AUTOPSY REPORT", "=" * 60]
    for team in teams[:2]:
        m = metrics_by_team.get(team, {})
        receipt_lines += [
            f"\n{team.upper()}",
            f"  PPDA                  : {m.get('ppda','—')}  ({m.get('press_class','—')})",
            f"  Avg defensive line    : {m.get('avg_defensive_x_m','—')}m",
            f"  Passes under pressure : {m.get('total_under_pressure','—')}",
            f"  Press-breaking exits  : {m.get('press_breaking_count','—')}",
            f"  Exit rate             : {m.get('press_exit_rate_pct','—')}%",
            f"  Avg gain per exit     : {m.get('avg_press_break_gain_m','—')}m",
        ]

    return {
        "match_id":      request.match_id,
        "mode":          request.mode,
        "team":          team_a,
        "pipeline_text": "\n".join(receipt_lines),
        "auto_story":    None,
        "graphic_b64":   fig_to_b64(fig),
        "metrics": {
            **ma,
            "verdict_label":    verdict,
            "vertical_state":   "—",
            "horizontal_state": "—",
            "teams_data_press": [
                {"team": t, **metrics_by_team.get(t, {})} for t in teams[:2]
            ],
        },
    }


def _exploit_finder(df: pd.DataFrame, request: AnalysisRequest) -> dict:
    teams      = get_teams(df)
    teams_data = [_exploit_finder_for_team(df, t) for t in teams]
    primary    = teams_data[0] if teams_data else {}

    receipt_lines = ["EXPLOIT FINDER REPORT", "=" * 60]
    for td in teams_data:
        if not td:
            continue
        receipt_lines += [
            f"\n{td['team'].upper()}",
            f"  Defender line (mean x of their actions) : {td['def_line_m']}m",
            f"  Midfield line (mean x of their actions) : {td['mid_line_m']}m",
            f"  The Space Between                   : {td['gap_m']}m  ({td['comp_class']})",
            f"  Avg line height                     : {td['avg_line_m']}m",
            f"  Vertical state                      : {td['v_state']}",
            f"  Horizontal state                    : {td['h_state']}",
            f"  PPDA                                : {td['ppda']}  ({td['press_class']})",
            f"  False High Line                     : {'YES ⚠' if td['false_hl'] else 'No'}",
            f"  Structural risk                     : {td['risk_label']}",
            f"  Defensive events (n)                : {td['n_events']}",
        ]
    receipt_lines += [
        "\nMETHODOLOGY", "=" * 60,
        "Defender line = mean X of defensive events taken by defenders (CB, FB, WB)",
        "Midfield line = mean X of defensive events taken by midfielders",
        "Gap            = (midfield line - defensive line) × 0.875m",
        "Thresholds     : Compact < 12m | Standard 12-18m | Gapped > 18m",
        f"PPDA           : < {PPDA_AGGRESSIVE_MAX:g} Aggressive | < {PPDA_MODERATE_MAX:g} Moderate | >= {PPDA_MODERATE_MAX:g} Passive",
        f"False High Line: v_state == High Line AND PPDA >= {PPDA_AGGRESSIVE_MAX:g}",
    ]

    return {
        "match_id": request.match_id, "mode": request.mode,
        "team": primary.get("team", teams[0] if teams else ""),
        "pipeline_text": "\n".join(receipt_lines),
        "auto_story": None,
        "graphic_b64": _render_exploit_pitch(teams_data),
        "metrics": {
            "avg_defensive_x_m":  primary.get("avg_line_m"),
            "vertical_state":     primary.get("v_state"),
            "horizontal_state":   primary.get("h_state"),
            "ppda":               primary.get("ppda"),
            "press_class":        primary.get("press_class"),
            "verdict_label":      _exploit_verdict(teams_data),
            "def_line_m":         primary.get("def_line_m"),
            "mid_line_m":         primary.get("mid_line_m"),
            "gap_m":              primary.get("gap_m"),
            "comp_class":         primary.get("comp_class"),
            "false_hl":           primary.get("false_hl", False),
            "risk_label":         primary.get("risk_label"),
            "risk_color":         primary.get("risk_color", "#6b7280"),
            "teams_data":         teams_data,
        },
    }


def _danger_map(df: pd.DataFrame, request: AnalysisRequest) -> dict:
    teams      = get_teams(df)
    teams_data = [_danger_map_for_team(df, t) for t in teams]
    primary    = teams_data[0] if teams_data else {}

    receipt_lines = ["DANGER MAP REPORT", "=" * 60]
    for td in teams_data:
        receipt_lines += [
            f"\n{td['team'].upper()}",
            f"  Total progressive passes : {td['total_prog']}",
            f"  Danger corridor entries  : {td['danger_count']}",
            f"  Clinical efficiency      : {td['danger_pct']}%",
            f"  Avg ground gained        : {td['avg_gain_m']}m per pass",
            f"  Efficiency class         : {td['efficiency_class']}",
        ]
    receipt_lines += [
        "\nMETHODOLOGY", "=" * 60,
        "Progressive pass: completed pass where Euclidean Delta-D > threshold",
        "  Own half to own half : Delta-D > 30u",
        "  Own half to opp half : Delta-D > 15u",
        "  Opp half to opp half : Delta-D > 10u",
        f"Danger corridor: x in [88, 120], y in [18, 62]",
        "Clinical thresholds: High >= 35% | Moderate 20-35% | Low < 20%",
        "Team B coordinates mirrored (x->120-x, y->80-y) so they attack left.",
    ]

    def _strip_coords(td: dict) -> dict:
        return {k: v for k, v in td.items()
                if k not in ("all_x1","all_y1","all_x2","all_y2",
                             "danger_x1","danger_y1","danger_x2","danger_y2")}

    return {
        "match_id":      request.match_id,
        "mode":          request.mode,
        "team":          primary.get("team", teams[0] if teams else ""),
        "pipeline_text": "\n".join(receipt_lines),
        "auto_story":    None,
        "graphic_b64":   _render_danger_pitch(teams_data),
        "metrics": {
            "ppda":                None,
            "press_class":         None,
            "vertical_state":      None,
            "horizontal_state":    None,
            "verdict_label":       _danger_map_verdict(teams_data),
            "total_prog":          primary.get("total_prog"),
            "danger_count":        primary.get("danger_count"),
            "danger_pct":          primary.get("danger_pct"),
            "avg_gain_m":          primary.get("avg_gain_m"),
            "efficiency_class":    primary.get("efficiency_class"),
            "efficiency_color":    primary.get("efficiency_color", "#6b7280"),
            "teams_data_danger":   [_strip_coords(td) for td in teams_data],
        },
    }


def _progress_trap(df: pd.DataFrame, request: AnalysisRequest) -> dict:
    teams  = get_teams(df)
    team_a = teams[0]
    team_b = teams[1] if len(teams) > 1 else teams[0]

    td_a = _progress_trap_for_team(df, team_a, team_b)
    td_b = _progress_trap_for_team(df, team_b, team_a)
    teams_data = [td_a, td_b]
    primary    = td_a

    receipt_lines = ["PROGRESS TRAP REPORT", "=" * 60]
    for td in teams_data:
        receipt_lines += [
            f"\n{td['team'].upper()}",
            f"  Forward pass attempts     : {td['total_attempts']}",
            f"  Completed                 : {td['completed_count']}",
            f"  Stalled (incomplete)      : {td['stalled_count']}",
            f"  Stall rate                : {td['stall_rate']}%",
            f"  Primary stall zone        : {td['primary_stall_zone']} (n={td['primary_stall_n']})",
            f"  Forced wide (of completed): {td['forced_wide_pct']}%",
            f"  Opponent block depth      : {td['block_depth_m']}m  ({td['block_label']})",
        ]
    receipt_lines += [
        "\nMETHODOLOGY", "=" * 60,
        "Forward pass: x2 > x1 + 5u",
        "Stall: incomplete forward pass",
        "Wide: |y1 - 40| > 20u",
        "Block depth: mean X of the opponent's defensive events (own frame, goal at 0)",
    ]

    def _strip(td):
        return {k: v for k, v in td.items()
                if k not in ("stall_x","stall_y","comp_x1","comp_y1","comp_x2","comp_y2")}

    return {
        "match_id":      request.match_id,
        "mode":          request.mode,
        "team":          primary["team"],
        "pipeline_text": "\n".join(receipt_lines),
        "auto_story":    None,
        "graphic_b64":   _render_progress_trap_pitch(teams_data),
        "metrics": {
            "ppda": None, "press_class": None,
            "vertical_state": None, "horizontal_state": None,
            "verdict_label":      _progress_trap_verdict(teams_data),
            "total_attempts":     primary["total_attempts"],
            "stall_rate":         primary["stall_rate"],
            "primary_stall_zone": primary["primary_stall_zone"],
            "forced_wide_pct":    primary["forced_wide_pct"],
            "block_depth_m":      primary["block_depth_m"],
            "block_label":        primary["block_label"],
            "block_color":        primary["block_color"],
            "teams_data_trap":    [_strip(td) for td in teams_data],
        },
    }
