"""
Shared constants, thresholds and per-team metric functions: PPDA, defensive
lines, compactness, progressive passes, danger-map and progress-trap numbers.
"""

import math

import pandas as pd


# ── Shared constants ──────────────────────────────────────────────────────────
GOAL         = (120.0, 40.0)


METERS       = 0.875


# PPDA = opponent passes in their own defensive two-thirds / our defensive
# actions in that same stretch of pitch. StatsBomb has no "Tackle" event type:
# tackles are Duel events with duel_type == "Tackle". Pressure events are
# deliberately excluded, they are not defensive actions in the Opta definition
# and counting them collapses PPDA to ~3.
# StatsBomb coordinates are normalised per team (every team attacks towards
# x=120), so each team's events are read in that team's own frame.
PPDA_ACTION_TYPES  = ["Interception", "Foul Committed"]


PPDA_PRESS_MIN_X   = 40.0    # pressing team's frame: opponent's defensive 2/3


PPDA_PASS_MAX_X    = 80.0    # opponent's frame: their own defensive 2/3


# Percentile-based on this dataset, not an external standard. The old 2.5 / 3.5 /
# 4.4 cut-offs sat at the 19th / 54th / 75th percentile of the old metric;
# scripts/calibrate_ppda.py maps those percentiles onto the corrected metric
# (8.9 / 14.4 / 19.3 over all 292 team-matches) and these are the rounded values.
# Resulting split: 19% Aggressive / 59% Moderate / 22% Passive.
PPDA_AGGRESSIVE_MAX = 9.0


PPDA_MODERATE_MAX   = 20.0


PPDA_PRESSED_MAX    = 14.0   # "opponent pressed hard" gate in the press-bypass story


DANGER_CORRIDOR = {"x_min": 88.0, "x_max": 120.0, "y_min": 18.0, "y_max": 62.0}


# ── Shared helpers ────────────────────────────────────────────────────────────
def euclidean_to_goal(x: float, y: float) -> float:
    return math.sqrt((GOAL[0] - x) ** 2 + (GOAL[1] - y) ** 2)


def get_teams(df):
    return sorted(df["team"].dropna().unique().tolist())


def compute_ppda(df: pd.DataFrame, pressing_team: str) -> float:
    teams    = df["team"].dropna().unique().tolist()
    opponent = next((t for t in teams if t != pressing_team), None)
    if not opponent:
        return float("inf")
    df = df.copy()
    df["loc_x"] = df["location"].apply(
        lambda l: float(l[0]) if isinstance(l, (list, tuple)) else float("nan"))
    in_play = df["period"] != 5
    if "duel_type" in df.columns:
        is_tackle = (df["type"] == "Duel") & (df["duel_type"] == "Tackle")
    else:
        is_tackle = pd.Series(False, index=df.index)
    opp_passes = len(df[
        (df["team"] == opponent) & (df["type"] == "Pass") & in_play &
        df["pass_outcome"].isna() & (df["loc_x"] <= PPDA_PASS_MAX_X)
    ])
    press_actions = len(df[
        (df["team"] == pressing_team) & in_play &
        (df["type"].isin(PPDA_ACTION_TYPES) | is_tackle) &
        (df["loc_x"] >= PPDA_PRESS_MIN_X)
    ])
    return round(opp_passes / press_actions, 2) if press_actions > 0 else float("inf")


def classify_ppda(ppda: float) -> str:
    if ppda < PPDA_AGGRESSIVE_MAX: return "Aggressive Press"
    if ppda < PPDA_MODERATE_MAX:   return "Moderate Press"
    return "Passive / Low Press"


def get_defensive_events(df: pd.DataFrame, team: str) -> pd.DataFrame:
    # StatsBomb has no "Tackle" event type: tackles are Duel events with
    # duel_type == "Tackle", so "Duel" below already covers them (along with
    # lost aerial duels). Every Duel is kept on purpose: narrowing to tackles
    # only would drop the aerials and shift defensive-line heights.
    DEF_TYPES = ["Pressure", "Interception", "Block", "Duel", "Clearance"]
    events = df[
        (df["team"] == team) & (df["type"].isin(DEF_TYPES)) & (df["period"] != 5)
    ].copy()
    events = events.dropna(subset=["location"])
    events["loc_x"] = events["location"].apply(lambda l: float(l[0]))
    events["loc_y"] = events["location"].apply(lambda l: float(l[1]))
    return events


def _exclude_goalkeeper(events: pd.DataFrame) -> pd.DataFrame:
    if "position" not in events.columns:
        return events
    def _is_gk(pos) -> bool:
        if isinstance(pos, dict):
            return pos.get("id") == 1 or pos.get("name") == "Goalkeeper"
        if isinstance(pos, str):
            return pos == "Goalkeeper"
        return False
    return events[~events["position"].apply(_is_gk)].copy()


