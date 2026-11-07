"""Table regions in a page's text, kept whole when chunking (AC-14).

pypdf gives a table as one row per line, right after its caption. Fixed-size
chunks cut such a block apart, and a row on its own does not say which column
is which dataset. A region is therefore recognised by its shape and chunked as
one piece: the caption line, the header lines, and the rows of numbers, up to
the first line of prose. Only tables with a caption and number rows count; a
case-study table of text cells is left to ordinary chunking.

The rows are then rewritten cell by cell with their column labels: pypdf's
"NaiveRAG -High NaiveRAG -High ..." header over "Overall 35.2% 64.8% ..." is
ambiguous to a reader who did not see the layout, whereas "Overall —
Agriculture: NaiveRAG 35.2%, -High 64.8%; ..." is not. The labels come from
the table itself: the first header line names the column groups, the second
the sub-columns of each group, and a header line between row groups renames
the sub-columns. A row whose figures do not match that shape is kept as is.
"""

import re
from dataclasses import dataclass
from typing import Protocol

_CAPTION = re.compile(r"^Table \d+[.:]")
_NUMBER_TOKEN = re.compile(r"^[<>≤≥≈~]?[-–]?\d+(?:[.,]\d+)*%?$|^[-–—]$|^[<>≤≥]$|^[×x]$")
_BARE_INTEGER = re.compile(r"^\d+$")
SECTION_MAX_WORDS = 6  # a line of words between rows that names the rows under it
_SENTENCE_END = (".", "!", "?", ":", ";", "。", "！", "？")
_BULLETS = ("•", "-", "–", "*")
NUMERIC_LINE_DENSITY = 0.4
HEADER_MAX_WORDS = 16
CAPTION_MAX_LINES = 12  # lines of caption prose and headers allowed before the first row


class _Counter(Protocol):
    def count(self, text: str) -> int: ...


def _numeric_density(line: str) -> float:
    words = line.split()
    if not words:
        return 0.0
    return sum(1 for word in words if _NUMBER_TOKEN.match(word)) / len(words)


def _is_number_row(line: str) -> bool:
    return _numeric_density(line) >= NUMERIC_LINE_DENSITY and len(line.split()) >= 2


_PROSE_MARKS = (". ", ", ", "; ", ": ")


def _is_prose_line(line: str) -> bool:
    """A sentence or a fragment of one: punctuation inside it, or too many words."""
    stripped = line.strip()
    return (
        any(mark in stripped for mark in _PROSE_MARKS)
        or stripped.endswith(_SENTENCE_END)
        or len(stripped.split()) > HEADER_MAX_WORDS
    )


def _is_header_line(line: str) -> bool:
    """A short line of labels: no sentence punctuation, no bullet, few words."""
    stripped = line.strip()
    words = stripped.split()
    return (
        0 < len(words) <= HEADER_MAX_WORDS
        and not stripped.endswith(_SENTENCE_END)
        and not stripped.startswith(_BULLETS)
    )


def find_table_regions(text: str) -> list[tuple[int, int]]:
    """Character ranges [start, end) of the table regions in the text, in order."""
    lines = text.splitlines(keepends=True)
    offsets: list[int] = []
    position = 0
    for line in lines:
        offsets.append(position)
        position += len(line)

    regions: list[tuple[int, int]] = []
    index = 0
    while index < len(lines):
        if not _CAPTION.match(lines[index].strip()):
            index += 1
            continue
        last = index  # the last line that belongs to the table
        has_rows = False
        before_rows = 0
        cursor = index + 1
        while cursor < len(lines):
            line = lines[cursor].rstrip("\r\n")
            if _is_number_row(line):
                has_rows = True
                last = cursor
            elif not has_rows:
                # Caption prose and header lines before the first row; which is which
                # is decided only where it matters (`header_lines`). A caption may run
                # over several lines (D81: nine in the GraphRAG paper's Table 6).
                if not line.strip() or before_rows >= CAPTION_MAX_LINES:
                    break
                before_rows += 1
                last = cursor
            elif _is_header_line(line) and _looks_like_block_header(line):
                last = cursor  # a block header between groups of rows
            else:
                break
            cursor += 1
        if has_rows:
            end = offsets[last] + len(lines[last].rstrip("\r\n"))
            regions.append((offsets[index], end))
            index = last + 1
        else:
            index += 1
    return regions


