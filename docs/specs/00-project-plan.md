# DocuMind-AI 專案規劃：讓 AI 跟文件對話（和碩 PEGAAI 面試作業 題目二）

## Context（為什麼做、要達成什麼）

和碩 AI Engineer 面試作業，期限 D+7。題目：做一個有聊天介面的網站，上傳文件後提問，LLM 依文件回答。

- **限制**：(1) 不能用 GPT/Gemini API 解析文件，LLM 只做 text-to-text；(2) 假定 LLM max context = 10K tokens。
- **必答三題**（文件為 LightRAG 論文 arXiv 2410.05779）：摘要全文、比較 LightRAG 與 GraphRAG、消融版本的表現。
- **必須說明**：文件超過 context 怎麼處理、summary 怎麼處理。
- **交付物**：程式碼（zip 或連結）、PPT（架構與結果／如何與 AI 協作／心得）、本地 Demo。
- **評分隱含重點**：和碩 Roadmap 的 Vibe Coding 欄寫明 **SDD、TDD、Checkpoint**。

**使用者定的整體目標**：完成一個可運作、可驗證、可解釋設計決策的 RAG 系統，而非單純整合 LLM API 的聊天介面。時間不足時的優先順序：端到端流程 → 來源引用 → 基本檢索測試 → 完整 Demo；其他列為延伸。

現況：資料夾只有 `docs/`（題目 PDF）、`test_data/`（論文 PDF）、`note/`（空）。不是 git repo。機器：2× A40 48GB、Ollama 0.24.0、Docker 29.5（含 `nvidia` runtime、Compose v5.1）、Python 3.12；**沒有** Node、conda、gh，系統 Python 缺 `ensurepip`，git 身分未設定。

## 決策總表

「來源」欄是互動紀錄的依據：誰主導了這個決定。

| # | 決策點 | 決定 | 來源 |
|---|---|---|---|
| 1 | LLM 後端 | 本地 Ollama `qwen3:32b`；OpenAI 相容介面可切換 | 採納 AI 建議 |
| 2 | 技術棧 | React + Vite + TypeScript / FastAPI + SSE | 採納 AI 建議 |
| 3 | 時程 | 6–7 天 | 使用者提供 |
| 4 | 檢索範圍 | MVP 先做向量檢索；Hybrid 與 rerank 由實驗數據決定是否加入；圖譜為延伸 | **使用者修改**（AI 原案把 Hybrid 列為核心） |
| 5 | 開發順序 | MVP-first：先打通端到端，再提升品質 | **使用者主導**（AI 原案是後端做完才做前端） |
| 6 | 功能範圍 | PDF/TXT/Markdown、多文件問答、引用（檔名＋頁碼＋片段）、找不到答案不編造 | **使用者主導** |
| 7 | 檢索品質驗證 | 用實驗比較 chunk size、Top-K、Vector vs Hybrid，指標 Recall@K、來源命中率、回答正確性 | **使用者主導**（AI 原案有評測，使用者指定了實驗變因與指標） |
| 8 | Python 環境 | 標準 venv + pip + requirements.txt | **使用者否決 AI 建議**（AI 建議 uv） |
| 9 | 部署 | Docker Compose | **使用者主動追加**（AI 原案列為加分） |
| 10 | 資料儲存 | PostgreSQL + pgvector | **使用者否決 AI 建議**（AI 建議 SQLite） |
| 11 | 架構控制 | 維持簡潔；不加 Redis、Kubernetes、微服務 | **使用者主導** |
| 12 | Ollama 位置 | 連主機既有的 Ollama；另附可選 compose profile | 採納 AI 建議 |
| 13 | 語言 | 文件與 PPT 繁中；程式、commit 英文；README 中英對照 | 採納 AI 建議 |
| 14 | 版控與交付 | GitHub 私有 repo＋zip | 採納 AI 建議 |
| 15 | 互動紀錄 | 結構化決策日誌＋精簡 session 摘要＋自動化原始紀錄＋選擇性截圖＋3–5 個代表案例 | **使用者主導**（AI 提初稿，使用者重新設計） |
| 16 | PPT | AI 產出 .pptx 初稿 | 採納 AI 建議 |
| 17 | PDF 解析／Embedding／UI | PyMuPDF／Ollama `bge-m3`／Tailwind + shadcn/ui | 採納 AI 建議 |
| 18 | 10K 的解讀 | 輸入＋輸出合計 ≤ 10,000 tokens | 採納 AI 建議 |

