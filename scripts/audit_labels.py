"""
Audit every verdict / label producing function in api.py across the whole
match index and print, for each one, the distribution of the underlying
number and the share of team-matches (or matches) that get each label.

A label that fires for ~100% (or ~0%) of teams is degenerate: it carries no
information. Run this before and after changing any threshold or definition.

    python scripts/audit_labels.py --cache <dir> [--csv out.csv]

Match ids are read from MATCH_INDEX in components/main-content.tsx. Event
data comes from StatsBomb open data and is cached in --cache (outside the repo)
so repeat runs need no network.
"""
import argparse
import os
import pickle
import re
import sys
import tempfile
import warnings
from collections import Counter, defaultdict
from pathlib import Path

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import api

PCTS = [0, 5, 25, 50, 75, 95, 100]


class Req:
    mode = "audit"

    def __init__(self, match_id, template):
        self.match_id = match_id
        self.template = template


def match_index():
    """[(competition, stage, match_id)] parsed from the frontend match index."""
    src = (ROOT / "components" / "main-content.tsx").read_text(encoding="utf-8")
    block = src[src.index("const MATCH_INDEX"):src.index("const STAGES")]
    out, stage = [], None
    for line in block.splitlines():
        m = re.match(r'\s*"([^"]+ · [^"]+)":\s*\[', line)
        if m:
            stage = m.group(1)
        for mid in re.findall(r"id:\s*(\d+)", line):
            out.append((stage.split(" · ")[0], stage, int(mid)))
    return out


def load_events(mid, cache):
    path = Path(cache) / f"{mid}.pkl"
    if path.exists():
        return pickle.loads(path.read_bytes())
    from statsbombpy import sb

    df = sb.events(match_id=mid)
    path.write_bytes(pickle.dumps(df))
    return df


def bucket(text, teams):
    """Verdict text with team names and numbers masked, so equal verdict
    templates group together."""
    t = text or ""
    for name in sorted(teams, key=len, reverse=True):
        t = t.replace(name, "TEAM")
    t = re.sub(r"\d+(\.\d+)?", "#", t)
    return t[:75]


def team_rows(df, comp, stage, mid):
    teams = api.get_teams(df)[:2]
    rows = []
    for team in teams:
        opp = next((t for t in teams if t != team), None)
        if opp is None:
            continue
        r = dict(match=mid, comp=comp, stage=stage, team=team)

        ppda = api.compute_ppda(df, team)
        r["ppda"], r["press_class"] = ppda, api.classify_ppda(ppda)

        ex = api._exploit_finder_for_team(df, team)
        if ex:
            de = api.get_defensive_events(df, team)
            r["avg_x_m"] = ex["avg_line_m"]
            r["vertical"] = ex["v_state"]
            r["h_offset_u"] = ex.get("h_offset_u", float((de["loc_y"] - 40.0).abs().mean()))
            r["horizontal"] = ex["h_state"]
            r["gap_m"] = ex["gap_m"]
            r["compactness"] = ex["comp_class"]
            r["exploit_label"] = ex["risk_label"]

        pt = api._progress_trap_for_team(df, team, opp)
        if pt.get("total_attempts"):
            r["block_depth_m"] = pt["block_depth_m"]
            r["block_label"] = pt["block_label"]
            r["stall_rate"] = pt["stall_rate"]
            r["forced_wide_pct"] = pt["forced_wide_pct"]
            v = pt["verdict"]
            r["trap_verdict"] = (
                "pinned in own half" if "pinned in their own half" in v else
                "hit a wall (final third)" if "hit a wall" in v else
                "forced wide" if "consistently forced wide" in v else
                "progressed efficiently" if "progressed efficiently" in v else
                "generic stall/zone summary")

        dm = api._danger_map_for_team(df, team)
        if dm.get("total_prog"):
            r["danger_pct"] = dm["danger_pct"]
            r["efficiency"] = dm["efficiency_class"]
        rows.append(r)
    return rows


