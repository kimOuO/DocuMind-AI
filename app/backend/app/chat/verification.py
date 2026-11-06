"""Checking the numbers in an answer against the original text of the cited pages (AC-26).

A summary answer is produced from summaries, two steps away from the text, so
every concrete number in it is looked up on the pages its cited sources cover.
A number is verified when the same value appears there, ignoring thousands
separators and a percent sign; the page and a snippet of the original text are
kept as evidence. A number that is not found is reported, never let through
silently. No LLM is involved.

A figure that is found may still be attributed wrongly: the model copies a
table value correctly and puts it under a neighbouring metric or variant (D64),
or on the wrong dataset (D67). Table chunks are written one row per line with
every figure next to its labels (app.ingestion.tables), so each table value is a
cell with known labels, and, where a row group pairs two columns, a known
comparator (the other cell). Every such figure in the answer is read as a claim:
the labels its sentence gives it, by role, never by distance. A label written
with the figure is its own; otherwise the one label of that kind the clause,
then the sentence, states; a method named right after "over", "against",
"compared to" and the like is the comparator, not the owner. The claim is
contradicted when no cell holding the value fits the labels it gives,
supported when a cell fits every label and none is missing, and otherwise
unresolved: the check does not guess, and says so.
"""

import re
import uuid
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from itertools import pairwise

from app.ingestion.tables import cells_of

# A number: with thousands separators, or plain; optional decimals; optional percent.
# Not preceded by a letter, digit or dot, so "v3" and the tail of "2410.05779" stay out.
_NUMBER = re.compile(r"(?<![\w.,])(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?%?")
# A number right after one of these words numbers a part of the document, not a result:
# "Section 4.3", "Table 2", "Fig. 2", "RQ2", "Appendix A.1", "Equation 3", "第 4 節".
_STRUCTURE_LABEL = re.compile(
    r"(?:\b(?:section|sec\.|subsection|chapter|table|tab\.|figure|fig\.|appendix|equation|eq\.|"
    r"algorithm|rq|page|pages|p\.|pp\.)\s*|§\s*|第\s*)$",
    re.IGNORECASE,
)
_CITATION = re.compile(r"\[\s*\d{1,3}(?:\s*,\s*\d{1,3})*\s*\]")
_PAGE_REFERENCE = re.compile(r"\(pp?\.\s*\d+(?:\s*[-–]\s*\d+)?\)")
_SNIPPET_RADIUS = 80
# Where one sentence ends: a full stop followed by space, unless it is an abbreviation.
_SENTENCE_END = re.compile(
    r"(?<!\be\.g\.)(?<!\bi\.e\.)(?<!\bvs\.)(?<!\betc\.)(?<=[.!?。！？])\s+|\n+"
)
# Where one statement about figures ends and the next begins inside a sentence: a
# semicolon or a connective after a comma.
_CLAUSE_BREAK = re.compile(r"\s*[;；]\s*|,\s+(?:and|but|while|whereas)\s+|，(?:而|但|且)")
# What may stand between a label and the figure it belongs to: "NaiveRAG 32.4%",
# "NaiveRAG's 32.4%", "NaiveRAG: 32.4%", "32.4% (NaiveRAG)", "32.4% comprehensiveness",
# "32.4% in Legal", "57.6% for the -High variant". A comma breaks the tie: in
# "67.6% comprehensiveness, 76.4%" the label is 67.6%'s.
# Up to four blanks: blanked emphasis markers ("**67.6%**") leave extra spaces.
_BEFORE_FIGURE = re.compile(r"(?:['’]s)?[\s:(]{0,4}")
_AFTER_FIGURE = re.compile(r"[\s(]{0,4}|\s+(?:in|for|on|of)\s+(?:the\s+)?")
# Two figures joined into a range ("32.4%–38.8%") share their labels.
_RANGE = re.compile(r"\s*[-–]\s*")
# What stands right before the name of the method a figure is compared against.
_COMPARISON_CUE = re.compile(
    r"(?:\b(?:over|against|than|versus|vs\.?|compared\s+(?:to|with)|relative\s+to)\s+(?:the\s+)?"
    r"|(?:優於|勝過|相較於|對比)\s*)$",
    re.IGNORECASE,
)
# A sentence that explicitly keeps the setting of the previous one ("in the same dataset").
_SAME_AS_BEFORE = re.compile(r"\bthe\s+same\s+\w+|同一", re.IGNORECASE)
# A list item: the heading of a list ("- Comprehensiveness:") labels the items under it.
_LIST_ITEM = re.compile(r"^\s*(?:[-*•]|\d+[.)])\s")
# A claim that holds everywhere, and a comparison: together, a universal comparison (D68).
# "Consistently", "in all cases", "across all …" range over every cell; a bare "all" or
# "every" may range over one slice only ("in all metrics", on some dataset left unsaid).
_EVERYWHERE = re.compile(
    r"\b(?:consistently|always|everywhere|across the board|in all cases|in every case"
    r"|without exception|across all|across every|on all|on every|for all|for every|in all datasets"
    r"|in every dataset)\b|全面|所有|一律|始終|全部|都",
    re.IGNORECASE,
)
_UNIVERSAL = re.compile(r"\b(?:all|every)\b|全部|所有|都", re.IGNORECASE)
_COMPARATIVE = re.compile(
    r"\b(?:outperform\w*|surpass\w*|exceed\w*|beats?|better|higher|lower|superior|inferior|best|worst)\b"
    r"|優於|勝過|領先|高於|低於|超過",
    re.IGNORECASE,
)
_HEDGE = re.compile(
    r"\b(?:most|many|nearly|almost|generally|typically|mostly|except|particularly|especially"
    r"|in particular)\b|大多|多數|幾乎|除了|尤其|特別",
    re.IGNORECASE,
)
_TABLE_CAPTION = re.compile(r"^\s*Table \d+[.:]")


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
class UnresolvedNumber:
    number: str  # as written in the answer
    answer_labels: list[str]  # the labels the answer gives it, in table order
    source_labels: list[list[str]]  # the cells holding this value that those labels fit
    sentence: str
    reason: str  # "missing": a label the cells have is not given; "ambiguous": two are


