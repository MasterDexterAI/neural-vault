# Neural Vault - Architecture Flow Diagram

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                          USER INTERFACE                              │
│                      (Streamlit Web App)                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐     │
│  │  PDF Uploader   │  │   Chat Interface │  │  Status Display │     │
│  └────────┬────────┘  └────────┬────────┘  └─────────────────┘     │
└───────────┼────────────────────┼────────────────────────────────────┘
            │                    │
            │                    │
┌───────────┼────────────────────┼────────────────────────────────────┐
│           │   RAG PIPELINE     │                                    │
│           │  (rag_pipeline.py) │                                    │
│           │                    │                                    │
│  ┌────────▼────────┐   ┌──────▼──────┐   ┌─────────────────┐       │
│  │  Document       │   │  Query      │   │  LLM Engine     │       │
│  │  Ingestion      │   │  Processing │   │  (llm_engine.py)│       │
│  │                 │   │             │   │                 │       │
│  │ • PDF Loading   │   │ • Retrieve  │   │ • GPT-2 Model   │       │
│  │ • Text Chunking │   │ • Vector    │   │ • Context       │       │
│  │ • Embedding     │   │   Search    │   │   Integration   │       │
│  │ • Vector Storage│   │ • Prompt    │   │ • Response      │       │
│  │                 │   │   Building │   │   Generation   │       │
│  └────────┬────────┘   └──────┬──────┘   └─────────────────┘       │
└───────────┼────────────────────┼────────────────────────────────────┘
            │                    │
            │                    │
┌───────────┼────────────────────┼────────────────────────────────────┐
│           │                    │                                    │
│  ┌────────▼────────┐   ┌──────▼──────┐   ┌─────────────────┐       │
│  │  Document       │   │  Vector     │   │  Model          │       │
│  │  Processor      │   │  Store      │   │  Layer          │       │
│  │(document_       │   │(vector_     │   │                 │       │
│  │ processor.py)   │   │ store.py)   │   │ • Transformers  │       │
│  │                 │   │             │   │ • PyTorch       │       │
│  │ • pypdf         │   │ • ChromaDB  │   │ • GPT-2         │       │
│  │ • Text          │   │ • Sentence  │   │ • Fallback      │       │
│  │   Chunking      │   │   Transformers│  │   Logic        │       │
│  │ • Overlap (200) │   │ • all-MiniLM│   │                 │       │
│  │   chars         │   │   -L6-v2    │   │                 │       │
│  └────────────────┘   └─────────────┘   └─────────────────┘       │
│                                                                        │
│  ┌─────────────────┐   ┌─────────────────┐                          │
│  │  Storage Layer  │   │  ML/AI Layer    │                          │
│  │                 │   │                 │                          │
│  │ • PDF Files     │   │ • Embeddings    │                          │
│  │   (data/)       │   │ • Vector DB     │                          │
│  │ • ChromaDB      │   │ • LLM Inference │                          │
│  │   (chroma_db/)  │   │ • Context       │                          │
│  │ • Models        │   │   Processing    │                          │
│  │   (models/)     │   │                 │                          │
│  └─────────────────┘   └─────────────────┘                          │
└────────────────────────────────────────────────────────────────────┘
```

## Data Flow Sequence

### 1. Document Ingestion Flow
```
User Upload PDF → Streamlit Interface → RAGPipeline.ingest_pdf()
    ↓
DocumentProcessor.load_pdf() → Extract text from PDF
    ↓
DocumentProcessor.chunk_text() → Create overlapping chunks (1000 chars, 200 overlap)
    ↓
VectorStore.add_documents() → Generate embeddings using all-MiniLM-L6-v2
    ↓
ChromaDB → Store vectors with cosine similarity metadata
    ↓
Success Message → UI shows chunk count
```

### 2. Query Processing Flow
```
User Question → Streamlit Chat Interface → RAGPipeline.query()
    ↓
VectorStore.query() → Generate question embedding
    ↓
