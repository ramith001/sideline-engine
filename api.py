"""
api.py  —  Sideline.ai FastAPI Backend  v0.1.0
Endpoints:
    GET  /health
    POST /analyze   (routes by `template` field)
"""

import os
from functools import lru_cache

import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from statsbombpy import sb

from sideline.models import AnalysisRequest
from sideline.templates import (
    _danger_map,
    _exploit_finder,
    _game_flow,
    _press_autopsy,
    _progress_trap,
)

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

# ── Health ────────────────────────────────────────────────────────────────────

@app.get("/health")
def health_check():
    # Render sets RENDER_GIT_COMMIT at runtime; "unknown" anywhere else.
    commit_short = os.environ.get("RENDER_GIT_COMMIT", "unknown")[:7]
    return {"status": "ok", "version": API_VERSION, "commit": commit_short}

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
