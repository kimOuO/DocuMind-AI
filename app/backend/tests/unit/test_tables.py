"""Finding table regions in a page's text, so that a table is one chunk (AC-14).

A region starts at a caption line ("Table N:") and runs through the header and
number rows that follow, ending at the first line of prose. A caption followed
by prose (a case-study table) is not a region.
"""

from pathlib import Path

import pytest

from app.ingestion.parsing import parse_document
from app.ingestion.tables import find_table_regions, split_table

SAMPLE_PAPER = Path(__file__).resolve().parents[4] / "sample-documents" / "2410.05779v3.pdf"


class WordTokenizer:
    def count(self, text: str) -> int:
        return len(text.split())


@pytest.fixture(scope="module")
def paper() -> dict[int, str]:
    return {page.number: page.text for page in parse_document(SAMPLE_PAPER, "pdf")}


def test_table_2_is_one_region_from_its_caption_to_its_last_row(paper: dict[int, str]) -> None:
    regions = find_table_regions(paper[8])

    assert len(regions) == 1
    text = paper[8][regions[0][0] : regions[0][1]]
    lines = text.splitlines()
    assert lines[0].startswith("Table 2: Performance of ablated versions of LightRAG")
    assert lines[1] == "Agriculture CS Legal Mix"
    assert lines[-1] == "Overall 25.6% 74.4% 39.2% 60.8% 15.6% 84.4% 44.4% 55.6%"
    assert len(lines) == 22  # caption, 2 header lines, 4 blocks of (header + 4 rows) - 1
    assert "NaiveRAG -High NaiveRAG -High" in text and "NaiveRAG -Origin" in text
    assert "Low-level-only Retrieval" not in text  # the prose after the table


def test_table_1_is_one_region_with_all_sixteen_rows(paper: dict[int, str]) -> None:
    regions = find_table_regions(paper[7])

    assert len(regions) == 1
    text = paper[7][regions[0][0] : regions[0][1]]
    assert text.startswith("Table 1: Win rates")
    assert sum(1 for line in text.splitlines() if line.startswith("Overall ")) == 4


def test_a_caption_followed_by_prose_is_not_a_region(paper: dict[int, str]) -> None:
    # Table 3 (page 9) is a case study: text cells, no number rows. Figure 2's
    # numbers on the same page have no table caption.
    assert find_table_regions(paper[9]) == []
    # Pages without tables.
    assert find_table_regions(paper[1]) == []
    assert find_table_regions(paper[4]) == []


def test_a_synthetic_table_region_ends_at_the_first_prose_line() -> None:
    text = (
        "Some introduction sentence that ends here.\n"
        "Table 9: Made-up numbers.\n"
        "A B C\n"
        "x 1.0% 2.0% 3.0%\n"
        "y 4.0% 5.0% 6.0%\n"
        "This sentence explains the table and is clearly prose.\n"
        "z 7.0% 8.0% 9.0%\n"
    )

    [(start, end)] = find_table_regions(text)

    assert text[start:end] == "Table 9: Made-up numbers.\nA B C\nx 1.0% 2.0% 3.0%\ny 4.0% 5.0% 6.0%"


def test_a_table_too_long_for_one_chunk_is_split_by_rows_with_its_headers_repeated() -> None:
    header = "Table 9: Made-up numbers.\nA B C"
    rows = [f"r{i} 1.0% 2.0% 3.0%" for i in range(6)]  # 4 words each
    text = header + "\n" + "\n".join(rows)

    pieces = split_table(text, WordTokenizer(), max_tokens=14)

    # Header is 7 words; 14 leaves room for one row... no: 7 + 4 = 11, 7 + 8 = 15 > 14.
    assert pieces == [header + "\n" + rows[i] for i in range(6)]
    assert split_table(text, WordTokenizer(), max_tokens=100) == [text]
