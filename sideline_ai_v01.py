# =============================================================================
# sideline_ai_v01.py
# Sideline.ai — Tactical Reasoning Engine | v0.1 Proof of Concept
# Match: Argentina vs France | 2022 FIFA World Cup Final | ID: 3869685
# =============================================================================

import pandas as pd
import math
import json
import os
from typing import Optional

# =============================================================================
# CONFIGURATION
# =============================================================================

MATCH_ID = 3869685

DEFENSIVE_EVENT_TYPES = [
    "Pressure",
    "Interception",
    "Block",
    "Duel",
    "Clearance",
]

# Recalibrated against 2022 World Cup data (4 matches, 8 team-observations)
# Old thresholds were club-football baselines — completely wrong for international.
# New: P10 = Low Block ceiling, P90 = High Line floor.
# Morocco (40.25u) → Low Block ✓  Spain (65.67u) → High Line ✓
VERTICAL_THRESHOLDS = {
    "low_block_max": 45.0,
    "high_line_min": 60.0,
}

# Recalibrated — horizontal offset barely varies at World Cup level (18.9–22.4u).
# Thresholds compressed to match actual distribution.
# Note: width is a weak signal at this level — shown in UI but not a primary verdict.
HORIZONTAL_THRESHOLDS = {
    "narrow_max": 19.5,
    "stretched_min": 22.0,
}

# PPDA thresholds — recalibrated against 2022 World Cup data.
# Club football baselines (< 8 aggressive) were far too loose — every WC team
# would have qualified as "Aggressive." New thresholds anchored to P25/P75.
# Argentina vs Saudi Arabia: ARG at 1.72 (most aggressive) ✓
# Spain vs Costa Rica: Spain at 4.68 (passive) → False High Line fires ✓
PPDA_THRESHOLDS = {
    "aggressive_max": 2.5,
    "passive_min":    4.4,
}

# =============================================================================
# OUTPUT MODE
# Controls verbosity of all print functions.
#   "beginner" — plain English narrative only, technical receipt hidden.
#   "analyst"  — full output including raw coordinates, thresholds, receipts.
# Streamlit UI (Task 5) will expose this as a radio button toggle.
# =============================================================================

OUTPUT_MODE_BEGINNER = "beginner"
OUTPUT_MODE_ANALYST  = "analyst"


def should_show_receipt(output_mode: str) -> bool:
    """Returns True if the technical receipt should be printed."""
    return output_mode == OUTPUT_MODE_ANALYST

# =============================================================================
# PERIOD MAPPING
# StatsBomb period codes → human-readable labels.
# Period 5 (Penalties) intentionally excluded — no positional data.
# =============================================================================

PERIOD_LABELS = {
    1: "1st Half       (0–45')",
    2: "2nd Half       (45–90')",
    3: "Extra Time 1st (90–105')",
    4: "Extra Time 2nd (105–120')",
}

# =============================================================================
# UNIT CONVERSION
# Source: StatsBomb spec — 1 pitch unit = 0.875 metres
# =============================================================================

METERS_PER_UNIT = 0.875
YARDS_PER_UNIT  = METERS_PER_UNIT * 1.09361

def u_to_m(units: float) -> float:
    """Convert units to metres. Minimum display value 0.1m to avoid '0.0m' in boundary notes."""
    result = round(units * METERS_PER_UNIT, 1)
    return max(result, 0.1)

def u_to_yd(units: float) -> float:
    return round(units * YARDS_PER_UNIT, 1)

def fmt_dist(units: float) -> str:
    return f"{u_to_m(units)}m ({u_to_yd(units)}yd)"

# =============================================================================
# PLAIN ENGLISH TRANSLATORS
# =============================================================================

VERTICAL_DESCRIPTIONS = {
    "Low Block": (
        "Parking the Bus",
        "defending deep in their own half, inviting the opponent to attack "
        "and looking to hit on the counter."
    ),
    "Mid Block": (
        "Controlled Defending",
        "sitting in a structured mid-field shape — neither pressing high "
        "nor retreating deep. A disciplined, standard defensive posture."
    ),
    "High Line": (
        "Aggressive Press",
        "defending far up the pitch, pressing the opponent aggressively "
        "in their own half. High risk, high reward."
    ),
}

HORIZONTAL_DESCRIPTIONS = {
    "Narrow": (
        "Compact & Central",
        "packed tightly through the middle of the pitch, forcing the "
        "opponent wide and protecting the central corridor."
    ),
    "Balanced": (
        "Covering the Half-Spaces",
        "maintaining a balanced width — neither completely central nor "
        "stretched wide. A standard, organised defensive width."
    ),
    "Stretched": (
        "Vulnerable Down the Middle",
        "spread too wide across the pitch, leaving gaps in the center "
        "that a sharp passing team can exploit."
    ),
}

PROGRESSION_ZONE_DESCRIPTIONS = {
    "30-Rule": (
        "Deep Build-up",
        "passes that broke out of their own defensive third under pressure "
        "— the hardest type of progression to achieve."
    ),
    "15-Rule": (
        "Midfield Transition",
        "passes that crossed the halfway line and carried the ball into "
        "the opponent's territory."
    ),
    "10-Rule": (
        "Final Third Penetration",
        "passes already inside the opponent's half that pushed closer "
        "to the box — the most dangerous zone."
    ),
}

def describe_stability(boundary_m: float, direction: str, target_state: str) -> str:
    if boundary_m < 5:
        return (f"Very unstable — just {boundary_m}m from being "
                f"reclassified as '{target_state}'.")
    elif boundary_m < 12:
        return (f"Moderately stable — {boundary_m}m away from "
                f"dropping into '{target_state}' territory.")
    else:
        return (f"Firmly established — {boundary_m}m clear of the "
                f"'{target_state}' threshold.")

# =============================================================================
# STAGE 1 — INGESTION
# =============================================================================

# =============================================================================
# DATA PROVIDER CONFIGURATION
#
# DATA_PROVIDER controls which source ingest_match_events() pulls from.
# Set via environment variable:
#   DATA_PROVIDER=statsbomb   (default — uses statsbombpy open data)
#   DATA_PROVIDER=sportradar  (live feed — expects normalised JSON at
#                              SPORTRADAR_EVENTS_DIR/{match_id}.json)
#   DATA_PROVIDER=file        (any pre-normalised JSON file at
#                              EVENTS_FILE_PATH env var)
#
# Sportradar JSON must be pre-normalised to StatsBomb coordinate schema
# (120x80 pitch, location as [x, y] list) by the adapter in
# ingest_sportradar_json() below before it reaches this pipeline.
# =============================================================================

DATA_PROVIDER         = os.getenv("DATA_PROVIDER", "statsbomb")
SPORTRADAR_EVENTS_DIR = os.getenv("SPORTRADAR_EVENTS_DIR", "./sportradar_events")
EVENTS_FILE_PATH      = os.getenv("EVENTS_FILE_PATH", "")


def _normalise_sportradar_event(raw: dict) -> dict:
    """
    Translates a single Sportradar Soccer v4 Extended Timeline event
    into the StatsBomb column schema expected by this pipeline.

    Sportradar → StatsBomb field mapping:
        type.name        → type
        period           → period  (1-4, same convention)
        clock.match_time → minute  (integer minutes)
        player.name      → player  (nested dict with "name")
        competitor       → team    (nested dict with "name")
        venue_coordinates→ location ([x_pct * 1.2, y_pct * 0.8] scaled to 120x80)
        qualifier        → pass_outcome, pass_end_location (see notes)

    Coordinate scaling:
        Sportradar uses percentage-of-pitch coordinates (0-100, 0-100).
        We scale to StatsBomb units: x * 1.2, y * 0.8 → fits 120x80.

    Pass end location:
        Sportradar's F24-equivalent feed includes pass end coordinates
        in the qualifier array under "type": "PassEndCoordinates".
        We extract and scale those here.

    Returns a dict compatible with pd.DataFrame row construction.
    """
    coords     = raw.get("venue_coordinates", {}) or {}
    raw_x      = float(coords.get("x", 0))
    raw_y      = float(coords.get("y", 0))
    loc_x      = raw_x * 1.2   # scale 0-100 → 0-120
    loc_y      = raw_y * 0.8   # scale 0-100 → 0-80

    event_type = (raw.get("type") or {}).get("name", "Unknown")
    team_name  = (raw.get("competitor") or {}).get("name", "")
    player     = {"name": (raw.get("player") or {}).get("name", "")}

    clock       = raw.get("clock") or {}
    minute_str  = clock.get("match_time", "0:00")
    try:
        minute = int(str(minute_str).split(":")[0])
    except (ValueError, IndexError):
        minute = 0

    # Pass end location from qualifiers
    pass_end = None
    pass_outcome = None
    qualifiers = raw.get("qualifiers") or []
    for q in qualifiers:
        q_type = (q.get("type") or {}).get("name", "")
        if q_type == "PassEndCoordinates":
            eq = q.get("value", "")
            try:
                parts = str(eq).split(",")
                ex = float(parts[0]) * 1.2
                ey = float(parts[1]) * 0.8
                pass_end = [ex, ey]
            except Exception:
                pass
        if q_type == "Incomplete":
            pass_outcome = "Incomplete"

    return {
        "id":                 raw.get("id", ""),
        "index":              raw.get("id", 0),
        "period":             int(raw.get("period", 1)),
        "minute":             minute,
        "second":             0,
        "timestamp":          f"00:{str(minute).zfill(2)}:00.000",
        "type":               event_type,
        "team":               team_name,
        "player":             player,
        "location":           [loc_x, loc_y],
        "pass_end_location":  pass_end,
        "pass_outcome":       pass_outcome,
        "shot_outcome":       None,
    }


