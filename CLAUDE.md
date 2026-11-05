# DocuMind-AI — AI 協作憲章

給 AI coding agent（Claude Code、OpenCode、Codex）讀的專案規則。人類讀者請看 `README.md`。

## 專案是什麼

和碩 PEGAAI 面試作業：一個網站，使用者上傳文件後用聊天介面提問，LLM 依文件內容回答。
目標是「可運作、可驗證、可解釋設計決策的 RAG 系統」，不是包一層 LLM API 的聊天介面。
完整規劃與階段見 `docs/specs/`，目前進度見 `docs/devlog/`。

## 不可違反的限制（來自題目）

1. **LLM 只做 text-to-text。** 不得把檔案、圖片交給任何 LLM 或雲端 API 解析。文件解析一律用本地程式庫。
2. **單次 LLM 呼叫的 prompt + completion ≤ 10,000 tokens。** 超量時用檢索、壓縮、map-reduce 處理，**絕不截斷**。所有呼叫都必須經過 `LLMClient` 的預算守門並寫入 `llm_calls` 帳本。
3. **找不到答案時不編造。** 回答必須有來源引用（檔名、頁碼、片段）。

## 常用指令

| 指令 | 作用 |
|---|---|
| `make setup` | 建立 `backend/.venv`、安裝前後端相依 |
| `make dev` | 起資料庫容器，後端跑 venv、前端跑 Vite（熱重載） |
| `make up` / `make down` | 全部用 Docker 啟動／停止（Demo 與交付模式） |
| `make check` | lint、型別檢查、單元測試（提交前必跑） |
| `make test` | 含需要資料庫的測試 |
| `make transcript` | 匯出對話逐字稿到 `docs/ai-collab/sessions/raw/` |

- **所有開發都在專案的 venv 內進行，不在主機上安裝或執行開發工具。** Python、pip、Node、npm 都在 `backend/.venv/bin/`（Node 由 nodeenv 裝進 venv）。
- 不要用系統 Python、不要 `pip install` 到別處、不要用 nvm 或全域 npm。直接下指令前先 `source backend/.venv/bin/activate`，或用 Makefile。
- 裝了新的 Python 套件，當下就寫進 `backend/requirements*.txt` 並釘死版本。
- 前端 lint 用 eslint。TypeScript 釘在 6.0，因為 typescript-eslint 尚不支援 7.x。
- 一次指令只做一件事，動手前先用一句話說明要做什麼；刪除專案以外的檔案前必須先取得同意。
- 埠：前端開發 5173、後端 8000、Postgres 5433（僅本機）、Docker 版前端 3000、Ollama 11434。

## 架構邊界

- `backend/app/`：`api`（HTTP）→ `chat`（流程編排）→ `retrieval` / `summarize` / `ingestion` → `llm`、`db`。上層可依賴下層，反之不可。
- LLM、Embedding、資料庫都放在介面（Protocol）後面；單元測試用假實作，不得連真服務。
- 新增相依要寫進 `backend/requirements*.txt` 並釘死版本（`==`）。
- 資料表變更一律寫 Alembic migration。
- 維持簡潔：**不加** Redis、Kubernetes、微服務、訊息佇列。想加之前先問。

## 開發流程（SDD → TDD → Checkpoint）

1. **Spec**：動手前先在 `docs/specs/` 寫或更新規格與驗收條件，經使用者核准。
2. **Test first**：先寫會失敗的測試，再實作。
3. **Implement**：小步提交，Conventional Commits（`feat:`、`fix:`、`docs:`、`test:`、`chore:`），英文。
4. **Verify**：`make check` 全綠；生成的程式碼要有測試或實跑結果佐證才算完成。
5. **Checkpoint**：階段結束時執行 `checkpoint` skill（`.claude/skills/checkpoint/SKILL.md`）。

有替代方案的技術選擇要寫 ADR（`docs/adr/`）。參數類決定（chunk size、Top-K、是否 Hybrid）必須引用 `eval/` 的實驗數據。

## 與使用者互動的規則

這個專案的互動過程本身是交付物（面試要報告「如何與 AI 協作」）。

- 提選項前先問使用者自己的想法，或至少附一題開放題；每個選項寫清楚取捨。
- 使用者的補充、反對、否決，**原文**記入 `docs/ai-collab/decision-log.md`。AI 建議被否決或修改的案例一定要保留。
- 紀錄必須忠實：只引用使用者實際說過的話，不替使用者補寫理由；沒說就標「未說明」或當場問。
- 不為了記錄中斷開發：紀錄在 checkpoint 時自動產生。
- 只在五種時刻提醒使用者截圖：重要決策、AI 出錯、人工介入修正、測試前後比較、最終 Demo。

## 語言

- 文件（`docs/`、PPT）、與使用者的對話：繁體中文。
- 程式碼、註解、commit message、API 欄位：英文。
- `README.md`：中英對照。
