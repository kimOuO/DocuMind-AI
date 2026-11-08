"""Conversation memory for follow-up questions (AC-16).

The memory given to the rewrite call keeps the most recent turns verbatim and
reduces earlier ones to their questions, within 800 tokens. Answers that did
not complete are left out.
"""

from app.chat.memory import (
    MEMORY_TOKEN_BUDGET,
    HistoryMessage,
    build_memory,
    clean_rewrite,
    needs_rewrite,
    rewrite_prompt,
)
from app.llm.tokenizer import Qwen3TokenCounter


class WordCounter:
    def count(self, text: str) -> int:
        return len(text.split())


def exchange(question: str, answer: str, status: str = "completed") -> list[HistoryMessage]:
    return [
        HistoryMessage("user", question, "completed"),
        HistoryMessage("assistant", answer, status),
    ]


def test_recent_turns_are_kept_verbatim_oldest_first() -> None:
    history = exchange("What does LightRAG build?", "A graph of entities [1].") + exchange(
        "How is it retrieved?", "At two levels [2]."
    )

    memory = build_memory(history, WordCounter(), budget_tokens=100)

    assert memory == (
        "User: What does LightRAG build?\n"
        "Assistant: A graph of entities [1].\n"
        "User: How is it retrieved?\n"
        "Assistant: At two levels [2]."
    )


def test_earlier_turns_keep_only_their_questions_when_the_budget_is_tight() -> None:
    history = (
        exchange("First question here?", "A long first answer with many many words in it.")
        + exchange("Second question here?", "A long second answer with many many words in it.")
        + exchange("Third question here?", "Short third answer.")
    )
    # Room for the last turn whole (9 words) and the earlier questions (4+4), not their answers.
    memory = build_memory(history, WordCounter(), budget_tokens=18)

    assert memory == (
        "User: First question here?\n"
        "User: Second question here?\n"
        "User: Third question here?\n"
        "Assistant: Short third answer."
    )


def test_the_oldest_questions_are_dropped_when_even_they_do_not_fit() -> None:
    history = (
        exchange("Q1 one?", "A1.")
        + exchange("Q2 two?", "A2 is a long answer.")
        + exchange("Q3 three?", "A3.")
    )
    # 8 words: the last turn (5), then the second question (3); the first question no longer fits.
    memory = build_memory(history, WordCounter(), budget_tokens=8)

    assert memory == "User: Q2 two?\nUser: Q3 three?\nAssistant: A3."


def test_answers_that_did_not_complete_are_left_out() -> None:
    history = (
        exchange("What does LightRAG build?", "A graph [1].")
        + exchange("And GraphRAG?", "GraphRAG bui", status="interrupted")
        + exchange("Any cost figures?", "", status="failed")
    )

    memory = build_memory(history, WordCounter(), budget_tokens=100)

    assert memory == (
        "User: What does LightRAG build?\nAssistant: A graph [1].\n"
        "User: And GraphRAG?\nUser: Any cost figures?"
    )


def test_no_history_means_no_memory() -> None:
    assert build_memory([], WordCounter(), budget_tokens=100) == ""


def test_the_rewrite_prompt_holds_the_memory_and_the_question_and_fits_its_budget() -> None:
    counter = Qwen3TokenCounter()
    memory = "User: What does LightRAG build?\nAssistant: A graph of entities [1]."

    prompt = rewrite_prompt(memory, "那它的缺點呢？")

    assert memory in prompt
    assert prompt.endswith("Latest question: 那它的缺點呢？\nStandalone question:")
    assert "same language" in prompt
    assert "Do not answer" in prompt
    # Instructions alone stay small; memory (800) and the question (200) come on top.
    assert counter.count(rewrite_prompt("", "")) <= 300
    assert MEMORY_TOKEN_BUDGET == 800


def test_the_rewritten_question_is_cleaned_or_rejected() -> None:
    assert clean_rewrite('  "What are the drawbacks of LightRAG?"  \n') == (
        "What are the drawbacks of LightRAG?"
    )
    assert clean_rewrite("Standalone question: What is LightRAG?") == "What is LightRAG?"
    assert clean_rewrite("「LightRAG 的缺點是什麼？」") == "LightRAG 的缺點是什麼？"
    assert clean_rewrite("   ") is None
    assert clean_rewrite("First line?\nSecond line explaining.") is None  # not a single question


def test_only_a_question_that_leans_on_the_conversation_is_rewritten() -> None:
    """D96: the rewrite resolves references; a question without any is used as asked (the
    model padded "compare lightRAG with GraphRAG" with both definitions, 8 → 66 tokens)."""
    for question in [
        "那它的缺點呢？",
        "and its drawbacks?",
        "what about the ablated versions?",
        "那第二篇呢？",
        "Which one is cheaper?",
        "它們的差別在哪？",
        "為什麼會這樣？",
        "Can you give the numbers for that?",
        "the second one?",
        "缺點？",
        "drawbacks?",
        "And the costs?",
    ]:
        assert needs_rewrite(question), question
    for question in [
        "summary this document.",
        "compare lightRAG with GraphRAG",
        "Performance of ablated versions of LightRAG",
        "LightRAG 用哪四個評估面向比較回答品質？各是什麼意思？",
        "In the Legal dataset, what are the Diversity win rates of NaiveRAG versus LightRAG?",
        "GraphRAG 論文中，Podcast 與 News 資料集建出的圖各有多少節點與邊？",
        "How large (in tokens) are the corpora each paper evaluates on?",
        "如何在家烤酸種麵包？",
    ]:
        assert not needs_rewrite(question), question