@dataclass(frozen=True)
class OverstatedClaim:
    """A sentence claiming one method wins everywhere, checked cell by cell (D68)."""

    sentence: str
    method: str  # the subject of the claim
    compared: list[str]  # the methods it is compared with (named, or every other one)
    higher: int  # shared cells where the method's value is above the other's
    lower: int  # shared cells where it is below
    examples: list[
        str
    ]  # the cells of the rarer direction, e.g. "Overall / Mix: A 60.0% vs B 64.8% (p. 8)"
    status: str  # "contradicted": both directions occur; "unresolved": no shared cells
    reason: str | None


@dataclass(frozen=True)
class NumberCheck:
    verified: list[VerifiedNumber]
    unverified: list[str]
    mislabelled: list[MislabelledNumber]  # contradicted by the table
    unresolved: list[UnresolvedNumber]  # neither confirmed nor contradicted
    overstated: list[OverstatedClaim]  # universal claims the tables do not bear out


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
        if _STRUCTURE_LABEL.search(stripped, 0, match.start()):
            continue  # "Section 4.3", "Table 2": a label of the document, not a figure
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
        return NumberCheck([], [], [], [], check_universal_claims(answer, pages))
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
    mislabelled, unresolved = check_labels(answer, pages)
    return NumberCheck(
        verified, unverified, mislabelled, unresolved, check_universal_claims(answer, pages)
    )


@dataclass(frozen=True)
class _Cell:
    labels: tuple[str, ...]  # row label, column group[, sub-column]
    comparator: str | None  # the other sub-column of a two-column group

    def shown(self) -> list[str]:
        return [*self.labels, f"vs {self.comparator}"] if self.comparator else list(self.labels)


def _key(number: str) -> str:
    """The value as the cells are keyed: without thousands separators, with the
    percent sign, so that 64.0 and 64.0% are different figures."""
    return number.replace(",", "")


