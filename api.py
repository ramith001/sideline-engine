"""
api.py  —  Sideline.ai FastAPI Backend  v0.1.0
Endpoints:
    GET  /health
    POST /analyze   (routes by `template` field)
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import io, base64, math
import os
from functools import lru_cache
from typing import Optional

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from mplsoccer import Pitch
from statsbombpy import sb
import pandas as pd
import numpy as np

API_VERSION = "0.1.0"

app = FastAPI(version=API_VERSION)

DEFAULT_CORS_ORIGINS = ["http://localhost:3000", "https://sideline-engine.vercel.app"]
CORS_ORIGINS = [
    o.strip() for o in os.environ.get("CORS_ORIGINS", "").split(",") if o.strip()
] or DEFAULT_CORS_ORIGINS

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalysisRequest(BaseModel):
    match_id: int
    mode:     str
    template: Optional[str] = "The Game Flow"

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
# Calibrated on 98 team-matches (49 matches) from the three tournaments:
# 22% / 56% / 21% Aggressive / Moderate / Passive, the same split the old
# 2.5 / 4.4 cut-offs gave on the old Pressure-dominated metric.
PPDA_AGGRESSIVE_MAX = 9.0
PPDA_MODERATE_MAX   = 20.0
PPDA_PRESSED_MAX    = 14.0   # "opponent pressed hard" gate in the press-bypass story

DANGER_CORRIDOR = {"x_min": 88.0, "x_max": 120.0, "y_min": 18.0, "y_max": 62.0}

# ── Shared helpers ────────────────────────────────────────────────────────────

def euclidean_to_goal(x: float, y: float) -> float:
    return math.sqrt((GOAL[0] - x) ** 2 + (GOAL[1] - y) ** 2)

def fig_to_b64(fig) -> str:
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight", transparent=True)
    buf.seek(0)
    b64 = base64.b64encode(buf.read()).decode("utf-8")
    plt.close(fig)
    return b64

def make_pitch(figsize=(8, 4)):
    pitch = Pitch(
        pitch_type="statsbomb",
        pitch_color="#111827",
        line_color="#4B5563",
    )
    fig, ax = pitch.draw(figsize=figsize)
    return pitch, fig, ax

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

# ── Health ────────────────────────────────────────────────────────────────────

@app.get("/health")
def health_check():
    return {"status": "ok", "version": API_VERSION}

# ── Main route ────────────────────────────────────────────────────────────────

@lru_cache(maxsize=32)
def _fetch_events(match_id: int) -> pd.DataFrame:
    return sb.events(match_id=match_id)

@app.post("/analyze")
async def run_tactical_engine(request: AnalysisRequest):
    df = _fetch_events(request.match_id).copy()
    if request.template == "The Press Autopsy":
        return _press_autopsy(df, request)
    elif request.template == "The Exploit Finder":
        return _exploit_finder(df, request)
    elif request.template == "The Danger Map":
        return _danger_map(df, request)
    elif request.template == "The Progress Trap":
        return _progress_trap(df, request)
    else:
        return _game_flow(df, request)


# =============================================================================
# AUTO-STORY ENGINE  v1.0
#
# Detects the highest-drama tactical moment in any match and generates
# a ready-to-post Twitter thread + YouTube hook automatically.
#
# Five story detectors, each scored on a 0-10 drama scale:
#   1. MOMENTUM_SHIFT     — Biggest change in progressive pass rate per half
#   2. FALSE_HIGH_LINE    — High defensive line + passive press (PPDA >= PPDA_AGGRESSIVE_MAX)
#   3. PRESS_BYPASS       — High press being beaten with dangerous exits
#   4. SHAPE_COLLAPSE     — Defensive line drops/rises sharply between halves
#   5. CLINICAL_SURGE     — One team significantly more dangerous per pass
#
# The highest-scoring story wins and generates the narrative.
# =============================================================================

# Game state. A defensive line or a progression rate that moves after half-time
# is often just the scoreline (leading teams sit deeper, trailing teams push
# up), so a story must know the half-time score before it blames tactics.

SHIFT_EXPLAINED_WEIGHT = 0.5   # drama weight of a line shift the half-time score explains


def _goals_scored(df: pd.DataFrame, team: str, periods: list) -> int:
    """Goals credited to `team` in the given periods: its shots that scored plus
    own goals scored against the other side."""
    in_periods = df["period"].isin(periods) & (df["team"] == team)
    shots = df[in_periods & (df["type"] == "Shot")]
    scored = shots["shot_outcome"].apply(
        lambda x: (x.get("name") == "Goal") if isinstance(x, dict) else (x == "Goal")
    )
    return int(scored.sum()) + int((in_periods & (df["type"] == "Own Goal For")).sum())


def _halftime_state(df: pd.DataFrame, team: str, opponent) -> dict:
    """Half-time score from `team`'s side: leading / level / trailing."""
    ht_for     = _goals_scored(df, team, [1])
    ht_against = _goals_scored(df, opponent, [1]) if opponent else 0
    margin     = ht_for - ht_against
    state      = "leading" if margin > 0 else ("trailing" if margin < 0 else "level")
    return {"ht_for": ht_for, "ht_against": ht_against, "ht_margin": margin, "state": state}


def _state_phrase(story: dict) -> str:
    """'leading 2-0' / 'level at 1-1' / 'trailing 0-1', the team's own score first."""
    score = f"{story['ht_for']}-{story['ht_against']}"
    return {"leading": f"leading {score}", "trailing": f"trailing {score}"}.get(
        story["state"], f"level at {score}")


def _compute_period_prog_rate(df: pd.DataFrame, team: str) -> dict:
    """Progressive pass count per period for a team."""
    rates = {}
    for period in [1, 2, 3, 4]:
        pf = df[(df["team"] == team) & (df["type"] == "Pass") &
                (df["period"] == period)].copy()
        pf = pf.dropna(subset=["location", "pass_end_location"])
        pf = pf[pf["pass_outcome"].isna()]
        if pf.empty:
            continue
        pf["x1"] = pf["location"].apply(lambda l: float(l[0]))
        pf["x2"] = pf["pass_end_location"].apply(lambda l: float(l[0]))
        pf["d_start"] = pf.apply(lambda r: euclidean_to_goal(r["x1"], r["location"].apply(lambda l: float(l[1])) if False else float(r["location"][1])), axis=1)
        # simplified: just count passes that gain > 10u forward
        pf["prog"] = pf["x2"] > pf["x1"] + 10
        rates[period] = int(pf["prog"].sum())
    return rates


