from src.document_processor import load_pdf, chunk_text
from src.vector_store import VectorStore
from src.llm_engine import LLMEngine

class RAGPipeline:
    def __init__(self):
        self.vector_store = VectorStore()
        self.llm = LLMEngine()

    def ingest_pdf(self, pdf_path: str):
        """Process and store one PDF"""
        text = load_pdf(pdf_path)
        chunks = chunk_text(text)
        
        # Optional: add filename as metadata
        metadata = [{"source": pdf_path} for _ in chunks]
        
        self.vector_store.add_documents(chunks, metadata)
        return len(chunks)

    def query(self, question: str):
        """Full RAG pipeline"""
        # 1. Retrieve relevant chunks
        retrieved_chunks = self.vector_store.query(question, n_results=6)
        
        if not retrieved_chunks:
            return "No relevant information found in documents."
        
        context = "\n\n".join(retrieved_chunks)
        
        # 2. Build prompt
        prompt = f"""You are a helpful AI assistant. Answer the question using ONLY the context below.
        If you don't know the answer, say "I don't have enough information."

        Context:
        {context}

        Question: {question}
        Answer:"""

        # 3. Stream response
        return self.llm.generate_stream(prompt)