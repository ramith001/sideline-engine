"""
Regenerate components/sample-report.json: the precomputed report the landing
page shows before anyone clicks "Run Analysis".

    python scripts/make_sample_report.py

It calls the real /analyze endpoint (in-process, via FastAPI's TestClient) for
the WC2022 final with The Game Flow template, so it is genuine engine output.
It needs network access for the StatsBomb open data. Re-run it whenever the
engine's output changes, otherwise the sample goes stale.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fastapi.testclient import TestClient

import api

MATCH_ID = 3869685          # WC2022 Final: Argentina vs France
TEMPLATE = "The Game Flow"  # must match SAMPLE_TEMPLATE in components/main-content.tsx
OUT = ROOT / "components" / "sample-report.json"


def main():
    res = TestClient(api.app).post(
        "/analyze", json={"match_id": MATCH_ID, "mode": "analyst", "template": TEMPLATE}
    )
    res.raise_for_status()
    OUT.write_text(json.dumps(res.json(), separators=(",", ":")), encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
