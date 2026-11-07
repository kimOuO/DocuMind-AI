"""Build graphrag-structure.json from the LaTeX source of arXiv:2404.16130v2.

Usage: python build_graphrag_structure.py <dir with the .tex files>

The cells of Tables 2, 3, 4 and 6 (community_table.tex, claim_comp_table.tex,
claim_div_table.tex, stats_table.tex), each with the labels the chunker's linearisation
gives them — (row, group, column) or (row, column) — so that
evaluation/table-generalization/check_cells.py can compare what the PDF parser and the
table linearizer produce against the paper's own source, independent of any PDF parsing.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TEX = re.compile(
    r"\\(?:textbf|textless|small|centering|multirow\{\d+\}\{\*\}|multicolumn\{\d+\}\{\w+\})"
)


def clean(cell: str) -> str:
    cell = cell.replace("\\textless", "<").replace("\\%", "%")
    cell = re.sub(
        r"\\(?:textbf|multirow\{\d+\}\{\*\}|multicolumn\{\d+\}\{\w+\})\s*\{", "{", cell
    )
    cell = re.sub(r"\\[a-zA-Z]+", "", cell)
    cell = cell.replace("{", "").replace("}", "")
    return " ".join(cell.split())


def rows_of(tex: str) -> list[list[str]]:
    """The body rows of the first tabular environment: lists of cleaned cells."""
    body = tex[tex.index("\\begin{tabular") : tex.index("\\end{tabular")]
    body = body.split("\n", 1)[1]
    rows = []
    for raw in re.split(r"\\\\", body):
        raw = re.sub(
            r"\\(?:hline|toprule|midrule|bottomrule|cmidrule(?:\([^)]*\))?\{[^}]*\})",
            " ",
            raw,
        )
        if "&" not in raw:
            continue
        rows.append([clean(c) for c in raw.split("&")])
    return rows


def table2(tex: str) -> list[dict]:
    rows = rows_of(tex)
    groups = ["Podcast Transcripts", "News Articles"]
    subs = ["C0", "C1", "C2", "C3", "TS"]
    cells = []
    for row in rows:
        if row[0] in ("Units", "Tokens", "% Max"):
            for i, value in enumerate(row[1:11]):
                cells.append(
                    {
                        "table": "Table 2",
                        "row": row[0],
                        "group": groups[i // 5],
                        "column": subs[i % 5],
                        "value": value,
                    }
                )
    return cells


def table3(tex: str) -> list[dict]:
    cells = []
    for row in rows_of(tex):
        if row[0] in ("C0", "C1", "C2", "C3", "TS", "SS"):
            for column, value in zip(
                ["News Articles", "Podcast Transcripts"], row[1:3], strict=True
            ):
                cells.append(
                    {
                        "table": "Table 3",
                        "row": row[0],
                        "group": "",
                        "column": column,
                        "value": value,
                    }
                )
    return cells


def table4(tex: str) -> list[dict]:
    cells = []
    subs = ["C0", "C1", "C2", "C3", "TS", "SS"]
    group = ""
    for row in rows_of(tex):
        if len(row) < 8:
            continue
        if row[0]:
            group = row[0]
        if re.fullmatch(r"0\.\d", row[1]):
            for column, value in zip(subs, row[2:8], strict=True):
                cells.append(
                    {
                        "table": "Table 4",
                        "row": row[1],
                        "group": group,
                        "column": column,
                        "value": value,
                    }
                )
    return cells


def table6(tex: str) -> list[dict]:
    cells = []
    groups = ["Podcast Transcripts", "News Articles"]
    subs = ["Mean 1", "Mean 2", "Z-value", "p-value"]
    metric = ""
    for row in rows_of(tex):
        if len(row) < 11:
            continue
        if row[0]:
            metric = row[0]
        c1, c2 = row[1], row[2]
        if not re.fullmatch(r"(?:C[0-3]|TS|SS)", c1):
            continue
        for i, value in enumerate(row[3:11]):
            cells.append(
                {
                    "table": "Table 6",
                    "row": f"{metric} / {c1} {c2}",
                    "group": groups[i // 4],
                    "column": subs[i % 4],
                    "value": value,
                }
            )
    return cells


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    tex_dir = Path(sys.argv[1])
    read = lambda name: (tex_dir / name).read_text(encoding="utf-8")
    cells = (
        table2(read("community_table.tex"))
        + table3(read("claim_comp_table.tex"))
        + table4(read("claim_div_table.tex"))
        + table6(read("stats_table.tex"))
    )
    out = {
        "source": "LaTeX source of arXiv:2404.16130v2 (https://arxiv.org/e-print/2404.16130v2)",
        "labels": "row, group ('' for one-level tables), column — as evaluation/../tables.cells_of gives them",
        "cells": cells,
    }
    (HERE / "graphrag-structure.json").write_text(
        json.dumps(out, indent=1, ensure_ascii=False) + "\n"
    )
    by_table: dict[str, int] = {}
    for c in cells:
        by_table[c["table"]] = by_table.get(c["table"], 0) + 1
    print(by_table)


if __name__ == "__main__":
    main()
