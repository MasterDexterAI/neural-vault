# Neural Vault

Offline-First RAG System with Quantized Small Language Models

## Overview

Neural Vault is a desktop application that runs advanced AI language models entirely on your local computer. It provides professional document analysis capabilities without requiring internet connectivity, cloud services, or API costs. The system is designed for professionals who handle sensitive documents and need privacy-focused AI assistance.

## Target Users

This application is designed for professionals in fields where data privacy is critical:

- Medical professionals (homeopathic doctors, physicians)
- Legal professionals (lawyers, paralegals)
- Finance professionals (accountants, analysts)
- Anyone handling confidential documents

## Problem and Solution

### Current Industry Problems

- Existing AI solutions require expensive monthly subscriptions
- Most tools process documents in the cloud creating privacy risks
- Limited options for offline document analysis
- High computational requirements typically need specialized hardware

### Our Solution

- Desktop application that runs locally on your computer
- Zero API costs after initial setup
- Complete data privacy with 100% offline processing
- Optimized to run on standard MacBooks without requiring dedicated graphics hardware
- Target pricing between $5,000 to $15,000 for enterprise deployment

## Technical Architecture

### Model Quantization

The system uses advanced quantization techniques to make large language models run efficiently on standard computers:

- Reduces precision of neural network weights from 32-bit or 16-bit to 4-bit integers
- Uses GGUF format which combines model architecture with compressed weights
- Maintains model accuracy while dramatically reducing memory requirements

### Local Model Execution

- C/C++ inference engine optimized for CPU processing
- Smart model loading strategies:
  - Lazy loading: loads only the weights needed for current operation
  - Separate embedding models keep total RAM usage under 6GB
- Metal acceleration support for Apple Silicon chips

### RAG Pipeline Components

#### Document Processing
- Text chunking with intelligent boundary detection
- Overlap preservation (200 characters) maintains context between sections
- Prevents context overflow in language models

#### Text Understanding
- Advanced embedding models replace traditional keyword search
- Uses all-MiniLM-L6-v2 model from HuggingFace
- Converts text to numerical vectors for semantic understanding

#### Local Vector Database
- ChromaDB for local vector storage and retrieval
- Persistent storage across application restarts
- Cosine similarity search for finding relevant content

#### Intelligent Response Generation
- Context-aware question answering
- Document-grounded responses with source attribution
- Streaming output for better user experience

## Getting Started

### Installation

1. Clone the repository
2. Create a virtual environment
3. Install dependencies
4. Download the required models
5. Run the application

For detailed installation instructions, see the ARCHITECTURE.md file.

### Usage

1. Upload PDF documents through the web interface
2. Ask questions about your documents in natural language
3. Receive intelligent responses based only on your uploaded content

## Project Structure

- app.py - Main Streamlit application interface
- src/rag_pipeline.py - Core RAG orchestration logic
- src/document_processor.py - PDF text extraction and chunking
- src/vector_store.py - Vector database management
- src/llm_engine.py - Language model interface
- data/documents/ - Uploaded PDF storage
- chroma_db/ - Vector database persistence
- models/ - AI model files

## Contributing

We welcome contributions to the Neural Vault project. Please see CONTRIBUTING.md for detailed guidelines on:

- Development workflow
- Issue selection process
- Code submission standards
- Pull request process
- Using AI assistants like Claude for development

## Architecture Documentation

For detailed technical architecture, data flow diagrams, and component descriptions, see ARCHITECTURE.md.

## Supplementary Tools

The Neural Suite ecosystem includes several complementary tools designed to extend Neural Vault capabilities:

### Neural-Sanitizer
A command-line utility for cleaning sensitive information before documents enter the RAG pipeline. Features reversible XML-style tagging and semantic masking to maintain grammatical consistency.

### Neural-Vision
Handles optical character recognition for tables, charts, and handwritten documents. Automatically processes scanned PDFs dropped into a watched folder and converts them to structured text.

### Neural-Bridge
Connects Neural Vault to local databases and applications using the Model Context Protocol. Enables querying local SQLite databases, CSV files, and Obsidian vaults.

### Neural-Airlock
Securely manages model updates for air-gapped environments. Provides safe download and verification of model weights with malware scanning capabilities.

## Development Roadmap

### Current Focus
- Memory management optimization
- Edge inference improvements
- Enhanced document processing capabilities

### Future Enhancements
- Support for additional document formats
- Advanced quantization options
- Multi-document analysis
- Export and reporting features
- Query history and document management interface

## Technical Specifications

- Language: Python 3.9+
- Interface: Streamlit web framework
- Storage: Local filesystem with ChromaDB
- Models: GPT-2 for text generation
- Embeddings: all-MiniLM-L6-v2
- Platform: macOS with Apple Silicon support

## Privacy and Security

- All processing happens locally on your computer
- Documents never leave your machine
- No internet connection required for operation
- No telemetry or data collection
- Professional-grade security for sensitive documents

## Performance

Memory usage is optimized for standard laptop specifications:
- Embeddings model: ~100MB
- Language model: ~500MB
- Vector database: Variable based on documents
- Total baseline: <1GB RAM

Designed to run efficiently on MacBook Air and similar hardware without dedicated graphics processing.

## License and Attribution

This project is part of the MasterDexter AI Engineer Accelerator program. See LICENSE file for details.

## Support and Issues

For bug reports, feature requests, or questions, please use the GitHub Issues tab. Issues will be reviewed and assigned by project maintainers.