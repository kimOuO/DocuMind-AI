"""Summarise the D71 A/B/C runs against the evidence-location ground truth.

Reads evaluation/navigator-abc/runs/*.json (written by
tests/integration/test_navigator_abc_real.py) and
evaluation/ground-truth/evidence-locations.json, and computes per arm and question:

- Location Recall at three stages: the retrieved sources (Top-K + table context, as
  every arm starts), the Navigator's located plan items (B only), and the sources the
  answering call finally saw;
- Evidence Coverage: required locations whose marker text occurs in the final sources;
- the plan's located rate, the number of chunks added, and the share of added chunks
  that hit no required location (redundant evidence) (B only);
- tokens, calls and latency.

It also writes answers.md: every run's final answer, the Navigator's plan (B), the sources
the answering call saw and the deterministic checks, so the answers can be judged by hand
without opening the JSON files.

The hand judgement of the answers (pass rate, citation support) is not here: it is
done by reading the answers and recorded in README.md.

Usage:  .venv/bin/python evaluation/navigator-abc/analyse.py
"""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
TRUTH = json.loads(
    (HERE.parent / "ground-truth" / "evidence-locations.json").read_text()
)


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", text).lower()


def _hits(location: dict, source: dict) -> bool:
    """A source carries a location when it lies on the location's pages and has a marker."""
    first, last = location["pages"]
    if not (source["page_start"] <= last and first <= source["page_end"]):
        return False
    text = _norm(source.get("snippet", ""))
    return any(_norm(m) in text for m in location["markers"])


def _page_hit(location: dict, pages: list[int]) -> bool:
    first, last = location["pages"]
    return any(first <= p <= last for p in pages)


def analyse(run: dict) -> dict:
    locations = TRUTH.get(run["question"], [])
    required = [loc for loc in locations if loc["required"]]
    sources = run.get("sources", [])
    retrieved = [
        s for s in sources if s["origin"] in ("retrieval", "table_context", "summary")
    ]
    final = sources
    navigation = (run.get("done") or {}).get("navigation") or {}
    items = navigation.get("items", [])
    located_pages = [p for i in items if i["located"] for p in i["pages"]]
    added = [s for s in sources if s["origin"] == "navigation"]

    def recall(check) -> float | None:  # type: ignore[no-untyped-def]
        if not required:
            return None
        return round(sum(1 for loc in required if check(loc)) / len(required), 2)

    coverage = recall(lambda loc: any(_hits(loc, s) for s in final))
    return {
        "arm": run["arm"],
        "question": run["question"],
        "run": run["run"],
        "status": (run.get("done") or {}).get("status")
        or (run.get("error") or {}).get("code"),
        "route": (run.get("route") or {}).get("type"),
        "recall_retrieved": recall(
            lambda loc: any(_page_hit(loc, [s["page_start"]]) for s in retrieved)
        ),
        "recall_plan": recall(lambda loc: _page_hit(loc, located_pages))
        if items
        else None,
        "recall_final": recall(
            lambda loc: any(_page_hit(loc, [s["page_start"]]) for s in final)
        ),
        "coverage_final": coverage,
        "plan_items": len(items),
        "plan_located": navigation.get("located"),
        "added_chunks": len(added),
        "redundant_added": sum(
            1 for s in added if not any(_hits(loc, s) for loc in locations)
        ),
        # D73 (B2): how the selection ruled chunks out.
        "excluded_low_relevance": sum(
            1 for e in navigation.get("log", []) if e.get("reason") == "low relevance"
        ),
        "excluded_budget": sum(
            1
            for e in navigation.get("log", [])
            if e.get("reason") == "over the evidence budget"
        ),
        # D74 (B3): coverage of the required targets, the supplementary chunks used, the
        # size of the evidence matrix and the four-way analysis status.
        "required_targets": sum(1 for i in items if i.get("priority") == "required"),
        "required_covered": sum(
            1
            for i in items
            if i.get("priority") == "required" and i.get("coverage") == "covered"
        ),
        "unmet_required": len(navigation.get("unmet_required") or []),
        "supplementary_used": navigation.get("supplementary_used"),
        "matrix_cells": (navigation.get("matrix") or {}).get("cells"),
        "analysis_status": (run.get("done") or {}).get("analysis_status"),
        "direction_issues": len((run.get("done") or {}).get("direction_issues") or []),
        # D75 (B4): what the deterministic correction did before the answer was sent.
        "correction_edits": len(
            ((run.get("done") or {}).get("correction") or {}).get("edits") or []
        ),
        "correction_removed": len(
            ((run.get("done") or {}).get("correction") or {}).get("removed") or []
        ),
        "correction_remaining": len(
            ((run.get("done") or {}).get("correction") or {}).get("remaining") or []
        ),
        "calls": len(run.get("llm_calls", [])),
        "tokens": sum(
            c["prompt_tokens"] + c["completion_tokens"]
            for c in run.get("llm_calls", [])
        ),
        "elapsed_seconds": run.get("elapsed_seconds"),
        "answer_chars": len(run.get("final_answer", "")),
    }


ORDER = {"Q1": 0, "Q2": 1, "Q3": 2, "G1": 3, "G2": 4}


