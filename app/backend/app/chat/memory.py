"""What a follow-up question is understood from: the conversation so far (AC-16).

A follow-up such as "and its drawbacks?" cannot be searched for as written.
Before retrieval, one LLM call rewrites it into a question that stands on its
own, given the memory of the conversation. The memory is bounded: the most
recent turns verbatim, earlier turns reduced to their questions, nothing from
answers that did not complete.
"""

from dataclasses import dataclass

from app.llm.tokenizer import TokenCounter

MEMORY_TOKEN_BUDGET = 800  # docs/02-specs/02-architecture.md, section 4.3
# D100 (user): the rewrite must see the previous answer — an answer longer than the memory
# was dropped whole, and "剛剛那張表裡 -Origin 贏了哪幾格" was rewritten with the wrong side.
# The rewrite's memory is larger, and a too-long newest answer keeps its head.
REWRITE_MEMORY_BUDGET = 2000
REWRITE_HEAD_TOKENS = 600

# D99 (user): whether a question needs the conversation is the model's call, not a keyword
# rule. The examples are about an unrelated report, so nothing of the user's documents is
# written here; "same topic" is explicitly not "follow-up" (the model called 16 of 19
# self-contained questions dependent when asked without that rule, decision log D95).
FOLLOW_UP_INSTRUCTIONS = """\
You decide whether a user's message can be answered by someone who has NOT seen the \
conversation, using only the documents.

Rule: being about the same topic as the conversation does NOT make a message a follow-up. A \
message is a FOLLOW-UP only if it cannot be understood without the conversation: it points \
back with words such as "it", "its", "they", "that", "the second one", "剛剛那個", "那它", or \
it is a bare fragment that completes an earlier question.

Examples (a conversation about some report on solar panels):
- "compare monocrystalline with polycrystalline panels" -> NEW (same topic, but complete on its own)
- "What test sites does the report use?" -> NEW
- "Efficiency of the panels after ten years" -> NEW
- "and its drawbacks?" -> FOLLOW-UP ("its" points back)
- "那它的成本呢？" -> FOLLOW-UP
- "what about the second site?" -> FOLLOW-UP
- "成本？" -> FOLLOW-UP (fragment)

Answer with exactly one word: NEW or FOLLOW-UP.

Conversation:
{memory}

Message: {question}
Answer:"""
FOLLOW_UP_MAX_OUTPUT_TOKENS = 8


def follow_up_prompt(memory: str, question: str) -> str:
    return FOLLOW_UP_INSTRUCTIONS.format(memory=memory, question=question)


def parse_follow_up(text: str) -> bool | None:
    """True for FOLLOW-UP, False for NEW, None when the answer is neither."""
    upper = text.strip().upper()
    if "FOLLOW" in upper:
        return True
    if "NEW" in upper:
        return False
    return None


@dataclass(frozen=True)
class HistoryMessage:
    role: str  # "user" or "assistant"
    content: str
    status: str


def _line(message: HistoryMessage) -> str:
    speaker = "User" if message.role == "user" else "Assistant"
    return f"{speaker}: {message.content.strip()}"


def _head(text: str, counter: TokenCounter, max_tokens: int) -> str:
    """The opening of the text within `max_tokens`, cut at a line or sentence end when one
    is near, marked as cut."""
    total = counter.count(text)
    if total <= max_tokens:
        return text
    cut = max(1, int(len(text) * max_tokens / total))
    piece = text[:cut]
    while piece and counter.count(piece) > max_tokens:
        piece = piece[: int(len(piece) * 0.9)]
    boundary = max(piece.rfind("\n"), piece.rfind(". "), piece.rfind("。"))
    if boundary > len(piece) * 0.6:
        piece = piece[: boundary + 1]
    return piece.rstrip() + " …"


def build_memory(
    history: list[HistoryMessage],
    counter: TokenCounter,
    *,
    budget_tokens: int,
    head_tokens: int = 0,
) -> str:
    """The conversation so far, oldest first, within the budget.

    Starting from the most recent message: whole lines while they fit; once
    they do not, only the questions of the remaining earlier turns; once those
    do not fit either, the rest is dropped. With `head_tokens` (D100), the most
    recent answer that does not fit keeps its head instead of being dropped.
    """
    usable = [
        m for m in history if m.content.strip() and (m.role == "user" or m.status == "completed")
    ]
    lines = [_line(m) for m in usable]
    kept: list[str] = []  # newest first
    spent = 0
    questions_only = False
    newest_answer = True
    for message, line in zip(reversed(usable), reversed(lines), strict=True):
        if questions_only and message.role != "user":
            continue
        cost = counter.count(line)
        if spent + cost > budget_tokens:
            if message.role == "user":
                break  # not even the question fits: everything earlier is dropped too
            if newest_answer and head_tokens > 0:
                head = _head(line, counter, min(head_tokens, budget_tokens - spent))
                kept.append(head)
                spent += counter.count(head)
            questions_only = True
            newest_answer = False
            continue
        if message.role != "user":
            newest_answer = False
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
