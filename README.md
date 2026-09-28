# iyuno-agent-portfolio

A reproducible AI-agent portfolio project built from the **Iyuno AI Agent Engineer** job-posting requirements used in the course assignment.

## 1. Why this project exists
The assignment asks us to translate job-posting language into working GitHub evidence. This repository implements the evidence directly:

| Job-posting requirement | GitHub evidence |
|---|---|
| LLM/Agent system design | `src/agent.py` router + answer pipeline |
| RAG search/response | `src/retriever.py`, `src/vector_store.py` |
| Tool calling/API | `src/tools.py`, FastAPI endpoints |
| API/database integration | `src/api.py`, JSONL feedback log |
| Multi-step workflow | route → retrieve/tool → answer → citation → feedback |
| Evaluation/feedback loop | `evaluation/run_eval.py`, `evaluation/metrics.json` |
| latency/cost/reliability | evaluation metrics + error handling + tests |

## 2. Features
- 20-source public security/technology document registry
- Chunking + vector retrieval
- Dense embedding backend with `sentence-transformers` + FAISS
- Lightweight TF-IDF fallback for CI/offline testing
- Citation-aware answers
- Tool router: calculator, source lookup, policy lookup
- Streamlit demo and FastAPI API
- Feedback logging for future retraining/evaluation data
- 30-question evaluation set
- Pytest + GitHub Actions CI

## 3. Architecture
```text
User question
    ↓
Agent / Router
 ┌───────────────┬──────────────────┐
 ↓               ↓                  ↓
RAG Retriever    Calculator Tool    Policy/Source Tool
 ↓               ↓                  ↓
Vector Search    Tool result        Tool result
 └───────────────┴──────────────────┘
             ↓
Answer + citations
             ↓
Feedback log (JSONL)
             ↓
Evaluation: Recall@3 · faithfulness proxy · latency · citation coverage
```

## 4. Quick start
```bash
python -m venv .venv
# Windows
.venv\\Scripts\\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
python scripts/build_demo_corpus.py
streamlit run src/app.py
```

API:
```bash
uvicorn src.api:app --reload
```
Then open `http://127.0.0.1:8000/docs`.

## 5. Public-source ingestion
`data/sources.csv` contains 20 public technical/security documents from OWASP, NIST, FastAPI, Streamlit, Python and GitHub documentation.

To fetch live pages:
```bash
python scripts/fetch_sources.py
```
The repository also includes a small **demo summary corpus** so the project can be tested without network access. Demo documents are original summaries, not copies of source pages.

## 6. Evaluation
Run:
```bash
python evaluation/run_eval.py
```
Outputs:
- `evaluation/metrics.json`
- `evaluation/results.csv`

Metrics:
- **Recall@3**: whether the expected source is among the top-3 retrieved documents
- **Faithfulness proxy**: lexical support of the extractive answer in retrieved context
- **Citation coverage**: whether an answer includes source metadata
- **Latency**: end-to-end retrieval/answer time

The faithfulness metric is intentionally labeled a proxy. It is not equivalent to LLM-as-a-judge or human factuality evaluation.

## 7. Tests and CI
```bash
pytest -q
```
GitHub Actions: `.github/workflows/ci.yml`.

## 8. Example questions
- `What is prompt injection?`
- `What does the NIST AI RMF help organizations do?`
- `How does Streamlit Session State work?`
- `calculate 125 * 0.08`
- `show source OWASP_LLM_TOP10`

## 9. Feedback loop
Every 👍/👎 submission is appended to `data/feedback.jsonl` with question, answer, cited sources, rating and optional comment. This creates structured data for later prompt/retriever improvements.

## 10. Honest limitations
- The default demo answerer is extractive and intentionally simple; it proves the RAG/tool/evaluation pipeline without requiring a paid LLM API.
- Live web ingestion may fail when a site blocks automated requests or changes HTML structure.
- The lexical faithfulness score is a proxy, not a semantic entailment metric.
- Dense embeddings require downloading a sentence-transformer model once.
- This project is a portfolio demonstration, not a production security advisory system.

## 11. Data provenance
See `data/sources.csv`. Each row records source id, title, organization, URL, license/note, and access date. No secret keys, private company data or personal information are included.

## 12. Reproducibility
```bash
python scripts/build_demo_corpus.py
python evaluation/run_eval.py
pytest -q
```

## 13. Reflection
I translated an actual job posting into executable evidence rather than listing skills as claims. The strongest evidence is the end-to-end workflow and measurable evaluation. The next step would be to add a production LLM provider, semantic faithfulness evaluation, Docker deployment, and a short demo video/GIF.

## License
MIT for project code. Linked public documents retain their original owners' terms.
