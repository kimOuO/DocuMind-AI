"""The Navigator/Analyst experiment (D71): the parts without a model or a database.

Two experimental answer modes exist beside the default single call:

- "roles": one call whose prompt asks the model to act first as a Navigator (name the
  places of the document that bear on the question, from a document map) and then as
  an Analyst (answer only from the sources). The evidence is the same as in the
  default mode.
- "navigate": a first call produces a reading plan from the document map; the plan is
  read back here, every item checked against the map, chunks of the located places
  fetched and appended behind the original Top-K within the evidence budget; a second
  call answers from the merged sources.

The document map is built from what the system already stores: the section summaries
(titles and page ranges) and the caption lines of tables and figures found in the
chunks. Nothing here knows any paper in particular; a plan item that names something
not on the map is kept as "not located" and never becomes evidence.
"""

import re
import uuid
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

from app.chat.prompting import LANGUAGE_RULES, question_language
from app.llm.tokenizer import TokenCounter
from app.retrieval.repository import RetrievedChunk
from app.summarization.repository import StoredSummary

NAVIGATION_MAX_OUTPUT_TOKENS = 400
NAVIGATION_MIN_OUTPUT_TOKENS = 200
_CAPTION = re.compile(r"^\s*((?:Table|Figure|Fig\.)\s*(\d+))\s*[.:]\s*(.*)$", re.IGNORECASE)
_PLAN_LINE = re.compile(r"^\s*(?:[-*•]|\d+[.)])\s*(.+?)\s*$")
_TABLE_REF = re.compile(r"\b(?:table|tab\.)\s*(\d+)\b", re.IGNORECASE)
_FIGURE_REF = re.compile(r"\b(?:figure|fig\.)\s*(\d+)\b", re.IGNORECASE)
_PAGE_REF = re.compile(r"\b(?:pages?|pp?\.)\s*(\d+)(?:\s*[-–]\s*(\d+))?", re.IGNORECASE)
_SECTION_NUMBER = re.compile(r"\b(?:section|sec\.|§)?\s*(\d+(?:\.\d+)*)\b", re.IGNORECASE)
_WORD = re.compile(r"[A-Za-z][A-Za-z-]{2,}")
_STOP = frozenset(
    [
        "the",
        "and",
        "for",
        "with",
        "from",
        "that",
        "this",
        "section",
        "sections",
        "paragraph",
        "paragraphs",
        "part",
        "text",
        "page",
        "pages",
        "table",
        "tables",
        "figure",
        "figures",
    ]
)

Caption = tuple[uuid.UUID, str, int, str]  # document id, filename, page, caption line


@dataclass(frozen=True)
class MapEntry:
    kind: str  # "section" | "table" | "figure"
    label: str  # the section title, or "Table 2" / "Figure 2"
    document_id: uuid.UUID
    filename: str
    page_start: int
    page_end: int
    caption: str = ""  # tables and figures: the caption without its label

    @property
    def pages(self) -> list[int]:
        return list(range(self.page_start, self.page_end + 1))


def build_map(summaries: Sequence[StoredSummary], captions: Sequence[Caption]) -> list[MapEntry]:
    """Sections (from the stored section summaries) and the tables and figures (from
    caption lines in the chunks), in page order."""
    entries: list[MapEntry] = []
    for s in summaries:
        if s.level != "section" or not s.title:
            continue
        entries.append(
            MapEntry("section", s.title, s.document_id, s.filename, s.page_start, s.page_end)
        )
    seen: set[tuple[uuid.UUID, str]] = set()
    for document_id, filename, page, line in captions:
        match = _CAPTION.match(line)
        if match is None:
            continue
        kind = "figure" if match.group(1).lower().startswith("f") else "table"
        label = f"{'Figure' if kind == 'figure' else 'Table'} {match.group(2)}"
        if (document_id, label) in seen:
            continue
        seen.add((document_id, label))
        entries.append(
            MapEntry(
                kind,
                label,
                document_id,
                filename,
                page,
                page,
                " ".join(match.group(3).split())[:100],
            )
        )
    return sorted(entries, key=lambda e: (e.page_start, e.kind != "section", e.label))


def map_text(entries: Sequence[MapEntry]) -> str:
    lines = []
    for e in entries:
        pages = (
            f"page {e.page_start}"
            if e.page_start == e.page_end
            else f"pages {e.page_start}-{e.page_end}"
        )
        if e.kind == "section":
            lines.append(f"- Section: {e.label} ({pages})")
        else:
            lines.append(f"- {e.label} ({pages}): {e.caption}")
    return "\n".join(lines)


@dataclass(frozen=True)
class PlanItem:
    text: str
    entry: MapEntry | None  # the map entry this item names, if any
    pages: list[int]  # the pages to fetch; empty when nothing could be located

    @property
    def located(self) -> bool:
        return bool(self.pages)


def _title_words(title: str) -> set[str]:
    return {w.lower() for w in _WORD.findall(title) if w.lower() not in _STOP}


def parse_plan(text: str, entries: Sequence[MapEntry]) -> list[PlanItem]:
    """The Navigator's lines, each located on the map (table/figure number, section
    number or title words, or an explicit page within the document) or not."""
    last_page = max((e.page_end for e in entries), default=0)
    items: list[PlanItem] = []
    for raw in text.splitlines():
        match = _PLAN_LINE.match(raw)
        if match is None:
            continue
        line = match.group(1)
        entry = _locate(line, entries)
        if entry is not None:
            items.append(PlanItem(line, entry, entry.pages))
            continue
        pages: list[int] = []
        page_ref = _PAGE_REF.search(line)
        if page_ref:
            first = int(page_ref.group(1))
            last = int(page_ref.group(2) or first)
            if 1 <= first <= last <= last_page:
                pages = list(range(first, last + 1))
        items.append(PlanItem(line, None, pages))
    return items