def ingest_sportradar_json(match_id: int) -> pd.DataFrame:
    """
    Loads a Sportradar Soccer v4 Extended Timeline JSON file,
    normalises every event to the StatsBomb schema, and returns
    a DataFrame the pipeline can process unchanged.

    Expected file path: {SPORTRADAR_EVENTS_DIR}/{match_id}.json

    The JSON must have the structure returned by Sportradar's
    Sport Event Extended Timeline endpoint:
        { "sport_event_status": { "timeline": [ ...events... ] } }
    """
    fpath = os.path.join(SPORTRADAR_EVENTS_DIR, f"{match_id}.json")
    if not os.path.exists(fpath):
        raise FileNotFoundError(
            f"Sportradar events file not found: {fpath}\n"
            f"Download from Sportradar API and save to {SPORTRADAR_EVENTS_DIR}/"
        )
    with open(fpath, encoding="utf-8") as f:
        data = json.load(f)

    raw_events = (
        data.get("sport_event_status", {})
            .get("timeline", [])
    )
    if not raw_events:
        raise ValueError(f"No timeline events found in {fpath}")

    rows = [_normalise_sportradar_event(e) for e in raw_events]
    df   = pd.DataFrame(rows)
    print(f"      ✓ Sportradar: {len(df):,} events normalised from {fpath}")
    return df


def ingest_match_events(
    match_id: int,
    provider: Optional[str] = None,
) -> pd.DataFrame:
    """
    Provider-agnostic event ingestion.

    Args:
        match_id — StatsBomb match ID (for StatsBomb/file modes)
                   or Sportradar sport_event_id (for sportradar mode)
        provider — override DATA_PROVIDER env var if passed directly

    Provider behaviour:
        "statsbomb"  — pulls from statsbombpy (open data or credentialed API)
        "sportradar" — loads pre-downloaded JSON from SPORTRADAR_EVENTS_DIR
        "file"       — loads a single JSON file at EVENTS_FILE_PATH

    The pipeline downstream is completely unchanged regardless of provider.
    All normalisation happens here so a single DataFrame with the correct
    StatsBomb column schema exits this function every time.
    """
    active_provider = provider or DATA_PROVIDER
    print(f"[1/5] Ingesting events for match ID: {match_id} "
          f"(provider: {active_provider})...")

    if active_provider == "statsbomb":
        from statsbombpy import sb
        events = sb.events(match_id=match_id)

    elif active_provider == "sportradar":
        events = ingest_sportradar_json(match_id)

    elif active_provider == "file":
        if not EVENTS_FILE_PATH or not os.path.exists(EVENTS_FILE_PATH):
            raise FileNotFoundError(
                f"EVENTS_FILE_PATH not set or file missing: {EVENTS_FILE_PATH}"
            )
        with open(EVENTS_FILE_PATH, encoding="utf-8") as f:
            raw = json.load(f)
        # Accept either a list of events or a Sportradar-style wrapper
        if isinstance(raw, list):
            events = pd.DataFrame(raw)
        else:
            events = ingest_sportradar_json.__wrapped__(raw)

    else:
        raise ValueError(
            f"Unknown DATA_PROVIDER: '{active_provider}'. "
            f"Valid options: statsbomb, sportradar, file"
        )

    print(f"      ✓ {len(events):,} total events loaded.")
    return events

# =============================================================================
# STAGE 2 — FILTRATION
# =============================================================================

def filter_defensive_events(events: pd.DataFrame) -> pd.DataFrame:
    print(f"[2/5] Filtering to defensive event types: {DEFENSIVE_EVENT_TYPES}...")
    mask = events["type"].isin(DEFENSIVE_EVENT_TYPES)
    defensive = events[mask].copy()
    defensive = defensive[defensive["period"] != 5]
    defensive = defensive.dropna(subset=["location"])
    print(f"      ✓ {len(defensive):,} defensive events retained.")
    return defensive

# =============================================================================
# STAGE 3 — TRANSFORMATION
# =============================================================================

def transform_coordinates(defensive: pd.DataFrame) -> pd.DataFrame:
    print("[3/5] Transforming coordinates and computing y_offset...")
    defensive["location_x"] = defensive["location"].apply(lambda loc: float(loc[0]))
    defensive["location_y"] = defensive["location"].apply(lambda loc: float(loc[1]))
    defensive["y_offset"]   = (defensive["location_y"] - 40.0).abs()
    print(f"      ✓ location_x, location_y, y_offset columns created.")
    return defensive

# =============================================================================
# STAGE 4 — AGGREGATION
# =============================================================================

def aggregate_by_team(defensive: pd.DataFrame) -> pd.DataFrame:
    print("[4/5] Aggregating metrics by team...")
    summary = (
        defensive
        .groupby("team")
        .agg(
            avg_defensive_x=("location_x", "mean"),
            avg_y_offset=("location_y", lambda y: (y - 40.0).abs().mean()),
            event_count=("location_x", "count"),
        )
        .reset_index()
    )
    print(f"      ✓ Aggregated {len(summary)} teams.")
    return summary

def aggregate_by_team_and_period(defensive: pd.DataFrame) -> pd.DataFrame:
    period_summary = (
        defensive
        .groupby(["team", "period"])
        .agg(
            avg_defensive_x=("location_x", "mean"),
            avg_y_offset=("location_y", lambda y: (y - 40.0).abs().mean()),
            event_count=("location_x", "count"),
        )
        .reset_index()
    )
    period_summary["period_label"] = period_summary["period"].map(PERIOD_LABELS)
    return period_summary

# =============================================================================
# STAGE 5 — LOGIC GATES
# =============================================================================

def classify_vertical(avg_x: float) -> str:
    if avg_x < VERTICAL_THRESHOLDS["low_block_max"]:
        return "Low Block"
    elif avg_x > VERTICAL_THRESHOLDS["high_line_min"]:
        return "High Line"
    else:
        return "Mid Block"

def classify_horizontal(avg_y_offset: float) -> str:
    if avg_y_offset < HORIZONTAL_THRESHOLDS["narrow_max"]:
        return "Narrow"
    elif avg_y_offset > HORIZONTAL_THRESHOLDS["stretched_min"]:
        return "Stretched"
    else:
        return "Balanced"

def classify_ppda(ppda: float) -> str:
    if ppda < PPDA_THRESHOLDS["aggressive_max"]:
        return "Aggressive Press"
    elif ppda > PPDA_THRESHOLDS["passive_min"]:
        return "Passive / Low Press"
    else:
        return "Moderate Press"

def apply_logic_gates(summary: pd.DataFrame) -> pd.DataFrame:
    print("[5/5] Applying logic gates...")
    summary["vertical_state"]   = summary["avg_defensive_x"].apply(classify_vertical)
    summary["horizontal_state"] = summary["avg_y_offset"].apply(classify_horizontal)
    print("      ✓ Tactical states classified.")
    return summary

# =============================================================================
# RECEIPT HELPERS — Boundary Proximity (internal, feeds plain-English output)
# =============================================================================

def vertical_boundary_metres(avg_x: float, state: str) -> tuple[float, str]:
    low_max  = VERTICAL_THRESHOLDS["low_block_max"]
    high_min = VERTICAL_THRESHOLDS["high_line_min"]
    if state == "Low Block":
        return u_to_m(low_max - avg_x), "Mid Block"
    elif state == "High Line":
        return u_to_m(avg_x - high_min), "Mid Block"
    else:
        to_low  = avg_x - low_max
        to_high = high_min - avg_x
        if to_low < to_high:
            return u_to_m(to_low), "Low Block"
        else:
            return u_to_m(to_high), "High Line"

def horizontal_boundary_metres(avg_offset: float, state: str) -> tuple[float, str]:
    narrow_max    = HORIZONTAL_THRESHOLDS["narrow_max"]
    stretched_min = HORIZONTAL_THRESHOLDS["stretched_min"]
    if state == "Narrow":
        return u_to_m(narrow_max - avg_offset), "Balanced"
    elif state == "Stretched":
        return u_to_m(avg_offset - stretched_min), "Balanced"
    else:
        to_narrow    = avg_offset - narrow_max
        to_stretched = stretched_min - avg_offset
        if to_narrow < to_stretched:
            return u_to_m(to_narrow), "Narrow"
        else:
            return u_to_m(to_stretched), "Stretched"

# =============================================================================
# STAGE 6 — OUTPUT: TACTICAL REPORT (Plain English)
# =============================================================================