def _auto_story_momentum_shift(df: pd.DataFrame, teams: list) -> dict:
    """Detect biggest momentum shift between 1st and 2nd half."""
    best = None
    best_score = 0

    for team in teams:
        p1 = df[(df["team"] == team) & (df["type"] == "Pass") &
                (df["period"] == 1)].copy()
        p2 = df[(df["team"] == team) & (df["type"] == "Pass") &
                (df["period"] == 2)].copy()

        for p in [p1, p2]:
            if "location" not in p.columns: continue
            p.dropna(subset=["location", "pass_end_location"], inplace=True)
            p["x1"] = p["location"].apply(lambda l: float(l[0]))
            p["y1"] = p["location"].apply(lambda l: float(l[1]))
            p["x2"] = p["pass_end_location"].apply(lambda l: float(l[0]))
            p["y2"] = p["pass_end_location"].apply(lambda l: float(l[1]))

        if p1.empty or p2.empty:
            continue

        def _is_prog_shift(row):
            x1, x2 = row["x1"], row["x2"]
            dd = euclidean_to_goal(x1, row["y1"]) - euclidean_to_goal(x2, row["y2"])
            if x1 <= 60 and x2 <= 60: return dd > 30
            if x1 <= 60 and x2 > 60:  return dd > 15
            if x1 > 60:                return dd > 10
            return False

        p1["prog"] = p1.apply(_is_prog_shift, axis=1)
        p2["prog"] = p2.apply(_is_prog_shift, axis=1)

        rate1 = int(p1["prog"].sum())
        rate2 = int(p2["prog"].sum())
        delta = abs(rate2 - rate1)

        # Drama: delta × 0.25, capped at 10
        drama = min(round(delta * 0.25, 1), 10.0)

        if drama > best_score:
            best_score = drama
            direction = "increased" if rate2 > rate1 else "dropped"
            minute_ref = "46'" if rate2 > rate1 else "HT"
            opp_name = next((t for t in teams if t != team), None)
            best = {
                **_halftime_state(df, team, opp_name),
                "story_type":    "momentum_shift",
                "drama_score":   drama,
                "team":          team,
                "rate1":         rate1,
                "rate2":         rate2,
                "delta":         delta,
                "direction":     direction,
                "minute_ref":    minute_ref,
            }
    return best or {}


def _auto_story_false_high_line(df: pd.DataFrame, teams: list) -> dict:
    """Detect False High Line — high line + passive press."""
    best = None
    best_score = 0

    for team in teams:
        def_ev = get_defensive_events(df, team)
        if def_ev.empty:
            continue

        lines      = _defensive_lines(def_ev)
        avg_x      = float(def_ev["loc_x"].mean())
        def_line_x = lines[0] if lines else avg_x
        ppda       = compute_ppda(df, team)

        v_state    = _classify_vertical(avg_x)
        press_cls  = classify_ppda(ppda)

        if v_state == "High Line" and press_cls in ["Passive / Low Press", "Moderate Press"]:
            # Drama: base 7 + how passive the press is
            drama = min(round(7.0 + max(0, ppda - PPDA_MODERATE_MAX) * 0.1, 1), 10.0)
            if drama > best_score:
                best_score = drama
                def_line_m = round(def_line_x * METERS, 1)
                avg_x_m    = round(avg_x * METERS, 1)
                best = {
                    "story_type":  "false_high_line",
                    "drama_score": drama,
                    "team":        team,
                    "def_line_m":  def_line_m,
                    "avg_x_m":     avg_x_m,
                    "ppda":        ppda,
                }
    return best or {}


def _auto_story_press_bypass(df: pd.DataFrame, teams: list) -> dict:
    """Detect team being pressed hard but escaping effectively."""
    best = None
    best_score = 0

    for team in teams:
        opponent = [t for t in teams if t != team]
        if not opponent:
            continue
        opp = opponent[0]
        opp_ppda = compute_ppda(df, opp)

        # Only interesting if opponent was pressing aggressively
        if opp_ppda > PPDA_PRESSED_MAX:
            continue

        pb = _get_press_breaking_passes(df, team)
        total_under = len(df[
            (df["team"] == team) & (df["type"] == "Pass") &
            (df["period"] != 5) & (df["under_pressure"] == True)
        ])
        if total_under == 0:
            continue

        exit_rate = round((len(pb) / total_under) * 100)
        avg_gain  = round(float(pb["delta_d"].mean()) * METERS, 1) if not pb.empty else 0

        # Drama: how good the bypass was vs how hard the press was
        drama = min(round((exit_rate * 0.08) + (40 - opp_ppda) * 0.125, 1), 10.0)

        if drama > best_score:
            best_score = drama
            best = {
                "story_type":    "press_bypass",
                "drama_score":   drama,
                "team":          team,
                "opp":           opp,
                "opp_ppda":      opp_ppda,
                "exit_rate":     exit_rate,
                "avg_gain_m":    avg_gain,
                "exit_count":    len(pb),
            }
    return best or {}


