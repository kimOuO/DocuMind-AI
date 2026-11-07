# ADR 0012（評估中）：通用表格推理架構——現況分析、可行性與實作規劃

- 狀態：**評估中**，尚未決定；本文件只做架構調查、可行性分析、實驗設計與實作規劃，沒有改程式、資料庫或提示詞
- 日期：2026-11-07
- 對應決策日誌：D74–D86（矩陣、比較事實、區塊向量、C8–C9、CS／BS 題庫測試）
- 數據來源：`evaluation/navigator-abc/`（B3–B9、C8、C9）、`evaluation/retrieval-parameters/`（含 `answers/` 的 38 筆）、本文件寫作時以真實 tokenizer 對 demo 部署裡的 Table 1 量測的 token 數（標「實測」）；其餘標「程式碼分析」或「估算」

---

## 1. Current Architecture Analysis（現況資料流與主要問題）

### 1.1 表格如何進入 chunk（程式碼分析，已確認）

1. `app/ingestion/tables.py::find_table_regions`：以形狀辨識表格區域——`Table N:` 標題行、之後最多 12 行說明或表頭、再接數字列，到第一行散文為止（D81 放寬說明行數）。
2. `linearize_table`：每一列逐格改寫成「列標籤 — 群組：子欄 值, 子欄 值; …」，表頭與區塊表頭保留原位。
3. `split_table`：整張表若 ≤ 4 × 400 ＝ 1,600 tokens 就是**一個 chunk**（LightRAG Table 1 實測 1,487 tokens、Table 2 約 1,450），否則依列切成多塊，各帶標題行與表頭（GraphRAG Table 6 3,001 tokens → 10 塊）。
4. `table_blocks`（D82）：多區塊表格另依區塊表頭切段，每段一個向量存 `chunk_vectors`；檢索時 chunk 取自身與各區塊向量的最佳分數。chunk 的文字不變。
5. 沒有任何結構化表格存進資料庫。**結構化的格子（`MatrixCell`）是回答時由 `app/chat/evidence.py::build_matrix` 從 chunk 文字重建**，欄位：table、group（資料集）、row（指標）、column（方法）、paired_with、block、value、unit、direction、direction_basis、complementary。命名是通用的，不綁論文語意；但它只認得 `linearize_table` 的輸出格式，對沒被逐格改寫的表（Table 6）沒有格子（coverage gap）。

### 1.2 Summary Tree 是否重複保留表格數字（程式碼分析＋紀錄，已確認）

會。章節摘要的輸入是該章節的全部 chunk（EVALUATION 章節 19 塊，含整張 Table 1、Table 2），模型寫 250 字摘要時會把表格數字寫進去；全文摘要再從章節摘要合併。所以同一個數字存在於：chunk 文字、章節摘要、全文摘要三處。但它們**不會在同一次 prompt 裡同時出現**（見 1.4）。

### 1.3 最終 Prompt Assembly 在哪裡（程式碼分析，已確認）

- `app/chat/prompting.py::build_answer_prompt`：前置文字（preamble）＋固定指示＋編號來源（依預算 5,500 tokens 裝到放不下為止）＋問題。
- `build_summary_prompt`：摘要路徑；來源是摘要節點，可附 Navigator 補的 chunk。
- `app/chat/service.py` navigate 分支：preamble ＝ Navigator 計畫 ＋ `analysis_preamble`（矩陣文字 ≤ 1,500 tokens ＋ 分析順序）。比較事實 `comparison_facts` 已算出但**不進 prompt**（B5 起使用者決定停用，供答後核對）。
- 守門：`estimate_prompt_tokens`（本地 tokenizer ＋ 16 緩衝）＋ 2,500 輸出保留 ≤ 10,000，超過拒絕呼叫；沒有截斷策略。

### 1.4 同一張表是否可能在單次輸入出現多次（程式碼分析，已確認）