使用者對 #8、#10 的理由與 #4–#7、#11、#15 的完整原話見文末附錄，P0 原文轉入決策日誌。

## 題目需求追溯表

| 題目原文 | 對應設計 | 如何驗證 |
|---|---|---|
| 不能用 GPT/Gemini API 解析文件 | PyMuPDF 本地解析，全程不呼叫雲端 | 程式無雲端 API 相依 |
| LLM 只做 text-to-text | `LLMClient` 介面只收字串、回字串 | 型別與單元測試 |
| max context 10K | `TokenBudget` 三層防線（§一.1） | 呼叫帳本最大值 ≤ 10,000 |
| 有聊天介面的 website，可上傳文件 | React 介面（§五） | 手動端到端 |
| LLM 根據提供的資料回答 | 檢索＋引用＋無答案拒答 | 評測的正確性與拒答率 |
| 問題 1：summary this document | 入庫時建的摘要樹（§一.3） | 評測題庫 |
| 問題 2：compare LightRAG with GraphRAG | 子問題拆解＋多路檢索 | 評測題庫 |
| 問題 3：ablated versions 的表現 | Table 2 表格 chunk＋4.3 內文 | 評測題庫，核對表格數字 |
| 以 AI Native 方法實作 | SDD/TDD/Checkpoint、互動紀錄（§三、§四） | commit、tag、決策日誌 |
| 打包寄出 | `make package` 產生 zip | 乾淨資料夾解壓後能啟動 |
| 說明如何處理超過 context／summary | `docs/specs/02`、`05`、README、PPT | — |
| PPT 三項內容 | P7 產出 .pptx | — |
| Demo：local run | `docker compose up` | 手動端到端 |

---

## 一、系統設計

### 1. 10K context 的處理：三層防線，永不截斷（MVP 就要有）

| 區塊 | 預算 |
|---|---|
| System prompt＋指令 | ~500 |
| 對話記憶（近幾輪＋舊對話滾動摘要） | ~800 |
| 使用者問題 | ~200 |
| 檢索到的證據 | ~5,500 |
| 輸出保留 | ~2,500 |
| 安全邊際 | ~500 |

1. **組裝前**：`ContextPacker` 依預算裝填證據；裝不下時不截斷，改走「證據壓縮」（對超量證據做 map-reduce 再裝填）。
2. **呼叫前**：`LLMClient` 預先計數，超過即拋 `ContextBudgetExceeded`（Ollama 超過 `num_ctx` 會默默截斷，必須自己擋）。同時 `num_ctx=10000`。
3. **呼叫後**：把 Ollama 回傳的 `prompt_eval_count + eval_count` 寫入 `llm_calls` 帳本；UI 顯示用量；測試斷言全部 ≤ 10,000。

### 2. 文件解析與索引

- **格式**：PDF（PyMuPDF）、TXT、Markdown（依標題切章節）。解析器放在同一介面後面。
- **MVP 切塊**：依 token 數固定長度切、有重疊，帶 metadata（文件、頁碼、位置）。
- **加深（P4，由實驗決定是否採用）**：
  - 結構感知切塊：修正 small-caps 標題（`I NTRODUCTION`），依章節切，前置章節標頭。
  - 表格獨立成 chunk：Table 2 是四區塊複合表，不可切開，保留 caption，另存逐列白話化文字。
  - 附錄 Figure 4–7 的 prompt 是圖片，抽不到文字：列為已知限制，本地 OCR 為延伸。
