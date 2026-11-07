# 03 介面：API、受管理的物件、資料表、設定

狀態：已確認（2026-11-05，決策日誌 D46）。P1 完成後凍結；之後只在實作或測試發現實際問題時修改，並記入決策日誌。
欄位名稱與程式碼一致，用英文。

## 1. HTTP API

### 1.1 約定

- RESTful，共同前綴 `/api/v1`（決策日誌 D42）。查詢用 GET、建立與動作用 POST、修改用 PATCH、刪除用 DELETE。GET 不改變資料。
- 除了註冊、登入、健康檢查與 API 文件頁，全部需要登入。未登入回 `401`。
- 資源識別一律用 UUID。
- 存取不存在或不屬於自己的資源，一律回 `404`（不回 `403`，避免洩漏資源是否存在）。
- 會改變資料的請求（POST、PATCH、DELETE）要通過來源檢查：看 `Origin`，沒有 `Origin` 時看 `Referer`；兩者都沒有或不在允許清單內回 `403`（見 `02-architecture.md` 第 2.4 節）。
- 錯誤格式：`{"detail": "給人看的說明", "code": "DOCUMENT_NOT_READY"}`。`code` 供前端判斷。
- 狀態碼：`400` 請求格式錯誤、`401` 未登入、`403` 來源檢查不通過、`404` 不存在或不屬於你、`409` 目前狀態不允許這個操作、`413` 檔案過大、`415` 格式不支援、`422` 欄位驗證失敗。
- 串流回應使用 Server-Sent Events。入庫進度是 GET，前端用 `EventSource`；提問是 POST，前端用 `fetch` 讀取串流。
- API 文件由 FastAPI 自動產生於 `/api/v1/docs`（不需登入），經 Nginx 也能開啟。

### 1.2 端點一覽

| 方法 | 路徑 | 用途 | 成功 | 階段 |
|---|---|---|---|---|
| POST | `/auth/register` | 註冊 | 201 | P2-A |
| POST | `/auth/login` | 登入，設定 Session Cookie | 200 | P2-A |
| POST | `/auth/logout` | 登出，刪除 Session | 204 | P2-A |
| GET | `/users/me` | 目前使用者 | 200 | P2-A |
| PATCH | `/users/me` | 修改顯示名稱與偏好 | 200 | P5 |
| GET | `/health` | 健康檢查（不需登入） | 200 | P0，改前綴 |
| POST | `/documents` | 上傳 | 202 | P2-B |
| GET | `/documents` | 自己的文件清單 | 200 | P2-B |
| GET | `/documents/{id}` | 單一文件與它最近的處理工作 | 200 | P2-B |
| DELETE | `/documents/{id}` | 刪除 | 204 | P2-B |
| POST | `/documents/{id}/retry` | 重試失敗的處理 | 202 | P2-C |
| GET | `/documents/{id}/events` | 處理進度（SSE） | 200 | P2-C |
| POST | `/conversations` | 建立對話 | 201 | P2-D |
| GET | `/conversations` | 自己的對話清單 | 200 | P2-D |
| GET | `/conversations/{id}` | 對話與其訊息 | 200 | P2-D |
| DELETE | `/conversations/{id}` | 刪除對話 | 204 | P2-D |
| POST | `/conversations/{id}/messages` | 提問；回應為 SSE 串流 | 200 | P2-D |
| GET | `/llm-calls` | 自己的 LLM 呼叫帳本 | 200 | P2-D |

現況：P0 實作的是 `GET /api/health`。P2-A 改為 `GET /api/v1/health`，並同步修改測試、前端與容器的健康檢查。

### 1.3 帳號

**`POST /auth/register`**：`{"username": "…", "password": "…"}`。使用者名稱 3–32 字元，密碼至少 8 字元。
回應 `201`：使用者物件（不含密碼）。使用者名稱已存在回 `409`。註冊不自動登入。

**`POST /auth/login`**：`{"username": "…", "password": "…"}`。
成功回 `200` 與使用者物件，並以 `Set-Cookie` 設定新的 Session。帳號或密碼錯誤一律回 `401`，訊息不區分是哪一個錯。

**`POST /auth/logout`**：刪除目前的 Session 並清除 Cookie，回 `204`。

**`GET /users/me`**

```json
{
  "id": "uuid",
  "username": "kim",
  "display_name": "Kim",
  "answer_language": "auto",
  "answer_detail": "normal",
  "created_at": "…",
  "last_login_at": "…"
}
```

**`PATCH /users/me`**（P5）：可修改 `display_name`、`answer_language`（`auto`／`zh-TW`／`en`）、`answer_detail`（`brief`／`normal`／`detailed`）。不能修改使用者名稱與密碼。

### 1.4 文件

**`POST /documents`**：`multipart/form-data`，欄位 `file`。接受 `.pdf`、`.txt`、`.md`，大小上限 50 MB。

回應 `202`：文件物件，`status` 為 `uploaded`。同時排入一筆 `index` 處理工作。
錯誤：`415` 不支援的格式；`413` 檔案過大；`422` 檔案是空的。
同一使用者上傳內容相同的檔案，回 `200` 與既有的文件，不重複建立。

**文件物件**（`GET /documents` 回傳陣列，`GET /documents/{id}` 回傳單一物件）