| 路徑 | 同一張表在一次 prompt 裡出現的次數 |
|---|---|
| single（預設） | 1 次：表格 chunk（1,487 tokens）；表格後文補的是討論段，不是表 |
| navigate | **2 次**：表格 chunk（1,487）＋ 矩陣文字（1,348）。同一個數字兩種格式並列 |
| 摘要路徑（Q1） | 0 次原表；數字以摘要句子的形式出現在全文摘要與章節摘要各一次（兩份摘要可能寫同一組數字） |
| navigate 的 Q1 | 同上，再加 Navigator 補的 1 塊 chunk（可能是表） |

**已有證據顯示重複有害**：BS-T3（問 CS 的 -High 對 NaiveRAG 的 Overall）在矩陣同一行看到兩個 NaiveRAG 值（配 LightRAG 的 38.8、配 -High 的 44.0），取了第一個；single 模式只看 chunk 一次，答對。B9-Q2-2 在矩陣與 chunk 並列時仍把 NaiveRAG 區塊的 LightRAG 值配給 GraphRAG。

### 1.5 主要問題的定位（紀錄，已確認）

D85 的 38 筆：單一事實查找 27/28 對；要綜合多格下結論的 Q2、Q3、G2 兩種模式 0/6；Q1 錯在摘要層；X1 錯在跨文件名額。C9（temperature 0）證明晃動來自取樣，固定後剩三種錯：摘要層一個數字配錯、Q2 不點例外、Q3 不給數字。**模型抄數字可靠，把多格變成判斷不可靠**——這是提案要解的問題，定位正確。

### 1.6 若只改 Query 路徑不改 Summary Tree，Q1 是否仍失敗（已確認）

會。Q1 走摘要路徑，回答只讀存好的摘要；C8／CS／C9 共 15 次 Q1 全部照抄摘要樹的錯句（三批三種錯法，同一來源：EVALUATION 章節摘要）。回答階段的模型是忠實轉述，temperature 0 也救不了。Q1 只能在入庫（Phase 4）處理。

---

## 2. Proposed Architecture（新增什麼、重用什麼）

### 2.1 已經存在、可直接重用的（程式碼分析）

| 提案的元件 | 專案現有對應 | 差距 |
|---|---|---|
| Universal Table Representation | `MatrixCell`（通用欄位、含配對與區塊）、`table_blocks` | 回答時重建、不存；只支援「列標籤 — 群組：子欄 值」形狀；無合併格、多層表頭、單位混合、腳註 |
| Table Query Tools：Compare、Find Exceptions | `comparison_facts`（直接配對：幾個條件高、幾個低、例外清單；跨配對標為趨勢） | 已有；只對同一配對 |
| Calculate Difference、pp change、ratio | `check_arithmetic`（核對答案裡的比值） | 只做核對，不做產生；差值與百分點未實作 |
| Filter／Ranking／Aggregate | 無 | 需新寫（對 `MatrixCell` 列表做即可，數十行） |
| Claim Verification | `verify_numbers`、`check_labels`、`check_universal_claims`、`check_directions`、`check_conclusions` | 已有，有三種誤報一種漏報（D83） |
| Summary 數值驗證 | `summarization/service.py::_verification`（VERIFIED／CONTRADICTED／UNCERTAIN／NOT_CHECKED） | 只核對數字存在與標籤；不改寫、不重試；不檢查全稱句 |
| Query Routing | `question_type`（summary／retrieval，關鍵字規則） | 沒有「表格比較」意圖 |
| Token 守門與帳本 | `LLMGateway`、`llm_calls` | 完整 |

結論：提案的 Phase 1、2 大半已存在，只是**沒有進 prompt、沒有存、沒有算差值**。真正新的是：(a) 把工具結果放進 prompt 並決定放多少（Phase 3 的路由與 packing），(b) 摘要階段用工具結果（Phase 4），(c) 表格結構的泛化（多層表頭等）。

### 2.2 建議的架構（最小）

