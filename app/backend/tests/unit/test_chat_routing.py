"""Which way a question goes: stored summaries, or retrieval.

A keyword rule decides (docs/02-specs/02-architecture.md, section 8, step 4);
when it cannot tell, the question goes to retrieval without an extra LLM call.
"""

import pytest

from app.chat.routing import question_type


@pytest.mark.parametrize(
    "question",
    [
        "summary this document.",
        "Summarize the paper",
        "Please summarise section 4 for me",
        "Give me a short summary",
        "What are the summaries of each chapter?",
        "請給我這篇論文的摘要",
        "總結一下這份文件",
        "概述 LightRAG 的方法",
    ],
)
def test_summary_questions_are_recognised(question: str) -> None:
    assert question_type(question) == "summary"


@pytest.mark.parametrize(
    "question",
    [
        "compare lightRAG with GraphRAG",
        "Performance of ablated versions of LightRAG",
        "What does LightRAG build?",
        "The case was dismissed summarily.",  # not the word 'summary'
        "LightRAG 跟 GraphRAG 有什麼差別",
        "",
    ],
)
def test_other_questions_go_to_retrieval(question: str) -> None:
    assert question_type(question) == "retrieval"
