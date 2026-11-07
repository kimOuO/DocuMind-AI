"""Prompts for building summaries at ingestion time, and the merge plan.

Every summary call fits the budget of one LLM call (docs/02-specs/02-architecture.md,
section 7): about 6,000 tokens of input, 500 of instructions, 1,500 of output.
Section summaries tag every specific number with the page it comes from, so
that an answer built from them can be traced back to the document (AC-26).
"""

from collections.abc import Sequence
from dataclasses import dataclass

from app.llm.tokenizer import TokenCounter

SECTION_INPUT_BUDGET = 6_000
SUMMARY_MAX_OUTPUT_TOKENS = 1_500
SECTION_SUMMARY_WORDS = 250
DOCUMENT_SUMMARY_WORDS = 400

SECTION_INSTRUCTIONS = """\
You summarise one section of a document for later question answering.

Rules:
- Write a faithful summary of the section below in at most {words} words, in the same \
language as the section.
- Keep every specific number, name and result that the section reports: percentages, \
counts, token figures, dataset names, method names, comparison outcomes.
- Keep the scope of every comparison outcome as the section states it. If some results go \
against the overall trend, keep them; do not write "in all cases" or "across all datasets" \
unless the section shows it for every case.
- Immediately after every specific number, write the page it appears on in \
parentheses, like "67.6% (p. 8)". The page is given in the "page" markers below.
- Do not add anything that is not in the section. Do not evaluate or praise it.
- Plain text, no headings, no bullet points.

Document: {filename}
Section: {title}
Pages: {pages}

"""

DOCUMENT_INSTRUCTIONS = """\
You write the overall summary of a document from the summaries of its sections.

Rules:
- Write at most {words} words, in the same language as the section summaries.
- Cover, in this order: the problem the document addresses, what it proposes or \
describes, and its main results or conclusions.
- State the main results with their specific numbers, taken from the section summaries, \
and keep the page reference that follows each number exactly as written, like \
"67.6% (p. 8)". Do not invent numbers or pages.
- Keep the scope of every comparison outcome as the section summaries state it. If some \
results go against the overall trend, keep them; do not write "in all cases" or "across all \
datasets" unless the summaries show it for every case.
- Do not add anything that is not in the section summaries. Do not evaluate or praise.
- Plain text, no headings, no bullet points.

Document: {filename}

Section summaries:
"""

MERGE_INSTRUCTIONS = """\
You condense several section summaries of one document into one shorter summary.

Rules:
- Write at most {words} words, in the same language as the input.
- Keep every specific number with its page reference, like "67.6% (p. 8)".
- Do not add anything that is not in the input.
- Plain text, no headings, no bullet points.

Document: {filename}

Section summaries:
"""


@dataclass(frozen=True)
class PageText:
    page: int
    text: str


def section_prompt(filename: str, title: str, pages: Sequence[PageText]) -> str:
    """The prompt for one section. Each page's text is preceded by a page marker."""
    page_range = (
        f"{pages[0].page}"
        if pages[0].page == pages[-1].page
        else f"{pages[0].page}-{pages[-1].page}"
    )
    body = "\n\n".join(f"[page {p.page}]\n{p.text}" for p in pages)
    return (
        SECTION_INSTRUCTIONS.format(
            words=SECTION_SUMMARY_WORDS, filename=filename, title=title, pages=page_range
        )
        + body
        + "\n\nSummary:"
    )


def _numbered(summaries: Sequence[tuple[str, str]]) -> str:
    return "\n\n".join(f"[{title}]\n{text}" for title, text in summaries)


def document_prompt(filename: str, summaries: Sequence[tuple[str, str]]) -> str:
    return (
        DOCUMENT_INSTRUCTIONS.format(words=DOCUMENT_SUMMARY_WORDS, filename=filename)
        + _numbered(summaries)
        + "\n\nOverall summary:"
    )


def merge_prompt(filename: str, summaries: Sequence[tuple[str, str]]) -> str:
    return (
        MERGE_INSTRUCTIONS.format(words=SECTION_SUMMARY_WORDS * 2, filename=filename)
        + _numbered(summaries)
        + "\n\nCondensed summary:"
    )


def group_within_budget(
    summaries: Sequence[tuple[str, str]], counter: TokenCounter, budget: int
) -> list[list[tuple[str, str]]]:
    """Consecutive groups of (title, text) whose texts together stay within the budget.

    Used when the section summaries are too many to merge in one call: each
    group is condensed first, and the condensed texts are merged in turn.
    """
    groups: list[list[tuple[str, str]]] = []
    current: list[tuple[str, str]] = []
    spent = 0
    for item in summaries:
        cost = counter.count(_numbered([item]))
        if current and spent + cost > budget:
            groups.append(current)
            current, spent = [], 0
        current.append(item)
        spent += cost
    if current:
        groups.append(current)
    return groups


REPAIR_INSTRUCTIONS = """\
You wrote the summary below of a section of a document. A program checked every figure in it \
against the tables on the section's pages and found the contradictions listed after it, each \
with the table's own figures. Rewrite ONLY the sentences listed, so that every figure is \
attributed exactly as the table gives it — the right method, dataset, metric and comparison — \
or is left out; keep every other sentence word for word; do not add any figure that is not in \
the table excerpts; keep the page markers like "(p. 8)". Return the whole corrected summary \
as plain text.

Document: {filename}
Section: {title}

Summary as written:
{summary}

Contradictions found by the program:
{evidence}

Table excerpts (as the program reads them; each pair is as the table pairs it):
{excerpts}

Corrected summary:"""


def repair_prompt(
    filename: str, title: str, summary: str, evidence: Sequence[str], excerpts: str
) -> str:
    """One rewrite of a summary whose figures contradict its tables (D87 experiment B)."""
    return REPAIR_INSTRUCTIONS.format(
        filename=filename,
        title=title,
        summary=summary,
        evidence="\n".join(f"- {line}" for line in evidence) or "- (none)",
        excerpts=excerpts or "(none)",
    )
