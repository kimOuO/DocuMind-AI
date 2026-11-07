"""Cell-by-cell check of the table pipeline against the papers' own LaTeX sources (D87).

For every table of both sample papers: parse the PDF with the app's parser, detect the
table regions, linearise them as the chunker does, read the cells back with
`cells_of`, and compare (row, group, column, value) with the ground truth built from the
LaTeX source (evaluation/ground-truth/paper-structure.json for LightRAG Tables 1 and 2,
graphrag-structure.json for GraphRAG Tables 2, 3, 4 and 6). Prints a table per paper and
writes results.json. Run from app/backend with the venv:

    python ../../evaluation/table-generalization/check_cells.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "app" / "backend"))

from app.ingestion.parsing import parse_document
from app.ingestion.tables import cells_of, find_table_regions, linearize_table

HERE = Path(__file__).resolve().parent
TRUTH = ROOT / "evaluation" / "ground-truth"
PAPERS = {
    "LightRAG (2410.05779v3)": ROOT / "sample-documents" / "2410.05779v3.pdf",
    "GraphRAG (2404.16130v2)": ROOT / "sample-documents" / "2404.16130v2.pdf",
}
Cell = tuple[str, str, str, str, str]  # table, row, group, column, value


def lightrag_truth() -> set[Cell]:
    structure = json.loads((TRUTH / "paper-structure.json").read_text())
    cells: set[Cell] = set()
    for name in ("table1", "table2"):
        for c in structure[name]:
            cells.add(
                (
                    name.replace("table", "Table "),
                    c["metric"],
                    c["dataset"],
                    c["system"],
                    c["value"],
                )
            )
    return cells


def graphrag_truth() -> set[Cell]:
    structure = json.loads((TRUTH / "graphrag-structure.json").read_text())
    return {
        (c["table"], c["row"], c["group"], c["column"], c["value"])
        for c in structure["cells"]
    }


def parsed_cells(pdf: Path) -> tuple[set[Cell], dict[str, int]]:
    cells: set[Cell] = set()
    detected: dict[str, int] = {}
    for page in parse_document(pdf, "pdf"):
        for start, end in find_table_regions(page.text):
            region = page.text[start:end]
            caption = region.splitlines()[0]
            table = caption.split(":")[0].strip()
            lines = linearize_table(region).splitlines()
            count = 0
            for line in lines:
                for value, labels in cells_of(line):
                    row, group, column = (
                        (labels[0], labels[1], labels[2])
                        if len(labels) == 3
                        else (labels[0], "", labels[1])
                    )
                    cells.add((table, row, group, column, value))
                    count += 1
            detected[table] = detected.get(table, 0) + count
    return cells, detected


def main() -> None:
    results = {}
    for paper, pdf in PAPERS.items():
        truth = lightrag_truth() if "LightRAG" in paper else graphrag_truth()
        found, _ = parsed_cells(pdf)
        tables = sorted({c[0] for c in truth})
        print(f"\n## {paper}\n")
        print(
            "| table | truth cells | parsed cells | matching | missing | wrong or extra |"
        )
        print("|---|---|---|---|---|---|")
        per_table = {}
        for table in tables:
            t = {c for c in truth if c[0] == table}
            f = {c for c in found if c[0] == table}
            matching = t & f
            missing = sorted(t - f)
            extra = sorted(f - t)
            per_table[table] = {
                "truth": len(t),
                "parsed": len(f),
                "matching": len(matching),
                "missing": missing[:20],
                "extra": extra[:20],
            }
            print(
                f"| {table} | {len(t)} | {len(f)} | {len(matching)} | {len(missing)} | {len(extra)} |"
            )
        others = sorted({c[0] for c in found} - set(tables))
        if others:
            print(f"\nTables parsed but without ground truth: {', '.join(others)}")
        results[paper] = {"tables": per_table, "without_truth": others}
    (HERE / "results.json").write_text(
        json.dumps(results, indent=1, ensure_ascii=False) + "\n"
    )


if __name__ == "__main__":
    main()
