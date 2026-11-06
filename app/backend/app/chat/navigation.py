"""The Navigator/Analyst experiment (D71, reworked in D73): the parts without a model or
a database.

Two experimental answer modes exist beside the default single call:

- "roles": one call whose prompt asks the model to act first as a Navigator (name the
  places of the document that bear on the question, from a document map) and then as
  an Analyst (answer only from the sources). The evidence is the same as in the
  default mode.
- "navigate": a first call produces a list of targets — where to look and what is
  needed there — from the document map and the retrieved sources; every target is
  located on the map, its candidate chunks are ranked by similarity to the question and
  to the need within the located range (tables and figures are taken by structure),
  and the targets take turns at the remaining evidence budget behind the original
  Top-K — a required target the retrieved sources already cover fetches nothing, and
  supplementary targets get at most two chunks in all (D74); a second call answers from
  the merged sources.

The document map is built from what the system already stores: the heading lines
found in the chunks (sections and subsections with their chunk ranges), the section
summaries as a fallback (page ranges only), and the caption lines of tables and
figures. Nothing here knows any paper in particular; a target that names something
not on the map is kept as "not located" and never becomes evidence.
"""

import json
import re
import uuid
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any

from app.chat.prompting import LANGUAGE_RULES, question_language
from app.ingestion.headings import normalize_title
from app.ingestion.tables import is_table_chunk
from app.llm.tokenizer import TokenCounter
from app.retrieval.repository import RetrievedChunk
from app.summarization.repository import StoredSummary

NAVIGATION_MAX_OUTPUT_TOKENS = 400
NAVIGATION_MIN_OUTPUT_TOKENS = 200
CHUNKS_PER_TARGET = 3  # D73: at most this many chunks per target
SUPPLEMENTARY_CAP = 2  # D74: at most this many supplementary chunks for the whole question
OVERLAP_MAX = (
    0.5  # D74: a supplementary chunk sharing this share of words with one selected repeats it
)
# D74: how far the retrieved sources already cover a target, judged by structure.
COVERED, PARTIAL, MISSING, UNKNOWN, NOT_LOCATED = (
    "covered",
    "partial",
    "missing",
    "unknown",
    "not_located",
)
_CONTENT_WORD = re.compile(r"[A-Za-z][A-Za-z-]{3,}")
_CAPTION = re.compile(r"^\s*((?:Table|Figure|Fig\.)\s*(\d+))\s*[.:]\s*(.*)$", re.IGNORECASE)
_NUMBERED_HEADING = re.compile(r"^(?P<number>\d{1,2}(?:\.\d{1,2})*)\s+(?P<title>\S.*)$")
_PLAN_LINE = re.compile(r"^\s*(?:[-*•]|\d+[.)])\s*(.+?)\s*$")
_FIELD = re.compile(
    r"^\s*(location|place|need|priority|status|reason|why)\s*[:：]\s*(.*)$", re.IGNORECASE
)
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
PRIORITIES = ("required", "supplementary")
STATUSES = ("covered", "missing")

Caption = tuple[uuid.UUID, str, int, int, str]  # document id, filename, page, ordinal, line
# document id, filename, page, chunk ordinal, line index within the chunk, heading line
HeadingLine = tuple[uuid.UUID, str, int, int, int, str]
ChunkPage = tuple[uuid.UUID, int, int]  # document id, chunk ordinal, page


@dataclass(frozen=True)
class MapEntry:
    kind: str  # "section" | "table" | "figure"
    label: str  # "4.3 ABLATION STUDIES", the summary's title, or "Table 2" / "Figure 2"
    document_id: uuid.UUID
    filename: str
    page_start: int
    page_end: int
    caption: str = ""  # tables and figures: the caption without its label
    number: str | None = None  # sections found by heading: "4.3"
    level: int = 0  # 1 for a section, 2 for a subsection; 0 when unknown (summaries)
    parent: str | None = None  # label of the enclosing section
    # The chunks of the place, inclusive; None when only the pages are known.
    ordinal_start: int | None = None
    ordinal_end: int | None = None

    @property
    def pages(self) -> list[int]:
        return list(range(self.page_start, self.page_end + 1))