def _answers(runs: list[dict]) -> str:
    lines = [
        "# navigator-abc — 45 次執行的完整回答",
        "",
        "由 `analyse.py` 從 `runs/*.json` 產生。每則列出：來源（頁碼與來路）、B 臂的閱讀計畫、"
        + "最終回答全文、確定性檢查的結果。人工判定在 `README.md`。",
        "",
    ]
    for run in sorted(runs, key=lambda r: (ORDER[r["question"]], r["arm"], r["run"])):
        done = run.get("done") or {}
        lines.append(f"## {run['arm']}-{run['question']}-{run['run']}")
        lines.append("")
        lines.append(
            f"- 問題：`{run['question_text']}`；模式 `{run['answer_mode']}`；"
            f"{run['elapsed_seconds']} 秒；{len(run.get('llm_calls', []))} 次呼叫；"
            f"tokens {sum(c['prompt_tokens'] + c['completion_tokens'] for c in run.get('llm_calls', []))}"
        )
        lines.append(
            "- 來源："
            + ", ".join(
                f"[{s['index']}] p{s['page_start']} {s['origin']}"
                for s in run.get("sources", [])
            )
        )
        navigation = done.get("navigation") or {}
        if navigation:
            lines.append(
                f"- 閱讀計畫（定位 {navigation.get('located')}/{len(navigation.get('items', []))}，"
                f"保留 {navigation.get('kept')}，超預算 {navigation.get('excluded_budget')}）："
            )
            for item in navigation.get("items", []):
                detail = ""
                if "selected" in item:  # D73 targets
                    detail = (
                        f" → 候選 {item.get('candidates', 0)}，納入 {item['selected']}，"
                        f"排除 {[(x['ordinal'], x['reason']) for x in item.get('excluded', [])]}"
                    )
                lines.append(
                    f"  - {'✓' if item['located'] else '✗'} {item['text']}{detail}"
                )
        if done.get("analysis_status") is not None:
            completeness = done.get("completeness") or {}
            lines.append(
                f"- 分析狀態：{done['analysis_status']}；完整性 {completeness.get('status')}"
                f"（required {completeness.get('required')}，缺 {completeness.get('missing')}，"
                f"條件 {completeness.get('condition')}）；方向核對 "
                f"{[(d['status'], d['left'], d['right']) for d in done.get('direction_issues') or []]}"
            )
        if done.get("correction"):
            c = done["correction"]
            lines.append(
                f"- 修正：{[(e['kind'], e['before'], e['after']) for e in c.get('edits', [])]}；"
                f"刪除 {c.get('removed')}；仍不符 {c.get('remaining')}；"
                f"方向待定 {[(u['cue'], u['left'], u['right']) for u in c.get('uncertain', [])]}"
            )
        if navigation.get("coverage") is not None:
            lines.append(
                "- 涵蓋判定："
                + "；".join(
                    f"{c['location']}→{c['status']}" for c in navigation["coverage"]
                )
                + f"；required 未納入 {navigation.get('unmet_required')}；supplementary 用 "
                f"{navigation.get('supplementary_used')}；Matrix {navigation.get('matrix')}"
            )
        lines.append(
            "- 檢查：標籤不符 "
            f"{[m['number'] for m in done.get('mislabelled_numbers') or []]}；"
            f"全稱宣稱 {len(done.get('overstated_claims') or [])}；"
            f"引用可疑 {[(d['cited'], d['closer']) for d in done.get('doubtful_citations') or []]}；"
            f"未解析 {len(done.get('unresolved_numbers') or [])}；"
            f"找不到的數字 {done.get('unverified_numbers', [])}"
        )
        lines.append("")
        lines.append("```text")
        lines.append(run.get("final_answer", "").strip())
        lines.append("```")
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    runs = [
        run
        for run in (
            json.loads(p.read_text()) for p in sorted((HERE / "runs").glob("*.json"))
        )
        if isinstance(run, dict)
        and "question" in run  # not the summary-verification records
    ]
    rows = [analyse(run) for run in runs]
    (HERE / "analysis.json").write_text(
        json.dumps(rows, indent=1, ensure_ascii=False) + "\n"
    )
    (HERE / "answers.md").write_text(_answers(runs))
    groups: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for r in rows:
        groups[(r["arm"], r["question"])].append(r)

    def mean(values: list[float | None]) -> str:
        real = [v for v in values if v is not None]
        return f"{sum(real) / len(real):.2f}" if real else "—"

    print(
        "| arm | Q | n | recall retrieved | recall plan | recall final | coverage final | "
        "plan located/items | added | redundant | low relevance | over budget | "
        "required covered | supp. used | matrix cells | corrections (edit/remove/left) | calls | tokens | s |"
    )
    print(
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"
    )
    for (arm, q), rs in sorted(groups.items(), key=lambda kv: (kv[0][1], kv[0][0])):
        located = sum(r["plan_located"] or 0 for r in rs)
        items = sum(r["plan_items"] for r in rs)
        print(
            f"| {arm} | {q} | {len(rs)} | {mean([r['recall_retrieved'] for r in rs])} | "
            f"{mean([r['recall_plan'] for r in rs])} | {mean([r['recall_final'] for r in rs])} | "
            f"{mean([r['coverage_final'] for r in rs])} | {located}/{items} | "
            f"{sum(r['added_chunks'] for r in rs)} | {sum(r['redundant_added'] for r in rs)} | "
            f"{sum(r['excluded_low_relevance'] for r in rs)} | {sum(r['excluded_budget'] for r in rs)} | "
            f"{sum(r['required_covered'] for r in rs)}/{sum(r['required_targets'] for r in rs)} | "
            f"{sum(r['supplementary_used'] or 0 for r in rs)} | "
            f"{sum(r['matrix_cells'] or 0 for r in rs)} | "
            f"{sum(r['correction_edits'] for r in rs)}/{sum(r['correction_removed'] for r in rs)}/"
            f"{sum(r['correction_remaining'] for r in rs)} | "
            f"{mean([r['calls'] for r in rs])} | {mean([r['tokens'] for r in rs])} | "
            f"{mean([r['elapsed_seconds'] for r in rs])} |"
        )


if __name__ == "__main__":
    main()
