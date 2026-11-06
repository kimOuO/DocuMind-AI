"""Structured evidence analysis (D74): the parts without a model or a database.

The chunker rewrites a table cell by cell ("Overall — Agriculture: NaiveRAG 35.2%, -High
64.8%; …", tables.py), so every figure of a table chunk already carries its row (the
metric), its column group (the dataset or condition) and its column (the method or
system). The Evidence Matrix here is that structure read back: one cell per figure,
with the column it is paired with in the same block of the table, the unit, the
direction of the metric when the caption says it ("win rate" is higher-is-better; an
unknown metric stays unknown) and the source that holds the table. A table the chunker
did not rewrite (no rows recognised) has no cells: the Analyst then reads the text.

Method definitions are sentences of the sources that name a column of the matrix and
an operation on it (removes, without, keeps only …); a name alone defines nothing.

Two deterministic checks use the matrix: whether a comparison of two figures in one
sentence goes the way the figures go (only when both figures resolve to cells of the
same dataset, metric and pairing, and the metric's direction is known), and whether an
answer to a question about the variants of a method compares every variant under one
dataset and metric — a requirement only when the tables show such variants. Nothing
here knows any paper in particular.
"""

import re
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from itertools import pairwise

from app.chat.verification import (
    _CITATION,
    _NUMBER,
    _PAGE_REFERENCE,
    _SENTENCE_END,
    NumberCheck,
    PageText,
    _is_worth_checking,
    _key,
    _label_pattern,
    _mentions,
    _pieces,
    _tidy,
    numbers_in,
)
from app.ingestion.tables import cells_of
from app.llm.tokenizer import TokenCounter
from app.retrieval.repository import RetrievedChunk

MATRIX_TOKEN_BUDGET = 900  # tokens the matrix and the definitions may add to the prompt
_CAPTION = re.compile(r"^\s*(Table\s+\d+)\s*[.:]\s*(.*)$", re.IGNORECASE)
# Generic measurement words that say which way a metric goes; anything else is unknown.
_HIGHER_IS_BETTER = re.compile(
    r"win\s*rates?|accuracy|\bf1\b|recall|precision|\bscores?\b|\bbleu\b|\brouge\b|\bauc\b|success",
    re.IGNORECASE,
)
_LOWER_IS_BETTER = re.compile(r"\berrors?\b|\bloss\b|perplexity|latency", re.IGNORECASE)
_OPERATION = re.compile(
    r"\b(?:remov|eliminat|omit|without|disabl|dropp?|replac|exclud|ablat|w/o)"
    r"|\b(?:keep|keeps|keeping|use|uses|using)\s+only\b",
    re.IGNORECASE,
)
_SENTENCE = re.compile(r"(?<=[.!?])\s+")
_ABLATION_QUESTION = re.compile(r"ablat|variant|消融|變體", re.IGNORECASE)
# A column that is a variant of the method it is paired with: "-High", "w/o text".
_VARIANT_LABEL = re.compile(r"^(?:[-–]\w|w/o\b|without\b)", re.IGNORECASE)
_POSITIVE_CUE = re.compile(
    r"\b(?:outperform\w*|better|higher|exceed\w*|surpass\w*|improv\w*|above|beat\w*|"
    r"rise\w*|rose|increas\w*|grow\w*|gain\w*)\b|優於|勝過|高於|超過|提升",
    re.IGNORECASE,
)
_NEGATIVE_CUE = re.compile(
    r"\b(?:worse|lower|below|drop\w*|fall\w*|fell|declin\w*|decreas\w*|reduc\w*|underperform\w*)\b"
    r"|低於|劣於|下降|降低",
    re.IGNORECASE,
)
_FROM = re.compile(r"\bfrom\s*$", re.IGNORECASE)
_TO = re.compile(r"\bto\b", re.IGNORECASE)


# --- the matrix ------------------------------------------------------------------------


@dataclass(frozen=True)
class MatrixCell:
    source_index: int  # the numbered source that holds the table
    page: int
    table: str  # "Table 2", or "table on page 8" when the caption has no number
    group: str  # column group: the dataset or condition
    row: str  # row label: the metric or item
    column: str  # the column: a method, system or measure
    paired_with: str | None  # the other column of the same pair in this block, if a pair
    block: int  # which block of the table (rows that come round again start a new one)
    value: str
    unit: str  # "%" or ""
    direction: str  # "higher" | "lower" | "unknown": which way the metric is better