def _table_cells(pages: Iterable[PageText]) -> dict[str, list[_Cell]]:
    """Value -> the table cells holding it, each with its labels and comparator."""
    cells: dict[str, list[_Cell]] = {}
    for page in pages:
        for line in page.text.splitlines():
            row = cells_of(line)
            groups: dict[tuple[str, ...], list[tuple[str, tuple[str, ...]]]] = {}
            for value, labels in row:
                groups.setdefault(labels[:2], []).append((value, labels))
            for members in groups.values():
                for index, (value, labels) in enumerate(members):
                    comparator = None
                    if len(members) == 2 and len(labels) == 3:
                        comparator = members[1 - index][1][2]
                    cell = _Cell(labels, comparator)
                    known = cells.setdefault(_key(value), [])
                    if cell not in known:
                        known.append(cell)
    return cells


def _label_pattern(label: str) -> re.Pattern[str]:
    # Whole words, case ignored; a label such as "-High" may follow a word directly; a
    # space may be written inside a camel-case name ("Naive RAG" for "NaiveRAG").
    prefix = r"(?<!\w)" if label[0].isalnum() else ""
    suffix = r"(?!\w)" if label[-1].isalnum() else ""
    body = re.sub(r"(?<=[a-z])(?=[A-Z])", r"\\s?", re.escape(label))
    return re.compile(prefix + body + suffix, re.IGNORECASE)


Span = tuple[int, int]
Mention = tuple[int, int, str]  # start, end, label


def _mentions(text: str, labels: Iterable[str]) -> list[Mention]:
    """Where the labels of one category are mentioned in the text.

    Two labels directly after one another ("LightRAG -High") are one compound
    name, and the later one is the name that counts.
    """
    found = sorted(
        (m.start(), m.end(), label)
        for label in labels
        for m in _label_pattern(label).finditer(text)
    )
    merged: list[Mention] = []
    for start, end, label in found:
        if merged and 0 <= start - merged[-1][1] <= 1:
            merged[-1] = (merged[-1][0], end, label)
        else:
            merged.append((start, end, label))
    return merged


def _attached(text: str, mention: Mention, figure: Span, figures: Sequence[Span]) -> bool:
    """A label written right before a figure ("LightRAG 67.6%") or right after it
    ("67.6% (LightRAG)", "67.6% in Legal") is that figure's own; one that could be
    either goes with the figure it precedes."""
    m_start, m_end, _ = mention
    start, end = figure
    if m_end <= start and _BEFORE_FIGURE.fullmatch(text[m_end:start]):
        return True
    if end <= m_start and _AFTER_FIGURE.fullmatch(text[end:m_start]):
        return not any(
            other_start >= m_end and _BEFORE_FIGURE.fullmatch(text[m_end:other_start])
            for other_start, _ in figures
            if other_start != start
        )
    return False


def _distinct(mentions: Iterable[Mention]) -> set[str]:
    return {label for _, _, label in mentions}


@dataclass(frozen=True)
class _Claim:
    figure: Span
    labels: list[str | None]  # one per label category, None when not given
    comparator: str | None
    ambiguous: bool  # some category had two candidate labels and none attached

    @property
    def empty(self) -> bool:
        return all(label is None for label in self.labels) and self.comparator is None

    def shown(self) -> list[str]:
        given = [label for label in self.labels if label is not None]
        return [*given, f"vs {self.comparator}"] if self.comparator else given


