"""Conditional verification-guided revision (D69): the parts without a model or a database.

An answer is produced once. The deterministic checks of this package may fault it:
a table figure under the wrong labels, a universal claim the table contradicts, a
citation of a source that was never given (hard faults), a statement whose citation
looks like the wrong source, a comparison target the question names but the answer
never mentions (soft faults). In the experimental two-call mode the service then
makes one more call that shows the model its own draft and those findings and asks
for a corrected answer; the revision goes through the same checks, and the final
answer is chosen by severity, never by a count: a revision with a new hard fault
loses, equal results keep the draft, and an answer with any remaining fault is
"unverified". Nothing here knows any document in particular.
"""

import re
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

from app.chat.citation_check import DoubtfulCitation
from app.chat.prompting import LANGUAGE_RULES, question_language
from app.chat.verification import NumberCheck, PageText, _label_pattern, _tables
from app.llm.tokenizer import TokenCounter

HARD = "hard"
SOFT = "soft"
REVISION_MAX_OUTPUT_TOKENS = 2_500
REVISION_MIN_OUTPUT_TOKENS = 800  # less room than this: do not revise
_CITATION = re.compile(r"\[\s*(\d{1,3}(?:\s*,\s*\d{1,3})*)\s*\]")
_ABLATION_QUESTION = re.compile(r"ablat|variant|消融|變體", re.IGNORECASE)
# A sub-column that is a variant of the method it is paired with: "-High", "w/o text".
_VARIANT_LABEL = re.compile(r"^(?:[-–]\w|w/o\b|without\b)", re.IGNORECASE)


@dataclass(frozen=True)
class Trigger:
    # mislabelled_number | overstated_claim | invalid_citation | doubtful_citation | incomplete
    kind: str
    severity: str  # HARD or SOFT
    feedback: str  # one finding, as told to the model
    key: str  # identity, to tell a fault the revision kept from one it added

    def as_dict(self) -> dict[str, Any]:
        return {"kind": self.kind, "severity": self.severity, "feedback": self.feedback}


@dataclass(frozen=True)
class Candidate:
    text: str
    triggers: list[Trigger]


@dataclass(frozen=True)
class Choice:
    chosen: str  # "draft" or "revision"
    status: str  # "verified": no fault left; "unverified": some fault remains
    reason: str


def invalid_citations(answer: str, available: int) -> list[int]:
    """Source numbers the answer cites that were never given, in order of appearance."""
    invalid: list[int] = []
    for match in _CITATION.finditer(answer):
        for number in match.group(1).split(","):
            index = int(number)
            if not 1 <= index <= available and index not in invalid:
                invalid.append(index)
    return invalid


def find_triggers(
    check: NumberCheck,
    doubts: Sequence[DoubtfulCitation],
    *,
    invalid: Sequence[int],
    missing: Sequence[str] = (),
    soft: bool = True,
) -> list[Trigger]:
    """What faults a draft, from the deterministic checks. Unresolved results never do."""
    triggers: list[Trigger] = []
    for m in check.mislabelled:
        cells = " / ".join(", ".join(labels) for labels in m.source_labels)
        triggers.append(
            Trigger(
                "mislabelled_number",
                HARD,
                f"The figure {m.number} is given the labels {', '.join(m.answer_labels)} in "
                f'"{m.sentence}", but the source table has {m.number} only as: {cells}.',
                f"mislabelled_number:{m.number}:{','.join(m.answer_labels)}",
            )
        )
    for c in check.overstated:
        if c.status != "contradicted":
            continue
        triggers.append(
            Trigger(
                "overstated_claim",
                HARD,
                f'The claim "{c.sentence}" is not borne out: {c.method} is above the compared '
                f"methods in {c.higher} cells and below in {c.lower}, for example "
                f"{'; '.join(c.examples[:3])}.",
                f"overstated_claim:{c.method}",
            )
        )
    for index in invalid:
        triggers.append(
            Trigger(
                "invalid_citation",
                HARD,
                f"The answer cites [{index}], but no source [{index}] was given; cite only the "
                "numbered sources.",
                f"invalid_citation:{index}",
            )
        )
    if soft:
        for d in doubts:
            closer = "".join(f"[{i}]" for i in d.closer)
            triggers.append(
                Trigger(
                    "doubtful_citation",
                    SOFT,
                    f'The statement "{d.sentence}" cites {"".join(f"[{i}]" for i in d.cited)}, '
                    f"which hardly contains it; {closer} states it. Cite the source that states "
                    "each statement.",
                    f"doubtful_citation:{d.sentence[:60]}",
                )
            )
    for name in missing:
        triggers.append(
            Trigger(
                "incomplete",
                SOFT,
                f"The answer never mentions {name}, which the question or the compared table "
                "covers; include it or say why it is left out.",
                f"incomplete:{name}",
            )
        )
    return triggers


