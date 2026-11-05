# 決策日誌

記錄每個重要技術決策：背景、AI 的建議、我的原始回覆、最終選擇、理由、驗證結果、對應 commit。
**AI 建議被否決或修改的案例也保留**，並標為代表案例候選。

規則：「我的原始回覆」只貼我實際說過的話；用選項作答的，記下我選的選項文字；沒說理由的標「未說明」。

## 總覽

| # | 日期 | 決策點 | 最終選擇 | 誰主導 | 案例候選 |
|---|---|---|---|---|---|
| D01 | 11-05 | LLM 後端 | 本地 Ollama `qwen3:32b` | 採納 AI 建議 | |
| D02 | 11-05 | 技術棧 | React + Vite + TS / FastAPI | 採納 AI 建議 | |
| D03 | 11-05 | 時程 | 6–7 天 | 我提供 | |
| D04 | 11-05 | 檢索範圍 | MVP 先做向量檢索；Hybrid、rerank 看實驗數據 | **我修改 AI 原案** | ✓ |
| D05 | 11-05 | 開發順序 | MVP-first | **我主導** | ✓ |
| D06 | 11-05 | 功能範圍 | PDF/TXT/MD、多文件、引用、不編造 | **我主導** | |
| D07 | 11-05 | 檢索品質驗證 | 以實驗比較參數，指定指標 | **我主導** | ✓ |
| D08 | 11-05 | Python 環境 | 標準 venv + pip | **我否決 AI 建議** | ✓ |
| D09 | 11-05 | 部署 | Docker Compose | **我主動追加** | |
| D10 | 11-05 | 資料儲存 | PostgreSQL + pgvector | **我否決 AI 建議** | ✓ |
| D11 | 11-05 | 架構控制 | 不加 Redis、K8s、微服務 | **我主導** | |
| D12 | 11-05 | Ollama 位置 | 容器連主機既有的 Ollama | 採納 AI 建議 | |
| D13 | 11-05 | 語言 | 文件繁中、程式英文 | 採納 AI 建議 | |
| D14 | 11-05 | 版控與交付 | GitHub 私有 repo＋zip | 採納 AI 建議 | |
| D15 | 11-05 | 互動紀錄方式 | 決策日誌＋精簡摘要＋自動逐字稿＋選擇性截圖＋代表案例 | **我主導**（重新設計 AI 初稿） | ✓ |
| D16 | 11-05 | PPT | AI 產出 .pptx 初稿 | 採納 AI 建議 | |
| D17 | 11-05 | PDF 解析／Embedding／UI | PyMuPDF／`bge-m3`／Tailwind + shadcn/ui | 採納 AI 建議 | |
| D18 | 11-05 | 10K 的解讀 | 輸入＋輸出合計 ≤ 10,000 | 採納 AI 建議 | |
| D19 | 11-05 | 前端 lint 工具 | eslint | **我否決 AI 的做法**（AI 未先問就用 oxlint） | ✓ |
| D20 | 11-05 | 開發工具的隔離範圍 | Node 也裝進 venv，不裝在主機 | **我主導** | ✓ |
| D21 | 11-05 | TypeScript 版本 | 釘在 6.0（為了相容 eslint） | 採納 AI 的處置（事後告知） | |
| D22 | 11-05 | 資料夾結構 | 依用途分區＋編號，完整英文名稱，不預建空資料夾 | **我提出問題並選定方案** | ✓ |
| D23 | 11-05 | GitHub repo 可見性 | 改為私有後才推送 | AI 發現不一致並提出，我修正 | ✓ |

注意：本檔 D01–D21 的內文是當時的紀錄，其中的路徑（如 `backend/.venv`、`docs/ai-collab/`）是 D22 調整前的舊路徑。

統計（規劃階段 D01–D18）：18 個經我確認的決策中，9 個採納 AI 建議、1 個由我提供資訊、8 個由我主導、修改或否決。

---