```json
{
  "id": "uuid",
  "filename": "2410.05779v3.pdf",
  "media_type": "pdf",
  "file_size": 1123301,
  "status": "uploaded | processing | ready | failed",
  "summary_status": "none | processing | ready | failed",
  "error": null,
  "page_count": 16,
  "chunk_count": 48,
  "created_at": "…",
  "updated_at": "…",
  "jobs": [
    {
      "id": "uuid",
      "kind": "index | summary",
      "status": "queued | running | completed | failed",
      "stage": "parsing | chunking | embedding | summarizing",
      "progress_current": 3,
      "progress_total": 9,
      "retry_count": 0,
      "error": null,
      "started_at": "…",
      "completed_at": null
    }
  ]
}
```

`jobs` 只在 `GET /documents/{id}` 回傳，列出每一類最近的一筆工作。`storage_path` 與 `content_hash` 不對外回傳。

**`DELETE /documents/{id}`**：回 `204`。文件、切塊、摘要、處理工作與原始檔案一併刪除；進行中的處理工作失效（見 `02-architecture.md` 第 3.4 節）。

**`POST /documents/{id}/retry`**：回 `202` 與文件物件。

- 文件狀態為 `failed`：排入新的 `index` 工作。
- 文件為 `ready` 且摘要狀態為 `failed`：排入新的 `summary` 工作。
- 其他情況，或同類工作已在 `queued`／`running`：回 `409`。

**`GET /documents/{id}/events`**（SSE）：連線後先送出目前的狀態，之後有變化時送出。沒有進行中的工作時送出 `done` 並結束。

| event | data |
|---|---|
| `progress` | `{"kind": "index", "stage": "embedding", "current": 2, "total": 5}` |
| `status` | `{"status": "ready", "summary_status": "processing"}` |
| `done` | `{"status": "ready", "summary_status": "ready"}` |

前端依 `status.summary_status` 與 `kind=summary` 的 `progress` 顯示摘要的狀態與進度（例：「可以提問 · 16 頁 · 46 個片段 · 摘要產生中 3/9」）；索引完成（`status` 變 `ready`）時即可提問，不必等摘要（AC-11）。摘要仍在產生的文件，前端重新整理後會繼續跟進度。
| `error` | `{"kind": "summary", "detail": "…"}` |

### 1.5 對話與提問

**`POST /conversations`**：`{"title": "可省略"}`。回 `201` 與對話物件。省略標題時，以第一個問題的前 40 字作為標題。

**`GET /conversations`**：自己的對話清單，依最後更新時間排序。每筆含 `id`、`title`、`created_at`、`updated_at`。

**`GET /conversations/{id}`**：對話物件加上 `messages` 陣列。

訊息物件：

```json
{
  "id": "uuid",
  "role": "user | assistant",
  "content": "…",
  "status": "pending | streaming | completed | failed | interrupted",
  "answered": true,
  "sources": [],
  "created_at": "…"
}
```

`status` 不是 `completed` 的助理訊息，介面必須標示為未完成，不當成完整回答顯示。

**`DELETE /conversations/{id}`**：回 `204`。訊息一併刪除；LLM 呼叫紀錄保留。

**`POST /conversations/{id}/messages`**：提問。

```json
{
  "question": "compare lightRAG with GraphRAG",
  "document_ids": ["uuid"]
}
```

搜尋範圍：

- `document_ids` 有值：只搜尋那些文件。其中任何一份不存在或不屬於自己，回 `404`；存在但尚未 `ready`，回 `409` 並列出是哪幾份。
- `document_ids` 省略或為空陣列：搜尋自己所有 `ready` 的文件〔使用者決定，D45〕。多份文件共用同一個 Top-K。
- 自己沒有任何 `ready` 的文件：回 `409`，`code` 為 `NO_READY_DOCUMENT`，不呼叫 LLM。
- `question` 的 token 數超過 `QUESTION_TOKEN_BUDGET`：回 `422`，`code` 為 `QUESTION_TOO_LONG`。不呼叫 LLM、不建立訊息、不截斷問題〔使用者決定，D45〕。

通過檢查後回 `200`，本文為 SSE 串流，事件依序出現：

