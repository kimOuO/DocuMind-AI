# DocuMind-AI

讓 AI 跟文件對話：上傳文件，用聊天介面提問，LLM 依文件內容回答並附上來源。

簡報：[`docs/06-report/DocuMind-AI.pdf`](docs/06-report/DocuMind-AI.pdf)（可編輯版 [`DocuMind-AI.pptx`](docs/06-report/DocuMind-AI.pptx)）

本機執行的文件問答平台：帳號與文件管理（PDF、TXT、Markdown）、入庫（表格整張保留並逐列改寫）、對話式問答（串流回答，來源附檔名、頁碼、片段；接著追問；文件沒有的就明說）、可選的全文摘要、每次模型呼叫的 token 帳本。

## 題目限制

| 限制 | 做法 |
|---|---|
| LLM 只做 text-to-text，不得用 GPT／Gemini API 解析文件 | 文件以本地程式庫解析；模型是本機的 Ollama，文字不離開機器 |
| LLM context 上限 10K tokens | 每次呼叫的 prompt 加輸出 ≤ 10,000：送出前以內附的 tokenizer 在本地計數並分配預算；每個請求都要求 Ollama 拒絕超量的輸入、不捨棄內容，所以不會被悄悄截斷 |
| 找不到答案不編造 | 回答只依據檢索到的來源並逐句標出處；文件沒提到就明說 |

## 快速啟動

### 1. 準備環境