- **儲存（PostgreSQL + pgvector）**：
  - 資料表：`documents`、`chunks`、`summary_nodes`、`conversations`、`messages`、`llm_calls`。
  - `chunks.embedding vector(1024)`＋HNSW cosine 索引；`tsvector` 欄位＋GIN 索引留給 Hybrid。
  - SQLAlchemy 2 + psycopg 3，Alembic 管 schema。儲存層在 repository 介面後面，單元測試用記憶體假實作。
- **Embedding**：Ollama `bge-m3`（多語，不必裝 torch）。

### 3. Summary 的處理：入庫時建「摘要樹」

- **Map**：每個章節（或每批 ≤ ~6K tokens 的 chunks）→ 局部摘要（≤ ~300 tokens，保留關鍵數字）。
- **Reduce**：局部摘要合併 → 全文摘要＋文件卡；合併仍超量就遞迴再摺一層。
- 摘要節點也進索引：全域問題命中摘要，細節問題命中原文。
- 依文件 hash 快取；入庫進度用 SSE 推給前端。

### 4. 問答流程

`問題 → 記憶濃縮成獨立問題 → Router → 檢索 → 裝填 → 生成（串流）→ 引用`

- **多文件**：對話可選全部或部分文件；檢索依選取範圍過濾；裝填時保證跨文件的證據都有份。「summary this document」在多文件時依選取的文件各自取摘要樹。
- **Router**（規則優先、LLM 後援）：`summary` 走摘要樹；`comparison` 拆子問題多路檢索；其餘走一般檢索。
- **引用**：每個論點附來源，含**文件名稱、頁碼、引用片段**；UI 可點開看原文。
- **找不到答案時不編造**，四道機制：
  1. 檢索相似度低於門檻 → 直接回覆「文件中找不到相關內容」，不呼叫生成。
  2. Prompt 規定只能依證據作答，證據不足要明說。
  3. 生成後檢查：沒有任何引用的回答標記為「無依據」。
  4. 評測題庫放入無答案題，量測正確拒答率；門檻由數據決定。
- **檢索**：MVP 用向量 Top-K。Hybrid（全文檢索＋向量，RRF 融合）與 rerank 在 P4 以實驗結果決定是否加入。

### 5. 環境隔離與部署

**開發：標準 venv + pip**

- `backend/.venv` 專案專屬環境，不碰系統 Python。
- 建立方式（P0 第一件事）：首選你執行 `sudo apt install python3.12-venv`；沒有 sudo 時用 `python3 -m venv --without-pip` 再以 `get-pip.py` 補 pip。
- 相依寫在 `requirements.txt`、`requirements-dev.txt`，版本釘死（`==`），面試官 `pip install -r` 即可重現。
- 指令一律經 Makefile 呼叫 `backend/.venv/bin/…`。
- 前端：nvm 裝 Node LTS，`.nvmrc` 與 `package-lock.json` 鎖版本。

**部署：Docker Compose（三個服務，維持簡潔）**

- `db`：`pgvector/pgvector:pg16`，具名 volume，healthcheck。只對 `127.0.0.1:5433` 開埠供開發用（主機 3306、8080 已被占用）。
- `backend`：映像內建 venv 並 `pip install -r requirements.txt`；非 root；啟動時 `alembic upgrade head`。
- `frontend`：Node 建置 → Nginx 提供靜態檔並反向代理 `/api`（SSE 關閉 proxy buffering）。
- **Ollama**：後端容器經 `host.docker.internal` 連主機 Ollama。P0 驗證連線；若主機只聽 127.0.0.1，需要你調整 `OLLAMA_HOST`，或改用 `ollama` profile。結果寫 ADR。
- `make dev`：只起 `db`，後端跑 venv、前端跑 Vite。`make up`：全部容器化，Demo 與交付用。
- 不加 Redis、Kubernetes、微服務。

### 6. 延伸項目（P6，有時間才做）

rerank｜輕量知識圖譜（呼應 GRAG）｜圖片 OCR。

---

## 二、專案資料夾規劃

