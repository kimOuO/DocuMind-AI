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
    _CLAUSE_BREAK,
    _NUMBER,
    _PAGE_REFERENCE,
    _SENTENCE_END,
    Aliases,
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
# D75: words that state the numeric ordering of two figures need no definition of the
# metric; words that state a performance conclusion do.
_ORDERING_UP = re.compile(
    r"\b(?:higher|exceed\w*|above|rise\w*|rose|increas\w*|grow\w*|grew|larger|greater|"
    r"more\s+than)\b|高於|上升|增加",
    re.IGNORECASE,
)
_ORDERING_DOWN = re.compile(
    r"\b(?:lower|below|drop\w*|fall\w*|fell|declin\w*|decreas\w*|reduc\w*|smaller|"
    r"less\s+than|shrink\w*|shrank)\b|低於|下降|降低|減少",
    re.IGNORECASE,
)
_PERFORMANCE_UP = re.compile(
    r"\b(?:outperform\w*|better|improv\w*|surpass\w*|beat\w*|superior|gain\w*|"
    r"advantage\w*|stronger)\b|優於|勝過|提升|較好",
    re.IGNORECASE,
)
_PERFORMANCE_DOWN = re.compile(
    r"\b(?:underperform\w*|worse|degrad\w*|regress\w*|inferior|deteriorat\w*|weaker|"
    r"trail\w*|lag\w*\s+behind)\b|劣於|退步|較差",
    re.IGNORECASE,
)
_PAIR_BRIDGE = re.compile(r"\b(?:to|vs\.?|versus|against|→)\b|→", re.IGNORECASE)
_FROM = re.compile(r"\bfrom\s*$", re.IGNORECASE)


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
    # D75: where the direction came from ("caption"; "complementary shares; metric stated in
    # the sources"; "unknown"), and whether the table's pairs sum to 100% — an auxiliary
    # signal that on its own never decides the direction.
    direction_basis: str = "unknown"
    complementary: bool = False


def _stated(text: str) -> str:
    """The direction a text states for its metric, by generic measurement words."""
    higher = _HIGHER_IS_BETTER.search(text) is not None
    lower = _LOWER_IS_BETTER.search(text) is not None
    if higher and not lower:
        return "higher"
    if lower and not higher:
        return "lower"
    return "unknown"


def stated_direction(texts: Iterable[str]) -> str:
    """What the sources as a whole say about their metric: "higher", "lower" or "unknown"."""
    return _stated(" ".join(texts))


def _complementary(parsed: Sequence[tuple[tuple[str, ...], str, int]]) -> bool:
    """Whether the table's pairs of percentages sum to 100: an auxiliary signal only."""
    pairs: dict[tuple[str, str, int], list[float]] = {}
    for labels, value, block in parsed:
        if len(labels) == 3 and value.endswith("%"):
            number = _as_float(value)
            if number is not None:
                pairs.setdefault((labels[0], labels[1], block), []).append(number)
    sums = [sum(v) for v in pairs.values() if len(v) == 2]
    return len(sums) >= 2 and sum(1 for t in sums if abs(t - 100) <= 0.3) / len(sums) >= 0.8


def _direction(
    caption: str, rows: Iterable[str], complementary: bool, stated: str
) -> tuple[str, str]:
    """The direction of the table's metric and its basis: the caption's own words first;
    else complementary pairs together with a direction the sources state; else unknown."""
    own = _stated(" ".join([caption, *rows]))
    if own != "unknown":
        return own, "caption"
    if complementary and stated == "higher":
        return "higher", "complementary shares; metric stated in the sources"
    return "unknown", "unknown"


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


def _cells_from_text(
    text: str, source_index: int, page: int, stated: str = "unknown"
) -> list[MatrixCell]:
    caption, parsed = _parsed_cells(text)
    if not parsed:
        return []
    match = _CAPTION.match(caption)
    table = match.group(1).title() if match else f"table on page {page}"
    complementary = _complementary(parsed)
    direction, basis = _direction(
        caption, {labels[0] for labels, _, _ in parsed}, complementary, stated
    )
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
                basis,
                complementary,
            )
        )
    return cells


