"""Turn an uploaded file into pages of text, using local libraries only.

No file is ever handed to an LLM or a cloud service. PDF text is extracted
with pypdf in its default mode (chosen by experiment, see ADR 0005).
"""

from dataclasses import dataclass
from pathlib import Path

from pypdf import PdfReader
from pypdf.errors import PyPdfError


@dataclass(frozen=True)
class Page:
    number: int  # starts at 1
    text: str


class DocumentParseError(Exception):
    """The file cannot be turned into text. The message is shown to the user."""


class NoTextFoundError(DocumentParseError):
    """The file was read, but it contains no text (for example a scanned PDF)."""


def parse_document(path: Path, media_type: str) -> list[Page]:
    """Return the pages of a document. Text files are a single page.

    Pages without text are kept, so that page numbers always match the file.
    """
    if media_type == "pdf":
        pages = _parse_pdf(path)
    elif media_type in ("txt", "md"):
        pages = [Page(1, _clean(_read_text(path)))]
    else:
        raise ValueError(f"Unsupported media type: {media_type}")

    if not any(page.text.strip() for page in pages):
        raise NoTextFoundError(
            "No text could be extracted from this file. Scanned documents and images "
            "are not supported."
        )
    return pages


def _read_text(path: Path) -> str:
    try:
        return path.read_bytes().decode("utf-8-sig")
    except UnicodeDecodeError as error:
        raise DocumentParseError(
            "This text file is not encoded as UTF-8. Save it as UTF-8 and upload it again."
        ) from error


def _parse_pdf(path: Path) -> list[Page]:
    try:
        reader = PdfReader(path)
        if reader.is_encrypted:
            raise DocumentParseError("This PDF is protected by a password and cannot be read.")
        return [
            Page(number, _clean(page.extract_text() or ""))
            for number, page in enumerate(reader.pages, start=1)
        ]
    except DocumentParseError:
        raise
    except (PyPdfError, ValueError, KeyError, OSError) as error:
        raise DocumentParseError(f"This PDF could not be read: {error}") from error


def _clean(text: str) -> str:
    # PostgreSQL cannot store NUL in text; line endings are unified for counting.
    return text.replace("\x00", "").replace("\r\n", "\n").replace("\r", "\n")