def build_map(
    summaries: Sequence[StoredSummary],
    captions: Sequence[Caption],
    headings: Sequence[HeadingLine] = (),
    chunk_pages: Sequence[ChunkPage] = (),
) -> list[MapEntry]:
    """Sections and subsections (from the heading lines of the chunks; the section
    summaries for a document without recognised headings), and the tables and figures
    (from caption lines), in page order."""
    entries: list[MapEntry] = []
    pages: dict[tuple[uuid.UUID, int], int] = {(d, o): p for d, o, p in chunk_pages}
    last: dict[uuid.UUID, int] = {}
    for d, o, _ in chunk_pages:
        last[d] = max(last.get(d, o), o)
    by_document: dict[uuid.UUID, list[HeadingLine]] = {}
    for h in headings:
        by_document.setdefault(h[0], []).append(h)
    for document_id, lines in by_document.items():
        entries.extend(_sections_from_headings(document_id, lines, pages, last.get(document_id)))
    for s in summaries:
        if s.level != "section" or not s.title or s.document_id in by_document:
            continue
        entries.append(
            MapEntry("section", s.title, s.document_id, s.filename, s.page_start, s.page_end)
        )
    seen: set[tuple[uuid.UUID, str]] = set()
    for document_id, filename, page, ordinal, line in captions:
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
                ordinal_start=ordinal,
                ordinal_end=ordinal,
            )
        )
    return sorted(
        entries,
        key=lambda e: (
            e.page_start,
            e.kind != "section",
            e.ordinal_start if e.ordinal_start is not None else -1,
            e.level,
            e.label,
        ),
    )


def _sections_from_headings(
    document_id: uuid.UUID,
    lines: Sequence[HeadingLine],
    pages: Mapping[tuple[uuid.UUID, int], int],
    last_ordinal: int | None,
) -> list[MapEntry]:
    """Each heading opens a section that runs to the next heading of its level or above.
    A chunk whose first line is that next heading is not shared; a chunk with the
    heading further inside it belongs to both sections."""
    ordered = sorted(lines, key=lambda h: (h[3], h[4]))
    parsed = []
    numbers_seen: set[str] = set()
    for _, filename, page, ordinal, line_index, raw in ordered:
        match = _NUMBERED_HEADING.match(" ".join(raw.split()))
        if match is None:
            continue
        number = match.group("number")
        if number in numbers_seen:
            continue  # the overlap of consecutive chunks repeats a heading
        numbers_seen.add(number)
        parsed.append(
            (filename, page, ordinal, line_index, number, normalize_title(match.group("title")))
        )
    entries: list[MapEntry] = []
    stack: list[tuple[str, str]] = []  # (number, label) of the enclosing sections
    for index, (filename, page, ordinal, _, number, title) in enumerate(parsed):
        level = number.count(".") + 1
        end = last_ordinal if last_ordinal is not None else ordinal
        for _, _, next_ordinal, next_line, next_number, _ in parsed[index + 1 :]:
            if next_number.count(".") + 1 <= level:
                end = next_ordinal - 1 if next_line == 0 else next_ordinal
                break
        end = max(end, ordinal)
        while stack and not (number.startswith(stack[-1][0] + ".")):
            stack.pop()
        parent = stack[-1][1] if stack else None
        label = f"{number} {title}"
        entries.append(
            MapEntry(
                "section",
                label,
                document_id,
                filename,
                page,
                pages.get((document_id, end), page),
                number=number,
                level=level,
                parent=parent,
                ordinal_start=ordinal,
                ordinal_end=end,
            )
        )
        stack.append((number, label))
    return entries


def map_text(entries: Sequence[MapEntry]) -> str:
    lines = []
    for e in entries:
        pages = (
            f"page {e.page_start}"
            if e.page_start == e.page_end
            else f"pages {e.page_start}-{e.page_end}"
        )
        if e.kind == "section":
            indent = "  " * max(e.level - 1, 0)
            lines.append(f"{indent}- Section {e.label} ({pages})")
        else:
            lines.append(f"- {e.label} ({pages}): {e.caption}")
    return "\n".join(lines)