```
DocuMind-AI/
├── CLAUDE.md            # AI 協作憲章：慣例、指令、10K 鐵則、互動規則
├── AGENTS.md            # 指向 CLAUDE.md（OpenCode / Codex 讀這個）
├── README.md            # 中英對照：快速啟動、架構、兩個說明題的答案
├── Makefile             # setup / dev / up / down / check / test / eval / package
├── docker-compose.yml   # db + backend + frontend（profile: ollama）
├── .env.example  .gitignore  .dockerignore  .editorconfig  .pre-commit-config.yaml
├── .github/             # workflows/ci.yml、pull_request_template.md
├── .claude/             # settings.json（權限、hook）、skills/checkpoint
├── backend/
│   ├── Dockerfile  pyproject.toml（工具設定）
│   ├── requirements.txt  requirements-dev.txt
│   ├── .venv/              # 隔離環境（gitignore）
│   ├── alembic.ini  migrations/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/            # documents.py  chat.py  health.py  schemas.py
│   │   ├── core/           # config.py  logging.py  tokens.py  errors.py
│   │   ├── db/             # session.py  models.py  repositories.py
│   │   ├── llm/            # base.py  ollama.py  fake.py  prompts/
│   │   ├── ingestion/      # parsers/{pdf,text,markdown}.py  chunker.py  tables.py  pipeline.py
│   │   ├── retrieval/      # embedder.py  vector.py  hybrid.py  packer.py
│   │   ├── summarize/      # map_reduce.py  tree.py
│   │   ├── chat/           # router.py  memory.py  orchestrator.py  citations.py  guard.py
│   │   └── observability/  # ledger.py
│   └── tests/              # unit/  integration/  fixtures/
├── frontend/
│   ├── Dockerfile  nginx.conf  .nvmrc  package.json
│   └── src/  # components/ui  features/{chat,documents,inspector}  lib/api  styles/tokens.css
├── eval/                # golden/*.yaml  run_eval.py  experiments/  reports/
├── docs/
│   ├── assignment/      # 題目 PDF（由 docs/ 移入）
│   ├── specs/           # 00-prd  01-architecture  02-token-budget  03-ingestion
│   │                    # 04-retrieval  05-summarization  06-api  07-frontend  08-deployment
│   ├── adr/             # 架構決策紀錄
│   ├── design/          # design-system.md  wireframes.md
│   ├── devlog/          # 每階段回顧 P0…P7（困難、解法、我的想法）
│   ├── ai-collab/       # decision-log.md  cases.md  insights.md
│   │                    # sessions/（摘要）  sessions/raw/（逐字稿）  screenshots/
│   └── report/          # 簡報大綱、.pptx、圖
├── note/                # 你的隨手筆記（原樣保留）
├── test_data/           # 測試文件（既有）
├── data/                # 上傳檔（gitignore；容器掛 volume）
└── scripts/             # setup.sh  package.sh  export_transcript.py
```

API：`POST /api/documents`、`GET /api/documents`、`GET /api/documents/{id}/events`（SSE 入庫進度）、`DELETE /api/documents/{id}`、`POST /api/chat`（SSE：route / retrieval / token_usage / delta / citations / done）、`GET /api/conversations/{id}`、`GET /api/llm-calls`、`GET /api/health`。

---

## 三、AI-Native 開發流程（SDD + TDD + Checkpoint）

每個階段跑同一個迴圈：

1. **Spec**：在 plan mode 寫規格與驗收條件。AI 提案前先問你的想法，你核准或修改。
2. **Test first**：由驗收條件產生會失敗的測試。
3. **Implement**：實作到綠燈，小步 commit（Conventional Commits）。
4. **Verify**：`make check`、`/code-review`、你看 diff。AI 生成的程式碼要有測試或實跑結果佐證才算完成。
5. **Checkpoint**：`checkpoint` skill 一次做完：跑檢查 → 更新決策日誌與 commit 對應 → 寫 session 摘要 → 匯出逐字稿 → `git tag cp-N` → push。

配套：