| event | data | 說明 |
|---|---|---|
| `start` | `{"user_message_id": "uuid", "assistant_message_id": "uuid", "scope": {"mode": "all \| selected", "document_ids": ["uuid"]}}` | 兩則訊息已建立；`scope` 是這次實際搜尋的文件範圍 |
| `route` | `{"type": "retrieval \| summary", "standalone_question": "…"}` | 問題類型與改寫後的問題 |
| `sources` | 來源清單，格式見下 | 這次回答可引用的來源 |
| `delta` | `{"text": "…"}` | 回答的一小段文字，重複多次 |
| `usage` | `{"prompt_tokens": 2610, "completion_tokens": 412, "limit": 10000}` | Ollama 回報的實測用量 |
| `stage` | `{"stage": "generating"}` — 只在實驗模式出現。兩次呼叫修正模式（`ANSWER_REVISION=true`，D69）依序 `generating`、`verifying`、（`revising`、`verifying`）、`finalizing`；此模式不串流初稿，`delta` 在 `finalizing` 之後才送，是**生成完成後的逐段傳送**，不是模型即時串流。導航模式（`ANSWER_MODE=navigate`，D71）在 `sources` 之前送一個 `navigating`，之後的回答仍是即時串流 | 進行中 |
| `done` | `{"status": "completed", "answered": true, "cited": [1, 3], "unverified_numbers": [], "verified_numbers": [{"number": "83.6%", "document_id": "uuid", "page": 7, "snippet": "…"}], "mislabelled_numbers": [{"number": "59.6%", "answer_labels": ["Overall", "Mix"], "source_labels": [["Comprehensiveness", "Mix", "-High", "vs NaiveRAG"]], "sentence": "…"}], "unresolved_numbers": [{"number": "57.6%", "answer_labels": ["Overall", "Mix"], "source_labels": [["Overall", "Mix", "-High", "vs NaiveRAG"]], "sentence": "…", "reason": "missing"}], "overstated_claims": [{"sentence": "…", "method": "LightRAG", "compared": ["-High"], "higher": 4, "lower": 2, "examples": ["Diversity / Agriculture: LightRAG 60.0% vs -High 62.0% (p. 1)"], "status": "contradicted", "reason": null}], "doubtful_citations": [{"sentence": "…", "cited": [3], "closer": [5], "coverage_cited": 0.1, "coverage_closer": 0.7}], "finish_reason": "stop", "revision": null}` | 結束 |
| `error` | `{"detail": "…", "code": "…"}` | 失敗；助理訊息的狀態為 `failed` |

`error.code`：`LLM_UNAVAILABLE`、`INPUT_EXCEEDS_CONTEXT`、`CONTEXT_BUDGET_EXCEEDED`、`EMBEDDING_UNAVAILABLE`（嵌入服務連不上或出錯）、`EMBEDDING_INPUT_FAILED`（D70：嵌入服務正常，但模型對這段文字算出 NaN——bge-m3 在 GPU 上對特定片語會如此，CPU 不會；前端提示換個說法，不改寫問題、不換模型）、`INTERNAL_ERROR`。

來源的格式（原文切塊與摘要共用）：

```json
{
  "index": 1,
  "kind": "chunk | summary",
  "document_id": "uuid",
  "filename": "2410.05779v3.pdf",
  "page_start": 8,
  "page_end": 8,
  "section_title": null,
  "snippet": "原文片段或摘要片段",
  "score": 0.61,
  "origin": "retrieval | table_context | summary"
}
```