## 詳細紀錄

### D01 LLM 後端

- **背景**：題目限制 LLM 只做 text-to-text、context 上限 10K。
- **AI 建議**：本地 Ollama（建議）；其他選項為雲端 API、本地為主加雲端備援。
- **我的原始回覆**：選擇「本地 Ollama (Recommended)」。理由未說明。
- **最終選擇**：本地 Ollama `qwen3:32b`，程式走可切換的介面。
- **驗證結果**：P0 確認主機 Ollama 0.24.0 在線，`qwen3:32b`、`bge-m3` 可用。
- **對應 commit**：`dc51c12`

### D02 技術棧

- **AI 建議**：React + Vite + TS / FastAPI（建議）；其他選項為 Next.js / FastAPI、純 Python。
- **我的原始回覆**：選擇「React+Vite+TS / FastAPI (Recommended)」。理由未說明。
- **驗證結果**：P0 前後端骨架可跑，前端 3 個、後端 4 個測試通過。
- **對應 commit**：`dc51c12`

### D03 時程

- **我的原始回覆**：選擇「6–7 天」。

### D04 檢索範圍

- **AI 原案**：混合檢索（BM25＋向量）、rerank、問題路由列為核心，知識圖譜為加分。我在第一輪選了這個建議選項。
- **我的原始回覆**（之後修改）：
  > 1. 功能與檢索：優先完成 PDF、TXT、Markdown 文件上傳，支援多文件問答、來源引用（文件名稱、頁碼、引用片段），並設計「找不到答案時不應自行編造」的機制。若時間允許，再加入 Hybrid Search（Vector + Full-text Search）及檢索結果重排序。
- **最終選擇**：MVP 先做向量檢索；Hybrid 與 rerank 由 P4 的實驗數據決定是否加入。
- **驗證結果**：待 P4。
- **對應 commit**：待回填

### D05 開發順序

- **AI 原案**：先規格，再依序做入庫、問答、前端（後端做完才有介面）。
- **我的原始回覆**：
  > 2. 開發順序：採用 MVP-first 策略，優先完成文件上傳 → Parsing → Chunking → Embedding → PostgreSQL/pgvector → Retrieval → LLM Answer 的完整端到端流程，確保基本功能可展示，再逐步提升檢索品質與使用體驗。
- **最終選擇**：P2 就打通端到端（含最小聊天介面），之後才加深。
- **驗證結果**：待 P2。

### D06 功能範圍

- **我的原始回覆**：同 D04 引文第 1 點。
- **最終選擇**：PDF/TXT/Markdown 上傳、多文件問答、引用含檔名＋頁碼＋片段、找不到答案不編造。
- **驗證結果**：待 P2、P3。

### D07 檢索品質驗證

- **AI 原案**：有評測題庫與自家消融，但實驗變因與指標由 AI 擬定。
- **我的原始回覆**：
  > 3. 檢索品質驗證：希望建立一組小型測試資料與標準問題，比較不同 Chunk Size、Top-K、Vector Search 與 Hybrid Search 的結果，使用 Recall@K、來源命中率與回答正確性等指標，讓架構設計與參數選擇有實驗依據，而不是只憑感覺調整。
- **最終選擇**：P4 依此設計實驗矩陣；參數類 ADR 必須引用實驗數據。
- **驗證結果**：待 P4。

### D08 Python 環境

- **背景**：我在 AI 第一次送審計畫時退回並要求：
  > 還要建立 python env 作環境隔離 部屬採用docker
- **AI 建議**：uv + `.venv`（建議），理由是免 sudo、速度快、Dockerfile 可用同一份 lock。其他選項為 conda、標準 venv + pip。
- **我的原始回覆**：選擇「標準 venv + pip」。理由：
  > 主要是考量專案只有一週的開發時間，且最終需要提供程式碼供面試官在本地端執行。相較於引入 uv，我希望先降低額外的工具依賴，使用 Python 常見的虛擬環境搭配 requirements.txt，讓環境建立與專案重現流程更直觀
