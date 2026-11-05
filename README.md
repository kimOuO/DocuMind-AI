# DocuMind-AI

讓 AI 跟文件對話：上傳文件，用聊天介面提問，LLM 依文件內容回答並附上來源。
Chat with your documents: upload a file, ask questions, get answers grounded in the document with citations.

> 狀態 / Status：**P0 基礎建設完成**。目前只有系統狀態頁；文件上傳與問答自 P2 起實作。
> P0 (scaffolding) is done. Only a system-status page exists so far; upload and Q&A arrive in P2.

## 題目限制 / Constraints

| 限制 | 做法 |
|---|---|
| LLM 只做 text-to-text，不得用 GPT/Gemini API 解析文件 | 文件以本地程式庫解析；LLM 為本機 Ollama |
| LLM context 上限 10K tokens | 每次呼叫的 prompt + completion ≤ 10,000，由程式強制檢查並記錄 |

## 快速啟動 / Quick start

需求 / Requirements：Docker（含 Compose）、[Ollama](https://ollama.com) 與下列模型：

```bash
ollama pull qwen3:32b
ollama pull bge-m3
```

啟動 / Run：

```bash
docker compose up --build -d --wait     # 或 make up
# 開啟 http://127.0.0.1:3000
```

狀態頁應顯示資料庫與 LLM 服務皆「正常」。
The status page should report both the database and the LLM server as healthy.

- Ollama 必須監聽容器連得到的位址（`OLLAMA_HOST=0.0.0.0`）。若沒有預裝 Ollama，可改用內建的容器：`docker compose --profile ollama up --build`，並在 `.env` 設定 `COMPOSE_OLLAMA_BASE_URL=http://ollama:11434`（此模式尚未實測）。
- 設定值見 `.env.example`；不建立 `.env` 也能以預設值執行。

## 本地開發 / Local development

```bash
make setup    # 建立 .venv（標準 venv + pip，Node 也裝在裡面）並安裝前後端相依
make dev      # 資料庫容器 + 後端（熱重載，:8000）+ 前端（Vite，:5173）
make check    # lint、型別檢查、單元測試
make help     # 所有指令
```

只需要 Python 3.12。所有開發工具（含 Node，版本見 `app/frontend/.node-version`）都裝在 `.venv` 內，不會安裝到主機。

## 架構 / Architecture

```
瀏覽器 ──► frontend (Nginx + React) ──/api──► backend (FastAPI)
                                                 ├──► db (PostgreSQL + pgvector)
                                                 └──► Ollama（主機：qwen3:32b、bge-m3）
```

## 資料夾導覽 / Folder guide

```
DocuMind-AI/
├── app/                        要執行的程式
│   ├── backend/                FastAPI 後端（程式、資料庫 migration、測試）
│   └── frontend/               React 前端
├── evaluation/                 檢索與回答品質的評測（P4 開始有內容）
├── sample-documents/           測試用文件（LightRAG 論文）
├── docs/                       依編號順序閱讀
│   ├── 01-assignment/          題目原文
│   ├── 02-specs/               規格；00-project-plan.md 是完整規劃
│   ├── 03-decisions/           架構決策紀錄：選了什麼、為什麼
│   ├── 04-dev-journal/         各階段回顧：做了什麼、遇到的困難、我的想法
│   ├── 05-ai-collaboration/    與 AI 協作的紀錄：決策日誌、session 摘要、逐字稿
│   └── 06-report/              簡報（P7）
├── scripts/                    工具腳本（匯出逐字稿、打包）
├── .venv/                      開發環境（不進版控，make setup 建立）
├── CLAUDE.md / AGENTS.md       給 AI coding agent 的專案規則
└── Makefile / docker-compose.yml / .env.example
```

原則：資料夾用完整英文名稱、不用縮寫；還沒有內容的資料夾不預先建立。

## 兩個說明題 / The two required explanations

設計已定案，實作完成後會在此補上實測數據。詳見 `docs/02-specs/00-project-plan.md` 第一節。

- **文件 token 超過 context 怎麼辦？** 文件切塊後建立索引，提問時只檢索相關片段；每次呼叫前依預算裝填，裝不下就先壓縮證據而不截斷；呼叫前後各檢查一次 token 數。
- **Summary 怎麼處理？** 入庫時以 map-reduce 建立摘要樹：先對各章節摘要，再合併成全文摘要；合併仍超量就遞迴再摺一層。

## 開發方式 / How this was built

以 AI-native 方式開發（Claude Code），流程為 SDD → TDD → Checkpoint。
每個技術決策，包含 AI 建議被否決或修改的案例，都記錄在 `docs/05-ai-collaboration/decision-log.md`。
