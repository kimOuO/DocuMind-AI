"""Which way a question is answered.

A keyword rule picks the stored summaries for questions that ask for a summary;
everything else goes to retrieval. When the rule cannot tell, no LLM call is
spent on deciding: the question goes to retrieval
(docs/02-specs/02-architecture.md, section 8, step 4).
"""

import re
from typing import Literal

QuestionType = Literal["summary", "retrieval"]

# English: the word family of "summary" as whole words. Chinese: the three terms.
_SUMMARY_WORDS = re.compile(
    r"\bsummar(?:y|ies|i[sz]e[sd]?|i[sz]ing|i[sz]ation)\b|摘要|總結|总结|概述", re.IGNORECASE
)


def question_type(question: str) -> QuestionType:
    return "summary" if _SUMMARY_WORDS.search(question) else "retrieval"
