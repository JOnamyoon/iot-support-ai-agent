# Final reflection

## What I implemented
I converted job-posting requirements into an executable portfolio: a RAG retriever, citation-aware response flow, three tools, a FastAPI/Streamlit interface, feedback logging, a 30-question evaluation set, automated tests and CI.

## What I learned
The most important step was translating vague phrases such as “RAG”, “tool calling” and “evaluation” into files, commands and measurable outputs. A GitHub repository is stronger evidence when a reviewer can reproduce the result rather than only read a claim.

## What remains
The current baseline uses extractive answers and an offline TF-IDF evaluation path. The repository already supports a dense sentence-transformer/FAISS backend, but a production version should add an LLM provider, semantic faithfulness evaluation, deployment, authentication, structured observability and a short demo video.
