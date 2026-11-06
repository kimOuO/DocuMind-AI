"""Replay the saved real answers through the AC-26 label check, before and after D67.

Every table figure in the answers of answers.json was labelled by hand against
Table 1 and Table 2 (evaluation/ground-truth/paper-structure.json): correct, or
wrong with the actual cell. The check's verdict for each figure is compared with
that label:

  TP  wrong figure, check says contradicted
  FP  correct figure, check says contradicted
  FN  wrong figure, check lets it through (supported, unchecked, or, before
      D67, silently passed)
  TN  correct figure, check lets it through
  UNRESOLVED  check says it cannot decide (after D67 only); split by label

"Before" is the check as committed in 21752a2 (D64 rules, two outcomes), loaded
from git so that no copy of old code is kept here. "After" is the check in the
working tree. The pages are the paper's pages 7-9 as the ingestion pipeline
rewrites them (table regions linearised), the same text the check sees in
production.

Usage (from the repository root, inside the project's venv):
    .venv/bin/python evaluation/number-check/replay.py

Writes before.results.json and after.results.json next to this script and
prints the summary table of README.md.
"""

from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BACKEND = ROOT / "app" / "backend"
sys.path.insert(0, str(BACKEND))

from app.chat import verification
from app.ingestion.parsing import parse_document
from app.ingestion.tables import find_table_regions, linearize_table

PDF = ROOT / "sample-documents" / "2410.05779v3.pdf"
BEFORE_COMMIT = "21752a2"
PAGES = (7, 8, 9)
NUMBER = re.compile(r"(?<![\w.,])(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?%?")
CITATION = re.compile(r"\[\s*\d{1,3}(?:\s*,\s*\d{1,3})*\s*\]")


def pages_as_ingested() -> list[verification.PageText]:
    document = uuid.uuid4()
    pages = []
    for page in parse_document(PDF, "pdf"):
        if page.number not in PAGES:
            continue
        text, lines = page.text, page.text.splitlines()
        for start, end in find_table_regions(page.text):
            region = "\n".join(lines[start:end])
            text = text.replace(region, linearize_table(region))
        pages.append(verification.PageText(document, page.number, text))
    return pages


def load_before():  # type: ignore[no-untyped-def]
    source = subprocess.run(
        ["git", "show", f"{BEFORE_COMMIT}:app/backend/app/chat/verification.py"],
        check=True,
        capture_output=True,
        text=True,
        cwd=ROOT,
    ).stdout
    spec = importlib.util.spec_from_loader("verification_before", loader=None)
    module = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
    sys.modules[module.__name__] = module  # dataclasses look the module up by name
    # The old module is executed from git history on purpose, so that no copy is kept.
    exec(compile(source, "verification@" + BEFORE_COMMIT, "exec"), module.__dict__)  # noqa: S102
    return module


def occurrence(answer: str, number: str, position: int) -> int:
    """The 1-based index of this figure among the occurrences of the same number."""
    blanked = CITATION.sub(lambda m: " " * len(m.group()), answer)
    return 1 + sum(
        1 for m in NUMBER.finditer(blanked, 0, position) if m.group() == number
    )


def table_values(pages: list[verification.PageText]) -> set[str]:
    return set(verification._table_cells(pages))


def figures_of(answer: str, values: set[str]) -> list[tuple[str, int, int]]:
    """(number, occurrence, position) of every table-valued figure in the answer."""
    blanked = CITATION.sub(lambda m: " " * len(m.group()), answer)
    found = []
    for m in NUMBER.finditer(blanked):
        if verification._key(m.group()) in values:
            found.append(
                (m.group(), occurrence(answer, m.group(), m.start()), m.start())
            )
    return found


def classify(truth: str, status: str) -> str:
    if status == "contradicted":
        return "TP" if truth == "wrong" else "FP"
    if status == "unresolved":
        return "UNRESOLVED-wrong" if truth == "wrong" else "UNRESOLVED-correct"
    return "FN" if truth == "wrong" else "TN"


