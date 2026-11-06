"""Building the answer prompt within its budget, and reading citations back."""

import uuid

import pytest

from app.chat.prompting import (
    build_answer_prompt,
    build_summary_prompt,
    cited_indexes,
    question_language,
    source_payload,
    summary_source_payload,
)
from app.llm.tokenizer import Qwen3TokenCounter
from app.retrieval.repository import RetrievedChunk
from app.summarization.repository import StoredSummary


def chunk(
    text: str, *, page: int = 1, filename: str = "paper.pdf", score: float = 0.6
) -> RetrievedChunk:
    return RetrievedChunk(
        chunk_id=uuid.uuid4(),
        document_id=uuid.uuid4(),
        filename=filename,
        page=page,
        ordinal=0,
        text=text,
        token_count=0,
        score=score,
    )


@pytest.fixture(scope="module")
def counter() -> Qwen3TokenCounter:
    return Qwen3TokenCounter()


def test_the_prompt_numbers_the_sources_and_ends_with_the_question(
    counter: Qwen3TokenCounter,
) -> None:
    chunks = [
        chunk("LightRAG builds a graph.", page=3),
        chunk("GraphRAG uses communities.", page=9),
    ]

    prompt, used = build_answer_prompt("compare lightRAG with GraphRAG", chunks, counter, 5_500)

    assert used == chunks
    assert "[1] paper.pdf, page 3\nLightRAG builds a graph." in prompt
    assert "[2] paper.pdf, page 9\nGraphRAG uses communities." in prompt
    assert prompt.index("[1] paper.pdf") < prompt.index("[2] paper.pdf")
    assert prompt.rstrip().endswith("Question: compare lightRAG with GraphRAG\nAnswer:")
    # The rules the answer must follow are stated before the sources.
    assert prompt.index("only the numbered sources") < prompt.index("[1] paper.pdf")
    assert "square brackets" in prompt
    assert "do not contain" in prompt


def test_sources_that_do_not_fit_the_evidence_budget_are_left_out_whole(
    counter: Qwen3TokenCounter,
) -> None:
    long_text = "The quick brown fox jumps over the lazy dog. " * 40  # about 400 tokens
    chunks = [chunk(long_text, page=n) for n in range(1, 6)]

    prompt, used = build_answer_prompt("What jumps?", chunks, counter, 1_000)

    # Two fit; the third would exceed the budget and is dropped, never cut short.
    assert [c.page for c in used] == [1, 2]
    assert "[3] paper.pdf" not in prompt
    assert prompt.count(long_text.strip()) == 2
    evidence = sum(
        counter.count(f"[{i}] paper.pdf, page {c.page}\n{c.text}") for i, c in enumerate(used, 1)
    )
    assert evidence <= 1_000


@pytest.mark.parametrize(
    ("question", "expected"),
    [
        ("compare lightRAG with GraphRAG", "other"),
        ("LightRAG 跟 GraphRAG 的差異？", "zh"),
        ("請摘要這份文件", "zh"),
        ("Table 2 的數字", "zh"),
    ],
)
def test_the_language_of_the_question_is_recognised(question: str, expected: str) -> None:
    assert question_language(question) == expected


def test_a_chinese_question_asks_for_traditional_chinese(counter: Qwen3TokenCounter) -> None:
    chinese, _ = build_answer_prompt("請摘要這份文件", [], counter, 100)
    english, _ = build_answer_prompt("summary this document.", [], counter, 100)

    assert "Traditional Chinese (繁體中文" in chinese and "never in Simplified" in chinese
    assert "繁體中文" not in english and "language of the question" in english


def test_the_instructions_fit_their_budget(counter: Qwen3TokenCounter) -> None:
    prompt, _ = build_answer_prompt("q", [], counter, 5_500)

    # Everything except the sources and the question: the 500 tokens reserved for instructions.
    assert counter.count(prompt) <= 500