# StatsBomb position names, grouped into the lines that "gap between lines"
# is measured between. Goalkeepers (and forwards) are in neither group.
DEFENDER_POSITIONS = {
    "Left Center Back", "Right Center Back", "Center Back",
    "Left Back", "Right Back", "Left Wing Back", "Right Wing Back",
}


MIDFIELDER_POSITIONS = {
    "Left Defensive Midfield", "Right Defensive Midfield", "Center Defensive Midfield",
    "Left Center Midfield", "Right Center Midfield", "Center Attacking Midfield",
    "Left Midfield", "Right Midfield", "Left Attacking Midfield", "Right Attacking Midfield",
}


MIN_LINE_EVENTS = 5   # defensive actions needed from each line to place it


def _defensive_lines(def_events: pd.DataFrame):
    """
    (defender_line_x, midfield_line_x) in pitch units, in the team's own frame,
    or None when either line has too few actions to place.

    Each line is where that group of players actually makes its defensive
    actions: the mean x of the defensive events taken by defenders, and by
    midfielders. The gap between lines is the distance between the two.
    (Not a spread of event positions: the P60-P15 spread of all defensive
    events used previously gave 26-48m for every team, which is not a gap
    between two lines of players.)
    """
    if def_events.empty or "position" not in def_events.columns:
        return None
    names = def_events["position"].apply(lambda p: p.get("name") if isinstance(p, dict) else p)
    back = def_events[names.isin(DEFENDER_POSITIONS)]
    mid  = def_events[names.isin(MIDFIELDER_POSITIONS)]
    if len(back) < MIN_LINE_EVENTS or len(mid) < MIN_LINE_EVENTS:
        return None
    return float(back["loc_x"].mean()), float(mid["loc_x"].mean())


def _is_danger_corridor(x2: float, y2: float) -> bool:
    return (
        DANGER_CORRIDOR["x_min"] <= x2 <= DANGER_CORRIDOR["x_max"] and
        DANGER_CORRIDOR["y_min"] <= y2 <= DANGER_CORRIDOR["y_max"]
    )


def _classify_vertical(avg_x: float) -> str:
    if avg_x < 45.0: return "Low Block"
    if avg_x > 60.0: return "High Line"
    return "Mid Block"


# Width = mean |y - 40| of a team's defensive events (pitch units). Events spread
# evenly across the pitch score 20, and across 292 team-matches the real range
# is 13-24 (5th-95th percentile 17-22), so the old 15 / 27 cut-offs sat outside
# nearly all of it (99% "Balanced"). Calibrated to the bottom and top fifth
# (20th / 80th percentile): 17% Narrow / 68% Balanced / 15% Stretched.
HORIZONTAL_NARROW_MAX    = 18.7


HORIZONTAL_STRETCHED_MIN = 21.1


def _classify_horizontal(avg_y_offset: float) -> str:
    if avg_y_offset < HORIZONTAL_NARROW_MAX:    return "Narrow"
    if avg_y_offset > HORIZONTAL_STRETCHED_MIN: return "Stretched"
    return "Balanced"


def _classify_compactness(gap_m: float) -> str:
    if gap_m < 12.0: return "Compact"
    if gap_m > 18.0: return "Gapped"
    return "Standard"


def _get_press_breaking_passes(df: pd.DataFrame, team: str) -> pd.DataFrame:
    passes = df[
        (df["team"] == team) & (df["type"] == "Pass") &
        (df["period"] != 5) & (df["under_pressure"] == True)
    ].copy()
    passes = passes.dropna(subset=["location", "pass_end_location"])
    passes = passes[passes["pass_outcome"].isna()]
    passes["x1"] = passes["location"].apply(lambda l: float(l[0]))
    passes["y1"] = passes["location"].apply(lambda l: float(l[1]))
    passes["x2"] = passes["pass_end_location"].apply(lambda l: float(l[0]))
    passes["y2"] = passes["pass_end_location"].apply(lambda l: float(l[1]))
    passes["d_start"] = passes.apply(lambda r: euclidean_to_goal(r["x1"], r["y1"]), axis=1)
    passes["d_end"]   = passes.apply(lambda r: euclidean_to_goal(r["x2"], r["y2"]), axis=1)
    passes["delta_d"] = passes["d_start"] - passes["d_end"]
    return passes[passes["delta_d"] >= 15.0].copy()


