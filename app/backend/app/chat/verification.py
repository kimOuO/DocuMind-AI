"""Checking the numbers in an answer against the original text of the cited pages (AC-26).

A summary answer is produced from summaries, two steps away from the text, so
every concrete number in it is looked up on the pages its cited sources cover.
A number is verified when the same value appears there, ignoring thousands
separators and a percent sign; the page and a snippet of the original text are
kept as evidence. A number that is not found is reported, never let through
silently. No LLM is involved.
"""

import re
import uuid
from collections.abc import Sequence
from dataclasses import dataclass

# A number: with thousands separators, or plain; optional decimals; optional percent.
# Not preceded by a letter, digit or dot, so "v3" and the tail of "2410.05779" stay out.
_NUMBER = re.compile(r"(?<![\w.,])(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?%?")
_CITATION = re.compile(r"\[\s*\d{1,3}(?:\s*,\s*\d{1,3})*\s*\]")
_PAGE_REFERENCE = re.compile(r"\(pp?\.\s*\d+(?:\s*[-–]\s*\d+)?\)")
_SNIPPET_RADIUS = 80


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
class NumberCheck:
    verified: list[VerifiedNumber]
    unverified: list[str]


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
    """Look every number of the answer up on the given pages, in their order."""
    wanted = numbers_in(answer)
    if not wanted:
        return NumberCheck([], [])
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
    return NumberCheck(verified, unverified)


_NOTES = {
    "other": "Numbers that could not be checked against the cited pages of the original text: {}.",
    "zh": "以下數字未能在引用的原文頁面中核對：{}。",
}


def check_note(unverified: Sequence[str], language: str) -> str:
    """What the reader is told after the answer when numbers could not be verified."""
    separator = "、" if language == "zh" else ", "
    return _NOTES[language].format(separator.join(unverified))
