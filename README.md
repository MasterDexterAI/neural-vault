# neural-vault
Offline-First RAG System with Quantized SLMs

business cases
- homoepathy doctor
- doctor
- lawyers
- finance

current solutions are expensive

our product
- desktop app
- 0 API cost
- 100% private
- runs on CPU (macbook)

value
- $5k to $15k


Quantization

- reduce the precision of every weight in the neural network
- 32 bit or 16 bit to 4 bit integers
- GGUF - binary file which will have model architecture and quantized weights


Run LLMs locally with llama.cpp

- c/c++ inference engine which will run quantied models on cpus/gpus
- model loading strategies (lazy or full)
    - lazy loading = only load weights when first called
    - keep embedding model separate (tiny) so total RAM stays under 6 GB


RAG pipeline 

- document chunking
    - chunking makes retrieval precise and prevents context overflow

- text embedding models
    - keyword search fails
    - all-minilm-l6-v2 (huggingface)

- vector db for local storage
    - chromaDB

- similarity search
    - cosine similarity

Buidling RAG System
Desktop application

extra
- memory management
- edge inference
