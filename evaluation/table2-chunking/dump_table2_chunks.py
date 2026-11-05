"""Record how the current chunking splits Table 2 of the LightRAG paper.

Table 2 is what the third required question ("Performance of ablated versions
of LightRAG") must be answered from. Fixed-size chunking cuts it into several
chunks; this script saves the chunks of that page and summarises, for every
table row, whether a chunk holds the whole row together with the headers needed
to read it. The output is the baseline for acceptance criterion AC-14 (P3).

Usage (from the repository root, inside the project's virtual environment):
    python evaluation/table2-chunking/dump_table2_chunks.py
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
TRUTH = ROOT / "evaluation" / "pdf-parser-comparison" / "ground_truth.json"
DATASET_HEADER = "Agriculture CS Legal Mix"


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
        holding = [chunk for chunk in page_chunks if line in chunk.text]
        summary.append(
            {
                "variant": row["variant"],
                "metric": row["metric"],
                "row": line,
                "chunks_with_whole_row": [chunk.ordinal for chunk in holding],
                "with_block_header": [
                    c.ordinal for c in holding if block_header in c.text
                ],
                "with_dataset_header": [
                    c.ordinal for c in holding if DATASET_HEADER in c.text
                ],
            }
        )

    result = {
        "chunk_size": settings.chunk_size,
        "chunk_overlap": settings.chunk_overlap,
        "total_chunks": len(chunks),
        "table_page": table_page,
        "page_chunks": [
            {"ordinal": c.ordinal, "token_count": c.token_count, "text": c.text}
            for c in page_chunks
        ],
        "rows": summary,
    }
    (HERE / "page_chunks.json").write_text(
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
