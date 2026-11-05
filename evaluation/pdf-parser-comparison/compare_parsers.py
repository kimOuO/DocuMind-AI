"""Compare PDF text extraction by PyMuPDF, pypdf and pdfplumber on one document.

Only the parsing layer is compared: no chunking, no embedding, no LLM.

Usage:
    python compare_parsers.py <pdf> [--libs <dir>]
        [--two-column-pdf <pdf> --two-column-tex <file.tex> ...]

Reads ../ground-truth/paper-structure.json. Writes one file per configuration,
<library>/<variant>.json, holding the configuration and all its results. The
optional two-column paper (with its LaTeX body files, in order) adds a
reading-order check that the single-column paper cannot provide.
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
import time
import unicodedata
from collections import Counter
from collections.abc import Callable
from importlib import metadata
from pathlib import Path

HERE = Path(__file__).parent
GROUND_TRUTH = HERE.parent / "ground-truth"
TIMING_RUNS = 5
LIGATURES = "ﬀﬁﬂﬃﬄﬅﬆ"


# --- extraction configurations -------------------------------------------------


def pymupdf_default(pdf: str) -> list[str]:
    import pymupdf

    with pymupdf.open(pdf) as doc:
        return [page.get_text() for page in doc]


def pymupdf_sorted(pdf: str) -> list[str]:
    import pymupdf

    with pymupdf.open(pdf) as doc:
        return [page.get_text(sort=True) for page in doc]


def pypdf_default(pdf: str) -> list[str]:
    import pypdf

    return [page.extract_text() for page in pypdf.PdfReader(pdf).pages]


def pypdf_layout(pdf: str) -> list[str]:
    import pypdf

    return [
        page.extract_text(extraction_mode="layout")
        for page in pypdf.PdfReader(pdf).pages
    ]


def pdfplumber_default(pdf: str) -> list[str]:
    import pdfplumber

    with pdfplumber.open(pdf) as doc:
        return [page.extract_text() or "" for page in doc.pages]


def pdfplumber_tight(pdf: str) -> list[str]:
    import pdfplumber

    with pdfplumber.open(pdf) as doc:
        return [page.extract_text(x_tolerance=1) or "" for page in doc.pages]


CONFIGS: dict[str, tuple[str, str, str, Callable[[str], list[str]]]] = {
    # key: (library, variant, how the text is extracted, extractor)
    "pymupdf/default": ("pymupdf", "default", "page.get_text()", pymupdf_default),
    "pymupdf/sorted": ("pymupdf", "sorted", "page.get_text(sort=True)", pymupdf_sorted),
    "pypdf/default": ("pypdf", "default", "page.extract_text()", pypdf_default),
    "pypdf/layout": (
        "pypdf",
        "layout",
        'page.extract_text(extraction_mode="layout")',
        pypdf_layout,
    ),
    "pdfplumber/default": (
        "pdfplumber",
        "default",
        "page.extract_text()",
        pdfplumber_default,
    ),
    "pdfplumber/x-tolerance-1": (
        "pdfplumber",
        "x-tolerance-1",
        "page.extract_text(x_tolerance=1)",
        pdfplumber_tight,
    ),
}


# --- text normalisation --------------------------------------------------------


def squash(text: str) -> str:
    """Letters and digits only. Insensitive to spacing, line breaks and hyphenation."""
    return re.sub(r"[^a-z0-9]", "", unicodedata.normalize("NFKC", text).lower())


def word_tokens(text: str) -> list[str]:
    """Lower-case word tokens with hyphenation undone, so that word boundaries matter."""
    text = unicodedata.normalize("NFKC", text).lower()
    text = re.sub(r"[-‐‑–]\s*\n\s*", "", text)  # a word broken across two lines
    text = re.sub(r"[-‐‑–]", "", text)  # compare compounds without their hyphen
    return re.findall(r"[a-z0-9]+", text)


def find_sequence(haystack: list[str], needle: list[str]) -> int:
    first = needle[0]
    for index in range(len(haystack) - len(needle) + 1):
        if haystack[index] == first and haystack[index : index + len(needle)] == needle:
            return index
    return -1


def longest_increasing(values: list[int]) -> int:
    tails: list[int] = []
    for value in values:
        low, high = 0, len(tails)
        while low < high:
            mid = (low + high) // 2
            if tails[mid] < value:
                low = mid + 1
            else:
                high = mid
        tails[low : low + 1] = [value]
    return len(tails)


# --- checks --------------------------------------------------------------------


def check_anchors(pages: list[str], anchors: list[dict]) -> dict:
    """Is every paragraph present, with its words intact, and in document order?"""
    squashed = squash("\n".join(pages))
    tokens = word_tokens("\n".join(pages))
    rows = []
    for anchor in anchors:
        key = squash(anchor["phrase"])
        rows.append(
            {
                "phrase": anchor["phrase"],
                "file": anchor["file"],
                "position": squashed.find(key),
                "occurrences": squashed.count(key),
                "intact": find_sequence(tokens, word_tokens(anchor["phrase"])) >= 0,
            }
        )
    return {"rows": rows}


def check_headings(pages: list[str], headings: list[dict]) -> dict:
    """Numbered headings: present, words intact, and on which page."""
    page_squashed = [squash(page) for page in pages]
    page_tokens = [word_tokens(page) for page in pages]
    rows = []
    section, subsection = 0, 0
    for heading in headings:
        if heading["level"] == "section":
            section, subsection = section + 1, 0
            number = str(section)
        else:
            subsection += 1
            number = f"{section}.{subsection}"
        label = f"{number} {heading['title']}"
        key = squash(label)
        needle = word_tokens(label)
        page = next(
            (i + 1 for i, text in enumerate(page_squashed) if key in text), None
        )
        intact = any(find_sequence(tokens, needle) >= 0 for tokens in page_tokens)
        rows.append({"heading": label, "page": page, "intact": intact})
    return {"rows": rows}


def check_page_numbers(pages: list[str]) -> dict:
    """The page number printed at the bottom of page N must be N."""
    matches = []
    for index, page in enumerate(pages):
        lines = [line.strip() for line in page.splitlines() if line.strip()]
        matches.append(bool(lines) and lines[-1] == str(index + 1))
    return {
        "page_count": len(pages),
        "footer_matches": sum(matches),
        "mismatched_pages": [i + 1 for i, ok in enumerate(matches) if not ok],
    }


def table2_rows(cells: list[dict]) -> list[dict]:
    rows: dict[tuple[int, str], dict] = {}
    for cell in cells:
        row = rows.setdefault(
            (cell["block"], cell["metric"]),
            {
                "block": cell["block"],
                "variant": cell["variant"],
                "metric": cell["metric"],
                "values": [],
            },
        )
        row["values"].append(cell["value"])
    return list(rows.values())


def check_table2(pages: list[str], cells: list[dict], datasets: list[str]) -> dict:
    """Does the linear text keep every value attached to its row and column?

    The text after the caption is split into tokens. A cell counts as correct
    only if it is found at the position that its row label and the column
    order assign to it, not merely somewhere on the page.
    """
    rows = table2_rows(cells)
    page_index = next(
        (
            i
            for i, p in enumerate(pages)
            if "table2performanceofablatedversions" in squash(p)
        ),
        None,
    )
    if page_index is None:
        return {"page": None, "error": "caption not found"}
    page = pages[page_index]
    caption = re.search(r"Table\s*2\s*:.*?reference\s*\.", page, flags=re.DOTALL)
    region = page[caption.end() :] if caption else page
    tokens = region.split()
    lines = [line.split() for line in region.splitlines()]

    expected = list(datasets)
    for block in range(4):
        block_rows = [row for row in rows if row["block"] == block]
        expected += ["NaiveRAG", block_rows[0]["variant"]] * 4
        for row in block_rows:
            expected += [row["metric"], *row["values"]]
    sequence_ok = tokens[: len(expected)] == expected
    first_mismatch = next(
        (
            {
                "index": i,
                "expected": want,
                "found": tokens[i] if i < len(tokens) else None,
            }
            for i, want in enumerate(expected)
            if i >= len(tokens) or tokens[i] != want
        ),
        None,
    )

    # Row by row: the n-th occurrence of a metric label belongs to block n.
    correct_cells = 0
    intact_rows = 0
    headers_ok = 0
    rows_on_one_line = 0
    label_positions: dict[str, list[int]] = {}
    for index, token in enumerate(tokens):
        label_positions.setdefault(token, []).append(index)
    for row in rows:
        positions = label_positions.get(row["metric"], [])
        if row["block"] < len(positions):
            start = positions[row["block"]]
            found = tokens[start + 1 : start + 9]
            matches = sum(1 for want, got in zip(row["values"], found) if want == got)
            correct_cells += matches
            intact_rows += matches == 8
            if row["metric"] == "Comprehensiveness":  # first row of its block
                header = tokens[max(0, start - 8) : start]
                headers_ok += header == ["NaiveRAG", row["variant"]] * 4
        rows_on_one_line += [row["metric"], *row["values"]] in lines

    percentages = Counter(re.findall(r"\d+\.\d+%", page))
    wanted = Counter(cell["value"] for cell in cells)
    present = sum(min(count, percentages[value]) for value, count in wanted.items())

    return {
        "page": page_index + 1,
        "caption_found": caption is not None,
        "values_present_anywhere": present,
        "cells_in_correct_position": correct_cells,
        "rows_intact": intact_rows,
        "rows_on_one_line": rows_on_one_line,
        "block_headers_correct": headers_ok,
        "dataset_header_correct": tokens[:4] == datasets,
        "whole_sequence_correct": sequence_ok,
        "first_mismatch": first_mismatch,
        "total_cells": len(cells),
        "total_rows": len(rows),
    }


def check_quality(pages: list[str]) -> dict:
    text = "\n".join(pages)
    tokens = text.split()
    long_tokens = [
        t for t in tokens if len(t) > 30 and not re.search(r"https?:|@|/|\\|_", t)
    ]
    return {
        "characters": len(text),
        "replacement_characters": text.count("�"),
        "ligature_characters": sum(text.count(c) for c in LIGATURES),
        "cid_placeholders": text.count("(cid:"),
        "private_use_characters": sum(
            1 for c in text if unicodedata.category(c) == "Co"
        ),
        "tokens_longer_than_30": len(long_tokens),
        "longest_token_examples": sorted(long_tokens, key=len, reverse=True)[:3],
        "characters_per_page": [len(page) for page in pages],
    }


# --- table detection APIs (supplementary) ---------------------------------------


def clean_cells(row: list) -> list[str]:
    return [str(cell).strip() for cell in row if cell is not None and str(cell).strip()]


def score_table_rows(tables: list[list[list]], cells: list[dict]) -> dict:
    rows = table2_rows(cells)
    flat = [clean_cells(row) for table in tables for row in table]
    recovered = sum(1 for row in rows if [row["metric"], *row["values"]] in flat)
    return {
        "tables_found": len(tables),
        "rows_recovered": recovered,
        "total_rows": len(rows),
    }


def check_table_apis(pdf: str, page_number: int, cells: list[dict]) -> dict:
    results: dict[str, dict] = {}
    index = page_number - 1

    import pdfplumber

    with pdfplumber.open(pdf) as doc:
        page = doc.pages[index]
        attempts = {
            "pdfplumber extract_tables() [lines]": {},
            "pdfplumber extract_tables() [text]": {
                "vertical_strategy": "text",
                "horizontal_strategy": "text",
            },
        }
        for name, settings in attempts.items():
            try:
                results[name] = score_table_rows(page.extract_tables(settings), cells)
            except Exception as error:  # noqa: BLE001 - report, do not hide
                results[name] = {"error": repr(error)}

    import pymupdf

    with pymupdf.open(pdf) as doc:
        page = doc[index]
        for name, kwargs in {
            "pymupdf find_tables() [lines]": {},
            "pymupdf find_tables() [text]": {"strategy": "text"},
        }.items():
            try:
                found = page.find_tables(**kwargs)
                results[name] = score_table_rows(
                    [table.extract() for table in found.tables], cells
                )
            except Exception as error:  # noqa: BLE001
                results[name] = {"error": repr(error)}

    results["pypdf"] = {"note": "no table detection API"}
    return results


# --- timing and packaging --------------------------------------------------------


def time_extraction(extract: Callable[[str], list[str]], pdf: str) -> dict:
    durations = []
    for _ in range(TIMING_RUNS):
        start = time.perf_counter()
        extract(pdf)
        durations.append((time.perf_counter() - start) * 1000)
    return {
        "median_ms": round(statistics.median(durations), 1),
        "min_ms": round(min(durations), 1),
        "max_ms": round(max(durations), 1),
    }


def licence_of(dist: metadata.Distribution) -> str:
    meta = dist.metadata
    if meta.get("License-Expression"):
        return meta["License-Expression"]
    classifiers = [
        c.split("::")[-1].strip()
        for c in meta.get_all("Classifier") or []
        if c.startswith("License")
    ]
    if classifiers:
        return "; ".join(classifiers)
    return re.sub(r"\s+", " ", (meta.get("License") or "unknown"))[:80]


def requirement_name(requirement: str) -> str | None:
    if "extra ==" in requirement:
        return None
    return re.match(r"[A-Za-z0-9_.-]+", requirement).group(0)  # type: ignore[union-attr]


def describe_package(name: str) -> dict:
    """Licence and installed size of a library and of everything it pulls in."""
    seen: dict[str, dict] = {}
    queue = [name]
    while queue:
        current = queue.pop(0)
        key = current.lower().replace("_", "-")
        if key in seen:
            continue
        try:
            dist = metadata.distribution(current)
        except metadata.PackageNotFoundError:
            seen[key] = {
                "name": current,
                "version": "not installed",
                "licence": "unknown",
                "size_mb": 0.0,
            }
            continue
        size = sum(
            f.locate().stat().st_size for f in dist.files or [] if f.locate().is_file()
        )
        seen[key] = {
            "name": dist.metadata["Name"],
            "version": dist.version,
            "licence": licence_of(dist),
            "size_mb": round(size / 1_000_000, 1),
        }
        for requirement in dist.requires or []:
            dependency = requirement_name(requirement)
            if dependency:
                queue.append(dependency)
    packages = list(seen.values())
    return {
        "package": packages[0],
        "dependencies": packages[1:],
        "total_size_mb": round(sum(p["size_mb"] for p in packages), 1),
    }


# --- report ----------------------------------------------------------------------


def summarise(name: str, result: dict) -> dict:
    anchors = result["anchors"]["rows"]
    usable = [row for row in anchors if row["in_document"]]
    found = [row for row in usable if row["position"] >= 0]
    unique = [row["position"] for row in found if row["occurrences"] == 1]
    headings = result["headings"]["rows"]
    return {
        "config": name,
        "anchors_total": len(usable),
        "anchors_found": len(found),
        "anchors_intact": sum(row["intact"] for row in usable),
        "anchors_out_of_order": len(unique) - longest_increasing(unique),
        "headings_total": len(headings),
        "headings_found": sum(row["page"] is not None for row in headings),
        "headings_intact": sum(row["intact"] for row in headings),
    }


def reading_order_summary(rows: list[dict], in_document: list[bool]) -> dict:
    usable = [row for row, present in zip(rows, in_document) if present]
    found = [row for row in usable if row["position"] >= 0]
    unique = [row["position"] for row in found if row["occurrences"] == 1]
    return {
        "anchors": len(usable),
        "found": len(found),
        "intact": sum(row["intact"] for row in usable),
        "out_of_order": len(unique) - longest_increasing(unique),
        "not_found": [row["phrase"] for row in usable if row["position"] < 0][:5],
    }


def mark_in_document(all_rows: dict[str, list[dict]]) -> list[bool]:
    """An anchor no configuration finds is text that is not in the PDF body."""
    count = len(next(iter(all_rows.values())))
    present = [
        any(rows[i]["position"] >= 0 for rows in all_rows.values())
        for i in range(count)
    ]
    for rows in all_rows.values():
        for row, in_document in zip(rows, present):
            row["in_document"] = in_document
    return present


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", help="the single-column paper (LightRAG)")
    parser.add_argument(
        "--libs", help="directory the three libraries were installed into"
    )
    parser.add_argument(
        "--two-column-pdf", help="a two-column paper for the reading-order check"
    )
    parser.add_argument(
        "--two-column-tex", nargs="*", default=[], help="its LaTeX body files, in order"
    )
    args = parser.parse_args()
    if args.libs:
        sys.path.insert(0, args.libs)
    sys.path.insert(0, str(GROUND_TRUTH))
    from build_paper_structure import anchors_from_files

    truth = json.loads(
        (GROUND_TRUTH / "paper-structure.json").read_text(encoding="utf-8")
    )
    datasets = list(dict.fromkeys(cell["dataset"] for cell in truth["table2"]))
    two_column_anchors = (
        anchors_from_files([Path(f) for f in args.two_column_tex])
        if args.two_column_pdf
        else []
    )

    single: dict[str, dict] = {}
    two_column_rows: dict[str, list[dict]] = {}
    for key, (library, variant, call, extract) in CONFIGS.items():
        pages = extract(args.pdf)
        single[key] = {
            "anchors": check_anchors(pages, truth["anchors"]),
            "headings": check_headings(pages, truth["headings"]),
            "page_numbers": check_page_numbers(pages),
            "table2": check_table2(pages, truth["table2"], datasets),
            "quality": check_quality(pages),
            "timing": time_extraction(extract, args.pdf),
        }
        if args.two_column_pdf:
            two_column_rows[key] = check_anchors(
                extract(args.two_column_pdf), two_column_anchors
            )["rows"]

    mark_in_document({key: result["anchors"]["rows"] for key, result in single.items()})
    two_column_present = mark_in_document(two_column_rows) if two_column_rows else []
    table_page = single["pypdf/default"]["table2"].get("page") or 8
    table_apis = check_table_apis(args.pdf, table_page, truth["table2"])
    packages = {
        library: describe_package(library)
        for library in ("pymupdf", "pypdf", "pdfplumber")
    }

    print(
        f"{'configuration':26} {'anchors':>9} {'intact':>7} {'order':>5} {'headings':>9} {'table2 cells':>13} {'rows/line':>9} {'ms':>6}  two-column"
    )
    for key, (library, variant, call, _) in CONFIGS.items():
        result = single[key]
        summary = summarise(key, result)
        two_column = (
            reading_order_summary(two_column_rows[key], two_column_present)
            if two_column_rows
            else None
        )
        report = {
            "config": {
                "library": library,
                "variant": variant,
                "call": call,
                "package": packages[library]["package"],
                "dependencies": packages[library]["dependencies"],
                "total_size_mb": packages[library]["total_size_mb"],
            },
            "single_column_paper": {
                "pdf": Path(args.pdf).name,
                "page_count": result["page_numbers"]["page_count"],
                "ground_truth": truth["source"],
                "summary": summary,
                **result,
            },
            "two_column_paper": (
                {"pdf": Path(args.two_column_pdf).name, "summary": two_column}
                if two_column is not None
                else None
            ),
            # Table detection APIs belong to the library, so they are reported once, on its default variant.
            "table_detection_api": (
                {
                    name: value
                    for name, value in table_apis.items()
                    if name.startswith(library)
                }
                if variant == "default"
                else None
            ),
        }
        out = HERE / library / f"{variant}.json"
        out.parent.mkdir(exist_ok=True)
        out.write_text(
            json.dumps(report, indent=1, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        t2 = result["table2"]
        two_text = (
            f"{two_column['found']}/{two_column['anchors']} found, {two_column['out_of_order']} out of order"
            if two_column
            else "-"
        )
        print(
            f"{key:26} {summary['anchors_found']:>3}/{summary['anchors_total']:<5} {summary['anchors_intact']:>7} {summary['anchors_out_of_order']:>5} "
            f"{summary['headings_intact']:>4}/{summary['headings_total']:<4} {t2.get('cells_in_correct_position', 0):>7}/{t2.get('total_cells', 128):<5} "
            f"{t2.get('rows_on_one_line', 0):>5}/16 {result['timing']['median_ms']:>6}  {two_text}"
        )


if __name__ == "__main__":
    main()