def _auto_story_shape_collapse(df: pd.DataFrame, teams: list) -> dict:
    """Detect significant defensive line shift between halves."""
    best = None
    best_score = 0

    for team in teams:
        def_ev = get_defensive_events(df, team)
        if def_ev.empty:
            continue

        p1 = def_ev[def_ev["period"] == 1]
        p2 = def_ev[def_ev["period"] == 2]
        if p1.empty or p2.empty:
            continue

        x1 = float(p1["loc_x"].mean())
        x2 = float(p2["loc_x"].mean())
        delta_u = x2 - x1
        delta_m = round(abs(delta_u) * METERS, 1)

        opp_name = next((t for t in teams if t != team), None)
        state    = _halftime_state(df, team, opp_name)
        # A leading team dropping deeper, or a trailing team pushing up, is the
        # scoreline talking, not a tactical story, so it counts for less.
        explained = (delta_u < 0 and state["state"] == "leading") or \
                    (delta_u > 0 and state["state"] == "trailing")

        # Drama: how big the shift was
        drama = min(round(delta_m * 0.55, 1), 10.0)
        if explained:
            drama = round(drama * SHIFT_EXPLAINED_WEIGHT, 1)

        if drama > best_score and delta_m >= 5.0:
            best_score = drama
            direction = "pushed higher" if delta_u > 0 else "dropped deeper"
            best = {
                **state,
                "explained":   explained,
                "story_type":  "shape_collapse",
                "drama_score": drama,
                "team":        team,
                "delta_m":     delta_m,
                "direction":   direction,
                "x1_m":        round(x1 * METERS, 1),
                "x2_m":        round(x2 * METERS, 1),
            }
    return best or {}


def _auto_story_clinical_surge(df: pd.DataFrame, teams: list) -> dict:
    """Detect large clinical efficiency gap between teams."""
    if len(teams) < 2:
        return {}

    data = {}
    for team in teams:
        prog = _get_progressive_passes(df, team)
        if prog.empty:
            data[team] = {"total": 0, "danger": 0, "pct": 0}
            continue
        total   = len(prog)
        danger  = int(prog["danger"].sum())
        pct     = round((danger / total) * 100) if total > 0 else 0
        data[team] = {"total": total, "danger": danger, "pct": pct}

    t0, t1 = teams[0], teams[1]
    gap = abs(data[t0]["pct"] - data[t1]["pct"])

    if gap < 10:
        return {}

    drama = min(round(gap * 0.22, 1), 10.0)
    better = t0 if data[t0]["pct"] > data[t1]["pct"] else t1
    worse  = t1 if better == t0 else t0

    return {
        "story_type":    "clinical_surge",
        "drama_score":   drama,
        "team":          better,
        "better_pct":    data[better]["pct"],
        "worse_pct":     data[worse]["pct"],
        "worse_team":    worse,
        "gap":           gap,
        "better_total":  data[better]["total"],
    }


