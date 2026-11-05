# DocuMind-AI

讓 AI 跟文件對話：上傳文件，用聊天介面提問，LLM 依文件內容回答並附上來源。
Chat with your documents: upload a file, ask questions, get answers grounded in the document with citations.

> 狀態 / Status：已完成帳號（註冊、登入、登出）、文件管理（上傳、清單、刪除）與文件入庫（解析、切塊、建立索引，可看進度、失敗可重試）。問答尚未實作。
> Accounts (register, log in, log out), document management (upload, list, delete) and ingestion (parsing, chunking and indexing, with visible progress and retry) are done. Question answering is not implemented yet.

## 題目限制 / Constraints

| 限制 | 做法 |
|---|---|
| LLM 只做 text-to-text，不得用 GPT/Gemini API 解析文件 | 文件以本地程式庫解析；LLM 為本機 Ollama |
| LLM context 上限 10K tokens | 每次呼叫的 prompt + completion ≤ 10,000：送出前以內附的 Qwen3 tokenizer 在本地計數並分配預算；每個請求都要求 Ollama 拒絕超量的輸入、不捨棄已有的內容（`truncate=false`、`shift=false`），所以不會被悄悄截斷 |

## 快速啟動 / Quick start

需求 / Requirements：Docker（含 Compose）、[Ollama](https://ollama.com) 與下列模型：

```bash
ollama pull qwen3:32b
ollama pull bge-m3
```

Qwen3 的 tokenizer 已內附在專案中（`app/backend/third-party/qwen3-tokenizer/`，Apache-2.0），建置時不需要連到 Hugging Face。內附的只有 tokenizer：上面兩個模型仍須事先用 Ollama 安裝。
The Qwen3 tokenizer is bundled with the project (Apache-2.0), so the build does not download it from Hugging Face. Only the tokenizer is bundled: the two models above must still be installed with Ollama beforehand.

啟動 / Run：

```bash
docker compose up --build -d --wait     # 或 make up
# 開啟 http://127.0.0.1:3000
```

註冊並登入後，可以上傳 PDF、TXT、Markdown 文件（文字檔須為 UTF-8）。上傳後會在背景解析並建立索引，清單上顯示進度；完成後顯示頁數與片段數，失敗時顯示原因並可重試。首頁同時顯示資料庫與 LLM 服務的狀態。
After registering and logging in you can upload PDF, TXT and Markdown documents (text files must be UTF-8). Each upload is parsed and indexed in the background while the list shows its progress; when it is done the list shows the number of pages and chunks, and a failure shows its reason and can be retried. The home page also shows whether the database and the LLM server are healthy.

請從 `http://127.0.0.1:3000` 或 `http://localhost:3000` 開啟。用其他位址（例如區網 IP）開啟時，把該位址加進 `.env` 的 `ALLOWED_ORIGINS`，否則會被來源檢查擋下。
Open the site at one of those two addresses. If you use another address, add it to `ALLOWED_ORIGINS` in `.env`; otherwise state-changing requests are refused by the origin check.

- Ollama 必須監聽容器連得到的位址（`OLLAMA_HOST=0.0.0.0`）。若沒有預裝 Ollama，可改用內建的容器：`docker compose --profile ollama up --build`，並在 `.env` 設定 `COMPOSE_OLLAMA_HOST=ollama`（此模式尚未實測）。
- 設定值見 `.env.sample`。`make setup`、`make up` 會在 `.env` 不存在時由它複製一份。
- API 文件：`http://127.0.0.1:3000/api/v1/docs`。

## 本地開發 / Local development

```bash
make setup    # 建立 .venv（標準 venv + pip，Node 也裝在裡面）並安裝前後端相依
make dev      # 資料庫容器 + 後端（熱重載，:8000）+ 前端（Vite，:5173）
make check    # lint、型別檢查、所有測試（會啟動資料庫容器）
make smoke    # 最小流程驗證：bge-m3 → pgvector → qwen3
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
├── docs/                       規格與架構決策紀錄
│   ├── 02-specs/               規格：01 需求、02 架構、03 介面、04 使用情境
│   └── 03-decisions/           架構決策紀錄：選了什麼、為什麼
├── scripts/                    工具腳本（匯出逐字稿、打包）
├── .venv/                      開發環境（不進版控，make setup 建立）
├── CLAUDE.md / AGENTS.md       給 AI coding agent 的專案規則
└── Makefile / docker-compose.yml / .env.sample
```

原則：資料夾用完整英文名稱、不用縮寫；還沒有內容的資料夾不預先建立。

## 兩個說明題 / The two required explanations

設計已定案，實作完成後會在此補上實測數據。

- **文件 token 超過 context 怎麼辦？** 文件切塊後建立索引，提問時只檢索相關片段；每次呼叫前依預算裝填，裝不下就先壓縮證據而不截斷；呼叫前後各檢查一次 token 數。
- **Summary 怎麼處理？** 入庫時以 map-reduce 建立摘要樹：先對各章節摘要，再合併成全文摘要；合併仍超量就遞迴再摺一層。

## 開發方式 / How this was built

以 AI-native 方式開發（Claude Code），流程為 SDD → TDD → Checkpoint。
每個技術決策，包含 AI 建議被否決或修改的案例，都有紀錄；架構層級的決策與理由見 `docs/03-decisions/`。
