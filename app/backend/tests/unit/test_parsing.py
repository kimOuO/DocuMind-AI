"""Parsing uploaded files into pages of text, with local libraries only."""

from pathlib import Path

import pytest
from pypdf import PdfWriter

from app.ingestion.parsing import DocumentParseError, NoTextFoundError, Page, parse_document

SAMPLE_PAPER = Path(__file__).resolve().parents[4] / "sample-documents" / "2410.05779v3.pdf"


def _write(tmp_path: Path, name: str, content: bytes) -> Path:
    path = tmp_path / name
    path.write_bytes(content)
    return path


def test_a_text_file_is_one_page(tmp_path: Path) -> None:
    path = _write(tmp_path, "notes.txt", "第一行\nsecond line\n".encode())

    assert parse_document(path, "txt") == [Page(number=1, text="第一行\nsecond line\n")]


def test_markdown_is_kept_as_written(tmp_path: Path) -> None:
    source = "# Title\n\n| a | b |\n|---|---|\n| 1 | 2 |\n"
    path = _write(tmp_path, "notes.md", source.encode())

    assert parse_document(path, "md") == [Page(number=1, text=source)]


def test_byte_order_mark_and_windows_line_endings_are_normalised(tmp_path: Path) -> None:
    path = _write(tmp_path, "notes.txt", b"\xef\xbb\xbfone\r\ntwo\r\n")

    assert parse_document(path, "txt") == [Page(number=1, text="one\ntwo\n")]


def test_null_characters_are_removed(tmp_path: Path) -> None:
    # PostgreSQL cannot store a NUL character in text.
    path = _write(tmp_path, "notes.txt", b"one\x00two")

    assert parse_document(path, "txt")[0].text == "onetwo"


def test_a_text_file_that_is_not_utf8_is_refused_with_a_reason(tmp_path: Path) -> None:
    path = _write(tmp_path, "big5.txt", "繁體中文".encode("big5"))

    with pytest.raises(DocumentParseError, match="UTF-8"):
        parse_document(path, "txt")


def test_utf16_is_refused_rather_than_guessed(tmp_path: Path) -> None:
    path = _write(tmp_path, "utf16.txt", "繁體中文 text".encode("utf-16"))

    with pytest.raises(DocumentParseError, match="UTF-8"):
        parse_document(path, "txt")


def test_the_reason_tells_the_user_what_to_do(tmp_path: Path) -> None:
    path = _write(tmp_path, "big5.md", "繁體中文".encode("big5"))

    with pytest.raises(DocumentParseError) as raised:
        parse_document(path, "md")

    assert str(raised.value) == (
        "This text file is not encoded as UTF-8. Save it as UTF-8 and upload it again."
    )


def test_a_file_with_only_whitespace_has_no_text(tmp_path: Path) -> None:
    path = _write(tmp_path, "blank.txt", b" \n\t\n")

    with pytest.raises(NoTextFoundError):
        parse_document(path, "txt")


def test_the_sample_paper_is_read_page_by_page() -> None:
    pages = parse_document(SAMPLE_PAPER, "pdf")

    assert [page.number for page in pages] == list(range(1, 17))
    assert "ABSTRACT" in pages[0].text
    # Table 2 is on page 8, one table row per line.
    assert "Table 2: Performance of ablated versions" in pages[7].text
    assert "Comprehensiveness 32.4% 67.6% 38.4% 61.6% 16.4% 83.6% 38.8% 61.2%" in pages[7].text
    assert all("\x00" not in page.text for page in pages)


def test_a_pdf_without_any_text_is_reported(tmp_path: Path) -> None:
    writer = PdfWriter()
    writer.add_blank_page(width=200, height=200)
    path = tmp_path / "blank.pdf"
    with path.open("wb") as handle:
        writer.write(handle)

    with pytest.raises(NoTextFoundError):
        parse_document(path, "pdf")


def test_a_pdf_keeps_the_page_numbers_of_pages_without_text(tmp_path: Path) -> None:
    writer = PdfWriter()
    writer.add_blank_page(width=200, height=200)
    writer.append(str(SAMPLE_PAPER), pages=(0, 1))
    path = tmp_path / "mixed.pdf"
    with path.open("wb") as handle:
        writer.write(handle)

    pages = parse_document(path, "pdf")

    # The blank first page is still page 1; the paper's first page is page 2.
    assert [page.number for page in pages] == [1, 2]
    assert pages[0].text == ""
    assert "ABSTRACT" in pages[1].text


def test_a_broken_pdf_is_refused_with_a_reason(tmp_path: Path) -> None:
    path = _write(tmp_path, "broken.pdf", b"this is not a pdf at all")

    with pytest.raises(DocumentParseError):
        parse_document(path, "pdf")


def test_a_password_protected_pdf_is_refused_with_a_reason(tmp_path: Path) -> None:
    writer = PdfWriter()
    writer.append(str(SAMPLE_PAPER), pages=(0, 1))
    writer.encrypt("secret")
    path = tmp_path / "locked.pdf"
    with path.open("wb") as handle:
        writer.write(handle)

    with pytest.raises(DocumentParseError, match="password"):
        parse_document(path, "pdf")


def test_an_unknown_media_type_is_a_programming_error(tmp_path: Path) -> None:
    path = _write(tmp_path, "notes.docx", b"x")

    with pytest.raises(ValueError):
        parse_document(path, "docx")
