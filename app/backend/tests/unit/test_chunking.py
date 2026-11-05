"""Chunking by token count, page by page: fixed-size prose, tables whole (AC-03, AC-14)."""

import re
from pathlib import Path

import pytest

from app.ingestion.chunking import chunk_pages
from app.ingestion.parsing import Page, parse_document
from app.llm.tokenizer import Qwen3TokenCounter

SAMPLE_PAPER = Path(__file__).resolve().parents[4] / "sample-documents" / "2410.05779v3.pdf"


class WordTokenizer:
    """One token per whitespace-separated word, so expected chunks are easy to state."""

    def count(self, text: str) -> int:
        return len(text.split())

    def spans(self, text: str) -> list[tuple[int, int]]:
        return [match.span() for match in re.finditer(r"\S+", text)]


def _words(first: int, last: int) -> str:
    return " ".join(f"w{index}" for index in range(first, last))


def test_chunks_have_a_fixed_size_and_overlap() -> None:
    page = Page(number=1, text=_words(0, 25))

    chunks = chunk_pages([page], WordTokenizer(), chunk_size=10, overlap=3)

    assert [chunk.text for chunk in chunks] == [
        _words(0, 10),
        _words(7, 17),
        _words(14, 24),
        _words(21, 25),
    ]
    assert [chunk.token_count for chunk in chunks] == [10, 10, 10, 4]
    assert [chunk.ordinal for chunk in chunks] == [0, 1, 2, 3]


def test_a_short_page_is_a_single_chunk() -> None:
    chunks = chunk_pages([Page(1, _words(0, 4))], WordTokenizer(), chunk_size=10, overlap=3)

    assert [(chunk.page, chunk.text) for chunk in chunks] == [(1, _words(0, 4))]


def test_the_last_chunk_is_not_a_repeat_of_the_previous_one() -> None:
    # Exactly one window: the overlap alone must not become a second chunk.
    chunks = chunk_pages([Page(1, _words(0, 10))], WordTokenizer(), chunk_size=10, overlap=3)

    assert len(chunks) == 1


def test_chunks_never_cross_a_page_and_keep_its_number() -> None:
    pages = [Page(1, _words(0, 12)), Page(2, ""), Page(3, _words(100, 105))]

    chunks = chunk_pages(pages, WordTokenizer(), chunk_size=10, overlap=3)

    assert [(chunk.ordinal, chunk.page) for chunk in chunks] == [(0, 1), (1, 1), (2, 3)]
    assert chunks[1].text == _words(7, 12)
    assert chunks[2].text == _words(100, 105)


def test_pages_without_text_produce_no_chunks() -> None:
    assert (
        chunk_pages([Page(1, ""), Page(2, " \n ")], WordTokenizer(), chunk_size=10, overlap=3) == []
    )


@pytest.mark.parametrize(("chunk_size", "overlap"), [(0, 0), (10, 10), (10, 11), (10, -1)])
def test_invalid_sizes_are_refused(chunk_size: int, overlap: int) -> None:
    with pytest.raises(ValueError):
        chunk_pages([Page(1, "a b c")], WordTokenizer(), chunk_size=chunk_size, overlap=overlap)


@pytest.fixture(scope="module")
def tokenizer() -> Qwen3TokenCounter:
    return Qwen3TokenCounter()


def test_the_real_tokenizer_never_exceeds_the_chunk_size_on_chinese_text(
    tokenizer: Qwen3TokenCounter,
) -> None:
    text = "本地執行的文件問答平台，回答必須附上來源：檔名、頁碼與片段。" * 60

    chunks = chunk_pages([Page(1, text)], tokenizer, chunk_size=50, overlap=10)

    assert len(chunks) > 5
    assert all(0 < chunk.token_count <= 50 for chunk in chunks)
    assert all(chunk.token_count == tokenizer.count(chunk.text) for chunk in chunks)
    # Nothing is lost: every character of the page is in some chunk.
    assert chunks[0].text.startswith("本地執行")
    assert chunks[-1].text.endswith("片段。")


