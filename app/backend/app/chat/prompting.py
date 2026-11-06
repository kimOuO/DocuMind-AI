"""The prompts for answering a question, and the citations read back from an answer.

The model is told to answer only from the numbered sources and to cite them
by number. Sources are added in order while they fit the evidence budget; one
that does not fit is left out whole, never cut short. Ordinary questions get
retrieved chunks as sources; summary questions get the stored summaries.
"""

import re
from collections.abc import Sequence
from typing import Any

from app.ingestion.tables import is_table_chunk
from app.llm.tokenizer import TokenCounter
from app.retrieval.repository import RetrievedChunk
from app.summarization.repository import StoredSummary

INSTRUCTIONS = """\
You answer questions about the user's documents.

Rules:
- Use only the numbered sources below. Do not use any other knowledge.
- After each statement, cite the source whose text states that statement, by its number in \
square brackets, for example [1] or [2][3]. A source about the same topic is not enough: a \
figure is cited to the source where the figure appears, an explanation to the source where the \
explanation appears, and two neighbouring statements may need different sources.
- Copy numbers and names exactly as they appear in the sources.
- When the question asks to compare or analyse experimental results, write in this order: \
the main findings; representative figures that support them; the results that go against the \
trend, named explicitly; then a conclusion that is no stronger than the figures you gave. Do \
not list every number a source has unless the question asks for the full table. Every figure \
keeps its labels: which method or variant, which dataset, which metric, its unit, and what it \
is compared against. If you named an exception, the conclusion must carry it too; never write \
"all", "every" or "consistently" about cases you have not checked one by one.
- If the sources do not contain the answer, say that the documents do not contain it and \
cite nothing.
{language_rule}

Sources:
"""

# Qwen answers Chinese questions in Simplified Chinese unless told otherwise;
# this platform's users write Traditional Chinese.
LANGUAGE_RULES = {
    "zh": "- The question is in Chinese: answer in Traditional Chinese (繁體中文，台灣用語), "
    "never in Simplified Chinese.",
    "other": "- Answer in the language of the question.",
}

_CJK = re.compile(r"[\u4e00-\u9fff\u3400-\u4dbf]")


def question_language(question: str) -> str:
    """'zh' when the question contains Chinese characters, otherwise 'other'."""
    return "zh" if _CJK.search(question) else "other"


_CITATION = re.compile(r"\[\s*(\d{1,3}(?:\s*,\s*\d{1,3})*)\s*\]")


def _source_block(index: int, chunk: RetrievedChunk) -> str:
    where = f"{chunk.filename}, page {chunk.page}"
    if chunk.origin == "table_context":
        where += " (the text that follows the table above)"
    elif is_table_chunk(chunk.text):
        where += " (a table)"
    return f"[{index}] {where}\n{chunk.text}"


def build_answer_prompt(
    question: str,
    chunks: list[RetrievedChunk],
    counter: TokenCounter,
    evidence_budget: int,
    *,
    preamble: str = "",
) -> tuple[str, list[RetrievedChunk]]:
    """The prompt, and the chunks that were included in it (numbered from 1 in that order).

    A preamble (D71: the two-role instructions, or the Navigator's plan) goes before
    the instructions; the default prompt has none."""
    used: list[RetrievedChunk] = []
    blocks: list[str] = []
    spent = 0
    for chunk in chunks:
        block = _source_block(len(used) + 1, chunk)
        cost = counter.count(block)
        if spent + cost > evidence_budget:
            # Stop at the first that does not fit, so the numbering stays in rank order.
            break
        used.append(chunk)
        blocks.append(block)
        spent += cost
    sources = "\n\n".join(blocks) if blocks else "(no sources)"
    instructions = INSTRUCTIONS.format(language_rule=LANGUAGE_RULES[question_language(question)])
    return f"{preamble}{instructions}{sources}\n\nQuestion: {question}\nAnswer:", used


def source_payload(index: int, chunk: RetrievedChunk) -> dict[str, Any]:
    """A source as it is sent to the client and stored with the answer."""
    return {
        "index": index,
        "kind": "chunk",
        "document_id": str(chunk.document_id),
        "filename": chunk.filename,
        "page_start": chunk.page,
        "page_end": chunk.page,
        "section_title": None,
        # The chunk as stored: it can be found verbatim on that page of the document.
        "snippet": chunk.text,
        "score": None if chunk.score is None else round(chunk.score, 4),
        "origin": chunk.origin,
    }


def cited_indexes(answer: str, available: int) -> list[int]:
    """Source numbers cited in the answer, in order of first appearance.

    Only numbers of sources that were actually given count; anything else in
    square brackets is ignored.
    """
    cited: list[int] = []
    for match in _CITATION.finditer(answer):
        for number in match.group(1).split(","):
            index = int(number)
            if 1 <= index <= available and index not in cited:
                cited.append(index)
    return cited


