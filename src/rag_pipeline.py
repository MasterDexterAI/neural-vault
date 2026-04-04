import os
from src.document_processor import load_pdf, chunk_text
from src.vector_store import VectorStore
from src.llm_engine import LLMEngine


class RAGPipeline:
    def __init__(self):
        self.vector_store = VectorStore()
        self.llm = LLMEngine()

    def ingest_pdf(self, pdf_path: str) -> int:
        """Process and store one PDF, preserving page-level metadata."""
        pages = load_pdf(pdf_path)
        chunks = chunk_text(pages)

        filename = os.path.basename(pdf_path)
        texts = [c["text"] for c in chunks]
        metadata = [{"source": filename, "page_number": c["page_number"]} for c in chunks]

        self.vector_store.add_documents(texts, metadata)
        return len(chunks)

    def query(self, question: str) -> tuple:
        """
        Full RAG pipeline.
        Returns (stream_generator, sources) where sources is a deduplicated
        list of {"source": str, "page_number": int} dicts.
        """
        docs, metas = self.vector_store.query(question, n_results=6)

        if not docs:
            def _empty():
                yield "No relevant information found in documents."
            return _empty(), []

        context = "\n\n".join(docs)

        prompt = f"""You are a helpful AI assistant. Answer the question using ONLY the context below.
If you don't know the answer, say "I don't have enough information."

Context:
{context}

Question: {question}
Answer:"""

        # Deduplicate sources while preserving order
        seen = set()
        sources = []
        for meta in metas:
            key = (meta.get("source", ""), meta.get("page_number", ""))
            if key not in seen:
                seen.add(key)
                sources.append({"source": meta.get("source", "Unknown"), "page_number": meta.get("page_number", "?")})

        return self.llm.generate_stream(prompt), sources