- 前端必須顯示這次的搜尋範圍：`scope.mode` 為 `all` 時顯示「所有可用文件」，為 `selected` 時列出所選的文件。
- 前端對每筆來源顯示檔名、頁碼（範圍以「第 7–9 頁」表示）與來歷：檢索結果顯示相似度，`table_context` 標「表格之後的討論」，摘要來源標「全文摘要」或「章節摘要：標題」；點開看片段（AC-11，2026-11-06）。
- 前端顯示 `route`：問題類型（檢索／摘要），改寫後的問題與原問題不同時一併顯示（AC-16 的可見化）。
- 前端在回答後顯示數字核對的結果：找到的數字附頁碼與原文片段、找不到的數字、標籤不符的數字與兩邊的標籤、未能判定的數字與它可能對應的格子（AC-26）。未能判定的不是錯誤，不用錯誤的樣式，也不在回答下方附說明（D67）。結論與表格不符的宣稱以錯誤樣式顯示並在回答下方附說明；引用可疑只在展開細節以灰字列出，不附說明（D68）。這些結果只隨 `done` 事件送出，不存入訊息；重新開啟對話時只剩回答文字內附的說明。
- `kind=chunk`：原文切塊，`page_start` 與 `page_end` 相同，`score` 為相似度。
- `kind=summary`：章節摘要，帶章節標題與頁碼範圍，`score` 為 `null`。
- `origin`（2026-11-06 補入，D62）：來源怎麼來的。`retrieval` 是向量檢索的 Top-K；`table_context` 是檢索結果含表格時，依文件結構補上的、緊接在該表格之後且屬於同一章節的討論段（最多兩塊，`score` 為 `null`，排在檢索結果之後，一樣受證據預算約束）；`summary` 是摘要類回答的來源。P4 比較不同 Top-K 時以 `origin=retrieval` 的來源為準。
- `done.answered=false` 表示判定為找不到答案；此時仍以 `delta` 送出一段固定的說明文字，`cited` 為空。
- `done.unverified_numbers` 列出回答中無法在所引用頁面原文找到的數字（AC-26）；此時另以 `delta` 在回答後附一段說明，列出這些數字。`done.verified_numbers` 列出找得到的數字與其所在的文件、頁碼及該頁原文片段（架構規格第 7 節「來源附上該頁原文片段」的落實；2026-11-06 補入）。核對範圍是被引用來源的頁碼範圍，沒有引用時為全部來源；比對時忽略千分位逗號與百分號；一位數的整數（如「Table 2」）不核對。
- `done.mislabelled_numbers`（2026-11-06 補入，D64；D67 改為結構化比對）：回答中來自表格的數字，其在答案裡的標籤被原文表格**否定**者。表格切塊的每一行是「列標籤 — 欄位分組: 子欄 數值, …」（架構規格第 5 節），所以每個數字在原文中是一個格子：列、分組、子欄三類標籤，加上同一組只有兩格時的「比較對象」（另一格的子欄，顯示為 `vs NaiveRAG`）。核對把答案中含該數字的句子讀成一個宣稱：每類標籤依角色取，不依距離——寫在數字旁的標籤（「NaiveRAG 32.4%」「32.4% (NaiveRAG)」「32.4% in Legal」「57.6% for -High」）是它自己的；否則取子句中唯一自由提及的那個，再退到整句唯一提及的那個；句中寫明「the same …」時可繼承上一句唯一的那個標籤。緊接在 over／against／than／versus／compared to／relative to（中文：優於／勝過／相較於／對比）之後的方法名是**比較對象**，不是數字的所屬方法。數值相同的格子中沒有任何一格符合答案給的標籤（含比較對象）→ 列入 `mislabelled_numbers`，附答案的標籤、原文各格的標籤與那個句子，並以 `delta` 在回答後附一段說明。
- `done.unresolved_numbers`（2026-11-06 補入，D67）：有格子符合答案給的標籤，但答案少給了該格子有的某類標籤（`reason: "missing"`），或同一類在子句裡有兩個自由的候選、核對不猜（`reason: "ambiguous"`）。欄位同 `mislabelled_numbers` 加 `reason`；`source_labels` 是符合的格子。這不是錯誤：核對不知道，不等於答案錯；回答下方不附說明。全部標籤都給了且有格子符合的數字不另列出（視為支持）。整個核對是規則比對、不呼叫 LLM、不含任何特定論文的字面；數字存在於頁面（`verified_numbers`）不代表歸屬正確，核對沒列出也不代表答案全對。
- `done.overstated_claims`（2026-11-06 補入，D68）：回答中宣稱某方法「在所有／每個／一律（all／every／consistently…）」情況下優於或劣於其他方法的句子，對引用頁面的表格逐格檢查。主詞是比較動詞（outperform／surpass／better／higher／lower…；優於／勝過／領先…）之前最近的方法名；比較對象是句中點名的其他方法，沒點名就取與主詞共享（列、欄位分組）格子的所有其他子欄；句中點名資料集或指標時只看那些格子。同一張表的不同區塊若重複同樣的列與分組（Table 2 的各變體區塊），視為可互相比較，重複出現的參照欄取主詞所在區塊的。對每一對共享格子數主詞較高與較低的格數：**兩邊都有** → `status: "contradicted"`，`examples` 列較少那一方向的格子（最多三個進說明），回答後以 `delta` 附說明；全部同一方向 → 不報（不假設指標是高好還是低好）；沒有任何共享格子 → `status: "unresolved"`。帶 most／many／nearly／generally 等限定詞的句子不算全稱。這只能發現矛盾，不能修正回答；驗收仍以回答內容為準。
- `done.doubtful_citations`（2026-11-06 補入，D68）：每句有引用的陳述，取內容詞（去停用詞與多數來源都有的詞、長度 ≥ 4 的英文詞）算每個來源的覆蓋率。數字也算內容詞。只有在被引來源最高覆蓋 ≤ 0.34、而某個未被引的來源覆蓋 ≥ 0.5、至少 3 個共同詞且 ≥ 被引的兩倍時，列出該句、被引編號、較接近的來源編號與兩個覆蓋率。與被引來源同一文件同一頁的來源算作被引（引用已指到正確的頁）；被引來源含有這句的某個數字時不列（引用是為了數字）；沒有自己引用的句子沿用同一段落中下一個有引用的句子的引用（模型常整段只引一次）；只檢查原文切塊來源（`kind: chunk`），摘要來源是改寫、不檢查。這是**懷疑**而非判錯，也不因關鍵字相同就判引用正確；不足 4 個內容詞、沒有引用、沒有以空白分詞的語言（中文）的句子不檢查。門檻在 `evaluation/answer-checks/` 的 13 份真實回答上選定。字面比對、不呼叫 LLM。
- `usage` 在兩次呼叫模式下是兩次呼叫的**合計**：`prompt_tokens`、`completion_tokens` 為總和，`limit` 為 `null`（上限是每次呼叫各自 10,000，合計沒有意義），另有 `calls`（1 或 2）。預設模式維持單次呼叫的數字與 `limit`。
- `done.revision`（D69）：預設模式為 `null`。兩次呼叫模式為 `{"mode": "conditional"|"always", "triggered": bool, "draft_triggers": [{"kind", "severity", "feedback"}], "revision_triggers": [...], "skipped": null|"budget"|"failed"|"revision cut short", "chosen": "draft"|"revision", "status": "verified"|"unverified", "reason": "…", "draft_text": "…", "revision_text": "…"|null}`（兩段文字只隨事件送出供實驗紀錄，不儲存、介面不顯示未選的那一段）。`kind` 為 `mislabelled_number`、`overstated_claim`、`invalid_citation`（hard）、`doubtful_citation`、`incomplete`（soft）。`verified` 只表示所選答案沒有任何檢查項目觸發，**不是正確的保證**；初稿不持久化，`finalizing` 前離開的客戶端得到空內容的 `interrupted` 訊息。前端顯示階段文字、所選版本與狀態；初稿與修正稿只在實驗紀錄（`evaluation/revision-ab/`）保存。
- `done.navigation`（D71）：預設與 roles 模式為 `null`。navigate 模式為 `{"map_entries", "plan"（Navigator 原文）, "items": [{"text", "located", "pages"}], "located", "fetched", "kept", "excluded_budget", "skipped": null|"budget"|"failed", "log": [{"ordinal", "page", "kept", "reason"}]}`。`items` 是 Navigator 的每一條，對照文件地圖（切塊裡的編號標題行給出的章節與子章節及其切塊範圍、章節摘要的頁碼範圍為後備、切塊裡的表／圖標題行）定位：表／圖編號、章節號或標題字、文件範圍內的明確頁碼；定位不到的不取證。D73 起每條另有 `location`、`need`、`priority`（`required`｜`supplementary`）、`status`（`covered`｜`missing`｜null，Navigator 自己的判斷）、`label`（定位到的地圖項目）、`candidates`、`selected`（納入的切塊 ordinal）、`excluded: [{"ordinal", "reason"}]`；頂層另有 `budget`（扣掉原始來源後的剩餘證據預算）、`evidence_tokens`、`embedding: {"texts", "failed"}`（need 向量的嵌入次數與失敗代碼）。D74 起 `items[]` 另有 `coverage`（`covered`｜`partial`｜`missing`｜`unknown`｜`not_located`，程式依結構判定），頂層另有 `coverage: [{"location", "status", "reason"}]`、`unmet_required`（required 卻沒進 prompt 的目標）、`supplementary_used`、`matrix: {"cells", "tables", "definitions"}`；`log[].reason` 多 `target already covered by the retrieved sources`／`all required evidence already covered`／`supplementary cap reached`／`repeats evidence already selected`。`done` 另有（所有模式）`direction_issues: [{"sentence", "left", "right", "status": "inconsistent"|"uncertain"|"incomparable", "detail"}]`、`completeness: {"status": "complete"|"incomplete"|"not_applicable", "required", "missing", "condition"}`、`analysis_status`（`SUPPORTED_AND_COMPLETE`｜`FACTUALLY_CORRECT_BUT_INCOMPLETE`｜`FACTUALLY_INCORRECT`｜`UNCERTAIN`；拒答時 null）。D75 起 `direction_issues[]` 另有 `kind`（`ordering`｜`performance`）、`cue`、`first_is_up`；`done.correction`（navigate 模式；其他模式 null）：`{"applied"（`AUTO_CORRECTION`，預設 false：只報告不改）, "changed", "edits": [{"kind": "label"|"figure"|"ordering"|"performance", "before", "after", …}], "removed": [刪去的括號或句子], "remaining": [修正後仍不符的項目], "reverted": [改了又因不符未減少而撤回的項目], "uncertain": [{"sentence", "cue", "left", "right"}], "step_numbering_stripped"}`；`stage` 多一個值 `correcting`（只在有修正時送出）。D76 起 `done` 另有 `conclusion_issues: [{"sentence", "status", "detail"}]`（「唯一例外」「沒有例外」等結論句對照矩陣算出的比較事實）與 `arithmetic_issues: [{"sentence", "stated", "computed", "status", "detail"}]`（回答自算的倍數）；`completeness.status` 多一個值 `uncertain`；`navigation.matrix` 另有 `facts`（比較事實數）與 `coverage_gaps`（來源點名、但沒有逐格矩陣的表）；摘要來源的 payload（`kind: "summary"`）多 `verification: {"status": "VERIFIED"|"CONTRADICTED"|"UNCERTAIN"|"NOT_CHECKED", "contradicted", "unverified", "unresolved", "checked_figures"} | null`。navigate 模式的 `delta` 自 D75 起為修正後文字的分段送出，不是模型串流。取到的切塊排在原始檢索來源之後，各目標輪流在預算內納入；`log` 逐塊記保留與否、原因、所屬目標與相關度（`retrieval`／`plan: <location>`／`low relevance`／`target quota reached`／`already among the retrieved sources`／`already selected for another target`／`over the evidence budget`）。`sources[].origin` 多一個值 `navigation`。`usage` 為兩次呼叫合計（`calls: 2`、`limit: null`）。
- `done.finish_reason`：LLM 呼叫的結束原因（`stop`、`output_limit`、`context_exhausted`…）；未呼叫 LLM 時為 `null`。
- 摘要類問題而摘要尚未 `ready`：以 `delta` 回覆摘要尚未完成或已失敗，`answered` 為 `false`（AC-42）。

