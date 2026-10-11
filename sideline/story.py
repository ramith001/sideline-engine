"""
Auto-Story engine: detects the highest-drama tactical moment of a match and
writes the thread and hooks, using the half-time score as context.

Five story detectors, each scored on a 0-10 drama scale:
  1. MOMENTUM_SHIFT     - biggest change in progressive pass rate per half
  2. FALSE_HIGH_LINE    - high defensive line + passive press
  3. PRESS_BYPASS       - an aggressive press beaten with dangerous exits
  4. SHAPE_COLLAPSE     - defensive line drops/rises sharply between halves
  5. CLINICAL_SURGE     - one team significantly more dangerous per pass
The highest-scoring story wins and generates the narrative.
"""

import pandas as pd

from sideline.metrics import (
    METERS,
    PPDA_MODERATE_MAX,
    PPDA_PRESSED_MAX,
    _classify_vertical,
    _defensive_lines,
    _get_press_breaking_passes,
    _get_progressive_passes,
    classify_ppda,
    compute_ppda,
    euclidean_to_goal,
    get_defensive_events,
)


# Game state. A defensive line or a progression rate that moves after half-time
# is often just the scoreline (leading teams sit deeper, trailing teams push
# up), so a story must know the half-time score before it blames tactics.
SHIFT_EXPLAINED_WEIGHT = 0.5   # drama weight of a line shift the half-time score explains


def _goals_scored(df: pd.DataFrame, team: str, periods: list) -> int:
    """Goals credited to `team` in the given periods: its shots that scored plus
    own goals scored against the other side."""
    in_periods = df["period"].isin(periods) & (df["team"] == team)
    shots = df[in_periods & (df["type"] == "Shot")]
    # Plain iteration, not Series.apply(...).sum(): on an empty selection pandas
    # can infer a string dtype for the result, and its sum() is '' rather than 0.
    scored = sum(
        (o.get("name") == "Goal") if isinstance(o, dict) else (o == "Goal")
        for o in shots["shot_outcome"]
    )
    return int(scored) + int((in_periods & (df["type"] == "Own Goal For")).sum())


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


# A press-bypass story needs the bypass to have actually worked. Over 292
# team-matches the exit rate (press-breaking passes / passes under pressure) runs
# 0-21%, median 6.2%, 75th percentile 8.4%. Previously only the opponent's PPDA
# gated the story and it supplied most of the drama, so a team that escaped 4% of
# the time still got "textbook press resistance" (77% of teams facing a hard
# press were eligible, 36% even in the bottom quartile of exit rate).
PRESS_BYPASS_MIN_EXIT_RATE = 8.5   # % of passes under pressure, ~75th percentile


PRESS_BYPASS_MIN_EXITS     = 5     # and enough actual exits that it is not 3 passes


def _auto_story_press_bypass(df: pd.DataFrame, teams: list) -> dict:
    """Detect team being pressed hard AND escaping effectively."""
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

        exit_pct = (len(pb) / total_under) * 100
        if exit_pct < PRESS_BYPASS_MIN_EXIT_RATE or len(pb) < PRESS_BYPASS_MIN_EXITS:
            continue
        exit_rate = round(exit_pct)
        avg_gain  = round(float(pb["delta_d"].mean()) * METERS, 1) if not pb.empty else 0

        # Drama: how good the bypass was (main driver) vs how hard the press was
        drama = min(round(exit_pct * 0.3 + (40 - opp_ppda) * 0.05, 1), 10.0)

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
        headline  = f"{team} broke {opp}'s press {exits} times — {exit_rate}% of passes under pressure (PPDA {opp_ppda})"
        hook      = f"{team} still found forward exits through {opp}'s press..."
        tweets    = [
            f"1/ {opp} pressed with a PPDA of {opp_ppda} ({classify_ppda(opp_ppda).lower()}).",
            f"2/ {team} still broke that press {exits} times under pressure, "
            f"each exit gaining an average of {gain_m}m toward goal: {exit_rate}% of their passes "
            f"under pressure, well above the typical rate.",
            f"3/ Resisting a press is one thing; turning it into forward progress is another. "
            f"The exit rate is the measure of whether it worked.",
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
        "twitter_hook":        hook,
        "twitter_thread":      tweets,
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
