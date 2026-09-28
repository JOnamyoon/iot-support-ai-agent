from __future__ import annotations
import csv
from pathlib import Path
import time
import requests
import trafilatura

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "fetched"
OUT.mkdir(parents=True, exist_ok=True)
HEADERS = {"User-Agent": "student-portfolio-rag/1.0 (educational use)"}

with (ROOT / "data" / "sources.csv").open(encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

for i, row in enumerate(rows, 1):
    sid, url = row["source_id"], row["url"]
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        r.raise_for_status()
        text = trafilatura.extract(r.text, include_links=False, include_images=False) or ""
        if len(text) < 200:
            raise RuntimeError("extracted text was too short")
        (OUT / f"{sid}.txt").write_text(text, encoding="utf-8")
        print(f"[{i:02d}/{len(rows)}] OK {sid} ({len(text)} chars)")
    except Exception as exc:
        print(f"[{i:02d}/{len(rows)}] FAIL {sid}: {exc}")
    time.sleep(0.4)