def _exploit_finder_for_team(df: pd.DataFrame, team: str) -> dict:
    def_events = get_defensive_events(df, team)
    if def_events.empty:
        return {}

    lines = _defensive_lines(def_events)
    if lines is None:
        return {}
    def_line_x, mid_line_x = lines
    avg_x       = float(def_events["loc_x"].mean())
    avg_y_off   = float((def_events["loc_y"] - 40.0).abs().mean())
    gap_units   = mid_line_x - def_line_x
    gap_m       = round(gap_units * METERS, 1)
    comp_class  = _classify_compactness(gap_m)
    v_state     = _classify_vertical(avg_x)
    h_state     = _classify_horizontal(avg_y_off)
    ppda        = compute_ppda(df, team)
    press_class = classify_ppda(ppda)
    false_hl    = (v_state == "High Line" and press_class in ["Passive / Low Press", "Moderate Press"])
    genuine_hl  = (v_state == "High Line" and press_class == "Aggressive Press")

    if false_hl:
        risk_label = "⚠ FALSE HIGH LINE — HIGH RISK"
        risk_color = "#ef4444"
        risk_desc  = (
            f"{team} sit {round(avg_x * METERS, 1)}m up the pitch (High Line) "
            f"but press with only moderate-to-passive intensity (PPDA {ppda}). "
            f"The line is exposed to balls in behind with no press to compensate. "
            f"A well-organised opponent will exploit this ruthlessly.")
    elif v_state == "High Line" and genuine_hl:
        risk_label = "Genuine High Press"; risk_color = "#22c55e"
        risk_desc  = (f"{team}'s high line (avg {round(avg_x * METERS, 1)}m) is backed by "
                      f"aggressive pressing (PPDA {ppda}). Coherent and dangerous — "
                      f"but space in behind remains the structural vulnerability.")
    elif comp_class == "Gapped" and h_state == "Narrow":
        risk_label = "⚠ HIDDEN VERTICAL GAP — MEDIUM RISK"; risk_color = "#f59e0b"
        risk_desc  = (f"{team} appear narrow horizontally, but have a {gap_m}m vertical gap "
                      f"between defensive ({round(def_line_x * METERS, 1)}m) and midfield "
                      f"({round(mid_line_x * METERS, 1)}m) lines. A runner from deep or dropped "
                      f"No.10 will find space between the lines.")
    elif comp_class == "Gapped":
        risk_label = "⚠ STRUCTURAL GAP BETWEEN LINES"; risk_color = "#f59e0b"
        risk_desc  = (f"A {gap_m}m gap between {team}'s defensive and midfield lines. "
                      f"The 'space between' is wide open — creative midfielders will operate freely here.")
    elif comp_class == "Compact" and h_state == "Narrow":
        risk_label = "Defensively Solid"; risk_color = "#22c55e"
        risk_desc  = (f"{team} are tight both vertically ({gap_m}m) and horizontally (Narrow). "
                      f"Very difficult to break down through the center.")
    else:
        risk_label = "Standard Defensive Shape"; risk_color = "#6b7280"
        risk_desc  = f"{team} show a standard defensive structure with no exceptional vulnerabilities flagged."

    return {
        "team": team, "def_line_x_u": round(def_line_x, 1),
        "mid_line_x_u": round(mid_line_x, 1),
        "def_line_m": round(def_line_x * METERS, 1),
        "mid_line_m": round(mid_line_x * METERS, 1),
        "avg_line_m": round(avg_x * METERS, 1),
        "gap_m": gap_m, "comp_class": comp_class,
        "v_state": v_state, "h_state": h_state,
        "ppda": ppda, "press_class": press_class,
        "false_hl": false_hl, "risk_label": risk_label,
        "risk_color": risk_color, "risk_desc": risk_desc,
        "h_offset_u": round(avg_y_off, 2),
        "n_events": len(def_events),
    }


def _get_progressive_passes(df: pd.DataFrame, team: str) -> pd.DataFrame:
    """Returns all completed progressive passes for a team with coordinates."""
    passes = df[
        (df["team"] == team) & (df["type"] == "Pass") & (df["period"] != 5)
    ].copy()
    passes = passes.dropna(subset=["location", "pass_end_location"])
    passes = passes[passes["pass_outcome"].isna()]

    passes["x1"] = passes["location"].apply(lambda l: float(l[0]))
    passes["y1"] = passes["location"].apply(lambda l: float(l[1]))
    passes["x2"] = passes["pass_end_location"].apply(lambda l: float(l[0]))
    passes["y2"] = passes["pass_end_location"].apply(lambda l: float(l[1]))

    passes["d_start"] = passes.apply(lambda r: euclidean_to_goal(r["x1"], r["y1"]), axis=1)
    passes["d_end"]   = passes.apply(lambda r: euclidean_to_goal(r["x2"], r["y2"]), axis=1)
    passes["delta_d"] = passes["d_start"] - passes["d_end"]

    def _is_progressive(row) -> bool:
        x1, x2, dd = row["x1"], row["x2"], row["delta_d"]
        if x1 <= 60 and x2 <= 60:   return dd > 30
        if x1 <= 60 and x2 > 60:    return dd > 15
        if x1 > 60:                  return dd > 10
        return False

    passes["is_progressive"] = passes.apply(_is_progressive, axis=1)
    passes["danger"] = passes.apply(lambda r: _is_danger_corridor(r["x2"], r["y2"]), axis=1)

    return passes[passes["is_progressive"]].copy()


