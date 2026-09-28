import streamlit as st
from agent import KnowledgeTriageAgent
from feedback import save_feedback

st.set_page_config(page_title="Knowledge Triage Agent", page_icon="🧭", layout="wide")
st.title("🧭 Knowledge Triage Agent")
st.caption("RAG + citations + tool routing + feedback loop")

@st.cache_resource
def get_agent():
    return KnowledgeTriageAgent(backend="tfidf")

agent = get_agent()
question = st.text_input("Ask a security/technology question", placeholder="What is prompt injection?")

if st.button("Ask", type="primary") and question:
    try:
        response = agent.answer(question)
        st.session_state["last"] = (question, response)
    except Exception as exc:
        st.error(str(exc))

if "last" in st.session_state:
    q, response = st.session_state["last"]
    st.subheader("Answer")
    st.write(response.answer)
    c1, c2 = st.columns(2)
    c1.metric("Route", response.route)
    c2.metric("Latency", f"{response.latency_ms:.1f} ms")
    if response.citations:
        st.subheader("Retrieved evidence")
        for hit in response.citations:
            with st.expander(f"{hit.source_id} · score {hit.score:.3f}"):
                st.write(hit.text)
                st.link_button("Open source", hit.url)
    st.subheader("Feedback")
    comment = st.text_input("Optional comment")
    b1, b2 = st.columns(2)
    if b1.button("👍 Helpful"):
        save_feedback(q, response.answer, response.citations, "positive", comment)
        st.success("Saved to data/feedback.jsonl")
    if b2.button("👎 Needs improvement"):
        save_feedback(q, response.answer, response.citations, "negative", comment)
        st.success("Saved to data/feedback.jsonl")
