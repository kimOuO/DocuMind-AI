"""Doubting citations that point at the wrong source (AC-13, D68).

The model is told to cite, after each statement, the source that states it. It
sometimes cites a source about the same topic instead: the figures of a cost
table for a statement about the update mechanism that stands in the next chunk.
Without another LLM call, the only evidence available is lexical: how many of a
statement's content words each source contains. That evidence can show that a
citation is doubtful; it can never show that one is right, so the check reports
doubts only, and only when they are clear-cut:

- the cited sources share hardly any of the statement's content words, and
- a source that was shown to the model but not cited for this statement shares
  most of them.

A source on the same page of the same document as a cited one counts as cited:
the citation already points the reader at the right page. A statement whose figure
stands in a cited source is not doubted either: the citation is for the figure. A
statement without a citation of its own takes the citation of the next cited
statement in its paragraph, since the model often cites once per paragraph. Statements with few
content words, without a citation, or not written in a language with
space-separated words are not checked. No LLM is involved.
"""

import re
import uuid
from collections.abc import Sequence
from dataclasses import dataclass

# Where one sentence ends (as in app.chat.verification).
_SENTENCE_END = re.compile(
    r"(?<!\be\.g\.)(?<!\bi\.e\.)(?<!\bvs\.)(?<!\betc\.)(?<=[.!?。！？])\s+|\n+"
)
_CITATION = re.compile(r"\[\s*(\d{1,3}(?:\s*,\s*\d{1,3})*)\s*\]")
# Content tokens: words of four letters or more, and figures (a figure is as telling as a word).
_WORD = re.compile(r"[A-Za-z][A-Za-z-]{3,}|\d[\d,]*(?:\.\d+)?%?")
# Function words and the words any statement about a document's methods tends to use.
_STOPWORDS = frozenset(
    [
        "about",
        "above",
        "after",
        "again",
        "against",
        "also",
        "although",
        "among",
        "another",
        "approximately",
        "because",
        "been",
        "before",
        "being",
        "below",
        "between",
        "both",
        "cannot",
        "could",
        "does",
        "doing",
        "done",
        "during",
        "each",
        "either",
        "every",
        "from",
        "further",
        "having",
        "here",
        "however",
        "into",
        "itself",
        "just",
        "like",
        "many",
        "more",
        "most",
        "much",
        "must",
        "neither",
        "nothing",
        "only",
        "other",
        "ought",
        "over",
        "same",
        "several",
        "shall",
        "should",
        "since",
        "some",
        "such",
        "than",
        "that",
        "their",
        "theirs",
        "them",
        "then",
        "there",
        "therefore",
        "these",
        "they",
        "this",
        "those",
        "through",
        "thus",
        "toward",
        "under",
        "until",
        "upon",
        "very",
        "were",
        "what",
        "when",
        "where",
        "whereas",
        "whether",
        "which",
        "while",
        "whom",
        "whose",
        "will",
        "with",
        "within",
        "without",
        "would",
        "your",
    ]
)
MIN_CONTENT_WORDS = 4  # chosen on the 13 saved answers of evaluation/answer-checks (D68)
# A citation is doubted when the best cited source covers at most this share of the
# statement's content words ...
CITED_COVERAGE_MAX = 0.34
# ... while an uncited source covers at least this share, with at least this many words.
CLOSER_COVERAGE_MIN = 0.5
CLOSER_SHARED_MIN = 3


@dataclass(frozen=True)
class SourceText:
    """A source as the model saw it: its number, text and place in the document."""

    index: int
    text: str
    document_id: uuid.UUID | None = None
    page_start: int | None = None
    page_end: int | None = None

    def overlaps(self, other: "SourceText") -> bool:
        if self.document_id is None or self.document_id != other.document_id:
            return False
        if None in (self.page_start, self.page_end, other.page_start, other.page_end):
            return False
        return self.page_start <= other.page_end and other.page_start <= self.page_end  # type: ignore[operator]


@dataclass(frozen=True)
class DoubtfulCitation:
    sentence: str
    cited: list[int]  # the sources the statement cites
    closer: list[int]  # the uncited sources that cover it far better, best first
    coverage_cited: float  # share of the statement's content words in the best cited source
    coverage_closer: float  # the same for the best uncited source


def _stem(word: str) -> str:
    word = word.lower()
    if word[0].isdigit():
        return word.replace(",", "")
    for suffix, replacement in (("ies", "y"), ("ing", ""), ("ed", ""), ("es", ""), ("s", "")):
        if word.endswith(suffix) and len(word) - len(suffix) >= 4:
            return word[: -len(suffix)] + replacement
    return word


def _content_words(text: str) -> set[str]:
    return {_stem(w) for w in _WORD.findall(text) if w.lower() not in _STOPWORDS}


def _tidy(sentence: str) -> str:
    without = _CITATION.sub(" ", sentence)
    return re.sub(r"\s+(?=[.,;:!?])", "", " ".join(without.split()))


def check_citations(answer: str, sources: Sequence[SourceText]) -> list[DoubtfulCitation]:
    """The statements whose citations are doubtful, given the sources the model was shown."""
    if len(sources) < 2:
        return []
    by_index = {source.index: source for source in sources}
    words_of = {source.index: _content_words(source.text) for source in sources}
    # Words that occur in most sources tell nothing about which source states a sentence.
    common = {
        word
        for word in set.union(*words_of.values())
        if sum(word in words for words in words_of.values()) > len(sources) / 2
    }
    doubts: list[DoubtfulCitation] = []
    for paragraph in re.split(r"\n\s*\n", answer):
        sentences = [s for s in _SENTENCE_END.split(paragraph) if s.strip()]
        own = [
            sorted(
                {int(n) for m in _CITATION.finditer(s) for n in m.group(1).split(",")}
                & set(words_of)
            )
            for s in sentences
        ]
        for i, sentence in enumerate(sentences):
            # An uncited statement is covered by the next citation in its paragraph.
            cited = own[i] or next((c for c in own[i:] if c), [])
            doubt = _doubt(sentence, cited, words_of, by_index, common)
            if doubt is not None:
                doubts.append(doubt)
    return doubts


def _doubt(
    sentence: str,
    cited: list[int],
    words_of: dict[int, set[str]],
    by_index: dict[int, SourceText],
    common: set[str],
) -> DoubtfulCitation | None:
    if not cited:
        return None
    words = _content_words(_CITATION.sub(" ", sentence)) - common
    if len(words) < MIN_CONTENT_WORDS:
        return None
    coverage = {index: len(words & found) / len(words) for index, found in words_of.items()}
    # Sources on the pages the citation points at count as cited.
    pointed = [
        i
        for i in words_of
        if i not in cited and any(by_index[i].overlaps(by_index[c]) for c in cited)
    ]
    best_cited = max(coverage[index] for index in [*cited, *pointed])
    if best_cited > CITED_COVERAGE_MAX:
        return None
    # A figure of the statement that stands in a cited source: the citation is for it.
    figures = {w for w in words if w[0].isdigit()}
    if any(figures & words_of[index] for index in [*cited, *pointed]):
        return None
    closer = sorted(
        (
            index
            for index in words_of
            if index not in cited
            and index not in pointed
            and coverage[index] >= CLOSER_COVERAGE_MIN
            and len(words & words_of[index]) >= CLOSER_SHARED_MIN
            and coverage[index] >= 2 * best_cited
        ),
        key=lambda index: -coverage[index],
    )
    if not closer:
        return None
    return DoubtfulCitation(
        _tidy(sentence), cited, closer, round(best_cited, 2), round(coverage[closer[0]], 2)
    )