### 1.6 `GET /llm-calls`

查詢參數：`conversation_id`、`document_id`、`limit`（預設 50）。只回傳自己的紀錄。

```json
{
  "limit": 10000,
  "measured": { "count": 12, "max_total_tokens": 7812 },
  "unmeasured": { "count": 1, "max_budget_upper_bound": 5098 },
  "underestimate_events": 0,
  "calls": [
    {
      "id": "uuid",
      "purpose": "answer | rewrite | section_summary | document_summary",
      "model": "qwen3:32b",
      "status": "pending | completed | failed | interrupted",
      "finish_reason": "stop | output_limit | context_exhausted | client_disconnect | unknown | null",
      "estimated_prompt_tokens": 2598,
      "max_output_tokens": 2500,
      "budget_upper_bound": 5098,
      "prompt_tokens": 2610,
      "completion_tokens": 412,
      "total_tokens": 3022,
      "received_output_tokens_estimated": null,
      "error": null,
      "duration_ms": 17450,
      "created_at": "…"
    }
  ]
}
```

- `prompt_tokens`、`completion_tokens`、`total_tokens` **只放 Ollama 回報的實測值**。拿不到時為 `null`，表示實測值未知。
- `budget_upper_bound` 是 `estimated_prompt_tokens + max_output_tokens`，即送出前通過檢查的預算上界，每筆都有。
- `received_output_tokens_estimated`：串流中斷時，以本地 tokenizer 對已收到的文字計數。這是預估值，只供參考，不計入實測。
- `measured`：有實測值的呼叫數，以及其中最大的實測總和。這是**實測合規**的依據。
- `unmeasured`：沒有實測值的呼叫數，以及其中最大的預算上界。這只能說明它們**送出前通過了預算檢查**，不能稱為實測合規。
- `underestimate_events`：實測 prompt tokens 大於預估值的次數，加上被 Ollama 以輸入超量拒絕的次數（AC-25）。
- `finish_reason`：這次呼叫如何結束；呼叫失敗時為 `null`，原因在 `error`。
- 合計數字涵蓋所有符合篩選條件的呼叫，`limit` 只限制 `calls` 清單的筆數（1–200）。

