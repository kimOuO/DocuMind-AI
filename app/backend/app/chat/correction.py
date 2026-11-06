"""Deterministic correction of an answer's table claims (D75): the parts without a model.

The checks of this package say where an answer contradicts the tables of its sources:
a figure under labels no cell carries, a comparison word that goes against the two
figures. This module fixes what has one clear reading in the table and removes what
has none — never inventing a figure, never touching a sentence the checks accept:

- a figure whose method, metric and dataset are all stated, and which one cell of those
  labels holds another value of: the figure becomes that cell's value;
- a figure that one other method (or one other pairing) of the same row and group holds:
  the wrong name becomes that method's (or pairing's) name — only when the name is
  written plainly, not as an alias;
- a figure with both readings, or neither: its parenthesis (or its sentence) is removed;
- an ordering word that goes against the figures: its antonym; a performance word, the
  same, but only when the metric's direction is known.

One pass, then the checks run again on the result; what still fails is reported, not
fixed again. Nothing here knows any paper in particular.
"""

import re
from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Any

from app.chat.evidence import (
    DirectionIssue,
    MatrixCell,
    check_directions,
    matrix_cells_of_pages,
)
from app.chat.verification import (
    Aliases,
    LabelOutcome,
    PageText,
    _key,
    _label_pattern,
    label_outcomes,
)

MAX_PASSES = 1
_STEP_NUMBER = re.compile(r"^\(\d{1,2}\)\s+", re.MULTILINE)
_PARENTHESIS = re.compile(r"\s?\([^()]*\)")
# A name written right after a figure ("32.4% for Other") or right before it ("Other 32.4%").
_NAME_AFTER = re.compile(r"^\s*(?:for|of|by|from|in|with|\()\s*([A-Z][\w.-]*)")
_NAME_BEFORE = re.compile(r"([A-Z][\w.-]*)(?:['’]s)?[\s:(]*$")
# Between two figures of one comparison: the second is the first's partner, not a second
# statement about the same method.
_BRIDGE = re.compile(
    r"^\s*(?:vs\.?|versus|against|compared\s+(?:to|with)|to|→|and)\s*$", re.IGNORECASE
)
_NOT_A_NAME = re.compile(
    r"^(?:In|On|For|The|A|An|Table|Figure|Section|Dataset|Datasets|Metric|Overall|And|But|With)$"
)

ANTONYMS = {
    # ordering
    "drops": "rises",
    "drop": "rise",
    "dropped": "rose",
    "dropping": "rising",
    "falls": "rises",
    "fall": "rise",
    "fell": "rose",
    "falling": "rising",
    "declines": "increases",
    "decline": "increase",
    "declined": "increased",
    "declining": "increasing",
    "decreases": "increases",
    "decrease": "increase",
    "decreased": "increased",
    "decreasing": "increasing",
    "reduces": "increases",
    "reduced": "increased",
    "reduction": "increase",
    "lower": "higher",
    "higher": "lower",
    "below": "above",
    "above": "below",
    "smaller": "larger",
    "larger": "smaller",
    "greater": "smaller",
    "less than": "more than",
    "more than": "less than",
    "rises": "falls",
    "rise": "fall",
    "rose": "fell",
    "rising": "falling",
    "increases": "decreases",
    "increase": "decrease",
    "increased": "decreased",
    "increasing": "decreasing",
    "exceeds": "falls below",
    "exceed": "fall below",
    "exceeded": "fell below",
    "grows": "shrinks",
    "grew": "shrank",
    # performance
    "outperforms": "underperforms",
    "outperform": "underperform",
    "outperformed": "underperformed",
    "outperforming": "underperforming",
    "underperforms": "outperforms",
    "underperform": "outperform",
    "underperformed": "outperformed",
    "better": "worse",
    "worse": "better",
    "improves": "declines",
    "improve": "decline",
    "improved": "declined",
    "improving": "declining",
    "improvement": "decline",
    "surpasses": "falls behind",
    "surpass": "fall behind",
    "surpassed": "fell behind",
    "superior": "inferior",
    "inferior": "superior",
    "beats": "trails",
    "beat": "trail",
    "degrades": "improves",
    "degraded": "improved",
    "stronger": "weaker",
    "weaker": "stronger",
}


@dataclass(frozen=True)
class Correction:
    text: str
    edits: list[dict[str, Any]] = field(default_factory=list)  # applied, in text order
    removed: list[str] = field(default_factory=list)  # text taken out
    remaining: list[str] = field(default_factory=list)  # faults the pass could not fix
    uncertain: list[DirectionIssue] = field(default_factory=list)  # not decidable, left alone