def entry_of(chunk: RetrievedChunk, entries: Sequence[MapEntry]) -> MapEntry | None:
    """The innermost section of the map that holds the chunk, by its ordinal (or page)."""
    best: MapEntry | None = None
    for e in entries:
        if e.kind != "section" or e.document_id != chunk.document_id:
            continue
        if e.ordinal_start is not None and e.ordinal_end is not None:
            inside = e.ordinal_start <= chunk.ordinal <= e.ordinal_end
        else:
            inside = e.page_start <= chunk.page <= e.page_end
        if inside and (best is None or e.level >= best.level):
            best = e
    return best


def describe_retrieved(
    chunks: Sequence[RetrievedChunk], entries: Sequence[MapEntry], *, snippet_chars: int = 160
) -> list[str]:
    """One line per retrieved source for the Navigator: where it is on the map, whether
    it is a table, and the start of its text — so that it can tell what is covered."""
    lines = []
    for index, c in enumerate(chunks, start=1):
        where = f"[{index}] {c.filename}, page {c.page}"
        section = entry_of(c, entries)
        if section is not None:
            where += f", Section {section.label}"
        caption = _CAPTION.match(c.text.splitlines()[0] if c.text else "")
        if caption is not None:
            where += f", {caption.group(1).title()}"
        if is_table_chunk(c.text):
            where += " (a table)"
        snippet = " ".join(c.text.split())[:snippet_chars]
        lines.append(f"{where}: {snippet}")
    return lines


@dataclass(frozen=True)
class PlanItem:
    """One target of the Navigator: a place, what is needed there, and how it was located."""

    text: str  # the line as written, for the record
    entry: MapEntry | None  # the map entry this target names, if any
    pages: list[int]  # the pages to fetch when no chunk range is known; empty if not located
    location: str = ""
    need: str = ""
    priority: str = "required"
    status: str | None = None  # the Navigator's own view: covered by the retrieval, or missing

    @property
    def located(self) -> bool:
        return bool(self.pages)


def _title_words(title: str) -> set[str]:
    return {w.lower() for w in _WORD.findall(title) if w.lower() not in _STOP}


def parse_plan(text: str, entries: Sequence[MapEntry]) -> list[PlanItem]:
    """The Navigator's targets — one per line ("- place | need: … | priority: … |
    status: …"), or the JSON form — each located on the map (table/figure number,
    section number or title words, or an explicit page within the document) or not."""
    items: list[PlanItem] = []
    for raw, fields in _targets(text):
        location = fields.get("location", "").strip() or raw
        need = fields.get("need", "").strip() or location
        priority = fields.get("priority", "").strip().lower()
        priority = (
            "supplementary" if priority.startswith(("supp", "optional", "补", "補")) else "required"
        )
        stated = fields.get("status", "").strip().lower()
        status = next((s for s in STATUSES if stated.startswith(s[:4])), None)
        entry, pages = _place(location, entries)
        items.append(PlanItem(raw, entry, pages, location, need, priority, status))
    return items


def _targets(text: str) -> list[tuple[str, dict[str, str]]]:
    stripped = text.strip()
    start = stripped.find("{")
    if start >= 0 and stripped.rstrip().endswith("}"):
        try:
            data = json.loads(stripped[start:])
        except json.JSONDecodeError:
            data = None
        targets = data.get("targets", data) if isinstance(data, dict) else data
        if isinstance(targets, list):
            parsed = []
            for t in targets:
                if isinstance(t, dict):
                    given = {str(k).lower(): str(v) for k, v in t.items()}
                    parsed.append((" | ".join(f"{k}: {v}" for k, v in given.items()), given))
            if parsed:
                return parsed
    parsed = []
    for raw in text.splitlines():
        match = _PLAN_LINE.match(raw)
        if match is None:
            continue
        line = match.group(1)
        fields: dict[str, str] = {}
        for position, part in enumerate(line.split("|")):
            field_match = _FIELD.match(part)
            if field_match is not None:
                key = field_match.group(1).lower()
                key = {"place": "location", "why": "reason"}.get(key, key)
                fields[key] = field_match.group(2)
            elif position == 0:
                fields["location"] = part
            elif "need" not in fields:
                fields["need"] = part
        parsed.append((line, fields))
    return parsed


