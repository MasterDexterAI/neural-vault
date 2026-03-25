import os
from pypdf import PdfReader

def load_pdf(file_path: str) -> str:
    """Extract text from PDF"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"PDF not found: {file_path}")
    
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text.strip()

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> list[str]:
    """Simple recursive-style chunker without LangChain"""
    if not text:
        return []
    
    chunks = []
    start = 0
    text_length = len(text)
    
    while start < text_length:
        end = start + chunk_size
        # Try to break at sentence end for better quality
        if end < text_length:
            # Look for period, question mark, etc.
            for i in range(end, max(start + chunk_size // 2, start), -1):
                if text[i-1] in ".!?":
                    end = i
                    break
        
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        
        start = end - overlap  # overlap for context continuity
    
    return chunks