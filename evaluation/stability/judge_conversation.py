"""Mechanical checks for the same-conversation runs (D95 follow-up): the three required
questions asked in order in one conversation, temperature 0, ten times, demo deployment.

Per run: the route of each question, Q2's Mix exceptions and any direct pair whose two win
rates do not add up to 100 (the "pairing" error: a LightRAG figure from the NaiveRAG column
put against GraphRAG), Q3's exceptions and variant definitions, and every self-computed
"(+a pp, +b% relative)" recomputed from its two figures. Pass/fail stays a human judgement.
Run from the repository root: python evaluation/stability/judge_conversation.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path

RUNS = Path(__file__).resolve().parent / "conversation-runs"
PCT = re.compile(r"(\d{1,2}\.\d)%")
PAIR = re.compile(
    r"(\d{1,2}\.\d)%\s*(?:vs\.?|compared to|against)\s*(?:[A-Za-z-]+'?s?\s*)?(\d{1,2}\.\d)%"
)
DELTA = re.compile(
    r"(\d{1,2}\.\d)%[^.\n]{0,60}?(\d{1,2}\.\d)%[^.\n]{0,40}?\(\s*\+?(-?\d+\.\d)\s*pp,\s*\+?(-?\d+\.\d)%\s*relative\)"
)
MIX = ["Comprehensiveness", "Empowerment", "Overall"]
DEF_WRONG = re.compile(
    r"-High[^.,]{0,40}(high-level-only|only high|high-level retrieval only|uses only high)|"
    r"-Low[^.,]{0,40}(low-level-only|only low|low-level retrieval only|uses only low)",
    re.IGNORECASE,
)
Q3_EXPECTED = [
    "63.2%",
    "62.0%",
    "64.0%",
    "61.2%",
    "64.8%",
    "57.2%",
    "60.0%",
    "75.2%",
    "74.4%",
    "68.0%",
    "67.6%",
]
Q1_EXPECTED = ["83.6%", "32.4%", "67.6%"]


def arithmetic(answer: str) -> list[str]:
    bad = []
    for a, b, pp, rel in DELTA.findall(answer):
        x, y = float(a), float(b)
        hi, lo = max(x, y), min(x, y)
        if (
            abs(abs(float(pp)) - (hi - lo)) > 0.06
            or abs(abs(float(rel)) - (hi - lo) / lo * 100) > 0.15
        ):
            bad.append(
                f"{a} vs {b}: wrote {pp} pp / {rel}% (true {hi - lo:.1f} pp / {(hi - lo) / lo * 100:.1f}%)"
            )
    return bad


def pairing(answer: str) -> list[str]:
    bad = []
    for line in answer.split("\n"):
        if line.startswith(("Numbers that", "Figures whose")):
            continue
        core = re.sub(r"\([^)]*\)", "", line)
        for a, b in PAIR.findall(core):
            if abs(float(a) + float(b) - 100) > 0.05:
                bad.append(f"{a}% vs {b}%")
    return bad


rows = []
for fn in sorted(RUNS.glob("CONV0-*.json"), key=lambda p: int(p.stem.split("-")[1])):
    r = json.loads(fn.read_text())
    q1, q2, q3 = r["questions"]
    a1, a2, a3 = q1["answer"], q2["answer"], q3["answer"]
    row = {
        "run": r["run"],
        "routes": [q["route"]["type"] if q["route"] else None for q in r["questions"]],
        "standalone": [
            q["route"]["standalone_question"][:60] if q["route"] else None
            for q in r["questions"]
        ],
        "q1_figures_present": sum(f in a1 for f in Q1_EXPECTED),
        "q1_mislabelled": [
            m["number"] for m in (q1["done"] or {}).get("mislabelled_numbers", [])
        ],
        "q2_13of16": "13" in a2 and "16" in a2,
        "q2_mix_named": sum(m in a2 and "Mix" in a2 for m in MIX),
        "q2_pairing": pairing(a2),
        "q2_mislabelled": [
            m["number"] for m in (q2["done"] or {}).get("mislabelled_numbers", [])
        ],
        "q2_arithmetic": arithmetic(a2),
        "q2_facts": ((q2["done"] or {}).get("facts") or {}).get("facts"),
        "q3_expected_present": sum(f in a3 for f in Q3_EXPECTED),
        "q3_def_wrong": bool(DEF_WRONG.search(a3)),
        "q3_mislabelled": [
            m["number"] for m in (q3["done"] or {}).get("mislabelled_numbers", [])
        ],
        "q3_arithmetic": arithmetic(a3),
        "q3_facts": ((q3["done"] or {}).get("facts") or {}).get("facts"),
        "errors": [q["error"] for q in r["questions"] if q["error"]],
        "tokens": [(q["usage"] or {}).get("completion_tokens") for q in r["questions"]],
    }
    rows.append(row)

for row in rows:
    print(json.dumps(row, ensure_ascii=False))
(RUNS / "analysis.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1))
answers = []
for fn in sorted(RUNS.glob("CONV0-*.json"), key=lambda p: int(p.stem.split("-")[1])):
    r = json.loads(fn.read_text())
    for q in r["questions"]:
        answers.append(
            f"## run {r['run']} — {q['question']}\n\nroute: {q['route']}\n\n{q['answer']}\n"
        )
(RUNS / "answers.md").write_text("\n".join(answers))
