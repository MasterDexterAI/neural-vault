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

Task
- research using ai tools on what small/mini problems we can solve around it,
small tools related to uploading documents, quantization library of your own, etc
take examples from the Build Your Own AI Everything github repo

- himanshu will add the issues in the github repo


# Neural Suite - Supplementary AI Tools

These tools are designed to be built as separate repositories or CLI utilities that "plug into" the Neural Vault ecosystem.

Tool 1: Neural-Sanitizer (PII CLI Utility)
Purpose: An "AI Airlock" for cleaning datasets before they enter the RAG pipeline.

Details:

Logic: Reversible XML-style tagging (e.g., <PII type="EMAIL" id="1">). 

Feature: "Semantic Masking"—preserving the gender or plurality of a masked name so the LLM keeps grammatical consistency during summarization. 

Tech: Python, onnxruntime (for speed), and cryptography library.

Tool 2: Neural-Vision (Local Vision Reviewer)
Purpose: Handles layout-aware OCR for tables, charts, and handwritten faxes. 

Details:

Logic: Uses a vision-SLM (like Qwen2-VL-2B or Phi-4-multimodal) to convert PDF images into structured Markdown tables. 

Feature: Watches a "Hot Folder"; any scanned PDF dropped in is automatically OCR'd and the text is pushed to the Neural Vault data/documents/ folder.

Tech: llama-cpp-python (with vision support), Watchdog.

Tool 3: Neural-Bridge (Local MCP Connector)
Purpose: Allows Neural Vault to "chat" with local databases and apps without APIs. 

Details:

Logic: Implements the Model Context Protocol (MCP). It acts as a gateway to local SQLite files, CSVs, or Obsidian vaults. 

Feature: The LLM can dynamically ask "What are my current tasks in Obsidian?" and the bridge retrieves it securely.

Tech: Python MCP SDK, SQLite.

Tool 4: Neural-Airlock (Secure Update Agent)
Purpose: Securely manages model weight updates in 100% air-gapped environments.

Details:

Logic: A two-part tool. Part A (Online) downloads GGUF weights and verifies SHA-256 hashes. Part B (Offline) scans the USB/media for malware before "sideloading" the model into Neural Vault.

Tech: hashlib, clamav (local scanner integration).