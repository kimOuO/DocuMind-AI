"""Replay the two answer-level checks of D68 on saved real answers.

- Universal comparison claims ("X consistently outperforms Y across all datasets"):
  app.chat.verification.check_universal_claims, against the tables on the pages of
  the sources the answer cited.
- Doubtful citations (a statement cited to a source that hardly states it):
  app.chat.citation_check.check_citations, against the texts of the sources the
  model was shown.

answers.json holds the answers with the sources the model saw (index, page,
origin, the first characters of the chunk). The full chunk texts are not stored:
they are rebuilt here by running the ingestion chunker on the paper with the
project's settings, and matched by page and prefix, so the replay sees exactly
what the model saw. Hand labels for every universal-claim sentence and every
doubt live in labels.json; the summary compares the checks with them.

Usage (from the repository root, inside the project's venv):
    .venv/bin/python evaluation/answer-checks/replay.py

Writes results.json next to this script and prints the summary of README.md.
"""

from __future__ import annotations

import json
import re
import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BACKEND = ROOT / "app" / "backend"
sys.path.insert(0, str(BACKEND))

from app.chat import verification
from app.chat.citation_check import SourceText, check_citations
from app.core.env_loader import get_settings
from app.ingestion.chunking import chunk_pages
from app.ingestion.parsing import parse_document
from app.ingestion.tables import find_table_regions, linearize_table
from app.llm.tokenizer import Qwen3TokenCounter

PDF = ROOT / "sample-documents" / "2410.05779v3.pdf"
HERE = Path(__file__).resolve().parent
DOCUMENT = uuid.uuid4()  # all sources come from the one paper


def rebuilt_chunks() -> list:
    settings = get_settings()
    pages = parse_document(PDF, "pdf")
    return chunk_pages(
        pages,
        Qwen3TokenCounter(),
        chunk_size=settings.chunk_size,
        overlap=settings.chunk_overlap,
    )


def page_texts() -> dict[int, verification.PageText]:
    document = uuid.uuid4()
    out = {}
    for page in parse_document(PDF, "pdf"):
        text, lines = page.text, page.text.splitlines()
        for start, end in find_table_regions(page.text):
            region = "\n".join(lines[start:end])
            text = text.replace(region, linearize_table(region))
        out[page.number] = verification.PageText(document, page.number, text)
    return out


def resolve(source: dict, chunks: list) -> str:
    """The full text of the chunk a saved source points at (same page, same start)."""
    prefix = " ".join(source["snippet"].split())[:40]
    for chunk in chunks:
        if chunk.page == source["page"] and " ".join(chunk.text.split()).startswith(
            prefix
        ):
            return chunk.text
    raise SystemExit(f"source not found among the rebuilt chunks: {source}")


def main() -> None:
    answers = json.loads((HERE / "answers.json").read_text())
    labels = (
        json.loads((HERE / "labels.json").read_text())
        if (HERE / "labels.json").exists()
        else {}
    )
    chunks = rebuilt_chunks()
    pages = page_texts()
    universal = re.compile(verification._UNIVERSAL.pattern, re.IGNORECASE)
    comparative = re.compile(verification._COMPARATIVE.pattern, re.IGNORECASE)

    results = []
    for entry in answers:
        sources = [
            SourceText(s["index"], resolve(s, chunks), DOCUMENT, s["page"], s["page"])
            for s in entry["sources"]
        ]
        cited_pages = sorted(
            {s["page"] for s in entry["sources"] if s["index"] in entry["cited"]}
        )
        claims = verification.check_universal_claims(
            entry["answer"], [pages[p] for p in cited_pages]
        )
        doubts = check_citations(entry["answer"], sources)
        # Every sentence with a universal and a comparative cue, flagged or not, for labelling.
        candidates = [
            " ".join(s.split())
            for s in re.split(r"(?<=[.!?。！？])\s+|\n+", entry["answer"])
            if universal.search(s) and comparative.search(s)
        ]
        results.append(
            {
                "id": entry["id"],
                "question": entry["question"],
                "condition": entry["condition"],
                "universal_candidates": candidates,
                "overstated_claims": [c.__dict__ for c in claims],
                "doubtful_citations": [d.__dict__ for d in doubts],
            }
        )

    summary = {"answers": len(results)}
    rows_u = {"TP": 0, "FP": 0, "FN": 0, "TN": 0, "UNRESOLVED": 0}
    rows_c = {"TP": 0, "FP": 0, "FN": 0}
    for r in results:
        truth = labels.get(r["id"], {})
        false_claims = set(truth.get("false_universal_claims", []))  # sentence prefixes
        flagged = {
            c["sentence"]
            for c in r["overstated_claims"]
            if c["status"] == "contradicted"
        }
        unresolved = {
            c["sentence"]
            for c in r["overstated_claims"]
            if c["status"] != "contradicted"
        }
        for sentence in r["universal_candidates"]:
            is_false = any(sentence.startswith(p) for p in false_claims)
            hit = any(
                sentence.startswith(f[:40]) or f.startswith(sentence[:40])
                for f in flagged
            )
            und = any(
                sentence.startswith(f[:40]) or f.startswith(sentence[:40])
                for f in unresolved
            )
            if und:
                rows_u["UNRESOLVED"] += 1
            elif is_false and hit:
                rows_u["TP"] += 1
            elif is_false:
                rows_u["FN"] += 1
            elif hit:
                rows_u["FP"] += 1
            else:
                rows_u["TN"] += 1
        wrong_cit = truth.get(
            "wrong_citations", []
        )  # sentence prefixes the human found miscited
        doubted = [d["sentence"] for d in r["doubtful_citations"]]
        for d in doubted:
            rows_c["TP" if any(d.startswith(p) for p in wrong_cit) else "FP"] += 1
        for p in wrong_cit:
            if not any(d.startswith(p) for d in doubted):
                rows_c["FN"] += 1
    summary["universal_claims"] = rows_u
    summary["citations"] = rows_c
    (HERE / "results.json").write_text(
        json.dumps(
            {
                "config": {
                    "checks": "app/backend/app/chat/verification.py check_universal_claims; "
                    "app/backend/app/chat/citation_check.py (working tree, D68)",
                    "sources": f"{PDF.name} re-chunked with the project settings; pages of the cited sources",
                    "ground_truth": "labels.json (hand-labelled)",
                },
                "summary": summary,
                "answers": results,
            },
            indent=1,
            ensure_ascii=False,
        )
        + "\n"
    )
    print(json.dumps(summary, ensure_ascii=False))
    for r in results:
        print(f"\n### {r['id']} {r['question']} — {r['condition']}")
        for s in r["universal_candidates"]:
            print(f"  candidate: {s[:200]}")
        for c in r["overstated_claims"]:
            print(
                f"  {c['status']:<12} {c['method']} vs {c['compared'] or 'all'}: higher {c['higher']}, lower {c['lower']} | {c['sentence'][:120]}"
            )
            for e in c["examples"][:3]:
                print(f"      e.g. {e}")
        for d in r["doubtful_citations"]:
            print(
                f"  doubt: cited {d['cited']} closer {d['closer']} ({d['coverage_cited']} vs {d['coverage_closer']}) | {d['sentence'][:150]}"
            )


if __name__ == "__main__":
    main()
