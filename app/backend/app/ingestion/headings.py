"""Recognise numbered section headings in parsed pages, and repair what the parser split.

The paper's headings are typeset in small caps. pypdf (ADR 0005) extracts them
with the first letter detached from the word: "1 I NTRODUCTION",
"3 T HE LIGHT RAG A RCHITECTURE". The number and the page are always right;
the text is repaired by rule where a rule can be sure, and kept as extracted
otherwise. Nothing here assumes the repaired title is correct: section
boundaries are taken from the number and the page, and the raw text is kept
(acceptance criterion AC-53).
"""

import re
from collections.abc import Sequence
from dataclasses import dataclass

from app.ingestion.parsing import Page

_NUMBERED_LINE = re.compile(r"^(?P<number>\d{1,2}(?:\.\d{1,2})*)\s+(?P<title>\S.*)$")
_MARKDOWN_LINE = re.compile(r"^(?P<hashes>#{1,6})\s+(?P<title>\S.*)$")
# A detached first letter: one capital, a space, then the rest of the word in capitals.
_DETACHED_INITIAL = re.compile(r"\b([A-Z]) (?=[A-Z]{2,}\b)")
_SPACE_BEFORE_HYPHEN = re.compile(r" +-(?=[A-Z])")
MIN_LETTERS = 3
MIN_UPPERCASE_SHARE = 0.6


@dataclass(frozen=True)
class Heading:
    number: str | None  # "4.2"; None for a Markdown heading
    level: int  # 1 for "4" or "#", 2 for "4.2" or "##", 3 for "4.2.1" or "###"
    raw: str  # the line as extracted, for the record
    title: str  # the normalised title text
    page: int
    line: int  # index of the line within the page


def normalize_title(raw: str) -> str:
    """Join letters that small-caps extraction detached, and tidy spacing.

    Only a lone capital followed by a word in capitals is joined ("I NTRODUCTION"),
    so ordinary titles ("A Survey of Graphs") are left alone. A name split into
    two capitalised words ("LIGHT RAG") cannot be told from two words and stays.
    """
    title = " ".join(raw.split())
    title = _DETACHED_INITIAL.sub(r"\1", title)
    title = _SPACE_BEFORE_HYPHEN.sub("-", title)
    return title.rstrip(".").strip()


def _looks_like_heading(title: str) -> bool:
    letters = [c for c in title if c.isalpha()]
    if len(letters) < MIN_LETTERS or "%" in title:
        return False
    # Either typeset in capitals (the paper), or a short line that starts with a
    # capital and has no sentence punctuation (plain-text and Markdown files).
    uppercase_share = sum(c.isupper() for c in letters) / len(letters)
    if uppercase_share >= MIN_UPPERCASE_SHARE:
        return True
    return title[0].isupper() and len(title) <= 80 and not title.rstrip().endswith((".", ":", ","))


def find_headings(pages: Sequence[Page]) -> list[Heading]:
    """Numbered headings (papers) and Markdown headings, in document order."""
    headings: list[Heading] = []
    for page in pages:
        for index, line in enumerate(page.text.splitlines()):
            stripped = line.strip()
            markdown = _MARKDOWN_LINE.match(stripped)
            if markdown is not None:
                headings.append(
                    Heading(
                        number=None,
                        level=len(markdown.group("hashes")),
                        raw=stripped,
                        title=" ".join(markdown.group("title").rstrip("#").split()),
                        page=page.number,
                        line=index,
                    )
                )
                continue
            match = _NUMBERED_LINE.match(stripped)
            if match is None or not _looks_like_heading(match.group("title")):
                continue
            number = match.group("number")
            headings.append(
                Heading(
                    number=number,
                    level=number.count(".") + 1,
                    raw=stripped,
                    title=normalize_title(match.group("title")),
                    page=page.number,
                    line=index,
                )
            )
    return headings
