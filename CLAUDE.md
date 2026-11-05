# DocuMind-AI — AI 協作憲章

給 AI coding agent（Claude Code、OpenCode、Codex）讀的專案規則。人類讀者請看 `README.md`。

## 專案是什麼

一個本地執行的 AI 文件管理與問答平台（實作題）：使用者註冊登入後管理自己的文件，用聊天介面對指定的文件提問，LLM 依文件內容回答並附上來源。
最核心的功能是能可靠回答文件問題的 RAG；平台功能不能犧牲題目的驗收條件。
規格見 `docs/02-specs/` 的 `01`–`04`，文件導覽見 `docs/README.md`，目前進度見 `docs/04-dev-journal/`。

- **`docs/` 只有規格（`02-specs/`）、架構決策紀錄（`03-decisions/`）與 `README.md` 納入 git。** 階段回顧、AI 協作紀錄、題目原文只保留在開發機（`.gitignore` 已設定），不要 `git add -f` 它們。
- **四份規格在 P1 完成後凍結。** 不再反覆修改已決定的設計；只有實作或測試發現實際問題時才改，改之前先向使用者說明，並在決策日誌新增一筆。
- `docs/02-specs/archive/` 是已被取代的文件，內容不代表現行設計，不要依它實作。

## 不可違反的限制（來自題目）

1. **LLM 只做 text-to-text。** 不得把檔案、圖片交給任何 LLM 或雲端 API 解析。文件解析一律用本地程式庫。
2. **單次 LLM 呼叫的 prompt + completion ≤ 10,000 tokens。** 超量時用檢索、壓縮、map-reduce 處理，**絕不截斷**。所有呼叫都必須經過 `LLMClient` 的預算守門並寫入 `llm_calls` 帳本。送給 Ollama 的生成請求只能由 `app/backend/app/llm/ollama_api.py` 組裝（固定帶 `num_ctx`、`num_predict`、`truncate=false`、`shift=false`）。
3. **找不到答案時不編造。** 回答必須有來源引用（檔名、頁碼、片段）。

## 常用指令

| 指令 | 作用 |
|---|---|
| `make setup` | 建立 `.venv`、安裝前後端相依 |
| `make dev` | 起資料庫容器，後端跑 venv、前端跑 Vite（熱重載） |
| `make up` / `make down` | 全部用 Docker 啟動／停止（Demo 與交付模式） |
| `make check` | lint、型別檢查、所有不需真實 LLM 的測試（會啟動資料庫容器；提交前必跑） |
| `make test` | 只跑後端測試 |
| `make smoke` | 最小流程驗證：bge-m3 → pgvector → qwen3 |
| `make transcript` | 匯出對話逐字稿到 `docs/05-ai-collaboration/sessions/raw/` |

- **所有開發都在專案的 venv 內進行，不在主機上安裝或執行開發工具。** Python、pip、Node、npm 都在 `.venv/bin/`（Node 由 nodeenv 裝進 venv）。
- 不要用系統 Python、不要 `pip install` 到別處、不要用 nvm 或全域 npm。直接下指令前先 `source .venv/bin/activate`，或用 Makefile。
- 環境變數只能在 `app/backend/app/core/env_loader.py` 讀取；其他地方不得使用 `os.getenv` 或 `os.environ`（有測試檢查）。範例檔是 `.env.sample`。
- 整合測試直接對真實的 PostgreSQL 執行，使用獨立的測試資料庫 `documind_test`；不為 Repository 建假實作。
- 裝了新的 Python 套件，當下就寫進 `app/backend/requirements*.txt` 並釘死版本。
- 前端 lint 用 eslint。TypeScript 釘在 6.0，因為 typescript-eslint 尚不支援 7.x。
- 一次指令只做一件事，動手前先用一句話說明要做什麼；刪除專案以外的檔案前必須先取得同意。
- 埠：前端開發 5173、後端 8000、Postgres 5433（僅本機）、Docker 版前端 3000、Ollama 11434。

## 架構邊界

- 資料夾結構見 `README.md` 的「資料夾導覽」。**命名用完整英文、不用縮寫；還沒有內容的資料夾不要預先建立**，新增資料夾前先向使用者說明用途。
- 後端依功能模組組織（`auth`、`documents`、`ingestion`、`retrieval`、`conversations`、`chat`、`summarization`、`llm`、`monitoring`），用到才建立。分層：Router → Application Service → Repository／LLM Gateway。細節見 `docs/02-specs/02-architecture.md` 第 2 節。
- Router 不直接操作資料庫。業務規則、權限與狀態轉換放在 Service；**Service 的每個方法都明確接收操作者（目前登入的使用者）**。
- Repository 的每個查詢都必須帶擁有者條件。存取別人的資源一律回 `404`。
- 呼叫 Ollama 只能經過 LLM Gateway；預算檢查與帳本不得被繞過。
- API 為 RESTful，前綴 `/api/v1`；GET 不改變資料。
- 不建立通用 Repository 基底類別或尚未使用的介面；只有 LLM、Embedding、Tokenizer 保留介面。
- LLM、Embedding、資料庫都放在介面（Protocol）後面；單元測試用假實作，不得連真服務。
- 新增相依要寫進 `app/backend/requirements*.txt` 並釘死版本（`==`）。
- 資料表變更一律寫 Alembic migration。
- 維持簡潔：**不加** Redis、Kubernetes、微服務、訊息佇列。想加之前先問。

## 開發流程（SDD → TDD → Checkpoint）

1. **Spec**：動手前先在 `docs/02-specs/` 寫或更新規格與驗收條件，經使用者核准。
2. **Test first**：先寫會失敗的測試，再實作。
3. **Implement**：實作到綠燈，小步提交。提交採 Conventional Commits：標題 `type(scope): description` 用英文（例：`feat(documents): add upload, listing and deletion`），scope 是功能模組、不放 P0／P1／P2 等階段編號；內文用繁體中文三段：階段、完成、驗證。Checkpoint Tag 為 `cp-{number}-{outcome}`，Release Tag 為 `v{major}.{minor}.{patch}`。這套規範已凍結，不再為了格式重寫歷史。完整內容見 `.claude/skills/checkpoint/references/git-workflow.md`。
4. **Verify**：`make check` 全綠；生成的程式碼要有測試或實跑結果佐證才算完成。
5. **Checkpoint**：階段結束時執行 `checkpoint` skill（`.claude/skills/checkpoint/SKILL.md`）。

有替代方案的技術選擇要寫 ADR（`docs/03-decisions/`）。參數類決定（chunk size、Top-K、是否 Hybrid）必須引用 `evaluation/` 的實驗數據。

## 與使用者互動的規則

這個專案的互動過程本身是交付物（要報告「如何與 AI 協作」）。

- 提選項前先問使用者自己的想法，或至少附一題開放題；每個選項寫清楚取捨。
- 使用者的補充、反對、否決，**原文**記入 `docs/05-ai-collaboration/decision-log.md`。AI 建議被否決或修改的案例一定要保留。
- 紀錄必須忠實：只引用使用者實際說過的話，不替使用者補寫理由；沒說就標「未說明」或當場問。
- 不為了記錄中斷開發：紀錄在 checkpoint 時自動產生。
- 只在五種時刻提醒使用者截圖：重要決策、AI 出錯、人工介入修正、測試前後比較、最終 Demo。

## 語言

- 文件（`docs/`、PPT）、與使用者的對話：繁體中文。
- 程式碼、註解、API 欄位：英文。
- commit 的標題與標記：英文；commit 的內文：繁體中文。
- `README.md`：中英對照。
