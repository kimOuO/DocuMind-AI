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


@pytest.mark.parametrize(
    "question",
    [
        # D72: a question *about* summaries in the paper is a content question, not a
        # request to summarise the document.
        "How many community summaries are there at each level of the graph?",
        "What summarization method does GraphRAG use for its community reports?",
        "How many context units and tokens do the root-level community summaries (C0) and the "
        "source-text summarization (TS) use on the Podcast and News datasets?",
        "Does LightRAG rely on map-reduce summarization of the source texts?",
        "Which condition had the highest number of summaries?",
        "論文中的摘要方法是什麼？",
        "社群摘要有幾層？",
        "GraphRAG 的摘要樹用了多少 token？",
    ],
)
def test_questions_about_summaries_in_the_text_go_to_retrieval(question: str) -> None:
    assert question_type(question) == "retrieval"


@pytest.mark.parametrize(
    "question",
    [
        "Summarize this paper's results section.",
        "Can you give me a summary of the whole document?",
        "摘要",
        "請幫我總結這篇",
    ],
)
def test_requests_to_summarise_the_document_still_go_to_summaries(question: str) -> None:
    assert question_type(question) == "summary"
