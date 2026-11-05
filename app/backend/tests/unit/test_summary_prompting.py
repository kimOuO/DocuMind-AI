"""The prompts that build section and document summaries."""

from app.llm.tokenizer import Qwen3TokenCounter
from app.summarization.prompting import (
    DOCUMENT_SUMMARY_WORDS,
    SECTION_INPUT_BUDGET,
    SECTION_SUMMARY_WORDS,
    SUMMARY_MAX_OUTPUT_TOKENS,
    PageText,
    document_prompt,
    group_within_budget,
    merge_prompt,
    section_prompt,
)


class WordTokenizer:
    def count(self, text: str) -> int:
        return len(text.split())


def test_a_section_prompt_marks_every_page_and_asks_for_page_tags_on_numbers() -> None:
    prompt = section_prompt(
        "paper.pdf",
        "ABLATION STUDIES (RQ2)",
        [PageText(7, "We also conduct ablation studies."), PageText(8, "Table 2: 67.6%")],
    )

    assert "Section: ABLATION STUDIES (RQ2)" in prompt
    assert "Pages: 7-8" in prompt
    assert "[page 7]\nWe also conduct ablation studies." in prompt
    assert "[page 8]\nTable 2: 67.6%" in prompt
    assert prompt.index("[page 7]") < prompt.index("[page 8]")
    assert '"67.6% (p. 8)"' in prompt  # the example of the required tag
    assert f"at most {SECTION_SUMMARY_WORDS} words" in prompt
    assert "same language as the section" in prompt
    assert prompt.endswith("Summary:")


def test_a_single_page_section_shows_one_page() -> None:
    assert "Pages: 3\n" in section_prompt("a.pdf", "T", [PageText(3, "x")])


def test_the_document_prompt_lists_the_section_summaries_in_order() -> None:
    prompt = document_prompt(
        "paper.pdf", [("INTRODUCTION", "Intro summary."), ("EVALUATION", "Eval summary.")]
    )

    assert "[INTRODUCTION]\nIntro summary." in prompt
    assert "[EVALUATION]\nEval summary." in prompt
    assert prompt.index("INTRODUCTION") < prompt.index("EVALUATION")
    assert "the problem the document addresses" in prompt
    assert f"at most {DOCUMENT_SUMMARY_WORDS} words" in prompt
    assert "Do not invent numbers or pages" in prompt
    assert prompt.endswith("Overall summary:")


def test_the_merge_prompt_keeps_page_references() -> None:
    prompt = merge_prompt("paper.pdf", [("A", "x (p. 1)"), ("B", "y (p. 2)")])

    assert "Keep every specific number with its page reference" in prompt
    assert prompt.endswith("Condensed summary:")


def test_summaries_are_grouped_within_the_budget_in_order() -> None:
    items = [
        (f"S{i}", "word " * 40) for i in range(5)
    ]  # 40 words of text each, plus the title line

    groups = group_within_budget(items, WordTokenizer(), budget=100)

    assert [[title for title, _ in group] for group in groups] == [
        ["S0", "S1"],
        ["S2", "S3"],
        ["S4"],
    ]


def test_a_single_summary_over_the_budget_is_still_its_own_group() -> None:
    groups = group_within_budget(
        [("Big", "word " * 500), ("Small", "x")], WordTokenizer(), budget=100
    )

    assert [[title for title, _ in group] for group in groups] == [["Big"], ["Small"]]


def test_the_budgets_leave_room_for_the_instructions_within_the_context_limit() -> None:
    counter = Qwen3TokenCounter()
    instructions = section_prompt("x.pdf", "T", [PageText(1, "")])

    # Input budget + instructions + output stays well under 10,000.
    assert counter.count(instructions) < 500
    assert SECTION_INPUT_BUDGET + 500 + SUMMARY_MAX_OUTPUT_TOKENS <= 8_000