def match_row(df, comp, stage, mid):
    teams = api.get_teams(df)
    r = dict(match=mid, comp=comp, stage=stage)
    det = {
        "momentum_shift": api._auto_story_momentum_shift(df, teams),
        "false_high_line": api._auto_story_false_high_line(df, teams),
        "press_bypass": api._auto_story_press_bypass(df, teams),
        "shape_collapse": api._auto_story_shape_collapse(df, teams),
        "clinical_surge": api._auto_story_clinical_surge(df, teams),
    }
    for k, v in det.items():
        r[f"drama_{k}"] = v.get("drama_score") if v else np.nan
    r["outcome_floor"] = api._get_match_outcome_floor(df)
    story = api.generate_auto_story(df, teams)
    r["story_type"] = story["story_type"] if story else "none"
    r["story_drama"] = story["drama_score"] if story else np.nan

    for tpl, fn in [
        ("verdict_game_flow", api._game_flow),
        ("verdict_press_autopsy", api._press_autopsy),
        ("verdict_exploit", api._exploit_finder),
        ("verdict_danger_map", api._danger_map),
        ("verdict_progress_trap", api._progress_trap),
    ]:
        out = fn(df.copy(), Req(mid, tpl))
        r[tpl] = bucket(out["metrics"].get("verdict_label", ""), teams)
        plt.close("all")
    return r


def describe(series, name, unit=""):
    s = pd.to_numeric(series, errors="coerce").replace([np.inf, -np.inf], np.nan).dropna()
    q = np.percentile(s, PCTS)
    print(f"  {name:<22}{unit:<3} n={len(s):<4} " + "  ".join(f"p{p}={v:.1f}" for p, v in zip(PCTS, q)))


def labels(series, title):
    c = series.value_counts(dropna=True)
    tot = c.sum()
    print(f"  {title}: " + " | ".join(f"{k} {100 * v / tot:.0f}%" for k, v in c.items()))


def main():
    sys.stdout.reconfigure(encoding="utf-8")   # labels contain non-cp1252 symbols on Windows
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default=str(Path(tempfile.gettempdir()) / "sideline_audit_cache"))
    ap.add_argument("--csv", help="write the per-team and per-match rows here (prefix)")
    ap.add_argument("--limit", type=int, help="only the first N matches (smoke test)")
    a = ap.parse_args()
    os.makedirs(a.cache, exist_ok=True)

    idx = match_index()[: a.limit]
    trows, mrows = [], []
    for i, (comp, stage, mid) in enumerate(idx, 1):
        df = load_events(mid, a.cache)
        trows += team_rows(df, comp, stage, mid)
        mrows.append(match_row(df, comp, stage, mid))
        if i % 20 == 0:
            print(f"  ... {i}/{len(idx)} matches", file=sys.stderr)
    T, M = pd.DataFrame(trows), pd.DataFrame(mrows)
    if a.csv:
        T.to_csv(a.csv + "_teams.csv", index=False)
        M.to_csv(a.csv + "_matches.csv", index=False)

    print(f"\n{len(M)} matches, {len(T)} team-matches\n")
    print("== PER-TEAM METRICS (underlying value, then label share) ==")
    for title, num, lab, unit in [
        ("PPDA / press class", "ppda", "press_class", ""),
        ("Defensive line height / vertical state", "avg_x_m", "vertical", "m"),
        ("Defensive width / horizontal state (mean |y-40|, pitch units)", "h_offset_u", "horizontal", ""),
        ("Gap between lines / compactness", "gap_m", "compactness", "m"),
        ("Exploit Finder risk label", None, "exploit_label", ""),
        ("Progress Trap block depth / block label", "block_depth_m", "block_label", "m"),
        ("Progress Trap stall rate", "stall_rate", None, "%"),
        ("Progress Trap forced-wide % / verdict branch", "forced_wide_pct", "trap_verdict", "%"),
        ("Danger Map danger % / efficiency class", "danger_pct", "efficiency", "%"),
    ]:
        print(f"\n[{title}]")
        if num:
            describe(T[num], num, unit)
        if lab:
            labels(T[lab], "labels")

    print("\n== PER-MATCH ==")
    print("\n[Auto-Story: raw drama per detector (NaN = detector did not fire)]")
    for k in [c for c in M.columns if c.startswith("drama_")]:
        s = M[k]
        print(f"  {k:<28} fires {100 * s.notna().mean():.0f}% of matches   median drama {s.median():.1f}")
    labels(M["story_type"], "story selected")
    print(f"  outcome floor > 0 in {100 * (M['outcome_floor'] > 0).mean():.0f}% of matches")
    for v in [c for c in M.columns if c.startswith("verdict_")]:
        print(f"\n[{v}] (team names -> TEAM, numbers -> #)")
        for k, n in Counter(M[v]).most_common(8):
            print(f"  {100 * n / len(M):>4.0f}%  {k}")

    print("\n== BY COMPETITION (press class, vertical, compactness) ==")
    for col in ["press_class", "vertical", "compactness", "block_label"]:
        print(f"[{col}]")
        print((100 * pd.crosstab(T["comp"], T[col], normalize="index")).round(0).astype(int).to_string())


if __name__ == "__main__":
    main()