def _direction(caption: str, rows: Iterable[str]) -> str:
    text = " ".join([caption, *rows])
    higher = _HIGHER_IS_BETTER.search(text) is not None
    lower = _LOWER_IS_BETTER.search(text) is not None
    if higher and not lower:
        return "higher"
    if lower and not higher:
        return "lower"
    return "unknown"


def _parsed_cells(text: str) -> tuple[str, list[tuple[tuple[str, ...], str, int]]]:
    """The caption line and (labels, value, block) of every cell the chunker wrote."""
    lines = text.splitlines()
    caption = lines[0].strip() if lines and _CAPTION.match(lines[0].strip()) else ""
    cells: list[tuple[tuple[str, ...], str, int]] = []
    block = 0
    seen_in_block: set[tuple[str, str]] = set()
    for line in lines:
        row = cells_of(line)
        if not row:
            continue
        keys = {(labels[0], labels[1]) for _, labels in row if len(labels) >= 2}
        if keys & seen_in_block:
            block += 1
            seen_in_block = set()
        for value, labels in row:
            cells.append((labels, value, block))
        seen_in_block |= keys
    return caption, cells


def _cells_from_text(text: str, source_index: int, page: int) -> list[MatrixCell]:
    caption, parsed = _parsed_cells(text)
    if not parsed:
        return []
    match = _CAPTION.match(caption)
    table = match.group(1).title() if match else f"table on page {page}"
    direction = _direction(caption, {labels[0] for labels, _, _ in parsed})
    # The columns that share a row, group and block pair up when there are two of them.
    groups: dict[tuple[str, str, int], list[str]] = {}
    for labels, _, block in parsed:
        if len(labels) == 3:
            groups.setdefault((labels[0], labels[1], block), []).append(labels[2])
    cells = []
    for labels, value, block in parsed:
        row, group = labels[0], labels[1] if len(labels) >= 2 else ""
        column = labels[2] if len(labels) == 3 else labels[1]
        partners = groups.get((row, group, block), [])
        paired = partners[1 - partners.index(column)] if len(partners) == 2 else None
        cells.append(
            MatrixCell(
                source_index,
                page,
                table,
                group if len(labels) == 3 else "",
                row,
                column,
                paired,
                block,
                value,
                "%" if value.endswith("%") else "",
                direction,
            )
        )
    return cells


def build_matrix(sources: Sequence[tuple[int, RetrievedChunk]]) -> list[MatrixCell]:
    """Every figure of every table chunk among the numbered sources, with its labels."""
    cells: list[MatrixCell] = []
    for index, chunk in sources:
        cells.extend(_cells_from_text(chunk.text, index, chunk.page))
    return cells


def _matrix_cells_of_pages(pages: Sequence[PageText]) -> list[MatrixCell]:
    cells: list[MatrixCell] = []
    for page in pages:
        # A page may hold several tables; each caption starts one.
        current: list[str] = []
        for line in [*page.text.splitlines(), None]:
            if line is None or (_CAPTION.match(line.strip()) and current):
                if current:
                    cells.extend(_cells_from_text("\n".join(current), 0, page.page))
                current = [] if line is None else [line]
            else:
                current.append(line)
    return cells


_DIRECTION_PHRASE = {
    "higher": "higher is better",
    "lower": "lower is better",
    "unknown": "direction of the metric unknown",
}