def _place(location: str, entries: Sequence[MapEntry]) -> tuple[MapEntry | None, list[int]]:
    entry = _locate(location, entries)
    if entry is not None:
        return entry, entry.pages
    last_page = max((e.page_end for e in entries), default=0)
    page_ref = _PAGE_REF.search(location)
    if page_ref:
        first = int(page_ref.group(1))
        last = int(page_ref.group(2) or first)
        if 1 <= first <= last <= last_page:
            return None, list(range(first, last + 1))
    return None, []


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


def coverage_of(item: PlanItem, base: Sequence[RetrievedChunk]) -> tuple[str, str]:
    """How far the retrieved sources already hold a target, by structure (D74): a table or
    figure by its caption's chunk — with rows, or caption only; a section by how many of
    its chunks are present. A place known only by its pages cannot be judged: it is
    UNKNOWN, which is not COVERED. Nothing here reads the text for keywords."""
    if not item.located:
        return NOT_LOCATED, "not on the document map"
    entry = item.entry
    if entry is not None and entry.ordinal_start is not None and entry.ordinal_end is not None:
        present = {
            c.ordinal
            for c in base
            if c.document_id == entry.document_id
            and entry.ordinal_start <= c.ordinal <= entry.ordinal_end
        }
        if entry.kind in ("table", "figure"):
            chunk = next(
                (
                    c
                    for c in base
                    if c.document_id == entry.document_id and c.ordinal == entry.ordinal_start
                ),
                None,
            )
            if chunk is None:
                return MISSING, f"the {entry.kind}'s chunk is not among the sources"
            if entry.kind == "figure" or is_table_chunk(chunk.text):
                return COVERED, f"the {entry.kind}'s chunk, with its rows, is among the sources"
            return PARTIAL, "only the caption's chunk is among the sources, without table rows"
        size = entry.ordinal_end - entry.ordinal_start + 1
        if len(present) == size:
            return COVERED, f"all {size} chunks of the section are among the sources"
        if present:
            return PARTIAL, f"{len(present)} of the section's {size} chunks are among the sources"
        return MISSING, "none of the section's chunks is among the sources"
    on_pages = any(c.page in item.pages for c in base)
    if on_pages:
        return UNKNOWN, "only the pages are known; a source on the page may not hold the target"
    return MISSING, "no source on the target's pages"


# --- selecting the evidence ------------------------------------------------------------


@dataclass(frozen=True)
class EvidenceCandidate:
    """A chunk a target could add, with its similarity to the question and to the need.
    A structural candidate (a named table or figure, and its discussion) is taken for
    its place, not its similarity."""

    chunk: RetrievedChunk
    question_score: float | None
    need_score: float | None
    structural: bool = False

    @property
    def relevance(self) -> float | None:
        if self.structural:
            return None
        scores = [s for s in (self.question_score, self.need_score) if s is not None]
        return round(sum(scores) / len(scores), 4) if scores else None

    def clears(self, floor: float) -> bool:
        if self.structural:
            return True
        scores = [s for s in (self.question_score, self.need_score) if s is not None]
        return bool(scores) and max(scores) >= floor


@dataclass(frozen=True)
class TargetCandidates:
    item: PlanItem
    candidates: list[EvidenceCandidate]  # best first
    coverage: str = UNKNOWN  # D74: coverage_of the target by the retrieved sources


@dataclass(frozen=True)
class Selection:
    chunks: list[RetrievedChunk]  # the Top-K whole, then what the targets added
    log: list[dict[str, Any]]  # one entry per chunk considered
    targets: list[dict[str, Any]]  # one record per target
    evidence_tokens: int = 0
    unmet_required: list[str] = field(default_factory=list)  # required targets that got nothing
    supplementary_used: int = 0


def _content_words(text: str) -> set[str]:
    return {w.lower() for w in _CONTENT_WORD.findall(text)}


def repeats(chunk: RetrievedChunk, selected: Sequence[RetrievedChunk]) -> bool:
    """Whether the chunk's content words largely repeat one of the selected chunks."""
    words = _content_words(chunk.text)
    if not words:
        return False
    for other in selected:
        theirs = _content_words(other.text)
        if theirs and len(words & theirs) / len(words | theirs) >= OVERLAP_MAX:
            return True
    return False