```
入庫：PDF → 區域偵測 → 逐格改寫 chunk → 向量（＋區塊向量）          （不變）
       ↘ 章節摘要時：先由 MatrixCell 算出該章節表格的「事實清單」交給摘要模型，
         摘要後驗證；CONTRADICTED 時帶反例重寫一次                     （Phase 4，新）

回答：問題 → 路由（摘要／檢索／表格比較）→ 檢索 Top-5＋表格後文
       → 若來源含表且問題含兩個以上出現在表頭的名稱：
           從來源的 chunk 重建 MatrixCell → 工具（compare、exceptions、difference）
           → 只把與問題相關的事實（約 100–400 tokens）放進 prompt
           → 表格 chunk 是否保留，依方案 B／C／D（見 §3）
       → 一次呼叫 → 答後核對照常
```

不新增 LLM 呼叫；工具全是確定性程式；不存結構化表（回答時重建，毫秒級）。

---

## 3. Context & Token Impact Analysis

### 3.1 研究問題 A：Context 是否重複

| 資料層 | 是否進同一次 prompt（single） | 是否進同一次 prompt（navigate） |
|---|---|---|
| 原文 chunk（逐列改寫的表） | 是（1 次） | 是 |
| 向量檢索 context | 同上（就是 chunk） | 同上 |
| 結構化 Table Store | 不存在 | 不存在；矩陣文字是它的即時渲染 → **是，與 chunk 重複** |
| Table Tool Result（比較事實） | 否（未啟用） | 否（B5 起停用） |
| Section／Document Summary | 否（檢索路徑不帶摘要） | 否 |

結論：single 今天沒有重複；navigate 今天就有一份重複（chunk＋矩陣），且 BS-T3 顯示重複的兩個 NaiveRAG 值造成錯選。新增工具結果若再加進去而不拿掉 chunk，就是第三份。

### 3.2 研究問題 B：Token 會增加多少（實測，Table 1，Qwen3 tokenizer）

| 表示方式 | tokens | 備註 |
|---|---|---|
| 逐列改寫的 Table 1 chunk（現況） | **1,487** | single 模式今天就在 prompt 裡 |
| 矯陣文字（整張） | 1,348 | navigate 今天額外加的 |
| 完整 MatrixCell JSON（128 格） | **11,681** | 單獨就超過 10K，**不可行** |
| 緊湊 JSON（row → block → column → value） | 1,891 | 比 chunk 還多 |
| 比較事實，全部 112 條 | 438 | 問題沒指名時 |
| 比較事實，只有問到的一對（LightRAG vs GraphRAG） | **97** | 含 13/16 計數與三個例外的數字 |
| 最小證據：只保留問到的配對那 16 行 | **420** | 可取代整塊 chunk 的角色 |

single Q2 現況 prompt 約 2,950 tokens（C9 實測 3,680 含輸出）。各方案的單次輸入估算：

| 情境 | 單次輸入 tokens | 增量 | 性質 |
|---|---|---|---|
| 原本 Text RAG | ≈ 2,950 | — | 實測 |
| ＋ 完整 Table JSON | ≈ 14,600 | 超過 10K | 實測相加 |
| ＋ 緊湊 JSON | ≈ 4,840 | ＋1,891 | 實測相加 |
| ＋ Table Tool Result（問到的一對） | ≈ 3,050 | ＋97 | 實測相加 |
| ＋ 全部事實 | ≈ 3,390 | ＋438 | 實測相加 |
| Evidence Replacement：拿掉表格 chunk、放最小證據＋事實 | ≈ 2,000 | **−950** | 估算（2,950 − 1,487 ＋ 420 ＋ 97） |
| Table-only query（只給最小證據與事實，不給散文） | ≈ 1,300 | −1,650 | 估算；但 Q2 需要 4.2、4.5 節的散文才能說「為什麼」 |
| Summary Tree ＋ Table Facts | 章節摘要輸入 ≤ 6,000 ＋ 事實 ≤ 438 | ＋≤438 | 估算；EVALUATION 章節輸入現約 5,900，加事實仍在 6,000 的切分門檻附近，需把事實算進切分 |

呼叫次數：方案 B／C／D 都維持 1 次（工具是程式）；navigate 2 次；累積輸入 ＝ 單次（single）。入庫端：建矩陣與事實毫秒級；摘要重寫一次是每個 CONTRADICTED 章節多一次 LLM 呼叫（LightRAG 論文約 1 次）。延遲：工具 < 10 ms；prompt 變短，回答變快。

