"""
core/file_utils.py
PDF / TXT extraction and token-safe truncation helpers.
"""
import io

# ── PDF support ───────────────────────────────────────────────────────────────
try:
    from pypdf import PdfReader
    PDF_SUPPORT = True
except ImportError:
    try:
        from PyPDF2 import PdfReader          # type: ignore
        PDF_SUPPORT = True
    except ImportError:
        PDF_SUPPORT = False

MAX_WORDS = 3000  # Groq free tier TPM budget


def extract_text_from_file(uploaded_file) -> str:
    """Extract plain text from a Streamlit UploadedFile (PDF or TXT)."""
    name = uploaded_file.name.lower()

    if name.endswith(".txt"):
        return uploaded_file.read().decode("utf-8", errors="ignore")

    if name.endswith(".pdf"):
        if not PDF_SUPPORT:
            raise RuntimeError("pypdf is not installed. Run: pip install pypdf")
        reader = PdfReader(io.BytesIO(uploaded_file.read()))
        pages  = [p.extract_text() for p in reader.pages if p.extract_text()]
        return "\n\n".join(pages)

    return ""


def truncate_for_llm(text: str, max_words: int = MAX_WORDS) -> tuple[str, bool]:
    """
    Truncate text to max_words words.
    Preserves the first 80 % (Abstract, Intro, Methods) and last 20 % (Conclusion).
    Returns (truncated_text, was_truncated).
    """
    words = text.split()
    if len(words) <= max_words:
        return text, False

    head = int(max_words * 0.80)
    tail = max_words - head
    truncated = (
        " ".join(words[:head])
        + "\n\n[... middle sections omitted to fit token limit ...]\n\n"
        + " ".join(words[-tail:])
    )
    return truncated, True


def title_from_filename(filename: str) -> str:
    """Convert a filename to a readable title."""
    return (
        filename
        .replace(".pdf", "")
        .replace(".txt", "")
        .replace("_", " ")
        .replace("-", " ")
        .title()
    )