- **最終選擇**：`backend/.venv`＋釘版的 `requirements.txt`／`requirements-dev.txt`。見 ADR 0001。
- **驗證結果**：P0 建立成功，`sys.prefix` 指向 `backend/.venv`，系統 Python 未被安裝任何套件。這台機器缺 `ensurepip`，改用 `python3 -m venv --without-pip` 加 `get-pip.py`，未使用 sudo。
- **對應 commit**：`dc51c12`

### D09 部署

- **AI 原案**：Docker Compose 列為加分項。
- **我的原始回覆**：同 D08 背景引文（「部屬採用docker」）。
- **最終選擇**：Docker Compose 為正式部署方式，三個服務（db、backend、frontend）。
- **驗證結果**：P0 `make up` 後三個容器皆 healthy；經 Nginx 存取 `/api/health` 回傳 `status: ok`。
- **對應 commit**：`dc51c12`

### D10 資料儲存

- **AI 建議**：SQLite + numpy（建議），理由是零額外服務、Demo 最穩。其他選項為 PostgreSQL + pgvector、Qdrant。
- **我的原始回覆**：選擇「PostgreSQL + pgvector」。理由：
  > 這次選擇 PostgreSQL + pgvector，主要是考量「讓 AI 與文件對話」本質上是一個 RAG 系統，需要管理文件、文字切塊（Chunks）、Embedding 向量及相關 Metadata，並支援語意相似度檢索。相較於 SQLite 搭配額外的向量搜尋方案，PostgreSQL + pgvector 可以在同一個資料庫中整合關聯式資料管理與向量檢索，降低資料分散管理的複雜度，也方便後續擴充多文件管理、使用者隔離及混合檢索（Hybrid Search）。此外，我希望這次專案不只是完成基本 Demo，也能呈現具備擴充潛力的系統架構。不過，這不代表 SQLite 無法實現 RAG，而是考量目前的技術目標與未來擴充需求後，選擇 PostgreSQL + pgvector 作為較合適的方案。
- **最終選擇**：PostgreSQL 16 + pgvector，Alembic 管 schema。見 ADR 0002。
- **驗證結果**：P0 容器啟動，migration 啟用 pgvector 0.8.7；向量檢索功能待 P2。
- **對應 commit**：`dc51c12`

### D11 架構控制

- **我的原始回覆**：
  > 5. 架構控制：目前先維持簡潔的服務設計，不為了展示技術而加入 Redis、Kubernetes 或複雜的微服務。PostgreSQL + pgvector 可透過 Docker Compose 啟動，但應保留容易重現的本地 Demo 流程。整體目標是完成一個可運作、可驗證、可解釋設計決策的 RAG 系統，而非單純整合 LLM API 的聊天介面。若時間不足，優先保證端到端流程、來源引用、基本檢索測試和完整 Demo，其他進階功能列為延伸項目。
- **最終選擇**：寫入 `CLAUDE.md` 作為規則；AI 原本列的 Prometheus 指標加分項因此移除。

### D12 Ollama 位置

- **AI 建議**：連主機既有的 Ollama（建議）；另一選項是把 Ollama 放進 compose。
- **我的原始回覆**：選擇「連主機的 Ollama (Recommended)」。理由未說明。
- **驗證結果**：P0 確認主機 Ollama 監聽 `0.0.0.0:11434`，後端容器經 `host.docker.internal` 連線成功。見 ADR 0003。
- **對應 commit**：`dc51c12`

### D13 語言／D14 版控與交付／D16 PPT

- **我的原始回覆**：分別選擇「繁中文件＋英文程式 (Recommended)」「GitHub 私有 repo＋zip (Recommended)」「AI 產出 .pptx 初稿 (Recommended)」。理由未說明。
- **驗證結果**：D14 的遠端 repo 尚未建立（待我提供）。

### D15 互動紀錄方式

