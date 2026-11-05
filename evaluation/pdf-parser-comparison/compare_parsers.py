"""Compare PDF text extraction by PyMuPDF, pypdf and pdfplumber on one document.

Only the parsing layer is compared: no chunking, no embedding, no LLM.

Usage:
    python compare_parsers.py <pdf> [--libs <directory the three libraries are installed in>]

Reads ground_truth.json (see build_ground_truth.py) and writes results.json and
results.md next to this script.
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


CONFIGS: dict[str, tuple[str, str, Callable[[str], list[str]]]] = {
    "pymupdf-default": ("pymupdf", "page.get_text()", pymupdf_default),
    "pymupdf-sorted": ("pymupdf", "page.get_text(sort=True)", pymupdf_sorted),
    "pypdf-default": ("pypdf", "page.extract_text()", pypdf_default),
    "pypdf-layout": (
        "pypdf",
        'page.extract_text(extraction_mode="layout")',
        pypdf_layout,
    ),
    "pdfplumber-default": ("pdfplumber", "page.extract_text()", pdfplumber_default),
    "pdfplumber-xtol1": (
        "pdfplumber",
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


def render_markdown(report: dict) -> str:
    configs = report["configs"]
    names = list(configs)
    lines = [
        "# PDF 解析器比較：實驗結果",
        "",
        f"由 `compare_parsers.py` 產生。文件：`{report['pdf']}`（{report['page_count']} 頁）。",
        "標準答案來自論文的 LaTeX 原始檔，與受測的解析器無關。",
        "",
        "## 受測設定",
        "",
        "| 設定 | 呼叫方式 | 套件版本 |",
        "|---|---|---|",
    ]
    for name in names:
        library = configs[name]["library"]
        lines.append(
            f"| {name} | `{configs[name]['call']}` | {library} {report['packages'][library]['package']['version']} |"
        )

    def table(title: str, header: list[str], rows: list[list]) -> None:
        lines.extend(
            [
                "",
                f"## {title}",
                "",
                "| " + " | ".join(header) + " |",
                "|" + "---|" * len(header),
            ]
        )
        lines.extend(
            "| " + " | ".join(str(cell) for cell in row) + " |" for row in rows
        )

    table(
        "內文：段落是否完整、順序是否正確",
        [
            "設定",
            "段落找得到",
            "單字邊界完整",
            "順序錯置",
            "標題找得到",
            "標題文字完整",
        ],
        [
            [
                n,
                f"{s['anchors_found']}/{s['anchors_total']}",
                f"{s['anchors_intact']}/{s['anchors_total']}",
                s["anchors_out_of_order"],
                f"{s['headings_found']}/{s['headings_total']}",
                f"{s['headings_intact']}/{s['headings_total']}",
            ]
            for n in names
            for s in [configs[n]["summary"]]
        ],
    )
    table(
        "Table 2：數值與列、欄的對應",
        [
            "設定",
            "頁碼",
            "數值出現在頁面上",
            "數值在正確的列與欄位置",
            "完整的列",
            "整列在同一行",
            "區塊標題正確",
            "資料集標題正確",
            "整張表順序完全正確",
        ],
        [
            [
                n,
                t.get("page"),
                f"{t.get('values_present_anywhere', 0)}/{t.get('total_cells', 128)}",
                f"{t.get('cells_in_correct_position', 0)}/{t.get('total_cells', 128)}",
                f"{t.get('rows_intact', 0)}/{t.get('total_rows', 16)}",
                f"{t.get('rows_on_one_line', 0)}/{t.get('total_rows', 16)}",
                f"{t.get('block_headers_correct', 0)}/4",
                "是" if t.get("dataset_header_correct") else "否",
                "是" if t.get("whole_sequence_correct") else "否",
            ]
            for n in names
            for t in [configs[n]["table2"]]
        ],
    )
    table(
        "頁碼",
        ["設定", "頁數", "頁尾印的頁碼與頁序相符", "不相符的頁"],
        [
            [
                n,
                p["page_count"],
                f"{p['footer_matches']}/{p['page_count']}",
                p["mismatched_pages"] or "無",
            ]
            for n in names
            for p in [configs[n]["page_numbers"]]
        ],
    )
    table(
        "文字品質與解析時間",
        [
            "設定",
            "字元數",
            "無法解碼的字元",
            "未展開的連字",
            "(cid:) 佔位",
            "超過 30 字元的字串",
            "解析時間中位數（毫秒）",
            "最短–最長",
        ],
        [
            [
                n,
                q["characters"],
                q["replacement_characters"],
                q["ligature_characters"],
                q["cid_placeholders"],
                q["tokens_longer_than_30"],
                t["median_ms"],
                f"{t['min_ms']}–{t['max_ms']}",
            ]
            for n in names
            for q, t in [(configs[n]["quality"], configs[n]["timing"])]
        ],
    )
    table(
        "表格偵測 API（補充）",
        ["方法", "偵測到的表格數", "還原成「指標＋8 個數值」的列"],
        [
            [
                name,
                r.get("tables_found", "—"),
                f"{r['rows_recovered']}/{r['total_rows']}"
                if "rows_recovered" in r
                else r.get("note") or r.get("error"),
            ]
            for name, r in report["table_apis"].items()
        ],
    )
    table(
        "授權與安裝大小",
        ["套件", "版本", "授權", "連同相依的安裝大小（MB）", "相依套件（授權）"],
        [
            [
                p["package"]["name"],
                p["package"]["version"],
                p["package"]["licence"],
                p["total_size_mb"],
                "；".join(
                    f"{d['name']} {d['version']}（{d['licence']}）"
                    for d in p["dependencies"]
                )
                or "無",
            ]
            for p in report["packages"].values()
        ],
    )

    lines.extend(["", "## 各設定的細節", ""])
    for name in names:
        result = configs[name]
        missing = [
            r["phrase"]
            for r in result["anchors"]["rows"]
            if r["in_document"] and r["position"] < 0
        ]
        broken = [
            r["phrase"]
            for r in result["anchors"]["rows"]
            if r["in_document"] and r["position"] >= 0 and not r["intact"]
        ]
        bad_headings = [
            r["heading"] for r in result["headings"]["rows"] if not r["intact"]
        ]
        lines.append(f"### {name}")
        lines.append("")
        lines.append(
            f"- 找不到的段落（{len(missing)}）："
            + ("；".join(f"`{m}`" for m in missing[:5]) or "無")
        )
        lines.append(
            f"- 單字邊界不完整的段落（{len(broken)}）："
            + ("；".join(f"`{b}`" for b in broken[:5]) or "無")
        )
        lines.append(
            f"- 文字不完整的標題（{len(bad_headings)}）："
            + ("；".join(f"`{h}`" for h in bad_headings[:6]) or "無")
        )
        mismatch = result["table2"].get("first_mismatch")
        if mismatch:
            lines.append(
                f"- Table 2 第一個不符的位置：第 {mismatch['index']} 個字串，預期 `{mismatch['expected']}`，實際 `{mismatch['found']}`"
            )
        examples = result["quality"]["longest_token_examples"]
        if examples:
            lines.append(
                "- 過長字串的例子：" + "；".join(f"`{e[:60]}`" for e in examples)
            )
        lines.append("")

    disagreements = report["heading_page_disagreements"]
    lines.extend(["## 各設定之間的頁碼一致性", ""])
    if disagreements:
        lines.extend(f"- `{d['heading']}`：{d['pages']}" for d in disagreements)
    else:
        lines.append("每個找得到的標題，在所有設定中都落在同一頁。")
    excluded = report["anchors_not_in_document"]
    lines.extend(["", "## 排除的錨點", ""])
    lines.append(
        f"{len(excluded)} 個錨點在所有設定中都找不到，視為 LaTeX 原始檔中有、但未出現在 PDF 內文的文字，不列入計分："
        + ("；".join(f"`{e}`" for e in excluded) or "無")
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf")
    parser.add_argument(
        "--libs",
        help="directory the three libraries were installed into with pip --target",
    )
    args = parser.parse_args()
    if args.libs:
        sys.path.insert(0, args.libs)

    truth = json.loads((HERE / "ground_truth.json").read_text(encoding="utf-8"))
    datasets = list(dict.fromkeys(cell["dataset"] for cell in truth["table2"]))

    configs: dict[str, dict] = {}
    for name, (library, call, extract) in CONFIGS.items():
        pages = extract(args.pdf)
        configs[name] = {
            "library": library,
            "call": call,
            "anchors": check_anchors(pages, truth["anchors"]),
            "headings": check_headings(pages, truth["headings"]),
            "page_numbers": check_page_numbers(pages),
            "table2": check_table2(pages, truth["table2"], datasets),
            "quality": check_quality(pages),
            "timing": time_extraction(extract, args.pdf),
        }

    # An anchor that no configuration can find is text that is in the LaTeX
    # source but not in the PDF body; it says nothing about the parsers.
    anchor_count = len(truth["anchors"])
    in_document = [
        any(configs[n]["anchors"]["rows"][i]["position"] >= 0 for n in configs)
        for i in range(anchor_count)
    ]
    for result in configs.values():
        for row, present in zip(result["anchors"]["rows"], in_document):
            row["in_document"] = present
    for name, result in configs.items():
        result["summary"] = summarise(name, result)

    disagreements = []
    for index, heading in enumerate(configs[next(iter(configs))]["headings"]["rows"]):
        pages_by_config = {
            n: configs[n]["headings"]["rows"][index]["page"] for n in configs
        }
        if len({p for p in pages_by_config.values() if p is not None}) > 1:
            disagreements.append(
                {"heading": heading["heading"], "pages": pages_by_config}
            )

    table_page = configs["pymupdf-default"]["table2"].get("page") or 8
    report = {
        "pdf": Path(args.pdf).name,
        "page_count": configs["pymupdf-default"]["page_numbers"]["page_count"],
        "ground_truth_source": truth["source"],
        "configs": configs,
        "heading_page_disagreements": disagreements,
        "anchors_not_in_document": [
            a["phrase"]
            for a, present in zip(truth["anchors"], in_document)
            if not present
        ],
        "table_apis": check_table_apis(args.pdf, table_page, truth["table2"]),
        "packages": {
            library: describe_package(library)
            for library in ("pymupdf", "pypdf", "pdfplumber")
        },
    }
    (HERE / "results.json").write_text(
        json.dumps(report, indent=1, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (HERE / "results.md").write_text(render_markdown(report), encoding="utf-8")
    for name, result in configs.items():
        print(
            name,
            result["summary"],
            {k: v for k, v in result["table2"].items() if k != "first_mismatch"},
            result["timing"],
        )


if __name__ == "__main__":
    main()