def print_tactical_report(
    summary: pd.DataFrame,
    period_summary: pd.DataFrame,
    output_mode: str = OUTPUT_MODE_ANALYST,
) -> None:
    divider = "=" * 68

    print(f"\n{divider}")
    print("  SIDELINE.AI — MATCH ANALYSIS")
    print(f"  Argentina vs France | 2022 World Cup Final")
    print(divider)

    for _, row in summary.iterrows():
        team       = row["team"]
        avg_x      = row["avg_defensive_x"]
        avg_offset = row["avg_y_offset"]
        v_state    = row["vertical_state"]
        h_state    = row["horizontal_state"]
        n_events   = int(row["event_count"])

        v_label, v_desc = VERTICAL_DESCRIPTIONS[v_state]
        h_label, h_desc = HORIZONTAL_DESCRIPTIONS[h_state]

        v_gap_m, v_nearest = vertical_boundary_metres(avg_x, v_state)
        h_gap_m, h_nearest = horizontal_boundary_metres(avg_offset, h_state)

        team_periods = period_summary[
            period_summary["team"] == team
        ].sort_values("period")

        print(f"\n  ── {team.upper()} ──────────────────────────────────────")
        print(f"\n  DEFENSIVE SHAPE VERDICT")
        print(f"  Setup     : {v_label}")
        print(f"  Width     : {h_label}")

        print(f"\n  WHAT THIS MEANS")
        print(f"  {team} were {v_desc}")
        print(f"  In terms of width, they were {h_desc}")

        print(f"\n  HOW STABLE WAS THIS SHAPE?")
        print(f"  Depth : {describe_stability(v_gap_m, 'depth', v_nearest)}")
        print(f"  Width : {describe_stability(h_gap_m, 'width', h_nearest)}")
        print(f"  (Based on {n_events} recorded defensive actions)")

        print(f"\n  HOW DID THE SHAPE EVOLVE?")
        prev_v, prev_h = None, None
        for _, p in team_periods.iterrows():
            label    = p["period_label"]
            px       = p["avg_defensive_x"]
            po       = p["avg_y_offset"]
            pn       = int(p["event_count"])
            pv       = classify_vertical(px)
            ph       = classify_horizontal(po)
            pv_label = VERTICAL_DESCRIPTIONS[pv][0]
            ph_label = HORIZONTAL_DESCRIPTIONS[ph][0]

            change_flag = ""
            if prev_v is not None and (pv != prev_v or ph != prev_h):
                change_flag = "  ⚠  Tactical shift detected"

            print(f"  {label}  →  {pv_label} | {ph_label}"
                  f"  (n={pn}){change_flag}")
            prev_v, prev_h = pv, ph

        periods_present = set(team_periods["period"].tolist())
        if not {3, 4}.intersection(periods_present):
            print(f"  (Match ended in regulation — no extra time data)")

    if should_show_receipt(output_mode):
        print(f"\n{divider}\n")
        print("  [TECHNICAL RECEIPT — for reference only]")
        print(f"  Pitch: 120×80 units | 1u = {METERS_PER_UNIT}m = {round(YARDS_PER_UNIT, 3)}yd")
        for _, row in summary.iterrows():
            print(f"  {row['team']}: "
                  f"Avg X = {row['avg_defensive_x']:.1f}u, "
                  f"Avg Y-Offset = {row['avg_y_offset']:.1f}u")
    print(f"\n{divider}\n")

# =============================================================================
# PROGRESSION ANALYSIS (Geometry of Progression — 30-15-10 Rule)
# =============================================================================

GOAL = (120.0, 40.0)

def euclidean_to_goal(x: float, y: float) -> float:
    return math.sqrt((GOAL[0] - x) ** 2 + (GOAL[1] - y) ** 2)

def classify_progressive(x1: float, x2: float, delta_d: float) -> tuple[bool, str]:
    if x1 <= 60 and x2 <= 60:
        return (delta_d > 30, "30-Rule")
    elif x1 <= 60 and x2 > 60:
        return (delta_d > 15, "15-Rule")
    elif x1 > 60:
        return (delta_d > 10, "10-Rule")
    return (False, "None")

def run_progression_analysis(events: pd.DataFrame) -> pd.DataFrame:
    print("\n[PROGRESSION] Filtering completed pass events...")
    passes = events[events["type"] == "Pass"].copy()
    passes = passes[passes["period"] != 5]
    passes = passes.dropna(subset=["location", "pass_end_location"])
    passes = passes[passes["pass_outcome"].isna()]
    print(f"             ✓ {len(passes):,} completed passes retained.")

    passes["x1"] = passes["location"].apply(lambda l: float(l[0]))
    passes["y1"] = passes["location"].apply(lambda l: float(l[1]))
    passes["x2"] = passes["pass_end_location"].apply(lambda l: float(l[0]))
    passes["y2"] = passes["pass_end_location"].apply(lambda l: float(l[1]))

    passes["d_start"] = passes.apply(
        lambda r: euclidean_to_goal(r["x1"], r["y1"]), axis=1)
    passes["d_end"] = passes.apply(
        lambda r: euclidean_to_goal(r["x2"], r["y2"]), axis=1)
    passes["delta_d"] = passes["d_start"] - passes["d_end"]

    results = passes.apply(
        lambda r: classify_progressive(r["x1"], r["x2"], r["delta_d"]), axis=1)
    passes["is_progressive"] = results.apply(lambda t: t[0])
    passes["prog_rule"]      = results.apply(lambda t: t[1])

    progressive = passes[passes["is_progressive"]]

    # Flag passes that entered the Danger Corridor
    progressive["danger_corridor"] = progressive.apply(
        lambda r: is_danger_corridor(r["x2"], r["y2"]), axis=1
    )

    summary = (
        progressive
        .groupby("team")
        .agg(
            progressive_pass_count=("is_progressive", "count"),
            avg_delta_d=("delta_d", "mean"),
            danger_corridor_count=("danger_corridor", "sum"),
        )
        .reset_index()
    )

    zone_counts = (
        progressive
        .groupby(["team", "prog_rule"])
        .size()
        .reset_index(name="count")
    )

    divider = "=" * 68
    print(f"\n{divider}")
    print("  SIDELINE.AI — ATTACKING EFFICIENCY REPORT")
    print(f"  Argentina vs France | 2022 World Cup Final")
    print(divider)

    for _, row in summary.iterrows():
        team          = row["team"]
        count         = int(row["progressive_pass_count"])
        avg_dd        = row["avg_delta_d"]
        avg_m         = u_to_m(avg_dd)
        danger_count  = int(row["danger_corridor_count"])
        danger_pct    = round((danger_count / count) * 100) if count > 0 else 0

        team_zones = zone_counts[zone_counts["team"] == team]
        zone_dict  = dict(zip(team_zones["prog_rule"], team_zones["count"]))

        deep  = zone_dict.get("30-Rule", 0)
        mid   = zone_dict.get("15-Rule", 0)
        final = zone_dict.get("10-Rule", 0)

        zone_max   = max(zone_dict, key=zone_dict.get) if zone_dict else "15-Rule"
        zone_label = PROGRESSION_ZONE_DESCRIPTIONS[zone_max][0]

        print(f"\n  ── {team.upper()} ──────────────────────────────────────")
        print(f"\n  PASSING PROGRESSION VERDICT")
        print(f"  Total Progressive Passes    : {count}")
        print(f"  Average Ground Gained       : {avg_m}m per pass")
        print(f"  Primary Mode                : {zone_label}")
        print(f"  Danger Corridor Entries     : {danger_count} passes ({danger_pct}% of progressions)")

        # Plain-English danger corridor interpretation
        if danger_pct >= 35:
            print(f"  → High clinical efficiency — more than 1 in 3 progressive")
            print(f"    passes arrived directly in a goal-threatening area.")
        elif danger_pct >= 20:
            print(f"  → Moderate clinical efficiency — roughly 1 in 5 progressive")
            print(f"    passes converted into genuine danger.")
        else:
            print(f"  → Low clinical efficiency — progression is happening but")
            print(f"    most of it isn't arriving in goal-threatening areas.")

        print(f"\n  WHERE DID THE PROGRESSION HAPPEN?")
        for rule, label_tuple in PROGRESSION_ZONE_DESCRIPTIONS.items():
            zone_name, zone_desc = label_tuple
            n   = zone_dict.get(rule, 0)
            pct = round((n / count) * 100) if count > 0 else 0
            print(f"\n  {zone_name} ({n} passes, {pct}% of total)")
            print(f"  These were {zone_desc}")

        print(f"\n  KEY INSIGHT")
        if danger_pct >= 35 and (final >= mid or mid >= deep):
            print(f"  {team} were not just progressing — they were progressing")
            print(f"  dangerously. {danger_pct}% of their advances arrived in the")
            print(f"  penalty area corridor, directly threatening goal.")
        elif final >= mid and final >= deep:
            print(f"  {team} were most dangerous in the final third — their "
                  f"progression was sharp and direct, consistently threatening "
                  f"the opponent's box.")
        elif mid >= final and mid >= deep:
            print(f"  {team} were primarily a midfield transition team — "
                  f"comfortable moving the ball into the opponent's half but "
                  f"with room to improve in the final third.")
        else:
            print(f"  {team} relied heavily on deep build-up play — breaking "
                  f"the first line of pressure from their own half, suggesting "
                  f"the opponent pressed them hard early.")

    print(f"\n{divider}\n")
    print("  [TECHNICAL RECEIPT — for reference only]")
    print(f"  Goal reference: G = (120, 40) | ΔD = Euclidean distance gained toward goal")
    print(f"  30-Rule: own half → own half, ΔD > 30u")
    print(f"  15-Rule: own half → opponent half, ΔD > 15u")
    print(f"  10-Rule: opponent half → opponent half, ΔD > 10u")
    print(f"\n{divider}\n")

    return summary


# =============================================================================
# DANGER CORRIDOR ENGINE
# Measures what % of progressive passes actually arrived in a goal-threatening
# area — separating productive progression from harmless ball recycling.
#
# Definition (StatsBomb 120×80 pitch):
#   x2 ∈ [88, 120]  — from edge of final third to goal line
#   y2 ∈ [18, 62]   — full penalty box width + central shooting lane
#
# This covers: shots from outside the box, balls into the penalty area,
# cutbacks, crosses into the six-yard box, and through balls to the striker.
# =============================================================================

DANGER_CORRIDOR = {
    "x_min": 88.0,
    "x_max": 120.0,
    "y_min": 18.0,
    "y_max": 62.0,
}


def is_danger_corridor(x2: float, y2: float) -> bool:
    """Returns True if pass end location falls inside the Danger Corridor."""
    return (
        DANGER_CORRIDOR["x_min"] <= x2 <= DANGER_CORRIDOR["x_max"] and
        DANGER_CORRIDOR["y_min"] <= y2 <= DANGER_CORRIDOR["y_max"]
    )

