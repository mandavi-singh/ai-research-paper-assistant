"""PDF processing utilities."""

from PyPDF2 import PdfReader


CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


def extract_text_from_pdf(pdf_file) -> str:
    """Extract all text from an uploaded PDF file."""
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text.strip()


def get_text_chunks(text: str) -> list[str]:
    """Split text into overlapping chunks."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + CHUNK_SIZE
        chunk = text[start:end]
        if chunk.strip():
            chunks.append(chunk)
        start += CHUNK_SIZE - CHUNK_OVERLAP
    return chunks