def test_the_instructions_ask_for_findings_first_labelled_figures_and_exceptions() -> None:
    """D63: general principles for experimental results, nothing about any one document."""
    prompt, _ = build_answer_prompt("q", [], WordCounter(), 5_500)

    assert "the main findings; representative figures" in prompt
    assert "Do not list every number" in prompt
    assert "which method or variant, which dataset, which metric, its unit, and what it" in prompt
    assert "go against the trend, named explicitly" in prompt
    # D68: the conclusion may not outrun the figures, and must carry any exception named.
    assert "a conclusion that is no stronger than the figures you gave" in prompt
    assert "If you named an exception, the conclusion must carry it too" in prompt
    assert "LightRAG" not in prompt and "Origin" not in prompt and "page 8" not in prompt


def test_a_table_source_is_marked_as_one(counter: Qwen3TokenCounter) -> None:
    """D68: the model sees which source is a table, so a figure is cited to it."""
    table = chunk(
        "Table 2: Win rates.\nAgriculture Mix\nLightRAG -High LightRAG -High\n"
        "Overall 67.6% 64.8% 60.0% 57.6%",
        page=8,
    )
    prompt, _ = build_answer_prompt("q", [table, chunk("Prose.", page=9)], counter, 5_500)

    assert "[1] paper.pdf, page 8 (a table)\nTable 2: Win rates." in prompt
    assert "[2] paper.pdf, page 9\nProse." in prompt


def test_the_instructions_ask_for_the_source_that_states_each_statement() -> None:
    """D68: a citation points at the source whose text states the statement."""
    prompt, _ = build_answer_prompt("q", [], WordCounter(), 5_500)

    assert "cite the source whose text states that statement" in prompt
    assert "A source about the same topic is not enough" in prompt
    assert "two neighbouring statements may need different sources" in prompt


def test_a_source_payload_carries_what_the_interface_shows(counter: Qwen3TokenCounter) -> None:
    source = chunk("Table 2: Performance of ablated versions", page=8, score=0.612345)

    payload = source_payload(1, source)

    assert payload == {
        "index": 1,
        "kind": "chunk",
        "document_id": str(source.document_id),
        "filename": "paper.pdf",
        "page_start": 8,
        "page_end": 8,
        "section_title": None,
        "snippet": "Table 2: Performance of ablated versions",
        "score": 0.6123,
        "origin": "retrieval",
    }


@pytest.mark.parametrize(
    ("answer", "available", "expected"),
    [
        ("LightRAG builds a graph [1]. GraphRAG does not [2][3].", 3, [1, 2, 3]),
        ("Both use graphs [2], and again [2] and [1].", 3, [2, 1]),
        # Numbers that are not sources are ignored: [9] does not exist, 2024 is a year.
        ("Published in [2024] according to [9] and [1].", 3, [1]),
        ("See [1, 3] and [ 2 ].", 3, [1, 3, 2]),
        ("The documents do not contain this.", 3, []),
        ("", 3, []),
        ("[1]", 0, []),
    ],
)
def test_citations_are_read_from_the_answer(
    answer: str, available: int, expected: list[int]
) -> None:
    assert cited_indexes(answer, available) == expected


# --- Summary questions: the prompt is built from stored summaries ---------------------


class WordCounter:
    def count(self, text: str) -> int:
        return len(text.split())


def stored(
    filename: str, level: str, ordinal: int, title: str | None, pages: tuple[int, int], text: str
) -> StoredSummary:
    return StoredSummary(
        document_id=uuid.uuid5(uuid.NAMESPACE_URL, filename),
        filename=filename,
        level=level,
        ordinal=ordinal,
        title=title,
        page_start=pages[0],
        page_end=pages[1],
        text=text,
        token_count=len(text.split()),
    )


PAPER = [
    stored("paper.pdf", "document", 0, None, (1, 16), "Overall: LightRAG; 67.6% (p. 8)."),
    stored("paper.pdf", "section", 1, "INTRODUCTION", (1, 2), "Intro summary."),
    stored("paper.pdf", "section", 2, "EVALUATION", (5, 10), "Eval summary 67.6% (p. 8)."),
]