# =============================================================================
# PPDA ENGINE
# Measures pressing intensity — how aggressively a team hunts the ball
# in the opponent's own half.
#
# Formula:
#   PPDA = Opponent passes in their own half (x <= 60)
#          ÷ Your pressing actions in that same zone
#          (Tackles + Interceptions + Pressures where x <= 60)
#
# Lower PPDA = more aggressive press.
# Numerator uses ALL opponent pass attempts (including incomplete) —
# every attempt represents a possession moment the pressing team
# had the opportunity to disrupt.
# =============================================================================

# Fouls included — a tactical foul high up the pitch is an active pressing
# action designed to stop progression. Omitting it understates pressing intensity.
PPDA_PRESSING_ACTIONS = ["Tackle", "Interception", "Pressure", "Foul Committed"]

def compute_ppda_for_team(
    pressing_team: str,
    events: pd.DataFrame,
) -> tuple[float, int, int]:
    """
    Computes PPDA for one pressing team against its opponent.

    Returns:
        ppda          — the PPDA value (float, lower = more aggressive)
        opp_passes    — numerator: opponent passes in their own half
        press_actions — denominator: pressing team's actions in opponent's half
    """
    teams = events["team"].dropna().unique()
    opponent = [t for t in teams if t != pressing_team]
    if not opponent:
        return float("nan"), 0, 0
    opponent = opponent[0]

    # Unpack location x for all events (needed for zone filter)
    events = events.copy()
    events["loc_x"] = events["location"].apply(
        lambda l: float(l[0]) if isinstance(l, (list, tuple)) else float("nan")
    )

    # Numerator — ALL opponent pass attempts in their own half (x <= 60)
    # Includes incomplete passes — every attempt is a possession moment
    opp_passes_df = events[
        (events["team"] == opponent) &
        (events["type"] == "Pass") &
        (events["period"] != 5) &
        (events["loc_x"] <= 60)
    ]
    opp_passes = len(opp_passes_df)

    # Denominator — pressing team's Tackles, Interceptions, Pressures
    # in the opponent's own half (same zone: x <= 60)
    # Note: coordinates are team-normalised, so x <= 60 for the pressing
    # team's actions means they are acting in the opponent's build-up zone.
    press_df = events[
        (events["team"] == pressing_team) &
        (events["type"].isin(PPDA_PRESSING_ACTIONS)) &
        (events["period"] != 5) &
        (events["loc_x"] <= 60)
    ]
    press_actions = len(press_df)

    if press_actions == 0:
        return float("inf"), opp_passes, 0

    ppda = opp_passes / press_actions
    return round(ppda, 2), opp_passes, press_actions


def compute_ppda_by_period(
    pressing_team: str,
    events: pd.DataFrame,
) -> pd.DataFrame:
    """
    Computes PPDA per period for one pressing team.
    Returns a DataFrame with columns: period, period_label, ppda,
    opp_passes, press_actions, press_classification.
    """
    events = events.copy()
    events["loc_x"] = events["location"].apply(
        lambda l: float(l[0]) if isinstance(l, (list, tuple)) else float("nan")
    )

    teams    = events["team"].dropna().unique()
    opponent = [t for t in teams if t != pressing_team]
    if not opponent:
        return pd.DataFrame()
    opponent = opponent[0]

    rows = []
    for period in sorted(events["period"].dropna().unique()):
        if period == 5:
            continue
        period_events = events[events["period"] == period]

        opp_passes = len(period_events[
            (period_events["team"] == opponent) &
            (period_events["type"] == "Pass") &
            (period_events["loc_x"] <= 60)
        ])

        press_actions = len(period_events[
            (period_events["team"] == pressing_team) &
            (period_events["type"].isin(PPDA_PRESSING_ACTIONS)) &
            (period_events["loc_x"] <= 60)
        ])

        ppda = round(opp_passes / press_actions, 2) if press_actions > 0 else float("inf")

        rows.append({
            "period":               int(period),
            "period_label":         PERIOD_LABELS.get(int(period), f"Period {int(period)}"),
            "ppda":                 ppda,
            "opp_passes":           opp_passes,
            "press_actions":        press_actions,
            "press_classification": classify_ppda(ppda),
        })

    return pd.DataFrame(rows)


def detect_pressing_verdict(v_state: str, ppda: float) -> tuple[str, str]:
    """
    Cross-references vertical shape with PPDA to detect the False High Line
    and other combined verdicts. Returns (verdict_label, explanation).
    """
    press_class = classify_ppda(ppda)

    if v_state == "High Line" and press_class == "Aggressive Press":
        return (
            "Genuine High Press",
            "The team's high defensive line is backed up by relentless "
            "ball-hunting. This is a coherent, aggressive tactical setup — "
            "but it leaves significant space in behind."
        )
    elif v_state == "High Line" and press_class == "Passive / Low Press":
        return (
            "⚠  FALSE HIGH LINE DETECTED",
            "The team is sitting high up the pitch but barely pressing. "
            "This is the most dangerous defensive setup in football — "
            "they are exposed to balls in behind without the pressing "
            "intensity to compensate. A well-organised opponent will "
            "exploit this ruthlessly."
        )
    elif v_state == "High Line" and press_class == "Moderate Press":
        return (
            "High Line with Moderate Press",
            "Sitting high and pressing with some intensity, but not "
            "aggressively enough to be truly suffocating. Functional, "
            "but leaves some exposure in behind."
        )
    elif v_state == "Mid Block" and press_class == "Aggressive Press":
        return (
            "Aggressive Mid-Press",
            "Defending from a midfield base but pressing with high "
            "intensity in the opponent's own half. An underrated and "
            "very difficult setup to play through — the opponent cannot "
            "build comfortably but there is no gaping space in behind."
        )
    elif v_state == "Low Block" and press_class == "Passive / Low Press":
        return (
            "Parking the Bus",
            "Deep defensive line with minimal pressing. Classic "
            "counter-attacking setup — defending the box and looking "
            "to exploit transitions."
        )
    else:
        return (
            f"{v_state} + {press_class}",
            "A standard tactical combination — no exceptional "
            "vulnerabilities or strengths flagged."
        )


def run_ppda_analysis(events: pd.DataFrame, shape_summary: pd.DataFrame) -> pd.DataFrame:
    """
    Computes PPDA for each team and prints a plain-English pressing report.
    Cross-references PPDA with vertical shape to detect combined verdicts
    including the False High Line.

    Args:
        events        — raw events DataFrame from ingest_match_events()
        shape_summary — team-level defensive shape summary (post logic gates)

    Returns:
        DataFrame with per-team PPDA values and classifications.
    """
    print("\n[PPDA] Computing pressing intensity per team...")

    teams = events["team"].dropna().unique()
    rows  = []

    for team in teams:
        ppda, opp_passes, press_actions = compute_ppda_for_team(team, events)
        press_class = classify_ppda(ppda)

        # Pull this team's vertical state from the shape summary
        team_shape = shape_summary[shape_summary["team"] == team]
        v_state = team_shape["vertical_state"].values[0] if len(team_shape) > 0 else "Unknown"

        verdict_label, verdict_desc = detect_pressing_verdict(v_state, ppda)

        rows.append({
            "team":             team,
            "ppda":             ppda,
            "opp_passes":       opp_passes,
            "press_actions":    press_actions,
            "press_class":      press_class,
            "vertical_state":   v_state,
            "verdict_label":    verdict_label,
            "verdict_desc":     verdict_desc,
        })

    summary = pd.DataFrame(rows)

    divider = "=" * 68
    print(f"\n{divider}")
    print("  SIDELINE.AI — PRESSING INTENSITY REPORT")
    print(f"  Argentina vs France | 2022 World Cup Final")
    print(divider)

    for _, row in summary.iterrows():
        team          = row["team"]
        ppda          = row["ppda"]
        press_class   = row["press_class"]
        verdict_label = row["verdict_label"]
        verdict_desc  = row["verdict_desc"]
        opp_passes    = int(row["opp_passes"])
        press_actions = int(row["press_actions"])

        print(f"\n  ── {team.upper()} ──────────────────────────────────────")
        print(f"\n  PRESSING VERDICT")
        print(f"  Classification : {press_class}")
        print(f"  Combined Verdict: {verdict_label}")

        print(f"\n  WHAT THIS MEANS")
        print(f"  {verdict_desc}")

        # Per-period breakdown
        period_df = compute_ppda_by_period(team, events)
        if not period_df.empty:
            print(f"\n  HOW DID PRESSING INTENSITY CHANGE?")
            prev_class = None
            for _, p in period_df.iterrows():
                change_flag = ""
                if prev_class is not None and p["press_classification"] != prev_class:
                    change_flag = "  ⚠  Pressing shift"
                print(f"  {p['period_label']}  →  {p['press_classification']}"
                      f"  (PPDA: {p['ppda']}){change_flag}")
                prev_class = p["press_classification"]

    print(f"\n{divider}\n")
    print("  [TECHNICAL RECEIPT — for reference only]")
    print(f"  PPDA = Opponent passes in their own half (x ≤ 60)")
    print(f"         ÷ Pressing actions in same zone (Tackle + Interception + Pressure + Foul Committed)")
    print(f"  Thresholds: < {PPDA_THRESHOLDS['aggressive_max']} Aggressive | "
          f"{PPDA_THRESHOLDS['aggressive_max']}–{PPDA_THRESHOLDS['passive_min']} Moderate | "
          f"> {PPDA_THRESHOLDS['passive_min']} Passive")
    print(f"  Note: Thresholds recalibrated against 2022 World Cup data (4 matches, 8 observations).")
    print(f"        To be recalibrated against 2022 World Cup group stage data.")
    for _, row in summary.iterrows():
        print(f"  {row['team']}: PPDA = {row['ppda']} "
              f"({int(row['opp_passes'])} opp passes ÷ {int(row['press_actions'])} press actions)")
    print(f"\n{divider}\n")

    return summary