def _build_story_content(story: dict, teams: list) -> dict:
    """Convert a story dict into the full auto_story format with thread + hooks."""
    stype  = story.get("story_type", "")
    drama  = story.get("drama_score", 5.0)
    team   = story.get("team", teams[0] if teams else "")
    opp    = [t for t in teams if t != team]
    opp    = opp[0] if opp else "the opponent"

    if stype == "momentum_shift":
        rate1, rate2, delta = story["rate1"], story["rate2"], story["delta"]
        direction = story["direction"]
        state     = story["state"]
        phrase    = _state_phrase(story)
        if direction == "increased":
            headline = f"HT: {team} shifts gears — progressive passing {direction} by {delta} in 2nd half"
            hook     = {"trailing": f"{team} went in at the break {phrase}. The second half looked very different...",
                        "leading":  f"{team} went in {phrase} and still turned it up after the break...",
                        }.get(state, f"The game was {phrase} at half-time. Then {team} stepped up...")
            verdict3 = {
                "trailing": f"3/ Behind at the break, some of that is simply a team chasing the game. "
                            f"The scoreline is part of the explanation; the numbers show the surge, not the instruction behind it.",
                "leading":  f"3/ They were already ahead and still raised the tempo, so this was a team pushing on "
                            f"from a position of strength rather than chasing the game.",
            }.get(state, f"3/ With the game level, nothing in the scoreline forced the change. "
                         f"The data shows the surge, not what caused it.")
            tweets   = [
                f"1/ In the first half, {team} managed {rate1} progressive passes. "
                f"They went into the break {phrase}.",
                f"2/ In the second half they generated {rate2} — a {delta}-pass surge.",
                verdict3,
            ]
            yt = f"{team}'s Second-Half Surge | Progression Breakdown"
            key_stat, key_label = f"+{delta}", "HT Surge"
        else:
            headline = f"HT: {team}'s momentum {direction} sharply — from {rate1} to {rate2} progressive passes"
            hook     = {"leading": f"{team} went in {phrase}. The second half was a much quieter game...",
                        }.get(state, f"{team} had {rate1} progressive passes in the first half. The second half was different...")
            verdict3 = {
                "leading":  f"3/ Fewer progressive passes while ahead is what game management looks like. "
                            f"The scoreline explains it better than a tactical failure would.",
                "trailing": f"3/ Progressing less while behind is the version that points to {opp} having adapted, "
                            f"though the event data shows the drop, not its cause.",
            }.get(state, f"3/ With the game level, the drop points to {opp} adapting or {team} tiring. "
                         f"The data shows that it happened, not why.")
            tweets   = [
                f"1/ {team} made {rate1} progressive passes in the first half and went into the break {phrase}.",
                f"2/ In the second half that dropped to {rate2} — a {delta}-pass fall-off.",
                verdict3,
            ]
            yt = f"Why {team}'s Progression Dropped | Half-Time Analysis"
            key_stat, key_label = f"-{delta}", "HT Drop"

    elif stype == "false_high_line":
        def_m = story["def_line_m"]
        ppda  = story["ppda"]
        headline = f"{team}'s False High Line — {def_m}m defensive line, PPDA {ppda}"
        hook     = f"{team} looked organised. The data said they were one ball in behind away from disaster..."
        tweets   = [
            f"1/ {team}'s defensive line was sitting at {def_m}m — deep into the opponent's half. "
            f"On paper, that's an aggressive, high-risk setup.",
            f"2/ But their PPDA was {ppda}. They weren't pressing to justify that line. "
            f"This is the most dangerous structure in football: high line, passive press.",
            f"3/ Any team with a quality striker and the courage to play the ball in behind "
            f"had a free run at {team}'s back four. This is a False High Line — "
            f"and it's exactly how World Cup-level games get decided.",
        ]
        yt = f"The Defensive Setup That Should Have Cost Them | {team} Tactical Analysis"
        key_stat, key_label = f"{ppda}", "PPDA"

    elif stype == "press_bypass":
        opp_ppda  = story["opp_ppda"]
        exit_rate = story["exit_rate"]
        gain_m    = story["avg_gain_m"]
        exits     = story["exit_count"]
        headline  = f"{team} bypassed {opp}'s press {exits} times — {exit_rate}% exit rate vs PPDA {opp_ppda}"
        hook      = f"{opp} pressed with everything they had. {team} found a way through every time..."
        tweets    = [
            f"1/ {opp} were hunting the ball with a PPDA of {opp_ppda} — "
            f"one of the most aggressive press setups you'll see at this level.",
            f"2/ {team} broke that press {exits} times under direct pressure, "
            f"each exit gaining an average of {gain_m}m toward goal. "
            f"A {exit_rate}% success rate against one of the tournament's best presses.",
            f"3/ This is what separates elite teams from the rest: not just resisting a press, "
            f"but converting it into immediate forward momentum. Textbook press resistance.",
        ]
        yt = f"How {team} Broke {opp}'s High Press | Tactical Breakdown"
        key_stat, key_label = f"{exit_rate}%", "Exit Rate"

    elif stype == "shape_collapse":
        delta_m   = story["delta_m"]
        direction = story["direction"]
        x1_m, x2_m = story["x1_m"], story["x2_m"]
        state     = story["state"]
        explained = story["explained"]
        phrase    = _state_phrase(story)
        ctx       = f"with the game {phrase}" if state == "level" else f"while {phrase}"
        headline  = f"{team} {direction} {delta_m}m after the break {ctx}"
        if explained:
            hook = f"The scoreline explains most of what {team}'s shape did after half-time..."
        else:
            hook = f"The scoreline doesn't explain what {team}'s shape did after half-time..."
        # The causal claim depends on the game state, never assumed.
        verdict3 = {
            ("dropped deeper", "leading"):
                "3/ A line dropping while a team leads is game management, not a collapse: "
                "the scoreline explains the shape change.",
            ("dropped deeper", "trailing"):
                f"3/ A team that is behind has no scoreline reason to sit deeper, so this points to {opp} "
                f"pushing them back or a deliberate change of shape. The event data shows the retreat, not which.",
            ("dropped deeper", "level"):
                f"3/ With the scoreline not forcing it, this is a genuine change of shape: an instruction, or {opp} "
                f"pushing them back. The event data shows the shift, not the cause.",
            ("pushed higher", "trailing"):
                "3/ Pushing up while behind is what chasing a game looks like: "
                "the scoreline explains the shape change.",
            ("pushed higher", "leading"):
                "3/ Pushing up while ahead is a choice rather than a necessity: this team kept attacking "
                "the game instead of sitting on the lead.",
            ("pushed higher", "level"):
                "3/ With the game level, nothing in the scoreline forced the move. "
                "The event data shows the shift, not the cause.",
        }[(direction, state)]
        tweets    = [
            f"1/ In the first half, {team}'s defensive line averaged {x1_m}m from their own goal. "
            f"They went into the break {phrase}.",
            f"2/ After the break the line {direction} by {delta_m}m, to {x2_m}m.",
            verdict3,
        ]
        if explained:
            yt = f"How the Scoreline Shaped {team} | Defensive Shape Breakdown"
        else:
            yt = f"The {delta_m}m Shift in {team}'s Shape | Tactical Analysis"
        key_stat  = f"{delta_m}m"
        key_label = "Line Drop" if direction == "dropped deeper" else "Line Push"

    elif stype == "clinical_surge":
        better_pct = story["better_pct"]
        worse_pct  = story["worse_pct"]
        worse_team = story["worse_team"]
        gap        = story["gap"]
        total      = story["better_total"]
        headline   = f"{team} were {gap}% more clinical than {worse_team} — {better_pct}% danger corridor rate"
        hook       = f"Both teams moved the ball forward. Only one of them actually threatened..."
        tweets     = [
            f"1/ Both {team} and {worse_team} generated progressive passes throughout the match. "
            f"On volume alone, it looked relatively even.",
            f"2/ But {team} converted {better_pct}% of their progressive passes into genuine danger — "
            f"passes arriving in the penalty area corridor. {worse_team} managed just {worse_pct}%.",
            f"3/ {gap}% clinical efficiency gap across {total} progressive passes. "
            f"The difference between winning and losing at tournament level is rarely about "
            f"who moved the ball — it's about who moved it dangerously.",
        ]
        yt = f"Why {team} Were So Much More Dangerous | Clinical Efficiency Breakdown"
        key_stat, key_label = f"{better_pct}%", "Clinical Rate"

    else:
        return None

    return {
        "story_type":           stype,
        "drama_score":          drama,
        "headline":             headline,
        "Messagecircle_hook":   hook,
        "Messagecircle_thread": tweets,
        "youtube_hook":         yt,
        "key_stat":             key_stat,
        "key_stat_label":       key_label,
    }


def _get_match_outcome_floor(df: pd.DataFrame) -> float:
    went_to_pens = 5 in df["period"].values
    went_to_et   = any(p in df["period"].values for p in [3, 4])

    goals = df[
        (df["type"] == "Shot") &
        (df["shot_outcome"].apply(
            lambda x: (x.get("name") == "Goal") if isinstance(x, dict) else (x == "Goal")
        )) &
        (~df["period"].isin([5]))
    ]
    total_goals = len(goals)

    teams = df["team"].dropna().unique().tolist()
    goals_per_team = [len(goals[goals["team"] == t]) for t in teams[:2]]
    goal_diff = abs(goals_per_team[0] - goals_per_team[1]) if len(goals_per_team) == 2 else 99

    if went_to_pens and total_goals >= 4 and goal_diff <= 1:
        return 10.0
    if went_to_pens and total_goals >= 3:
        return 9.2
    if went_to_pens:
        return 8.5
    if went_to_et and total_goals >= 4:
        return 8.0
    if went_to_et:
        return 7.5
    if total_goals >= 5 and goal_diff <= 1:
        return 7.5
    if total_goals >= 4:
        return 6.5
    return 0.0