def matrix_text(
    cells: Sequence[MatrixCell], counter: TokenCounter, *, budget: int
) -> tuple[str, list[str]]:
    """The matrix table by table, each row of it one dataset and metric with the pairs of
    that row in block order; tables that do not fit the budget whole are left out and
    named."""
    by_table: dict[tuple[str, int], list[MatrixCell]] = {}
    for c in cells:
        by_table.setdefault((c.table, c.source_index), []).append(c)
    blocks: list[str] = []
    left_out: list[str] = []
    spent = 0
    for (table, index), members in by_table.items():
        lines = [
            f"{table} [{index}] (p. {members[0].page}), {_DIRECTION_PHRASE[members[0].direction]}:"
        ]
        order: dict[tuple[str, str], list[MatrixCell]] = {}
        for c in members:
            order.setdefault((c.group, c.row), []).append(c)
        for (group, row), group_cells in order.items():
            pairs: dict[int, list[MatrixCell]] = {}
            for c in group_cells:
                pairs.setdefault(c.block, []).append(c)
            shown = "; ".join(
                " | ".join(f"{c.column} {c.value}" for c in pair) for pair in pairs.values()
            )
            head = f"{group} / {row}" if group else row
            lines.append(f"  {head}: {shown}")
        block = "\n".join(lines)
        cost = counter.count(block)
        if spent + cost > budget:
            left_out.append(f"{table} [{index}]")
            continue
        blocks.append(block)
        spent += cost
    return "\n".join(blocks), left_out


# --- method definitions ----------------------------------------------------------------


@dataclass(frozen=True)
class MethodDefinition:
    method: str
    sentence: str
    source_index: int
    page: int


def method_definitions(
    sources: Sequence[tuple[int, RetrievedChunk]], methods: Iterable[str]
) -> list[MethodDefinition]:
    """For each method (a column of the matrix), the first sentence of the sources that
    names it together with an operation on it (removes, without, keeps only …). A
    sentence that merely names the method defines nothing."""
    wanted = sorted({m for m in methods if m.strip()}, key=len, reverse=True)
    found: dict[str, tuple[int, MethodDefinition]] = {}
    position = 0
    for index, chunk in sources:
        for raw in _SENTENCE.split(" ".join(chunk.text.split())):
            position += 1
            sentence = raw.strip()
            if not sentence or _OPERATION.search(sentence) is None:
                continue
            for method in wanted:
                if method not in found and _label_pattern(method).search(sentence):
                    found[method] = (
                        position,
                        MethodDefinition(method, sentence, index, chunk.page),
                    )
    return [d for _, d in sorted(found.values(), key=lambda pair: pair[0])]


# --- the Analyst's preamble ------------------------------------------------------------


ANALYSIS_ORDER = """\
Answer in this order: (1) say what the question asks for — which methods, datasets and \
metrics; (2) read the evidence matrix and the method definitions; (3) compare only figures \
that share the same dataset, the same metric and the same pairing — never a figure of one \
dataset, metric or pairing with one of another, and never treat two methods' separate scores \
against a reference as a test between those two methods; (4) name the improvements, the \
regressions and every exception; (5) check that each "higher", "lower", "outperforms" or \
"drops" agrees with the figures it stands next to; (6) cite the table's source for a figure \
and the defining passage for a definition; (7) check that nothing the question asks for is \
missing. You may begin with a compact comparison table of the figures you use, then the \
analysis. Do not describe these steps; write the answer.
"""


def analysis_preamble(
    cells: Sequence[MatrixCell],
    definitions: Sequence[MethodDefinition],
    counter: TokenCounter,
    *,
    budget: int,
) -> str:
    """What goes before the answering instructions in the navigate mode (D74): the matrix,
    the definitions found (and the methods with none), and the order of analysis."""
    parts = [
        "Structured evidence, read from the numbered sources below (read it before answering).\n"
    ]
    text, left_out = matrix_text(cells, counter, budget=budget) if cells else ("", [])
    if text:
        parts.append(
            "Evidence matrix — each figure with its dataset / metric, its column and, after "
            '"|", the column it is paired with in the same row of the table; [n] is the '
            "source that holds the table:\n" + text
        )
        if left_out:
            parts.append(
                "Tables left out of the matrix for room (read them in the sources): "
                + ", ".join(left_out)
            )
    else:
        parts.append(
            "No structured table data could be read from the sources: take every figure "
            "from the source text with the labels written there."
        )
    methods = sorted({c.column for c in cells})
    if methods or definitions:
        lines = [
            "Method definitions found in the sources (a method with none may only be "
            "described by quoting the source, never from its name):"
        ]
        defined = {d.method: d for d in definitions}
        for method in methods or sorted(defined):
            d = defined.get(method)
            if d is None:
                lines.append(f"- {method}: no definition found in the sources")
            else:
                lines.append(f"- {method} [{d.source_index}]: {d.sentence}")
        parts.append("\n".join(lines))
    parts.append(ANALYSIS_ORDER)
    return "\n\n".join(parts) + "\n"


