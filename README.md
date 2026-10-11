# Sideline AI

Automated tactical reasoning engine for football. Converts raw coordinate-level match event data into tactical verdicts, pitch visuals, and creator-ready content, instantly instead of through manual video review.

## What it does

Five specialised analysis templates with dynamic two-team verdicts. An Auto-Story engine that scores and narrates the highest-drama tactical moment of a match automatically. Covers 147 matches across FIFA World Cup 2022, UEFA Euro 2024, and Copa America 2024. Built to the Stats Perform (Opta) MA3 feed specification, with full coordinate conversion from StatsBomb's 120x80 pitch space to Opta's 100x100 space, Opta event type ID mapping, and a Qualifier 72 (Under Pressure) implementation, designed for direct live feed integration via penaltyblog's Opta MA3 connector, a single function swap from demo data to a live feed.

## Stack

FastAPI (Python) backend with pandas, numpy, scipy, statsbombpy, and mplsoccer. Next.js/React frontend with Tailwind CSS. Originally deployed on Railway (backend) and Vercel (frontend).

## Files

`api.py` and `app.py` for the backend and analysis endpoints, `match_index.py` for match indexing across the three tournaments, `visuals.py` and `visuals_v2.py` for pitch visual generation, and `app/` plus `components/` for the Next.js frontend.

## Background

Co-founded and built with Panav Java over roughly four months in 2026. Secured Raees Mahmood (Pythagoras in Boots, Sky Sports analyst) as a launch partner.