def _looks_like_block_header(line: str) -> bool:
    """Between row groups, a header repeats labels (e.g. "NaiveRAG -High" four times)
    or is short; prose that merely lacks a full stop is longer than that."""
    words = line.split()
    if not any(any(ch.isalpha() for ch in word) for word in words):
        return False  # a bare number (a page number) is not a block header
    return len(words) <= 8 or len(set(words)) <= len(words) // 2


def header_lines(lines: list[str], first_row: int) -> list[str]:
    """The header lines of a table: the run of label lines (no sentence punctuation, few
    words) immediately before the first row. Caption prose before them is not a header."""
    run: list[str] = []
    for line in reversed(lines[1:first_row]):
        if line.strip() and _is_header_line(line) and not _is_prose_line(line):
            run.append(line)
        else:
            break
    return list(reversed(run))


def table_blocks(text: str) -> list[str]:
    """A table chunk split at its block headers — the header lines between groups of rows,
    one per compared system in a results table — each block with the caption and the group
    header. Empty when the chunk is not a table or has a single block.

    D82 (user's idea): a table chunk holding several comparisons embeds as their average,
    so the one the question asks about ranks low; each block gets a vector of its own and
    the chunk scores by its best one (see RetrievalRepository.search)."""
    lines = text.splitlines()
    if not lines or not _CAPTION.match(lines[0].strip()):
        return []
    first_row = next((i for i, line in enumerate(lines) if _is_row(line)), None)
    if first_row is None:
        return []
    head = [lines[0], *header_lines(lines, first_row)]
    blocks: list[list[str]] = []
    current: list[str] = []
    for line in lines[first_row:]:
        if not _is_row(line) and _is_header_line(line) and not _is_prose_line(line):
            if current:
                blocks.append(current)
            current = [line]
        else:
            current.append(line)
    if current:
        blocks.append(current)
    if len(blocks) <= 1:
        return []
    # The first block's column header is the last header line; the later blocks each start
    # with their own, so they take the caption and the group header only.
    shared = head[:-1] if len(head) > 1 else head
    return ["\n".join([*head, *blocks[0]])] + ["\n".join([*shared, *block]) for block in blocks[1:]]


def _is_row(line: str) -> bool:
    """A row as pypdf wrote it, or as linearize_table rewrote it."""
    return _is_number_row(line) or " — " in line


def split_table(text: str, counter: _Counter, *, max_tokens: int) -> list[str]:
    """The table whole if it fits, else pieces of consecutive rows, each headed by
    the caption and header lines so that every piece can be read on its own."""
    if counter.count(text) <= max_tokens:
        return [text]
    lines = text.splitlines()
    first_row = next((i for i, line in enumerate(lines) if _is_row(line)), len(lines))
    # The first piece carries the whole caption; the later pieces repeat only the caption
    # line and the header lines (D81), not the caption's prose.
    full_header = "\n".join(lines[:first_row])
    short_header = "\n".join([lines[0], *header_lines(lines, first_row)])
    pieces: list[str] = []
    current: list[str] = []
    header = full_header
    for row in lines[first_row:]:
        candidate = "\n".join([header, *current, row])
        if current and counter.count(candidate) > max_tokens:
            pieces.append("\n".join([header, *current]))
            current = []
            header = short_header
        current.append(row)
    if current:
        pieces.append("\n".join([header, *current]))
    return pieces


def _header_words(line: str) -> list[str]:
    """The column names of a header line. A bare integer continues the name before it
    ("Condition 1", "Mean 2"), so that it is not read as a column of its own."""
    words: list[str] = []
    for word in line.split():
        if words and _BARE_INTEGER.match(word):
            words[-1] = f"{words[-1]} {word}"
        else:
            words.append(word)
    return words


@dataclass(frozen=True)
class _Layout:
    """How a table's columns are laid out: the groups (one level) or the groups and the
    sub-columns repeated under each (two levels)."""

    groups: list[str]
    subs: list[str] | None
    per_group: int

    @property
    def expected(self) -> int:
        return len(self.groups) * self.per_group