@dataclass(frozen=True)
class _Edit:
    start: int
    end: int
    replacement: str
    record: dict[str, Any]


def strip_step_numbering(text: str) -> str:
    """Remove "(1) ", "(2) " … at the start of lines when the answer is numbered after the
    analysis steps (two or more such lines); a lone "(1)" is left as it is."""
    if len(_STEP_NUMBER.findall(text)) < 2:
        return text
    return _STEP_NUMBER.sub("", text)


def _remove_span(
    text: str, start: int, end: int, sentence: tuple[int, int] | None = None
) -> tuple[int, int, str]:
    """The span to cut for a figure: its enclosing parenthesis when it is in one, else the
    sentence it is in; and the text being cut."""
    for m in _PARENTHESIS.finditer(text):
        if m.start() <= start and end <= m.end():
            return m.start(), m.end(), m.group().strip()
    if sentence is not None:
        s_start, s_end = sentence
        while s_end < len(text) and text[s_end] in " \n":
            s_end += 1
        return s_start, s_end, text[s_start : sentence[1]].strip()
    return 0, len(text), text.strip()


def _unknown_name(
    sentence: str, figure_at: int, figure_end: int, known: set[str]
) -> tuple[int, int] | None:
    """A name attached to the figure that no table knows: the figure's stated subject."""
    after = _NAME_AFTER.match(sentence[figure_end:])
    if after is not None:
        name = after.group(1)
        if name not in known and not _NOT_A_NAME.match(name):
            return figure_end + after.start(1), figure_end + after.end(1)
    before = _NAME_BEFORE.search(sentence[:figure_at])
    if before is not None:
        name = before.group(1)
        if name not in known and not _NOT_A_NAME.match(name):
            return before.start(1), before.end(1)
    return None


def _figure_edit(
    text: str, outcome: LabelOutcome, cells: Sequence[MatrixCell], aliases: Aliases | None
) -> _Edit | None:
    """One clear reading of a contradicted figure, or None.

    Two readings are tried. Name reading: the figure is right and credited to the wrong
    method or pairing — one other column (or pairing) of the same row and group holds it,
    and the wrong name is written plainly. Figure reading: the stated method, metric and
    dataset name one cell with another value. When both are possible, the place of the
    wrong name decides: a name attached after the figure ("16.4% for X") was put on the
    figure by the writer and is the part to fix; a subject before the figure ("X reaches
    16.4%") is what the sentence is about, so the figure is the part to fix."""
    row, group, method = [*outcome.claim, None, None, None][:3]
    comparator = outcome.comparator
    sentence_start, sentence_end = outcome.sentence_span
    sentence = text[sentence_start:sentence_end]
    figure_at, figure_end = outcome.position - sentence_start, outcome.end - sentence_start
    known = {label for c in cells for label in (c.row, c.group, c.column) if label}

    holders = [
        c
        for c in cells
        if _key(c.value) == _key(outcome.number)
        and (row is None or c.row == row)
        and (group is None or c.group == group)
    ]
    columns = {c.column for c in holders}
    pairings = {c.paired_with for c in holders}
    name_edit: _Edit | None = None
    name_after = False
    if len(columns) == 1 and method not in columns:
        right = next(iter(columns))
        unknown = _unknown_name(sentence, figure_at, figure_end, known)
        span: tuple[int, int] | None = None
        wrong = method or ""
        if unknown is not None:
            span, wrong = unknown, sentence[unknown[0] : unknown[1]]
        elif method is not None:
            plain = [
                (m.start(), m.end())
                for m in _label_pattern(method).finditer(sentence)
                if not any(p.search(m.group()) for p in (aliases or {}).get(method, ()))
            ]
            if plain:
                span = min(plain, key=lambda s: abs(s[0] - figure_at))
        if span is not None:
            name_after = span[0] >= figure_end
            name_edit = _Edit(
                sentence_start + span[0],
                sentence_start + span[1],
                right,
                {"kind": "label", "before": wrong, "after": right, "figure": outcome.number},
            )
    elif (
        comparator is not None
        and len(pairings) == 1
        and next(iter(pairings)) is not None
        and comparator not in pairings
    ):
        right = str(next(iter(pairings)))
        after = [
            (m.start(), m.end())
            for m in _label_pattern(comparator).finditer(sentence)
            if m.start() > figure_at
        ]
        if after:
            span = min(after, key=lambda s: s[0] - figure_at)
            name_after = True
            name_edit = _Edit(
                sentence_start + span[0],
                sentence_start + span[1],
                right,
                {"kind": "label", "before": comparator, "after": right, "figure": outcome.number},
            )

    stated = [
        c
        for c in cells
        if method is not None
        and row is not None
        and group is not None
        and c.row == row
        and c.group == group
        and c.column == method
        and (comparator is None or c.paired_with == comparator)
    ]
    figure_edit: _Edit | None = None
    if len({_key(c.value) for c in stated}) == 1:
        figure_edit = _Edit(
            outcome.position,
            outcome.end,
            stated[0].value,
            {
                "kind": "figure",
                "before": outcome.number,
                "after": stated[0].value,
                "labels": outcome.answer_labels,
            },
        )
    if name_edit is not None and figure_edit is not None:
        return name_edit if name_after else figure_edit
    return name_edit or figure_edit


