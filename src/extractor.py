"""
extractor.py — Text Extraction Module
======================================
Handles extraction of raw text from PDF, DOCX, and TXT resume files.
Supports both file paths (strings) and in-memory BytesIO streams
(as returned by Streamlit's file_uploader).
"""

import io
import logging

# ── PDF libraries ──────────────────────────────────────────────────────────────
try:
    import pdfplumber  # Preferred: better layout handling
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False

try:
    import PyPDF2  # Fallback PDF reader
    PYPDF2_AVAILABLE = True
except ImportError:
    PYPDF2_AVAILABLE = False

# ── DOCX library ───────────────────────────────────────────────────────────────
try:
    from docx import Document
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

logger = logging.getLogger(__name__)


def extract_text_from_pdf(file_obj) -> str:
    """
    Extract all text from a PDF file.

    Args:
        file_obj: A file path (str) or BytesIO stream.

    Returns:
        Concatenated text string from all pages.
    """
    text = ""

    # Wrap raw bytes in a BytesIO stream if needed
    if isinstance(file_obj, bytes):
        file_obj = io.BytesIO(file_obj)

    # Primary extractor: pdfplumber (handles complex layouts better)
    if PDFPLUMBER_AVAILABLE:
        try:
            with pdfplumber.open(file_obj) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            if text.strip():
                return text
        except Exception as e:
            logger.warning(f"pdfplumber failed: {e}. Trying PyPDF2...")
            # Reset stream position for the fallback
            if hasattr(file_obj, "seek"):
                file_obj.seek(0)

    # Fallback extractor: PyPDF2
    if PYPDF2_AVAILABLE:
        try:
            reader = PyPDF2.PdfReader(file_obj)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        except Exception as e:
            logger.error(f"PyPDF2 also failed: {e}")

    return text


def extract_text_from_docx(file_obj) -> str:
    """
    Extract all text from a DOCX (Word) file.

    Args:
        file_obj: A file path (str) or BytesIO stream.

    Returns:
        Concatenated text string from all paragraphs.
    """
    if not DOCX_AVAILABLE:
        logger.error("python-docx not installed. Cannot read .docx files.")
        return ""

    if isinstance(file_obj, bytes):
        file_obj = io.BytesIO(file_obj)

    try:
        doc = Document(file_obj)
        # Join all non-empty paragraph texts with newlines
        paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]
        return "\n".join(paragraphs)
    except Exception as e:
        logger.error(f"Failed to read DOCX: {e}")
        return ""


def extract_text_from_txt(file_obj) -> str:
    """
    Extract text from a plain text (.txt) file.

    Args:
        file_obj: A file path (str), BytesIO stream, or bytes.

    Returns:
        Decoded text string.
    """
    try:
        if isinstance(file_obj, bytes):
            return file_obj.decode("utf-8", errors="replace")
        if isinstance(file_obj, io.BytesIO):
            return file_obj.read().decode("utf-8", errors="replace")
        # Treat as file path
        with open(file_obj, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except Exception as e:
        logger.error(f"Failed to read TXT file: {e}")
        return ""


def extract_text(file_obj, filename: str) -> str:
    """
    Dispatch text extraction based on the file extension.

    Args:
        file_obj: File path (str), BytesIO, or bytes object.
        filename:  Original filename used to determine the file type.

    Returns:
        Extracted raw text, or empty string on failure.
    """
    ext = filename.lower().rsplit(".", 1)[-1] if "." in filename else ""

    if ext == "pdf":
        return extract_text_from_pdf(file_obj)
    elif ext in ("docx", "doc"):
        return extract_text_from_docx(file_obj)
    elif ext == "txt":
        return extract_text_from_txt(file_obj)
    else:
        logger.warning(f"Unsupported file type: .{ext} — attempting TXT read.")
        return extract_text_from_txt(file_obj)
