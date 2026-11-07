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
    label_outcomes,
    numbers_in,
)
from app.ingestion.tables import cells_of
from app.llm.tokenizer import TokenCounter
from app.retrieval.repository import RetrievedChunk

# Tokens the matrix may add to the prompt. One full results table of a paper (four
# datasets × four metrics × four baseline blocks, 128 cells) costs about 1,350 tokens in the
# matrix form; the budget must hold one such table whole. Until 2026-11-07 it was 900, so
# for every question that needed such a table the matrix was left out and the model saw only
# the source text (found by tracing a run; see ADR 0009). Reserved out of the navigate mode's
# evidence budget, so the call stays within the context limit.
MATRIX_TOKEN_BUDGET = 1_500
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
_PRONOUN_SUBJECT = re.compile(r"^\s*(?:It|This|That|They|These|Those)\b", re.IGNORECASE)


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
    # B5 baseline (2026-11-07, user's decision): the B3 wording. The D75 wording was
    # "direction of the metric unknown — compare values as higher or lower, not as better
    # or worse".
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
        head = members[0]
        # B5 baseline: the direction's basis is kept for the checks, not shown to the model
        # (D75 appended it as " (complementary; stated)"; B3 did not).
        lines = [f"{table} [{index}] (p. {head.page}), {_DIRECTION_PHRASE[head.direction]}:"]
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


# The B3 wording with step (2) reading definitions from the sources (D84, after B8 showed
# D79's counted-conclusion wording harmful). The earlier wordings (B3, D75, D79) are kept
# for the record in evaluation/navigator-abc/README.md, not here.
ANALYSIS_ORDER = """\
Answer in this order: (1) say what the question asks for — which methods, datasets and \
metrics; (2) read the evidence matrix and the passages of the sources that define each \
method or variant; (3) compare only figures that share the same dataset, the same metric \
and the same pairing — never a figure of one dataset, metric or pairing with one of another, \
and never treat two methods' separate scores against a reference as a test between those two \
methods; (4) name the improvements, the regressions and every exception; (5) check that each \
"higher", "lower", "outperforms" or "drops" agrees with the figures it stands next to; (6) \
cite the table's source for a figure and the defining passage for a definition; (7) check \
that nothing the question asks for is missing. You may begin with a compact comparison table \
of the figures you use, then the analysis. Do not describe these steps; write the answer.
"""


