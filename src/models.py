from __future__ import annotations
from dataclasses import dataclass
from typing import List

@dataclass
class Document:
    source_id: str
    title: str
    url: str
    text: str

@dataclass
class RetrievalHit:
    source_id: str
    title: str
    url: str
    text: str
    score: float

@dataclass
class AgentResponse:
    answer: str
    route: str
    citations: List[RetrievalHit]
    latency_ms: float