def build_matrix(sources: Sequence[tuple[int, RetrievedChunk]]) -> list[MatrixCell]:
    """Every figure of every table chunk among the numbered sources, with its labels. The
    sources' own text may state the metric's direction (D75)."""
    stated = stated_direction(chunk.text for _, chunk in sources)
    cells: list[MatrixCell] = []
    for index, chunk in sources:
        cells.extend(_cells_from_text(chunk.text, index, chunk.page, stated))
    return cells


def matrix_cells_of_pages(pages: Sequence[PageText]) -> list[MatrixCell]:
    """The matrix read from page texts (the cited pages of an answer, or the chunks of a
    summarised section), each table starting at its caption."""
    stated = stated_direction(page.text for page in pages)
    cells: list[MatrixCell] = []
    for page in pages:
        # A page may hold several tables; each caption starts one.
        current: list[str] = []
        for line in [*page.text.splitlines(), None]:
            if line is None or (_CAPTION.match(line.strip()) and current):
                if current:
                    cells.extend(_cells_from_text("\n".join(current), 0, page.page, stated))
                current = [] if line is None else [line]
            else:
                current.append(line)
    return cells


_matrix_cells_of_pages = matrix_cells_of_pages


_DIRECTION_PHRASE = {
    "higher": "higher is better",
    "lower": "lower is better",
    "unknown": "direction of the metric unknown — compare values as higher or lower, "
    "not as better or worse",
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
        head = members[0]
        basis = (
            "" if head.direction_basis in ("caption", "unknown") else f" ({head.direction_basis})"
        )
        lines = [f"{table} [{index}] (p. {head.page}), {_DIRECTION_PHRASE[head.direction]}{basis}:"]
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
            heading = f"{group} / {row}" if group else row
            lines.append(f"  {heading}: {shown}")
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


_ALIAS_STOP = re.compile(
    r"^(?:and|or|which|that|while|whereas|but|to|in|for|from|with|by|as|so|if|when|than)$",
    re.IGNORECASE,
)
_ALIAS_WORD = re.compile(r"[A-Za-z][\w-]*")
_REMOVAL_VERB = r"(?:remov|eliminat|omit|exclud|dropp?|without|disabl)\w*"
_ONLY_VERB = r"(?:keep|keeps|keeping|kept|use|uses|using|used|retain\w*)\s+only"
_OPERATION_SPLIT = re.compile(
    rf"({_REMOVAL_VERB}|{_ONLY_VERB})\s+(?:the\s+|its\s+|any\s+|all\s+)?(?:use\s+of\s+(?:the\s+)?)?",
    re.IGNORECASE,
)


def method_aliases(definitions: Sequence[MethodDefinition]) -> dict[str, list[re.Pattern[str]]]:
    """Other ways a text may name a method, read from its definition: "the -High variant
    removes high-level retrieval" lets "removing high-level retrieval" count as -High. The
    operation's object (up to four words, to the next conjunction or punctuation) must
    follow the same kind of operation word; a name alone is never inferred."""
    aliases: dict[str, list[re.Pattern[str]]] = {}
    for d in definitions:
        for match in _OPERATION_SPLIT.finditer(d.sentence):
            rest = d.sentence[match.end() :]
            words: list[str] = []
            for token in re.split(r"\s+", rest):
                word = _ALIAS_WORD.match(token)
                if word is None or _ALIAS_STOP.match(word.group()) or len(words) == 4:
                    break
                words.append(word.group())
                if not token.endswith(word.group()):  # punctuation closes the object
                    break
            if not words:
                continue
            verb = (
                _ONLY_VERB if re.search(r"only$", match.group(1), re.IGNORECASE) else _REMOVAL_VERB
            )
            body = r"[\s-]+".join(re.escape(w).replace(r"\-", "[-\\s]") for w in words)
            pattern = re.compile(
                rf"{verb}\s+(?:the\s+|its\s+|any\s+|all\s+)?(?:use\s+of\s+(?:the\s+)?)?{body}(?!\w)",
                re.IGNORECASE,
            )
            aliases.setdefault(d.method, []).append(pattern)
    return aliases


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
missing. Where a table's direction is marked unknown, say only which figure is higher or lower; \
do not call either better, worse, improved or degraded. You may begin with a compact comparison \
table of the figures you use, then the analysis. Do not describe these steps, and do not number \
your paragraphs after them; write the answer as prose.
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
    kind: str = "ordering"  # "ordering" (numeric size) | "performance" (needs the direction)
    cue: str = ""  # the word that states the relation
    cue_span: tuple[int, int] = (0, 0)  # where the cue is in the answer
    first_is_up: bool | None = None  # what the figures say: the first is the larger


def _blank(answer: str) -> str:
    return _PAGE_REFERENCE.sub(
        lambda m: " " * len(m.group()), _CITATION.sub(lambda m: " " * len(m.group()), answer)
    ).replace("*", " ")


def _resolve(
    side: str,
    scopes: Sequence[str],
    vocabulary: Sequence[set[str]],
    value: str,
    cells: Sequence[MatrixCell],
    aliases: Aliases | None,
) -> MatrixCell | None:
    """The one cell with this value whose labels the side of the clause names: for each
    kind of label, the single mention on that side, else the single mention in the clause,
    then in the sentence; two mentions on the side are an ambiguity, not a choice. When the
    inferred column fits no cell, the row and group alone may still name one cell."""
    given: list[str | None] = []
    for labels in vocabulary:
        on_side = {label for _, _, label in _mentions(side, labels, aliases)}
        if len(on_side) > 1:
            return None
        if len(on_side) == 1:
            given.append(on_side.pop())
            continue
        found = None
        for scope in scopes:
            in_scope = {label for _, _, label in _mentions(scope, labels, aliases)}
            if len(in_scope) == 1:
                found = in_scope.pop()
                break
            if len(in_scope) > 1:
                break
        given.append(found)
    row, group, column = given

    def fitting(use_column: bool) -> MatrixCell | None:
        matches = [
            c
            for c in cells
            if _key(c.value) == _key(value)
            and (row is None or c.row == row)
            and (group is None or c.group == group)
            and (not use_column or column is None or c.column == column)
        ]
        distinct = {(c.row, c.group, c.column, c.paired_with, c.direction) for c in matches}
        return matches[0] if len(distinct) == 1 else None

    return fitting(True) or (fitting(False) if column is not None else None)


def _comparable(left: MatrixCell, right: MatrixCell) -> str | None:
    """Why two cells cannot be compared, or None when they can: the same column group,
    and either the same row or the same column; and the same pairing — or each other's."""
    if left.group != right.group or (left.row == right.row) == (left.column == right.column):
        return (
            f"{left.group or left.table} / {left.row} / {left.column} against "
            f"{right.group or right.table} / {right.row} / {right.column}: different conditions"
        )
    each_others = left.paired_with == right.column and right.paired_with == left.column
    if left.paired_with != right.paired_with and not each_others:
        return (
            f"paired with {left.paired_with} against paired with {right.paired_with}: "
            "different pairings"
        )
    return None


def _cue_before(text: str) -> tuple[re.Match[str], str, bool] | None:
    """The last ordering or performance cue in the text, its kind and whether it says up."""
    found: list[tuple[int, re.Match[str], str, bool]] = []
    for pattern, kind, up in (
        (_ORDERING_UP, "ordering", True),
        (_ORDERING_DOWN, "ordering", False),
        (_PERFORMANCE_UP, "performance", True),
        (_PERFORMANCE_DOWN, "performance", False),
    ):
        for m in pattern.finditer(text):
            found.append((m.start(), m, kind, up))
    if not found:
        return None
    _, m, kind, up = max(found)
    return m, kind, up


def check_directions(
    answer: str, pages: Sequence[PageText], aliases: Aliases | None = None
) -> list[DirectionIssue]:
    """Comparisons of two figures in one clause checked against the matrix of the cited
    pages. Two forms: "A <cue> B" ("67.6% is higher than 65.2%", "A outperforms B"), and a
    change from the first figure to the second ("drops from A to B", "drops (A vs B)") with
    the cue before the pair. An ordering cue is checked by arithmetic alone; a performance
    cue needs the metric's direction and is uncertain without it. Figures of different
    conditions are incomparable."""
    cells = matrix_cells_of_pages(pages)
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
        clauses = _pieces(sentence, _CLAUSE_BREAK)
        figures = [m for m in _NUMBER.finditer(sentence) if _is_worth_checking(m.group())]
        for first, second in pairwise(figures):
            clause = next(
                (c for c in clauses if c[0] <= first.start() and second.end() <= c[1]), None
            )
            if clause is None:
                continue  # the two figures are in different clauses
            c_start, c_end = clause
            between = sentence[first.end() : second.start()]
            bridge = _PAIR_BRIDGE.search(between)
            inner = _cue_before(between)  # "A higher than B": the cue between the figures
            change = None
            if inner is None and bridge is not None and not _NUMBER.search(between):
                # "drops from A to B", "drops (A vs B)": the cue before the pair.
                before = sentence[c_start : first.start()]
                change = _cue_before(before)
                if change is not None and _FROM.search(before) is None and "(" not in before[-3:]:
                    # Without "from" or an opening parenthesis the pair is a plain "A vs B"
                    # comparison: the cue before it says which side is up, as "A <cue> B".
                    pass
            found = inner or change
            if found is None:
                continue
            cue_match, kind, says_up = found
            cue_offset = first.end() if inner is not None else c_start
            split = first.end() + (
                bridge.start() if inner is None and bridge else cue_match.start()
            )
            left_text = sentence[c_start:split]
            right_text = sentence[split:c_end]
            scopes = [sentence[c_start:c_end], sentence]
            left = _resolve(left_text, scopes, vocabulary, first.group(), cells, aliases)
            right = _resolve(right_text, scopes, vocabulary, second.group(), cells, aliases)
            if left is None or right is None:
                continue
            # "drops (A vs B) for X": the cue is about the clause's subject X, whichever
            # side of the pair X's figure is on. Without one named subject — or with
            # "from A to B" — the pair reads as a change from the first to the second.
            subject_first: bool | None = None
            if inner is None and _FROM.search(sentence[c_start : first.start()]) is None:
                outside = sentence[c_start : first.start()] + " " + sentence[second.end() : c_end]
                subjects = {label for _, _, label in _mentions(outside, vocabulary[2], aliases)}
                if len(subjects) == 1:
                    subject = subjects.pop()
                    if (left.column == subject) != (right.column == subject):
                        subject_first = left.column == subject
            shown = _tidy(answer[s_start:s_end])
            cue_span = (
                s_start + cue_offset + cue_match.start(),
                s_start + cue_offset + cue_match.end(),
            )
            cue = cue_match.group()
            reason = _comparable(left, right)
            if reason is not None:
                issues.append(
                    DirectionIssue(
                        shown,
                        first.group(),
                        second.group(),
                        "incomparable",
                        reason,
                        kind,
                        cue,
                        cue_span,
                    )
                )
                continue
            a, b = _as_float(first.group()), _as_float(second.group())
            if a is None or b is None or a == b:
                continue
            first_is_up = a > b
            # What the sentence says about the first figure: in "A <cue> B" the cue is about
            # A; in a change from A to B an upward cue means B is up, so A is down; with a
            # named subject the cue is about the subject's figure.
            if inner is not None:
                first_said_up = says_up
            elif subject_first is not None:
                first_said_up = says_up if subject_first else not says_up
            else:
                first_said_up = not says_up
            if kind == "performance":
                if left.direction == "unknown":
                    issues.append(
                        DirectionIssue(
                            shown,
                            first.group(),
                            second.group(),
                            "uncertain",
                            f"the direction of {left.row} is not stated in the sources, so "
                            f'"{cue}" cannot be checked; the figures only say that '
                            f"{first.group()} is {'higher' if first_is_up else 'lower'}",
                            kind,
                            cue,
                            cue_span,
                            first_is_up,
                        )
                    )
                    continue
                first_said_up = first_said_up if left.direction == "higher" else not first_said_up
            if first_said_up != first_is_up:
                issues.append(
                    DirectionIssue(
                        shown,
                        first.group(),
                        second.group(),
                        "inconsistent",
                        f"{left.row} / {left.group or left.table}: {first.group()} "
                        f"{'>' if first_is_up else '<'} {second.group()}"
                        + (
                            f", {_DIRECTION_PHRASE[left.direction]}"
                            if kind == "performance"
                            else ""
                        )
                        + f', but the sentence says "{cue}"',
                        kind,
                        cue,
                        cue_span,
                        first_is_up,
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