def generate_auto_story(df: pd.DataFrame, teams: list) -> dict | None:
    MIN_DRAMA = 4.0

    detectors = [
        _auto_story_momentum_shift(df, teams),
        _auto_story_false_high_line(df, teams),
        _auto_story_press_bypass(df, teams),
        _auto_story_shape_collapse(df, teams),
        _auto_story_clinical_surge(df, teams),
    ]

    candidates = [d for d in detectors if d and d.get("drama_score", 0) >= MIN_DRAMA]
    if not candidates:
        candidates = [d for d in detectors if d]
        if not candidates:
            return None

    best = max(candidates, key=lambda d: d["drama_score"])

    outcome_floor = _get_match_outcome_floor(df)
    if outcome_floor > best["drama_score"]:
        best = best.copy()
        best["drama_score"] = outcome_floor

    best["drama_score"] = min(round(best["drama_score"], 1), 10.0)

    return _build_story_content(best, teams)


# =============================================================================
# PATH 1 — GAME FLOW
# =============================================================================

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


# =============================================================================
# PATH 2 — PRESS AUTOPSY
# =============================================================================

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


# =============================================================================
# PATH 3 — EXPLOIT FINDER
# =============================================================================


def _exploit_verdict(teams_data: list) -> str:
    """Dynamic two-team verdict for Exploit Finder."""
    valid = [td for td in teams_data if td]
    if not valid:
        return "No data available."
    if len(valid) == 1:
        td = valid[0]
        return td.get("risk_desc", "")

    t0, t1 = valid[0], valid[1]
    name0, name1 = t0["team"], t1["team"]
    fhl0, fhl1   = t0.get("false_hl", False), t1.get("false_hl", False)
    gap0, gap1   = t0.get("gap_m", 0), t1.get("gap_m", 0)
    ppda0, ppda1 = t0.get("ppda", 99), t1.get("ppda", 99)
    v0, v1       = t0.get("v_state", ""), t1.get("v_state", "")
    comp0, comp1 = t0.get("comp_class", ""), t1.get("comp_class", "")
    line0, line1 = t0.get("def_line_m", 0), t1.get("def_line_m", 0)

    # Both have False High Line
    if fhl0 and fhl1:
        return (
            f"Both {name0} and {name1} were structurally exposed — high defensive lines "
            f"({line0}m and {line1}m respectively) with passive pressing (PPDA {ppda0} and {ppda1}). "
            f"Either side had the space to exploit balls in behind. A match defined by mutual vulnerability."
        )
    # One False High Line
    if fhl0:
        return (
            f"{name0}'s False High Line ({line0}m, PPDA {ppda0}) was the key structural finding. "
            f"By contrast, {name1} were more coherent — {comp1} shape ({gap1}m between lines), "
            f"PPDA {ppda1}. {name0}'s exposure to balls in behind was the defining tactical risk of this match."
        )
    if fhl1:
        return (
            f"{name1}'s False High Line ({line1}m, PPDA {ppda1}) was the key structural finding. "
            f"By contrast, {name0} were more coherent — {comp0} shape ({gap0}m between lines), "
            f"PPDA {ppda0}. {name1}'s exposure to balls in behind was the defining tactical risk of this match."
        )
    # Both gapped
    if comp0 == "Gapped" and comp1 == "Gapped":
        bigger_gap = name0 if gap0 >= gap1 else name1
        bigger_m   = max(gap0, gap1)
        smaller_m  = min(gap0, gap1)
        return (
            f"Both teams left space between their lines — {name0} {gap0}m, {name1} {gap1}m. "
            f"{bigger_gap}'s {bigger_m}m gap was the larger structural opening. "
            f"Creative midfielders on either side had room to operate."
        )
    # One gapped, one compact
    if comp0 == "Gapped" and comp1 == "Compact":
        return (
            f"A clear structural contrast: {name0} were Gapped ({gap0}m between lines) while "
            f"{name1} were Compact ({gap1}m). {name1}'s tight structure gave them a defensive "
            f"advantage — {name0} were the team with the exploitable space."
        )
    if comp1 == "Gapped" and comp0 == "Compact":
        return (
            f"A clear structural contrast: {name1} were Gapped ({gap1}m between lines) while "
            f"{name0} were Compact ({gap0}m). {name0}'s tight structure gave them a defensive "
            f"advantage — {name1} were the team with the exploitable space."
        )
    # Both compact
    if comp0 == "Compact" and comp1 == "Compact":
        return (
            f"Both {name0} and {name1} maintained compact defensive shapes — {gap0}m and {gap1}m "
            f"between lines respectively. This was a match where structural vulnerability was low "
            f"for both sides; the decisive moments came from individual errors rather than systemic gaps."
        )
    # Fallback
    return (
        f"{name0}: {comp0} shape ({gap0}m gap, PPDA {ppda0}). "
        f"{name1}: {comp1} shape ({gap1}m gap, PPDA {ppda1}). "
        f"{'Neither team showed a clear structural vulnerability.' if comp0 != 'Gapped' and comp1 != 'Gapped' else 'The space between the lines was the key battleground.'}"
    )

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