### 3.3 研究問題 C：資訊增加是否降低品質

已有證據：(1) navigate（chunk＋矩陣）在 CS／BS 與 C8／B8 都沒有比 single 多答對任何一題，BS 的 T3 因重複值選錯；(2) 矩陣在 prompt 裡仍發生配對混淆（B9-Q2-2）；(3) temperature 0 後錯誤只剩「不點例外」「不給數字」——這兩件事正是工具結果能直接提供的（例外清單、該條件的四個數字）。推論（待實驗）：**用少而對的事實取代多而重複的原文，比再加一層更可能有效**。

優先級規則（建議）：工具結果 ＞ 原文 chunk ＞ 摘要；不一致時以工具結果為準並在答案標示（工具結果可逐格追溯到頁碼與原文）。完整 JSON 不給模型（實測 11,681 tokens）。「全部例外」類問題，事實清單必須完整列出例外（97 tokens 就含全部三個），不摘要。重複 chunk 去重：同一 chunk id 只出現一次（現有 `select_evidence` 已做）；表格 chunk 與其事實並存時，依方案 C 拿掉 chunk 或只留表頭與問到的列（方案 D）。

### 3.4 研究問題 D：四個方案

| 方案 | 單次輸入（Q2 估） | 資訊完整性 | 數值正確性 | 語意 | 複雜度 | 延遲 | 對現有架構 |
|---|---|---|---|---|---|---|---|
| A 全給（chunk＋JSON＋事實＋摘要） | > 10K（完整 JSON）或 ≈ 5,300（緊湊） | 最高但重複三份 | 重複值已證明會害（BS-T3） | 低 | 低 | 高 | navigate 現狀的延伸，不建議 |
| B 依意圖選 | 一般題不變；表格題 ≈ 3,050 | 高 | 事實正確、chunk 仍在 | 中 | 中（路由規則） | 不變 | 加一個意圖與一段 preamble |
| C Evidence Replacement | ≈ 2,000 | 失去原表的散文脈絡？（表格 chunk 只有數字，散文在別的 chunk，影響小） | 只剩一份數字來源，消除重複 | 需確保引用仍可追溯（事實帶頁碼與表名） | 中 | 變快 | 改 `build_answer_prompt` 的裝填：表格 chunk 以「事實＋最小證據」替身進入同一個來源編號 |
| D Minimal Packing | ≈ 2,000–2,400 | 只給問到的列與事實 | 同 C | 同 C | 中高（要從問題決定哪些列） | 變快 | 同 C，多一個選列規則 |

程式面 C 與 D 幾乎同一處改動；D 是 C 的細化。**實驗應先做 B（最小、可回退），再做 C；A 不做。**

---

## 4. Table Schema Design（最小）

不新增資料表。結構化表示沿用 `MatrixCell`，補三個欄位（估算，約 30 行）：`caption`（標題全文）、`source_chunk_id`、`confidence`（"linearised"：逐格改寫成功；"region_only"：區域偵測到但未改寫，如 Table 6；"none"）。來源追蹤：每格帶 `source_index`、`page`、`table`，事實帶 `table`、`page`、兩格的值。正規化限制（明列為不支援）：多層表頭（兩層以上）、合併格、單位混合、腳註符號（↑↓、*）、跨頁表的接續、文字格。這些情況 `confidence` 為 region_only，工具不計算、答案標「表格結構未能解析，請見原文」。若日後要存，`chunk_vectors` 的做法（一張附表、外鍵隨 chunk 刪）可照搬為 `chunk_cells`，但目前沒有必要。

## 5. Tool API Design（確定性函式，不是 LLM 工具呼叫）

```python
cells = build_matrix(indexed_sources)                      # 既有
facts = comparison_facts(cells, question)                  # 既有：compare + find_exceptions（同配對）
differences(cells, a, b) -> [Difference(group,row,value_a,value_b,pp_change,ratio)]   # 新
rank(cells, group=None, row=None) -> [Cell]                # 新，依 direction 排序
filter(cells, **labels) -> [Cells]                         # 新（薄封裝）
pack(facts, cells, question, budget) -> str                # 新：只渲染問到的配對與列（方案 C／D）
```

