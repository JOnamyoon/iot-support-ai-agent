from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable
from .models import RetrievalHit

ROOT = Path(__file__).resolve().parents[1]


def save_feedback(question: str, answer: str, citations: Iterable[RetrievalHit], rating: str, comment: str = "") -> None:
    record = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "question": question,
        "answer": answer,
        "source_ids": [c.source_id for c in citations],
        "rating": rating,
        "comment": comment,
    }
    path = ROOT / "data" / "feedback.jsonl"
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