- **分支**：`main` 受保護，短命 feature 分支＋PR。
- **CI**（GitHub Actions）：ruff、mypy、pytest（pgvector service container）、eslint、tsc、vitest、Docker 映像建置。
- **測試**：LLM 用假 provider、儲存層用假實作做單元測試；真打 Ollama 的測試標 `@pytest.mark.llm`，CI 不跑。
- **ADR**：有替代方案的選擇都寫。預計：PDF 解析器、token 計數法、qwen3 thinking 開關、venv+pip、PostgreSQL+pgvector、容器連 Ollama、chunk size 與 Top-K、是否採 Hybrid、是否 rerank、摘要策略。參數類的 ADR 必須引用實驗數據。

---

## 四、紀錄與報告（依使用者的設計）

原則：**紀錄忠實、流程自動化、不為了記錄中斷開發。** 你的想法只記你實際說過的話。

| 紀錄 | 必要性 | 內容 | 如何產生 |
|---|---|---|---|
| 決策日誌 `decision-log.md` | 必做 | 問題背景｜AI 建議｜我的原始回覆｜最終選擇｜選擇理由｜驗證結果｜對應 commit｜是否為案例候選。**包含 AI 建議被否決或修改的案例** | 決策當下我寫入；checkpoint 時補 commit 與驗證結果 |
| Session 摘要 `sessions/日期-序號.md` | 必做、精簡 | 本次目標｜AI 完成的工作｜我介入修改的部分｜遇到的問題｜下一步 | `checkpoint` skill 自動產生，不逐輪整理 |
| 原始逐字稿 `sessions/raw/` | 建議 | 完整對話 | `scripts/export_transcript.py` 把 Claude Code 的 session 檔轉成 Markdown，checkpoint 時自動執行；也可手動 `/export`。匯出時遮蔽金鑰與個資；是否隨 zip 交付由你決定 |
| 截圖 `screenshots/` | 選擇性 | 只截：重要決策、AI 出錯、人工介入修正、測試前後比較、最終 Demo | 由你截（AI 看不到螢幕）；我在這五種時刻提醒一句 |
| 代表案例 `cases.md` | 最後整理 | 3–5 個「AI 提案 → 人工判斷 → 實作 → 測試驗證 → 改善結果」 | P7 從決策日誌的案例候選中挑，直接變成 PPT 內容 |
| 階段回顧 `devlog/P{n}.md` | 每階段一篇、精簡 | 困難與解法表｜我的想法｜驗證證據 | 由 session 摘要彙整，checkpoint 時問你 2–3 題 |

時間不足時優先保全：決策日誌、重要 commit、關鍵測試結果、代表性互動證據。

**本次規劃 session 的事實**（P0 寫成 `sessions/2026-11-05-01.md`，並回填決策日誌）：

| 輪次 | 發生的事 | 使用者的作為 |
|---|---|---|
| 1 | 使用者提供題目、職缺、履歷，要求一起規劃 | 設定目標與範圍 |
| 2 | AI 讀完題目、履歷、論文與環境，回報三個解析坑與環境缺口 | — |
| 3–4 | 兩輪共 8 題選項 | 皆採 AI 建議 |
| 5 | AI 第一次送審 | 退回，追加：Python 環境隔離、Docker 部署 |
| 6 | AI 第二次送審 | 退回，要求重新確認決策點；AI 列出 9 項未經確認的自行決定 |
| 7 | 第三輪選項 | 否決 2 項（uv → venv+pip；SQLite → PostgreSQL+pgvector）；貼題目原文要求對照，AI 加入需求追溯表 |
| 8 | AI 第三次送審 | 退回，要求互動紀錄機制，且互動要包含自己的想法 |
| 9 | AI 改問開放題 | 說明兩項否決的理由；提出五點調整（功能範圍、MVP-first、實驗驗證、Demo 重點、架構控制）；重新設計紀錄方式（五點）。AI 據此改寫計畫 |

候選代表案例（已出現）：(a) SQLite → PostgreSQL + pgvector；(b) uv → venv + pip；(c) 後端先行 → MVP-first；(d) 憑感覺調參 → 實驗驅動。

