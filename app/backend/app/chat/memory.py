"""What a follow-up question is understood from: the conversation so far (AC-16).

A follow-up such as "and its drawbacks?" cannot be searched for as written.
Before retrieval, one LLM call rewrites it into a question that stands on its
own, given the memory of the conversation. The memory is bounded: the most
recent turns verbatim, earlier turns reduced to their questions, nothing from
answers that did not complete.
"""

import re
from dataclasses import dataclass

from app.llm.tokenizer import TokenCounter

MEMORY_TOKEN_BUDGET = 800  # docs/02-specs/02-architecture.md, section 4.3

# D96: what makes a question lean on the conversation — a pronoun, a demonstrative (not
# one pointing at the document itself: "this paper"), a connective at the start, a Chinese
# referent, or a sentence-final 呢. A closed set, so a rule decides; the model asked the
# same question called 16 of 19 self-contained questions "dependent" (decision log D95).
_REFERENCE = re.compile(
    r"\b(?:it|its|it's|they|them|their|theirs|one|ones|former|latter|above|same|also|too"
    r"|either|both|other|others|another|such|then|again|previous|earlier|mentioned|said)\b"
    r"|\b(?:this|that|these|those)\b(?!\s+(?:paper|document|file|report|article|study|work)s?\b)"
    r"|\b(?:what|how)\s+about\b|^\s*(?:and|or|but|also|plus)\b"
    r"|它|他們|她們|它們|牠|其|此|該|前者|後者|上述|同樣|也|又|還有|那麼|怎麼樣|如何呢|哪一?個|兩者|二者"
    r"|(?:這|那)(?!(?:篇|份|個|本)?(?:論文|文件|文章|報告|檔案))"
    r"|呢\s*[?？]?\s*$",
    re.IGNORECASE,
)
_WORD = re.compile(r"[A-Za-z0-9][\w'-]*")
_CJK = re.compile(r"[\u4e00-\u9fff]")


def needs_rewrite(question: str) -> bool:
    """Whether a follow-up has to be rewritten before retrieval (D96): it refers to the
    conversation, or it is a fragment of two or three words. A complete question is used
    as asked — the rewrite only adds material to it."""
    text = question.strip()
    if _REFERENCE.search(text):
        return True
    cjk = _CJK.findall(text)
    words = _WORD.findall(text)
    if cjk:
        return len(cjk) <= 4 and not words
    return len(words) <= 2


@dataclass(frozen=True)
class HistoryMessage:
    role: str  # "user" or "assistant"
    content: str
    status: str


def _line(message: HistoryMessage) -> str:
    speaker = "User" if message.role == "user" else "Assistant"
    return f"{speaker}: {message.content.strip()}"


def build_memory(
    history: list[HistoryMessage], counter: TokenCounter, *, budget_tokens: int
) -> str:
    """The conversation so far, oldest first, within the budget.

    Starting from the most recent message: whole lines while they fit; once
    they do not, only the questions of the remaining earlier turns; once those
    do not fit either, the rest is dropped.
    """
    usable = [
        m for m in history if m.content.strip() and (m.role == "user" or m.status == "completed")
    ]
    lines = [_line(m) for m in usable]
    kept: list[str] = []  # newest first
    spent = 0
    questions_only = False
    for message, line in zip(reversed(usable), reversed(lines), strict=True):
        if questions_only and message.role != "user":
            continue
        cost = counter.count(line)
        if spent + cost > budget_tokens:
            if message.role == "user":
                break  # not even the question fits: everything earlier is dropped too
            questions_only = True
            continue
        kept.append(line)
        spent += cost
    return "\n".join(reversed(kept))


REWRITE_INSTRUCTIONS = """\
Below is a conversation between a user and an assistant about the user's documents, followed \
by the user's latest question. Rewrite the latest question so that it can be understood on its \
own, without the conversation: replace pronouns and references such as "it", "they", "that \
method" or "the second one" with what they refer to in the conversation.

Rules:
- Keep the same language as the latest question.
- Keep the question's meaning and scope; add nothing that was not asked.
- If the question already stands on its own, return it unchanged.
- Do not answer the question. Output the rewritten question only, on one line.

Conversation:
{memory}

Latest question: {question}
Standalone question:"""


def rewrite_prompt(memory: str, question: str) -> str:
    return REWRITE_INSTRUCTIONS.format(memory=memory, question=question)


_QUOTES = "\"'“”‘’「」『』"
_LABEL = "standalone question:"


def clean_rewrite(text: str) -> str | None:
    """The rewritten question as a single line, or None if the output is not usable."""
    cleaned = text.strip()
    if cleaned.lower().startswith(_LABEL):
        cleaned = cleaned[len(_LABEL) :].strip()
    cleaned = cleaned.strip(_QUOTES).strip()
    if not cleaned or "\n" in cleaned:
        return None
    return cleaned
