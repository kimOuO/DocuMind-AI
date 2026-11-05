"""Split a document into the units that are summarised one call each.

Boundaries are the recognised headings, located by page and line; the heading
text is carried along but never trusted (AC-53). The reference list is left
out. A unit that would not fit one summary call is split into its subsections,
and a unit that still does not fit is cut into batches of lines, so that every
unit keeps a true page range.
"""

import re
from collections.abc import Sequence
from dataclasses import dataclass

from app.ingestion.headings import Heading
from app.ingestion.parsing import Page
from app.llm.tokenizer import TokenCounter

# Unnumbered headings after which nothing is summarised, until the next heading.
_EXCLUDED_HEADINGS = {"references", "bibliography", "acknowledgments", "acknowledgements"}
_CAPITALS_ONLY = re.compile(r"^[A-Z ]+$")


@dataclass(frozen=True)
class PageSlice:
    """The part of one page that belongs to a unit."""

    page: int
    text: str


@dataclass(frozen=True)
class SummaryUnit:
    number: str | None
    title: str
    page_start: int
    page_end: int
    text: str
    token_count: int
    pages: tuple[PageSlice, ...] = ()


@dataclass(frozen=True)
class _Line:
    page: int
    text: str


def _slices(lines: list[_Line]) -> tuple[PageSlice, ...]:
    """The lines regrouped by page, blank edges removed."""
    grouped: list[list[_Line]] = []
    for line in lines:
        if grouped and grouped[-1][0].page == line.page:
            grouped[-1].append(line)
        else:
            grouped.append([line])
    slices = (PageSlice(g[0].page, "\n".join(x.text for x in g).strip()) for g in grouped)
    return tuple(s for s in slices if s.text)


@dataclass(frozen=True)
class _Span:
    """A run of lines [start, stop) with the heading that opens it, if any."""

    start: int
    stop: int
    number: str | None
    title: str
    level: int  # level of the heading that opens it; 0 for text before any heading


def plan_summary_units(
    pages: Sequence[Page],
    headings: Sequence[Heading],
    counter: TokenCounter,
    *,
    budget_tokens: int,
) -> list[SummaryUnit]:
    """The units to summarise, in document order, each within `budget_tokens`."""
    lines = [_Line(page.number, text) for page in pages for text in page.text.splitlines()]
    if not any(line.text.strip() for line in lines):
        return []
    offsets = _page_offsets(pages)
    located = sorted(
        ((offsets[h.page] + h.line, h) for h in headings if h.page in offsets),
        key=lambda item: item[0],
    )
    excluded = _excluded_ranges(lines, [index for index, _ in located])

    top_level = min((h.level for _, h in located), default=0)
    if top_level == 0:
        spans = [_Span(0, len(lines), None, "Full text", 0)]
    else:
        spans = _spans_at_level(located, top_level, 0, len(lines), None, "Front matter", 0)

    units: list[SummaryUnit] = []
    for span in spans:
        units.extend(_fit(span, lines, located, excluded, counter, budget_tokens))
    return units


def _page_offsets(pages: Sequence[Page]) -> dict[int, int]:
    offsets: dict[int, int] = {}
    total = 0
    for page in pages:
        offsets[page.number] = total
        total += len(page.text.splitlines())
    return offsets


def _excluded_ranges(lines: list[_Line], heading_indexes: list[int]) -> list[tuple[int, int]]:
    """Line ranges of the reference list and the like: from the heading to the next heading."""
    ranges = []
    for index, line in enumerate(lines):
        stripped = line.text.strip()
        if (
            _CAPITALS_ONLY.match(stripped)
            and stripped.replace(" ", "").lower() in _EXCLUDED_HEADINGS
        ):
            following = [h for h in heading_indexes if h > index]
            ranges.append((index, following[0] if following else len(lines)))
    return ranges


def _spans_at_level(
    located: list[tuple[int, Heading]],
    level: int,
    start: int,
    stop: int,
    number: str | None,
    title: str,
    parent_level: int,
) -> list[_Span]:
    """Split [start, stop) at the headings of `level`.

    Text before the first such heading keeps the enclosing `number` and `title`.
    """
    inside = [(i, h) for i, h in located if h.level == level and start <= i < stop]
    spans: list[_Span] = []
    first = inside[0][0] if inside else stop
    if first > start:
        spans.append(_Span(start, first, number, title, parent_level))
    for position, (index, heading) in enumerate(inside):
        end = inside[position + 1][0] if position + 1 < len(inside) else stop
        spans.append(_Span(index, end, heading.number, heading.title, heading.level))
    return spans


def _fit(
    span: _Span,
    lines: list[_Line],
    located: list[tuple[int, Heading]],
    excluded: list[tuple[int, int]],
    counter: TokenCounter,
    budget: int,
) -> list[SummaryUnit]:
    kept = _kept_lines(span, lines, excluded)
    if not any(line.text.strip() for line in kept):
        return []
    text = "\n".join(line.text for line in kept).strip()
    tokens = counter.count(text)
    if tokens <= budget:
        return [
            SummaryUnit(
                span.number, span.title, kept[0].page, kept[-1].page, text, tokens, _slices(kept)
            )
        ]

    deeper = [h.level for i, h in located if span.start < i < span.stop and h.level > span.level]
    if deeper:
        units: list[SummaryUnit] = []
        for part in _spans_at_level(
            located, min(deeper), span.start, span.stop, span.number, span.title, span.level
        ):
            units.extend(_fit(part, lines, located, excluded, counter, budget))
        return units
    return _batches(span, kept, counter, budget)


def _kept_lines(span: _Span, lines: list[_Line], excluded: list[tuple[int, int]]) -> list[_Line]:
    kept = []
    for index in range(span.start, span.stop):
        if any(a <= index < b for a, b in excluded):
            continue
        kept.append(lines[index])
    # Trim blank lines at both ends so the page range is that of real text.
    while kept and not kept[0].text.strip():
        kept.pop(0)
    while kept and not kept[-1].text.strip():
        kept.pop()
    return kept


def _batches(
    span: _Span, kept: list[_Line], counter: TokenCounter, budget: int
) -> list[SummaryUnit]:
    """Consecutive batches of lines within the budget; a single long line is cut by words."""
    pieces: list[_Line] = []
    for line in kept:
        if counter.count(line.text) > budget:
            pieces.extend(
                _Line(line.page, part) for part in _split_words(line.text, counter, budget)
            )
        else:
            pieces.append(line)

    groups: list[list[_Line]] = []
    current: list[_Line] = []
    current_tokens = 0
    for piece in pieces:
        cost = counter.count(piece.text)
        if current and current_tokens + cost > budget:
            groups.append(current)
            current, current_tokens = [], 0
        current.append(piece)
        current_tokens += cost
    if current:
        groups.append(current)

    units = []
    for position, group in enumerate(groups, start=1):
        text = "\n".join(line.text for line in group).strip()
        title = (
            f"{span.title} (part {position}/{len(groups)})" if span.level else f"Part {position}"
        )
        units.append(
            SummaryUnit(
                span.number,
                title,
                group[0].page,
                group[-1].page,
                text,
                counter.count(text),
                _slices(group),
            )
        )
    return units


def _split_words(text: str, counter: TokenCounter, budget: int) -> list[str]:
    pieces: list[str] = []
    current: list[str] = []
    for word in text.split():
        if current and counter.count(" ".join([*current, word])) > budget:
            pieces.append(" ".join(current))
            current = []
        current.append(word)
    if current:
        pieces.append(" ".join(current))
    return pieces
