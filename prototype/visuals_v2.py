"""
visuals_v2.py
Sideline.ai v0.2 — Advanced Tactical Feature Modules

Four new differentiating visual and text modules:
    1. Rest-Defence Snapshot      — CB/DM positions during opponent attacks
    2. Isolation Island           — Overload-to-isolate switch pass visualiser
    3. Game State Split           — PPDA + line height before vs after first goal
    4. Transition Sequence Tracer — Pass chain length + location after turnovers

All data filters wrapped in @st.cache_data.
All visuals use mplsoccer + matplotlib vector geometry only — no raster heatmaps.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from mplsoccer import Pitch
from scipy.spatial import ConvexHull
import streamlit as st


# =============================================================================
# SHARED PITCH HELPER
# =============================================================================

def make_dark_pitch():
    pitch = Pitch(
        pitch_type="statsbomb",
        pitch_color="#0d1117",
        line_color="#3d4451",
        linewidth=1.2,
    )
    fig, ax = pitch.draw(figsize=(12, 8))
    fig.patch.set_facecolor("#0d1117")
    return pitch, fig, ax


# =============================================================================
# MODULE 4: REST-DEFENCE SNAPSHOT
#
# Filters for moments when the team is in possession in the final third
# (x >= 80u), then maps where their CBs and DMs are sitting on average.
# Reveals how aggressively the backline pushes up when the team attacks.
#
# Position inference: StatsBomb lineup data includes position names.
# We match "Centre Back", "Defensive Midfield" from lineup and cross-reference
# with event player IDs during final-third possession moments.
# =============================================================================

@st.cache_data
def get_lineup_positions(match_id: int) -> pd.DataFrame:
    """
    Pulls lineup data and returns a DataFrame mapping player_id → position_name.
    Requires statsbombpy.
    """
    from statsbombpy import sb
    lineups = sb.lineups(match_id=match_id)
    rows = []
    for team_name, lineup_df in lineups.items():
        for _, player in lineup_df.iterrows():
            pos = player.get("positions", [])
            pos_name = pos[0]["position"] if pos else "Unknown"
            rows.append({
                "team":          team_name,
                "player_id":     player["player_id"],
                "player_name":   player["player_name"],
                "position":      pos_name,
            })
    return pd.DataFrame(rows)


@st.cache_data
def get_rest_defence_coords(
    events: pd.DataFrame,
    team: str,
    match_id: int,
) -> dict:
    """
    Returns average XY positions of CBs and DMs for `team`
    during moments when the team has the ball in the final third (x >= 80u).

    We use "Pressure" and "Ball Receipt*" events in x >= 80 as proxies
    for final-third possession moments, since carry/pass locations in
    StatsBomb reflect the team in possession.

    Returns:
        {
          "cb":  [(avg_x, avg_y), ...] per CB player,
          "dm":  [(avg_x, avg_y), ...] per DM player,
          "n_moments": int
        }
    """
    lineup_df = get_lineup_positions(match_id)
    team_lineup = lineup_df[lineup_df["team"] == team]

    cb_ids = set(team_lineup[
        team_lineup["position"].str.contains("Centre Back", case=False, na=False)
    ]["player_id"].tolist())

    dm_ids = set(team_lineup[
        team_lineup["position"].str.contains("Defensive Midfield", case=False, na=False)
    ]["player_id"].tolist())

    # Final-third possession: passes and carries by this team in x >= 80
    final_third = events[
        (events["team"] == team) &
        (events["type"].isin(["Pass", "Carry", "Ball Receipt*"])) &
        (events["period"] != 5)
    ].copy()
    final_third = final_third.dropna(subset=["location"])
    final_third["x"] = final_third["location"].apply(lambda l: float(l[0]))
    final_third = final_third[final_third["x"] >= 80]

    if final_third.empty:
        return {"cb": [], "dm": [], "n_moments": 0}

    # For each final-third moment, find what the CBs/DMs were doing nearby
    # (within same minute — StatsBomb minute resolution)
    # We filter all events in those minutes and find CB/DM locations
    ft_minutes = set(final_third["minute"].tolist())

    nearby = events[
        (events["minute"].isin(ft_minutes)) &
        (events["team"] == team) &
        (events["period"] != 5)
    ].copy()
    nearby = nearby.dropna(subset=["location"])
    nearby["x"] = nearby["location"].apply(lambda l: float(l[0]))
    nearby["y"] = nearby["location"].apply(lambda l: float(l[1]))

    cb_positions, dm_positions = [], []

    for pid in cb_ids:
        player_events = nearby[nearby["player_id"] == pid] if "player_id" in nearby.columns else pd.DataFrame()
        if not player_events.empty:
            cb_positions.append((
                float(player_events["x"].mean()),
                float(player_events["y"].mean()),
            ))

    for pid in dm_ids:
        player_events = nearby[nearby["player_id"] == pid] if "player_id" in nearby.columns else pd.DataFrame()
        if not player_events.empty:
            dm_positions.append((
                float(player_events["x"].mean()),
                float(player_events["y"].mean()),
            ))

    return {
        "cb":       cb_positions,
        "dm":       dm_positions,
        "n_moments": len(final_third),
    }


def render_rest_defence(ax, events, team, match_id):
    """
    Draws the Rest-Defence Snapshot onto the pitch.
    CBs shown as filled blue circles, DMs as filled teal diamonds.
    A dashed horizontal line shows the average backline height.
    """
    data = get_rest_defence_coords(events, team, match_id)

    cb_pts = data["cb"]
    dm_pts = data["dm"]
    n      = data["n_moments"]

    if not cb_pts and not dm_pts:
        return

    # Draw CBs
    for x, y in cb_pts:
        ax.scatter(x, y, s=220, color="#3a7bd5", zorder=6, alpha=0.9)
        ax.scatter(x, y, s=340, color="#3a7bd5", zorder=5, alpha=0.18)  # glow ring

    # Draw DMs
    for x, y in dm_pts:
        ax.scatter(x, y, s=200, marker="D", color="#1d9e75", zorder=6, alpha=0.9)
        ax.scatter(x, y, s=320, marker="D", color="#1d9e75", zorder=5, alpha=0.18)

    # Average backline X — dashed horizontal line
    all_x = [pt[0] for pt in cb_pts + dm_pts]
    if all_x:
        avg_x = float(np.mean(all_x))
        ax.axvline(
            x=avg_x,
            color="#ffcc00",
            linewidth=1.4,
            linestyle="--",
            alpha=0.55,
            zorder=4,
        )
        ax.text(
            avg_x + 0.8, 2,
            f"Avg line: {round(avg_x * 0.875, 1)}m",
            color="#ffcc00",
            fontsize=8,
            alpha=0.75,
        )

    # Caption
    ax.text(
        2, 76,
        f"Rest-defence during {n} final-third possession moments",
        color="white", fontsize=7.5, alpha=0.6,
    )


# =============================================================================
# MODULE 5: ISOLATION ISLAND
#
# Filters for horizontal switches: completed passes with |Δy| >= 35u
# (≈ 30.6m across the pitch) that land in the final third.
# Draws:
#   — A ConvexHull "Gravity Net" around all players clustered on the
#     departure side of the switch
#   — A spotlight circle around the isolated receiver
# =============================================================================

@st.cache_data
def get_isolation_switches(events: pd.DataFrame, team: str) -> pd.DataFrame:
    """
    Filters for horizontal switch passes:
        - Completed passes (pass_outcome is null)
        - |y2 - y1| >= 35u  (wide horizontal switch)
        - x2 >= 60u          (arriving in opponent's half or final third)
        - Forward or neutral direction (x2 >= x1 - 10)

    Returns DataFrame with x1, y1, x2, y2, delta_y columns.
    """
    passes = events[
        (events["team"] == team) &
        (events["type"] == "Pass") &
        (events["period"] != 5)
    ].copy()
    passes = passes.dropna(subset=["location", "pass_end_location"])
    passes = passes[passes["pass_outcome"].isna()]  # completed only

    passes["x1"] = passes["location"].apply(lambda l: float(l[0]))
    passes["y1"] = passes["location"].apply(lambda l: float(l[1]))
    passes["x2"] = passes["pass_end_location"].apply(lambda l: float(l[0]))
    passes["y2"] = passes["pass_end_location"].apply(lambda l: float(l[1]))
    passes["delta_y"] = (passes["y2"] - passes["y1"]).abs()

    switches = passes[
        (passes["delta_y"] >= 35) &
        (passes["x2"] >= 60) &
        (passes["x2"] >= passes["x1"] - 10)
    ].copy()

    return switches.reset_index(drop=True)


@st.cache_data
def get_crowded_side_coords(
    events: pd.DataFrame,
    team: str,
    switch_y1: float,
    minute_window: int = 1,
    switch_minute: int = 0,
) -> tuple:
    """
    For a given switch pass departure point (y1), finds all team events
    within ±minute_window minutes on the departure side of the pitch
    (same half as y1) to approximate the overloaded cluster.

    Returns (x_coords, y_coords) arrays.
    """
    half_y = 40.0
    departure_side_min = 0 if switch_y1 < half_y else half_y
    departure_side_max = half_y if switch_y1 < half_y else 80.0

    window_events = events[
        (events["team"] == team) &
        (events["minute"].between(switch_minute - minute_window,
                                   switch_minute + minute_window)) &
        (events["period"] != 5)
    ].copy()
    window_events = window_events.dropna(subset=["location"])
    window_events["ex"] = window_events["location"].apply(lambda l: float(l[0]))
    window_events["ey"] = window_events["location"].apply(lambda l: float(l[1]))

    crowd = window_events[
        window_events["ey"].between(departure_side_min, departure_side_max)
    ]
    return crowd["ex"].values, crowd["ey"].values


def render_isolation_island(ax, events, team):
    """
    Draws the Isolation Island visual for the most dramatic switch of the match.
    Picks the switch with the largest |Δy| as the showcase example.
    """
    switches = get_isolation_switches(events, team)
    if switches.empty:
        return

    # Pick the most dramatic switch (widest Δy)
    best = switches.loc[switches["delta_y"].idxmax()]

    x1, y1 = best["x1"], best["y1"]
    x2, y2 = best["x2"], best["y2"]
    switch_minute = int(best.get("minute", 0)) if "minute" in best else 0

    # ── Gravity Net: cluster on departure side ──
    cx, cy = get_crowded_side_coords(events, team, y1, switch_minute=switch_minute)
    if len(cx) >= 3:
        points = np.column_stack([cx, cy])
        try:
            hull  = ConvexHull(points)
            hpts  = points[hull.vertices]
            poly  = plt.Polygon(
                hpts, closed=True,
                facecolor="#3a7bd5", edgecolor="#3a7bd5",
                alpha=0.18, linestyle="--", linewidth=1.5,
            )
            ax.add_patch(poly)
            # Label
            ax.text(
                np.mean(cx), np.mean(cy),
                "OVERLOAD",
                color="#3a7bd5", fontsize=8, fontweight="bold",
                ha="center", va="center", alpha=0.7,
            )
        except Exception:
            pass

    # ── Switch arrow ──
    glow_layers = [
        {"lw": 8,   "alpha": 0.07},
        {"lw": 4,   "alpha": 0.15},
        {"lw": 2,   "alpha": 0.95},
    ]
    for layer in glow_layers:
        ax.annotate(
            "",
            xy=(x2, y2), xytext=(x1, y1),
            arrowprops=dict(
                arrowstyle="-|>",
                color="#ffcc00",
                lw=layer["lw"],
                alpha=layer["alpha"],
                mutation_scale=16,
            ),
        )

    # ── Spotlight circle around isolated receiver ──
    spotlight = plt.Circle(
        (x2, y2), radius=7.0,
        facecolor="#ffcc00", edgecolor="#ffcc00",
        alpha=0.18, linewidth=1.5, zorder=4,
    )
    ax.add_patch(spotlight)

    # Outer ring
    outer = plt.Circle(
        (x2, y2), radius=9.0,
        facecolor="none", edgecolor="#ffcc00",
        alpha=0.35, linewidth=1.0, linestyle="--", zorder=4,
    )
    ax.add_patch(outer)

    ax.text(
        x2, y2 - 11,
        "ISOLATED",
        color="#ffcc00", fontsize=8, fontweight="bold",
        ha="center", alpha=0.8,
    )

    delta_m = round(best["delta_y"] * 0.875, 1)
    ax.text(
        2, 76,
        f"Switch width: {delta_m}m  |  Minute: {switch_minute}'",
        color="white", fontsize=7.5, alpha=0.55,
    )


# =============================================================================
# MODULE 6: GAME STATE SPLIT
#
# Finds the minute of the first goal. Calculates PPDA and Avg Defensive X
# for events before that minute vs after that minute.
# Returns a structured dict for Streamlit text rendering.
# No pitch visual — this is a text/metric template.
# =============================================================================

@st.cache_data
def get_game_state_split(events: pd.DataFrame, team: str) -> dict:
    """
    Splits the match at the first goal and compares:
        - PPDA (pressing intensity) before vs after
        - Avg Defensive Line X before vs after

    Returns a dict with all values pre-computed for Streamlit rendering.
    """
    PPDA_ACTIONS = ["Tackle", "Interception", "Pressure", "Foul Committed"]
    DEF_TYPES    = ["Pressure", "Interception", "Block", "Duel", "Clearance"]
    METERS       = 0.875

    # ── Find first goal minute ──
    shot_events = events[
        (events["type"] == "Shot") &
        (events["shot_outcome"].apply(
            lambda x: x == "Goal" if isinstance(x, str) else
                      (x.get("name") == "Goal" if isinstance(x, dict) else False)
        ))
    ].copy()

    if shot_events.empty:
        return {"error": "No goals found in this match — cannot split."}

    shot_events_sorted = shot_events.sort_values(["period", "minute", "second"])
    first_goal         = shot_events_sorted.iloc[0]
    goal_minute        = int(first_goal["minute"])
    goal_period        = int(first_goal["period"])
    goal_team          = first_goal.get("team", "Unknown")

    # ── Helper: compute PPDA and avg_x for a subset ──
    def compute_metrics(subset, pressing_team):
        opp = [t for t in subset["team"].dropna().unique() if t != pressing_team]
        opp = opp[0] if opp else None

        pressing = subset[
            (subset["team"] == pressing_team) &
            (subset["type"].isin(PPDA_ACTIONS))
        ].copy()
        pressing = pressing.dropna(subset=["location"])
        pressing["px"] = pressing["location"].apply(lambda l: float(l[0]))
        pressing_zone  = pressing[pressing["px"] <= 60]

        if opp:
            opp_passes = subset[
                (subset["team"] == opp) &
                (subset["type"] == "Pass")
            ].copy()
            opp_passes = opp_passes.dropna(subset=["location"])
            opp_passes["px"] = opp_passes["location"].apply(lambda l: float(l[0]))
            opp_build  = opp_passes[opp_passes["px"] <= 60]
        else:
            opp_build = pd.DataFrame()

        ppda = (
            round(len(opp_build) / len(pressing_zone), 2)
            if len(pressing_zone) > 0
            else float("inf")
        )

        def_events = subset[
            (subset["team"] == pressing_team) &
            (subset["type"].isin(DEF_TYPES))
        ].copy()
        def_events = def_events.dropna(subset=["location"])
        def_events["dx"] = def_events["location"].apply(lambda l: float(l[0]))
        avg_x = round(def_events["dx"].mean(), 1) if not def_events.empty else float("nan")

        return {"ppda": ppda, "avg_x": avg_x, "n_events": len(subset)}

    # ── Split events ──
    # "Before" = all periods before the goal period, plus events in goal period before goal minute
    before_mask = (
        (events["period"] < goal_period) |
        ((events["period"] == goal_period) & (events["minute"] < goal_minute))
    )
    after_mask = (
        (events["period"] > goal_period) |
        ((events["period"] == goal_period) & (events["minute"] > goal_minute))
    )

    before_events = events[before_mask]
    after_events  = events[after_mask]

    before_metrics = compute_metrics(before_events, team)
    after_metrics  = compute_metrics(after_events,  team)

    # ── Build narrative ──
    ppda_delta = round(after_metrics["ppda"] - before_metrics["ppda"], 2)
    x_delta    = round((after_metrics["avg_x"] or 0) - (before_metrics["avg_x"] or 0), 1)

    if ppda_delta > 1.0:
        ppda_narrative = (
            f"{team} pressed significantly less after the goal "
            f"(PPDA rose from {before_metrics['ppda']} to {after_metrics['ppda']}). "
            "They sat deeper and invited pressure."
        )
    elif ppda_delta < -1.0:
        ppda_narrative = (
            f"{team} intensified their press after the goal "
            f"(PPDA dropped from {before_metrics['ppda']} to {after_metrics['ppda']}). "
            "They chased the game aggressively."
        )
    else:
        ppda_narrative = (
            f"{team}'s pressing intensity was largely unchanged "
            f"(PPDA: {before_metrics['ppda']} → {after_metrics['ppda']}). "
            "A disciplined, consistent tactical setup."
        )

    if abs(x_delta) >= 3:
        direction = "pushed higher" if x_delta > 0 else "dropped deeper"
        x_narrative = (
            f"Their defensive line {direction} by {round(abs(x_delta) * METERS, 1)}m "
            f"after the goal ({round(before_metrics['avg_x'] * METERS, 1)}m → "
            f"{round(after_metrics['avg_x'] * METERS, 1)}m)."
        )
    else:
        x_narrative = (
            f"Their defensive line height was stable "
            f"({round(before_metrics['avg_x'] * METERS, 1)}m → "
            f"{round(after_metrics['avg_x'] * METERS, 1)}m)."
        )

    return {
        "goal_minute":      goal_minute,
        "goal_team":        goal_team,
        "before":           before_metrics,
        "after":            after_metrics,
        "ppda_delta":       ppda_delta,
        "x_delta_m":        round(x_delta * METERS, 1),
        "ppda_narrative":   ppda_narrative,
        "x_narrative":      x_narrative,
        "error":            None,
    }


# =============================================================================
# MODULE 7: TRANSITION SEQUENCE TRACER
#
# After every turnover (Ball Recovery, Interception), counts how many
# consecutive passes the team completes before losing the ball again.
# Draws arrows showing transition chains that reached the final third.
# Reveals counter-pressing vs counter-attacking style numerically.
# =============================================================================

@st.cache_data
def get_transition_sequences(events: pd.DataFrame, team: str) -> pd.DataFrame:
    """
    Finds all turnover → pass chain sequences for `team`.

    For each ball-winning event:
        1. Record the start location (turnover point)
        2. Count consecutive completed passes by the same team immediately after
        3. Record where the chain died (lost possession or end of match)

    Returns DataFrame: turnover_x, turnover_y, chain_length, reached_final_third.
    """
    WIN_TYPES = ["Ball Recovery", "Interception"]

    all_events = events[events["period"] != 5].copy().sort_values(
        ["period", "minute", "second", "index"]
    ).reset_index(drop=True)

    win_indices = all_events[
        (all_events["team"] == team) &
        (all_events["type"].isin(WIN_TYPES)) &
        (all_events["location"].notna())
    ].index.tolist()

    rows = []
    for win_idx in win_indices:
        win_row = all_events.loc[win_idx]
        loc     = win_row["location"]
        tx      = float(loc[0]) if isinstance(loc, list) else float("nan")
        ty      = float(loc[1]) if isinstance(loc, list) else float("nan")

        chain_len   = 0
        reached_ft  = False

        for j in range(win_idx + 1, min(win_idx + 25, len(all_events))):
            ev = all_events.loc[j]
            if ev["team"] != team:
                break
            if ev["type"] == "Pass":
                if pd.isna(ev.get("pass_outcome")):  # completed
                    chain_len += 1
                    if ev.get("pass_end_location") is not None:
                        end_x = float(ev["pass_end_location"][0])
                        if end_x >= 80:
                            reached_ft = True
                else:
                    break  # incomplete pass — chain ends

        rows.append({
            "turnover_x":        tx,
            "turnover_y":        ty,
            "chain_length":      chain_len,
            "reached_final_third": reached_ft,
        })

    return pd.DataFrame(rows)


def render_transition_tracer(ax, events, team):
    """
    Draws the Transition Sequence Tracer.

    — Small orange dots for short transitions (< 3 passes)
    — Larger green dots for medium transitions (3-6 passes)
    — Bright green with pulse ring for transitions that reached the final third
    — A text summary of avg chain length in corner
    """
    df = get_transition_sequences(events, team)
    if df.empty:
        return

    for _, row in df.iterrows():
        x, y = row["turnover_x"], row["turnover_y"]
        cl   = int(row["chain_length"])
        ft   = bool(row["reached_final_third"])

        if ft:
            color  = "#00ff88"
            size   = 120 + cl * 20
            alpha  = 0.85
            # Pulse ring
            ring = plt.Circle((x, y), radius=5.5, facecolor="none",
                               edgecolor="#00ff88", linewidth=1.2,
                               alpha=0.35, zorder=4)
            ax.add_patch(ring)
        elif cl >= 3:
            color = "#88cc44"
            size  = 80 + cl * 12
            alpha = 0.65
        else:
            color = "#ff7700"
            size  = 40
            alpha = 0.45

        ax.scatter(x, y, s=size, color=color, alpha=alpha, zorder=5)

    # Summary stats
    avg_chain = round(df["chain_length"].mean(), 1)
    pct_ft    = round(df["reached_final_third"].mean() * 100)
    n_total   = len(df)

    ax.text(
        2, 76,
        f"Transitions: {n_total}  |  Avg chain: {avg_chain} passes  "
        f"|  {pct_ft}% reached final third",
        color="white", fontsize=7.5, alpha=0.6,
    )


# =============================================================================
# LEGEND FOR NEW MODULES
# =============================================================================

# =============================================================================
# MODULE 8: THE LINE SHIFT GRAPHIC
#
# Visually proves how a team's defensive block moved after the first goal.
# Designed to be a shareable Twitter/YouTube graphic.
#
# Layout (on a StatsBomb 120x80 pitch):
#   — Dashed blue vertical line  = Avg Defensive X BEFORE goal
#   — Solid red vertical line    = Avg Defensive X AFTER goal
#   — Glowing arrow              = Direction and magnitude of shift
#   — Delta annotation           = "Dropped 15.2m" or "Pushed 4.1m"
#   — Shaded zone between lines  = Magnitude of the shift made visible
# =============================================================================

def render_game_state_shift(ax, events, team, split_data: dict):
    """
    Draws the Line Shift graphic onto a pitch axis.

    Args:
        ax         — matplotlib axis from make_dark_pitch()
        events     — full match events DataFrame (used for context only)
        team       — team name string (for labelling)
        split_data — dict returned by get_game_state_split(events, team)
                     Must contain keys: before.avg_x, after.avg_x,
                     goal_minute, goal_team, x_delta_m, error
    """
    if split_data.get("error"):
        ax.text(
            60, 40, split_data["error"],
            color="white", fontsize=11, ha="center", va="center", alpha=0.6,
        )
        return

    METERS       = 0.875
    before_x     = split_data["before"]["avg_x"]   # in pitch units
    after_x      = split_data["after"]["avg_x"]    # in pitch units
    goal_minute  = split_data["goal_minute"]
    goal_team    = split_data["goal_team"]
    delta_m      = split_data["x_delta_m"]          # already in metres

    if before_x is None or after_x is None or np.isnan(before_x) or np.isnan(after_x):
        ax.text(60, 40, "Insufficient data for line shift.",
                color="white", fontsize=10, ha="center", alpha=0.5)
        return

    moved_forward = after_x > before_x
    direction_label = (
        f"Pushed {abs(delta_m):.1f}m higher"
        if moved_forward
        else f"Dropped {abs(delta_m):.1f}m deeper"
    )

    # ── Shaded zone between the two lines ────────────────────────
    shade_left  = min(before_x, after_x)
    shade_right = max(before_x, after_x)
    shade_color = "#00ff88" if moved_forward else "#e84560"

    shade = plt.Rectangle(
        (shade_left, 0),
        width=shade_right - shade_left,
        height=80,
        facecolor=shade_color,
        alpha=0.07,
        zorder=1,
    )
    ax.add_patch(shade)

    # ── BEFORE line — dashed blue ─────────────────────────────────
    ax.axvline(
        x=before_x,
        color="#3a7bd5",
        linewidth=2.0,
        linestyle="--",
        alpha=0.75,
        zorder=3,
    )
    ax.text(
        before_x - 1.2, 76,
        "BEFORE",
        color="#3a7bd5", fontsize=9, fontweight="bold",
        ha="right", va="top", alpha=0.85,
    )
    ax.text(
        before_x - 1.2, 71,
        f"{round(before_x * METERS, 1)}m",
        color="#3a7bd5", fontsize=8,
        ha="right", va="top", alpha=0.65,
    )

    # ── AFTER line — solid red ────────────────────────────────────
    ax.axvline(
        x=after_x,
        color="#e84560",
        linewidth=2.5,
        linestyle="-",
        alpha=0.90,
        zorder=3,
    )
    ax.text(
        after_x + 1.2, 76,
        "AFTER",
        color="#e84560", fontsize=9, fontweight="bold",
        ha="left", va="top", alpha=0.90,
    )
    ax.text(
        after_x + 1.2, 71,
        f"{round(after_x * METERS, 1)}m",
        color="#e84560", fontsize=8,
        ha="left", va="top", alpha=0.70,
    )

    # ── Glowing vector arrow connecting before → after ───────────
    # Arrow runs horizontally across the middle of the pitch (y=40)
    arrow_y      = 40.0
    box_y        = 40.0
    arrow_color  = "#00ff88" if moved_forward else "#ff6644"

    glow_layers = [
        {"lw": 16,  "alpha": 0.04},
        {"lw": 10,  "alpha": 0.09},
        {"lw": 5,   "alpha": 0.18},
        {"lw": 2.5, "alpha": 0.95},
    ]
    for layer in glow_layers:
        ax.annotate(
            "",
            xy=(after_x, arrow_y),
            xytext=(before_x, arrow_y),
            arrowprops=dict(
                arrowstyle="-|>",
                color=arrow_color,
                lw=layer["lw"],
                alpha=layer["alpha"],
                mutation_scale=22,
            ),
            zorder=5,
        )

    # ── Delta annotation box ──────────────────────────────────────
    mid_x = (before_x + after_x) / 2

    # Background pill for the label
    ax.text(
        mid_x, box_y + 6,
        direction_label,
        color=arrow_color,
        fontsize=11,
        fontweight="bold",
        ha="center",
        va="center",
        zorder=6,
        bbox=dict(
            boxstyle="round,pad=0.4",
            facecolor="#0d1117",
            edgecolor=arrow_color,
            alpha=0.85,
            linewidth=1.5,
        ),
    )

    # ── Goal event marker on the pitch ───────────────────────────
    # Small vertical band at x=60 (halfway) with goal annotation
    ax.text(
        2, 4,
        f"First goal: {goal_minute}'  ({goal_team})",
        color="white", fontsize=8, alpha=0.50,
    )

    # ── Team title ────────────────────────────────────────────────
    ax.text(
        60, 3,
        f"{team.upper()} — DEFENSIVE LINE SHIFT",
        color="white", fontsize=9, fontweight="bold",
        ha="center", alpha=0.70,
    )


def add_advanced_legend(ax, show_rest_def, show_isolation, show_transition):
    handles = []
    if show_rest_def:
        handles.append(mpatches.Patch(
            facecolor="#3a7bd5", alpha=0.7, label="Centre Back (rest-defence)"))
        handles.append(mpatches.Patch(
            facecolor="#1d9e75", alpha=0.7, label="Defensive Mid (rest-defence)"))
    if show_isolation:
        handles.append(mpatches.Patch(
            facecolor="#ffcc00", alpha=0.5, label="Switch receiver (isolated)"))
        handles.append(mpatches.Patch(
            facecolor="#3a7bd5", alpha=0.3, label="Overloaded cluster"))
    if show_transition:
        handles.append(mpatches.Patch(
            facecolor="#00ff88", alpha=0.7, label="Transition → final third"))
        handles.append(mpatches.Patch(
            facecolor="#88cc44", alpha=0.7, label="Transition 3+ passes"))
        handles.append(mpatches.Patch(
            facecolor="#ff7700", alpha=0.6, label="Transition < 3 passes"))
    if handles:
        ax.legend(
            handles=handles, loc="lower left", fontsize=7.5,
            framealpha=0.3, facecolor="#0d1117",
            edgecolor="#3d4451", labelcolor="white",
        )