# --- the direction check ---------------------------------------------------------------


@dataclass(frozen=True)
class DirectionIssue:
    sentence: str
    left: str  # the first figure
    right: str  # the second figure
    status: str  # "inconsistent" | "uncertain" | "incomparable"
    detail: str


def _blank(answer: str) -> str:
    return _PAGE_REFERENCE.sub(
        lambda m: " " * len(m.group()), _CITATION.sub(lambda m: " " * len(m.group()), answer)
    ).replace("*", " ")


def _resolve(
    side: str, whole: str, vocabulary: Sequence[set[str]], value: str, cells: Sequence[MatrixCell]
) -> MatrixCell | None:
    """The one cell with this value whose labels the side of the sentence names: for each
    kind of label, the single mention on that side, else the single mention in the whole
    sentence; two mentions on the side are an ambiguity, not a choice."""
    given: list[str | None] = []
    for labels in vocabulary:
        on_side = {label for _, _, label in _mentions(side, labels)}
        if len(on_side) == 1:
            given.append(on_side.pop())
        elif len(on_side) > 1:
            return None
        else:
            in_sentence = {label for _, _, label in _mentions(whole, labels)}
            given.append(in_sentence.pop() if len(in_sentence) == 1 else None)
    row, group, column = given
    fitting = [
        c
        for c in cells
        if _key(c.value) == _key(value)
        and (row is None or c.row == row)
        and (group is None or c.group == group)
        and (column is None or c.column == column)
    ]
    distinct = {(c.row, c.group, c.column, c.paired_with, c.direction) for c in fitting}
    return fitting[0] if len(distinct) == 1 else None


def check_directions(answer: str, pages: Sequence[PageText]) -> list[DirectionIssue]:
    """Comparisons of two figures in one sentence ("A outperforms B", "falls from A to
    B") checked against the matrix of the cited pages: inconsistent when the figures go
    the other way, uncertain when the metric's direction is unknown, incomparable when
    the figures are of different datasets, metrics or pairings."""
    cells = _matrix_cells_of_pages(pages)
    if not cells:
        return []
    vocabulary = [
        {c.row for c in cells},
        {c.group for c in cells if c.group},
        {c.column for c in cells},
    ]
    blanked = _blank(answer)
    issues: list[DirectionIssue] = []
    for s_start, s_end in _pieces(blanked, _SENTENCE_END):
        sentence = blanked[s_start:s_end]
        figures = [m for m in _NUMBER.finditer(sentence) if _is_worth_checking(m.group())]
        for first, second in pairwise(figures):
            between = sentence[first.end() : second.start()]
            from_to = _FROM.search(sentence[: first.start()]) is not None and _TO.search(between)
            cue_text = sentence[: second.start()] if from_to else between
            positive = _POSITIVE_CUE.search(cue_text)
            negative = _NEGATIVE_CUE.search(cue_text)
            if positive is None and negative is None:
                continue
            split = (
                first.end() + _TO.search(between).start()  # type: ignore[union-attr]
                if from_to
                else first.end() + (positive or negative).start()  # type: ignore[union-attr]
            )
            left = _resolve(sentence[:split], sentence, vocabulary, first.group(), cells)
            right = _resolve(sentence[split:], sentence, vocabulary, second.group(), cells)
            if left is None or right is None:
                continue
            shown = _tidy(answer[s_start:s_end])
            # Comparable: the same column group, and the same row or the same column (a
            # table may put the methods in its rows or in its columns).
            same_group = left.group == right.group
            one_axis = (left.row == right.row) != (left.column == right.column)
            if not same_group or not one_axis:
                issues.append(
                    DirectionIssue(
                        shown,
                        first.group(),
                        second.group(),
                        "incomparable",
                        f"{first.group()} is {left.group or left.table} / {left.row} / "
                        f"{left.column}, {second.group()} is {right.group or right.table} / "
                        f"{right.row} / {right.column}: different conditions",
                    )
                )
                continue
            if left.paired_with != right.paired_with:
                issues.append(
                    DirectionIssue(
                        shown,
                        first.group(),
                        second.group(),
                        "incomparable",
                        f"{first.group()} is paired with {left.paired_with}, "
                        f"{second.group()} with {right.paired_with}: different pairings",
                    )
                )
                continue
            if left.direction == "unknown":
                issues.append(
                    DirectionIssue(
                        shown,
                        first.group(),
                        second.group(),
                        "uncertain",
                        f"the direction of {left.row} is not known, so the comparison "
                        "cannot be checked",
                    )
                )
                continue
            a, b = _as_float(first.group()), _as_float(second.group())
            if a is None or b is None or a == b:
                continue
            # Which figure the sentence says is better: normally the first ("A better than
            # B"); in "falls from A to B" the first, in "rises from A to B" the second.
            first_is_better = (negative is not None) if from_to else (positive is not None)
            better_is_higher = left.direction == "higher"
            first_higher = a > b
            consistent = (first_higher == better_is_higher) == first_is_better
            if not consistent:
                issues.append(
                    DirectionIssue(
                        shown,
                        first.group(),
                        second.group(),
                        "inconsistent",
                        f"{left.row} / {left.group or left.table}: "
                        f"{_DIRECTION_PHRASE[left.direction]}, but {first.group()} "
                        f"{'>' if first_higher else '<'} {second.group()}",
                    )
                )
    return issues