### 1.7 `GET /health`

不需登入。回應整體狀態、資料庫與 Ollama 各自是否正常、模型名稱、context 上限。格式與 P0 相同。

## 2. 受管理的物件與生命週期

| 物件 | 擁有者 | 如何產生 | 狀態機 | 如何結束 |
|---|---|---|---|---|
| User | — | 註冊 | 無 | 不提供刪除 |
| Session | User | 登入 | 無 | 登出或到期時刪除 |
| Document | User | 上傳 | 文件狀態、摘要狀態 | 使用者刪除；連同工作、切塊、摘要與檔案 |
| IngestionJob | Document | 上傳、重試、建索引成功後自動排入摘要 | 有 | 隨文件刪除 |
| Chunk | Document | 建索引工作 | 無 | 隨文件刪除；重試時整批重建 |
| Summary | Document | 摘要工作 | 無（狀態在 Document） | 隨文件刪除；重試時整批重建 |
| Conversation | User | 使用者建立 | 無 | 使用者刪除；連同訊息 |
| Message | Conversation | 提問 | 助理訊息有 | 隨對話刪除 |
| LLMCall | User | 每次呼叫 LLM 前寫入 | 有 | 不刪除；關聯的物件被刪除時，關聯欄位清空 |

**Document 的文件狀態**

```
上傳 → uploaded → processing → ready
                      │
                      └→ failed ──（重試）──→ processing
```

**Document 的摘要狀態**（獨立於文件狀態）

```
none → processing → ready
           │
           └→ failed ──（重試）──→ processing
```

**IngestionJob**：`queued → running → completed` 或 `failed`。

不設 `cancelled` 狀態〔使用者決定，D45〕：刪除文件時處理工作的紀錄一併刪除，進行中的工作以「寫入前確認」失效（`02-architecture.md` 第 3.4 節）。

**Message（助理訊息）**：`pending → streaming → completed` 或 `failed` 或 `interrupted`。使用者訊息建立時即為 `completed`。

`completed` 只用於模型自然結束的回答。串流中斷，或回答因輸出上限、context 用盡而未完整生成時，皆為 `interrupted`（`02-architecture.md` 第 4.2 節，AC-57）。

**LLMCall**：`pending → completed` 或 `failed` 或 `interrupted`。

合法的轉換只有上面列出的。Service 收到不合法的轉換要求時回 `409`。

## 3. 資料表

以 Alembic migration 建立。主鍵皆為 UUID，時間皆為 UTC。P2-A 建立 P2 需要的全部資料表；`summaries` 在 P3 加入。

### `users`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `id` | uuid | 主鍵 |
| `username` | text | 唯一 |
| `password_hash` | text | Argon2 雜湊，含 salt |
| `display_name` | text | |
| `answer_language` | text | 偏好：`auto`／`zh-TW`／`en`，預設 `auto` |
| `answer_detail` | text | 偏好：`brief`／`normal`／`detailed`，預設 `normal` |
| `created_at`、`updated_at` | timestamptz | |
| `last_login_at` | timestamptz，可為空 | |

不建立 `email` 與 `status`（沒有對應的使用情境）。

### `sessions`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `id` | uuid | 主鍵 |
| `user_id` | uuid | 外鍵 |
| `token_hash` | text | Session token 的 SHA-256，唯一。token 本身不存入資料庫 |
| `expires_at` | timestamptz | |
| `created_at` | timestamptz | |

### `documents`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `id` | uuid | 主鍵 |
| `owner_id` | uuid | 外鍵 |
| `filename` | text | 原始檔名 |
| `content_hash` | text | 內容的 SHA-256；`(owner_id, content_hash)` 唯一 |
| `media_type` | text | `pdf`／`txt`／`md` |
| `file_size` | bigint | 位元組 |
| `storage_path` | text | 檔案在儲存目錄中的相對路徑 |
| `status` | text | `uploaded`／`processing`／`ready`／`failed` |
| `summary_status` | text | `none`／`processing`／`ready`／`failed` |
| `error` | text，可為空 | 最近一次失敗的原因 |
| `page_count` | int，可為空 | |
| `created_at`、`updated_at` | timestamptz | |

