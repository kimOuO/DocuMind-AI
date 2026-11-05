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
from typing import Protocol

_CAPTION = re.compile(r"^Table \d+[.:]")
_NUMBER_TOKEN = re.compile(r"^[-–]?\d+(?:[.,]\d+)*%?$|^[-–—]$|^[<>≤≥]$|^[×x]$")
_SENTENCE_END = (".", "!", "?", ":", ";", "。", "！", "？")
_BULLETS = ("•", "-", "–", "*")
NUMERIC_LINE_DENSITY = 0.4
HEADER_MAX_WORDS = 16


class _Counter(Protocol):
    def count(self, text: str) -> int: ...


def _numeric_density(line: str) -> float:
    words = line.split()
    if not words:
        return 0.0
    return sum(1 for word in words if _NUMBER_TOKEN.match(word)) / len(words)


def _is_number_row(line: str) -> bool:
    return _numeric_density(line) >= NUMERIC_LINE_DENSITY and len(line.split()) >= 2


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
        cursor = index + 1
        while cursor < len(lines):
            line = lines[cursor].rstrip("\r\n")
            if _is_number_row(line):
                has_rows = True
                last = cursor
            elif not has_rows and _is_header_line(line):
                last = cursor  # header lines before the first row
            elif has_rows and _is_header_line(line) and _looks_like_block_header(line):
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
    return len(words) <= 8 or len(set(words)) <= len(words) // 2


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
    header = "\n".join(lines[:first_row])
    pieces: list[str] = []
    current: list[str] = []
    for row in lines[first_row:]:
        candidate = "\n".join([header, *current, row])
        if current and counter.count(candidate) > max_tokens:
            pieces.append("\n".join([header, *current]))
            current = []
        current.append(row)
    if current:
        pieces.append("\n".join([header, *current]))
    return pieces


def linearize_table(text: str) -> str:
    """The table with each row written cell by cell: "label — Group: sub value, ...; ...".

    The caption and header lines are kept in front, and block header lines stay
    where they are, so the text still reads as the table it came from.
    """
    lines = text.splitlines()
    first_row = next((i for i, line in enumerate(lines) if _is_number_row(line)), len(lines))
    headers = [line for line in lines[1:first_row] if line.strip()]
    if not headers:
        return text
    groups = headers[0].split()
    second = headers[1].split() if len(headers) >= 2 else []
    subs: list[str] | None = None
    per_group = 1  # one header line: its words are the column names
    if second and len(second) % len(groups) == 0:
        subs, per_group = second, len(second) // len(groups)

    out = lines[:first_row]
    for line in lines[first_row:]:
        words = line.split()
        figures = [w for w in words if _NUMBER_TOKEN.match(w)]
        label_words = words[: len(words) - len(figures)]
        columns = groups
        if subs is None and label_words and len(figures) == len(groups) - 1:
            columns = groups[1:]  # the first header word names the row-label column
        expected = len(columns) * per_group
        if (
            figures
            and len(figures) == expected
            and label_words
            and all(_NUMBER_TOKEN.match(w) for w in words[len(label_words) :])
        ):
            out.append(_linear_row(" ".join(label_words), figures, columns, subs, per_group))
        elif not figures and subs is not None and len(words) == expected:
            subs = words  # a block header: the sub-column names for the rows below
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
