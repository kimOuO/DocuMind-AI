# DocuMind-AI

讓 AI 跟文件對話：上傳文件，用聊天介面提問，LLM 依文件內容回答並附上來源。
Chat with your documents: upload a file, ask questions, get answers grounded in the document with citations.

> 狀態 / Status（2026-11-08）：帳號、文件管理（PDF／TXT／Markdown）、入庫（表格整塊保留並逐格改寫、五種表格排版、多區塊表格一區塊一向量）、入庫時建立摘要樹（章節摘要 → 全文摘要，數字核對；可選的證據導向修復）、對話式問答（串流、來源的檔名／頁碼／片段、追問改寫、文件沒有的就明說、問系統本身也會回答、回答後的數字與結論核對；可選的比較事實注入）皆已完成；另有實驗性的兩次呼叫 `navigate` 模式（預設關閉）。已知限制：模型偶爾把正確數字寫成方向相反的句子；核對器對部分句型有誤報；表格支援範圍見 `evaluation/table-generalization/`。
> Accounts, document management (PDF/TXT/Markdown), ingestion (tables kept whole and rewritten cell by cell in five layouts, one vector per block of a multi-block table), a summary tree built at ingestion (section summaries → document summary, figures checked; optional evidence-guided repair), and conversational chat (streaming, sources with file name/page/snippet, follow-up rewriting, saying plainly when the documents do not cover a question, answering questions about the assistant itself, post-answer checks of figures and conclusions; optional injection of program-computed comparison facts) are done; an experimental two-call `navigate` mode exists (off by default). Known limits: the model occasionally words a correct figure in the wrong direction; the checker has false positives on some sentence shapes; the supported table layouts are listed in `evaluation/table-generalization/`.

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

註冊並登入後，可以上傳 PDF、TXT、Markdown 文件（文字檔須為 UTF-8）。上傳後會在背景解析並建立索引，清單上顯示進度；完成後顯示頁數與片段數，失敗時顯示原因並可重試。文件就緒後可在「提問」區塊發問：不勾選文件時搜尋所有可用的文件，回答下方列出來源，並顯示這次呼叫實際使用的 token 數。首頁同時顯示資料庫與 LLM 服務的狀態。
After registering and logging in you can upload PDF, TXT and Markdown documents (text files must be UTF-8). Each upload is parsed and indexed in the background while the list shows its progress; when it is done the list shows the number of pages and chunks, and a failure shows its reason and can be retried. Once a document is ready you can ask questions in the chat panel: with no document ticked, all available documents are searched; each answer lists its sources and the tokens the call actually used. The home page also shows whether the database and the LLM server are healthy.

請從 `http://127.0.0.1:3000` 或 `http://localhost:3000` 開啟。用其他位址（例如區網 IP）開啟時，把該位址加進 `.env` 的 `ALLOWED_ORIGINS`，否則會被來源檢查擋下。
Open the site at one of those two addresses. If you use another address, add it to `ALLOWED_ORIGINS` in `.env`; otherwise state-changing requests are refused by the origin check.