### `ingestion_jobs`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `id` | uuid | 主鍵 |
| `document_id` | uuid | 外鍵，文件刪除時一併刪除 |
| `kind` | text | `index`／`summary` |
| `status` | text | `queued`／`running`／`completed`／`failed` |
| `stage` | text，可為空 | `parsing`／`chunking`／`embedding`／`summarizing` |
| `progress_current`、`progress_total` | int，可為空 | |
| `retry_count` | int | 同一文件同類工作的第幾次重試，首次為 0 |
| `error` | text，可為空 | |
| `created_at`、`started_at`、`completed_at` | timestamptz | 後兩者可為空 |

同一文件同一類工作，同時最多一筆處於 `queued` 或 `running`（以部分唯一索引保證）。

### `chunks`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `id` | uuid | 主鍵 |
| `document_id` | uuid | 外鍵，文件刪除時一併刪除 |
| `ordinal` | int | 在文件中的順序 |
| `page` | int | 頁碼，從 1 起算 |
| `text` | text | 切塊內容 |
| `token_count` | int | |
| `embedding` | vector(1024) | `bge-m3` 向量；HNSW cosine 索引 |
| `created_at` | timestamptz | |

切塊沒有 `owner_id`。檢索時一律 join `documents` 並以 `documents.owner_id` 過濾。
P4 的 Hybrid 實驗在實驗工具內計算、未達採用條件（ADR 0010），沒有加入全文檢索欄位。

### `chunk_vectors`（P4，D82）

| 欄位 | 型別 | 說明 |
|---|---|---|
| `id` | uuid | 主鍵 |
| `chunk_id` | uuid | 外鍵，切塊刪除時一併刪除 |
| `ordinal` | int | 區塊在表格內的順序 |
| `embedding` | vector(1024) | 該區塊（標題行＋群組表頭＋區塊表頭＋該區塊的列）的 `bge-m3` 向量；HNSW cosine 索引 |
| `created_at` | timestamptz | |

只有多區塊的表格切塊有列；一個切塊的檢索分數是自身向量與這些向量中最好的一個（架構 §6）。

### `summaries`（P3）

| 欄位 | 型別 | 說明 |
|---|---|---|
| `id` | uuid | 主鍵 |
| `document_id` | uuid | 外鍵，文件刪除時一併刪除 |
| `level` | text | `section`／`document` |
| `ordinal` | int | 章節順序；全文摘要為 0 |
| `title` | text，可為空 | 章節標題 |
| `page_start`、`page_end` | int | 涵蓋的頁碼範圍 |
| `source_chunk_ids` | uuid[] | 章節摘要：產生它的原文切塊 |
| `source_summary_ids` | uuid[] | 全文摘要：合併自哪些章節摘要 |
| `text` | text | 摘要內容；具體數字後帶頁碼標註 |
| `token_count` | int | |
| `created_at` | timestamptz | |

### `conversations`

`id`、`owner_id`（外鍵）、`title`、`created_at`、`updated_at`。

### `messages`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `id` | uuid | 主鍵 |
| `conversation_id` | uuid | 外鍵，對話刪除時一併刪除 |
| `role` | text | `user`／`assistant` |
| `content` | text | 訊息內容；串流中逐步寫入 |
| `sources` | jsonb | 助理訊息所附的來源，格式同 1.5。保存當時的檔名、頁碼與片段，文件日後被刪除也不受影響 |
| `status` | text | `pending`／`streaming`／`completed`／`failed`／`interrupted` |
| `answered` | bool，可為空 | 是否判定為有答案 |
| `created_at`、`updated_at` | timestamptz | |

### `llm_calls`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `id` | uuid | 主鍵 |
| `owner_id` | uuid | 外鍵 |
| `conversation_id` | uuid，可為空 | 對話被刪除時清空 |
| `message_id` | uuid，可為空 | 訊息被刪除時清空 |
| `document_id` | uuid，可為空 | 文件被刪除時清空 |
| `purpose` | text | `answer`／`rewrite`／`section_summary`／`document_summary` |
| `model` | text | |
| `status` | text | `pending`／`completed`／`failed`／`interrupted` |
| `estimated_prompt_tokens` | int | 送出前的本地計數（含安全緩衝） |
| `max_output_tokens` | int | 這次呼叫的輸出上限 |
| `prompt_tokens` | int，可為空 | **只放 Ollama 回報的實測值**；未知為空 |
| `completion_tokens` | int，可為空 | **只放 Ollama 回報的實測值**；未知為空 |
| `received_output_tokens_estimated` | int，可為空 | 中斷時對已收到文字的本地計數，預估值 |
| `finish_reason` | text，可為空 | 這次呼叫如何結束：`stop`（自然結束）／`output_limit`／`context_exhausted`／`client_disconnect`／`unknown`。呼叫失敗（含被 Ollama 拒絕）時為空，原因在 `error`。此欄在 P2-D 以 migration 加入 |
| `error` | text，可為空 | |
| `duration_ms` | int，可為空 | |
| `created_at`、`updated_at` | timestamptz | |

### 刪除規則

