"""
Calibrate and validate the PPDA classification thresholds in api.py.

    python scripts/calibrate_ppda.py --cache <dir>

What it does, over every team-match in the frontend match index:

1. CALIBRATION. The original Aggressive / Moderate / Passive cut-offs (2.5 and
   4.4, plus a 3.5 "pressed hard" gate) were tuned to a PPDA that mostly counted
   Pressure events and read the pressing team's own half. Those cut-offs
   corresponded to percentiles of that old distribution. The script recomputes
   the old metric (kept below as legacy_ppda, for this comparison only), finds
   the percentile each old cut-off sat at, and reports the value at the same
   percentile of the corrected metric. That is how 2.5 / 3.5 / 4.4 became
   9 / 14 / 20 in api.py.

2. CURRENT SPLIT. The label shares metrics.classify_ppda gives today, overall and
   per tournament.

3. VALIDATION. Spearman rank correlation between metrics.compute_ppda and a
   separately written standard-definition PPDA (Opta style: opponent passes in
   their own 60% of the pitch over tackles, interceptions, fouls and
   challenges in the opposition's 60%).

The thresholds are percentile-based on this dataset (three tournaments). They
are not an absolute external standard: another competition, or the same
tournaments with a different mix of opponents, would shift the distribution.
"""
import argparse
import os
import sys
import tempfile
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
import pandas as pd

from sideline import metrics
from audit_labels import load_events, match_index

OLD_THRESHOLDS = {"aggressive_max": 2.5, "pressed_gate": 3.5, "moderate_max": 4.4}


def _loc_x(df):
    return df["location"].apply(lambda l: float(l[0]) if isinstance(l, (list, tuple)) else np.nan)


def legacy_ppda(df, team):
    """The pre-fix definition. Kept only to recover the percentiles the old
    cut-offs sat at. 'Tackle' is not a StatsBomb event type, and x <= 60 on the
    pressing team's own frame selects its own half."""
    opp = next((t for t in df["team"].dropna().unique() if t != team), None)
    if opp is None:
        return np.nan
    x = _loc_x(df)
    in_play = df["period"] != 5
    passes = ((df["team"] == opp) & (df["type"] == "Pass") & in_play & (x <= 60)).sum()
    acts = ((df["team"] == team) & df["type"].isin(["Tackle", "Interception", "Pressure"]) & in_play & (x <= 60)).sum()
    return passes / acts if acts else np.nan


def standard_ppda(df, team):
    """Opta-style PPDA, written independently of metrics.compute_ppda: all opponent
    passes in their own 60% of the pitch, over the pressing team's tackles,
    interceptions, fouls and challenges (StatsBomb 'Dribbled Past') in the
    opposition's 60%. Each team's events are in that team's own frame."""
    opp = next((t for t in df["team"].dropna().unique() if t != team), None)
    if opp is None:
        return np.nan
    x = _loc_x(df)
    in_play = df["period"] != 5
    passes = ((df["team"] == opp) & (df["type"] == "Pass") & in_play & (x <= 0.60 * 120)).sum()
    tackle = (df["type"] == "Duel") & (df["duel_type"] == "Tackle")
    action = tackle | df["type"].isin(["Interception", "Foul Committed", "Dribbled Past"])
    acts = ((df["team"] == team) & action & in_play & (x >= 0.40 * 120)).sum()
    return passes / acts if acts else np.nan


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default=str(Path(tempfile.gettempdir()) / "sideline_audit_cache"))
    a = ap.parse_args()
    os.makedirs(a.cache, exist_ok=True)

    rows = []
    for comp, stage, mid in match_index():
        df = load_events(mid, a.cache)
        for team in metrics.get_teams(df)[:2]:
            ppda = metrics.compute_ppda(df, team)
            rows.append(dict(match=mid, comp=comp, team=team, ppda=ppda,
                             label=metrics.classify_ppda(ppda),
                             legacy=legacy_ppda(df, team), standard=standard_ppda(df, team)))
    R = pd.DataFrame(rows)
    R = R.replace([np.inf, -np.inf], np.nan)
    n_matches = R["match"].nunique()
    print(f"{n_matches} matches, {len(R)} team-matches\n")

    print("== 1. CALIBRATION (old cut-offs -> same percentile of the corrected metric) ==")
    legacy = R["legacy"].dropna()
    new = R["ppda"].dropna()
    print(f"legacy PPDA  p5/25/50/75/95 = {np.round(np.percentile(legacy, [5, 25, 50, 75, 95]), 2)}")
    print(f"corrected    p5/25/50/75/95 = {np.round(np.percentile(new, [5, 25, 50, 75, 95]), 1)}")
    for name, thr in OLD_THRESHOLDS.items():
        pct = 100 * (legacy < thr).mean()
        print(f"  old {name:<15}{thr:>4}: percentile {pct:5.1f} -> corrected value {np.percentile(new, pct):5.1f}")
    print(f"current api.py constants: aggressive < {metrics.PPDA_AGGRESSIVE_MAX:g}, "
          f"moderate < {metrics.PPDA_MODERATE_MAX:g}, pressed-hard gate <= {metrics.PPDA_PRESSED_MAX:g}")

    print("\n== 2. CURRENT LABEL SPLIT ==")
    share = (100 * R["label"].value_counts(normalize=True)).round(0).astype(int)
    print("overall:", " | ".join(f"{k} {v}%" for k, v in share.items()))
    print("by tournament (% of team-matches):")
    print((100 * pd.crosstab(R["comp"], R["label"], normalize="index")).round(0).astype(int).to_string())

    print("\n== 3. VALIDATION vs an independent standard-definition PPDA ==")
    both = R[["ppda", "standard"]].dropna()
    rho = both["ppda"].corr(both["standard"], method="spearman")
    print(f"Spearman rank correlation, metrics.compute_ppda vs standard definition: {rho:.2f} (n={len(both)})")
    print(f"standard-definition PPDA p5/25/50/75/95 = {np.round(np.percentile(both['standard'], [5, 25, 50, 75, 95]), 1)}")


if __name__ == "__main__":
    main()
