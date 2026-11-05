"""Build the ground truth for the PDF parser comparison from the paper's LaTeX source.

The ground truth must not depend on any of the PDF parsers under test, so it is
derived from the LaTeX source that arXiv publishes for the same version of the
paper (https://arxiv.org/e-print/2410.05779v3).

Usage:
    python build_ground_truth.py <directory containing the extracted .tex files>

Writes ground_truth.json next to this script, containing:
  - table2:   every cell of Table 2 (block, metric, dataset, system, value)
  - headings: section and subsection titles in document order
  - anchors:  one short phrase per body paragraph, in document order
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

# Body files in the order main.tex includes them. References come from main.bbl
# and are not checked; the appendix is checked for headings only, because most
# of its content is figures.
BODY_FILES = ["intro", "model", "solution", "eval", "relate", "conclusion"]
HEADING_FILES = [*BODY_FILES, "appendix"]

MODEL_NAME = "LightRAG"  # \def\model{LightRAG} in main.tex
DATASETS = ["Agriculture", "CS", "Legal", "Mix"]
METRICS = ["Comprehensiveness", "Diversity", "Empowerment", "Overall"]
ANCHOR_WORDS = 8

FLOAT_ENVIRONMENTS = ["table", "figure", "wrapfigure", "align", "equation", "tabular"]
PLAIN_WORD = r"[A-Za-z]+(?:-[A-Za-z]+)*"
PLAIN_RUN = re.compile(
    rf"(?<![\\{{}}$~^_\w-]){PLAIN_WORD}(?:[ \n]{PLAIN_WORD}){{{ANCHOR_WORDS - 1}}}(?![\w{{}}$^_-])"
)


def strip_comments(tex: str) -> str:
    """Remove LaTeX comments (an unescaped % to the end of the line)."""
    return "\n".join(re.sub(r"(?<!\\)%.*$", "", line) for line in tex.splitlines())


def clean_title(title: str) -> str:
    title = title.replace("\\model\\", MODEL_NAME).replace("\\model", MODEL_NAME)
    title = re.sub(r"\\[a-zA-Z]+\{([^}]*)\}", r"\1", title)
    return re.sub(r"\s+", " ", title).strip(" .")


def read_headings(tex_dir: Path) -> list[dict[str, str]]:
    headings = []
    for name in HEADING_FILES:
        tex = strip_comments((tex_dir / f"{name}.tex").read_text(encoding="utf-8"))
        for level, title in re.findall(
            r"\\(section|subsection)\{((?:[^{}]|\{[^{}]*\})*)\}", tex
        ):
            headings.append({"file": name, "level": level, "title": clean_title(title)})
    return headings


def anchors_from_files(paths: list[Path]) -> list[dict[str, str]]:
    """One phrase of plain words from each body paragraph, in document order.

    Floats and equations are removed first because LaTeX moves them, so their
    position in the source says nothing about their position on the page.
    """
    anchors = []
    for path in paths:
        tex = strip_comments(path.read_text(encoding="utf-8"))
        for env in FLOAT_ENVIRONMENTS:
            tex = re.sub(
                rf"\\begin\{{{env}\*?\}}.*?\\end\{{{env}\*?\}}",
                "\n\n",
                tex,
                flags=re.DOTALL,
            )
        tex = re.sub(
            r"\\(section|subsection|subsubsection|paragraph)\{(?:[^{}]|\{[^{}]*\})*\}",
            "\n\n",
            tex,
        )
        for paragraph in re.split(r"\n\s*\n|\\item\b", tex):
            match = PLAIN_RUN.search(paragraph)
            if match:
                phrase = re.sub(r"\s+", " ", match.group(0))
                anchors.append({"file": path.stem, "phrase": phrase})
    return anchors


def read_anchors(tex_dir: Path) -> list[dict[str, str]]:
    return anchors_from_files([tex_dir / f"{name}.tex" for name in BODY_FILES])


def read_table2(tex_dir: Path) -> list[dict[str, str | int]]:
    tex = strip_comments((tex_dir / "eval.tex").read_text(encoding="utf-8"))
    table = re.search(
        r"\\label\{tab:ablation\}.*?\\end\{tabular\}", tex, flags=re.DOTALL
    )
    if table is None:
        raise SystemExit("Table 2 (tab:ablation) not found in eval.tex")

    cells: list[dict[str, str | int]] = []
    block_index = -1
    variant = ""
    for row in table.group(0).split("\\\\"):
        row = re.sub(
            r"\\(cmidrule\(lr\)\{[^}]*\}|midrule|toprule|bottomrule)", "", row
        ).strip()
        fields = [
            re.sub(r"\\(textbf|underline)\{([^}]*)\}", r"\2", f).strip()
            for f in row.split("&")
        ]
        fields = [f.replace("\\model", MODEL_NAME).replace("\\%", "%") for f in fields]
        if len(fields) == 9 and fields[1] == "NaiveRAG":
            block_index += 1
            variant = fields[2]
            if fields[1:] != ["NaiveRAG", variant] * 4:
                raise SystemExit(f"unexpected sub-header: {fields}")
        elif len(fields) == 9 and fields[0] in METRICS:
            for column, value in enumerate(fields[1:]):
                cells.append(
                    {
                        "block": block_index,
                        "variant": variant,
                        "metric": fields[0],
                        "dataset": DATASETS[column // 2],
                        "system": "NaiveRAG" if column % 2 == 0 else variant,
                        "value": value,
                    }
                )
    if len(cells) != 4 * len(METRICS) * 8:
        raise SystemExit(f"expected 128 cells, found {len(cells)}")
    return cells


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    tex_dir = Path(sys.argv[1])
    truth = {
        "source": "LaTeX source of arXiv:2410.05779v3 (https://arxiv.org/e-print/2410.05779v3)",
        "table2": read_table2(tex_dir),
        "headings": read_headings(tex_dir),
        "anchors": read_anchors(tex_dir),
    }
    out = Path(__file__).with_name("ground_truth.json")
    out.write_text(
        json.dumps(truth, indent=1, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"table2 cells: {len(truth['table2'])}")
    print(f"headings:     {len(truth['headings'])}")
    print(f"anchors:      {len(truth['anchors'])}")
    print(f"written to {out}")


if __name__ == "__main__":
    main()