def test_the_summary_prompt_numbers_the_summaries_with_their_pages_and_sections() -> None:
    prompt, used = build_summary_prompt(
        "summary this document.", PAPER, WordCounter(), evidence_budget=1_000
    )

    assert used == PAPER
    assert "[1] paper.pdf, pages 1-16, whole document\nOverall: LightRAG; 67.6% (p. 8)." in prompt
    assert "[2] paper.pdf, pages 1-2, section: INTRODUCTION\nIntro summary." in prompt
    assert "[3] paper.pdf, pages 5-10, section: EVALUATION\nEval summary 67.6% (p. 8)." in prompt
    assert prompt.index("[1]") < prompt.index("[2]") < prompt.index("[3]")
    assert "(p. 8)" in prompt  # the model is told to keep such page references
    assert "keep the page reference" in prompt
    assert prompt.endswith("Question: summary this document.\nAnswer:")
    # One document: no instruction about separating documents.
    assert "one separate part per document" not in prompt


def test_summaries_that_do_not_fit_are_left_out_whole_in_document_order() -> None:
    counter = WordCounter()
    # Budget for the document summary and the first section only.
    budget = sum(
        counter.count(block)
        for block in [
            "[1] paper.pdf, pages 1-16, whole document\nOverall: LightRAG; 67.6% (p. 8).",
            "[2] paper.pdf, pages 1-2, section: INTRODUCTION\nIntro summary.",
        ]
    )

    _, used = build_summary_prompt("summary", PAPER, counter, evidence_budget=budget)

    assert used == PAPER[:2]


def test_with_several_documents_each_gets_its_share_and_its_own_part() -> None:
    other = [
        stored("notes.md", "document", 0, None, (1, 1), "Overall: notes."),
        stored("notes.md", "section", 1, "Indexing", (1, 1), "Indexing summary."),
    ]
    counter = WordCounter()
    # Each document gets half. Half fits both summaries of the notes; for the paper it fits
    # the whole-document summary but not the first section as well.
    budget = 2 * sum(
        counter.count(block)
        for block in [
            "[2] notes.md, pages 1-1, whole document\nOverall: notes.",
            "[3] notes.md, pages 1-1, section: Indexing\nIndexing summary.",
        ]
    )

    prompt, used = build_summary_prompt("summary", PAPER + other, counter, evidence_budget=budget)

    assert [(s.filename, s.level) for s in used] == [
        ("paper.pdf", "document"),
        ("notes.md", "document"),
        ("notes.md", "section"),
    ]
    assert "sources come from 2 documents" in prompt
    assert "one separate part per document" in prompt


def test_a_summary_source_payload_carries_the_section_and_page_range() -> None:
    payload = summary_source_payload(2, PAPER[2])

    assert payload == {
        "index": 2,
        "kind": "summary",
        "document_id": str(PAPER[2].document_id),
        "filename": "paper.pdf",
        "page_start": 5,
        "page_end": 10,
        "section_title": "EVALUATION",
        "snippet": "Eval summary 67.6% (p. 8).",
        "score": None,
        "origin": "summary",
        "verification": None,
    }
    assert summary_source_payload(1, PAPER[0])["section_title"] is None


def test_the_summary_instructions_keep_the_scope_of_comparison_outcomes() -> None:
    """D63 applies to answers from summaries too: no "in all cases" without every case."""
    prompt, _ = build_summary_prompt("q", [], WordCounter(), evidence_budget=0)

    assert "go against the overall trend" in prompt
    assert '"in all cases"' in prompt
    assert "every case" in prompt


def test_the_summary_instructions_fit_their_budget(counter: Qwen3TokenCounter) -> None:
    prompt, _ = build_summary_prompt("summary this document.", [], counter, evidence_budget=0)
    assert counter.count(prompt) <= 500