def _locate(line: str, entries: Sequence[MapEntry]) -> MapEntry | None:
    table = _TABLE_REF.search(line)
    if table:
        return next(
            (e for e in entries if e.kind == "table" and e.label == f"Table {table.group(1)}"), None
        )
    figure = _FIGURE_REF.search(line)
    if figure:
        return next(
            (e for e in entries if e.kind == "figure" and e.label == f"Figure {figure.group(1)}"),
            None,
        )
    sections = [e for e in entries if e.kind == "section"]
    for number in _SECTION_NUMBER.findall(line):
        if "." in number:
            hit = next(
                (e for e in sections if e.label.startswith(number + " ") or e.label == number), None
            )
            if hit:
                return hit
    words = _title_words(line)
    best: tuple[int, MapEntry] | None = None
    for e in sections:
        title = _title_words(e.label)
        shared = len(words & title)
        # Enough of the title: two of its content words, or all of it when it has fewer.
        if 0 < shared >= min(2, len(title)) and (best is None or shared > best[0]):
            best = (shared, e)
    return best[1] if best else None


def merge_evidence(
    base: Sequence[RetrievedChunk],
    fetched: Sequence[tuple[PlanItem, Sequence[RetrievedChunk]]],
    counter: TokenCounter,
    *,
    budget: int,
) -> tuple[list[RetrievedChunk], list[dict[str, Any]]]:
    """The original Top-K whole, then the plan's chunks in plan order while the budget
    lasts; a log says what became of every chunk."""
    used: list[RetrievedChunk] = list(base)
    log: list[dict[str, Any]] = [
        {"ordinal": c.ordinal, "page": c.page, "kept": True, "reason": c.origin} for c in base
    ]
    spent = sum(c.token_count for c in base)
    present = {c.chunk_id for c in base}
    for item, chunks in fetched:
        for c in chunks:
            if c.chunk_id in present:
                log.append(
                    {
                        "ordinal": c.ordinal,
                        "page": c.page,
                        "kept": False,
                        "reason": "already among the retrieved sources",
                    }
                )
                continue
            cost = c.token_count
            if spent + cost > budget:
                log.append(
                    {
                        "ordinal": c.ordinal,
                        "page": c.page,
                        "kept": False,
                        "reason": "over the evidence budget",
                    }
                )
                continue
            used.append(
                RetrievedChunk(
                    c.chunk_id,
                    c.document_id,
                    c.filename,
                    c.page,
                    c.ordinal,
                    c.text,
                    c.token_count,
                    None,
                    "navigation",
                )
            )
            present.add(c.chunk_id)
            spent += cost
            log.append(
                {"ordinal": c.ordinal, "page": c.page, "kept": True, "reason": f"plan: {item.text}"}
            )
    return used, log


NAVIGATION_INSTRUCTIONS = """\
You are the Navigator for a question about the user's documents. Your job is to say where in \
the documents the evidence is, not what it says.

Rules:
- Use the document map below and the sources already retrieved. List the sections, tables, \
figures or pages that the answer needs. Prefer not to miss evidence; the list is short, \
at most six items.
- One item per line, starting with "- ", naming the place as the map names it (for example \
"Table 2 (page 8)" or "Section: EVALUATION") and in a few words why it is needed.
- Do not answer the question. Do not state any fact, number or conclusion from the documents.
{language_rule}

Document map:
{map}

Sources already retrieved (headers only):
{headers}

Question: {question}

Reading plan:"""


def build_navigation_prompt(
    question: str,
    entries: Sequence[MapEntry],
    source_headers: Sequence[str],
    counter: TokenCounter,
    limit: int,
) -> tuple[str, int]:
    prompt = NAVIGATION_INSTRUCTIONS.format(
        language_rule=LANGUAGE_RULES[question_language(question)],
        map=map_text(entries) or "- (no map available)",
        headers="\n".join(source_headers) or "(none)",
        question=question,
    )
    room = limit - counter.count(prompt)
    return prompt, max(NAVIGATION_MIN_OUTPUT_TOKENS, min(NAVIGATION_MAX_OUTPUT_TOKENS, room))


ROLES_PREAMBLE = """\
Work in two roles, in this order, and label each part.

Navigator: from the document map below, name the sections, tables, figures or pages that \
bear on the question, in a few lines. These are candidates, not facts: do not state any \
fact, number or conclusion here.

Analyst: then answer the question following the rules below, using only the numbered \
sources. The Navigator's list is not evidence; if a place it names is not among the \
sources, say that it was not available rather than guessing its content.

Document map:
{map}

"""


def roles_preamble(entries: Sequence[MapEntry]) -> str:
    return ROLES_PREAMBLE.format(map=map_text(entries) or "- (no map available)")


def analyst_preamble(items: Sequence[PlanItem]) -> str:
    """For the second call of the navigate mode: what the Navigator proposed, marked as such."""
    lines = [f"- {i.text}" + ("" if i.located else " (not found in the document)") for i in items]
    return (
        "A Navigator proposed where to look (candidates, not verified):\n"
        + ("\n".join(lines) or "- (nothing)")
        + "\nAnswer only from the numbered sources below; do not assume those places are right.\n\n"
    )
