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
    r"\bsummar(?:y|ies|i[sz]e[sd]?|i[sz]ing|i[sz]ation)\b|摘要|總結|总结|概述"
    # D88: the everyday ways of asking what a document is about go the same way.
    r"|\b(?:key\s+points?|main\s+points?|main\s+ideas?|overview|gist|tl;?dr|in\s+a\s+nutshell)\b"
    r"|\bwhat\s+(?:is|are|does)\s+(?:this|the|these)\s+(?:paper|document|article|file|report)s?\s+"
    r"(?:about|say|cover|discuss)"
    r"|重點|主旨|主要內容|大意|大綱|核心內容|核心貢獻"
    r"|(?:這|这|此|該|该)(?:篇|份|個|个)?(?:論文|论文|文件|文章|報告|报告)?(?:主要)?(?:在|是)?(?:講|讲|說|说|談|谈|寫|写)(?:了)?(?:什麼|甚麼|什么|些什麼|哪些)"
    r"|介紹(?:一下)?(?:這|这|此)(?:篇|份)",
    re.IGNORECASE,
)
# The same words used as the *subject matter* of a question about the text (D72): a
# summary of something inside the document ("community summaries", "the summarization
# method"), or a question counting or describing such summaries. Those are content
# questions and go to retrieval; only a request to summarise the document itself does not.
_ABOUT_SUMMARIES = re.compile(
    r"\b(?:how\s+many|how\s+much|number\s+of|count\s+of)\b.{0,60}summar"
    r"|\b(?:[\w-]+-level|community|communities|text|texts|source|chunk|section|graph|node|"
    r"global|local|hierarchical|intermediate|map-?reduce|query-focused|abstractive|extractive)"
    r"\s+summar"
    r"|summar\w*\s+(?:method|methods|approach|approaches|algorithm|technique|module|tree|"
    r"level|levels|node|nodes|unit|units|token|tokens|report|reports|count|counts)\b"
    r"|(?:社群|章節|文本|層級|層)摘要|摘要(?:方法|演算法|技術|樹|層)",
    re.IGNORECASE,
)


def question_type(question: str) -> QuestionType:
    if not _SUMMARY_WORDS.search(question):
        return "retrieval"
    if _ABOUT_SUMMARIES.search(question):
        return "retrieval"
    return "summary"