# =============================================================================
# VERTICAL COMPACTNESS ENGINE
# Measures the gap between a team's deepest and highest defensive actions.
# Captures space between the lines — invisible to Avg X and Y-Offset alone.
#
# Formula:
#   C_v = X_max - X_min
#   Where X_max and X_min are the highest and lowest X coordinates
#   across all defensive events in a given window.
#
# A small C_v = unit defending as one compact block.
# A large C_v = dangerous gap between defensive lines.
#
# Thresholds (working baseline — to be recalibrated vs 2022 group stage data):
#   Compact  : C_v < 20u  (~17.5m)
#   Standard : 20u <= C_v <= 35u  (~17.5–30.6m)
#   Gapped   : C_v > 35u  (~30.6m)
# =============================================================================

# Compactness thresholds — FINAL, recalibrated using correct 2022 WC match IDs.
# Formula: IQR (X_p75 - X_p25). Correct calibration data (4 matches, 8 observations):
#   Min=28.80u  P25=37.06u  P50=39.77u  P75=41.75u  Max=49.00u
# Morocco C_v=28.80u (Compact, Low Block) and Spain C_v=49.00u (Gapped) confirmed.
COMPACTNESS_THRESHOLDS = {
    "compact_max":  37.0,
    "gapped_min":   42.0,
}

def classify_compactness(c_v: float) -> str:
    if c_v < COMPACTNESS_THRESHOLDS["compact_max"]:
        return "Compact"
    elif c_v > COMPACTNESS_THRESHOLDS["gapped_min"]:
        return "Gapped"
    else:
        return "Standard"


def compute_compactness_for_team(
    team: str,
    defensive: pd.DataFrame,
) -> tuple[float, float, float]:
    """
    Computes match-wide vertical compactness for one team using IQR.

    Formula: C_v = X_p75 - X_p25
    Measures where the middle 50% of defensive actions are concentrated.
    IQR is used instead of X_max - X_min because a single clearance at x=2u
    or a pressure at x=116u inflates the range to ~114u for every team,
    making the metric useless. IQR is outlier-immune.

    Returns:
        c_v   — IQR of location_x (the between-lines gap in units)
        x_p75 — 75th percentile of defensive action X coordinates
        x_p25 — 25th percentile of defensive action X coordinates
    """
    team_events = defensive[defensive["team"] == team]
    if team_events.empty:
        return float("nan"), float("nan"), float("nan")

    x_p75 = team_events["location_x"].quantile(0.75)
    x_p25 = team_events["location_x"].quantile(0.25)
    c_v   = round(x_p75 - x_p25, 2)
    return c_v, x_p75, x_p25


def compute_compactness_by_period(
    team: str,
    defensive: pd.DataFrame,
) -> pd.DataFrame:
    """
    Computes vertical compactness per StatsBomb period for one team.
    Returns a DataFrame with columns:
        period, period_label, c_v, x_max, x_min, classification.
    """
    rows = []
    team_events = defensive[defensive["team"] == team]

    for period in sorted(team_events["period"].dropna().unique()):
        period_events = team_events[team_events["period"] == period]
        if period_events.empty:
            continue

        x_p75 = period_events["location_x"].quantile(0.75)
        x_p25 = period_events["location_x"].quantile(0.25)
        c_v   = round(x_p75 - x_p25, 2)

        rows.append({
            "period":         int(period),
            "period_label":   PERIOD_LABELS.get(int(period), f"Period {int(period)}"),
            "c_v":            c_v,
            "x_p75":          round(x_p75, 1),
            "x_p25":          round(x_p25, 1),
            "classification": classify_compactness(c_v),
        })

    return pd.DataFrame(rows)


def detect_compactness_risk(
    h_state: str,
    compactness_class: str,
) -> tuple[str, str]:
    """
    Cross-references horizontal state (narrow/balanced/stretched) with
    vertical compactness to detect combined risk profiles.

    The most dangerous combination: Narrow + Gapped.
    Looks organised horizontally but has a lethal gap between the lines.

    Returns (risk_label, explanation).
    """
    if h_state == "Narrow" and compactness_class == "Gapped":
        return (
            "⚠  HIDDEN GAP — HIGH RISK",
            "The team looks narrow and organised from side to side, but "
            "has a dangerous vertical gap between its defensive lines. "
            "A sharp through ball or a second striker dropping into this "
            "space will find acres of room. This is the setup most "
            "commonly exploited by World Cup-level attacking teams."
        )
    elif h_state == "Stretched" and compactness_class == "Gapped":
        return (
            "⚠  OPEN — VERY HIGH RISK",
            "The team is both horizontally stretched and vertically gapped. "
            "They are exposed in the center, the half-spaces, and between "
            "the lines simultaneously. A well-organised attacking team "
            "will find space almost anywhere."
        )
    elif h_state == "Narrow" and compactness_class == "Compact":
        return (
            "Defensively Solid",
            "The team is compact both horizontally and vertically — "
            "a tight, disciplined defensive block. Very difficult to "
            "break down through the middle. Opponent will likely be "
            "forced to try from distance or wide areas."
        )
    elif compactness_class == "Compact":
        return (
            "Vertically Tight",
            "The lines are well-connected vertically — limited space "
            "between defence and midfield. Any vulnerability is "
            "likely out wide rather than through the center."
        )
    elif compactness_class == "Gapped":
        return (
            "⚠  Gap Between Lines",
            "A notable space exists between the defensive lines. "
            "Runners from midfield or a creative No.10 will find "
            "room to receive and turn in this gap."
        )
    else:
        return (
            "Standard Shape",
            "Normal vertical spread — no exceptional risk flagged "
            "between the defensive lines."
        )


# Event types used for compactness calculation.
# Deliberately narrower than DEFENSIVE_EVENT_TYPES — Clearances and Blocks
# occur at pitch extremes (own box, goal line) and inflate C_v to ~100m,
# destroying the between-the-lines signal. Only pressing/winning actions
# that occur in the active defensive shape are used here.
COMPACTNESS_EVENT_TYPES = ["Tackle", "Interception", "Pressure"]


def run_compactness_analysis(
    defensive: pd.DataFrame,
    shape_summary: pd.DataFrame,
) -> pd.DataFrame:
    """
    Computes vertical compactness for each team and prints a plain-English
    between-the-lines report. Cross-references with horizontal state to
    detect combined risk profiles — especially the Hidden Gap pattern.

    Uses only Tackles, Interceptions, and Pressures for C_v calculation.
    Clearances and Blocks are excluded — they happen at pitch extremes and
    inflate the gap metric to the full pitch length (~100m), which is
    meaningless for between-the-lines analysis.

    Args:
        defensive     — transformed defensive events DataFrame
        shape_summary — team-level shape summary (post logic gates),
                        used to pull horizontal_state per team

    Returns:
        DataFrame with per-team compactness values and classifications.
    """
    print("\n[COMPACTNESS] Computing vertical compactness per team...")

    # Filter to pressing/winning actions only for compactness signal
    defensive = defensive[defensive["type"].isin(COMPACTNESS_EVENT_TYPES)].copy()

    teams = defensive["team"].dropna().unique()
    rows  = []

    for team in teams:
        c_v, x_max, x_min = compute_compactness_for_team(team, defensive)
        comp_class = classify_compactness(c_v)

        # Pull horizontal state from shape summary for combined risk detection
        team_shape = shape_summary[shape_summary["team"] == team]
        h_state = (team_shape["horizontal_state"].values[0]
                   if len(team_shape) > 0 else "Unknown")

        risk_label, risk_desc = detect_compactness_risk(h_state, comp_class)

        rows.append({
            "team":             team,
            "c_v":              c_v,
            "x_max":            x_max,
            "x_min":            x_min,
            "classification":   comp_class,
            "horizontal_state": h_state,
            "risk_label":       risk_label,
            "risk_desc":        risk_desc,
        })

    summary = pd.DataFrame(rows)

    divider = "=" * 68
    print(f"\n{divider}")
    print("  SIDELINE.AI — BETWEEN THE LINES REPORT")
    print(f"  Argentina vs France | 2022 World Cup Final")
    print(divider)

    for _, row in summary.iterrows():
        team       = row["team"]
        c_v        = row["c_v"]
        comp_class = row["classification"]
        risk_label = row["risk_label"]
        risk_desc  = row["risk_desc"]

        c_v_m  = u_to_m(c_v)
        c_v_yd = u_to_yd(c_v)

        print(f"\n  ── {team.upper()} ──────────────────────────────────────")
        print(f"\n  BETWEEN-THE-LINES VERDICT")
        print(f"  Vertical Compactness : {comp_class}")
        print(f"  Between-Lines IQR    : {c_v_m}m ({c_v_yd}yd)")
        print(f"  Combined Risk        : {risk_label}")

        print(f"\n  WHAT THIS MEANS")
        print(f"  {risk_desc}")

        # Period-by-period breakdown
        period_df = compute_compactness_by_period(team, defensive)
        if not period_df.empty:
            print(f"\n  HOW DID COMPACTNESS EVOLVE?")
            prev_class = None
            for _, p in period_df.iterrows():
                change_flag = ""
                if prev_class is not None and p["classification"] != prev_class:
                    change_flag = "  ⚠  Compactness shift"

                print(f"  {p['period_label']}  →  {p['classification']}"
                      f"   Gap: {u_to_m(p['c_v'])}m ({u_to_yd(p['c_v'])}yd)"
                      f"{change_flag}")
                prev_class = p["classification"]

    print(f"\n{divider}\n")
    print("  [TECHNICAL RECEIPT — for reference only]")
    print(f"  C_v = IQR (X_p75 - X_p25) across all defensive events")
    print(f"  IQR used instead of range to eliminate outlier inflation.")
    print(f"  Thresholds: "
          f"< {COMPACTNESS_THRESHOLDS['compact_max']}u Compact | "
          f"{COMPACTNESS_THRESHOLDS['compact_max']}–"
          f"{COMPACTNESS_THRESHOLDS['gapped_min']}u Standard | "
          f"> {COMPACTNESS_THRESHOLDS['gapped_min']}u Gapped")
    print(f"  Note: Thresholds to be recalibrated vs 2022 group stage data.")
    for _, row in summary.iterrows():
        print(f"  {row['team']}: C_v = {row['c_v']}u "
              f"(X_p75={row['x_max']}u, X_p25={row['x_min']}u)")
    print(f"\n{divider}\n")

    return summary