def _claims(
    sentence: str,
    vocabulary: Sequence[set[str]],
    inherited: Sequence[str | None],
    heading: Sequence[str | None] = (),
) -> list[_Claim]:
    """What the sentence claims about each table figure in it, by role.

    For every label category: the label written with the figure; else the one
    label the figure's clause states freely (not with another figure, not as a
    comparator); else the one label the sentence states; else, when the sentence
    says it keeps the previous one's setting, that sentence's label; else the
    label of the list heading the sentence is an item of. Two free candidates are
    an ambiguity, not a choice. The last category names methods, and a method
    right after a comparison word is the comparator.
    """
    figures = [
        (m.start(), m.end()) for m in _NUMBER.finditer(sentence) if _is_worth_checking(m.group())
    ]
    clauses = _pieces(sentence, _CLAUSE_BREAK)
    keeps_setting = bool(_SAME_AS_BEFORE.search(sentence))
    method = len(vocabulary) - 1
    claims: list[_Claim] = []
    per_category = [_mentions(sentence, labels) for labels in vocabulary]
    owner: dict[Mention, Span | None] = {
        m: next((f for f in figures if _attached(sentence, m, f, figures)), None)
        for mentions in per_category
        for m in mentions
    }

    def after_cue(m: Mention) -> bool:
        at = m[0] if owner[m] is None or owner[m][0] > m[0] else owner[m][0]  # type: ignore[index]
        return _COMPARISON_CUE.search(sentence[:at]) is not None

    # Figures joined by a dash form a range and are read as one: "32.4%–38.8%".
    ranges: dict[Span, set[Span]] = {f: {f} for f in figures}
    for previous, figure in pairwise(figures):
        if _RANGE.fullmatch(sentence[previous[1] : figure[0]]):
            joined = ranges[previous] | ranges[figure]
            for member in joined:
                ranges[member] = joined

    for figure in figures:
        clause = next((c for c in clauses if c[0] <= figure[0] < c[1]), (0, len(sentence)))
        labels: list[str | None] = []
        ambiguous = False
        comparator: str | None = None
        for position, mentions in enumerate(per_category):
            is_method = position == method
            own = [m for m in mentions if owner[m] in ranges[figure]]
            if own:
                labels.append(own[0][2])
                continue
            free = [m for m in mentions if owner[m] is None and not (is_method and after_cue(m))]
            in_clause = _distinct(m for m in free if clause[0] <= m[0] < clause[1])
            if len(in_clause) == 1:
                labels.append(in_clause.pop())
                continue
            if len(in_clause) > 1:
                ambiguous = True
                labels.append(None)
                continue
            in_sentence = _distinct(free if is_method else mentions)
            if len(in_sentence) == 1:
                labels.append(in_sentence.pop())
            elif len(in_sentence) > 1 and is_method:
                ambiguous = True
                labels.append(None)
            elif keeps_setting and inherited[position] is not None:
                labels.append(inherited[position])
            else:
                labels.append(heading[position] if heading else None)
        cues = [m for m in per_category[method] if owner[m] is None and after_cue(m)]
        # "83.6% against A, 88.4% against B": each comparator belongs to the figure before
        # it. A figure without one takes the clause's (then the sentence's) single
        # comparator, unless a comparison phrase names something the tables do not know.
        following = [m for m in cues if m[0] > figure[1]]
        next_figure = next((f[0] for f in figures if f[0] > figure[1]), len(sentence))
        own_cue = [m for m in following if m[0] < next_figure]
        if own_cue:
            comparator = own_cue[0][2]
        elif not _unknown_comparator(sentence, clause, per_category[method]):
            for scope in ([m for m in cues if clause[0] <= m[0] < clause[1]], cues):
                if len(_distinct(scope)) == 1:
                    comparator = scope[0][2]
                    break
        claims.append(_Claim(figure, labels, comparator, ambiguous))
    return claims


_COMPARISON_PHRASE = re.compile(
    r"\b(?:over|against|than|versus|vs\.?|compared\s+(?:to|with)|relative\s+to)\s+(?:the\s+)?"
    r"|優於|勝過|相較於|對比",
    re.IGNORECASE,
)


def _unknown_comparator(sentence: str, clause: Span, mentions: Sequence[Mention]) -> bool:
    """Whether a comparison phrase in the clause is followed by something that is not a
    known method name (or a figure): a comparator the tables cannot name."""
    starts = {m[0] for m in mentions}
    for phrase in _COMPARISON_PHRASE.finditer(sentence, clause[0], clause[1]):
        rest = sentence[phrase.end() :]
        if not rest.strip():
            return True
        if phrase.end() in starts or _NUMBER.match(rest) or rest[:1] == "(":
            continue
        return True
    return False


