import streamlit as st
import requests

API = "http://localhost:8000"

st.set_page_config(page_title="RAG Chatbot", page_icon="🤖")
st.title("RAG Knowledge Base Chatbot")
st.caption("Upload a PDF and ask questions about it")

# ── Upload section ──────────────────────
st.subheader("1. Upload your document")
uploaded = st.file_uploader("Choose a PDF", type=["pdf"])

if uploaded is not None:
    if st.button("Ingest Document", type="primary"):
        with st.spinner("Processing your PDF..."):
            try:
                r = requests.post(
                    f"{API}/upload",
                    files={"file": (uploaded.name, uploaded, "application/pdf")}
                )
                data = r.json()
                st.success(
                    f"Done! {data['pages_loaded']} pages → {data['chunks_created']} chunks stored"
                )
            except Exception as e:
                st.error(f"Upload failed: {e}. Is the backend running?")

st.divider()

# ── Chat section ────────────────────────
st.subheader("2. Ask a question")
question = st.text_input(
    "Your question",
    placeholder="What is this document about?"
)

if st.button("Ask", type="primary") and question:
    with st.spinner("Thinking..."):
        try:
            r = requests.post(
                f"{API}/chat",
                json={"question": question}
            )
            data = r.json()

            st.markdown("### Answer")
            st.write(data["answer"])

            if data.get("sources"):
                with st.expander("Sources used"):
                    for s in data["sources"]:
                        st.write(f"- {s['source']}  |  page {s['page']}")

            if data.get("chunks"):
                with st.expander("Retrieved chunks (debug)"):
                    for i, c in enumerate(data["chunks"]):
                        st.markdown(f"**Chunk {i+1}** — score: `{c['score']}`")
                        st.write(c["content"][:200] + "...")

        except Exception as e:
            st.error(f"Error: {e}. Is the backend running?")