每個結果都帶 table、page、所用格子的值；缺值時結果標 `incomplete`。路由不交給 LLM：規則「來源含有格子的表，且問題的詞命中該表至少兩個欄名或區塊名」→ 表格比較；否則不動。Query Plan 不做（避免第二次 LLM 呼叫與無限工具呼叫），這是受控的後端固定路由。

## 6. Summary Verification Design（Q1）

1. 章節摘要的輸入在原文前加「本章節表格的事實清單」（由 `comparison_facts` 對該章節的格子算，≤ 438 tokens），要求摘要的比較句只能引用清單裡的事實。
2. 摘要後照常 `_verification`；新增對摘要跑 `check_universal_claims`（表格就在章節裡，格子可得）。
3. 判 CONTRADICTED 或全稱句被反駁時，**帶具體反例重寫一次**（第二次呼叫，入庫時允許），再驗；仍不符就保留原文並存狀態（現行）。
4. 回答 Q1 時，摘要路徑的 prompt 附驗證註記（D76 已寫好 `_verification_note`，B5 起停用），讓模型不照抄被反駁的數字。
5. 無法驗證的敘述（UNCERTAIN）維持現狀：存、標、不改。
6. 對合併品質的影響：章節摘要多 ≤ 438 tokens 輸入，仍在 6,000 門檻內；全文摘要不變。

這是唯一能碰到 Q1 的改動；C9 已證明回答端無法修 Q1。

## 7. Architecture Alternatives（更簡單的替代）

| 替代 | 改動量 | 預期效果 | 風險 |
|---|---|---|---|
| 只把 D76 的比較事實開回 prompt（方案 B 的最小版，一行設定） | 幾乎零 | 直接供應 Q2 缺的「例外清單」；Q3 缺的「四版本數字」要再加一條渲染 | 多 97–438 tokens；B4 時代設計過但從未在真實批次測過 |
| 提示詞只加「例外必須逐條點名」「變體題必須給同條件四個數字」 | 零 | C9 顯示錯就剩這兩件 | 提示詞規則模型不一定守（B3–B8 的經驗） |
| temperature 0 設為預設 | 一行 | 不提高正確率，但結果可重現、Demo 可預測 | 無 |
| 摘要重寫一次（§6 第 3 點） | 中 | 唯一能碰 Q1 的 | 多一次入庫呼叫 |
| 完整 Table Store ＋ Agent Tool Calling | 大 | 不確定 | 多次 LLM 呼叫、10K 內很難、與「不加第三次呼叫」衝突 |

## 8. Risk Analysis

- 語意對應：工具結果本身來自 `linearize_table` 的格子，若逐格改寫錯（目前兩張表 256 格無誤，Table 6 無格子），事實就錯；用 `confidence` 擋住 region_only 的表。
- 解析失敗：多層表頭、合併格不支援，必須標示而不是猜；泛化測試要用第三份不同領域的文件。
- 路由選錯：規則太寬會對不該算的表算；太窄沒效果。可記錄「路由命中」與人工判定對照。
- Context 成長：方案 A 立即超 10K；B 可控（≤ 438）；C／D 反而減少。
- 重複與衝突：事實與 chunk 並存時模型可能二選一；方案 C 消除。
- 工具結果的錯誤被當事實：事實清單要帶來源頁碼，答後核對照常跑。

## 9. Evaluation Plan

- 文件與題目：題庫 19 題（`question-set.json`）＋ Q1–Q3 各 3 次；泛化加一份不同領域有表格的 PDF（≥ 3 題，先建標準答案）。
- 控制變因：同模型 qwen3:32b、`ANSWER_TEMPERATURE=0`（讓每題一次即可比較）、同入庫、同 K 與門檻。
- 臂：Baseline（現有 single）、A 不做、B（意圖路由＋事實）、C（事實取代表格 chunk）、D（最小列）。
- 正確性指標：格子正確率（既有腳本逐格對）、工具事實正確率（對 ground truth）、例外集合完全一致、算術正確、全稱句命中、最終判定、無依據宣稱率。
- 效率指標：每次呼叫輸入 tokens、每題累積 tokens、呼叫次數、工具次數、延遲、入庫額外時間。
- **重複比例定義**：一次 prompt 中「出現兩次以上的（表格、資料集、指標、方法、值）五元組」的數量 ÷ prompt 內該類五元組總數；由 `cells_of` 對 prompt 的每個來源與事實段落抽格子計算，不用字面相似度。
- 成功判準：B 或 C 在 Q2、Q3 的判定不低於 Baseline、重複比例下降、單次輸入不升；Q1 由 §6 另測（重建摘要樹後 3 次）。