- **背景**：我在 AI 第三次送審計畫時退回並要求：
  > 另外因為我向他們報告使用AI的方式 所以現在這個plan mode 要幫我記錄良好的使用方式 並且在你提供選項時 不只聽從你的建議 我也提出想法 在其他給你更詳細的建議 我希望要有這樣的互動紀錄 甚至截圖
- **AI 初稿**：決策日誌＋每次 session 逐輪整理＋使用者截圖與 `/export` 逐字稿，四樣都做。
- **我的原始回覆**：
  > 我希望採用「結構化決策日誌＋關鍵互動紀錄＋自動化原始紀錄」的方式，兼顧可追溯性與開發效率。1. 決策日誌（必做）：記錄重要技術決策，包括問題背景、AI 建議、我的原始回覆、最終選擇、選擇理由、驗證結果與對應 Commit。除了成功決策，也要保留 AI 建議被否決或修改的案例。2. Session Summary（必做，但精簡）：每次開發 Session 結束時，自動整理本次目標、AI 完成的工作、我介入修改的部分、遇到的問題及下一步。不需要逐輪人工整理所有對話。3. 原始逐字稿（建議保留）：若 AI Coding 工具支援 /export 或其他匯出功能，就在重要 Checkpoint 匯出完整對話，作為原始證據保存，不需要人工逐字整理。4. 關鍵截圖（選擇性）：只針對重要決策、AI 發生錯誤、人工介入修正、測試前後比較及最終 Demo 截圖，不需要每個步驟都截圖。5. AI 協作品質分析：希望最後能從紀錄中挑選 3～5 個代表性案例，呈現「AI 提案 → 人工判斷 → 實作 → 測試驗證 → 改善結果」的完整過程，作為 PPT 的 AI Collaboration 與 Lessons Learned 內容。請盡量將上述紀錄流程自動化，避免為了記錄而中斷主要開發工作。若時間有限，優先確保決策日誌、重要 Commit、關鍵測試結果與代表性 AI 互動證據完整，其他紀錄可以簡化。
- **最終選擇**：本檔＋`sessions/`（精簡摘要）＋`sessions/raw/`（腳本自動匯出）＋`screenshots/`（選擇性）＋`cases.md`。
- **驗證結果**：P0 `scripts/export_transcript.py` 匯出本次 session，收錄 1 則輸入訊息與 8 次回覆；電子郵件與電話已遮蔽。SessionEnd／PreCompact hook 已設定，尚未實際觸發過。
- **對應 commit**：`dc51c12`

### D17 PDF 解析／Embedding／UI、D18 10K 的解讀

- **背景**：這幾項原本是 AI 自行決定、未經確認。我要求：
  > 再跟我確認一次決策點
  AI 因此列出 9 項未確認的決定並逐一詢問。
- **我的原始回覆**：選擇「全部照建議」，並貼上題目原文。AI 據此在計畫中加入「題目需求追溯表」。
- **驗證結果**：`bge-m3` 已下載可用；其餘待 P2。

### D19 前端 lint 工具

- **背景**：計畫寫的是 eslint。P0 建立前端時，Vite 的官方 React 樣板已改用 oxlint。
- **AI 的決定**：沿用樣板預設的 oxlint，未另裝 eslint。這一項**沒有先問我**，事後才提出確認。
- **我的原始回覆**：
  > 用eslint 且記得使用venv內開發 不再本機開發
- **最終選擇**：改用 eslint（flat config，含 typescript-eslint、react-hooks、react-refresh），移除 oxlint。
- **驗證結果**：`npm run check`（eslint、tsc、vitest）通過。
- **對應 commit**：`dc51c12`

### D20 開發工具的隔離範圍

