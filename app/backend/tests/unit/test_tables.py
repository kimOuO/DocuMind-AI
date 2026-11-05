"""Finding table regions in a page's text, so that a table is one chunk (AC-14).

A region starts at a caption line ("Table N:") and runs through the header and
number rows that follow, ending at the first line of prose. A caption followed
by prose (a case-study table) is not a region.
"""

from pathlib import Path

import pytest

from app.ingestion.parsing import parse_document
from app.ingestion.tables import find_table_regions, linearize_table, split_table

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


# --- Linearising rows: every figure next to its column labels -------------------------


TABLE = (
    "Table 2: Performance of ablated versions of LightRAG, using NaiveRAG as reference.\n"
    "Agriculture CS Legal Mix\n"
    "NaiveRAG LightRAG NaiveRAG LightRAG NaiveRAG LightRAG NaiveRAG LightRAG\n"
    "Comprehensiveness 32.4% 67.6% 38.4% 61.6% 16.4% 83.6% 38.8% 61.2%\n"
    "NaiveRAG -High NaiveRAG -High NaiveRAG -High NaiveRAG -High\n"
    "Overall 35.2% 64.8% 44.0% 56.0% 22.0% 78.0% 42.4% 57.6%"
)


def test_rows_of_a_grouped_header_table_are_written_cell_by_cell_with_their_labels() -> None:
    lines = linearize_table(TABLE).splitlines()

    assert lines[:3] == TABLE.splitlines()[:3]  # caption and header lines are kept
    assert lines[3] == (
        "Comprehensiveness — Agriculture: NaiveRAG 32.4%, LightRAG 67.6%; "
        "CS: NaiveRAG 38.4%, LightRAG 61.6%; Legal: NaiveRAG 16.4%, LightRAG 83.6%; "
        "Mix: NaiveRAG 38.8%, LightRAG 61.2%"
    )
    # A block header renames the sub-columns for the rows under it, and stays in the text.
    assert lines[4] == "NaiveRAG -High NaiveRAG -High NaiveRAG -High NaiveRAG -High"
    assert lines[5] == (
        "Overall — Agriculture: NaiveRAG 35.2%, -High 64.8%; CS: NaiveRAG 44.0%, -High 56.0%; "
        "Legal: NaiveRAG 22.0%, -High 78.0%; Mix: NaiveRAG 42.4%, -High 57.6%"
    )


def test_the_whole_of_table_2_linearises_with_its_sixteen_rows(paper: dict[int, str]) -> None:
    [(start, end)] = find_table_regions(paper[8])
    text = linearize_table(paper[8][start:end])

    rows = [line for line in text.splitlines() if " — " in line]
    assert len(rows) == 16
    assert rows[15].startswith("Overall — Agriculture: NaiveRAG 25.6%, -Origin 74.4%;")
    assert rows[7] == (
        "Overall — Agriculture: NaiveRAG 35.2%, -High 64.8%; CS: NaiveRAG 44.0%, -High 56.0%; "
        "Legal: NaiveRAG 22.0%, -High 78.0%; Mix: NaiveRAG 42.4%, -High 57.6%"
    )


def test_a_table_with_a_single_header_line_uses_it_as_the_column_names() -> None:
    text = (
        "Table 4: Statistics.\nDataset Documents Tokens\n"
        "Agriculture 12 2,017,886\nLegal 94 5,081,069"
    )

    lines = linearize_table(text).splitlines()

    assert lines[2] == "Agriculture — Documents: 12; Tokens: 2,017,886"
    assert lines[3] == "Legal — Documents: 94; Tokens: 5,081,069"


def test_rows_that_do_not_match_the_header_shape_are_kept_as_they_are() -> None:
    text = "Table 9: Odd.\nA B\nx 1 2 3\ny 4 5"  # 3 figures under 2 columns, then 2

    lines = linearize_table(text).splitlines()

    assert lines[2] == "x 1 2 3"
    assert lines[3] == "y — A: 4; B: 5"


def test_a_table_without_a_readable_header_is_left_unchanged() -> None:
    text = "Table 9: No header.\n1 2 3\n4 5 6"
    assert linearize_table(text) == text
