"""The prompt for answering a question from retrieved sources, and its citations.

The model is told to answer only from the numbered sources and to cite them
by number. Sources are added in order of relevance while they fit the evidence
budget; one that does not fit is left out whole, never cut short.
"""

import re
from typing import Any

from app.llm.tokenizer import TokenCounter
from app.retrieval.repository import RetrievedChunk

INSTRUCTIONS = """\
You answer questions about the user's documents.

Rules:
- Use only the numbered sources below. Do not use any other knowledge.
- After each statement, cite the sources it comes from by their numbers in square brackets, \
for example [1] or [2][3].
- Copy numbers and names exactly as they appear in the sources.
- If the sources do not contain the answer, say that the documents do not contain it and \
cite nothing.
- Answer in the language of the question.

Sources:
"""

_CITATION = re.compile(r"\[\s*(\d{1,3}(?:\s*,\s*\d{1,3})*)\s*\]")


def _source_block(index: int, chunk: RetrievedChunk) -> str:
    return f"[{index}] {chunk.filename}, page {chunk.page}\n{chunk.text}"


def build_answer_prompt(
    question: str, chunks: list[RetrievedChunk], counter: TokenCounter, evidence_budget: int
) -> tuple[str, list[RetrievedChunk]]:
    """The prompt, and the chunks that were included in it (numbered from 1 in that order)."""
    used: list[RetrievedChunk] = []
    blocks: list[str] = []
    spent = 0
    for chunk in chunks:
        block = _source_block(len(used) + 1, chunk)
        cost = counter.count(block)
        if spent + cost > evidence_budget:
            # Stop at the first that does not fit, so the numbering stays in rank order.
            break
        used.append(chunk)
        blocks.append(block)
        spent += cost
    sources = "\n\n".join(blocks) if blocks else "(no sources)"
    return f"{INSTRUCTIONS}{sources}\n\nQuestion: {question}\nAnswer:", used


def source_payload(index: int, chunk: RetrievedChunk) -> dict[str, Any]:
    """A source as it is sent to the client and stored with the answer."""
    return {
        "index": index,
        "kind": "chunk",
        "document_id": str(chunk.document_id),
        "filename": chunk.filename,
        "page_start": chunk.page,
        "page_end": chunk.page,
        "section_title": None,
        # The chunk as stored: it can be found verbatim on that page of the document.
        "snippet": chunk.text,
        "score": round(chunk.score, 4),
    }


def cited_indexes(answer: str, available: int) -> list[int]:
    """Source numbers cited in the answer, in order of first appearance.

    Only numbers of sources that were actually given count; anything else in
    square brackets is ignored.
    """
    cited: list[int] = []
    for match in _CITATION.finditer(answer):
        for number in match.group(1).split(","):
            index = int(number)
            if 1 <= index <= available and index not in cited:
                cited.append(index)
    return cited