def _contradicted(outcomes: Sequence[LabelOutcome], text: str) -> list[LabelOutcome]:
    """The contradicted figures that are a statement of their own: a figure right after a
    comparison bridge ("34.8% vs. 67.6%") with the same labels as the one before it is
    that one's partner, whose method the sentence does not name — not a fault to fix."""
    kept: list[LabelOutcome] = []
    previous: LabelOutcome | None = None
    for outcome in outcomes:
        partner = (
            previous is not None
            and previous.sentence_span == outcome.sentence_span
            and previous.claim == outcome.claim
            and _BRIDGE.match(text[previous.end : outcome.position]) is not None
        )
        if outcome.status == "contradicted" and not partner:
            kept.append(outcome)
        previous = outcome
    return kept


def correct(
    text: str,
    pages: Sequence[PageText],
    *,
    aliases: Aliases | None = None,
    unverified: Sequence[str] = (),
) -> Correction:
    """Fix or remove what the tables of the pages contradict, once; report the rest."""
    cells = matrix_cells_of_pages(pages)
    edits: list[dict[str, Any]] = []
    removed: list[str] = []
    working = text
    # Figures found on no cited page go first (their parenthesis or sentence), so that the
    # label check below does not read the neighbours of a figure that is leaving anyway.
    for number in unverified:
        at = working.find(number)
        if at < 0:
            continue
        start, end, cut = _remove_span(working, at, at + len(number))
        working = working[:start] + working[end:]
        removed.append(cut)
    if not cells:
        return Correction(working, edits, removed, [], [])

    planned: list[_Edit] = []
    seen: set[tuple[int, int]] = set()
    for outcome in _contradicted(label_outcomes(working, pages, aliases), working):
        if (outcome.position, outcome.end) in seen:
            continue
        seen.add((outcome.position, outcome.end))
        edit = _figure_edit(working, outcome, cells, aliases)
        if edit is None:
            start, end, cut = _remove_span(
                working, outcome.position, outcome.end, outcome.sentence_span
            )
            planned.append(_Edit(start, end, "", {"kind": "remove", "text": cut}))
        else:
            planned.append(edit)
    for issue in check_directions(working, pages, aliases):
        if issue.status != "inconsistent":
            continue
        antonym = ANTONYMS.get(issue.cue.lower())
        if antonym is None:
            continue
        if issue.cue[:1].isupper():
            antonym = antonym[:1].upper() + antonym[1:]
        planned.append(
            _Edit(
                issue.cue_span[0],
                issue.cue_span[1],
                antonym,
                {
                    "kind": issue.kind,
                    "before": issue.cue,
                    "after": antonym,
                    "figures": [issue.left, issue.right],
                },
            )
        )
    # Apply from the end so that earlier positions stay valid; skip overlaps.
    taken: list[tuple[int, int]] = []
    for edit in sorted(planned, key=lambda e: e.start, reverse=True):
        if any(not (edit.end <= a or edit.start >= b) for a, b in taken):
            continue
        taken.append((edit.start, edit.end))
        working = working[: edit.start] + edit.replacement + working[edit.end :]
        if edit.record["kind"] == "remove":
            removed.append(edit.record["text"])
        else:
            edits.append(edit.record)
    edits.reverse()

    # The checks run again on the result; what still fails is reported, not fixed again.
    remaining = [
        f"{o.number} ({', '.join(o.answer_labels)})"
        for o in _contradicted(label_outcomes(working, pages, aliases), working)
    ]
    after = check_directions(working, pages, aliases)
    remaining.extend(
        f'"{i.cue}" ({i.left} / {i.right})' for i in after if i.status == "inconsistent"
    )
    uncertain = [i for i in after if i.status == "uncertain"]
    return Correction(working, edits, removed, remaining, uncertain)