def _render_exploit_pitch(teams_data: list) -> str:
    # Create two subplots side-by-side
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.patch.set_facecolor("#111827")
    fig.subplots_adjust(wspace=0.08)

    for i, (ax, td) in enumerate(zip(axes, teams_data)):
        # Draw a fresh pitch for each team
        pitch = Pitch(pitch_type="statsbomb", pitch_color="#111827",
                      line_color="#4B5563", linewidth=1.0)
        pitch.draw(ax=ax)

        if not td:
            continue
            
        def_x    = td["def_line_x_u"]
        mid_x    = td["mid_line_x_u"]
        gap_m    = td["gap_m"]
        comp     = td["comp_class"]
        false_hl = td["false_hl"]
        team     = td["team"]

        # 1. Band color is now strictly tied to compactness (Space Between)
        if comp == "Gapped":
            band_color, band_alpha = "#f59e0b", 0.12
        elif comp == "Compact":
            band_color, band_alpha = "#22c55e", 0.10
        else:
            band_color, band_alpha = "#6b7280", 0.08

        # Draw full pitch height shaded band
        ax.add_patch(plt.Rectangle(
            (min(def_x, mid_x), 0), width=abs(mid_x - def_x), height=80,
            facecolor=band_color, alpha=band_alpha, zorder=1))

        # 2. Add the False High Line warning aura BEHIND the blue line
        if false_hl:
            # Thick translucent red glow
            ax.plot([def_x, def_x], [0, 80], color="#ef4444", linewidth=12.0, linestyle="-", alpha=0.25, zorder=2)
            # Warning text near the top of the line
            ax.text(def_x - 2.5, 75, "⚠ EXPOSED", color="#ef4444", fontsize=6.5, fontweight="bold", alpha=0.90, ha="right")

        # 3. Always draw the standard dashed lines on top
        ax.plot([def_x, def_x], [0, 80], color="#3b82f6", linewidth=1.8, linestyle="--", alpha=0.80, zorder=3)
        ax.plot([mid_x, mid_x], [0, 80], color="#14b8a6", linewidth=1.8, linestyle="--", alpha=0.80, zorder=3)

        # Team Title
        ax.set_title(team.upper(), color="white", fontsize=9, fontweight="bold", pad=8)
        
        # Gap label centered inside the band
        mid_band = (def_x + mid_x) / 2
        gap_label_color = band_color if comp != "Standard" else "#9ca3af"
        ax.text(mid_band, 40, f"{gap_m}m\n({comp})",
                color=gap_label_color, fontsize=7.5, ha="center", va="center", fontweight="bold", alpha=0.90)

    handles = [
        mpatches.Patch(facecolor="#3b82f6", alpha=0.8, label="Defender line"),
        mpatches.Patch(facecolor="#14b8a6", alpha=0.8, label="Midfield line"),
        mpatches.Patch(facecolor="#f59e0b", alpha=0.6, label="Gapped — space between lines"),
        mpatches.Patch(facecolor="#22c55e", alpha=0.6, label="Compact — tight structure"),
        mpatches.Patch(facecolor="#ef4444", alpha=0.6, label="False High Line Indicator"),
    ]
    
    fig.legend(handles=handles, loc="lower center", ncol=5, fontsize=6.5,
               framealpha=0.20, facecolor="#111827", edgecolor="#374151",
               labelcolor="white", bbox_to_anchor=(0.5, -0.06))
    
    fig.tight_layout(rect=[0, 0.05, 1, 1]) 
    return fig_to_b64(fig)

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

# =============================================================================
# PATH 4 — THE DANGER MAP
#
# Jon Mackenzie framing: progression is only dangerous if it arrives
# in a zone that directly threatens goal. Volume of progressive passes
# is meaningless without clinical efficiency.
#
# Methodology:
#   Progressive pass: completed pass where Euclidean ΔD to goal
#     satisfies the 30-15-10 rule (zone-dependent threshold).
#   Danger corridor: x ∈ [88, 120], y ∈ [18, 62]
#     (full penalty box width + central shooting lane)
#   Clinical efficiency = danger corridor entries / total progressive passes
#
# Pitch render:
#   — Dim grey arrows: all progressive passes (the volume)
#   — Bright cyan arrows: progressive passes that entered the danger corridor
#   — Red shaded rectangle: the danger corridor zone
#   — Text annotation: clinical efficiency % per team
# =============================================================================

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



def _render_danger_pitch(teams_data: list) -> str:
    """
    Team A attacks right (normal StatsBomb orientation).
    Team B coordinates are mirrored (x -> 120-x, y -> 80-y)
    so they attack left — exactly like a real match.
    Both danger zones shown on their respective ends.
    """
    pitch, fig, ax = make_pitch(figsize=(10, 5))
    fig.patch.set_facecolor("#111827")

    dc = DANGER_CORRIDOR

    # Team A danger zone — right end (normal)
    ax.add_patch(plt.Rectangle(
        (dc["x_min"], dc["y_min"]),
        width  = dc["x_max"] - dc["x_min"],
        height = dc["y_max"] - dc["y_min"],
        facecolor="#ef4444", alpha=0.08, zorder=1,
        linewidth=1.0, edgecolor="#ef4444",
    ))

    # Team B danger zone — left end (mirrored: x 0-32, y 18-62)
    ax.add_patch(plt.Rectangle(
        (0, dc["y_min"]),
        width  = 120 - dc["x_min"],   # 32u wide from left
        height = dc["y_max"] - dc["y_min"],
        facecolor="#ef4444", alpha=0.08, zorder=1,
        linewidth=1.0, edgecolor="#ef4444",
    ))

    # Centre line label
    ax.text(60, 76, "← attack direction →",
            color="#374151", fontsize=6, alpha=0.6, ha="center")

    team_colors = [
        {"all": "#4b5563", "danger": "#00e5ff"},   # team A — cyan, attacks right
        {"all": "#44403c", "danger": "#a78bfa"},   # team B — warm grey / purple, attacks left
    ]

    for i, td in enumerate(teams_data):
        if not td or td["total_prog"] == 0:
            continue
        col = team_colors[i % 2]

        x1 = list(td["all_x1"])
        y1 = list(td["all_y1"])
        x2 = list(td["all_x2"])
        y2 = list(td["all_y2"])
        dx1 = list(td["danger_x1"])
        dy1 = list(td["danger_y1"])
        dx2 = list(td["danger_x2"])
        dy2 = list(td["danger_y2"])

        # Mirror team B coordinates so they attack left
        if i == 1:
            x1  = [120 - v for v in x1]
            y1  = [80  - v for v in y1]
            x2  = [120 - v for v in x2]
            y2  = [80  - v for v in y2]
            dx1 = [120 - v for v in dx1]
            dy1 = [80  - v for v in dy1]
            dx2 = [120 - v for v in dx2]
            dy2 = [80  - v for v in dy2]

        # All progressive passes — dim
        if x1:
            pitch.arrows(
                x1, y1, x2, y2,
                width=1.2, headwidth=6, headlength=6,
                color=col["all"], ax=ax, alpha=0.30, zorder=2,
            )

        # Danger corridor arrivals — bright
        if dx1:
            pitch.arrows(
                dx1, dy1, dx2, dy2,
                width=2, headwidth=10, headlength=10,
                color=col["danger"], ax=ax, alpha=0.90, zorder=3,
            )

        # Team label
        ly = 76 if i == 0 else 4
        lx = 62 if i == 0 else 2
        ax.text(
            lx, ly,
            f"{td['team'].upper()}  —  {td['danger_pct']}% clinical  ({td['danger_count']}/{td['total_prog']})",
            color=col["danger"], fontsize=7, alpha=0.85, fontweight="bold",
        )

    # Legend
    handles = [
        mpatches.Patch(facecolor="#4b5563", alpha=0.7, label="Progressive pass (non-dangerous)"),
        mpatches.Patch(facecolor="#00e5ff", alpha=0.8, label=f"{teams_data[0]['team']} — danger arrival (attacks right →)"),
        mpatches.Patch(facecolor="#a78bfa", alpha=0.8, label=f"{teams_data[1]['team']} — danger arrival (← attacks left)" if len(teams_data) > 1 else ""),
    ]
    fig.legend(handles=[h for h in handles if h.get_label()],
               loc="lower center", ncol=3, fontsize=6.5,
               framealpha=0.20, facecolor="#111827", edgecolor="#374151",
               labelcolor="white", bbox_to_anchor=(0.5, -0.08))
    fig.tight_layout()
    return fig_to_b64(fig)

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