def _chunks(words: list[str], count: int) -> list[str]:
    size = len(words) // count
    return [" ".join(words[i * size : (i + 1) * size]) for i in range(count)]


def _repeats(subs: list[str], count: int) -> bool:
    size = len(subs) // count
    return count >= 1 and all(subs[i * size : (i + 1) * size] == subs[:size] for i in range(count))


def _two_level(
    first: list[str], second: list[str], figures: int, label_words: int = 1
) -> _Layout | None:
    """Groups from the line above, sub-columns from the line below. The sub-column names
    repeat once per group ("NaiveRAG LightRAG" × 4; "Mean 1 Mean 2 Z p" × 2), which is what
    tells how many groups there are when a group's name has several words ("Podcast
    Transcripts News Articles"). Names before the sub-columns that have no figures under
    them ("Condition 1 Condition 2") label the row."""
    for label_columns in (0, len(second) - figures):
        subs = second[label_columns:]
        if label_columns < 0 or len(subs) != figures or not subs:
            continue
        if label_columns and label_columns != label_words:
            continue  # the names set aside must be the row's label words, as many as it has
        candidates = [
            k
            for k in range(min(len(first), len(subs)), 1, -1)
            if len(subs) % k == 0 and len(first) % k == 0
        ]
        repeating = [k for k in candidates if _repeats(subs, k)]
        chosen = repeating or [k for k in candidates if k == len(first)] or candidates[:1]
        # A single "group" is a heading over the whole table, not a column group: the
        # columns are then the sub-column line alone (one level).
        if chosen:
            k = chosen[0]
            return _Layout(_chunks(first, k), subs, len(subs) // k)
    return None


def _single_level(words: list[str], figures: int) -> _Layout | None:
    """Columns from one header line: one name per figure; a first name over the row labels
    ("Statistics Agriculture CS Legal Mix"); or several words per column ("News Articles
    Podcast Transcripts")."""
    if not figures:
        return None
    if len(words) == figures:
        return _Layout(words, None, 1)
    if len(words) == figures + 1:
        return _Layout(words[1:], None, 1)
    if len(words) % figures == 0:
        return _Layout(_chunks(words, figures), None, 1)
    return None


def _layout(headers: list[str], figures: int, label_words: int = 1) -> _Layout | None:
    first = _header_words(headers[0])
    last = _header_words(headers[-1])
    if len(headers) >= 2:
        layout = _two_level(_header_words(headers[-2]), last, figures, label_words)
        if layout is not None:
            return layout
        if len(headers) >= 3:
            layout = _two_level(first, last, figures, label_words)
            if layout is not None:
                return layout
    return _single_level(last, figures)


def _typical(values: list[int]) -> list[int]:
    """The values by how often they occur, the most common first; ties to the smaller."""
    counts: dict[int, int] = {}
    for value in values:
        counts[value] = counts.get(value, 0) + 1
    return sorted(counts, key=lambda c: (-counts[c], c))


def _row_parts(line: str) -> tuple[list[str], list[str]]:
    """The label words and the figures of a row; empty figures when the row has words
    after its figures (prose, not a table row)."""
    words = line.split()
    figures = [w for w in words if _NUMBER_TOKEN.match(w)]
    label_words = words[: len(words) - len(figures)]
    if not all(_NUMBER_TOKEN.match(w) for w in words[len(label_words) :]):
        return label_words, []
    return label_words, figures


def _row_shapes(lines: list[str]) -> tuple[list[int], int]:
    """The figure counts the rows have (most common first) and how many label words a row
    typically has. A numeric row label ("0.5 23.42 …") is a figure too; it is told apart
    later, so such rows count one figure less."""
    figure_counts: list[int] = []
    label_counts: list[int] = []
    for line in lines:
        label_words, figures = _row_parts(line)
        if figures and _is_number_row(line):
            figure_counts.append(len(figures) - (0 if label_words else 1))
            label_counts.append(len(label_words) or 1)
    typical_labels = _typical(label_counts)
    return _typical(figure_counts), (typical_labels[0] if typical_labels else 1)


def linearize_table(text: str) -> str:
    """The table with each row written cell by cell: "label — Group: sub value, ...; ...".

    The caption and header lines are kept in front, and block header lines stay
    where they are, so the text still reads as the table it came from. A line of words
    between rows ("News Articles", "Comprehensiveness") names the rows under it: it
    becomes their group (one-level tables) or a prefix of their label (two-level tables).
    """
    lines = text.splitlines()
    first_row = next((i for i, line in enumerate(lines) if _is_number_row(line)), len(lines))
    headers = header_lines(lines, first_row)
    if not headers:
        return text
    figure_counts, typical_labels = _row_shapes(lines[first_row:])
    # The header lines right before the rows may be a section name ("News Articles",
    # "Comprehensiveness") rather than column names: try without them when the columns
    # cannot be read with them.
    layout: _Layout | None = None
    section: str | None = None
    for drop in range(len(headers)):
        used = headers[: len(headers) - drop]
        layout = next(
            (
                found
                for count in figure_counts
                if (found := _layout(used, count, typical_labels)) is not None
            ),
            None,
        )
        if layout is not None:
            section = headers[-1].strip() if drop else None
            break
    if layout is None:
        return text
    groups, subs, per_group = layout.groups, layout.subs, layout.per_group
    expected = layout.expected

    out = lines[:first_row]
    for line in lines[first_row:]:
        label_words, figures = _row_parts(line)
        if not label_words and len(figures) == expected + 1:
            label_words, figures = figures[:1], figures[1:]  # a numeric row label
        words = line.split()
        if figures and len(figures) == expected and label_words:
            label = " ".join(label_words)
            if subs is None and section is not None:
                out.append(_linear_row(label, figures, [section], groups, len(groups)))
            else:
                if section is not None:
                    label = f"{section} / {label}"
                out.append(_linear_row(label, figures, groups, subs, per_group))
        elif not figures and subs is not None and len(_header_words(line)) == expected:
            subs = _header_words(line)  # a block header: the sub-column names for the rows below
            out.append(line)
        elif (
            not figures
            and _is_header_line(line)
            and not _is_prose_line(line)
            and len(words) <= SECTION_MAX_WORDS
        ):
            section = line.strip()
            out.append(line)
        else:
            out.append(line)
    return "\n".join(out)


def _linear_row(
    label: str, figures: list[str], groups: list[str], subs: list[str] | None, per_group: int
) -> str:
    parts = []
    for g, group in enumerate(groups):
        cells = figures[g * per_group : (g + 1) * per_group]
        if subs is None:
            parts.append(f"{group}: {cells[0]}")
        else:
            named = ", ".join(f"{subs[g * per_group + j]} {value}" for j, value in enumerate(cells))
            parts.append(f"{group}: {named}")
    return f"{label} — " + "; ".join(parts)


_LINEAR_ROW = re.compile(r"^(?P<label>[^—]+?) — (?P<rest>.+)$")


def cells_of(line: str) -> list[tuple[str, tuple[str, ...]]]:
    """The figures of a row written by linearize_table, each with its labels.

    "Overall — Agriculture: NaiveRAG 35.2%, -High 64.8%" gives
    ("35.2%", ("Overall", "Agriculture", "NaiveRAG")) and so on; a row of a
    single-header table gives (value, (row label, column)). Any other line gives
    nothing.
    """
    match = _LINEAR_ROW.match(line.strip())
    if match is None:
        return []
    label, rest = match.group("label").strip(), match.group("rest")
    cells: list[tuple[str, tuple[str, ...]]] = []
    for segment in rest.split("; "):
        group, separator, body = segment.partition(": ")
        if not separator or not group.strip() or not body.strip():
            return []
        for cell in body.split(", "):
            words = cell.split()
            if not words or not _NUMBER_TOKEN.match(words[-1]):
                return []
            if len(words) == 1:
                cells.append((words[-1], (label, group.strip())))
            else:
                cells.append((words[-1], (label, group.strip(), " ".join(words[:-1]))))
    return cells


def is_table_chunk(text: str) -> bool:
    """A chunk that is a table region: a caption first, and at least one row."""
    lines = text.splitlines()
    if not lines or not _CAPTION.match(lines[0].strip()):
        return False
    return any(_is_row(line) for line in lines[1:])