- Ollama 必須監聽容器連得到的位址（`OLLAMA_HOST=0.0.0.0`）。若沒有預裝 Ollama，可改用內建的容器：`docker compose --profile ollama up --build`，並在 `.env` 設定 `COMPOSE_OLLAMA_HOST=ollama`（此模式尚未實測）。
- 設定值見 `.env.sample`。`make setup`、`make up` 會在 `.env` 不存在時由它複製一份。
- 兩個可選的回答改善，預設關閉，實驗數據在 `evaluation/facts-ab/`：`ANSWER_FACTS=inject` 把程式從表格算出的比較事實（哪邊高、差幾個百分點、哪些例外）放進 prompt，讓比較題的結論與例外對得上表格；`SUMMARY_REPAIR=true` 在入庫時對數字歸錯對象或不存在的摘要句，以表格證據重寫一次，仍錯就刪句。`ANSWER_TEMPERATURE` 是回答取樣溫度的預設值（空白＝模型預設）；前端輸入框旁的滑桿可逐題調整 0 到 1，每則回答標示它用的溫度（AC-60）。
- Two optional answering improvements, off by default, measured in `evaluation/facts-ab/`: `ANSWER_FACTS=inject` puts the program's comparison facts from the tables (which side is higher, by how many points, every exception) into the prompt so that conclusions match the tables; `SUMMARY_REPAIR=true` rewrites, once and with the table's figures as evidence, a summary sentence whose figure is misattributed or absent from the pages, removing it if still wrong. `ANSWER_TEMPERATURE` is the default answer sampling temperature (empty = the model's default); a slider beside the composer sets it per question between 0 and 1, and every answer shows the temperature it used (AC-60).
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

**文件 token 超過 context 怎麼辦？ / What if a document exceeds the context window?**

一份論文約 20,000 到 40,000 tokens，從不整份送進模型。做法分四層，每層都有數據（`evaluation/`、`docs/03-decisions/0010`）：

1. **切塊索引**：入庫時依 400 tokens、重疊 80 切塊（三種大小的實驗中 Recall 最高；切點不落在字或數字中間），表格整塊保留並逐格改寫成「列 — 群組: 欄 值」（支援兩層欄頭成對子欄、多字群組名、跨欄總標題、數值列標籤加分段列、成對比較表五種排版，兩篇論文六張表 570 格與 LaTeX 原始檔逐格全符）；每塊一個 bge-m3 向量存進 pgvector，多區塊的表格另存每個區塊的向量。
2. **只取相關片段**：提問時取相似度前 5 的切塊（約 2,100 tokens），命中表格時補入表格後面的討論段；證據預算 5,500 tokens，裝不下的不送也不截斷。相似度都低於 0.50 時仍把最相近的三段交給模型自行判斷，並附上文件清單與摘要開頭，讓它能回答「這篇在講什麼」或明說文件沒提到。
3. **呼叫前守門**：以內附的 Qwen3 tokenizer 在本地計數，prompt 加上輸出保留 2,500 必須 ≤ 10,000，超過就拒絕呼叫；對 Ollama 的請求固定 `num_ctx=10000`、`truncate=false`、`shift=false`，模型端不會悄悄截斷。
4. **呼叫後記帳**：Ollama 回報的 `prompt_eval_count + eval_count` 寫進 `llm_calls` 帳本，介面顯示用量條；實驗工具對每次呼叫斷言 ≤ 10,000，到目前 100 多次真實模型紀錄全部合規（單次最高約 9,900）。

A paper is 20,000–40,000 tokens and is never sent whole. Four layers, each measured in `evaluation/`: (1) chunk at ingestion (400 tokens, 80 overlap — the best Recall of three sizes; boundaries never split a word or a number; tables kept whole and rewritten cell by cell as "row — group: column value" in five layouts, 570 cells of six tables across two papers matching the LaTeX sources cell by cell; one bge-m3 vector per chunk in pgvector, plus one per block of a multi-block table); (2) retrieve only the top-5 similar chunks (~2,100 tokens) plus the discussion that follows a retrieved table, within a 5,500-token evidence budget — what does not fit is left out, never cut; when nothing reaches similarity 0.50 the three closest passages still go to the model, with the list of documents and their summary openings, so it can answer "what is this paper about" or say plainly that the documents do not cover the question; (3) guard before the call: the bundled Qwen3 tokenizer counts locally, prompt + a 2,500-token output reserve must be ≤ 10,000 or the call is refused, and every Ollama request carries `num_ctx=10000`, `truncate=false`, `shift=false`; (4) account after the call: Ollama's `prompt_eval_count + eval_count` goes into the `llm_calls` ledger, shown in the UI; the experiment harness asserts ≤ 10,000 on every call — all 100+ recorded runs comply (peak ≈ 9,900).

**Summary 怎麼處理？ / How is "summary this document" handled?**

全文摘要在入庫時建好，不在提問時現做：

1. **章節切分**：辨識標題的編號與頁碼，依章節切成摘要單位（參考文獻排除）；超過 6,000 tokens 的章節再往下切。
2. **章節摘要**：每個單位一次呼叫，最多 250 字，保留關鍵數字並附頁碼；撞到輸出上限的摘要重試兩次。
3. **全文摘要**：由各章節摘要合併成最多 400 字的全文摘要；合併仍超量就再摺一層。
4. **驗證狀態**：每份摘要的數字對照原文核對，存 VERIFIED／CONTRADICTED／UNCERTAIN／NOT_CHECKED。預設不改寫摘要；開 `SUMMARY_REPAIR=true` 時，數字歸錯對象、被表格反證的全稱句、或頁面上不存在的數字，會以表格的真實數字當證據請模型重寫一次，再核對，仍錯的句子刪除（實測四次觸發修對三條真錯，一條誤報在核對器修正後消失；見 `evaluation/facts-ab/`）。
5. **回答**：「summary this document」走摘要路徑，以全文摘要加章節摘要回答並引用摘要節點（章節標題與頁碼範圍）；索引完成即可問一般問題，摘要還沒好時摘要類問題會明說尚未可用。

已知限制：摘要本身是模型寫的，門檻式的全稱句（「所有指標都在 60% 以上」）核對抓不到；回答端的核對器對部分句型仍有誤報（例外句的比較對象範圍、「100 個 token」對上表格的 100），見 `evaluation/facts-ab/README.md`。

The whole-document summary is built at ingestion, not at question time: (1) sections are cut by heading numbers and pages (references excluded; sections over 6,000 tokens split further); (2) one call per section, ≤ 250 words, key figures kept with page numbers, retried twice when the output limit is hit; (3) section summaries merge into a ≤ 400-word document summary, folding again if still too long; (4) every summary's figures are checked against the source text and stored with a status — VERIFIED / CONTRADICTED / UNCERTAIN / NOT_CHECKED; by default nothing is rewritten, and with `SUMMARY_REPAIR=true` a misattributed figure, a universal claim the table contradicts, or a figure absent from the pages is sent back once with the table's own figures as evidence, re-checked, and removed if still wrong (three real errors fixed in four triggers in our runs; see `evaluation/facts-ab/`); (5) "summary this document" answers from the document and section summaries and cites the summary nodes (section title and page range); ordinary questions work as soon as indexing finishes, and a summary question says so while the summary is still being built. Known limits: a model-written summary may make a threshold claim ("above 60% in all metrics") that the checks cannot catch; the answer-side checker still has false positives on some sentence shapes — see `evaluation/facts-ab/README.md`.

## 開發方式 / How this was built

以 AI-native 方式開發（Claude Code），流程為 SDD → TDD → Checkpoint。
每個技術決策，包含 AI 建議被否決或修改的案例，都有紀錄；架構層級的決策與理由見 `docs/03-decisions/`。