# =============================================================================
# MOMENTUM SHIFT DETECTOR
# Identifies the exact period boundary where the balance of power between
# both teams flipped simultaneously.
#
# Unlike Shape Shift Alert (which tracks one team's shape in isolation),
# Momentum Shift requires BOTH of these to fire at the same period boundary:
#
#   Condition 1 — Shape collapse:
#     Team A's Avg X drops by > 10u between periods (they retreated)
#
#   Condition 2 — Progression surge:
#     Team B's Progression Rate increases by > 15pp between the same periods
#     Progression Rate = progressive passes ÷ total completed passes (per period)
#
# The 15pp threshold filters out natural fluctuation (~5–10pp noise).
# A 15pp jump = structural change, not randomness.
# =============================================================================

# Momentum thresholds — recalibrated against 2022 WC data.
# Old surge threshold (15pp) exceeded the entire progression rate range (7.4pp)
# and would never fire. New threshold (4pp) ≈ half SD of the distribution.
MOMENTUM_THRESHOLDS = {
    "shape_collapse_u":      10.0,   # units — unchanged, validated
    "progression_surge_pct":  4.0,   # pp — recalibrated from 15pp (too high)
}


def compute_progression_rate_by_period(events: pd.DataFrame) -> pd.DataFrame:
    """
    Computes progressive pass rate per team per period.
    Rate = (progressive passes in period) / (total completed passes in period) * 100

    Returns DataFrame with columns:
        team, period, period_label, prog_count, total_passes, prog_rate_pct
    """
    # Completed passes only, no penalties
    passes = events[events["type"] == "Pass"].copy()
    passes = passes[passes["period"] != 5]
    passes = passes.dropna(subset=["location", "pass_end_location"])
    passes = passes[passes["pass_outcome"].isna()]

    # Unpack coordinates
    passes["x1"] = passes["location"].apply(lambda l: float(l[0]))
    passes["y1"] = passes["location"].apply(lambda l: float(l[1]))
    passes["x2"] = passes["pass_end_location"].apply(lambda l: float(l[0]))
    passes["y2"] = passes["pass_end_location"].apply(lambda l: float(l[1]))

    passes["d_start"] = passes.apply(
        lambda r: euclidean_to_goal(r["x1"], r["y1"]), axis=1)
    passes["d_end"] = passes.apply(
        lambda r: euclidean_to_goal(r["x2"], r["y2"]), axis=1)
    passes["delta_d"] = passes["d_start"] - passes["d_end"]

    results = passes.apply(
        lambda r: classify_progressive(r["x1"], r["x2"], r["delta_d"]), axis=1)
    passes["is_progressive"] = results.apply(lambda t: t[0])

    rows = []
    for team in passes["team"].dropna().unique():
        for period in sorted(passes["period"].dropna().unique()):
            period_passes = passes[
                (passes["team"] == team) &
                (passes["period"] == period)
            ]
            total     = len(period_passes)
            prog      = int(period_passes["is_progressive"].sum())
            rate      = round((prog / total) * 100, 1) if total > 0 else 0.0
            rows.append({
                "team":          team,
                "period":        int(period),
                "period_label":  PERIOD_LABELS.get(int(period), f"Period {int(period)}"),
                "prog_count":    prog,
                "total_passes":  total,
                "prog_rate_pct": rate,
            })

    return pd.DataFrame(rows)


def detect_momentum_shifts(
    period_summary: pd.DataFrame,
    prog_rate_df: pd.DataFrame,
) -> list[dict]:
    """
    Scans consecutive periods for simultaneous shape collapse + progression surge.

    For each period boundary, checks all team-pair combinations:
        - Team A collapses (Avg X drop > 10u)
        - Team B surges (Progression Rate increase > 15pp)

    Returns a list of momentum shift event dicts.
    """
    teams = period_summary["team"].dropna().unique()
    if len(teams) < 2:
        return []

    team_a, team_b = teams[0], teams[1]
    periods = sorted(period_summary["period"].dropna().unique())
    shifts  = []

    for i in range(1, len(periods)):
        prev_period = periods[i - 1]
        curr_period = periods[i]

        from_label = PERIOD_LABELS.get(int(prev_period), f"Period {int(prev_period)}")
        to_label   = PERIOD_LABELS.get(int(curr_period), f"Period {int(curr_period)}")

        def get_avg_x(team, period):
            row = period_summary[
                (period_summary["team"] == team) &
                (period_summary["period"] == period)
            ]
            return row["avg_defensive_x"].values[0] if len(row) > 0 else None

        def get_prog_rate(team, period):
            row = prog_rate_df[
                (prog_rate_df["team"] == team) &
                (prog_rate_df["period"] == period)
            ]
            return row["prog_rate_pct"].values[0] if len(row) > 0 else None

        # Check both team-pair directions: A collapses + B surges, and vice versa
        for collapsing, surging in [(team_a, team_b), (team_b, team_a)]:
            x_prev = get_avg_x(collapsing, prev_period)
            x_curr = get_avg_x(collapsing, curr_period)
            r_prev = get_prog_rate(surging, prev_period)
            r_curr = get_prog_rate(surging, curr_period)

            if any(v is None for v in [x_prev, x_curr, r_prev, r_curr]):
                continue

            delta_x    = x_prev - x_curr          # positive = dropped deeper
            delta_rate = r_curr - r_prev           # positive = surged

            cond1 = delta_x    > MOMENTUM_THRESHOLDS["shape_collapse_u"]
            cond2 = delta_rate > MOMENTUM_THRESHOLDS["progression_surge_pct"]

            if cond1 and cond2:
                shifts.append({
                    "from_period":    from_label,
                    "to_period":      to_label,
                    "collapsing_team": collapsing,
                    "surging_team":    surging,
                    "delta_x_m":      u_to_m(delta_x),
                    "rate_before_pct": r_prev,
                    "rate_after_pct":  r_curr,
                    "delta_rate_pct":  round(delta_rate, 1),
                })

    return shifts


def run_momentum_shift_detector(
    period_summary: pd.DataFrame,
    events: pd.DataFrame,
    output_mode: str = OUTPUT_MODE_ANALYST,
) -> pd.DataFrame:
    """
    Runs the Momentum Shift Detector and prints a plain-English report.

    Args:
        period_summary — per-team per-period defensive shape aggregation
        events         — raw events DataFrame (for progression rate computation)
        output_mode    — "beginner" or "analyst"

    Returns:
        DataFrame of detected momentum shifts.
    """
    print("\n[MOMENTUM] Computing per-period progression rates...")
    prog_rate_df = compute_progression_rate_by_period(events)

    print("[MOMENTUM] Scanning for momentum shifts...")
    shifts = detect_momentum_shifts(period_summary, prog_rate_df)
    shifts_df = pd.DataFrame(shifts) if shifts else pd.DataFrame()

    divider = "=" * 68
    print(f"\n{divider}")
    print("  SIDELINE.AI — MOMENTUM SHIFT REPORT")
    print(f"  Argentina vs France | 2022 World Cup Final")
    print(divider)

    if shifts_df.empty:
        print("\n  No momentum shifts detected — the balance of power")
        print("  remained stable throughout the match.")
        print(f"\n{divider}\n")
        return shifts_df

    print(f"\n  {len(shifts)} momentum shift(s) detected:\n")

    for i, shift in enumerate(shifts, 1):
        delta_rate = shift["delta_rate_pct"]
        depth      = shift["delta_x_m"]

        print(f"  ⚡ MOMENTUM SHIFT [{i}]")
        print(f"  {shift['from_period'].strip()} → {shift['to_period'].strip()}")
        print()
        print(f"  {shift['collapsing_team']} retreated {depth}m deeper into their"
              f" own half.")
        print(f"  {shift['surging_team']}\'s progression rate jumped from"
              f" {shift['rate_before_pct']}% → {shift['rate_after_pct']}%"
              f" (+{delta_rate}pp).")
        print()

        # Plain-English interpretation of severity
        if delta_rate >= 25:
            print(f"  → Decisive shift. {shift['surging_team']} went from struggling")
            print(f"    to progress to dominating the ball in dangerous areas.")
        elif delta_rate >= 15:
            print(f"  → Clear shift. {shift['surging_team']} gained significant")
            print(f"    territorial control as {shift['collapsing_team']} dropped.")
        print()

    if should_show_receipt(output_mode):
        print(f"  [TECHNICAL RECEIPT — for reference only]")
        print(f"  Shape collapse trigger    : Avg X drop > "
              f"{MOMENTUM_THRESHOLDS['shape_collapse_u']}u "
              f"({u_to_m(MOMENTUM_THRESHOLDS['shape_collapse_u'])}m)")
        print(f"  Progression surge trigger : Rate increase > "
              f"{MOMENTUM_THRESHOLDS['progression_surge_pct']}pp")
        print(f"  Both conditions must fire at the same period boundary.")
        print()
        print(f"  Per-period progression rates:")
        for _, row in prog_rate_df.iterrows():
            print(f"  {row['team']} | {row['period_label'].strip()}: "
                  f"{row['prog_rate_pct']}% "
                  f"({row['prog_count']} progressive / {row['total_passes']} total)")

    print(f"\n{divider}\n")
    return shifts_df


