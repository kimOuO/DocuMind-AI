"""Checking the numbers in an answer against the original text of the cited pages (AC-26).

A summary answer is produced from summaries, two steps away from the text, so
every concrete number in it is looked up on the pages its cited sources cover.
A number is verified when the same value appears there, ignoring thousands
separators and a percent sign; the page and a snippet of the original text are
kept as evidence. A number that is not found is reported, never let through
silently. No LLM is involved.

A figure that is found may still be attributed wrongly: the model copies a
table value correctly and puts it under a neighbouring metric or variant (D64).
Table chunks are written one row per line with every figure next to its labels
(app.ingestion.tables), so each table value has a known set of labels. For
every such figure in the answer, the labels mentioned nearest to it in its
clause are compared with the labels of the cells holding that value; a figure
whose mentioned labels fit none of them is reported as mislabelled. A label
category the clause does not mention is not compared, so this finds wrong
labels, not missing ones.
"""

import re
import uuid
from collections.abc import Iterable, Sequence
from dataclasses import dataclass

from app.ingestion.tables import cells_of

# A number: with thousands separators, or plain; optional decimals; optional percent.
# Not preceded by a letter, digit or dot, so "v3" and the tail of "2410.05779" stay out.
_NUMBER = re.compile(r"(?<![\w.,])(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?%?")
_CITATION = re.compile(r"\[\s*\d{1,3}(?:\s*,\s*\d{1,3})*\s*\]")
_PAGE_REFERENCE = re.compile(r"\(pp?\.\s*\d+(?:\s*[-–]\s*\d+)?\)")
_SNIPPET_RADIUS = 80
# Where one sentence ends: a full stop followed by space, unless it is an abbreviation.
_SENTENCE_END = re.compile(
    r"(?<!\be\.g\.)(?<!\bi\.e\.)(?<!\bvs\.)(?<!\betc\.)(?<=[.!?。！？])\s+|\n+"
)
# Where one statement about figures ends and the next begins inside a sentence: a
# semicolon, a connective, or a comparison whose two sides are different things.
_CLAUSE_BREAK = re.compile(
    r"\s*[;；]\s*|,\s+(?:and|but|while|whereas)\s+|,?\s+(?:compared (?:to|with)|versus|vs\.?)\s+"
    r"|，(?:而|但|且)"
)
# What may stand between a label and the figure it belongs to: "NaiveRAG 32.4%",
# "NaiveRAG's 32.4%", "NaiveRAG: 32.4%", "32.4% (NaiveRAG)", "32.4% comprehensiveness".
# A comma breaks the tie: in "67.6% comprehensiveness, 76.4%" the label is 67.6%'s.
_BEFORE_FIGURE = re.compile(r"(?:['’]s)?[\s:(]{0,2}")
_AFTER_FIGURE = re.compile(r"[\s(]{0,2}")


@dataclass(frozen=True)
class PageText:
    document_id: uuid.UUID
    page: int
    text: str


@dataclass(frozen=True)
class VerifiedNumber:
    number: str  # as written in the answer
    document_id: uuid.UUID
    page: int
    snippet: str  # the original text around the number


@dataclass(frozen=True)
class MislabelledNumber:
    number: str  # as written in the answer
    answer_labels: list[str]  # the labels the answer put nearest to it, in table order
    source_labels: list[list[str]]  # the labels of each table cell holding this value
    sentence: str  # the answer's sentence the figure is in


@dataclass(frozen=True)
class NumberCheck:
    verified: list[VerifiedNumber]
    unverified: list[str]
    mislabelled: list[MislabelledNumber]


def _normalise(number: str) -> str:
    return number.replace(",", "").rstrip("%")


def _is_worth_checking(number: str) -> bool:
    """Single digits without a decimal or percent are labels and counts ("Table 2",
    "4 datasets", usually written as words in the text), not results."""
    return "." in number or number.endswith("%") or len(_normalise(number)) >= 2


def numbers_in(answer: str) -> list[str]:
    """The numbers in the answer, as written, once each in order of first appearance.

    Citation markers and page references are not numbers of the answer.
    """
    stripped = _PAGE_REFERENCE.sub(" ", _CITATION.sub(" ", answer))
    found: list[str] = []
    for match in _NUMBER.finditer(stripped):
        number = match.group()
        if _is_worth_checking(number) and number not in found:
            found.append(number)
    return found