@dataclass
class _Turn:
    index: int
    target: TargetCandidates
    queue: list[EvidenceCandidate] = field(default_factory=list)
    taken: int = 0

    @property
    def rank(self) -> tuple[int, float]:
        """Lower sorts first: required targets, then the best next candidate (a structural
        one, such as a named table, before any similarity score)."""
        head = self.queue[0]
        best = float("inf") if head.structural else (head.relevance or 0.0)
        return (0 if self.target.item.priority == "required" else 1, -best)


def select_evidence(
    base: Sequence[RetrievedChunk],
    targets: Sequence[TargetCandidates],
    *,
    budget: int,
    floor: float,
    per_target: int = CHUNKS_PER_TARGET,
    supplementary_cap: int = SUPPLEMENTARY_CAP,
) -> Selection:
    """The original Top-K whole; then the required targets take turns adding their best
    remaining candidate while the budget lasts (the target whose next candidate scores
    highest first, a named table before any score); then, with what budget is left, the
    supplementary targets take turns up to `supplementary_cap` chunks in all — none when
    every required target is already covered by the retrieved sources (D74). A candidate
    below the relevance floor, already present, repeating selected text (supplementary),
    or over the budget is logged and skipped; a target adds at most `per_target` chunks."""
    chunks: list[RetrievedChunk] = list(base)
    log: list[dict[str, Any]] = [
        {
            "ordinal": c.ordinal,
            "page": c.page,
            "kept": True,
            "reason": c.origin,
            "target": None,
            "score": None,
        }
        for c in base
    ]
    spent = sum(c.token_count for c in base)
    present: dict[uuid.UUID, int | None] = {c.chunk_id: None for c in base}
    records: list[dict[str, Any]] = [
        {
            "location": t.item.location,
            "need": t.item.need,
            "priority": t.item.priority,
            "status": t.item.status,
            "coverage": t.coverage,
            "located": t.item.located,
            "label": t.item.entry.label if t.item.entry else None,
            "candidates": len(t.candidates),
            "selected": [],
            "excluded": [],
        }
        for t in targets
    ]
    turns = [_Turn(i, t, list(t.candidates)) for i, t in enumerate(targets)]

    def drop(turn: _Turn, candidate: EvidenceCandidate, reason: str) -> None:
        c = candidate.chunk
        log.append(
            {
                "ordinal": c.ordinal,
                "page": c.page,
                "kept": False,
                "reason": reason,
                "target": turn.index,
                "score": candidate.relevance,
            }
        )
        records[turn.index]["excluded"].append({"ordinal": c.ordinal, "reason": reason})

    required = [t for t in turns if t.target.item.priority == "required"]
    supplementary = [t for t in turns if t.target.item.priority != "required"]
    all_required_covered = bool(required) and all(t.target.coverage == COVERED for t in required)

    # Candidates that cannot be taken whatever the budget are settled first, so that the
    # turns only ever look at live candidates.
    for turn in turns:
        live = []
        for candidate in turn.queue:
            if turn.target.coverage == COVERED and turn in required:
                drop(turn, candidate, "target already covered by the retrieved sources")
            elif turn in supplementary and all_required_covered:
                drop(turn, candidate, "all required evidence already covered")
            elif not candidate.clears(floor):
                drop(turn, candidate, "low relevance")
            else:
                live.append(candidate)
        turn.queue = live

    supplementary_used = 0

    def take_turns(group: list[_Turn], *, is_supplementary: bool) -> None:
        nonlocal spent, supplementary_used
        while any(t.queue for t in group):
            for turn in sorted((t for t in group if t.queue), key=lambda t: t.rank):
                candidate = turn.queue.pop(0)
                c = candidate.chunk
                if turn.taken >= per_target:
                    drop(turn, candidate, "target quota reached")
                    continue
                if is_supplementary and supplementary_used >= supplementary_cap:
                    drop(turn, candidate, "supplementary cap reached")
                    continue
                if c.chunk_id in present:
                    drop(
                        turn,
                        candidate,
                        "already among the retrieved sources"
                        if present[c.chunk_id] is None
                        else "already selected for another target",
                    )
                    continue
                if is_supplementary and repeats(c, chunks):
                    drop(turn, candidate, "repeats evidence already selected")
                    continue
                if spent + c.token_count > budget:
                    drop(turn, candidate, "over the evidence budget")
                    continue
                chunks.append(
                    RetrievedChunk(
                        c.chunk_id,
                        c.document_id,
                        c.filename,
                        c.page,
                        c.ordinal,
                        c.text,
                        c.token_count,
                        candidate.relevance,
                        "navigation",
                    )
                )
                present[c.chunk_id] = turn.index
                spent += c.token_count
                turn.taken += 1
                if is_supplementary:
                    supplementary_used += 1
                log.append(
                    {
                        "ordinal": c.ordinal,
                        "page": c.page,
                        "kept": True,
                        "reason": f"plan: {turn.target.item.location}",
                        "target": turn.index,
                        "score": candidate.relevance,
                    }
                )
                records[turn.index]["selected"].append(c.ordinal)

    take_turns(required, is_supplementary=False)
    take_turns(supplementary, is_supplementary=True)
    # Required evidence that did not reach the prompt (not located, low relevance, over
    # the budget): named so that nobody mistakes it for covered. A target whose every
    # candidate was already among the sources did reach the prompt, by another road.
    already = ("already among the retrieved sources", "already selected for another target")
    unmet = [
        t.target.item.location
        for t in required
        if t.target.coverage != COVERED
        and not records[t.index]["selected"]
        and not (
            records[t.index]["excluded"]
            and all(x["reason"] in already for x in records[t.index]["excluded"])
        )
    ]
    return Selection(chunks, log, records, spent, unmet, supplementary_used)