def _danger_map_for_team(df: pd.DataFrame, team: str) -> dict:
    prog = _get_progressive_passes(df, team)
    if prog.empty:
        return {"team": team, "total_prog": 0, "danger_count": 0,
                "danger_pct": 0, "avg_gain_m": 0.0,
                "efficiency_class": "No data", "efficiency_color": "#6b7280",
                "verdict": f"No progressive pass data found for {team}.",
                "all_x1": [], "all_y1": [], "all_x2": [], "all_y2": [],
                "danger_x1": [], "danger_y1": [], "danger_x2": [], "danger_y2": []}

    total_prog   = len(prog)
    danger_count = int(prog["danger"].sum())
    danger_pct   = round((danger_count / total_prog) * 100) if total_prog > 0 else 0
    avg_gain_m   = round(float(prog["delta_d"].mean()) * METERS, 1)

    if danger_pct >= 35:
        eff_class = "High Clinical Efficiency"
        eff_color = "#22c55e"
        verdict   = (f"{team} were clinically efficient — {danger_pct}% of progressive passes "
                     f"arrived in the danger corridor ({danger_count}/{total_prog}). "
                     f"Every 3 forward moves created a genuine threat.")
    elif danger_pct >= 20:
        eff_class = "Moderate Clinical Efficiency"
        eff_color = "#f59e0b"
        verdict   = (f"{team} progressed the ball effectively but conversion to danger was moderate — "
                     f"only {danger_pct}% of {total_prog} progressive passes reached the danger corridor. "
                     f"The opponent's block absorbed most of the volume.")
    else:
        eff_class = "Low Clinical Efficiency"
        eff_color = "#ef4444"
        verdict   = (f"{team} moved the ball forward ({total_prog} progressive passes, avg {avg_gain_m}m gain) "
                     f"but only {danger_pct}% arrived in a genuine danger zone. "
                     f"Progression was happening — it just wasn't threatening.")

    return {
        "team":             team,
        "total_prog":       total_prog,
        "danger_count":     danger_count,
        "danger_pct":       danger_pct,
        "avg_gain_m":       avg_gain_m,
        "efficiency_class": eff_class,
        "efficiency_color": eff_color,
        "verdict":          verdict,
        "all_x1":     prog["x1"].tolist(),
        "all_y1":     prog["y1"].tolist(),
        "all_x2":     prog["x2"].tolist(),
        "all_y2":     prog["y2"].tolist(),
        "danger_x1":  prog[prog["danger"]]["x1"].tolist(),
        "danger_y1":  prog[prog["danger"]]["y1"].tolist(),
        "danger_x2":  prog[prog["danger"]]["x2"].tolist(),
        "danger_y2":  prog[prog["danger"]]["y2"].tolist(),
    }


# Share of a team's completed progressive passes that start in the wide channels
# (|y-40| > 20). Over 292 team-matches it runs 26-59% (median 42%, 90th
# percentile 52%), so the old 60% cut-off could never be reached: the
# "forced wide" verdict fired for 0% of teams. Set at the 90th percentile,
# so only the clear outliers are called out (10.6%).
FORCED_WIDE_MIN    = 52


FORCED_WIDE_MARGIN = 10   # the other team must be this many points less wide


def _get_progressive_attempts(df: pd.DataFrame, team: str) -> pd.DataFrame:
    passes = df[
        (df["team"] == team) & (df["type"] == "Pass") & (df["period"] != 5)
    ].copy()
    passes = passes.dropna(subset=["location", "pass_end_location"])
    passes["x1"] = passes["location"].apply(lambda l: float(l[0]))
    passes["y1"] = passes["location"].apply(lambda l: float(l[1]))
    passes["x2"] = passes["pass_end_location"].apply(lambda l: float(l[0]))
    passes["y2"] = passes["pass_end_location"].apply(lambda l: float(l[1]))
    passes["dx"] = passes["x2"] - passes["x1"]
    passes = passes[passes["dx"] > 5].copy()
    passes["completed"]  = passes["pass_outcome"].isna()
    passes["is_wide"]    = (passes["y1"] - 40).abs() > 20
    passes["stall_zone"] = passes["x1"].apply(
        lambda x: "Defensive Third" if x < 40 else ("Middle Third" if x < 80 else "Final Third"))
    return passes