# --- Summary questions ----------------------------------------------------------------

SUMMARY_INSTRUCTIONS = """\
You answer questions about the user's documents from the summaries below. Each summary \
covers a whole document or one of its sections.

Rules:
- Use only the numbered sources below. Do not use any other knowledge.
- After each statement, cite the sources it comes from by their numbers in square brackets, \
for example [1] or [2][3].
- Copy numbers and names exactly as they appear, and keep the page reference that follows \
a number, for example "67.6% (p. 8)".
- When asked for a summary of a document, cover the problem it addresses, what it proposes \
or does, and its main results, as far as the sources say so.
- Keep the scope of every comparison outcome as the sources state it. If some results go \
against the overall trend, say so explicitly; do not claim "in all cases" or "outperforms \
everywhere" unless the sources show it for every case.
- If the sources do not contain what the question asks, say so and cite nothing.
{documents_rule}{language_rule}

Sources:
"""

DOCUMENTS_RULE = (
    "- The sources come from {count} documents. Write one separate part per document, headed "
    "by its file name, and never mix the content of different documents.\n"
)


def _summary_block(index: int, summary: StoredSummary) -> str:
    where = "whole document" if summary.level == "document" else f"section: {summary.title}"
    pages = f"pages {summary.page_start}-{summary.page_end}"
    # B5 baseline (2026-11-07, user's decision): the D76 verification note is not shown to
    # the model; the status is still stored and reported. To restore: append
    # _verification_note(summary.verification) after {where}.
    return f"[{index}] {summary.filename}, {pages}, {where}\n{summary.text}"


def _verification_note(verification: dict[str, Any] | None) -> str:
    """D76: what the summary's own check found, told to the model so that a contradicted
    figure is not repeated and an unverified one is not presented as certain."""
    if not verification:
        return ""
    status = verification.get("status")
    if status == "CONTRADICTED":
        figures = ", ".join(verification.get("contradicted", []))
        return (
            f"\nVerification: the figures {figures} in this summary contradict the source "
            "tables; do not repeat them, and prefer a source that holds the table itself."
        )
    if status == "UNCERTAIN":
        figures = ", ".join(
            [*verification.get("unverified", []), *verification.get("unresolved", [])]
        )
        return (
            f"\nVerification: the figures {figures} could not be confirmed in the source "
            "pages; do not present them as certain."
        )
    return ""


def build_summary_prompt(
    question: str,
    summaries: list[StoredSummary],
    counter: TokenCounter,
    *,
    evidence_budget: int,
    preamble: str = "",
    extra_chunks: Sequence[RetrievedChunk] = (),
) -> tuple[str, list[StoredSummary | RetrievedChunk]]:
    """The prompt, and the sources included in it (numbered from 1 in that order).

    The budget is shared equally between the documents, so that with several
    documents each one gets its part (D32). Within a document the whole-document
    summary comes first, then the sections in order; the first that does not
    fit ends that document's share. Extra chunks (D71: what a reading plan fetched)
    come after every summary, while the whole budget lasts; a preamble goes first.
    """
    documents = list(dict.fromkeys(s.document_id for s in summaries))
    share = evidence_budget // len(documents) if documents else evidence_budget
    used: list[StoredSummary | RetrievedChunk] = []
    blocks: list[str] = []
    total = 0
    for document_id in documents:
        spent = 0
        for summary in (s for s in summaries if s.document_id == document_id):
            block = _summary_block(len(used) + 1, summary)
            cost = counter.count(block)
            if spent + cost > share:
                break
            used.append(summary)
            blocks.append(block)
            spent += cost
            total += cost
    for chunk in extra_chunks:
        block = _source_block(len(used) + 1, chunk)
        cost = counter.count(block)
        if total + cost > evidence_budget:
            break
        used.append(chunk)
        blocks.append(block)
        total += cost
    sources = "\n\n".join(blocks) if blocks else "(no sources)"
    documents_rule = DOCUMENTS_RULE.format(count=len(documents)) if len(documents) > 1 else ""
    instructions = SUMMARY_INSTRUCTIONS.format(
        documents_rule=documents_rule,
        language_rule=LANGUAGE_RULES[question_language(question)],
    )
    return f"{preamble}{instructions}{sources}\n\nQuestion: {question}\nAnswer:", used


def summary_source_payload(index: int, summary: StoredSummary) -> dict[str, Any]:
    """A summary as a source: file name, section title and page range (AC-26)."""
    return {
        "index": index,
        "kind": "summary",
        "document_id": str(summary.document_id),
        "filename": summary.filename,
        "page_start": summary.page_start,
        "page_end": summary.page_end,
        "section_title": summary.title,
        "snippet": summary.text,
        "score": None,
        "origin": "summary",
        "verification": summary.verification,
    }