def _danger_map_verdict(teams_data: list) -> str:
    """Dynamic two-team verdict for Danger Map."""
    valid = [td for td in teams_data if td and td.get("total_prog", 0) > 0]
    if not valid:
        return "Insufficient data."
    if len(valid) == 1:
        return valid[0].get("verdict", "")

    t0, t1     = valid[0], valid[1]
    n0, n1     = t0["team"], t1["team"]
    pct0, pct1 = t0["danger_pct"], t1["danger_pct"]
    tot0, tot1 = t0["total_prog"], t1["total_prog"]
    dc0, dc1   = t0["danger_count"], t1["danger_count"]
    gain0, gain1 = t0["avg_gain_m"], t1["avg_gain_m"]
    gap = abs(pct0 - pct1)
    more_clinical = n0 if pct0 >= pct1 else n1
    less_clinical = n1 if more_clinical == n0 else n0
    more_pct = max(pct0, pct1)
    less_pct = min(pct0, pct1)
    more_dc  = dc0 if more_clinical == n0 else dc1
    less_dc  = dc1 if more_clinical == n0 else dc0
    more_tot = tot0 if more_clinical == n0 else tot1
    less_tot = tot1 if more_clinical == n0 else tot0

    if gap >= 15:
        return (f"{more_clinical} were significantly more clinical — {more_pct}% of progressive passes "
                f"reached the danger corridor ({more_dc}/{more_tot}), compared to just {less_pct}% for "
                f"{less_clinical} ({less_dc}/{less_tot}). {less_clinical} moved the ball forward but "
                f"their progression repeatedly broke down before reaching a genuine threat position. "
                f"The {gap}% efficiency gap was the clearest tactical difference in this match.")
    elif gap >= 7:
        vol_leader = n0 if tot0 >= tot1 else n1
        vol_lagger = n1 if vol_leader == n0 else n0
        return (f"{more_clinical} edged clinical efficiency ({more_pct}% vs {less_pct}%). "
                f"{vol_leader} dominated in volume with {max(tot0,tot1)} progressive passes vs "
                f"{min(tot0,tot1)} for {vol_lagger}. "
                f"The combination of volume and efficiency tells the full story of who controlled progression.")
    elif abs(tot0 - tot1) >= 20:
        vol_leader = n0 if tot0 >= tot1 else n1
        vol_lagger = n1 if vol_leader == n0 else n0
        return (f"Clinical efficiency was similar — {pct0}% vs {pct1}% — but {vol_leader} "
                f"generated far more progressive passes ({max(tot0,tot1)} vs {min(tot0,tot1)}). "
                f"Volume of ball progression, not efficiency, was the key differentiator. "
                f"Average gain per pass: {gain0}m ({n0}) vs {gain1}m ({n1}).")
    else:
        return (f"Both teams were closely matched in danger corridor efficiency — {n0} {pct0}% "
                f"({dc0}/{tot0}) vs {n1} {pct1}% ({dc1}/{tot1}). "
                f"Average ground gained per progressive pass: {gain0}m vs {gain1}m. "
                f"Neither side found a clear edge in turning possession into genuine threat.")


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


# =============================================================================
# PATH 5 — THE PROGRESS TRAP
# =============================================================================

# Share of a team's completed progressive passes that start in the wide channels
# (|y-40| > 20). Over 292 team-matches it runs 26-59% (median 42%, 90th
# percentile 52%), so the old 60% cut-off could never be reached: the
# "forced wide" verdict fired for 0% of teams. Set at the 90th percentile,
# so only the clear outliers are called out (10.6%).
FORCED_WIDE_MIN    = 52
FORCED_WIDE_MARGIN = 10   # the other team must be this many points less wide