# =============================================================================
# THE GAME FLOW (Merged Template B + F)
# A single unified report that answers: "How did this match unfold tactically?"
#
# Combines:
#   - Shape Shift Alert   : per-team shape changes between periods
#   - Momentum Shift      : cross-team balance-of-power flips
#
# Together these tell the complete story:
#   WHAT changed (shape), WHEN it changed (period boundary),
#   and WHETHER it flipped the balance of power (momentum).
#
# Replaces the standalone Template B (Tactical Pivot) and
# Template F (Momentum Report) in the Streamlit UI.
# =============================================================================

def run_game_flow_template(
    period_summary: pd.DataFrame,
    events: pd.DataFrame,
    output_mode: str = OUTPUT_MODE_ANALYST,
) -> dict:
    """
    Unified "Game Flow" template — merges Shape Shift Alert and Momentum Shift
    into a single chronological narrative of how the match unfolded.

    Structure of output:
      1. Per-period shape timeline for both teams (from Shape Shift)
      2. Shape shift alerts flagged inline on the timeline
      3. Momentum shift verdicts where both conditions fire simultaneously

    Args:
        period_summary — per-team per-period defensive shape aggregation
        events         — raw events DataFrame
        output_mode    — "beginner" or "analyst"

    Returns:
        Dict with keys "shape_shifts" and "momentum_shifts" DataFrames.
    """
    print("\n[GAME FLOW] Running unified tactical narrative...")

    # Compute both underlying analyses
    prog_rate_df  = compute_progression_rate_by_period(events)
    shape_shifts  = []
    teams = period_summary["team"].dropna().unique()
    for team in teams:
        for s in detect_shape_shifts(team, period_summary):
            s["team"] = team
            shape_shifts.append(s)

    momentum_shifts = detect_momentum_shifts(period_summary, prog_rate_df)

    divider = "=" * 68
    print(f"\n{divider}")
    print("  SIDELINE.AI — THE GAME FLOW")
    print(f"  Argentina vs France | 2022 World Cup Final")
    print(f"  How did this match unfold tactically?")
    print(divider)

    # Build a unified period-by-period timeline
    all_periods = sorted(period_summary["period"].dropna().unique())

    for i, period in enumerate(all_periods):
        period_label = PERIOD_LABELS.get(int(period), f"Period {int(period)}")
        print(f"\n  ── {period_label.strip()} ─────────────────────────────────")

        # Shape snapshot for each team this period
        for team in teams:
            row = period_summary[
                (period_summary["team"] == team) &
                (period_summary["period"] == period)
            ]
            if row.empty:
                continue

            avg_x    = row["avg_defensive_x"].values[0]
            avg_off  = row["avg_y_offset"].values[0]
            n        = int(row["event_count"].values[0])
            v_state  = classify_vertical(avg_x)
            h_state  = classify_horizontal(avg_off)
            v_label  = VERTICAL_DESCRIPTIONS[v_state][0]
            h_label  = HORIZONTAL_DESCRIPTIONS[h_state][0]

            # Progression rate this period
            prog_row = prog_rate_df[
                (prog_rate_df["team"] == team) &
                (prog_rate_df["period"] == period)
            ]
            prog_rate = prog_row["prog_rate_pct"].values[0] if not prog_row.empty else 0.0

            print(f"  {team:20s} : {v_label} | {h_label}"
                  f"  — Progression rate: {prog_rate}%  (n={n})")

        # Flag any shape shifts entering THIS period (from prev → this)
        if i > 0:
            prev_period = all_periods[i - 1]
            from_label  = PERIOD_LABELS.get(int(prev_period), f"Period {int(prev_period)}")
            to_label    = period_label

            period_shape_shifts = [
                s for s in shape_shifts
                if s["from_period"].strip() == from_label.strip()
            ]
            for s in period_shape_shifts:
                severity = "🔴" if s["severity"] == "major" else "🟡"
                print(f"  {severity} {s['team']} — {s['description']}")

            # Flag momentum shift at this boundary if one exists
            period_momentum = [
                m for m in momentum_shifts
                if m["from_period"].strip() == from_label.strip()
            ]
            for m in period_momentum:
                print(f"  ⚡ MOMENTUM SHIFT — {m['surging_team']} gained territorial"
                      f" dominance as {m['collapsing_team']} retreated {m['delta_x_m']}m.")
                print(f"     {m['surging_team']}\'s progression: "
                      f"{m['rate_before_pct']}% → {m['rate_after_pct']}%"
                      f" (+{m['delta_rate_pct']}pp)")

    # Summary verdict
    print(f"\n  ── MATCH VERDICT ───────────────────────────────────")
    if momentum_shifts:
        key = momentum_shifts[0]
        print(f"  The decisive moment was the transition from")
        print(f"  {key['from_period'].strip()} to {key['to_period'].strip()}.")
        print(f"  {key['surging_team']} took control as {key['collapsing_team']}")
        print(f"  dropped deeper and conceded territorial dominance.")
    else:
        print(f"  No single decisive momentum shift detected —")
        print(f"  the balance of power remained contested throughout.")

    if should_show_receipt(output_mode):
        print(f"\n  [TECHNICAL RECEIPT — for reference only]")
        print(f"  Shape collapse trigger    : ΔX > "
              f"{SHIFT_THRESHOLDS['vertical_magnitude']}u "
              f"({u_to_m(SHIFT_THRESHOLDS['vertical_magnitude'])}m)")
        print(f"  Progression surge trigger : Rate increase > "
              f"{MOMENTUM_THRESHOLDS['progression_surge_pct']}pp")
        print(f"  Momentum requires BOTH conditions at same period boundary.")

    print(f"\n{divider}\n")

    return {
        "shape_shifts":    pd.DataFrame(shape_shifts) if shape_shifts else pd.DataFrame(),
        "momentum_shifts": pd.DataFrame(momentum_shifts) if momentum_shifts else pd.DataFrame(),
    }

# =============================================================================
# MAIN PIPELINE ENTRY POINT
# =============================================================================


# =============================================================================
# SHAPE SHIFT ALERT ENGINE
# Proactively detects meaningful tactical changes between periods.
# Fires on two trigger conditions:
#   1. Classification change  — team crosses a threshold boundary
#      (e.g. Mid Block → Low Block, Balanced → Stretched)
#   2. Magnitude shift        — team stays in same class but moves
#      significantly within it (large delta in Avg X or Avg Offset)
#
# Magnitude thresholds:
#   Vertical   : |ΔX|      > 10u (~8.8m) between consecutive periods
#   Horizontal : |ΔOffset| > 5u  (~4.4m) between consecutive periods
# =============================================================================

SHIFT_THRESHOLDS = {
    "vertical_magnitude":   10.0,   # units
    "horizontal_magnitude":  5.0,   # units
}


def detect_shape_shifts(
    team: str,
    period_summary: pd.DataFrame,
) -> list[dict]:
    """
    Scans period-by-period shape data for one team and returns a list
    of shift events. Each shift event is a dict with:
        from_period, to_period, shift_type, description, severity.

    Severity: "major" (classification change) or "notable" (magnitude only).
    """
    team_periods = (
        period_summary[period_summary["team"] == team]
        .sort_values("period")
        .reset_index(drop=True)
    )

    if len(team_periods) < 2:
        return []

    shifts = []

    for i in range(1, len(team_periods)):
        prev = team_periods.iloc[i - 1]
        curr = team_periods.iloc[i]

        prev_v = classify_vertical(prev["avg_defensive_x"])
        curr_v = classify_vertical(curr["avg_defensive_x"])
        prev_h = classify_horizontal(prev["avg_y_offset"])
        curr_h = classify_horizontal(curr["avg_y_offset"])

        delta_x      = curr["avg_defensive_x"] - prev["avg_defensive_x"]
        delta_offset = curr["avg_y_offset"]     - prev["avg_y_offset"]

        from_label = PERIOD_LABELS.get(int(prev["period"]), f"Period {int(prev['period'])}")
        to_label   = PERIOD_LABELS.get(int(curr["period"]), f"Period {int(curr['period'])}")

        # --- Trigger 1: Classification change ---
        if prev_v != curr_v:
            direction = "dropped deeper" if delta_x < 0 else "pushed higher"
            shifts.append({
                "from_period":  from_label,
                "to_period":    to_label,
                "shift_type":   "Vertical Classification Change",
                "severity":     "major",
                "description": (
                    f"{team} {direction} between the "
                    f"{from_label.strip()} and {to_label.strip()} — "
                    f"shape shifted from {VERTICAL_DESCRIPTIONS[prev_v][0]} "
                    f"to {VERTICAL_DESCRIPTIONS[curr_v][0]}. "
                    f"Line moved {u_to_m(abs(delta_x))}m "
                    f"({'back' if delta_x < 0 else 'forward'})."
                ),
            })

        if prev_h != curr_h:
            direction = "narrowed" if delta_offset < 0 else "widened"
            shifts.append({
                "from_period":  from_label,
                "to_period":    to_label,
                "shift_type":   "Horizontal Classification Change",
                "severity":     "major",
                "description": (
                    f"{team}'s width {direction} between the "
                    f"{from_label.strip()} and {to_label.strip()} — "
                    f"shape shifted from {HORIZONTAL_DESCRIPTIONS[prev_h][0]} "
                    f"to {HORIZONTAL_DESCRIPTIONS[curr_h][0]}. "
                    f"Spread changed by {u_to_m(abs(delta_offset))}m."
                ),
            })

        # --- Trigger 2: Magnitude shift (no classification change needed) ---
        if prev_v == curr_v and abs(delta_x) > SHIFT_THRESHOLDS["vertical_magnitude"]:
            direction = "dropped back" if delta_x < 0 else "pushed up"
            shifts.append({
                "from_period":  from_label,
                "to_period":    to_label,
                "shift_type":   "Significant Vertical Movement",
                "severity":     "notable",
                "description": (
                    f"{team} {direction} significantly within the "
                    f"{VERTICAL_DESCRIPTIONS[curr_v][0]} shape — "
                    f"a {u_to_m(abs(delta_x))}m shift in defensive line "
                    f"without crossing a classification boundary. "
                    f"Still '{VERTICAL_DESCRIPTIONS[curr_v][0]}' "
                    f"but meaningfully {('deeper' if delta_x < 0 else 'higher')}."
                ),
            })

        if prev_h == curr_h and abs(delta_offset) > SHIFT_THRESHOLDS["horizontal_magnitude"]:
            direction = "compressed" if delta_offset < 0 else "spread"
            shifts.append({
                "from_period":  from_label,
                "to_period":    to_label,
                "shift_type":   "Significant Horizontal Movement",
                "severity":     "notable",
                "description": (
                    f"{team}'s width {direction} significantly between periods — "
                    f"a {u_to_m(abs(delta_offset))}m change in lateral spread "
                    f"without crossing a classification boundary."
                ),
            })

    return shifts


