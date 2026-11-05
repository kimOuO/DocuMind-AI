"""Table regions in a page's text, kept whole when chunking (AC-14).

pypdf gives a table as one row per line, right after its caption. Fixed-size
chunks cut such a block apart, and a row on its own does not say which column
is which dataset. A region is therefore recognised by its shape and chunked as
one piece: the caption line, the header lines, and the rows of numbers, up to
the first line of prose. Only tables with a caption and number rows count; a
case-study table of text cells is left to ordinary chunking.
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


def split_table(text: str, counter: _Counter, *, max_tokens: int) -> list[str]:
    """The table whole if it fits, else pieces of consecutive rows, each headed by
    the caption and header lines so that every piece can be read on its own."""
    if counter.count(text) <= max_tokens:
        return [text]
    lines = text.splitlines()
    first_row = next((i for i, line in enumerate(lines) if _is_number_row(line)), len(lines))
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