def _progress_trap_verdict(teams_data: list) -> str:
    valid = [td for td in teams_data if td and td.get("total_attempts", 0) > 0]
    if not valid:
        return "Insufficient data."
    if len(valid) == 1:
        return valid[0].get("verdict", "")

    t0, t1   = valid[0], valid[1]
    n0, n1   = t0["team"], t1["team"]
    sr0, sr1 = t0["stall_rate"], t1["stall_rate"]
    zone0, zone1   = t0["primary_stall_zone"], t1["primary_stall_zone"]
    block0, block1 = t0["block_depth_m"], t1["block_depth_m"]
    label0, label1 = t0["block_label"], t1["block_label"]
    wide0, wide1   = t0["forced_wide_pct"], t1["forced_wide_pct"]

    stall_gap    = abs(sr0 - sr1)
    deeper_block = n0 if block0 <= block1 else n1
    deeper_m     = min(block0, block1)
    shallower_m  = max(block0, block1)
    higher_stall = n0 if sr0 >= sr1 else n1
    lower_stall  = n1 if higher_stall == n0 else n0
    higher_sr    = max(sr0, sr1)
    lower_sr     = min(sr0, sr1)

    if stall_gap >= 20:
        return (f"A sharp contrast in progression efficiency. {higher_stall} stalled on {higher_sr}% "
                f"of forward passes — primarily in the {zone0 if higher_stall==n0 else zone1} — "
                f"facing {deeper_block}'s block at {deeper_m}m. "
                f"{lower_stall}, by contrast, stalled on only {lower_sr}% despite facing a block at {shallower_m}m. "
                f"The difference in press resistance and build-up quality was decisive.")
    elif sr0 >= 40 and sr1 >= 40:
        return (f"Both teams struggled to progress the ball — {n0} {sr0}% stall rate, {n1} {sr1}%. "
                f"Forced wide percentages: {n0} {wide0}%, {n1} {wide1}%. "
                f"This was a match where the central corridor was largely shut down for both sides.")
    elif wide0 >= FORCED_WIDE_MIN and wide1 <= wide0 - FORCED_WIDE_MARGIN:
        return (f"{n0} were consistently forced wide ({wide0}% of completions) "
                f"while {n1} found the central route more accessible ({wide1}% forced wide). "
                f"Block depths: {n0} facing {block1}m ({label1}), {n1} facing {block0}m ({label0}).")
    elif wide1 >= FORCED_WIDE_MIN and wide0 <= wide1 - FORCED_WIDE_MARGIN:
        return (f"{n1} were consistently forced wide ({wide1}% of completions) "
                f"while {n0} found the central route more accessible ({wide0}% forced wide). "
                f"Block depths: {n1} facing {block0}m ({label0}), {n0} facing {block1}m ({label1}).")
    else:
        return (f"{n0}: {sr0}% stall rate (primary zone: {zone0}), block facing them {block1}m ({label1}), {wide0}% forced wide. "
                f"{n1}: {sr1}% stall rate (primary zone: {zone1}), block facing them {block0}m ({label0}), {wide1}% forced wide. "
                f"{'Both teams found progression similarly challenging.' if stall_gap < 10 else f'{lower_stall} were the more effective ball progressors.'}")


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


def _block_line_x(block_x_u: float) -> float:
    """
    block_x_u is the opponent's defensive-line x in the opponent's own frame
    (their goal at x=0). The pitch is drawn in the attacking team's frame,
    where that same goal is at x=120, so the line must be mirrored.
    """
    return 120.0 - block_x_u


def _render_progress_trap_pitch(teams_data: list) -> str:
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.patch.set_facecolor("#111827")
    fig.subplots_adjust(wspace=0.06)
    team_accent = ["#00e5ff", "#a78bfa"]

    for i, (ax, td) in enumerate(zip(axes, teams_data)):
        accent = team_accent[i % 2]
        pitch  = Pitch(pitch_type="statsbomb", pitch_color="#111827",
                       line_color="#4B5563", linewidth=1.0)
        pitch.draw(ax=ax)

        if not td or td["total_attempts"] == 0:
            ax.set_title(td.get("team", ""), color="white", fontsize=9, pad=6)
            continue

        for x_start, x_end, alpha in [(0,40,0.04),(40,80,0.02),(80,120,0.03)]:
            ax.add_patch(plt.Rectangle((x_start,0), width=x_end-x_start, height=80,
                         facecolor="#ffffff", alpha=alpha, zorder=1))

        zone_colors = {"Defensive Third":"#ef4444","Middle Third":"#f59e0b","Final Third":"#a78bfa"}
        stall_df = pd.DataFrame({"x": td["stall_x"], "y": td["stall_y"]})
        if not stall_df.empty:
            stall_df["zone"] = stall_df["x"].apply(
                lambda x: "Defensive Third" if x < 40 else ("Middle Third" if x < 80 else "Final Third"))
            for zone, color in zone_colors.items():
                z = stall_df[stall_df["zone"] == zone]
                if not z.empty:
                    ax.scatter(z["x"], z["y"], marker="x", s=35, color=color,
                               alpha=0.65, linewidths=1.4, zorder=3)

        block_x = _block_line_x(td["block_x_u"])
        ax.axvline(x=block_x, color="#fbbf24", linewidth=1.8, linestyle="--", alpha=0.70, zorder=4)
        ax.text(block_x-0.8, 74, f"block {td['block_depth_m']}m", ha="right",
                color="#fbbf24", fontsize=6.5, alpha=0.85, fontweight="bold")

        ax.set_title(f"{td['team']}  —  {td['stall_rate']}% stall rate  ({td['stalled_count']}/{td['total_attempts']} attempts)",
                     color=accent, fontsize=8, fontweight="bold", pad=6)

        stall_df2 = pd.DataFrame({"x": td["stall_x"]})
        if not stall_df2.empty:
            d3 = int((stall_df2["x"] < 40).sum())
            m3 = int(((stall_df2["x"] >= 40) & (stall_df2["x"] < 80)).sum())
            f3 = int((stall_df2["x"] >= 80).sum())
            ax.text(2, 4, f"Def: {d3}  |  Mid: {m3}  |  Final: {f3}",
                    color="#9ca3af", fontsize=6.5, alpha=0.70)

    handles = [
        plt.Line2D([0],[0], marker="x", color="#ef4444", markersize=7, linewidth=0, label="Stalled — Defensive Third"),
        plt.Line2D([0],[0], marker="x", color="#f59e0b", markersize=7, linewidth=0, label="Stalled — Middle Third"),
        plt.Line2D([0],[0], marker="x", color="#a78bfa", markersize=7, linewidth=0, label="Stalled — Final Third"),
        plt.Line2D([0],[0], color="#fbbf24", linewidth=1.5, linestyle="--", label="Opponent block depth"),
    ]
    fig.legend(handles=handles, loc="lower center", ncol=4, fontsize=6.5,
               framealpha=0.20, facecolor="#111827", edgecolor="#374151",
               labelcolor="white", bbox_to_anchor=(0.5, -0.06))
    fig.tight_layout()
    return fig_to_b64(fig)


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