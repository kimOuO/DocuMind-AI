"""AC-53: section headings are recognised and normalised, and the limits are on record.

The ground truth is the paper's LaTeX source (evaluation/ground-truth/
paper-structure.json): 22 numbered section and subsection titles. pypdf splits
small-caps titles ("1 I NTRODUCTION"), so the normalised text is compared with
the truth and every title that cannot be restored by rule is listed here.
"""

import json
from pathlib import Path

import pytest

from app.ingestion.headings import Heading, find_headings, normalize_title
from app.ingestion.parsing import Page, parse_document

ROOT = Path(__file__).resolve().parents[4]
SAMPLE_PDF = ROOT / "sample-documents" / "2410.05779v3.pdf"
GROUND_TRUTH = ROOT / "evaluation" / "ground-truth" / "paper-structure.json"

# Page of each numbered heading in the PDF (checked by hand against the file, 2026-11-05).
EXPECTED_PAGES = {
    "1": 1, "2": 2, "3": 3, "3.1": 3, "3.2": 4, "3.3": 5, "3.4": 5, "4": 5, "4.1": 5,
    "4.2": 6, "4.3": 7, "4.4": 8, "4.5": 9, "5": 10, "5.1": 10, "5.2": 10, "6": 10,
    "7": 13, "7.1": 13, "7.2": 13, "7.3": 14, "7.4": 16,
}  # fmt: skip

# Titles pypdf splits inside a word in a way no rule can tell apart from two words
# ("LIGHT RAG", "LLM S", "NAIVE RAG"). Known limitation of the chosen parser (ADR 0005).
KNOWN_UNRECOVERABLE = {"3", "3.4", "4.2", "5.1", "7.2", "7.3", "7.4"}


def numbered_truth() -> dict[str, str]:
    """Ground-truth titles keyed by their section number."""
    headings = json.loads(GROUND_TRUTH.read_text(encoding="utf-8"))["headings"]
    numbered: dict[str, str] = {}
    section = subsection = 0
    for heading in headings:
        if heading["level"] == "section":
            section, subsection = section + 1, 0
            numbered[str(section)] = heading["title"]
        else:
            subsection += 1
            numbered[f"{section}.{subsection}"] = heading["title"]
    return numbered


@pytest.fixture(scope="module")
def paper_headings() -> list[Heading]:
    return find_headings(parse_document(SAMPLE_PDF, "pdf"))


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("I NTRODUCTION", "INTRODUCTION"),
        ("T HE LIGHT RAG A RCHITECTURE", "THE LIGHT RAG ARCHITECTURE"),  # LIGHT RAG stays split
        ("R ETRIEVAL -AUGMENTED GENERATION", "RETRIEVAL-AUGMENTED GENERATION"),
        ("G RAPH -BASED TEXT INDEXING", "GRAPH-BASED TEXT INDEXING"),
        (
            "C OMPARISON OF LIGHT RAG WITH EXISTING RAG M ETHODS (RQ1)",
            "COMPARISON OF LIGHT RAG WITH EXISTING RAG METHODS (RQ1)",
        ),
        (
            "C ASE EXAMPLE OF RETRIEVAL -AUGMENTED GENERATION IN LIGHT RAG.",
            "CASE EXAMPLE OF RETRIEVAL-AUGMENTED GENERATION IN LIGHT RAG",
        ),
        ("P ROMPTS FOR RAG E VALUATION", "PROMPTS FOR RAG EVALUATION"),
        # Ordinary text is left alone: a one-letter word before a real word is not a split.
        ("Introduction", "Introduction"),
        ("A Survey of Graphs", "A Survey of Graphs"),
        ("  Related   Work  ", "Related Work"),
    ],
)
def test_split_small_caps_are_joined(raw: str, expected: str) -> None:
    assert normalize_title(raw) == expected


def test_every_numbered_heading_is_found_with_its_number_and_page(
    paper_headings: list[Heading],
) -> None:
    found = {
        heading.number: heading.page
        for heading in paper_headings
        if heading.number in EXPECTED_PAGES
    }

    assert found == EXPECTED_PAGES
    # Headings appear in document order.
    positions = [(h.page, h.line) for h in paper_headings]
    assert positions == sorted(positions)


def test_deeper_levels_in_the_appendix_are_found_too(paper_headings: list[Heading]) -> None:
    deeper = [
        (h.number, h.level, h.title) for h in paper_headings if h.number not in EXPECTED_PAGES
    ]

    assert deeper == [
        ("7.3.1", 3, "PROMPTS FOR GRAPH GENERATION"),
        ("7.3.2", 3, "PROMPTS FOR QUERY GENERATION"),
        ("7.3.3", 3, "PROMPTS FOR KEYWORD EXTRACTION"),
        ("7.3.4", 3, "PROMPTS FOR RAG EVALUATION"),
    ]
    assert {h.level for h in paper_headings if h.number in EXPECTED_PAGES} == {1, 2}


def test_normalised_titles_match_the_ground_truth_except_the_known_cases(
    paper_headings: list[Heading],
) -> None:
    """AC-53: the match count is recorded, and every unrecoverable title is listed."""
    truth = numbered_truth()
    by_number = {h.number: h for h in paper_headings}

    matched = {n for n, title in truth.items() if by_number[n].title.casefold() == title.casefold()}
    unrecoverable = set(truth) - matched

    assert len(truth) == 22
    assert len(matched) == 15
    assert unrecoverable == KNOWN_UNRECOVERABLE
    # The unrecoverable ones differ only by a space inside a name, never in meaning.
    for number in unrecoverable:
        assert (
            by_number[number].title.replace(" ", "").casefold()
            == truth[number].replace(" ", "").casefold()
        )


def test_the_raw_text_is_kept_next_to_the_normalised_title(paper_headings: list[Heading]) -> None:
    first = paper_headings[0]

    assert (first.number, first.raw, first.title) == ("1", "1 I NTRODUCTION", "INTRODUCTION")


def test_table_rows_captions_and_body_text_are_not_headings() -> None:
    page = Page(
        1,
        "Table 2: Performance of ablated versions of LightRAG\n"
        "Comprehensiveness 32.4% 67.6% 38.4% 61.6%\n"
        "1 2 3 4\n"
        "1. Precision [...] 2. Recall [...]\n"
        "610 × 1,000 < 100\n"
        "In total, this process results in 125 questions for each dataset.\n"
        "2 R ETRIEVAL -AUGMENTED GENERATION\n",
    )

    assert [(h.number, h.title) for h in find_headings([page])] == [
        ("2", "RETRIEVAL-AUGMENTED GENERATION")
    ]


def test_markdown_style_numbered_headings_in_plain_text_are_found() -> None:
    page = Page(1, "1 Introduction\nSome text.\n1.1 Background\nMore text.\n")

    assert [(h.number, h.level, h.title) for h in find_headings([page])] == [
        ("1", 1, "Introduction"),
        ("1.1", 2, "Background"),
    ]