def main() -> None:
    here = Path(__file__).resolve().parent
    answers = json.loads((here / "answers.json").read_text())
    pages = pages_as_ingested()
    values = table_values(pages)
    before = load_before()

    runs = {"before": [], "after": []}
    for entry in answers:
        answer = entry["answer"]
        wrong = {
            (w["number"], w["occurrence"]): w["why"] for w in entry["wrong_figures"]
        }
        figures = figures_of(answer, values)
        if len(figures) != entry["table_figures"]:
            raise SystemExit(
                f"{entry['id']}: {len(figures)} table figures found, "
                f"{entry['table_figures_listed']} were labelled"
            )
        # After: one outcome per figure, matched by position.
        after_by_position = {
            o.position: o for o in verification.label_outcomes(answer, pages)
        }
        # Before: only contradictions were reported, each (number, sentence) once.
        reported = {(m.number, m.sentence) for m in before.check_labels(answer, pages)}
        for number, index, position in figures:
            truth = "wrong" if (number, index) in wrong else "correct"
            outcome = after_by_position[position]
            runs["after"].append(
                {
                    "answer": entry["id"],
                    "number": number,
                    "occurrence": index,
                    "truth": truth,
                    "why_wrong": wrong.get((number, index)),
                    "status": outcome.status,
                    "reason": outcome.reason,
                    "answer_labels": outcome.answer_labels,
                    "source_labels": outcome.source_labels,
                    "sentence": outcome.sentence,
                    "class": classify(truth, outcome.status),
                }
            )
            before_status = (
                "contradicted" if (number, outcome.sentence) in reported else "passed"
            )
            runs["before"].append(
                {
                    "answer": entry["id"],
                    "number": number,
                    "occurrence": index,
                    "truth": truth,
                    "status": before_status,
                    "sentence": outcome.sentence,
                    "class": classify(truth, before_status),
                }
            )

    summary = {}
    for name, rows in runs.items():
        counts = {
            k: 0
            for k in ("TP", "FP", "FN", "TN", "UNRESOLVED-wrong", "UNRESOLVED-correct")
        }
        for row in rows:
            counts[row["class"]] += 1
        tp, fp, fn = counts["TP"], counts["FP"], counts["FN"]
        decided = tp + fp + fn + counts["TN"]
        summary[name] = {
            **counts,
            "figures": len(rows),
            "wrong_figures": sum(1 for r in rows if r["truth"] == "wrong"),
            "precision": round(tp / (tp + fp), 3) if tp + fp else None,
            "recall": round(tp / (tp + fn), 3) if tp + fn else None,
            # Strict: a wrong figure the check left unresolved was not caught either.
            "recall_strict": round(tp / (tp + fn + counts["UNRESOLVED-wrong"]), 3)
            if tp + fn + counts["UNRESOLVED-wrong"]
            else None,
            "unresolved_rate": round((len(rows) - decided) / len(rows), 3)
            if rows
            else None,
            "unresolved_missing": sum(1 for r in rows if r.get("reason") == "missing"),
            "unresolved_ambiguous": sum(
                1 for r in rows if r.get("reason") == "ambiguous"
            ),
        }
        config = {
            "check": f"app/backend/app/chat/verification.py at {BEFORE_COMMIT} (D64 rules)"
            if name == "before"
            else "app/backend/app/chat/verification.py in the working tree (D67)",
            "pages": f"{PDF.name} pages {PAGES}, table regions linearised by app.ingestion.tables",
            "ground_truth": "answers.json (hand-labelled against paper-structure.json)",
        }
        (here / f"{name}.results.json").write_text(
            json.dumps(
                {"config": config, "summary": summary[name], "figures": rows},
                indent=1,
                ensure_ascii=False,
            )
            + "\n"
        )

    print(
        f"{len(runs['after'])} table figures in {len(answers)} answers, "
        f"{summary['after']['wrong_figures']} labelled wrong\n"
    )
    print("| | before (D64) | after (D67) |\n|---|---|---|")
    for key in (
        "TP",
        "FP",
        "FN",
        "TN",
        "UNRESOLVED-wrong",
        "UNRESOLVED-correct",
        "precision",
        "recall",
        "recall_strict",
        "unresolved_rate",
        "unresolved_missing",
        "unresolved_ambiguous",
    ):
        print(f"| {key} | {summary['before'][key]} | {summary['after'][key]} |")
    print("\nafter: figures the check got wrong or could not decide")
    for row in runs["after"]:
        if row["class"] in ("FP", "FN") or row["class"].startswith("UNRESOLVED"):
            print(
                f"  {row['class']:<18} {row['answer']} {row['number']:>6} #{row['occurrence']} "
                f"{row['answer_labels']} | {row['sentence'][:110]}"
            )


if __name__ == "__main__":
    main()