def test_the_sample_paper_is_chunked_within_the_configured_size(
    tokenizer: Qwen3TokenCounter,
) -> None:
    """AC-03: no chunk exceeds the chunk size, and each records its page."""
    pages = parse_document(SAMPLE_PAPER, "pdf")

    chunks = chunk_pages(pages, tokenizer, chunk_size=400, overlap=80)

    assert all(0 < c.token_count <= 400 for c in chunks if not c.text.startswith("Table "))
    assert all(chunk.token_count == tokenizer.count(chunk.text) for chunk in chunks)
    assert {chunk.page for chunk in chunks} == set(range(1, 17))
    assert [chunk.ordinal for chunk in chunks] == list(range(len(chunks)))
    # Pages appear in order, and each chunk's text comes from its own page.
    assert [chunk.page for chunk in chunks] == sorted(chunk.page for chunk in chunks)
    by_page = {page.number: page.text for page in pages}
    tables = [c for c in chunks if c.text.startswith("Table ") and " — " in c.text]
    assert all(chunk.text in by_page[chunk.page] for chunk in chunks if chunk not in tables)
    # A table chunk is rewritten cell by cell, but every figure in it is the page's own.
    for table in tables:
        figures = re.findall(r"\d[\d,]*(?:\.\d+)?%?", table.text)
        assert figures and all(figure in by_page[table.page] for figure in figures)
    assert [(t.page, t.text[:8]) for t in tables] == [
        (7, "Table 1:"),
        (8, "Table 2:"),
        (13, "Table 4:"),
    ]
    # Table 2, which question 3 needs, is one chunk: every row next to its headers.
    [table] = [c for c in chunks if c.text.startswith("Table 2: Performance of ablated")]
    assert table.page == 8 and 400 < table.token_count <= 4 * 400
    assert table.text.count("Overall — ") == 4 and "Agriculture CS Legal Mix" in table.text
    assert table.text.endswith(
        "Overall — Agriculture: NaiveRAG 25.6%, -Origin 74.4%; CS: NaiveRAG 39.2%, -Origin 60.8%; "
        "Legal: NaiveRAG 15.6%, -Origin 84.4%; Mix: NaiveRAG 44.4%, -Origin 55.6%"
    )
    # The prose after the table starts a fresh chunk and does not repeat the table.
    after = chunks[table.ordinal + 1]
    assert after.page == 8 and after.text.startswith("• Low-level-only Retrieval")
    # Only table chunks may exceed the chunk size.
    oversize = [c for c in chunks if c.token_count > 400]
    assert all(c.text.startswith("Table ") for c in oversize) and len(oversize) == 2


def test_a_table_region_is_one_chunk_and_the_prose_around_it_is_chunked_as_usual() -> None:
    table = "Table 1: Numbers.\nA B\n" + "\n".join(f"r{i} 1% 2%" for i in range(10))
    page = Page(number=3, text=f"{_words(0, 7)}\n{table}\n{_words(100, 112)}")

    chunks = chunk_pages([page], WordTokenizer(), chunk_size=5, overlap=1)

    assert chunks[0].text == _words(0, 5) and chunks[1].text == _words(4, 7)
    # The table (10 rows of 6 words once linearised) exceeds 4 x 5, so it is split by
    # rows, headers repeated.
    table_chunks = [c for c in chunks if c.text.startswith("Table 1: Numbers.")]
    assert len(table_chunks) == 5
    assert all(c.text.startswith("Table 1: Numbers.\nA B\n") for c in table_chunks)
    assert all(c.token_count <= 20 for c in table_chunks)
    rows = [line for c in table_chunks for line in c.text.splitlines()[2:]]
    assert rows == [f"r{i} — A: 1%; B: 2%" for i in range(10)]
    assert chunks[-1].text.endswith("w111")
    assert [c.ordinal for c in chunks] == list(range(len(chunks)))
    assert all(c.page == 3 for c in chunks)
