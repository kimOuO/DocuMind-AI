"""Mechanical part of judging experiment A (D87): for every record in runs/, the table
figures in the answer checked cell by cell against the paper's tables as ingested, the
program's own checks, the universal-claim wording, and the question-specific marks
(Q2: are the three Mix exceptions named; Q3: are the variants defined, are LightRAG's own
figures given, are there figures at all). The pass/fail judgement stays human (README),
this script only lays out what it is made from. Writes analysis.json and answers.md.

Run from the backend venv:  python ../../evaluation/facts-ab/judge.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "app" / "backend"))
sys.path.insert(0, str(ROOT / "evaluation" / "number-check"))

from app.chat import verification
from replay import figures_of, pages_as_ingested, table_values

HERE = Path(__file__).resolve().parent
RUNS = HERE / "runs"
UNIVERSAL = re.compile(
    r"\b(consistently|across all|all (?:four )?(?:datasets|metrics|dimensions)|in all|every|"
    r"only (?:exception|regression|case)|without exception|uniformly)\b",
    re.IGNORECASE,
)
# Table 1, GraphRAG block: the three cells where GraphRAG is above LightRAG (all in Mix).
Q2_EXCEPTIONS = {
    "Comprehensiveness": ("50.4%", "49.6%"),
    "Empowerment": ("50.8%", "49.2%"),
    "Overall": ("50.4%", "49.6%"),
}
Q3_DEFINITIONS = {
    "-High": re.compile(r"high-?(?:level|order)", re.IGNORECASE),
    "-Low": re.compile(r"low-?(?:level|order)", re.IGNORECASE),
    "-Origin": re.compile(r"original text", re.IGNORECASE),
}
LIGHTRAG_TABLE2 = {
    "67.6%",
    "61.6%",
    "83.6%",
    "61.2%",
    "76.4%",
    "62.0%",
    "86.4%",
    "84.8%",
    "60.0%",
}
SENTENCE = re.compile(r"(?<=[.!?])\s+")
NOTE_PREFIX = re.compile(
    r"^(A claim the source table does not bear out|以下結論與原文表格不符|"
    r"Figures whose labels differ from the source table|以下數字的標籤與原文表格不符|"
    r"Numbers that could not be checked against the cited pages|"
    r"以下數字未能在引用的原文頁面中核對)",
)


def sentences(text: str) -> list[str]:
    return [s.strip() for s in SENTENCE.split(text) if s.strip()]


def q2_exceptions(answer: str) -> dict[str, bool]:
    """A Mix exception counts as named when one sentence has "Mix", the metric and both
    figures of the pair, or "Mix" and the metric with words of GraphRAG being ahead."""
    named = {}
    for metric, pair in Q2_EXCEPTIONS.items():
        hit = False
        for s in sentences(answer):
            if "mix" not in s.lower() or metric.lower() not in s.lower():
                continue
            # Listing LightRAG's figures metric by metric is not naming an exception: the
            # sentence must hold both figures of the pair, or say that GraphRAG is ahead.
            if all(v in s for v in pair) or re.search(
                r"graphrag[^.]*(?:outperform|ahead|higher|better|edge|lead|win)|"
                r"(?:regress|lower|lag|behind|loses|trail|exception|underperform)",
                s,
                re.IGNORECASE,
            ):
                hit = True
                break
        named[metric] = hit
    return named


def model_text(final_answer: str) -> str:
    """The answer without the notes the program appends after it (the label, figure and
    claim notes): the judgement is of what the model wrote."""
    paragraphs = final_answer.split("\n\n")
    kept = [p for p in paragraphs if not NOTE_PREFIX.match(p.strip())]
    return "\n\n".join(kept)


def judge(record: dict, pages: list[verification.PageText], values: set[str]) -> dict:
    answer = model_text(record["final_answer"] or "")
    question = record["question"]
    done = record.get("done") or {}
    figures = figures_of(answer, values)
    check = verification.verify_numbers(answer, pages, {})
    out = {
        "arm": record["arm"],
        "question": question,
        "run": record["run"],
        "status": done.get("status", record.get("error")),
        "analysis_status": done.get("analysis_status"),
        "answer_prompt_tokens": next(
            (
                c["prompt_tokens"]
                for c in record["llm_calls"]
                if c["purpose"] == "answer"
            ),
            None,
        ),
        "answer_completion_tokens": next(
            (
                c["completion_tokens"]
                for c in record["llm_calls"]
                if c["purpose"] == "answer"
            ),
            None,
        ),
        "calls": len(record["llm_calls"]),
        "facts": done.get("facts"),
        "table_figures": len(figures),
        "figures_mislabelled": [m.number for m in check.mislabelled],
        "figures_unresolved": [u.number for u in check.unresolved],
        "overstated_by_program": [
            (o.get("sentence") or "")[:90] if isinstance(o, dict) else str(o)[:90]
            for o in done.get("overstated_claims") or []
        ],
        "universal_wording": sorted(
            {m.group().lower() for m in UNIVERSAL.finditer(answer)}
        ),
        "sentences_with_universal_wording": [
            s[:160] for s in sentences(answer) if UNIVERSAL.search(s)
        ],
    }
    if question == "Q2":
        named = q2_exceptions(answer)
        out["mix_exceptions_named"] = named
        out["mix_exceptions_count"] = sum(named.values())
    if question == "Q3":
        out["definitions"] = {
            k: bool(p.search(answer)) for k, p in Q3_DEFINITIONS.items()
        }
        out["lightrag_own_figures"] = sum(
            1 for f, _, _ in figures if f in LIGHTRAG_TABLE2
        )
        out["variant_figures"] = len(figures) - out["lightrag_own_figures"]
    return out


def main() -> None:
    pages = pages_as_ingested()
    values = table_values(pages)
    records = [json.loads(p.read_text()) for p in sorted(RUNS.glob("A*-Q*-*.json"))]
    results = [judge(r, pages, values) for r in records]
    (HERE / "analysis.json").write_text(
        json.dumps(results, indent=1, ensure_ascii=False) + "\n"
    )
    lines = ["# Experiment A — the 36 answers\n"]
    for r, j in zip(records, results, strict=True):
        lines.append(f"## {r['arm']}-{r['question']}-{r['run']}\n")
        lines.append(
            f"status={j['status']} analysis={j['analysis_status']} "
            f"prompt={j['answer_prompt_tokens']} "
            f"completion={j['answer_completion_tokens']} figures={j['table_figures']} "
            f"mislabelled={j['figures_mislabelled']} universal={j['universal_wording']}\n"
        )
        if j.get("facts"):
            lines.append(f"facts: {json.dumps(j['facts'], ensure_ascii=False)}\n")
        lines.append((r["final_answer"] or "(no answer)") + "\n")
    (HERE / "answers.md").write_text("\n".join(lines))
    header = (
        "| record | tokens | figures | mislabelled | universal wording | "
        "Q2 Mix exceptions / Q3 defs+own figures | program status |"
    )
    print(header)
    print("|" + "---|" * 7)
    for j in results:
        extra = (
            f"{j['mix_exceptions_count']}/3"
            if j["question"] == "Q2"
            else (
                f"defs {sum(j['definitions'].values())}/3, own {j['lightrag_own_figures']}, "
                f"variants {j['variant_figures']}"
            )
        )
        print(
            f"| {j['arm']}-{j['question']}-{j['run']} | "
            f"{j['answer_prompt_tokens']}+{j['answer_completion_tokens']} | "
            f"{j['table_figures']} | {len(j['figures_mislabelled'])} | "
            f"{', '.join(j['universal_wording']) or '—'} | "
            f"{extra} | {j['analysis_status']} |"
        )


if __name__ == "__main__":
    main()