def run_shape_shift_alert(
    period_summary: pd.DataFrame,
    output_mode: str = OUTPUT_MODE_ANALYST,
) -> pd.DataFrame:
    """
    Runs Shape Shift detection for all teams and prints a proactive
    alert report. Returns a DataFrame of all detected shift events.

    Args:
        period_summary — per-team per-period shape aggregation
        output_mode    — "beginner" or "analyst"
    """
    print("\n[SHAPE SHIFT] Scanning for tactical changes between periods...")

    teams = period_summary["team"].dropna().unique()
    all_shifts = []

    for team in teams:
        shifts = detect_shape_shifts(team, period_summary)
        for s in shifts:
            s["team"] = team
            all_shifts.append(s)

    shifts_df = pd.DataFrame(all_shifts) if all_shifts else pd.DataFrame()

    divider = "=" * 68
    print(f"\n{divider}")
    print("  SIDELINE.AI — SHAPE SHIFT ALERT")
    print(f"  Argentina vs France | 2022 World Cup Final")
    print(divider)

    if shifts_df.empty:
        print("\n  No significant tactical shifts detected.")
        print(f"\n{divider}\n")
        return shifts_df

    for team in teams:
        team_shifts = [s for s in all_shifts if s["team"] == team]
        if not team_shifts:
            print(f"\n  ── {team.upper()} — No significant shifts detected.")
            continue

        print(f"\n  ── {team.upper()} ──────────────────────────────────────")
        print(f"  {len(team_shifts)} tactical shift(s) detected:\n")

        for i, shift in enumerate(team_shifts, 1):
            severity_label = "🔴 MAJOR" if shift["severity"] == "major" else "🟡 NOTABLE"
            print(f"  [{i}] {severity_label} — {shift['shift_type']}")
            print(f"      {shift['from_period'].strip()} → {shift['to_period'].strip()}")
            print(f"      {shift['description']}")
            print()

    # Analyst mode: show magnitude thresholds used
    if should_show_receipt(output_mode):
        print(f"  [TECHNICAL RECEIPT — for reference only]")
        print(f"  Vertical magnitude trigger   : |ΔX| > "
              f"{SHIFT_THRESHOLDS['vertical_magnitude']}u "
              f"({u_to_m(SHIFT_THRESHOLDS['vertical_magnitude'])}m)")
        print(f"  Horizontal magnitude trigger : |ΔOffset| > "
              f"{SHIFT_THRESHOLDS['horizontal_magnitude']}u "
              f"({u_to_m(SHIFT_THRESHOLDS['horizontal_magnitude'])}m)")

    print(f"\n{divider}\n")
    return shifts_df


# =============================================================================
# MAIN PIPELINE ENTRY POINT
# =============================================================================


# =============================================================================
# PRESS-BREAKING PASS FILTER
# Standalone helper used by api.py Press Autopsy path.
#
# Methodology (matches dossier sent to FIFA / The Athletic):
#   - Source: StatsBomb `under_pressure` boolean flag on Pass events
#   - Filter: completed passes only (pass_outcome is null)
#   - Threshold: Euclidean ΔD to goal > 15u (~13.1m)
#   - PPDA context: most meaningful when team PPDA < 2.5
#     (WC-recalibrated Aggressive Press threshold — P25 of 2022 WC)
# =============================================================================

def get_press_breaking_passes(
    events: pd.DataFrame,
    team: str,
    min_gain_units: float = 15.0,
) -> pd.DataFrame:
    """
    Returns completed passes for `team` made under pressure that
    gained >= min_gain_units Euclidean distance toward goal.

    Args:
        events          — raw match events DataFrame
        team            — team name string
        min_gain_units  — minimum Euclidean gain threshold (default 15u ≈ 13.1m)

    Returns:
        DataFrame with columns: x1, y1, x2, y2, delta_d, minute, player
    """
    passes = events[
        (events["team"]   == team) &
        (events["type"]   == "Pass") &
        (events["period"] != 5) &
        (events["under_pressure"] == True)
    ].copy()

    passes = passes.dropna(subset=["location", "pass_end_location"])
    passes = passes[passes["pass_outcome"].isna()]   # completed only

    passes["x1"] = passes["location"].apply(lambda l: float(l[0]))
    passes["y1"] = passes["location"].apply(lambda l: float(l[1]))
    passes["x2"] = passes["pass_end_location"].apply(lambda l: float(l[0]))
    passes["y2"] = passes["pass_end_location"].apply(lambda l: float(l[1]))

    passes["d_start"] = passes.apply(
        lambda r: euclidean_to_goal(r["x1"], r["y1"]), axis=1)
    passes["d_end"] = passes.apply(
        lambda r: euclidean_to_goal(r["x2"], r["y2"]), axis=1)
    passes["delta_d"] = passes["d_start"] - passes["d_end"]

    result = passes[passes["delta_d"] >= min_gain_units].copy()

    print(f"[PRESS AUTOPSY] {team}: "
          f"{len(result)} press-breaking passes "
          f"(from {len(passes)} completed passes under pressure)")

    return result[["x1", "y1", "x2", "y2", "delta_d", "minute", "player"]].reset_index(drop=True)


def run_pipeline(match_id: int = MATCH_ID, output_mode: str = OUTPUT_MODE_ANALYST) -> dict:
    """
    Orchestrates the full Sideline.ai v0.1 pipeline:
      1. Defensive Shape Analysis    (Avg X + Y-Offset + Logic Receipt)
      2. Offensive Progression       (30-15-10 Euclidean Rule + Danger Corridor)
      3. Pressing Intensity          (PPDA Engine)
      4. Between the Lines           (Vertical Compactness Engine)
      5. The Game Flow               (Merged B+F: Shape Shift + Momentum unified)

    Args:
        match_id    — StatsBomb match ID (default: 3869685, ARG vs FRA 2022)
        output_mode — "beginner" (narrative only) or "analyst" (full receipts)
                      Streamlit UI exposes this as a radio button toggle.

    Returns:
        Dict of all summary DataFrames for downstream use.
    """
    print(f"\n  Mode: {output_mode.upper()}")

    events         = ingest_match_events(match_id)

    # --- Defensive Shape Pipeline ---
    defensive      = filter_defensive_events(events)
    defensive      = transform_coordinates(defensive)
    summary        = aggregate_by_team(defensive)
    period_summary = aggregate_by_team_and_period(defensive)
    summary        = apply_logic_gates(summary)
    print_tactical_report(summary, period_summary, output_mode)

    # --- Progression Pipeline ---
    prog_summary   = run_progression_analysis(events)

    # --- PPDA Pipeline ---
    ppda_summary   = run_ppda_analysis(events, summary)

    # --- Vertical Compactness Pipeline ---
    comp_summary   = run_compactness_analysis(defensive, summary)

    # --- The Game Flow (Merged Template B + F) ---
    # Unified chronological narrative combining Shape Shift Alert and
    # Momentum Shift Detector. Replaces running them as separate reports.
    # run_shape_shift_alert and run_momentum_shift_detector remain available
    # as standalone functions for internal use and testing.
    game_flow = run_game_flow_template(period_summary, events, output_mode)

    return {
        "defensive_summary":   summary,
        "period_summary":      period_summary,
        "progression_summary": prog_summary,
        "ppda_summary":        ppda_summary,
        "compactness_summary": comp_summary,
        "game_flow":           game_flow,
    }


if __name__ == "__main__":
    # Default: analyst mode. Switch to "beginner" for simplified output.
    results = run_pipeline(output_mode=OUTPUT_MODE_ANALYST)

if __name__ == "__main__":
    results = run_pipeline()