# --- the prompts -----------------------------------------------------------------------


# N4 (2026-11-07): without this rule the Navigator named the table a question needs in 7/10
# (Table 1 for the comparison question) and 4/10 (Table 6 for the GraphRAG pairwise question)
# Navigator-only runs; with it and temperature 0, 10/10 and 10/10 (N1–N4 in
# evaluation/navigator-abc/runs). The rule is a template field so an experiment can drop it.
TABLES_RULE = (
    "- The figures of a paper are in its tables: name every table or figure on the map whose "
    "caption concerns what the question asks about — a method, a dataset or a measure it "
    "names, or the comparison it asks for — even when the caption does not use the "
    "question's words. A section that discusses a table does not replace the table.\n"
)

NAVIGATION_INSTRUCTIONS = """\
You are the Navigator for a question about the user's documents. Your job is to say where in \
the documents the evidence is and what is needed from each place, not what it says.

Rules:
- Use the document map and the sources already retrieved below. List the targets the answer \
needs: a section or subsection, a table, a figure or a page, named as the map names it, with \
what is needed from it. Prefer not to miss evidence; at most six targets.
{tables_rule}- One target per line, in this form:
  - <place as the map names it> | need: <what to find there, in a few words> | priority: \
required or supplementary | status: covered or missing
  "status: covered" means the retrieved sources already hold that evidence; "missing" means \
it still has to be fetched. You may name a covered place again; it will not be fetched twice.
- Do not answer the question. Do not state any fact, number or conclusion from the documents, \
and do not guess what a place contains beyond its title.
{language_rule}

Document map:
{map}

Sources already retrieved:
{retrieved}

Question: {question}

Reading plan:"""


def build_navigation_prompt(
    question: str,
    entries: Sequence[MapEntry],
    retrieved: Sequence[str],
    counter: TokenCounter,
    limit: int,
) -> tuple[str, int]:
    prompt = NAVIGATION_INSTRUCTIONS.format(
        tables_rule=TABLES_RULE,
        language_rule=LANGUAGE_RULES[question_language(question)],
        map=map_text(entries) or "- (no map available)",
        retrieved="\n".join(retrieved) or "(none)",
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
    """For the second call of the navigate mode: what the Navigator asked for, marked as such."""
    lines = [
        f"- {i.location}: {i.need}" + ("" if i.located else " (not found in the document)")
        for i in items
    ]
    return (
        "A Navigator proposed where to look and what is needed there (candidates, not verified):\n"
        + ("\n".join(lines) or "- (nothing)")
        + "\nAnswer only from the numbered sources below; do not assume those places are right.\n\n"
    )
