"""
Unit tests for the PPDA metric and its classifier in api.py.

All data is synthetic and hand-built: no network, no StatsBomb download.
StatsBomb events are stored in each team's own frame (every team attacks
towards x=120), so a pressing team's actions count at x >= PPDA_PRESS_MIN_X
and the opponent's passes count at x <= PPDA_PASS_MAX_X.
"""
import math

import pandas as pd
import pytest

from api import (
    PPDA_AGGRESSIVE_MAX,
    PPDA_MODERATE_MAX,
    PPDA_PASS_MAX_X,
    PPDA_PRESS_MIN_X,
    classify_ppda,
    compute_ppda,
)

PRESS, OPP = "Pressers", "Opponents"
MID = (PPDA_PRESS_MIN_X + PPDA_PASS_MAX_X) / 2   # a safely in-zone x for both


def ev(team, type_, x, *, duel_type=None, incomplete=False, period=1):
    """One synthetic event row with only the columns compute_ppda reads."""
    return {
        "team": team,
        "type": type_,
        "location": [float(x), 40.0],
        "duel_type": duel_type,
        "pass_outcome": "Incomplete" if incomplete else None,
        "period": period,
    }


def frame(*rows):
    return pd.DataFrame(list(rows))


def opp_passes(n, x=MID, **kw):
    return [ev(OPP, "Pass", x, **kw) for _ in range(n)]


def press_actions(n, type_="Interception", x=MID, **kw):
    return [ev(PRESS, type_, x, **kw) for _ in range(n)]


# ── PPDA value ────────────────────────────────────────────────────────────────

def test_known_value_by_hand():
    # Hand count. Denominator: 12 completed opponent passes inside their own
    # defensive two-thirds. Numerator: 1 interception + 1 foul + 1 tackle duel
    # by the pressing team in the opponent's defensive two-thirds = 3.
    # 12 / 3 = 4.0. Noise that must not change it: 2 opponent passes beyond
    # PPDA_PASS_MAX_X, 1 incomplete pass, and a pressing-team pass.
    df = frame(
        *opp_passes(12),
        ev(PRESS, "Interception", 60),
        ev(PRESS, "Foul Committed", 50),
        ev(PRESS, "Duel", 45, duel_type="Tackle"),
        *opp_passes(2, x=PPDA_PASS_MAX_X + 10),
        ev(OPP, "Pass", 30, incomplete=True),
        ev(PRESS, "Pass", 70),
    )
    assert compute_ppda(df, PRESS) == 4.0


def test_pressure_events_are_not_counted():
    base = frame(*opp_passes(12), *press_actions(3))
    with_pressure = frame(
        *opp_passes(12), *press_actions(3), *press_actions(50, type_="Pressure")
    )
    assert compute_ppda(base, PRESS) == 4.0
    assert compute_ppda(with_pressure, PRESS) == compute_ppda(base, PRESS)


def test_tackle_duel_counts_other_duels_do_not():
    passes = opp_passes(10)
    tackle = frame(*passes, ev(PRESS, "Duel", MID, duel_type="Tackle"))
    aerial = frame(*passes, ev(PRESS, "Duel", MID, duel_type="Aerial Lost"))
    assert compute_ppda(tackle, PRESS) == 10.0            # 10 / 1
    assert compute_ppda(aerial, PRESS) == float("inf")    # 0 actions


def test_works_without_duel_type_column():
    df = frame(*opp_passes(8), *press_actions(2)).drop(columns=["duel_type"])
    assert compute_ppda(df, PRESS) == 4.0


# ── Zone / coordinate frame ───────────────────────────────────────────────────

def test_press_action_zone_boundary():
    passes = opp_passes(10)
    below = frame(*passes, ev(PRESS, "Interception", PPDA_PRESS_MIN_X - 0.1))
    at = frame(*passes, ev(PRESS, "Interception", PPDA_PRESS_MIN_X))
    assert compute_ppda(below, PRESS) == float("inf")   # own half: not counted
    assert compute_ppda(at, PRESS) == 10.0               # counted


def test_press_actions_deep_in_own_half_are_ignored():
    # Regression for the old flipped frame (x <= 60 selected the pressing
    # team's own half): a defensive action near their own goal must not count.
    df = frame(*opp_passes(10), ev(PRESS, "Interception", 15),
               ev(PRESS, "Duel", 20, duel_type="Tackle"))
    assert compute_ppda(df, PRESS) == float("inf")


def test_opponent_pass_zone_boundary():
    action = [ev(PRESS, "Interception", MID)]
    inside = frame(*action, ev(OPP, "Pass", PPDA_PASS_MAX_X))
    outside = frame(*action, ev(OPP, "Pass", PPDA_PASS_MAX_X + 0.1))
    assert compute_ppda(inside, PRESS) == 1.0    # 1 pass / 1 action
    assert compute_ppda(outside, PRESS) == 0.0   # pass not counted


# ── Completed passes only ─────────────────────────────────────────────────────

def test_only_completed_passes_count():
    action = [ev(PRESS, "Interception", MID)]
    completed = frame(*action, ev(OPP, "Pass", 30))
    incomplete = frame(*action, ev(OPP, "Pass", 30, incomplete=True))
    assert compute_ppda(completed, PRESS) == 1.0
    assert compute_ppda(incomplete, PRESS) == 0.0


# ── Other behaviour ───────────────────────────────────────────────────────────

def test_penalty_shootout_events_are_excluded():
    df = frame(*opp_passes(10), *press_actions(2),
               *opp_passes(5, period=5), *press_actions(5, period=5))
    assert compute_ppda(df, PRESS) == 5.0   # 10 / 2, shootout rows ignored


def test_no_defensive_actions_is_infinite():
    assert math.isinf(compute_ppda(frame(*opp_passes(10), ev(PRESS, "Pass", MID)), PRESS))


def test_missing_opponent_is_infinite():
    assert math.isinf(compute_ppda(frame(*press_actions(3)), PRESS))


# ── Classifier ────────────────────────────────────────────────────────────────

@pytest.mark.parametrize(
    "value, label",
    [
        (0.0, "Aggressive Press"),
        (PPDA_AGGRESSIVE_MAX - 0.01, "Aggressive Press"),
        (PPDA_AGGRESSIVE_MAX, "Moderate Press"),
        (PPDA_AGGRESSIVE_MAX + 0.01, "Moderate Press"),
        (PPDA_MODERATE_MAX - 0.01, "Moderate Press"),
        (PPDA_MODERATE_MAX, "Passive / Low Press"),
        (PPDA_MODERATE_MAX + 0.01, "Passive / Low Press"),
        (float("inf"), "Passive / Low Press"),
    ],
)
def test_classify_ppda_boundaries(value, label):
    assert classify_ppda(value) == label


def test_thresholds_are_ordered():
    assert 0 < PPDA_AGGRESSIVE_MAX < PPDA_MODERATE_MAX
    assert PPDA_PRESS_MIN_X < PPDA_PASS_MAX_X   # the zones overlap, by design
