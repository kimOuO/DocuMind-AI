# ADR 0002：資料儲存用 PostgreSQL + pgvector

- 狀態：已採用
- 日期：2026-11-05
- 對應決策日誌：D10

## 背景

系統要儲存文件、文字切塊、embedding 向量、metadata、摘要、對話與 LLM 呼叫帳本，並支援語意相似度檢索。之後可能加入全文檢索做 Hybrid Search。

## 考慮過的選項

| 選項 | 優點 | 缺點 |
|---|---|---|
| SQLite + numpy（AI 建議） | 零額外服務、Demo 最穩、單檔 | 向量檢索要自己算；不易擴充到多使用者 |
| PostgreSQL + pgvector | 關聯資料與向量在同一個資料庫；內建全文檢索；可擴充 | 多一個容器；約多半天工作 |
| Qdrant | 專用向量庫 | 關聯資料與關鍵字檢索要另外處理，資料分散 |

## 決定

採用 PostgreSQL 16 + pgvector，以 Docker Compose 的 `db` 服務提供，Alembic 管理 schema。
理由（使用者）：在同一個資料庫整合關聯式資料管理與向量檢索，降低資料分散管理的複雜度，方便日後擴充多文件管理、使用者隔離與 Hybrid Search；專案要呈現具備擴充潛力的架構。SQLite 也能實現 RAG，這是依目前技術目標與擴充需求所做的選擇。

## 後果

- 開發與測試都需要資料庫容器：`make dev` 會先起 `db`；CI 用 service container。
- 儲存層放在 repository 介面後面，單元測試用記憶體假實作，不依賴資料庫。
- PostgreSQL 內建全文檢索的排序（`ts_rank_cd`）不是嚴格的 BM25。是否足以支撐 Hybrid Search，由 P4 實驗決定並另寫 ADR。
- Postgres 只對 `127.0.0.1:5433` 開埠，避免與主機上既有服務衝突，也不對外暴露。