- **背景**：P0 一開始，AI 用 nvm 把 Node 裝在使用者家目錄（`~/.nvm`），只有 Python 在 venv 內。
- **我的原始回覆**：同 D19 引文（「記得使用venv內開發 不再本機開發」）。
- **AI 的處置**：用 nodeenv 把 Node 裝進 `backend/.venv`，Makefile 與 CI 改用 venv 內的 Node。
- **過程中的介入**：AI 把「改設定、補 requirements、刪除 `~/.nvm`」包成一個指令且未說明，被我擋下並質疑：
  > 可以解釋一下目前是要執行甚麼嗎 不是應該盡速venv後 開始安裝每一個套件 並寫成requirment嗎
  AI 說明現況並列出三個待決事項後，我回覆：
  > 好接受
- **最終選擇**：Node 裝在 venv 內；`nodeenv` 寫入 `requirements-dev.txt`；`~/.nvm` 未取得明確同意，AI 不刪除，留給我自行處理。
- **驗證結果**：`which node` 指向 `backend/.venv/bin/node`；`make check` 全數通過。
- **對應 commit**：`dc51c12`

### D21 TypeScript 版本

- **背景**：Vite 樣板帶的是 TypeScript 7.0，但 typescript-eslint 8.72 只支援 `<6.1.0`，eslint 因此裝不起來。
- **AI 的處置**：把 TypeScript 降到 6.0.3。這個副作用是事後才告訴我的。
- **我的原始回覆**：
  > 好接受
- **驗證結果**：`tsc -b` 與 3 個前端測試通過。
- **對應 commit**：`dc51c12`

### D22 資料夾結構

- **背景**：AI 在 P0 依核准的計畫建立資料夾，包含許多還沒有內容的空資料夾，並使用 `adr`、`devlog`、`eval`、`ai-collab` 等縮寫。
- **我的原始回覆**（回答 P0「我的想法」時提出）：
  > 目前的資料夾 以及資料夾內的資料夾 太亂了 讓我不好看出檔案結構的目的 取名也不夠明確看出資料夾目的
- **AI 的處置**：沒有直接改，先提出三種結構草圖（依用途分區＋編號／位置不動只改名與清空／文件資料夾用中文名），並問我哪些部分最亂。
- **我的原始回覆**：選擇「依用途分區＋編號」。最亂的部分四項全選：「後端裡一堆空資料夾, 英文縮寫看不懂, docs 底下分類看不懂, 最上層東西太多」。
- **最終選擇**：
  - 程式集中到 `app/backend`、`app/frontend`；`eval` → `evaluation`；`test_data` → `sample-documents`。
  - `docs/` 改為 `01-assignment`、`02-specs`、`03-decisions`、`04-dev-journal`、`05-ai-collaboration`、`06-report`。
  - 移除 `note/`、`data/`、`docs/design/` 與後端 6 個空套件；規則寫入 `CLAUDE.md`：完整英文名稱、不預建空資料夾。
  - venv 移到專案根目錄 `.venv`。
- **驗證結果**：用 `make setup` 從零重建 `.venv` 成功；`make check` 全過（後端 4 個、前端 3 個測試）；`make up` 後 `/api/health` 回傳 `status: ok`。
- **對應 commit**：tag `cp-0-foundation`

### D23 GitHub repo 可見性

- **背景**：規劃時我選的是私有 repo（D14）。我貼給 AI 的 repo 網址實際上是公開的。
- **AI 的處置**：推送前先查詢遠端，發現不登入也查得到（公開），停下來問我，並說明推上去會公開題目 PDF、作答與逐字稿。
- **我的原始回覆**：
  > 改好了
- **驗證結果**：AI 再次查詢，未登入狀態回傳 404，確認已是私有。之後 AI 的推送指令被 Claude Code 的權限機制擋下，需由我自行執行 `git push`。
- **對應 commit**：不適用

### D20 補充：`~/.nvm` 的刪除

- AI 單獨詢問是否刪除它稍早安裝在家目錄的 `~/.nvm`。**我的原始回覆**：選擇「請幫我刪掉」。AI 刪除後確認該路徑已不存在。