def _progress_trap_for_team(df: pd.DataFrame, team: str, opponent: str) -> dict:
    attempts = _get_progressive_attempts(df, team)
    if attempts.empty:
        return {"team": team, "total_attempts": 0, "stall_rate": 0,
                "primary_stall_zone": "No data", "primary_stall_n": 0,
                "completed_count": 0, "stalled_count": 0,
                "forced_wide_pct": 0, "block_x_u": 52.0,
                "block_depth_m": 0.0, "block_label": "—", "block_color": "#6b7280",
                "verdict": f"No data for {team}.",
                "stall_x": [], "stall_y": [], "comp_x1": [], "comp_y1": [], "comp_x2": [], "comp_y2": []}

    total_att  = len(attempts)
    completed  = attempts[attempts["completed"]]
    stalled    = attempts[~attempts["completed"]]
    stall_rate = round((len(stalled) / total_att) * 100) if total_att > 0 else 0

    if not stalled.empty:
        stall_zone_counts  = stalled["stall_zone"].value_counts()
        primary_stall_zone = stall_zone_counts.index[0]
        primary_stall_n    = int(stall_zone_counts.iloc[0])
    else:
        primary_stall_zone, primary_stall_n = "None", 0

    forced_wide_pct = round((int(completed["is_wide"].sum()) / len(completed)) * 100) if not completed.empty else 0

    # Block height = where the opponent defends on average: the same mean x of
    # defensive events the Exploit Finder reports as avg_line_m, so one team has
    # one number across templates. (This was the 15th percentile of those
    # events, i.e. by construction the deepest ones: 37% clearances although
    # clearances are 10% of defensive events, and ~12m for every team.)
    opp_def      = get_defensive_events(df, opponent)
    block_x_u    = float(opp_def["loc_x"].mean()) if not opp_def.empty else 52.0
    block_depth_m = round(block_x_u * METERS, 1)

    if block_x_u < 35:
        block_label, block_color = "Extreme Low Block", "#ef4444"
    elif block_x_u < 45:
        block_label, block_color = "Deep Block", "#f59e0b"
    elif block_x_u < 55:
        block_label, block_color = "Mid Block", "#6b7280"
    else:
        block_label, block_color = "High Block / Pressing", "#22c55e"

    if stall_rate >= 50 and primary_stall_zone == "Defensive Third":
        verdict = (f"{team} were pinned in their own half — {stall_rate}% of forward passes stalled "
                   f"in the defensive third. The opponent's press suffocated their build-up.")
    elif stall_rate >= 50 and primary_stall_zone == "Final Third":
        verdict = (f"{team} progressed into the final third but hit a wall — {stall_rate}% stall rate. "
                   f"The opponent's {block_label} ({block_depth_m}m) absorbed the volume.")
    elif forced_wide_pct >= FORCED_WIDE_MIN:
        verdict = (f"{team} were consistently forced wide — {forced_wide_pct}% of completed progressions "
                   f"went through the wide corridor. The central route was shut down.")
    elif stall_rate < 30:
        verdict = (f"{team} progressed efficiently — only {stall_rate}% stall rate. "
                   f"The {block_label} at {block_depth_m}m didn't prevent forward movement.")
    else:
        verdict = (f"{team}: {stall_rate}% stall rate, primarily {primary_stall_zone}. "
                   f"{block_label} at {block_depth_m}m. {forced_wide_pct}% forced wide.")

    return {
        "team": team, "total_attempts": total_att,
        "completed_count": len(completed), "stalled_count": len(stalled),
        "stall_rate": stall_rate, "primary_stall_zone": primary_stall_zone,
        "primary_stall_n": primary_stall_n, "forced_wide_pct": forced_wide_pct,
        "block_x_u": round(block_x_u, 1), "block_depth_m": block_depth_m,
        "block_label": block_label, "block_color": block_color, "verdict": verdict,
        "stall_x": stalled["x1"].tolist(), "stall_y": stalled["y1"].tolist(),
        "comp_x1": completed["x1"].tolist(), "comp_y1": completed["y1"].tolist(),
        "comp_x2": completed["x2"].tolist(), "comp_y2": completed["y2"].tolist(),
    }
