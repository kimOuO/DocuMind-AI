# 代表案例（AI 提案 → 人工判斷 → 實作 → 測試驗證 → 改善結果）

P7 從下列候選中挑 3–5 個寫完整，作為 PPT「AI Collaboration」與「Lessons Learned」的內容。
目前只有前兩欄是事實；「實作／驗證／結果」隨階段推進補上，不預先填寫。

| 候選 | AI 提案 | 人工判斷 | 實作 | 測試驗證 | 改善結果 |
|---|---|---|---|---|---|
| A | 資料儲存用 SQLite + numpy | 改 PostgreSQL + pgvector（D10） | P0 完成容器與 migration | pgvector 0.8.7 啟用；檢索待 P2 | 待補 |
| B | Python 環境用 uv | 改標準 venv + pip（D08） | P0 完成 | `sys.prefix` 指向 `backend/.venv` | 待補 |
| C | 後端做完再做前端 | 改 MVP-first（D05） | 待 P2 | 待補 | 待補 |
| D | Hybrid 檢索直接列為核心 | 改為實驗數據決定（D04、D07） | 待 P4 | 待補 | 待補 |
| E | 紀錄四樣全做、逐輪整理 | 改為自動化、精簡（D15） | P0 完成匯出腳本與 hook | 匯出 1 則訊息＋8 次回覆 | 待補 |
