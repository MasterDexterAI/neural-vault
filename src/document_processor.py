import os
from pypdf import PdfReader


def load_pdf(file_path: str) -> list[dict]:
    """Extract text per page. Returns [{"page_number": int, "text": str}, ...]."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"PDF not found: {file_path}")

    reader = PdfReader(file_path)
    pages = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text and text.strip():
            pages.append({"page_number": i + 1, "text": text.strip()})
    return pages


def chunk_text(pages: list[dict], chunk_size: int = 1000, overlap: int = 200) -> list[dict]:
    """
    Chunk each page's text independently so every chunk retains its page_number.
    Returns [{"text": str, "page_number": int}, ...]
    """
    chunks = []
    for page_data in pages:
        for chunk in _split_text(page_data["text"], chunk_size, overlap):
            chunks.append({"text": chunk, "page_number": page_data["page_number"]})
    return chunks


def _split_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    """Split a single string into overlapping chunks, breaking at sentence boundaries."""
    if not text:
        return []

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        if end < text_length:
            for i in range(end, max(start + chunk_size // 2, start), -1):
                if text[i - 1] in ".!?":
                    end = i
                    break

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        start = end - overlap

    return chunks