**PPT**（P7 產出 .pptx，約 12 頁），依你指定的重點：
系統架構 → 超過 context 怎麼辦 → summary 怎麼做 → 實際問答（三題）→ 跨文件整合 → 來源可追溯 → 無答案處理 → 檢索實驗數據 → AI Native 過程（任務拆解、用 Agent 開發、驗證生成的程式、修正錯誤、哪些決策由我主導）→ 代表案例 → 心得。

---

## 五、設計系統（UI）

- **Design tokens**：`frontend/src/styles/tokens.css` 以 CSS 變數定義色彩、字級、間距、圓角、陰影，含淺色／深色；Tailwind 對應 tokens。
- **元件基礎**：shadcn/ui（Radix）。
- **版面**：三欄。左：文件（上傳、清單、勾選問答範圍、入庫進度）；中：對話（Markdown 與表格渲染、引用標籤、三題快捷鈕、無答案提示樣式）；右：Inspector（檢索片段、token 用量條、流程步驟）。
- MVP 階段只做能用的最小介面；設計系統在 P5 套用。`docs/design/` 先畫線框再做。

---

## 六、階段與時程（MVP-first，7 天）

| 階段 | 時間 | 內容 | Checkpoint 產出 |
|---|---|---|---|
| P0 基礎建設 | D1 上午 | git、骨架、CLAUDE.md、樣板、`backend/.venv`、Node、compose 三服務骨架、Alembic、驗證容器連 Ollama、CI、私有 repo、`ollama pull bge-m3`、紀錄機制與第一份 session 紀錄 | `cp-0`：`make dev` 與 `make up` 都能起 health 頁，連得到 db 與 Ollama |
| P1 精簡規格 | D1 下午 | PRD 與驗收條件、架構、token 預算、API；spike：qwen3 計數與 thinking、Ollama embedding | `cp-1`：規格核准 |
| P2 MVP 端到端 | D2–D3 上午 | 上傳（PDF/TXT/MD）→ Parsing → Chunking → Embedding → pgvector → 向量檢索 → LLM 回答；含 token 守門、引用（檔名＋頁碼＋片段）、多文件、最小聊天介面與串流 | `cp-2`：瀏覽器上傳論文可問答並看到引用 |
| P3 摘要與防編造 | D3 下午–D4 上午 | 摘要樹、Router、對話記憶、證據壓縮、無答案四道機制 | `cp-3`：三題必答皆可回答；無答案題會拒答 |
| P4 檢索品質實驗 | D4 下午–D5 上午 | 題庫與評測腳本；實驗矩陣；依數據加入結構切塊、表格處理、Hybrid | `cp-4`：實驗報告＋參數 ADR |
| P5 使用體驗 | D5 下午–D6 上午 | 設計系統、三欄版面、Inspector、錯誤與空狀態；容器內驗證 SSE | `cp-5`：`make up` 後完整體驗 |
| P6 延伸與穩定 | D6 下午 | rerank 等延伸項（有時間才做）、乾淨環境重現測試、修 bug | `cp-6` |
| P7 交付 | D7 | README、代表案例、PPT、打包 zip、Demo 腳本與排練、錄影備援 | `cp-7`：可寄出 |

**P4 實驗設計**

- 測試資料：LightRAG 論文（主）；一份短 TXT/MD；跨文件用的第二份論文（AI 建議用 GraphRAG 論文 arXiv 2404.16130，P4 開始前請你確認）。
- 題庫約 15–20 題，每題標註預期來源與關鍵事實：必答 3 題、細節事實題、表格數字題、跨文件題、無答案題。
- 實驗變因：chunk size（如 256／400／600）× Top-K（3／5／8）× 檢索法（Vector／Hybrid）；另比較結構切塊與表格處理的有無。
- 指標：Recall@K、來源命中率、回答正確性（關鍵事實涵蓋，本地 LLM 評審輔助）、無答案題正確拒答率、10K 合規率、延遲。
- 檢索指標不需呼叫 LLM，可全矩陣跑；回答正確性只跑表現最好的幾組。

