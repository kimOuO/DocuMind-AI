"""Measure how a chunking method splits Table 2 of the LightRAG paper.

Table 2 is what the third required question ("Performance of ablated versions
of LightRAG") must be answered from. Fixed-size chunking cuts it into several
chunks; this script measures, for every table row, whether some chunk holds the whole
row together with the headers needed to read it, and saves the chunks of that
page. One output file per method, <method>.table2-rows.json, so that the
methods tried for acceptance criterion AC-14 (P3) can be compared side by side.

Usage (from the repository root, inside the project's virtual environment):
    python evaluation/table2-chunking/measure_table2_rows.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "app" / "backend"))

from app.core.env_loader import get_settings
from app.ingestion.chunking import chunk_pages
from app.ingestion.parsing import parse_document
from app.llm.tokenizer import Qwen3TokenCounter

PAPER = ROOT / "sample-documents" / "2410.05779v3.pdf"
TRUTH = ROOT / "evaluation" / "ground-truth" / "paper-structure.json"
DATASET_HEADER = "Agriculture CS Legal Mix"


def _row_line(text: str, metric: str, values: list[str]) -> str | None:
    """The line of the chunk that holds the metric and all its values in order, if any."""
    for line in text.splitlines():
        if not line.startswith(metric):
            continue
        position = 0
        for value in values:
            position = line.find(value, position)
            if position < 0:
                break
            position += len(value)
        else:
            return line
    return None


def _row_in(text: str, metric: str, values: list[str]) -> bool:
    return _row_line(text, metric, values) is not None


def _row_labelled(text: str, metric: str, values: list[str], *labels: str) -> bool:
    """The row's own line carries the labels (the cell-by-cell form)."""
    line = _row_line(text, metric, values)
    return line is not None and all(label in line for label in labels)


def main() -> None:
    settings = get_settings()
    pages = parse_document(PAPER, "pdf")
    chunks = chunk_pages(
        pages,
        Qwen3TokenCounter(),
        chunk_size=settings.chunk_size,
        overlap=settings.chunk_overlap,
    )
    table_page = next(
        p.number for p in pages if "Table 2: Performance of ablated" in p.text
    )
    page_chunks = [chunk for chunk in chunks if chunk.page == table_page]

    rows: dict[tuple[int, str], dict] = {}
    for cell in json.loads(TRUTH.read_text(encoding="utf-8"))["table2"]:
        row = rows.setdefault(
            (cell["block"], cell["metric"]),
            {"variant": cell["variant"], "metric": cell["metric"], "values": []},
        )
        row["values"].append(cell["value"])

    summary = []
    for row in rows.values():
        line = " ".join([row["metric"], *row["values"]])
        block_header = " ".join(["NaiveRAG", row["variant"]] * 4)
        # A row is whole in a chunk when its metric and its eight values appear in order
        # on one line of the chunk: as pypdf wrote it, or rewritten cell by cell.
        holding = [
            chunk
            for chunk in page_chunks
            if _row_in(chunk.text, row["metric"], row["values"])
        ]
        summary.append(
            {
                "variant": row["variant"],
                "metric": row["metric"],
                "row": line,
                "chunks_with_whole_row": [chunk.ordinal for chunk in holding],
                "with_block_header": [
                    c.ordinal
                    for c in holding
                    if block_header in c.text
                    or _row_labelled(
                        c.text, row["metric"], row["values"], row["variant"]
                    )
                ],
                "with_dataset_header": [
                    c.ordinal
                    for c in holding
                    if DATASET_HEADER in c.text
                    or _row_labelled(
                        c.text, row["metric"], row["values"], *DATASET_HEADER.split()
                    )
                ],
            }
        )

    # The current implementation keeps table regions whole (app/ingestion/tables.py);
    # the fixed-size-only baseline measured before that change is kept as its own file.
    method = f"table-region-linearized-{settings.chunk_size}-{settings.chunk_overlap}"
    result = {
        "method": {
            "name": method,
            "description": "Table regions (caption, headers, number rows) kept as one chunk "
            "of up to 4 x chunk size, each row rewritten cell by cell with its column labels; "
            "the rest in fixed-size chunks measured in tokens, page by page, consecutive "
            "chunks overlapping.",
            "chunk_size_tokens": settings.chunk_size,
            "overlap_tokens": settings.chunk_overlap,
            "table_chunk_max_tokens": 4 * settings.chunk_size,
            "pdf_parser": "pypdf default",
            "implementation": "app/ingestion/chunking.py, app/ingestion/tables.py",
        },
        "measurements": {
            "total_chunks": len(chunks),
            "table_page": table_page,
            "rows_total": len(summary),
            "rows_whole_in_some_chunk": sum(
                bool(r["chunks_with_whole_row"]) for r in summary
            ),
            "rows_with_block_header": sum(
                bool(r["with_block_header"]) for r in summary
            ),
            "rows_with_dataset_header": sum(
                bool(r["with_dataset_header"]) for r in summary
            ),
            "rows": summary,
        },
        "page_chunks": [
            {"ordinal": c.ordinal, "token_count": c.token_count, "text": c.text}
            for c in page_chunks
        ],
    }
    (HERE / f"{method}.table2-rows.json").write_text(
        json.dumps(result, indent=1, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    print(
        f"chunk {settings.chunk_size} / overlap {settings.chunk_overlap}: {len(chunks)} chunks, Table 2 on page {table_page}"
    )
    for chunk in page_chunks:
        print(
            f"  chunk #{chunk.ordinal}: {chunk.token_count} tokens | starts {chunk.text[:40]!r} | ends {chunk.text[-40:]!r}"
        )
    whole = sum(bool(r["chunks_with_whole_row"]) for r in summary)
    block = sum(bool(r["with_block_header"]) for r in summary)
    dataset = sum(bool(r["with_dataset_header"]) for r in summary)
    print(
        f"rows whole in some chunk: {whole}/16 | together with their block header: {block}/16 | together with the dataset header: {dataset}/16"
    )
    for r in summary:
        print(
            f"  {r['variant']:9} {r['metric']:18} whole in {r['chunks_with_whole_row']} block header in {r['with_block_header']} dataset header in {r['with_dataset_header']}"
        )


if __name__ == "__main__":
    main()