def _fits(claim: _Claim, cell: _Cell) -> bool:
    return all(
        given is None or given == label
        for given, label in zip(claim.labels, cell.labels, strict=False)
    ) and (claim.comparator is None or cell.comparator in (None, claim.comparator))


def _complete(claim: _Claim, cell: _Cell) -> bool:
    return all(label is not None for label in claim.labels[: len(cell.labels)])


@dataclass(frozen=True)
class LabelOutcome:
    """What the table says about one figure of the answer, for evaluation and display."""

    number: str
    status: str  # "supported", "contradicted", "unresolved" or "unchecked" (no labels given)
    answer_labels: list[str]
    source_labels: list[list[str]]  # contradicted: every cell with the value; else the fitting ones
    sentence: str
    reason: str | None  # unresolved only: "missing" or "ambiguous"
    position: int  # where the figure starts in the answer


def label_outcomes(answer: str, pages: Sequence[PageText]) -> list[LabelOutcome]:
    """One outcome per table figure of the answer, in order of appearance."""
    cells = _table_cells(pages)
    if not cells:
        return []
    categories = max(len(cell.labels) for known in cells.values() for cell in known)
    vocabulary: list[set[str]] = [set() for _ in range(categories)]
    for known in cells.values():
        for cell in known:
            for position, label in enumerate(cell.labels):
                vocabulary[position].add(label)
    # Citation markers, page references and emphasis markers are blanked, not
    # removed, so that positions stay those of the answer.
    blanked = _PAGE_REFERENCE.sub(
        lambda m: " " * len(m.group()), _CITATION.sub(lambda m: " " * len(m.group()), answer)
    ).replace("*", " ")
    outcomes: list[LabelOutcome] = []
    inherited: list[str | None] = [None] * categories
    heading: list[str | None] = [None] * categories
    for s_start, s_end in _pieces(blanked, _SENTENCE_END):
        sentence = blanked[s_start:s_end]
        shown_sentence = _tidy(answer[s_start:s_end])
        mentions = [_mentions(sentence, labels) for labels in vocabulary]
        if _is_heading(sentence, mentions):
            # "- Comprehensiveness:" labels the list items that follow it.
            heading = [
                next(iter(found)) if len(found := _distinct(found_mentions)) == 1 else None
                for found_mentions in mentions
            ]
            continue
        if not _LIST_ITEM.match(sentence):
            heading = [None] * categories
        for claim in _claims(sentence, vocabulary, inherited, heading):
            start, end = claim.figure
            number = sentence[start:end]
            candidates = cells.get(_key(number))
            if not candidates:
                continue
            fitting = [cell for cell in candidates if _fits(claim, cell)]
            if claim.empty:
                status, reason, shown = "unchecked", None, fitting
            elif not fitting:
                status, reason, shown = "contradicted", None, candidates
            elif claim.ambiguous:
                status, reason, shown = "unresolved", "ambiguous", fitting
            elif not any(_complete(claim, cell) for cell in fitting):
                status, reason, shown = "unresolved", "missing", fitting
            else:
                status, reason, shown = "supported", None, fitting
            outcomes.append(
                LabelOutcome(
                    number,
                    status,
                    claim.shown(),
                    [cell.shown() for cell in shown],
                    shown_sentence,
                    reason,
                    s_start + start,
                )
            )
        # What the next sentence may inherit: the one label of each kind this one states.
        inherited = [
            next(iter(found)) if len(found := _distinct(found_mentions)) == 1 else None
            for found_mentions in mentions
        ]
    return outcomes


def _is_heading(sentence: str, mentions: Sequence[Sequence[Mention]]) -> bool:
    """A line that is nothing but labels and punctuation, such as "- Comprehensiveness:"."""
    if not any(mentions) or _NUMBER.search(sentence):
        return False
    rest = list(sentence)
    for category in mentions:
        for start, end, _ in category:
            rest[start:end] = " " * (end - start)
    return not re.search(r"\w", "".join(rest))


