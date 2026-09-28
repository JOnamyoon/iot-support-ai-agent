from __future__ import annotations
import csv
import json
import re
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.agent import KnowledgeTriageAgent  # noqa: E402


def tokens(text: str) -> set[str]:
    return {t.lower() for t in re.findall(r"[A-Za-z0-9_]+", text) if len(t) > 2}

items = json.loads((ROOT / "evaluation" / "eval_questions.json").read_text(encoding="utf-8"))
agent = KnowledgeTriageAgent(backend="tfidf")
rows = []
for item in items:
    response = agent.answer(item["question"], k=3)
    ids = [h.source_id for h in response.citations]
    recall = 1 if item["expected"] in ids else 0
    context = " ".join(h.text for h in response.citations)
    answer_main = response.answer.split("Source:")[0]
    at = tokens(answer_main)
    ct = tokens(context)
    faithfulness = 1.0 if not at else len(at & ct) / len(at)
    citation_coverage = 1 if response.citations and "Source:" in response.answer else 0
    rows.append({
        "question": item["question"],
        "expected": item["expected"],
        "top3": "|".join(ids),
        "recall_at_3": recall,
        "faithfulness_proxy": round(faithfulness, 4),
        "citation_coverage": citation_coverage,
        "latency_ms": round(response.latency_ms, 3),
    })

metrics = {
    "questions": len(rows),
    "recall_at_3": round(sum(r["recall_at_3"] for r in rows) / len(rows), 4),
    "faithfulness_proxy": round(sum(r["faithfulness_proxy"] for r in rows) / len(rows), 4),
    "citation_coverage": round(sum(r["citation_coverage"] for r in rows) / len(rows), 4),
    "latency_ms_mean": round(statistics.mean(r["latency_ms"] for r in rows), 3),
    "latency_ms_p95": round(sorted(r["latency_ms"] for r in rows)[int(len(rows)*0.95)-1], 3),
    "backend": "TF-IDF offline baseline",
    "note": "Faithfulness is a lexical support proxy because the baseline answerer is extractive; it is not semantic factuality evaluation."
}
(ROOT / "evaluation" / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
with (ROOT / "evaluation" / "results.csv").open("w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader(); writer.writerows(rows)
print(json.dumps(metrics, indent=2))