ChromaDB Similarity Search → Retrieve top 6 relevant chunks
    ↓
Prompt Construction → Build context + question prompt
    ↓
LLMEngine.generate_stream() → Generate response using GPT-2
    ↓
Token Streaming → Display response character by character
    ↓
Complete Response → Chat history update
```

## Component Architecture

### **Layer 1: User Interface**
- **Streamlit App** (`app.py`)
  - File upload widget for PDFs
  - Chat interface for queries
  - Session state management
  - Response streaming

### **Layer 2: Application Logic**
- **RAG Pipeline** (`src/rag_pipeline.py`)
  - Orchestrates document processing
  - Manages query flow
  - Integrates all components

### **Layer 3: Core Services**
- **Document Processor** (`src/document_processor.py`)
  - PDF text extraction using pypdf
  - Intelligent chunking with sentence boundaries
  - Overlap preservation for context

- **Vector Store** (`src/vector_store.py`)
  - ChromaDB persistent storage
  - Sentence Transformers embeddings
  - Cosine similarity search
  - Metadata management

- **LLM Engine** (`src/llm_engine.py`)
  - Transformers integration
  - GPT-2 model loading
  - Context-aware generation
  - Streaming responses

### **Layer 4: Storage & Models**
- **File System**
  - `data/documents/` - Uploaded PDFs
  - `chroma_db/` - Vector database
  - `models/` - AI model files

- **ML/AI Layer**
  - all-MiniLM-L6-v2 (embeddings)
  - GPT-2 (text generation)
  - ChromaDB (vector operations)

## Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **UI Framework** | Streamlit | Web interface |
| **PDF Processing** | pypdf | Document text extraction |
| **Embeddings** | Sentence Transformers | Text vectorization |
| **Vector Database** | ChromaDB | Local vector storage |
| **LLM** | Transformers + GPT-2 | Text generation |
| **Math/ML** | PyTorch, NumPy | Numerical operations |
| **Storage** | Local filesystem | Document & model storage |

## Key Design Decisions

### **Privacy & Security**
- ✅ 100% local processing - no cloud APIs
- ✅ Documents never leave the machine
- ✅ No external dependencies during operation
- ✅ Persistent local storage only

### **Performance Optimizations**
- ✅ Lazy model loading
- ✅ Document chunking (1000 chars) to prevent context overflow
- ✅ Overlap (200 chars) for context continuity
- ✅ Small models optimized for CPU inference
- ✅ Cosine similarity for efficient vector search

### **Scalability Considerations**
- ✅ Modular architecture for easy component replacement
- ✅ Persistent vector store for incremental document additions
- ✅ Streaming responses for better UX
- ✅ Graceful fallback when models unavailable

## Error Handling & Fallbacks

```
┌─────────────────────────────────────────────────────────┐
│                  ERROR HANDLING                         │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  llama-cpp-python unavailable → Use GPT-2                │
│  GPT-2 unavailable → Smart context responses             │
│  PDF processing fails → Error message + retry option     │
│  Vector store issues → Recreate collection               │
│  Model loading fails → Demo mode with instructions       │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## Memory & Resource Management

| Component | Memory Usage | Optimization |
|-----------|-------------|--------------|
| Embeddings Model | ~100MB | CPU-optimized |
| GPT-2 Model | ~500MB | Small variant |
| ChromaDB | Variable | Lazy loading |
| PDF Processing | ~50MB per doc | Streaming chunks |
| **Total** | <1GB baseline | Designed for MacBook Air |

## Future Enhancement Points

1. **Model Upgrades**
   - Larger quantized models (Llama-3.2-3B)
   - Fine-tuned domain-specific models
   - Multi-model support for different tasks

2. **Performance**
   - GPU acceleration (Metal/MPS)
   - Parallel document processing
   - Caching strategies

3. **Features**
   - Multi-document support
   - Document source tracking
   - Export functionality
   - Query history
   - Document management UI