def check_labels(
    answer: str, pages: Sequence[PageText]
) -> tuple[list[MislabelledNumber], list[UnresolvedNumber]]:
    """The table figures of the answer that the table contradicts, and those it can
    neither confirm nor contradict; each figure with the same labels once."""
    mislabelled: list[MislabelledNumber] = []
    unresolved: list[UnresolvedNumber] = []
    seen: set[tuple[str, tuple[str, ...]]] = set()
    for outcome in label_outcomes(answer, pages):
        key = (outcome.number, tuple(outcome.answer_labels))
        if outcome.status in ("supported", "unchecked") or key in seen:
            continue
        seen.add(key)
        if outcome.status == "contradicted":
            mislabelled.append(
                MislabelledNumber(
                    outcome.number, outcome.answer_labels, outcome.source_labels, outcome.sentence
                )
            )
        else:
            unresolved.append(
                UnresolvedNumber(
                    outcome.number,
                    outcome.answer_labels,
                    outcome.source_labels,
                    outcome.sentence,
                    outcome.reason or "missing",
                )
            )
    return mislabelled, unresolved


Occurrence = tuple[str, str, int]  # sub-column, value, block of the table it is in


@dataclass(frozen=True)
class _Table:
    page: int
    cells: dict[tuple[str, str], list[Occurrence]]  # (row, group) -> the cells of that key


def _tables(pages: Iterable[PageText]) -> list[_Table]:
    """The tables of the pages as the chunker rewrote them, one per caption.

    A table may repeat its rows in several blocks ("NaiveRAG -High", "NaiveRAG -Low"):
    cells with the same row and group from different blocks are compared with one
    another, since they measure the same thing; a sub-column that recurs in every
    block (the reference) is taken from the block of the method it is compared with.
    """
    tables: list[_Table] = []
    for page in pages:
        current: _Table | None = None
        block = 0
        seen_in_block: set[tuple[str, str]] = set()
        for line in page.text.splitlines():
            if _TABLE_CAPTION.match(line):
                current = _Table(page.page, {})
                tables.append(current)
                block, seen_in_block = 0, set()
                continue
            row = cells_of(line)
            if not row:
                continue
            if current is None:
                current = _Table(page.page, {})
                tables.append(current)
            keys = {(labels[0], labels[1]) for _, labels in row if len(labels) == 3}
            if keys & seen_in_block:  # a row label comes round again: a new block
                block += 1
                seen_in_block = set()
            for value, labels in row:
                if len(labels) == 3:
                    current.cells.setdefault((labels[0], labels[1]), []).append(
                        (labels[2], value, block)
                    )
            seen_in_block |= keys
    return [t for t in tables if t.cells]


def _as_number(value: str) -> tuple[float, str] | None:
    try:
        return float(value.replace(",", "").rstrip("%")), "%" if value.endswith("%") else ""
    except ValueError:
        return None