def missing_coverage(question: str, answer: str, pages: Sequence[PageText]) -> list[str]:
    """Methods the answer should cover but does not, read conservatively from the tables
    of the cited pages: those the question names; and, for a question about an
    ablation, the variants of a table that pairs a reference with variant columns
    ("-High", "w/o text"). Nothing is required when the structure is not that clear."""
    tables = _tables(pages)
    methods = {sub for t in tables for cells in t.cells.values() for sub, _, _ in cells}
    if not methods:
        return []
    required: list[str] = []
    for method in sorted(methods):
        if _label_pattern(method).search(question):
            required.append(method)
    if _ABLATION_QUESTION.search(question):
        for table in tables:
            variants = {
                sub
                for cells in table.cells.values()
                for sub, _, _ in cells
                if _VARIANT_LABEL.match(sub)
            }
            if len(variants) >= 2:
                required.extend(v for v in sorted(variants) if v not in required)
    return [m for m in required if not _label_pattern(m).search(answer)]


REVISION_INSTRUCTIONS = """\
You revise your own draft answer to a question about the user's documents.

Rules:
- Use only the numbered sources below. Do not use any other knowledge.
- Correct every finding listed under "Checks of the draft found". Keep everything in the \
draft that is right. Do not add new figures unless a finding asks for them.
- Re-check every figure you keep: its method or variant, dataset, metric, unit and what it \
is compared against, read from the source table. Re-check the direction of every comparison \
("higher", "drops", "outperforms") against the figures. Name exceptions; a conclusion may not \
be stronger than the figures.
- After each statement, cite the source whose text states that statement, by its number in \
square brackets. Never cite a number that is not in the sources.
- Write only the revised answer, for the user; do not describe what you changed.
{language_rule}

Sources:
"""


def _source_block(source: dict[str, Any]) -> str:
    pages = (
        f"page {source['page_start']}"
        if source["page_start"] == source["page_end"]
        else f"pages {source['page_start']}-{source['page_end']}"
    )
    section = source.get("section_title")
    where = f"{source['filename']}, {pages}" + (f", section: {section}" if section else "")
    return f"[{source['index']}] {where}\n{source['snippet']}"


def build_revision_prompt(
    question: str,
    sources: Sequence[dict[str, Any]],
    draft: str,
    triggers: Sequence[Trigger],
    counter: TokenCounter,
    limit: int,
) -> tuple[str, int] | None:
    """The prompt of the second call and its output cap, or None when the answer would
    have too little room under the limit (then the draft stands, unrevised)."""
    language_rule = LANGUAGE_RULES[question_language(question)]
    findings = "\n".join(f"- {t.feedback}" for t in triggers)
    prompt = (
        REVISION_INSTRUCTIONS.format(language_rule=language_rule)
        + "\n\n".join(_source_block(s) for s in sources)
        + f"\n\nQuestion: {question}\n\nDraft answer:\n{draft}\n\n"
        f"Checks of the draft found:\n{findings}\n\nRevised answer:"
    )
    room = limit - counter.count(prompt)
    max_output = min(REVISION_MAX_OUTPUT_TOKENS, room)
    if max_output < REVISION_MIN_OUTPUT_TOKENS:
        return None
    return prompt, max_output


def _keys(candidate: Candidate, severity: str) -> set[str]:
    return {t.key for t in candidate.triggers if t.severity == severity}


def choose_final(draft: Candidate, revision: Candidate | None) -> Choice:
    """Pick by severity, never by count. A revision wins only when it removes hard faults
    without adding any, or, with the same hard faults, removes soft ones; otherwise the
    draft stays. "verified" means the chosen answer has no fault left at all."""
    if revision is None:
        return Choice("draft", _status(draft), "no revision")
    draft_hard, revision_hard = _keys(draft, HARD), _keys(revision, HARD)
    if revision_hard - draft_hard:
        return Choice("draft", _status(draft), "the revision has a new hard fault")
    if revision_hard < draft_hard:
        return Choice("revision", _status(revision), "the revision removed hard faults")
    if _keys(revision, SOFT) < _keys(draft, SOFT):
        return Choice("revision", _status(revision), "the revision removed soft faults")
    if revision_hard == draft_hard and not draft.triggers and not revision.triggers:
        return Choice("draft", "verified", "nothing to choose between: no faults either way")
    return Choice("draft", _status(draft), "the revision did not improve on the draft")


def _status(candidate: Candidate) -> str:
    return "verified" if not candidate.triggers else "unverified"
