"""Supplementary check: reading order on a two-column paper.

The LightRAG paper is single-column, so it cannot show whether a parser reads
two columns in the right order. This script runs the same paragraph-order check
on any paper whose LaTeX source is available.

Usage:
    python check_reading_order.py <pdf> <tex file> [<tex file> ...] [--libs <dir>] [--label <name>]

The .tex files are given in the order the paper includes them. Writes
results_reading_order.json next to this script.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from build_ground_truth import anchors_from_files


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf")
    parser.add_argument("tex", nargs="+")
    parser.add_argument("--libs")
    parser.add_argument("--label", default="")
    args = parser.parse_args()
    if args.libs:
        sys.path.insert(0, args.libs)
    import compare_parsers as cp

    anchors = anchors_from_files([Path(p) for p in args.tex])
    rows = {
        name: cp.check_anchors(extract(args.pdf), anchors)["rows"]
        for name, (_, _, extract) in cp.CONFIGS.items()
    }
    in_document = [
        any(rows[n][i]["position"] >= 0 for n in rows) for i in range(len(anchors))
    ]

    report = {
        "paper": args.label or Path(args.pdf).name,
        "anchors_from_latex": len(anchors),
        "anchors_in_document": sum(in_document),
        "configs": {},
    }
    for name, config_rows in rows.items():
        usable = [row for row, present in zip(config_rows, in_document) if present]
        found = [row for row in usable if row["position"] >= 0]
        unique = [row["position"] for row in found if row["occurrences"] == 1]
        report["configs"][name] = {
            "found": len(found),
            "intact": sum(row["intact"] for row in usable),
            "out_of_order": len(unique) - cp.longest_increasing(unique),
            "not_found": [row["phrase"] for row in usable if row["position"] < 0][:5],
        }
        print(
            f"{name:20} found {len(found)}/{len(usable)}  intact {report['configs'][name]['intact']}/{len(usable)}  out of order {report['configs'][name]['out_of_order']}"
        )
    Path(__file__).with_name("results_reading_order.json").write_text(
        json.dumps(report, indent=1, ensure_ascii=False) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