def check_universal_claims(answer: str, pages: Sequence[PageText]) -> list[OverstatedClaim]:
    """Sentences that claim one method is above (or below) others everywhere, checked
    against every table of the pages that holds that method."""
    tables = _tables(pages)
    if not tables:
        return []
    methods = {o[0] for t in tables for cells in t.cells.values() for o in cells}
    rows = {key[0] for t in tables for key in t.cells}
    groups = {key[1] for t in tables for key in t.cells}
    blanked = _PAGE_REFERENCE.sub(
        lambda m: " " * len(m.group()), _CITATION.sub(lambda m: " " * len(m.group()), answer)
    ).replace("*", " ")
    claims: list[OverstatedClaim] = []
    for s_start, s_end in _pieces(blanked, _SENTENCE_END):
        sentence = blanked[s_start:s_end]
        everywhere = _EVERYWHERE.search(sentence) is not None
        comparative = _COMPARATIVE.search(sentence)
        if not (everywhere or _UNIVERSAL.search(sentence)) or not comparative:
            continue
        if _HEDGE.search(sentence):
            continue
        mentioned = _mentions(sentence, methods)
        before = [m for m in mentioned if m[1] <= comparative.start()]
        if not before:
            continue  # no method is the subject of the comparison
        method = before[-1][2]
        compared = list(dict.fromkeys(label for _, _, label in mentioned if label != method))
        row_scope = _distinct(_mentions(sentence, rows))
        group_scope = _distinct(_mentions(sentence, groups))
        above: list[str] = []
        below: list[str] = []
        # Per slice (one row, or one group) and per table: which way the method goes.
        slices: dict[tuple[str, str], set[str]] = {}
        for table in tables:
            for (row, group), cells in table.cells.items():
                if (row_scope and row not in row_scope) or (
                    group_scope and group not in group_scope
                ):
                    continue
                others = [o for o in cells if o[0] != method and (not compared or o[0] in compared)]
                for sub, own_value, own_block in cells:
                    if sub != method or (own := _as_number(own_value)) is None:
                        continue
                    for other in dict.fromkeys(o[0] for o in others):
                        same = [o for o in others if o[0] == other and o[2] == own_block]
                        for _, value, _ in same or [o for o in others if o[0] == other]:
                            theirs = _as_number(value)
                            if theirs is None or theirs[1] != own[1]:
                                continue
                            example = (
                                f"{row} / {group}: {method} {own_value} vs {other} {value} "
                                f"(p. {table.page})"
                            )
                            if own[0] > theirs[0]:
                                above.append(example)
                                direction = "above"
                            elif own[0] < theirs[0]:
                                below.append(example)
                                direction = "below"
                            else:
                                continue
                            slices.setdefault(("row", row), set()).add(direction)
                            slices.setdefault(("group", group), set()).add(direction)
        shown = _tidy(answer[s_start:s_end])
        higher, lower = len(above), len(below)
        # A bare "all metrics" may be about one dataset the sentence does not name: the
        # claim stands if some slice is one-way. "Consistently" leaves no such room.
        one_way_slice = any(len(directions) == 1 for directions in slices.values())
        if higher and lower and (everywhere or not one_way_slice):
            examples = _spread(below if lower <= higher else above)
            claims.append(
                OverstatedClaim(
                    shown, method, compared, higher, lower, examples, "contradicted", None
                )
            )
        elif not higher and not lower:
            claims.append(
                OverstatedClaim(
                    shown,
                    method,
                    compared,
                    0,
                    0,
                    [],
                    "unresolved",
                    "the cited tables pair this method with none of the compared ones",
                )
            )
    return claims


def _spread(examples: list[str]) -> list[str]:
    """The examples with those from different pages first, so that a note that shows
    three of them does not show one table only."""
    by_page: dict[str, list[str]] = {}
    for example in examples:
        by_page.setdefault(example.rsplit("(p. ", 1)[-1], []).append(example)
    spread: list[str] = []
    queues = list(by_page.values())
    while any(queues):
        for queue in queues:
            if queue:
                spread.append(queue.pop(0))
    return spread


_CLAIM_NOTES = {
    "other": "A claim the source table does not bear out: {}",
    "zh": "以下結論與原文表格不符：{}",
}


def claim_note(claims: Sequence[OverstatedClaim], language: str) -> str:
    """What the reader is told after the answer when a universal claim is contradicted."""
    items = []
    for c in claims:
        if c.status != "contradicted":
            continue
        shown = c.examples[:3]
        if language == "zh":
            items.append(
                f"「{c.sentence}」——{c.method} 在 {c.higher} 格高於比較對象、{c.lower} 格低於，"
                f"例如 {'；'.join(shown)}"
            )
        else:
            items.append(
                f'"{c.sentence}" — {c.method} is above the compared methods in {c.higher} cells '
                f"and below in {c.lower}, for example {'; '.join(shown)}"
            )
    joiner = "；" if language == "zh" else " / "
    end = "。" if language == "zh" else "."
    return _CLAIM_NOTES["zh" if language == "zh" else "other"].format(joiner.join(items) + end)


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
