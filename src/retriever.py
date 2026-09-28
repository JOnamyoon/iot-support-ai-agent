from __future__ import annotations
import csv
from pathlib import Path
from typing import List
from .models import Document, RetrievalHit
from .vector_store import TfidfVectorStore, DenseFaissVectorStore

ROOT = Path(__file__).resolve().parents[1]


def load_demo_documents() -> List[Document]:
    docs: List[Document] = []
    for path in sorted((ROOT / "data" / "demo_docs").glob("*.md")):
        text = path.read_text(encoding="utf-8")
        meta = {}
        body_lines = []
        for line in text.splitlines():
            if line.startswith("source_id:"):
                meta["source_id"] = line.split(":", 1)[1].strip()
            elif line.startswith("title:"):
                meta["title"] = line.split(":", 1)[1].strip()
            elif line.startswith("url:"):
                meta["url"] = line.split(":", 1)[1].strip()
            else:
                body_lines.append(line)
        docs.append(Document(meta["source_id"], meta["title"], meta["url"], "\n".join(body_lines).strip()))
    if not docs:
        raise FileNotFoundError("No demo docs found. Run: python scripts/build_demo_corpus.py")
    return docs


class Retriever:
    def __init__(self, backend: str = "tfidf"):
        docs = load_demo_documents()
        self.store = DenseFaissVectorStore(docs) if backend == "dense" else TfidfVectorStore(docs)

    def search(self, query: str, k: int = 3) -> List[RetrievalHit]:
        return self.store.search(query, k)
