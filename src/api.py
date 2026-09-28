from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .agent import KnowledgeTriageAgent
from .feedback import save_feedback

app = FastAPI(title="Knowledge Triage Agent", version="1.0.0")
agent = KnowledgeTriageAgent(backend="tfidf")

class AskRequest(BaseModel):
    question: str

class FeedbackRequest(BaseModel):
    question: str
    answer: str
    rating: str
    comment: str = ""
    source_ids: list[str] = []

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ask")
def ask(req: AskRequest):
    try:
        response = agent.answer(req.question)
    except (ValueError, KeyError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {
        "answer": response.answer,
        "route": response.route,
        "latency_ms": round(response.latency_ms, 2),
        "citations": [{"source_id": c.source_id, "title": c.title, "url": c.url, "score": c.score} for c in response.citations],
    }