**風險控管**

- D3 上午前 MVP 必須端到端可展示；D4 上午前三題必答可回答。
- Demo 依賴這台伺服器在線，P7 錄備援影片。

**需要你親自做的事**

- `sudo apt install python3.12-venv`（或同意免 sudo 的替代做法）。
- 設定 git 姓名與 email；建 GitHub 私有 repo 並提供推送方式。
- 若主機 Ollama 只聽 127.0.0.1，調整監聽位址。
- 每個 checkpoint 回答 2–3 題「我的想法」；在五種時刻截圖。

---

## 七、驗證方式

- 環境隔離：`backend/.venv/bin/python -c "import sys; print(sys.prefix)"` 指向 `backend/.venv`。
- `make check`：ruff、mypy、pytest、eslint、tsc、vitest 全綠。
- 部署：`make up` 後三個容器皆 healthy，migration 已套用，後端容器能呼叫 Ollama。
- `make eval`：產出 `eval/reports/`；含各實驗組的 Recall@K、來源命中率、正確性、拒答率；10K 合規率 100%。
- 手動端到端（Docker 部署版）：上傳 `test_data/2410.05779v3.pdf` 與第二份文件 → 問三題必答 → 問一題跨文件 → 問一題無答案 → 檢查引用的檔名、頁碼、片段與 Inspector 的 token 用量 ≤ 10,000。
- 查帳本：`GET /api/llm-calls` 最大 `prompt+completion` ≤ 10,000。
- 乾淨環境：zip 解到新資料夾，照 README 只用 `docker compose up --build` 啟動成功。
- 紀錄：決策日誌每列都有「我的原始回覆」與對應 commit；`cases.md` 有 3–5 個完整案例。

---

## 八、核准後的第一步（P0）

1. `git init`、`.gitignore`、題目 PDF 移到 `docs/assignment/`。
2. 資料夾骨架、`CLAUDE.md`（含互動規則）、`AGENTS.md`、ADR／規格／日誌樣板；互動規則寫入專案記憶。
3. 建 `backend/.venv` 與釘版 requirements；裝 nvm＋Node LTS；`ollama pull bge-m3`。
4. 後端與前端最小骨架、Makefile、pre-commit、CI。
5. `docker-compose.yml`＋兩個 Dockerfile＋Alembic 初始 migration；`make up` 起得來並連得到主機 Ollama。
6. 紀錄機制：`decision-log.md`（回填決策總表 18 項與附錄原話）、`sessions/2026-11-05-01.md`、`scripts/export_transcript.py`、`checkpoint` skill；以 update-config skill 設定自動匯出的 hook。
7. `docs/devlog/P0.md`，問你「我的想法」，打 `cp-0`。

互動規則（寫入 `CLAUDE.md`）：提選項前先問使用者的想法或附開放題；每個選項寫清楚取捨；使用者的補充與反對原文記入決策日誌；只在五種時刻提醒截圖。

---

## 附錄：使用者原話（2026-11-05，P0 原文轉入決策日誌）

**為何選標準 venv + pip 而非 uv**

> 主要是考量專案只有一週的開發時間，且最終需要提供程式碼供面試官在本地端執行。相較於引入 uv，我希望先降低額外的工具依賴，使用 Python 常見的虛擬環境搭配 requirements.txt，讓環境建立與專案重現流程更直觀

**為何選 PostgreSQL + pgvector 而非 SQLite**

> 這次選擇 PostgreSQL + pgvector，主要是考量「讓 AI 與文件對話」本質上是一個 RAG 系統，需要管理文件、文字切塊（Chunks）、Embedding 向量及相關 Metadata，並支援語意相似度檢索。相較於 SQLite 搭配額外的向量搜尋方案，PostgreSQL + pgvector 可以在同一個資料庫中整合關聯式資料管理與向量檢索，降低資料分散管理的複雜度，也方便後續擴充多文件管理、使用者隔離及混合檢索（Hybrid Search）。此外，我希望這次專案不只是完成基本 Demo，也能呈現具備擴充潛力的系統架構。不過，這不代表 SQLite 無法實現 RAG，而是考量目前的技術目標與未來擴充需求後，選擇 PostgreSQL + pgvector 作為較合適的方案。

