from __future__ import annotations
import re
import time
from typing import Optional
from .models import AgentResponse
from .retriever import Retriever
from .tools import calculator, source_lookup, policy_lookup

CALC_RE = re.compile(r"(?:calculate|calc|계산)\s*[: ]\s*(.+)", re.I)
SOURCE_RE = re.compile(r"^(?:show source|출처)\s+([A-Z0-9_\-]+)$", re.I)


class KnowledgeTriageAgent:
    def __init__(self, backend: str = "tfidf"):
        self.retriever = Retriever(backend=backend)

    def answer(self, question: str, k: int = 3) -> AgentResponse:
        started = time.perf_counter()
        q = question.strip()
        if not q:
            raise ValueError("question must not be empty")

        if m := CALC_RE.search(q):
            result = calculator(m.group(1))
            return AgentResponse(f"Calculator result: {result:g}", "tool:calculator", [], (time.perf_counter()-started)*1000)

        if m := SOURCE_RE.search(q):
            row = source_lookup(m.group(1))
            answer = f"{row['title']} — {row['organization']}\n{row['url']}"
            return AgentResponse(answer, "tool:source_lookup", [], (time.perf_counter()-started)*1000)

        if q.lower().startswith("policy ") or q.startswith("정책 "):
            topic = q.split(" ", 1)[1]
            return AgentResponse(policy_lookup(topic), "tool:policy_lookup", [], (time.perf_counter()-started)*1000)

        hits = self.retriever.search(q, k=k)
        top = hits[0]
        # Extractive answer = auditable baseline that minimizes unsupported generation.
        sentences = re.split(r"(?<=[.!?])\s+", top.text)
        answer = " ".join(sentences[:2]).strip()
        answer += f"\n\nSource: {top.title} ({top.url})"
        return AgentResponse(answer, "rag", hits, (time.perf_counter()-started)*1000)
