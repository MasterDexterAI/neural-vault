# streamlet UI
import streamlit as st
import os
from src.rag_pipeline import RAGPipeline

# Page config
st.set_page_config(page_title="Neural Vault", page_icon="🔒", layout="wide")
st.title("Neural Vault")
st.caption("100% Offline • Private • Runs on your PC")

# Initialize pipeline
if "pipeline" not in st.session_state:
    st.session_state.pipeline = RAGPipeline()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar - Document Upload
with st.sidebar:
    st.header("📄 Upload Documents")
    uploaded_files = st.file_uploader(
        "Upload sensitive PDFs (they stay on your device)",
        type="pdf",
        accept_multiple_files=True
    )

    if uploaded_files:
        for uploaded_file in uploaded_files:
            save_path = f"data/documents/{uploaded_file.name}"
            os.makedirs("data/documents", exist_ok=True)
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            with st.spinner(f"Processing {uploaded_file.name}..."):
                chunk_count = st.session_state.pipeline.ingest_pdf(save_path)
            st.success(f"✅ {uploaded_file.name} added ({chunk_count} chunks)")

def _render_sources(sources: list[dict]):
    """Display a collapsible source card for each (document, page) citation."""
    if not sources:
        return
    with st.expander("📎 Sources", expanded=False):
        cols = st.columns(min(len(sources), 3))
        for i, src in enumerate(sources):
            with cols[i % len(cols)]:
                st.markdown(
                    f"""<div style="
                        border: 1px solid #444;
                        border-radius: 6px;
                        padding: 8px 12px;
                        margin-bottom: 6px;
                        font-size: 0.85em;
                    ">
                    📄 <b>{src['source']}</b><br/>
                    🔖 Page {src['page_number']}
                    </div>""",
                    unsafe_allow_html=True,
                )

# Main Chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("sources"):
            _render_sources(message["sources"])

if prompt := st.chat_input("Ask anything about your documents..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        stream, sources = st.session_state.pipeline.query(prompt)

        for chunk in stream:
            if isinstance(chunk, dict) and "content" in chunk:
                token = chunk["content"]
            else:
                token = chunk
            full_response += token
            message_placeholder.markdown(full_response + "▌")

        message_placeholder.markdown(full_response)
        _render_sources(sources)

    st.session_state.messages.append({
        "role": "assistant",
        "content": full_response,
        "sources": sources,
    })
