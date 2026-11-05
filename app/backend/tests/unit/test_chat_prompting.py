"""Building the answer prompt within its budget, and reading citations back."""

import uuid

import pytest

from app.chat.prompting import (
    build_answer_prompt,
    cited_indexes,
    question_language,
    source_payload,
)
from app.llm.tokenizer import Qwen3TokenCounter
from app.retrieval.repository import RetrievedChunk


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