| 項目 | 版本 | 說明 |
|---|---|---|
| Docker Engine | ≥ 20.10（實測 29.5） | 含 Compose 外掛 ≥ 2.2（實測 5.1） |
| [Ollama](https://ollama.com/download) | ≥ 0.24.0（實測 0.24.0） | 要讓容器連得到：設定環境變數 `OLLAMA_HOST=0.0.0.0` 後重啟 Ollama |
| 模型 `qwen3:32b` | 約 20 GB | 生成模型，必要 |
| 模型 `bge-m3` | 約 1.2 GB | 嵌入模型，必要 |
| 模型 `qwen3.6:27b-q4_K_M` | 約 17 GB | 選用：前端可切換的第二個生成模型 |

```bash
ollama pull qwen3:32b
ollama pull bge-m3
ollama pull qwen3.6:27b-q4_K_M   # 選用
```

建議資源：顯示記憶體 ≥ 24 GB（實測 NVIDIA A40 46 GB）、記憶體 ≥ 16 GB、磁碟可用 ≥ 10 GB（模型另需約 21 GB）。沒有 GPU 也能執行，但一題可能要數分鐘。

計算 token 用的 tokenizer 已內附在專案中，建置時不需要另外下載。

### 2. 啟動

```bash
git clone git@github.com:kimOuO/DocuMind-AI.git
cd DocuMind-AI
make up
```

直接執行 `make up` 就會檢查環境並部署：

- 先檢查第 1 步的項目。缺什麼會一次列出並說明怎麼補，有缺就不啟動。
- 通過後建置並啟動資料庫、後端、前端三個容器。主機不用另外安裝 Python 或 Node。
- 完成後開啟 `http://127.0.0.1:3000`，註冊帳號即可使用。

### 3. 調整設定（需要時）

設定都在專案根目錄的 `.env`。第一次 `make up` 會自動從 `.env.sample` 複製一份；也可以先自己複製再改：

```bash
cp .env.sample .env    # 已經有 .env 就直接編輯
make up                # 改完重新執行才會生效
```

常會用到的設定：

| 設定 | 預設 | 什麼時候要改 |
|---|---|---|
| `WEB_PORT` | `3000` | 3000 埠已被占用 |
| `WEB_BIND` | `127.0.0.1` | 要讓區網其他電腦連進來時改成 `0.0.0.0` |
| `ALLOWED_ORIGINS` | `http://127.0.0.1:3000,http://localhost:3000` | 用其他網址開網頁時把它加進去，例如 `http://192.168.1.10:3000`；沒加的話登入與提問會被擋 |
| `DB_PORT` | `5433` | 5433 埠已被占用 |
| `COMPOSE_OLLAMA_HOST` | `host.docker.internal`（本機） | Ollama 裝在另一台機器時，填那台機器的 IP |
| `HTTP_OLLAMA_PORT` | `11434` | Ollama 不在預設的埠 |
| `LLM_MODEL`／`EMBED_MODEL` | `qwen3:32b`／`bge-m3` | 換模型；換生成模型要連同 tokenizer 設定一起改，見 `.env.sample` 的說明 |
| `ALT_LLM_MODEL` | `qwen3.6:27b-q4_K_M` | 不提供第二個模型時留空 |
| `ANSWER_TEMPERATURE` | `0` | 回答溫度的預設值；前端也能逐題調整 |
| `LLM_THINKING` | `false` | 思考模式的預設值；前端也能逐題勾選 |
| `CHECK_NOTES` | `false` | 改成 `true` 會在回答後附上數字核對的註記（除錯用） |

**用 IP 連線的兩種情況**

- 從別台電腦開這個網站：先查這台機器的 IP（`hostname -I`），在 `.env` 設 `WEB_BIND=0.0.0.0`，並把 `http://<這台機器的 IP>:3000` 加進 `ALLOWED_ORIGINS`（逗號分隔），重新 `make up` 後用該網址開啟。
- Ollama 在另一台機器：在 `.env` 設 `COMPOSE_OLLAMA_HOST=<Ollama 那台的 IP>`，那台的 Ollama 同樣要監聽 `0.0.0.0`。

其餘設定與說明見 `.env.sample`。

### 4. 檢查（選用）

`make preflight` 不需要任何準備。其餘指令會用到開發環境，第一次請先執行：

```bash
make setup    # 只需要 Python 3.12；工具都裝在專案的 .venv 內，不動到主機
```

| 指令 | 檢查什麼 |
|---|---|
| `make preflight` | 只檢查環境，不啟動 |
| `make smoke-api` | 部署後對運行中的系統實際操作一遍：註冊、上傳、提問、追問、無答案題、10K 帳本 |
| `make check` | 程式本身：lint、型別檢查、自動測試 |
| `make smoke` | 嵌入模型、向量庫、生成模型三者接不接得起來 |
| `make deploy` | 一次做完：`make check` → `make up` → `make smoke-api`，任何一步失敗就停 |

### 5. 使用

上傳 PDF、TXT 或 Markdown（文字檔須為 UTF-8）。上傳後在背景解析並建立索引，清單顯示進度；完成後顯示頁數與片段數，失敗時顯示原因並可重試。文件就緒後在對話區提問：

- **來源**：不勾選文件時搜尋所有可用的文件；回答下方列出來源，點引用可看原文段落與 PDF 該頁。
- **追問**：同一對話裡接著問時，模型先判斷這句是新問題還是延續前文，延續才把「他」「前一題的」改寫成實際對象再檢索。
- **摘要**：要讀完整篇的摘要，按輸入框旁的「建立摘要」。系統先為範圍內的文件建摘要樹（16 頁論文約 3 分鐘，進度顯示在對話裡），再把摘要寫進對話。上傳時預設不建摘要樹。
- **選項**：輸入框下方可逐題調整溫度、切換模型、勾選思考模式；預設是溫度 0、`qwen3:32b`、思考關。
- **用量**：每則回答末尾標示它用的模型、溫度，以及每一次模型呼叫的 token。

API 文件在 `http://127.0.0.1:3000/api/v1/docs`。

## 其他指令

```bash
make down    # 停止 Docker 部署（資料保留）
make dev     # 開發模式：資料庫容器 + 後端熱重載（:8000）+ 前端 Vite（:5173）
make help    # 所有指令
```

## 架構

```
瀏覽器 ──► 前端（Nginx + React）──/api──► 後端（FastAPI）
                                            ├──► 資料庫（PostgreSQL + pgvector）
                                            └──► Ollama（主機：qwen3:32b、bge-m3）
```

部署由 `docker-compose.yml` 定義：資料庫、後端、前端三個容器，加上主機的 Ollama。

### 程式碼架構

後端依功能模組組織，每個模組內分三層：Router 收請求、Service 管業務規則與權限（每個方法都接收目前登入的使用者）、Repository 讀寫資料庫（每個查詢都帶擁有者條件）。模型只經過 `llm/` 的 Gateway：送出前以本地 tokenizer 計數、超過 10,000 就拒絕，每次呼叫寫入 `llm_calls` 帳本。

| 後端模組 `app/backend/app/` | 負責 |
|---|---|
| `auth` | 註冊、登入、session cookie（Argon2id） |
| `documents` | 上傳、清單、刪除、重試；檔案存放 |
| `ingestion` | 解析（pypdf）、標題與章節、表格偵測與逐列改寫、切塊、嵌入、背景工作排程 |
| `retrieval` | 向量檢索（pgvector）、相似度門檻、表格後文補充 |
| `summarization` | 摘要樹（map-reduce）、摘要數字核對與修復 |
| `conversations` | 對話與訊息的儲存與讀取 |
| `chat` | 問答流程：追問判斷與改寫、路由、證據裝填與比較事實、prompt、串流回答、答後核對 |
| `llm` | Ollama 請求組裝、預算守門、帳本、tokenizer、嵌入 |
| `monitoring` | `/health`、帳本查詢 |
| `core` | 設定（唯一讀取環境變數的地方）、資料庫連線、錯誤格式、SSE |

資料表（`models.py`、`migrations/`）：`users`、`sessions`、`documents`、`ingestion_jobs`、`chunks`、`chunk_vectors`、`summaries`、`conversations`、`messages`、`llm_calls`。

前端 `app/frontend/src/features/`：`auth`、`documents`（上傳與清單）、`chat`（對話、來源檢視、溫度、模型、思考、建立摘要）、`home`；`lib/api.ts` 是唯一呼叫後端的地方。

細節與每個決定的理由見 `docs/02-specs/02-architecture.md` 與 `docs/03-decisions/`。

## 資料夾導覽

```
DocuMind-AI/
├── app/                        要執行的程式
│   ├── backend/                FastAPI 後端（程式、資料庫 migration、測試）
│   └── frontend/               React 前端
├── docs/                       規格與架構決策紀錄
│   ├── 02-specs/               規格：01 需求與驗收條件、02 架構、03 介面、04 使用情境
│   ├── 03-decisions/           架構決策紀錄：選了什麼、為什麼
│   └── 06-report/              簡報（PDF 與 PPTX）
├── evaluation/                 評測程式（題庫、標準答案與逐題紀錄保留在開發機，未公開）
├── sample-documents/           測試用文件（LightRAG 論文）
├── scripts/                    工具：啟動前檢查、API 測試、最小流程驗證、打包、匯出逐字稿
├── CLAUDE.md                   給 AI coding agent（Claude Code）的專案規則
├── .claude/                    Claude Code 的設定與兩個流程（checkpoint、verify）
└── Makefile / docker-compose.yml / .env.sample
```

## 目前結果

三個必答題在示範部署上各問 10 次（十個對話，每個對話依序問三題；溫度 0、不建摘要樹）。判定由人逐句對原文，有錯誤資訊才算不通過。

| 題目 | 10 次結果 | 回答的狀況 |
|---|---|---|
| Q1 summary this document. | 10 / 10 無錯誤資訊 | 走一般檢索：研究問題與方法都有寫，缺實驗結果與數字。按「建立摘要」用摘要樹回答時，問題、方法、實驗結果都有，數字附頁碼 |
| Q2 compare lightRAG with GraphRAG | 10 / 10 | 16 項比較中 LightRAG 13 項較高，Mix 資料集的 3 項例外與差距都正確；十次逐字相同 |
| Q3 Performance of ablated versions of LightRAG | 10 / 10 | 各版本的數字、較高與較低的項數、例外都正確；十次逐字相同。沒有解釋三個版本各拿掉什麼 |

三題每一次模型呼叫都在 10,000 tokens 內（單次最大 6,290）。

## 兩個說明題

**文件 token 超過 context 怎麼辦？**

一份論文約 20,000 到 40,000 tokens，從不整份送進模型。分四層：

1. **切塊索引**：入庫時依 400 tokens 切塊（三種大小的實驗中找得最全；切點不落在字或數字中間）。表格整張保留，逐列改寫成每個數字都帶方法、資料集、指標的句子；多組比較的表格每一組各建一個向量，任何一組符合問題就取回整張表。
2. **只取相關片段**：提問時取相似度前 5 段，命中表格時補上表格後面的討論段；證據有預算上限，裝不下的整塊不送，不截斷。相似度都偏低時仍把最相近的三段交給模型判斷，由它明說文件沒提到。
3. **呼叫前守門**：以模型自己的 tokenizer 在本地計數，prompt 加上保留的輸出必須 ≤ 10,000，超過就拒絕呼叫；對 Ollama 的請求固定上限並關閉自動截斷，超量時 Ollama 回錯誤而不是默默丟內容。
4. **呼叫後記帳**：每次呼叫實際用了多少 tokens 都寫進帳本，介面也顯示。

守的是每一次呼叫；整份文件靠分段讀完。

**Summary 怎麼處理？**

兩種做法都有：

- **摘要樹**（上傳時勾選，或在對話按「建立摘要」）：程式依章節把文件切成單位，每個單位一次呼叫寫章節摘要並附頁碼，再一次呼叫合成全文摘要；章節摘要合起來太長就先分組濃縮。每次呼叫各自守 10K。摘要裡的數字會對回原文與表格，矛盾時憑表格重寫一次。之後問摘要只要一次呼叫，來源是各章節的摘要與頁碼範圍。讀完整篇，但 16 頁論文要先花約 3 分鐘、十一次呼叫。
- **走一般檢索**（預設）：把「summary this document.」當一般問題，取最相近的 5 段回答。不用等，但只看到約一成多的論文，問題與方法寫得出來，常缺實驗結果。

## 開發方式

以 AI-native 方式開發（Claude Code），流程為規格先行、測試先行、每階段 checkpoint。協作規則寫在 `CLAUDE.md`：依規格與計畫推進並在每個階段先說明取得許可；改了前後端模組先完整檢查、再部署、再跑 API 測試；跑完測試劇本先記錄與分析，再討論修改。階段標記為 `cp-0` 到 `cp-6`；架構層級的決策與理由見 `docs/03-decisions/`。
