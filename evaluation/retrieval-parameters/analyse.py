"""Aggregate evaluation/retrieval-parameters/runs/chunk*.json into the tables of README.md.

Recall@K: for each question with evidence, the share of its evidence items covered by the
top K chunks; averaged over questions. Source hit rate: share of questions whose top K cover
at least one item. Evidence tokens: mean token count of the top K. Keyword-type questions
are reported separately (spec 02 §9.3). The threshold sweep (§9.5) uses every question's
top-1 similarity: the no-answer questions should fall below the threshold, the others above.
Prints Markdown; writes analysis.json."""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
KS = ("3", "5", "8")
THRESHOLDS = [round(0.30 + 0.05 * i, 2) for i in range(7)]


def mean(values):
    values = [v for v in values if v is not None]
    return sum(values) / len(values) if values else None


def fmt(v, digits=2):
    return "—" if v is None else f"{v:.{digits}f}"


def main() -> None:
    runs = {}
    for path in sorted((HERE / "runs").glob("chunk*.json")):
        record = json.loads(path.read_text())
        runs[record["config"]["chunk_size"]] = record
    out = {"configs": {}, "thresholds": {}}
    lines = []
    lines.append(
        "| 切塊 | 切塊數 | K | Vector Recall@K | 命中率 | Hybrid Recall@K | 命中率 | "
        "Vector＋表格後文 Recall | 命中率 | 多向量（表格分區塊取最大）Recall | 命中率 | "
        "關鍵字型 Recall V/H/M | 證據 tokens V/H/V＋後文 |"
    )
    lines.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for size, record in sorted(runs.items()):
        questions = [q for q in record["questions"] if not q["expect_refusal"]]
        keyword = [q for q in questions if q["keyword_type"]]
        for k in KS:
            row = {}
            for method in ("vector", "hybrid", "vector_context", "vector_max"):
                row[method] = {
                    "recall": mean(q[method][k]["recall"] for q in questions),
                    "hit": mean(1.0 if q[method][k]["hit"] else 0.0 for q in questions),
                    "keyword_recall": mean(q[method][k]["recall"] for q in keyword),
                    "tokens": mean(q[method][k]["evidence_tokens"] for q in questions),
                }
            out["configs"][f"{size}x{k}"] = row
            v, h, c, m = (
                row["vector"],
                row["hybrid"],
                row["vector_context"],
                row["vector_max"],
            )
            lines.append(
                f"| {size} | {record['chunk_count']} | {k} | "
                f"{fmt(v['recall'])} | {fmt(v['hit'])} | {fmt(h['recall'])} | {fmt(h['hit'])} | "
                f"{fmt(c['recall'])} | {fmt(c['hit'])} | {fmt(m['recall'])} | {fmt(m['hit'])} | "
                f"{fmt(v['keyword_recall'])} / {fmt(h['keyword_recall'])} / "
                f"{fmt(m['keyword_recall'])} | "
                f"{fmt(v['tokens'], 0)} / {fmt(h['tokens'], 0)} / {fmt(c['tokens'], 0)} |"
            )
    lines.append("")
    lines.append(
        "每題（K=5；R = Vector、H = Hybrid、C = Vector＋表格後文 的 Recall）："
    )
    lines.append(
        "| 題 | 類型 | " + " | ".join(f"切塊 {s}" for s in sorted(runs)) + " |"
    )
    lines.append("|---|---|" + "---|" * len(runs))
    ids = [q["id"] for q in next(iter(runs.values()))["questions"]]
    by = {size: {q["id"]: q for q in r["questions"]} for size, r in runs.items()}
    for qid in ids:
        cells = []
        for size in sorted(runs):
            q = by[size][qid]
            if q["expect_refusal"]:
                cells.append(f"top-1 {fmt(q['top1_similarity'])}")
            else:
                cells.append(
                    f"R {fmt(q['vector']['5']['recall'])} / H {fmt(q['hybrid']['5']['recall'])}"
                    f" / C {fmt(q['vector_context']['5']['recall'])}"
                    f" / M {fmt(q['vector_max']['5']['recall'])}"
                    f" (top-1 {fmt(q['top1_similarity'])}; M top-1 {fmt(q.get('vector_max_top1'))})"
                )
        kind = next(iter(runs.values()))["questions"][ids.index(qid)]["kind"]
        lines.append(f"| {qid} | {kind} | " + " | ".join(cells) + " |")
    lines.append("")
    lines.append("相似度門檻（各切塊；無答案題應低於門檻、其他題應高於）：")
    lines.append("| 切塊 | 門檻 | 無答案題正確拒答 | 有答案題誤拒答 |")
    lines.append("|---|---|---|---|")
    for size, record in sorted(runs.items()):
        none = [
            q["top1_similarity"] for q in record["questions"] if q["expect_refusal"]
        ]
        answerable = [
            q["top1_similarity"] for q in record["questions"] if not q["expect_refusal"]
        ]
        for t in THRESHOLDS:
            refused = sum(1 for s in none if s is not None and s < t)
            wrongly = sum(1 for s in answerable if s is not None and s < t)
            out["thresholds"][f"{size}@{t}"] = {
                "refused": refused,
                "of_none": len(none),
                "wrongly_refused": wrongly,
                "of_answerable": len(answerable),
            }
            lines.append(
                f"| {size} | {t:.2f} | {refused}/{len(none)} | {wrongly}/{len(answerable)} |"
            )
    (HERE / "analysis.json").write_text(
        json.dumps(out, indent=1, ensure_ascii=False) + "\n"
    )
    print("\n".join(lines))


if __name__ == "__main__":
    main()