def _as_float(value: str) -> float | None:
    try:
        return float(value.replace(",", "").rstrip("%"))
    except ValueError:
        return None


# --- completeness ----------------------------------------------------------------------


@dataclass(frozen=True)
class Completeness:
    status: str  # "complete" | "incomplete" | "not_applicable"
    required: list[str]  # the methods the answer should compare
    missing: list[str]  # required methods the answer gives no figure of at all
    condition: str | None  # the "dataset / metric" under which every method is given


def check_completeness(question: str, answer: str, pages: Sequence[PageText]) -> Completeness:
    """For a question about the variants of a method, whether the answer gives, under one
    dataset and metric, a figure of every variant the tables show (and of every method
    the question names). Not a requirement for other questions, nor without such tables."""
    cells = _matrix_cells_of_pages(pages)
    columns = sorted({c.column for c in cells})
    variants = [c for c in columns if _VARIANT_LABEL.match(c)]
    if not cells or not _ABLATION_QUESTION.search(question) or len(variants) < 2:
        return Completeness("not_applicable", [], [], None)
    named = [c for c in columns if _label_pattern(c).search(question)]
    required = sorted(set(variants) | set(named))
    figures = {_key(n) for n in numbers_in(answer)}
    conditions: dict[tuple[str, str, str], dict[str, set[str]]] = {}
    for c in cells:
        if c.column in required:
            conditions.setdefault((c.table, c.group, c.row), {}).setdefault(c.column, set()).add(
                _key(c.value)
            )
    for (_table, group, row), by_method in conditions.items():
        if all(by_method.get(m, set()) & figures for m in required):
            return Completeness("complete", required, [], f"{group} / {row}" if group else row)
    # A method counts as given when the answer names it and carries one of its figures;
    # a figure alone may belong to another method with the same value.
    given = {
        c.column
        for c in cells
        if c.column in required
        and _key(c.value) in figures
        and _label_pattern(c.column).search(answer)
    }
    return Completeness("incomplete", required, [m for m in required if m not in given], None)


def overall_status(
    check: NumberCheck, directions: Sequence[DirectionIssue], completeness: Completeness
) -> str:
    """The four-way summary the checks can stand behind: a factual error found; no error
    but a required comparison missing; every required comparison given and no error; or
    nothing the checks could vouch for."""
    wrong = (
        bool(check.mislabelled)
        or any(c.status == "contradicted" for c in check.overstated)
        or any(d.status == "inconsistent" for d in directions)
    )
    if wrong:
        return "FACTUALLY_INCORRECT"
    if completeness.status == "incomplete":
        return "FACTUALLY_CORRECT_BUT_INCOMPLETE"
    if completeness.status == "complete":
        return "SUPPORTED_AND_COMPLETE"
    return "UNCERTAIN"
