"""Mechanical judging of the stability batches (D93): temperature × repeats.

Reuses evaluation/facts-ab/judge.py for the figure check and the Q2/Q3 marks, and adds
Q1 (the five key points and the error classes), the GraphRAG questions (expected figures
and definitions) and a direction heuristic for Q3's exceptions. The pass/fail judgement
stays human; this prints per-batch counts and writes analysis.json and answers.md.

Run from app/backend with the venv:  python ../../evaluation/stability/judge.py
"""

from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "app" / "backend"))
sys.path.insert(0, str(ROOT / "evaluation" / "number-check"))
sys.path.insert(0, str(ROOT / "evaluation" / "facts-ab"))

from judge import judge as base_judge
from judge import model_text, sentences
from replay import pages_as_ingested, table_values

HERE = Path(__file__).resolve().parent
RUNS = HERE / "runs"

Q1_POINTS = {
    "S1 problem": re.compile(
        r"flat|fragment|contextual awareness|扁平|碎片|片段化|脈絡", re.IGNORECASE
    ),
    "S2 graph": re.compile(r"graph|圖", re.IGNORECASE),
    "S3 dual-level": re.compile(
        r"dual[- ]level|low[- ]level|high[- ]level|雙層|低層|高層", re.IGNORECASE
    ),
    "S4 incremental": re.compile(r"incremental|增量|新資料|new data", re.IGNORECASE),
    "S5 result": re.compile(
        r"comprehensiveness|diversity|empowerment|win rate|全面|多樣|勝率",
        re.IGNORECASE,
    ),
}
G_EXPECTED = {
    "G1": ["34", "26,657", "1,669", "1,014,611", "55", "39,770", "3,197", "1,707,694"],
    "G2": ["77.76", "22.24", "79.2", "20.8"],
    "G3": ["8,564", "20,691", "15,754", "19,520"],
    "G4": [],
}
G4_TERMS = ["C0", "C1", "C2", "C3", "TS", "SS"]
# Table 2's exceptions: the variant above LightRAG in that condition. A sentence that holds
# the pair's figures and says the variant does worse/lower/drops is a reversed direction.
Q3_EXCEPTIONS = [
    ("-High", "CS", "Diversity", "63.2%", "62.0%"),
    ("-Low", "Mix", "Comprehensiveness", "64.0%", "61.2%"),
    ("-Low", "Mix", "Empowerment", "64.8%", "57.2%"),
    ("-Low", "Mix", "Overall", "64.8%", "60.0%"),
    ("-Origin", "Agriculture", "Comprehensiveness", "75.2%", "67.6%"),
    ("-Origin", "Mix", "Diversity", "74.4%", "67.6%"),
    ("-Origin", "Agriculture", "Empowerment", "68.0%", "67.6%"),
    ("-Origin", "Agriculture", "Overall", "74.4%", "67.6%"),
]
WORSE = re.compile(
    r"\b(worse|underperform\w*|lower|drops?|declin\w*|below|lags?|trails?)\b",
    re.IGNORECASE,
)
DEF_WRONG = {
    "-High": re.compile(
        r"-High[^.]{0,40}(high-level-only|only high|high-level retrieval only|uses only high)",
        re.IGNORECASE,
    ),
    "-Low": re.compile(
        r"-Low[^.]{0,40}(low-level-only|only low|low-level retrieval only|uses only low)",
        re.IGNORECASE,
    ),
    "-Origin": re.compile(
        r"-Origin[^.]{0,60}(uses the original text|using the original text|with original text|retains? the original)",
        re.IGNORECASE,
    ),
}


def q3_direction_slips(text: str) -> list[str]:
    slips = []
    for variant, group, row, v_variant, v_light in Q3_EXCEPTIONS:
        for s in sentences(text):
            if v_variant in s and v_light in s and variant in s and WORSE.search(s):
                # the variant is named with "worse"-words in a sentence carrying the pair:
                # reversed unless the sentence says LightRAG is the one below
                if not re.search(
                    r"LightRAG[^.]{0,30}" + WORSE.pattern, s, re.IGNORECASE
                ):
                    slips.append(f"{group}/{row}: {s[:120]}")
                break
    return slips


def main() -> None:
    pages = pages_as_ingested()
    values = table_values(pages)
    records = [
        json.loads(p.read_text())
        for p in sorted(RUNS.glob("*-Q*-*.json")) + sorted(RUNS.glob("*-G*-*.json"))
    ]
    results = []
    for r in records:
        j = base_judge(r, pages, values)
        text = model_text(r["final_answer"] or "")
        q = r["question"]
        if q == "Q1":
            j["q1_points"] = {k: bool(p.search(text)) for k, p in Q1_POINTS.items()}
            j["q1_points_count"] = sum(j["q1_points"].values())
        if q == "Q3":
            j["direction_slips"] = q3_direction_slips(text)
            j["definition_wrong"] = [k for k, p in DEF_WRONG.items() if p.search(text)]
        if q in G_EXPECTED:
            expected = G_EXPECTED[q]
            j["expected_present"] = [
                n for n in expected if n in text or n.replace(",", "") in text
            ]
            j["expected_missing"] = [
                n for n in expected if n not in text and n.replace(",", "") not in text
            ]
            if q == "G4":
                j["g4_terms"] = [t for t in G4_TERMS if re.search(rf"\b{t}\b", text)]
        results.append(j)
    (HERE / "analysis.json").write_text(
        json.dumps(results, indent=1, ensure_ascii=False) + "\n"
    )
    lines = ["# D93 stability batches — every answer\n"]
    for r, j in zip(records, results, strict=True):
        lines.append(f"## {r['arm']}-{r['question']}-{r['run']}\n")
        lines.append(
            json.dumps(
                {k: v for k, v in j.items() if k not in ("arm", "question", "run")},
                ensure_ascii=False,
            )
            + "\n"
        )
        lines.append((r["final_answer"] or "(no answer)") + "\n")
    (HERE / "answers.md").write_text("\n".join(lines))

    by = defaultdict(list)
    for j in results:
        by[(j["arm"], j["question"])].append(j)
    print(
        "| batch | n | figures (avg) | mislabelled>0 | universal wording | question marks |"
    )
    print("|---|---|---|---|---|---|")
    for (arm, q), js in sorted(by.items()):
        n = len(js)
        figs = sum(j["table_figures"] for j in js) / n
        misl = sum(1 for j in js if j["figures_mislabelled"])
        uni = sum(1 for j in js if j["universal_wording"])
        if q == "Q1":
            mark = f"S1–S5 all present {sum(1 for j in js if j['q1_points_count'] == 5)}/{n}"
        elif q == "Q2":
            mark = f"Mix exceptions 3/3 in {sum(1 for j in js if j['mix_exceptions_count'] == 3)}/{n}"
        elif q == "Q3":
            mark = (
                f"defs 3/3 in {sum(1 for j in js if sum(j['definitions'].values()) == 3)}/{n}; "
                f"direction slips in {sum(1 for j in js if j['direction_slips'])}/{n}; "
                f"definition wrong in {sum(1 for j in js if j['definition_wrong'])}/{n}; "
                f"own figures>0 in {sum(1 for j in js if j['lightrag_own_figures'])}/{n}"
            )
        elif q == "G4":
            mark = f"six conditions named in {sum(1 for j in js if len(j['g4_terms']) == 6)}/{n}"
        else:
            mark = f"all expected figures in {sum(1 for j in js if not j['expected_missing'])}/{n}"
        print(f"| {arm}-{q} | {n} | {figs:.0f} | {misl} | {uni} | {mark} |")


if __name__ == "__main__":
    main()
