"""Splitting a document into the units that get summarised.

Boundaries come from the recognised headings (number and page), never from
the heading text. References are left out. A unit that is too long for one
summary call is split into its subsections, then into batches.
"""

from pathlib import Path

import pytest

from app.ingestion.headings import find_headings
from app.ingestion.parsing import Page, parse_document
from app.ingestion.sections import SummaryUnit, plan_summary_units
from app.llm.tokenizer import Qwen3TokenCounter

SAMPLE_PDF = Path(__file__).resolve().parents[4] / "sample-documents" / "2410.05779v3.pdf"


class WordTokenizer:
    def count(self, text: str) -> int:
        return len(text.split())


@pytest.fixture(scope="module")
def tokenizer() -> Qwen3TokenCounter:
    return Qwen3TokenCounter()


@pytest.fixture(scope="module")
def paper_pages() -> list[Page]:
    return parse_document(SAMPLE_PDF, "pdf")


def plan(pages: list[Page], counter, budget: int) -> list[SummaryUnit]:  # type: ignore[no-untyped-def]
    return plan_summary_units(pages, find_headings(pages), counter, budget_tokens=budget)


def test_the_paper_splits_into_its_top_level_sections_without_the_references(
    paper_pages: list[Page], tokenizer: Qwen3TokenCounter
) -> None:
    units = plan(paper_pages, tokenizer, 6_000)

    assert [(u.number, u.title, u.page_start, u.page_end) for u in units] == [
        (None, "Front matter", 1, 1),
        ("1", "INTRODUCTION", 1, 2),
        ("2", "RETRIEVAL-AUGMENTED GENERATION", 2, 3),
        ("3", "THE LIGHT RAG ARCHITECTURE", 3, 5),
        ("4", "EVALUATION", 5, 10),
        ("5", "RELATED WORK", 10, 10),
        ("6", "CONCLUSION", 10, 10),
        ("7", "APPENDIX", 13, 16),
    ]
    assert all(0 < u.token_count <= 6_000 for u in units)
    assert all(u.token_count == tokenizer.count(u.text) for u in units)
    # The abstract is in the front matter; the reference list (pages 11-12) is nowhere.
    assert "ABSTRACT" in units[0].text
    joined = "\n".join(u.text for u in units)
    assert not any(line.strip() == "REFERENCES" for line in joined.splitlines())
    assert "Congrat: Self-supervised contrastive pretraining" not in joined  # the first reference
    assert all(not (11 <= u.page_start <= 12 or 11 <= u.page_end <= 12) for u in units)
    # Each unit starts with its heading line and the text is the document's own.
    assert units[4].text.startswith("4 E VALUATION")
    assert "Table 2: Performance of ablated versions" in units[4].text


def test_a_section_over_the_budget_is_split_into_its_subsections(
    paper_pages: list[Page], tokenizer: Qwen3TokenCounter
) -> None:
    units = plan(paper_pages, tokenizer, 3_000)

    evaluation = [u for u in units if (u.number or "").startswith("4")]
    assert [(u.number, u.title) for u in evaluation] == [
        ("4", "EVALUATION"),  # the paragraph before 4.1
        ("4.1", "EXPERIMENTAL SETTINGS"),
        ("4.2", "COMPARISON OF LIGHT RAG WITH EXISTING RAG METHODS (RQ1)"),
        ("4.3", "ABLATION STUDIES (RQ2)"),
        ("4.4", "CASE STUDY (RQ3)"),
        ("4.5", "MODEL COST AND ADAPTABILITY ANALYSIS (RQ4)"),
    ]
    assert all(u.token_count <= 3_000 for u in units)
    assert (evaluation[3].page_start, evaluation[3].page_end) == (7, 8)
    # Other sections that fit stay whole.
    assert [u.number for u in units if (u.number or "").startswith("3")] == ["3"]


def test_a_unit_still_over_the_budget_is_cut_into_batches_by_page() -> None:
    pages = [Page(n, f"{'word ' * 100}") for n in range(1, 6)]  # 100 words per page, no headings

    units = plan_summary_units(pages, [], WordTokenizer(), budget_tokens=250)

    assert [(u.number, u.title, u.page_start, u.page_end, u.token_count) for u in units] == [
        (None, "Part 1", 1, 2, 200),
        (None, "Part 2", 3, 4, 200),
        (None, "Part 3", 5, 5, 100),
    ]


def test_a_single_page_over_the_budget_is_cut_within_the_page() -> None:
    pages = [Page(1, "word " * 500)]

    units = plan_summary_units(pages, [], WordTokenizer(), budget_tokens=200)

    assert [u.token_count for u in units] == [200, 200, 100]
    assert all((u.page_start, u.page_end) == (1, 1) for u in units)
    assert " ".join(u.text for u in units).split() == ["word"] * 500


def test_markdown_headings_make_the_units() -> None:
    text = (
        "# Notes on LightRAG\n\nIntro line.\n\n"
        "## Indexing\n\nGraph text.\n\n## Retrieval\n\nDual level.\n"
    )
    pages = [Page(1, text)]

    headings = find_headings(pages)

    # The whole note fits one call: one unit, named after the top heading.
    whole = plan_summary_units(pages, headings, WordTokenizer(), budget_tokens=1_000)
    # Too long for one call: split at the second-level headings.
    split = plan_summary_units(pages, headings, WordTokenizer(), budget_tokens=6)

    assert [(u.number, u.title) for u in whole] == [(None, "Notes on LightRAG")]
    assert [(u.number, u.title) for u in split] == [
        (None, "Notes on LightRAG"),  # the intro line, before the first subsection
        (None, "Indexing"),
        (None, "Retrieval"),
    ]
    assert split[1].text == "## Indexing\n\nGraph text."


def test_a_document_without_headings_is_one_unit_when_it_fits() -> None:
    pages = [Page(1, "Just a short note.")]

    units = plan_summary_units(pages, [], WordTokenizer(), budget_tokens=100)

    assert [(u.number, u.title, u.text) for u in units] == [
        (None, "Full text", "Just a short note.")
    ]


def test_empty_pages_add_nothing() -> None:
    assert (
        plan_summary_units([Page(1, ""), Page(2, "  \n")], [], WordTokenizer(), budget_tokens=100)
        == []
    )
