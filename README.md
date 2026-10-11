# Sideline AI

![tests](https://github.com/ramith001/sideline-engine/actions/workflows/tests.yml/badge.svg)

A rule-based football analysis tool. Converts raw coordinate-level match event data into tactical reports, pitch visuals, and written summaries.

## What it does

Five specialised analysis templates with dynamic two-team verdicts. An Auto-Story engine that scores and narrates the highest-drama tactical moment of a match automatically. Covers 146 matches across FIFA World Cup 2022, UEFA Euro 2024, and Copa America 2024.

## Live Demo

https://sideline-engine.vercel.app (backend is on Render's free tier, so the first request after a period of inactivity can take 20-30 seconds to respond while it spins back up)

## Stack

FastAPI (Python) backend with pandas, numpy, scipy, statsbombpy, and mplsoccer. Next.js/React frontend with Tailwind CSS. Backend deployed on Render, frontend on Vercel.

## Files

**Backend.** `api.py` is the thin FastAPI app: the `/analyze` and `/health` endpoints and CORS setup. The analysis engine is the `sideline/` package:

- `sideline/metrics.py`: shared constants, thresholds and the per-team metrics (PPDA, defensive lines, compactness, progressive passes, block depth).
- `sideline/verdicts.py`: the two-team verdict text for the Exploit Finder, Danger Map and Progress Trap.
- `sideline/story.py`: the Auto-Story engine, which picks and narrates the highest-drama moment of a match using the half-time score as context.
- `sideline/visuals.py`: pitch rendering.
- `sideline/templates.py`: the five analysis templates, which tie the pieces above together.
- `sideline/models.py`: the request model.

**Frontend.** `app/` and `components/` are the Next.js frontend.

**Tooling.** `tests/` is the pytest suite (run by CI on every push). `scripts/` holds the label audit (`audit_labels.py`), the PPDA calibration (`calibrate_ppda.py`) and the generator for the landing-page sample report (`make_sample_report.py`).

**Prototype.** `prototype/` holds `app.py`, `sideline_ai_v01.py`, `visuals.py`, `visuals_v2.py` and `match_index.py`, from an earlier Streamlit-based prototype of the same engine. They're kept as project history but aren't used by the current live stack, which was rewritten as a FastAPI backend with a Next.js frontend.

## Validation

PPDA labels (Aggressive / Moderate / Passive) are calibrated on this dataset, not taken from an external standard. Over all 146 matches (292 team-matches):

- **Split:** 19% Aggressive, 59% Moderate, 22% Passive (Aggressive below 9, Passive at 20 and above). The cut-offs sit at the percentiles the original thresholds occupied before the metric was corrected.
- **Agreement with a standard definition:** 0.95 Spearman rank correlation between the app's PPDA and a separately computed standard-definition PPDA (opponent passes in their own 60% of the pitch per tackle, interception, foul or challenge in the opposition's 60%).
- **Spread across tournaments:** the Aggressive share varies a lot, from 39% at Copa America 2024 to 16% at the 2022 World Cup and 11% at Euro 2024.

Because the thresholds are percentile-based on these three tournaments, the labels are relative to this dataset. A different competition would shift the split. Reproduce with `python scripts/calibrate_ppda.py`.

## Background

Co-founded and built with Panav Java over roughly four months in 2026.