## 10. Implementation Roadmap（依優先序；都還沒做）

| 序 | 項目 | 改動檔 | 測試 | 估時 |
|---|---|---|---|---|
| 1 | `ANSWER_TEMPERATURE=0` 設為預設 | env_loader、.env.sample、規格 03 | 既有 | 10 分 |
| 2 | 方案 B：表格比較意圖（規則）＋事實進 prompt（重啟 `facts=`） | service.py、evidence.py（`pack`） | 單元：路由規則、pack 的 token 上限；真實：Q2、Q3、T1–T3 各 1 次 | 半天 |
| 3 | 方案 C：事實＋最小列取代表格 chunk，同來源編號 | prompting.py、service.py | 單元：引用編號與頁碼追溯；真實同上 | 半天 |
| 4 | §6 摘要重寫一次＋全稱檢查＋驗證註記進 Q1 prompt | summarization/service.py、prompting.py | 整合：CONTRADICTED 觸發重寫、第二次仍錯則保留；真實：重建摘要樹、Q1 × 3 | 半天到一天 |
| 5 | `differences`／`rank`／`filter` 與 `confidence` 欄位 | evidence.py | 單元 | 2 小時 |
| 6 | 泛化：第三份文件與標準答案、不支援形狀的拒算測試 | evaluation/ground-truth | 腳本 | 半天 |

---

## 最後的直接回答

1. **能否改善 Q1、Q2、Q3 的核心錯誤？** Q2、Q3：有合理機會，因為 C9 固定後剩的錯正是「例外沒點名」「四版本數字沒給」，而工具結果就是這兩樣（97 與 420 tokens 實測）；但這是待實驗的假設，D76 的事實從未在真實批次測過。Q1：只有 §6 的摘要階段改動能碰到，回答端任何方案都不行（15 次證據）。
2. **10K 會不會不足？** 完整 JSON 會（11,681 tokens 實測）；事實清單不會（97–438）；方案 C 反而把 Q2 的輸入從約 2,950 降到約 2,000。
3. **要不要把原 RAG context 與表格資料全給？** 不要。navigate 已經是「chunk＋矩陣」兩份，沒有比 single 好，還因重複值錯了 T3。
4. **能否避免重複並降 token？** 能：事實取代表格 chunk（方案 C／D），估算每題省約 950 tokens，重複比例歸零；待實測。
5. **最值得優先的最小方案？** 序 1→2→4：temperature 0 預設；重啟比較事實進 prompt 並補「問到的列」渲染（Q2、Q3）；摘要階段帶反例重寫一次（Q1）。三者合計約一天半，不新增回答時的 LLM 呼叫、不新增資料表。
6. **有沒有更簡單的替代？** 有，就是序 1 與 2 的最小版：一行設定加一行 `facts=facts`（B5 時停用的那一行），先測一批再決定要不要做 C、D 與完整 schema。完整的 Universal Table Store 與 Agent Tool Calling 在剩餘時程內不建議，且與「回答不加第三次呼叫」衝突。

## 事實、推測、假設的區分

- 已確認：§1 全部、§3.1、§3.2 的實測行、BS-T3 與 B9-Q2-2 的重複致錯、C9 的三種殘餘錯誤、Q1 在回答端不可修。
- 合理推測：§3.2 的估算行、方案 C 的省 token 量、工具結果能補 Q2／Q3 缺的內容。
- 待實驗：B／C／D 的正確率、§6 對 Q1 的效果、泛化到第三份文件。