| 刪除 | 一併刪除 | 保留並清空關聯 |
|---|---|---|
| Document | IngestionJob、Chunk、Summary、原始檔案 | LLMCall 的 `document_id` |
| Conversation | Message | LLMCall 的 `conversation_id`、`message_id` |
| Session（登出、到期） | — | — |

不使用 Soft Delete。

## 4. 程式內部介面

只有單元測試需要替換的三個外部相依保留 `Protocol`：

```python
class TokenCounter(Protocol):
    def count(self, text: str) -> int: ...

class LLMGateway(Protocol):
    """Text in, text out. Raises ContextBudgetExceeded before sending if the
    prompt plus max_output_tokens would exceed the context limit. Writes a
    ledger row before sending and updates it on completion, failure or
    interruption."""

    async def generate(
        self, prompt: str, *, purpose: str, max_output_tokens: int, context: CallContext
    ) -> LLMResult: ...

    def stream(
        self, prompt: str, *, purpose: str, max_output_tokens: int, context: CallContext
    ) -> AsyncIterator[LLMChunk]: ...

class Embedder(Protocol):
    async def embed(self, texts: list[str]) -> list[list[float]]: ...
```

- `CallContext` 帶擁有者與可選的對話、訊息、文件，供帳本記錄。
- `LLMGateway` 只收字串，這是限制 C-1 在型別上的保證。帳本的寫入在 Gateway 的實作內完成，呼叫端無法繞過。
- Repository 是一般的類別，不另建介面與假實作，直接對真實的 PostgreSQL 測試。每個查詢方法都要求傳入擁有者。
- Service 的每個方法都明確接收操作者（目前的使用者）。未來的 Agent Tool Adapter 只能呼叫 Service。

## 5. 環境變數

決策日誌 D41。

### 5.1 檔案

- `.env` 必須存在。它不進版本控制；`make setup` 在它不存在時由 `.env.sample` 複製一份。
- `.env.sample` 提供範例與預設值（取代現有的 `.env.example`）。

### 5.2 命名

| 變數 | 預設 | 說明 |
|---|---|---|
| `DB_HOST` | `127.0.0.1` | 容器內為 `db` |
| `DB_PORT` | `5433` | 容器內為 `5432` |
| `DB_NAME`、`DB_USER`、`DB_PASSWORD` | `documind` | |
| `HTTP_OLLAMA_HOST` | `127.0.0.1` | 容器內為 `host.docker.internal` |
| `HTTP_OLLAMA_PORT` | `11434` | |
| `LLM_MODEL` | `qwen3:32b` | |
| `EMBED_MODEL` | `bge-m3` | |
| `LLM_CONTEXT_LIMIT` | `10000` | 單次呼叫的 token 上限 |
| `LLM_THINKING` | `false` | D34 |
| `CHUNK_SIZE` | `400` | tokens；D30，P4 實驗調整 |
| `CHUNK_OVERLAP` | `80` | tokens；D30 |
| `TOP_K` | `5` | D30，P4 實驗調整 |
| `MIN_SIMILARITY` | `0.50` | 拒答門檻；D36；P4 以題庫校正（ADR 0010：0.50 擋下全部無答案題且無誤拒，0.45 只擋 1–2 題；餘裕 0.03–0.04） |
| `TOKEN_SAFETY_BUFFER` | `16` | token 計數的安全緩衝（AC-25）。不是絕對保證，見 `02-architecture.md` 第 4.1 節 |
| `QUESTION_TOKEN_BUDGET` | `200` | 問題的 token 上限；超過時請使用者縮短（D45）。未來可改為動態分配 |
| `MAX_UPLOAD_MB` | `50` | |
| `DATA_DIR` | `.data` | 上傳檔案的儲存目錄 |
| `SESSION_TTL_HOURS` | `168` | Session 有效時間（7 天） |
| `SESSION_COOKIE_SECURE` | `false` | 本地以 HTTP 執行時為 `false`；經 HTTPS 提供服務時必須設為 `true` |
| `ALLOWED_ORIGINS` | `http://127.0.0.1:3000,http://localhost:3000,http://127.0.0.1:5173,http://localhost:5173` | 來源檢查（`Origin`／`Referer`）的允許清單 |
| `WEB_BIND`、`WEB_PORT` | `127.0.0.1`、`3000` | Docker 版前端對外的位址與埠 |

現有的 `DATABASE_URL`、`POSTGRES_*`、`OLLAMA_BASE_URL` 會改為上表的鍵名；資料庫連線字串由 `DB_*` 在程式內組合。

### 5.3 讀取規則

- 所有環境變數只能透過單一的載入模組讀取；其他程式碼禁止直接使用 `os.getenv()` 或 `os.environ`。
- 本專案的載入模組為 `app/core/env_loader.py`（由現有的 `app/core/config.py` 改名）。規範原文指定的匯入路徑 `main.utils.env_loader` 是 Django 專案的結構；依使用者「名稱來不及就算了」不另外改名。
- 以自動測試檢查：`app/` 內除了載入模組之外，不得出現 `os.getenv` 或 `os.environ`。

### 5.4 未採用的項目

- `DJANGO_*` 變數：本專案不是 Django。
- Repo 名稱 `{platform}-{system}`：repo 已建立為 `DocuMind-AI`，依使用者指示不改名。
