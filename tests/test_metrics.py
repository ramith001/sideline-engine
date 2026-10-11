"""
Unit tests for the PPDA metric and its classifier in api.py.

All data is synthetic and hand-built: no network, no StatsBomb download.
StatsBomb events are stored in each team's own frame (every team attacks
towards x=120), so a pressing team's actions count at x >= PPDA_PRESS_MIN_X
and the opponent's passes count at x <= PPDA_PASS_MAX_X.
"""
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.axes
import pandas as pd
import pytest

from api import (
    PPDA_AGGRESSIVE_MAX,
    PPDA_MODERATE_MAX,
    PPDA_PASS_MAX_X,
    PPDA_PRESS_MIN_X,
    classify_ppda,
    compute_ppda,
    _defensive_lines,
    _exploit_finder_for_team,
    get_defensive_events,
)

PRESS, OPP = "Pressers", "Opponents"
MID = (PPDA_PRESS_MIN_X + PPDA_PASS_MAX_X) / 2   # a safely in-zone x for both


def ev(team, type_, x, *, duel_type=None, incomplete=False, period=1, position=None, y=40.0):
    """One synthetic event row with only the columns compute_ppda reads."""
    return {
        "team": team,
        "type": type_,
        "location": [float(x), float(y)],
        "duel_type": duel_type,
        "pass_outcome": "Incomplete" if incomplete else None,
        "period": period,
        "position": position,
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


# ── Defensive events (defensive-line height) ──────────────────────────────────

def test_tackle_duels_are_defensive_events():
    # StatsBomb has no "Tackle" event type; a tackle is a Duel row with
    # duel_type == "Tackle". It must feed the defensive-line calculation.
    df = frame(
        ev(PRESS, "Duel", 30, duel_type="Tackle"),
        ev(PRESS, "Duel", 50, duel_type="Tackle"),
        ev(PRESS, "Pass", 90),
        ev(OPP, "Duel", 70, duel_type="Tackle"),
    )
    out = get_defensive_events(df, PRESS)
    assert out["loc_x"].tolist() == [30.0, 50.0]   # own tackles only, no passes


def test_defensive_events_exclude_shootout_and_other_types():
    df = frame(
        ev(PRESS, "Interception", 40),
        ev(PRESS, "Duel", 20, duel_type="Tackle", period=5),   # shootout
        ev(PRESS, "Carry", 60),
        ev(PRESS, "Shot", 100),
    )
    assert get_defensive_events(df, PRESS)["loc_x"].tolist() == [40.0]


# ── Progress Trap block line (coordinate frame) ───────────────────────────────

def _progress_trap_td(team, block_x_u):
    return {
        "team": team, "total_attempts": 10, "stalled_count": 4, "stall_rate": 40,
        "stall_x": [20.0, 60.0, 100.0], "stall_y": [30.0, 40.0, 50.0],
        "block_x_u": block_x_u, "block_depth_m": round(block_x_u * 0.875, 1),
    }


def test_progress_trap_block_line_is_mirrored_into_attackers_frame(monkeypatch):
    # block_x_u is the opponent's line in the opponent's own frame (their goal
    # at x=0). The pitch is the attacker's frame (that goal is at x=120), so a
    # deep block at x=15 must be drawn at x=105, next to the goal being
    # attacked, not at x=15 inside the attacker's own half.
    from api import _render_progress_trap_pitch

    drawn = []
    real = matplotlib.axes.Axes.axvline

    def spy(self, x=0, *a, **kw):
        drawn.append(x)
        return real(self, x, *a, **kw)

    monkeypatch.setattr(matplotlib.axes.Axes, "axvline", spy)
    _render_progress_trap_pitch([_progress_trap_td("A", 15.0), _progress_trap_td("B", 40.0)])
    assert drawn == [105.0, 80.0]


def test_block_line_mirror_helper():
    from api import _block_line_x
    assert _block_line_x(15.0) == 105.0
    assert _block_line_x(60.0) == 60.0     # halfway line maps to itself
    assert _block_line_x(0.0) == 120.0


# ── Gap between lines (compactness) ───────────────────────────────────────────

def _line_events(n, x, position, type_="Pressure", team=PRESS):
    return [ev(team, type_, x, position=position) for _ in range(n)]


def test_defensive_lines_are_where_each_line_defends():
    df = frame(
        *_line_events(10, 30, "Left Center Back"),
        *_line_events(10, 34, "Right Back"),          # defenders: mean 32
        *_line_events(10, 46, "Center Defensive Midfield"),
        *_line_events(10, 50, "Left Center Midfield"),  # midfielders: mean 48
        *_line_events(10, 95, "Center Forward"),        # forwards belong to neither line
        *_line_events(10, 2, "Goalkeeper"),
    )
    back, mid = _defensive_lines(get_defensive_events(df, PRESS))
    assert (back, mid) == (32.0, 48.0)


def test_defensive_lines_need_enough_actions_from_both_lines():
    df = frame(*_line_events(10, 30, "Left Center Back"),
               *_line_events(2, 48, "Center Defensive Midfield"))
    assert _defensive_lines(get_defensive_events(df, PRESS)) is None


def test_gap_between_lines_ignores_events_from_other_players():
    # Regression: the gap used to be P60 - P15 of ALL defensive event x, i.e. a
    # spread of event positions. Lines that sit level (gap 0) must read as
    # Compact no matter how many high-up events other players contribute.
    df = frame(
        *opp_passes(10),
        *_line_events(10, 30, "Left Center Back"),
        *_line_events(10, 30, "Center Defensive Midfield"),
        *_line_events(60, 100, "Center Forward"),   # drags the old P60 far upfield
    )
    td = _exploit_finder_for_team(df, PRESS)
    assert td["gap_m"] == 0.0
    assert td["comp_class"] == "Compact"


def test_gap_between_lines_value_and_classification():
    # defenders defend at x=30, midfielders at x=45: 15 units = 13.1m (Standard)
    df = frame(
        *opp_passes(10),
        *_line_events(10, 30, "Left Center Back"),
        *_line_events(10, 45, "Center Defensive Midfield"),
    )
    td = _exploit_finder_for_team(df, PRESS)
    assert td["gap_m"] == pytest.approx(13.1, abs=0.05)
    assert td["comp_class"] == "Standard"
    wide = frame(
        *opp_passes(10),
        *_line_events(10, 20, "Left Center Back"),
        *_line_events(10, 50, "Center Defensive Midfield"),   # 30 units = 26.2m
    )
    assert _exploit_finder_for_team(wide, PRESS)["comp_class"] == "Gapped"


def test_exploit_finder_returns_nothing_without_a_midfield_line():
    df = frame(*opp_passes(5), *_line_events(10, 30, "Left Center Back"))
    assert _exploit_finder_for_team(df, PRESS) == {}
