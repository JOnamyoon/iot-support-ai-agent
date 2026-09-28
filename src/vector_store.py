from __future__ import annotations
from typing import List
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .models import Document, RetrievalHit


class TfidfVectorStore:
    """Deterministic offline vector-search backend used by CI and evaluation."""

    def __init__(self, documents: List[Document]):
        if not documents:
            raise ValueError("documents must not be empty")
        self.documents = documents
        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        self.matrix = self.vectorizer.fit_transform([d.text for d in documents])

    def search(self, query: str, k: int = 3) -> List[RetrievalHit]:
        q = self.vectorizer.transform([query])
        scores = cosine_similarity(q, self.matrix).ravel()
        order = np.argsort(scores)[::-1][:k]
        return [
            RetrievalHit(
                source_id=self.documents[i].source_id,
                title=self.documents[i].title,
                url=self.documents[i].url,
                text=self.documents[i].text,
                score=float(scores[i]),
            )
            for i in order
        ]


class DenseFaissVectorStore:
    """Production-like dense embedding backend. Model downloads on first use."""

    def __init__(self, documents: List[Document], model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        if not documents:
            raise ValueError("documents must not be empty")
        try:
            import faiss  # type: ignore
            from sentence_transformers import SentenceTransformer  # type: ignore
        except ImportError as exc:
            raise RuntimeError("Install sentence-transformers and faiss-cpu for dense retrieval") from exc

        self.documents = documents
        self.model = SentenceTransformer(model_name)
        embeddings = self.model.encode([d.text for d in documents], normalize_embeddings=True)
        self.embeddings = np.asarray(embeddings, dtype="float32")
        self.index = faiss.IndexFlatIP(self.embeddings.shape[1])
        self.index.add(self.embeddings)

    def search(self, query: str, k: int = 3) -> List[RetrievalHit]:
        q = np.asarray(self.model.encode([query], normalize_embeddings=True), dtype="float32")
        scores, indices = self.index.search(q, min(k, len(self.documents)))
        hits: List[RetrievalHit] = []
        for score, i in zip(scores[0], indices[0]):
            d = self.documents[int(i)]
            hits.append(RetrievalHit(d.source_id, d.title, d.url, d.text, float(score)))
        return hits