**對規劃的五點調整**

> 我希望在原有規劃上做以下調整：1. 功能與檢索：優先完成 PDF、TXT、Markdown 文件上傳，支援多文件問答、來源引用（文件名稱、頁碼、引用片段），並設計「找不到答案時不應自行編造」的機制。若時間允許，再加入 Hybrid Search（Vector + Full-text Search）及檢索結果重排序。2. 開發順序：採用 MVP-first 策略，優先完成文件上傳 → Parsing → Chunking → Embedding → PostgreSQL/pgvector → Retrieval → LLM Answer 的完整端到端流程，確保基本功能可展示，再逐步提升檢索品質與使用體驗。3. 檢索品質驗證：希望建立一組小型測試資料與標準問題，比較不同 Chunk Size、Top-K、Vector Search 與 Hybrid Search 的結果，使用 Recall@K、來源命中率與回答正確性等指標，讓架構設計與參數選擇有實驗依據，而不是只憑感覺調整。4. Demo 與報告：希望呈現完整系統架構、實際文件問答、跨文件資訊整合、來源可追溯性及無答案問題的處理。另外，特別強調 AI Native 開發過程，包含如何拆解任務、使用 AI Agent 開發、驗證生成程式碼、修正錯誤，以及哪些技術決策由我主導。5. 架構控制：目前先維持簡潔的服務設計，不為了展示技術而加入 Redis、Kubernetes 或複雜的微服務。PostgreSQL + pgvector 可透過 Docker Compose 啟動，但應保留容易重現的本地 Demo 流程。整體目標是完成一個可運作、可驗證、可解釋設計決策的 RAG 系統，而非單純整合 LLM API 的聊天介面。若時間不足，優先保證端到端流程、來源引用、基本檢索測試和完整 Demo，其他進階功能列為延伸項目。

**對互動紀錄的設計**

> 我希望採用「結構化決策日誌＋關鍵互動紀錄＋自動化原始紀錄」的方式，兼顧可追溯性與開發效率。1. 決策日誌（必做）：記錄重要技術決策，包括問題背景、AI 建議、我的原始回覆、最終選擇、選擇理由、驗證結果與對應 Commit。除了成功決策，也要保留 AI 建議被否決或修改的案例。2. Session Summary（必做，但精簡）：每次開發 Session 結束時，自動整理本次目標、AI 完成的工作、我介入修改的部分、遇到的問題及下一步。不需要逐輪人工整理所有對話。3. 原始逐字稿（建議保留）：若 AI Coding 工具支援 /export 或其他匯出功能，就在重要 Checkpoint 匯出完整對話，作為原始證據保存，不需要人工逐字整理。4. 關鍵截圖（選擇性）：只針對重要決策、AI 發生錯誤、人工介入修正、測試前後比較及最終 Demo 截圖，不需要每個步驟都截圖。5. AI 協作品質分析：希望最後能從紀錄中挑選 3～5 個代表性案例，呈現「AI 提案 → 人工判斷 → 實作 → 測試驗證 → 改善結果」的完整過程，作為 PPT 的 AI Collaboration 與 Lessons Learned 內容。請盡量將上述紀錄流程自動化，避免為了記錄而中斷主要開發工作。若時間有限，優先確保決策日誌、重要 Commit、關鍵測試結果與代表性 AI 互動證據完整，其他紀錄可以簡化。

**更早的兩次退回**

> 還要建立 python env 作環境隔離 部屬採用docker

> 再跟我確認一次決策點

> 另外因為我向他們報告使用AI的方式 所以現在這個plan mode 要幫我記錄良好的使用方式 並且在你提供選項時 不只聽從你的建議 我也提出想法 在其他給你更詳細的建議 我希望要有這樣的互動紀錄 甚至截圖