def analysis_preamble(
    cells: Sequence[MatrixCell],
    definitions: Sequence[MethodDefinition],
    counter: TokenCounter,
    *,
    budget: int,
    facts: Sequence["Fact"] = (),
) -> str:
    """What goes before the answering instructions in the navigate mode (D74): the matrix and
    the order of analysis. `definitions` is accepted for the callers' convenience and no
    longer rendered (D79)."""
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
    elif left_out:
        parts.append(
            "The tables in the sources were too large for the matrix (read them in the "
            "sources, keeping each figure with the pairing written on its row): "
            + ", ".join(left_out)
        )
    else:
        parts.append(
            "No structured table data could be read from the sources: take every figure "
            "from the source text with the labels written there."
        )
    # D79 (user's decision, 2026-11-07): the method definitions are no longer shown to the
    # model. The sentences the program finds depend on the wording of one paper (its verb
    # list was written from a single sentence), and a method it misses used to be announced
    # as "no definition found" although the sources defined it. The model reads the sources'
    # own defining passages instead (rule 7); the definitions still feed the checks' aliases.
    del definitions
    if facts:
        parts.append(
            "Verified comparison facts, computed from the matrix (a conclusion must agree "
            "with these counts; every condition listed as an exception must be named as "
            "one; an indirect comparison is a trend, not a proven difference):\n"
            + facts_text(facts, counter, budget=max(budget // 3, 150))
        )
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
    column: str | None = None,
) -> MatrixCell | None:
    """The one cell with this value whose labels the side of the clause names: for each
    kind of label, the single mention on that side, else the single mention in the clause,
    then in the sentence; two mentions on the side are an ambiguity, not a choice. When the
    inferred column fits no cell, the row and group alone may still name one cell."""
    given: list[str | None] = []
    for index, labels in enumerate(vocabulary):
        if index == 2 and column is not None:
            given.append(column)  # the column the sentence's structure assigns to this side
            continue
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
            subject_first: bool | None = None
            subject_note = ""
            forced: tuple[str | None, str | None] = (None, None)
            pair_form = inner is None and _FROM.search(sentence[c_start : first.start()]) is None
            if pair_form:
                before_pair = sentence[c_start : first.start()]
                after_pair = sentence[second.end() : c_end]
                before_mentions = _mentions(before_pair, vocabulary[2], aliases)
                named_before = list(dict.fromkeys(label for _, _, label in before_mentions))
                named_after = [
                    label for _, _, label in _mentions(after_pair, vocabulary[2], aliases)
                ]
                cue_at = cue_match.start() if change is not None else -1
                if (
                    len(named_before) == 2
                    and not named_after
                    and cue_at >= 0
                    and any(m[0] < cue_at for m in before_mentions)
                    and any(m[0] > cue_at for m in before_mentions)
                ):
                    # "S outperforms C in M (a vs b)": a is S's figure, b is C's.
                    forced = (named_before[0], named_before[1])
                    subject_first = True
                elif (
                    _PRONOUN_SUBJECT.match(before_pair)
                    and len(set(named_before + named_after)) == 1
                ):
                    # "It performs better (a vs b for X)": X owns one figure; the pronoun's
                    # figure is the other one. Which one is settled after resolution.
                    subject_note = (
                        " (the pronoun subject is read as the method the named one is not)"
                    )
            left = _resolve(left_text, scopes, vocabulary, first.group(), cells, aliases, forced[0])
            right = _resolve(
                right_text, scopes, vocabulary, second.group(), cells, aliases, forced[1]
            )
            if left is None or right is None:
                continue
            # "drops (A vs B) for X": the cue is about the clause's subject X, whichever
            # side of the pair X's figure is on. Without one named subject — or with
            # "from A to B" — the pair reads as a change from the first to the second.
            if pair_form and subject_first is None:
                outside = sentence[c_start : first.start()] + " " + sentence[second.end() : c_end]
                subjects = {label for _, _, label in _mentions(outside, vocabulary[2], aliases)}
                if len(subjects) == 1:
                    subject = subjects.pop()
                    if (left.column == subject) != (right.column == subject):
                        # With a pronoun subject the named method is the comparator, so the
                        # subject's figure is the other side.
                        is_left = left.column == subject
                        subject_first = (not is_left) if subject_note else is_left
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
                        + f', but the sentence says "{cue}"'
                        + subject_note,
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


def check_completeness(
    question: str, answer: str, pages: Sequence[PageText], aliases: Aliases | None = None
) -> Completeness:
    """For a question about the variants of a method, whether the answer gives, under one
    dataset and metric, each variant's figure *as that variant's* (a figure the label check
    ties to the method, D76) — a figure that merely equals another method's does not count.
    Figures the check cannot tie to any method leave the verdict uncertain. Not a
    requirement for other questions, nor without such tables."""
    cells = matrix_cells_of_pages(pages)
    columns = sorted({c.column for c in cells})
    variants = [c for c in columns if _VARIANT_LABEL.match(c)]
    if not cells or not _ABLATION_QUESTION.search(question) or len(variants) < 2:
        return Completeness("not_applicable", [], [], None)
    named = [c for c in columns if _label_pattern(c).search(question)]
    required = sorted(set(variants) | set(named))
    outcomes = label_outcomes(answer, pages, aliases)
    expressed: set[tuple[str, str, str]] = set()
    for o in outcomes:
        if o.status == "supported" and len(o.claim) >= 3:
            row, group, method = o.claim[0], o.claim[1], o.claim[2]
            if row and group and method in required:
                expressed.add((row, group, method))
    conditions: dict[tuple[str, str], set[str]] = {}
    for c in cells:
        if c.column in required:
            conditions.setdefault((c.row, c.group), set()).add(c.column)
    for (row, group), methods in conditions.items():
        if methods >= set(required) and all((row, group, m) in expressed for m in required):
            return Completeness("complete", required, [], f"{group} / {row}" if group else row)
    covered = {m for _, _, m in expressed}
    missing = [m for m in required if m not in covered]
    # A figure of a missing method that the answer carries without a label it could be
    # tied to: the check cannot say whether that method was given or not.
    loose = {_key(o.number) for o in outcomes if o.status in ("unresolved", "unchecked")}
    values = {m: {_key(c.value) for c in cells if c.column == m} for m in required}
    if missing and all(values[m] & loose for m in missing):
        return Completeness("uncertain", required, missing, None)
    return Completeness("incomplete", required, missing, None)


def overall_status(
    check: NumberCheck,
    directions: Sequence[DirectionIssue],
    completeness: Completeness,
    conclusions: Sequence["ConclusionIssue"] = (),
    arithmetic: Sequence["ArithmeticIssue"] = (),
) -> str:
    """The four-way summary the checks can stand behind: a factual error found; no error
    but a required comparison missing; every required comparison given and no error; or
    nothing the checks could vouch for."""
    wrong = (
        bool(check.mislabelled)
        or any(c.status == "contradicted" for c in check.overstated)
        or any(d.status == "inconsistent" for d in directions)
        or any(c.status == "contradicted" for c in conclusions)
        or any(a.status == "inconsistent" for a in arithmetic)
    )
    if wrong:
        return "FACTUALLY_INCORRECT"
    if completeness.status == "incomplete":
        return "FACTUALLY_CORRECT_BUT_INCOMPLETE"
    if completeness.status == "complete":
        return "SUPPORTED_AND_COMPLETE"
    return "UNCERTAIN"


# --- comparison facts (D76) --------------------------------------------------------------


@dataclass(frozen=True)
class Fact:
    """Two figures of one condition that may be compared: the same table, group and row,
    and either each other's pair in a block ("direct pair") or two columns each paired
    with the same reference in different blocks ("each against R" — a trend read across
    separate pairings, not a test between the two)."""

    method_a: str
    method_b: str
    group: str
    row: str
    value_a: str
    value_b: str
    relation: str  # GREATER | LESS | EQUAL | UNKNOWN (value_a against value_b)
    direction: str  # the metric's direction: higher | lower | unknown
    better: str | None  # the method the direction says is better; None if unknown or indirect
    setting: str
    confidence: str  # direct | indirect
    table: str
    source_index: int
    page: int


def _relation(a: str, b: str) -> str:
    x, y = _as_float(a), _as_float(b)
    if x is None or y is None:
        return "UNKNOWN"
    return "GREATER" if x > y else "LESS" if x < y else "EQUAL"


def comparison_facts(cells: Sequence[MatrixCell], question: str) -> list[Fact]:
    """The comparable pairs of the matrix that bear on the question: when the question
    names methods, the pairs involving them (the named method first); otherwise the direct
    pairs of every condition."""
    columns = sorted({c.column for c in cells})
    positions = {
        c: m.start() for c in columns if (m := _label_pattern(c).search(question)) is not None
    }
    named = sorted(positions, key=lambda c: positions[c])
    # D87: a question that names a group (dataset) or a row (metric) is about that condition
    # only — "the Overall win rate on CS" wants one fact, not every condition's (T3).
    named_groups = _named_labels({c.group for c in cells}, question)
    named_rows = _named_labels({c.row for c in cells}, question)
    by_condition: dict[tuple[str, int, str, str], list[MatrixCell]] = {}
    for c in cells:
        by_condition.setdefault((c.table, c.source_index, c.group, c.row), []).append(c)
    facts: list[Fact] = []
    seen: set[tuple[str, int, str, str, frozenset[str], str]] = set()

    def add(a: MatrixCell, b: MatrixCell, setting: str, confidence: str) -> None:
        key = (a.table, a.source_index, a.group, a.row, frozenset({a.column, b.column}), setting)
        if key in seen or a.column == b.column:
            return
        seen.add(key)
        # The named method, or the one named first in the question, is method_a.
        order = {m: i for i, m in enumerate(named)}
        if order.get(b.column, 99) < order.get(a.column, 99):
            a, b = b, a
        relation = _relation(a.value, b.value)
        better: str | None = None
        if confidence == "direct" and a.direction != "unknown" and relation in ("GREATER", "LESS"):
            higher_is_better = a.direction == "higher"
            better = a.column if (relation == "GREATER") == higher_is_better else b.column
        facts.append(
            Fact(
                a.column,
                b.column,
                a.group,
                a.row,
                a.value,
                b.value,
                relation,
                a.direction,
                better,
                setting,
                confidence,
                a.table,
                a.source_index,
                a.page,
            )
        )

    for members in by_condition.values():
        for c in members:
            if c.paired_with:
                partner = next(
                    (o for o in members if o.column == c.paired_with and o.block == c.block),
                    None,
                )
                if partner is not None:
                    add(c, partner, "direct pair", "direct")
        references = {c.paired_with for c in members if c.paired_with}
        for ref in sorted(r for r in references if r):
            against = [c for c in members if c.paired_with == ref and c.column != ref]
            for i, a in enumerate(against):
                for b in against[i + 1 :]:
                    if a.block != b.block:
                        add(a, b, f"each against {ref}", "indirect")
        # D87: a group of three or more columns in one row ("C0 C1 C2 C3 TS") pairs nothing;
        # its columns are compared only when the question names one of them, each named
        # column against the others of its row — the columns may be unlike measures
        # ("Mean 1", "Z-value"), so nothing is compared unasked.
        unpaired = [c for c in members if c.paired_with is None]
        for a in unpaired:
            if a.column in named:
                for b in unpaired:
                    if b.block == a.block and b.column != a.column:
                        add(a, b, "same row", "direct")
    if named:
        facts = [f for f in facts if f.method_a in named or f.method_b in named]
    if named_groups:
        facts = [f for f in facts if f.group in named_groups]
    if named_rows:
        facts = [f for f in facts if f.row in named_rows]
    return facts


def _named_labels(labels: Iterable[str], question: str) -> set[str]:
    """The table labels the question mentions as whole words (a label of a letter or two,
    or a bare number such as a threshold, is not looked for: too easy to hit by chance)."""
    found = set()
    for label in labels:
        if len(label) < 3 or not any(ch.isalpha() for ch in label):
            continue
        if _label_pattern(label).search(question) is not None:
            found.add(label)
    return found


def facts_text(facts: Sequence[Fact], counter: TokenCounter, *, budget: int) -> str:
    """The facts summarised per pair of methods and setting: how often the first is
    higher, lower or equal, and the conditions that go the other way (the exceptions),
    with the limits of the comparison."""
    groups: dict[tuple[str, str, str], list[Fact]] = {}
    for f in facts:
        groups.setdefault((f.method_a, f.method_b, f.setting), []).append(f)
    lines: list[str] = []
    spent = 0
    for (a, b, setting), members in groups.items():
        higher = [f for f in members if f.relation == "GREATER"]
        lower = [f for f in members if f.relation == "LESS"]
        equal = [f for f in members if f.relation == "EQUAL"]
        total = len(members)
        minority = lower if len(lower) <= len(higher) else higher
        word = "lower" if minority is lower else "higher"
        direction = members[0].direction
        limits = []
        if members[0].confidence == "indirect":
            limits.append(
                f"{setting}: figures from separate pairings — a trend, not a test between the two"
            )
        else:
            limits.append(setting)
        if direction == "unknown":
            limits.append("direction of the metric not stated: higher is not known to be better")
        else:
            limits.append(f"{direction} is better")
        head = (
            f"- {a} vs {b} ({'; '.join(limits)}): {a} higher in {len(higher)} of {total} "
            f"conditions, lower in {len(lower)}"
            + (f", equal in {len(equal)}" if equal else "")
            + "."
        )
        if minority:
            shown = "; ".join(
                f"{f.group + ' / ' if f.group else ''}{f.row}: {f.value_a} vs {f.value_b}"
                f"{_delta(f.value_a, f.value_b)}"
                for f in minority[:6]
            )
            head += f" {a} {word} in: {shown}" + ("; …" if len(minority) > 6 else "") + "."
        cost = counter.count(head)
        if spent + cost > budget:
            lines.append(f"- {a} vs {b}: left out for room.")
            continue
        lines.append(head)
        spent += cost
    return "\n".join(lines)


def _delta(a: str, b: str) -> str:
    """The difference of two figures, as the program computes it: percentage points for
    percentages (and the relative change), a plain difference otherwise (D87 A3.4)."""
    x, y = _as_float(a), _as_float(b)
    if x is None or y is None or y == 0:
        return ""
    diff = x - y
    if a.endswith("%") and b.endswith("%"):
        return f" ({diff:+.1f} pp, {diff / y * 100:+.1f}% relative)"
    return f" ({diff:+g})"


FACTS_INTRODUCTION = (
    "Comparison facts computed by the program from the tables among the sources (each fact "
    "gives the two figures as written, which is higher, whether the metric's higher is "
    "better, the difference, and every condition that goes the other way). A conclusion must "
    "agree with these counts and name every exception listed; an indirect comparison is a "
    "trend, not a result:"
)
# D87: a sentence sending the model to the text passages for what each method or variant is
# was tried (C1, 2026-11-07) and reverted: Q3 lost its definitions altogether and Q2 gained a
# wrong indirect comparison; A1's wording above is the one kept.


def facts_block(facts: Sequence["Fact"], counter: TokenCounter, *, budget: int) -> str:
    """The facts as a block of the prompt, or "" when there are none (D87 experiment A)."""
    if not facts:
        return ""
    return FACTS_INTRODUCTION + "\n" + facts_text(facts, counter, budget=budget) + "\n\n"


def named_columns(cells: Sequence[MatrixCell], question: str) -> list[str]:
    """The table columns the question names, in the order it names them."""
    columns = sorted({c.column for c in cells})
    positions = {
        c: m.start() for c in columns if (m := _label_pattern(c).search(question)) is not None
    }
    return sorted(positions, key=lambda c: positions[c])


def minimal_table_text(
    cells: Sequence[MatrixCell], caption: str, named: Sequence[str]
) -> str | None:
    """A table chunk reduced to the rows of the compared columns (D87 experiment A2): the
    caption, a note, then — in the same cell-by-cell form the chunker writes, so the chunk
    still reads as a table — only the pairs that involve the named columns: between them
    when two or more are named, every pair of the one column otherwise. None when the
    question names no column of this table: then nothing is replaced and no figure the
    model may need is lost."""
    wanted = [c for c in named if any(x.column == c for x in cells)]
    if not wanted:
        return None
    if len(wanted) >= 2:
        keep = [c for c in cells if c.column in wanted and c.paired_with in wanted]
    else:
        keep = [c for c in cells if c.column == wanted[0] or c.paired_with == wanted[0]]
    if not keep:
        return None
    lines = [
        caption,
        f"(Rows reduced by the program to the columns the question names: {', '.join(wanted)}; "
        "each pair is as the table pairs it. The full table is on the same page.)",
    ]
    # One block at a time, as the chunker wrote it: a header of the pair, then one line per
    # row with the groups of that row.
    blocks: dict[int, dict[str, dict[str, list[MatrixCell]]]] = {}
    for c in keep:
        blocks.setdefault(c.block, {}).setdefault(c.row, {}).setdefault(c.group, []).append(c)
    for block in sorted(blocks):
        rows = blocks[block]
        first = next(iter(next(iter(rows.values())).values()))
        pair = [first[0].column, first[0].paired_with or ""]
        lines.append(" ".join(name for name in pair * 2 if name))
        for row, groups in rows.items():
            segments = [
                (f"{group}: " if group else "")
                + ", ".join(f"{c.column} {c.value}" for c in members)
                for group, members in groups.items()
            ]
            lines.append(f"{row} — " + "; ".join(segments))
    return "\n".join(lines)


@dataclass(frozen=True)
class ConclusionIssue:
    sentence: str
    status: str  # contradicted | uncertain
    detail: str


_ONLY_EXCEPTION = re.compile(
    r"\b(?:the\s+)?only\s+exceptions?\b|\bthe\s+only\s+(?:case|dataset|metric|condition|category)\b"
    r"|唯一(?:的)?例外",
    re.IGNORECASE,
)
_NO_EXCEPTION = re.compile(
    r"\bno\s+exceptions?\b|\bwithout\s+exceptions?\b|\bno\s+(?:cases?|conditions?)\s+(?:where|in\s+which)"
    r"|沒有例外|無例外",
    re.IGNORECASE,
)


def check_conclusions(answer: str, facts: Sequence[Fact]) -> list[ConclusionIssue]:
    """Sentences that count the exceptions ("the only exception", "no exceptions") checked
    against the facts of the pair of methods the answer compares: the exceptions are the
    conditions where the method the answer puts first is lower."""
    if not facts:
        return []
    pairs = list(dict.fromkeys((f.method_a, f.method_b) for f in facts))
    blanked = _blank(answer)
    issues: list[ConclusionIssue] = []
    for s_start, s_end in _pieces(blanked, _SENTENCE_END):
        sentence = blanked[s_start:s_end]
        only = _ONLY_EXCEPTION.search(sentence) is not None
        none = _NO_EXCEPTION.search(sentence) is not None
        if not (only or none):
            continue
        # The pair: the one whose methods the answer mentions most; the first-mentioned leads.
        best: tuple[int, tuple[str, str], str] | None = None
        for a, b in pairs:
            mentions = _mentions(blanked, {a, b})
            if not mentions:
                continue
            leader = mentions[0][2]
            if best is None or len(mentions) > best[0]:
                best = (len(mentions), (a, b), leader)
        if best is None:
            continue
        _, (a, b), leader = best
        pair_facts = [f for f in facts if {f.method_a, f.method_b} == {a, b}]
        exceptions = [
            f
            for f in pair_facts
            if (f.relation == "LESS" and f.method_a == leader)
            or (f.relation == "GREATER" and f.method_b == leader)
        ]
        shown = _tidy(answer[s_start:s_end])
        listed = "; ".join(
            f"{f.group + ' / ' if f.group else ''}{f.row} ({f.value_a} vs {f.value_b})"
            for f in exceptions[:6]
        )
        if only and len(exceptions) != 1:
            issues.append(
                ConclusionIssue(
                    shown,
                    "contradicted",
                    f"the facts hold {len(exceptions)} conditions where {leader} is lower, "
                    f"not one: {listed or 'none'}",
                )
            )
        elif none and exceptions:
            issues.append(
                ConclusionIssue(
                    shown,
                    "contradicted",
                    f"the facts hold {len(exceptions)} conditions where {leader} is lower: "
                    f"{listed}",
                )
            )
    return issues


# --- derived arithmetic (D76) -------------------------------------------------------------


@dataclass(frozen=True)
class ArithmeticIssue:
    sentence: str
    stated: str  # the ratio as written, e.g. "9x"
    computed: float | None  # the ratio of the two base figures, when exactly two were found
    status: str  # inconsistent | unchecked
    detail: str


_RATIO = re.compile(r"(?<![\d.])(\d+(?:\.\d+)?)\s*(?:x|×|times)\b", re.IGNORECASE)
_RATIO_TOLERANCE = 0.05


def check_arithmetic(answer: str, pages: Sequence[PageText]) -> list[ArithmeticIssue]:
    """A ratio the answer states ("9x fewer", "49.09 times more") checked against the two
    base figures of the same sentence when exactly two are found on the cited pages;
    otherwise reported as unchecked, never as verified."""
    page_keys = {_key(n) for n in numbers_in(" ".join(p.text for p in pages))}
    blanked = _blank(answer)
    issues: list[ArithmeticIssue] = []
    for s_start, s_end in _pieces(blanked, _SENTENCE_END):
        sentence = blanked[s_start:s_end]
        ratios = list(_RATIO.finditer(sentence))
        if not ratios:
            continue
        ratio_spans = [(m.start(1), m.end(1)) for m in ratios]
        bases = []
        for m in _NUMBER.finditer(sentence):
            if any(a <= m.start() < b for a, b in ratio_spans) or m.group().endswith("%"):
                continue
            value = _as_float(m.group())
            if value is None or _key(m.group()) not in page_keys:
                continue
            bases.append(value)
        shown = _tidy(answer[s_start:s_end])
        for m in ratios:
            stated = m.group(0).strip()
            factor = float(m.group(1))
            if len(bases) != 2 or min(bases) == 0:
                issues.append(
                    ArithmeticIssue(
                        shown,
                        stated,
                        None,
                        "unchecked",
                        "the sentence does not carry exactly two figures found on the cited "
                        "pages to derive the ratio from",
                    )
                )
                continue
            computed = max(bases) / min(bases)
            if abs(computed - factor) / computed > _RATIO_TOLERANCE:
                issues.append(
                    ArithmeticIssue(
                        shown,
                        stated,
                        round(computed, 2),
                        "inconsistent",
                        f"{max(bases):g} / {min(bases):g} = {computed:.2f}, not {factor:g}",
                    )
                )
    return issues
