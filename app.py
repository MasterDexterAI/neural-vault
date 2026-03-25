# streamlet UI
import streamlit as st
import os
from src.rag_pipeline import RAGPipeline

# Page config
st.set_page_config(page_title="Neural Vault", page_icon="🔒", layout="wide")
st.title("Neural Vault")
st.caption("100% Offline • Private • Runs on your Mac")

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
            # Save temporarily
            save_path = f"data/documents/{uploaded_file.name}"
            os.makedirs("data/documents", exist_ok=True)
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Ingest
            with st.spinner(f"Processing {uploaded_file.name}..."):
                chunk_count = st.session_state.pipeline.ingest_pdf(save_path)
            st.success(f"✅ {uploaded_file.name} added ({chunk_count} chunks)")

# Main Chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask anything about your documents..."):
    # Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Stream tokens
        for chunk in st.session_state.pipeline.query(prompt):
            if isinstance(chunk, dict) and "content" in chunk:  # llama.cpp streaming format
                token = chunk["content"]
            else:
                token = chunk  # fallback
            full_response += token
            message_placeholder.markdown(full_response + "▌")
        
        message_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})