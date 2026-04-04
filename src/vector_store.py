import chromadb
from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer
import os

class VectorStore:
    def __init__(self, persist_directory: str = "chroma_db", collection_name: str = "neural_vault"):
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        
        # Use SentenceTransformer for embeddings (fast on CPU/MPS)
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # ChromaDB in embedded mode (no server)
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Create collection with cosine similarity
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )

    def add_documents(self, chunks: list[str], metadata: list[dict] = None):
        """Add text chunks to vector store"""
        if not chunks:
            return

        embeddings = self.embedding_model.encode(chunks, normalize_embeddings=True).tolist()

        # Use content hash as ID to avoid collisions across multiple ingests
        import hashlib
        ids = [hashlib.md5(chunk.encode()).hexdigest() for chunk in chunks]

        self.collection.add(
            embeddings=embeddings,
            documents=chunks,
            ids=ids,
            metadatas=metadata or [{} for _ in chunks]
        )

    def query(self, query_text: str, n_results: int = 6) -> tuple[list[str], list[dict]]:
        """Semantic search. Returns (documents, metadatas)."""
        query_embedding = self.embedding_model.encode([query_text], normalize_embeddings=True).tolist()

        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=n_results,
            include=["documents", "metadatas", "distances"]
        )

        docs = results["documents"][0] if results["documents"] else []
        metas = results["metadatas"][0] if results["metadatas"] else []
        return docs, metas