def _snippet(text: str, start: int, end: int) -> str:
    left = max(0, start - _SNIPPET_RADIUS)
    right = min(len(text), end + _SNIPPET_RADIUS)
    piece = " ".join(text[left:right].split())
    return f"{'…' if left > 0 else ''}{piece}{'…' if right < len(text) else ''}"


def verify_numbers(answer: str, pages: Sequence[PageText]) -> NumberCheck:
    """Look every number of the answer up on the given pages, in their order, and
    compare the labels of the table figures among them."""
    wanted = numbers_in(answer)
    if not wanted:
        return NumberCheck([], [], [])
    # Where each value occurs: the first page that has it, with the match position.
    located: dict[str, tuple[PageText, int, int]] = {}
    for page in pages:
        for match in _NUMBER.finditer(page.text):
            value = _normalise(match.group())
            if value not in located:
                located[value] = (page, match.start(), match.end())
    verified: list[VerifiedNumber] = []
    unverified: list[str] = []
    for number in wanted:
        hit = located.get(_normalise(number))
        if hit is None:
            unverified.append(number)
        else:
            page, start, end = hit
            verified.append(
                VerifiedNumber(number, page.document_id, page.page, _snippet(page.text, start, end))
            )
    return NumberCheck(verified, unverified, check_labels(answer, pages))


def _table_cells(pages: Iterable[PageText]) -> dict[str, list[tuple[str, ...]]]:
    """Normalised value -> the label tuples of the table cells holding it."""
    cells: dict[str, list[tuple[str, ...]]] = {}
    for page in pages:
        for line in page.text.splitlines():
            for value, labels in cells_of(line):
                known = cells.setdefault(_normalise(value), [])
                if labels not in known:
                    known.append(labels)
    return cells


def _label_pattern(label: str) -> re.Pattern[str]:
    # Whole words, case ignored; a label such as "-High" may follow a word directly.
    prefix = r"(?<!\w)" if label[0].isalnum() else ""
    suffix = r"(?!\w)" if label[-1].isalnum() else ""
    return re.compile(prefix + re.escape(label) + suffix, re.IGNORECASE)


Span = tuple[int, int]
Mention = tuple[int, int, str]  # start, end, label


def _mentions(clause: str, labels: Iterable[str]) -> list[Mention]:
    """Where the labels of one category are mentioned in the clause.

    Two labels directly after one another ("LightRAG -High") are one compound
    name, and the later one is the name that counts.
    """
    found = sorted(
        (m.start(), m.end(), label)
        for label in labels
        for m in _label_pattern(label).finditer(clause)
    )
    merged: list[Mention] = []
    for start, end, label in found:
        if merged and 0 <= start - merged[-1][1] <= 1:
            merged[-1] = (merged[-1][0], end, label)
        else:
            merged.append((start, end, label))
    return merged


def _attached(clause: str, mention: Mention, figure: Span, figures: Sequence[Span]) -> bool:
    """A label written right before a figure ("LightRAG 67.6%") or right after it
    ("67.6% (LightRAG)") is that figure's own; one that could be either goes with
    the figure it precedes."""
    m_start, m_end, _ = mention
    start, end = figure
    if m_end <= start and _BEFORE_FIGURE.fullmatch(clause[m_end:start]):
        return True
    if end <= m_start and _AFTER_FIGURE.fullmatch(clause[end:m_start]):
        return not any(
            other_start >= m_end and _BEFORE_FIGURE.fullmatch(clause[m_end:other_start])
            for other_start, _ in figures
            if other_start != start
        )
    return False


def _nearest(mentions: Sequence[Mention], figure: Span) -> str | None:
    start, end = figure
    best: tuple[int, int, str] | None = None
    for m_start, m_end, label in mentions:
        distance = max(m_start - end, start - m_end, 0)
        if best is None or (distance, -len(label)) < best[:2]:
            best = (distance, -len(label), label)
    return None if best is None else best[2]


def _label_for(
    clause: str, figure: Span, figures: Sequence[Span], mentions: Sequence[Mention]
) -> str | None:
    """The label of one category that the clause gives a figure: its own attached
    label; otherwise the label the clause states for all its figures (one distinct
    unattached mention), otherwise the nearest unattached one; None if the clause
    names none."""
    own = [m for m in mentions if _attached(clause, m, figure, figures)]
    if own:
        return _nearest(own, figure)
    free = [
        m for m in mentions if not any(_attached(clause, m, other, figures) for other in figures)
    ]
    distinct = {label for _, _, label in free}
    if len(distinct) == 1:
        return distinct.pop()
    return _nearest(free, figure)


def check_labels(answer: str, pages: Sequence[PageText]) -> list[MislabelledNumber]:
    """The table figures of the answer whose labels fit no cell holding that value."""
    cells = _table_cells(pages)
    if not cells:
        return []
    categories = max(len(labels) for known in cells.values() for labels in known)
    vocabulary: list[set[str]] = [set() for _ in range(categories)]
    for known in cells.values():
        for labels in known:
            for position, label in enumerate(labels):
                vocabulary[position].add(label)
    # Citation markers and page references are blanked, not removed, so that
    # positions stay those of the answer.
    blanked = _PAGE_REFERENCE.sub(
        lambda m: " " * len(m.group()), _CITATION.sub(lambda m: " " * len(m.group()), answer)
    )
    reported: list[MislabelledNumber] = []
    seen: set[tuple[str, tuple[str, ...]]] = set()
    for s_start, s_end in _pieces(blanked, _SENTENCE_END):
        sentence = blanked[s_start:s_end]
        for c_start, c_end in _pieces(sentence, _CLAUSE_BREAK):
            clause = sentence[c_start:c_end]
            mentions = [_mentions(clause, labels) for labels in vocabulary]
            figures = [
                (m.start(), m.end())
                for m in _NUMBER.finditer(clause)
                if _is_worth_checking(m.group())
            ]
            for start, end in figures:
                number = clause[start:end]
                candidates = cells.get(_normalise(number))
                if not candidates:
                    continue
                given = [_label_for(clause, (start, end), figures, m) for m in mentions]
                if all(label is None for label in given):
                    continue
                if any(
                    all(
                        given[position] is None or given[position] == label
                        for position, label in enumerate(labels)
                    )
                    for labels in candidates
                ):
                    continue
                answer_labels = [label for label in given if label is not None]
                key = (number, tuple(answer_labels))
                if key not in seen:
                    seen.add(key)
                    reported.append(
                        MislabelledNumber(
                            number,
                            answer_labels,
                            [list(labels) for labels in candidates],
                            _tidy(answer[s_start:s_end]),
                        )
                    )
    return reported


def _pieces(text: str, boundary: re.Pattern[str]) -> list[Span]:
    """The non-blank stretches of the text between its boundaries, as spans."""
    pieces: list[Span] = []
    position = 0
    for match in boundary.finditer(text):
        pieces.append((position, match.start()))
        position = match.end()
    pieces.append((position, len(text)))
    return [(start, end) for start, end in pieces if text[start:end].strip()]


def _tidy(sentence: str) -> str:
    """The sentence as the reader saw it, without citation markers."""
    without = _PAGE_REFERENCE.sub(" ", _CITATION.sub(" ", sentence))
    return re.sub(r"\s+(?=[.,;:!?])", "", " ".join(without.split()))


_LABEL_NOTES = {
    "other": "Figures whose labels differ from the source table: {}.",
    "zh": "以下數字的標籤與原文表格不符：{}。",
}


def label_note(mislabelled: Sequence[MislabelledNumber], language: str) -> str:
    """What the reader is told after the answer when a figure's labels do not match."""
    if language == "zh":
        items = [
            f"{m.number}（答案：{'、'.join(m.answer_labels)}；原文："
            f"{' / '.join('、'.join(labels) for labels in m.source_labels)}）"
            for m in mislabelled
        ]
        return _LABEL_NOTES["zh"].format("；".join(items))
    items = [
        f"{m.number} (answer: {', '.join(m.answer_labels)}; source: "
        f"{' / '.join(', '.join(labels) for labels in m.source_labels)})"
        for m in mislabelled
    ]
    return _LABEL_NOTES["other"].format("; ".join(items))


_NOTES = {
    "other": "Numbers that could not be checked against the cited pages of the original text: {}.",
    "zh": "以下數字未能在引用的原文頁面中核對：{}。",
}


def check_note(unverified: Sequence[str], language: str) -> str:
    """What the reader is told after the answer when numbers could not be verified."""
    separator = "、" if language == "zh" else ", "
    return _NOTES[language].format(separator.join(unverified))
