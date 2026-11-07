# D87 兩階段 A/B 實驗：比較事實注入（Q2、Q3）與摘要證據導向重寫（Q1）

使用者任務書「RAG 表格推理與摘要驗證改善 — 兩階段 A/B 實驗」（2026-11-07）的實測紀錄。
任務書原文在決策日誌 D87；可行性分析在 ADR 0012。本資料夾：

- `runs/`：每次回答一個 JSON（與 `navigator-abc/` 同格式），檔名 `{組}-{題}-{次}.json`；`{組}-summaries.json` 是該次入庫的摘要核對（B 組含 `repairs`）。
- `judge.py`：機械判定（逐格核對答案中的表格數字、全稱用語、Q2 是否點名 Mix 三個例外、Q3 是否有定義與 LightRAG 自身數字），產生 `analysis.json` 與 `answers.md`（36 份答案全文）。通過與否由人判（標準同 `ground-truth/key-facts.md`）。

## 設定（所有組共同）

| 項 | 值 |
|---|---|
| 模型 | qwen3:32b（回答 `ANSWER_TEMPERATURE=0`）；bge-m3 |
| 模式 | single（Top-5、門檻 0.50、chunk 400／80、區塊向量） |
| 每組 | Q2、Q3 各 6 次（A）；Q1 共 6 次＝3 次入庫 × 2 次回答（B，摘要本身有隨機性，所以分三次入庫） |
| 判定 | 人工（key-facts 標準）＋ `judge.py` 機械項 |

## 實驗 A：Query-time Evidence Injection

| 組 | `ANSWER_FACTS` | 進 prompt 的東西 |
|---|---|---|
| A0 | off | 原本的 chunk（表格 chunk 是逐列改寫文字） |
| A1 | inject | A0 ＋ 程式算好的比較事實（每對「x 格高、y 格低、例外：…（±pp，相對 %）」，預算 500 tokens） |
| A2 | replace | 被矩陣覆蓋的表格 chunk 換成只含問題點名欄位的最小表；比較事實照 A1 注入 |

### 執行紀錄

- A0、A1 各 Q2 × 6、Q3 × 6（A1 的 Q3 跑到第 4 次時停止）；A2 各 1 次。A0 用時 556 秒含入庫。A0 的六次回答一字不差；A1 的 Q2 六次一字不差，Q3 出現兩種輸出（第 1 次，與第 2–4 次）。**temperature 0 在 Ollama 上接近但不是完全可重現**。
- 使用者看到 A0 六次相同後指示「那目前都測試一次就好」：A2 與其後的 B、C 組每組只跑一次。

### 機械判定（`judge.py`；數字逐格對 `ground-truth/paper-structure.json`，程式附加的註記不算模型文字）

| 記錄 | 回答 prompt＋completion | 表格數字 | 標籤核對報錯 | 全稱用語 | Q2：點名 Mix 三例外 ／ Q3：定義、自身數字、變體數字 | 程式判定 |
|---|---|---|---|---|---|---|
| A0-Q2（×6 相同） | 3,267＋279 | 16 | 0 | consistently | 0/3 | FACTUALLY_INCORRECT |
| A0-Q3（×6 相同） | 3,697＋342 | 0 | 0 | all datasets | 定義 3/3、自身 0、變體 0 | FACTUALLY_CORRECT_BUT_INCOMPLETE |
| A1-Q2（×6 相同） | 3,775＋301 | 14 | 4（全誤報） | consistently, only exception | 3/3 | FACTUALLY_INCORRECT |
| A1-Q3-1 | 4,245＋794 | 16 | 0 | in all | 定義 3/3、自身 7、變體 9 | FACTUALLY_CORRECT_BUT_INCOMPLETE |
| A1-Q3-2／3／4（相同） | 4,245＋944 | 26 | 7（全誤報） | consistently, in all, only exception | 定義 3/3、自身 11、變體 15 | FACTUALLY_INCORRECT |
| A2-Q2-1 | 2,698＋579 | 22 | 0 | consistently, in all | 3/3 | UNCERTAIN（只有 pp 差值無法核對） |
| A2-Q3-1 | 3,182＋678 | 16 | 8（全誤報） | in all, only exception | 定義 2/3（誤判：只是提到 high-level／low-level）、自身 7、變體 9 | FACTUALLY_INCORRECT |

### 人工判定（key-facts 標準）

| 記錄 | 判定 | 原因 |
|---|---|---|
| A0-Q2 | 不通過 | 16 個數字全對（只列 LightRAG 一側），但「LightRAG consistently outperforms GraphRAG across multiple datasets and evaluation dimensions」是全稱句，且沒有點出 Mix 的三個例外（Comprehensiveness 49.6<50.4、Empowerment 49.2<50.8、Overall 49.6<50.4）。與 C9 同型。 |
| A0-Q3 | 不通過 | -High／-Low／-Origin 的定義與觀察（A1–A5）全對，但整篇沒有一個 Table 2 數字（A6 缺）；「across nearly all datasets and metrics」是引述原文。與 C9 同型。 |
| A1-Q2 | **通過** | 14 個數字全對，含三個例外的成對數字；「Across 16 conditions, LightRAG is higher in 13 and lower in 3」對；三個 Mix 例外全部點名。「consistently outperforms GraphRAG in most conditions」措辭矛盾但有「in most」限定且例外列出。「GraphRAG shows a trend of outperforming NaiveRAG in 15 of 16」是跨區塊的間接比較，答案照事實塊的規定寫成 trend，數字（23.6 vs 22.8、29.2 vs 22.8）對。 |
| A1-Q3-1 | 不通過（差一步） | 16 個數字全對，每個變體對 LightRAG 的「x of 16」與例外清單全對（含 -Low 的 11/3/2 平手、-Origin 的 11/4/1 平手）；定義與觀察全對。未達 A6：沒有任何一個「同一資料集、同一指標」把四個版本的數字並列。 |
| A1-Q3-2／3／4 | 不通過 | 26 個數字全對、例外清單全對；但 **-Origin 的定義寫反**（「using original text instead of graph-based indexing」，正確是去掉原文）；「consistently outperformed … in most conditions」矛盾措辭；同樣未達 A6。 |
| A2-Q2-1 | **通過** | 22 個數字全對，四個指標逐一說明哪三個資料集贏、Mix 哪裡輸，三個例外附成對數字與 pp；「Diversity … in all datasets」對（四個都贏）。prompt 反而比 A0 少 569 tokens，因為 Table 1 被縮成只剩 GraphRAG 那一區塊。程式判定 UNCERTAIN（沒有誤報，因為答案寫的是直接配對）。 |
| A2-Q3-1 | 不通過 | 16 個數字全對、三個變體的計數與例外全對；但 **整篇沒有變體的定義與 4.3 節的觀察**（A1–A5 全缺），只剩數字與計數；A6 也未達。原因見下。 |

### 要誠實說的

- **有幫助的部分（實測）**：把程式算好的「x 格高、y 格低、例外是哪幾格（±pp）」放進 prompt 後，Q2 的結論從「consistently、沒有例外」變成「13 of 16、三個例外全點名」，六次都如此；Q3 從「沒有數字」變成「每個變體對 LightRAG 的計數與例外全對」。這是 D74 以來第一次 Q2 在 single 模式通過。
- **沒有解決的部分（實測）**：模型仍愛用「consistently」這個字（即使後面接「in most conditions」）；Q3 的 A6（同一條件四版本並列）沒有出現，因為事實塊是以「配對」組織的，模型就照配對寫；A1-Q3 第 2–4 次把 -Origin 的定義寫反，與數字無關，是模型讀 4.3 節的錯。
- **核對器誤報（程式碼可證）**：A1 的 11 條「標籤不符」全是誤報。原因：答案寫「LightRAG (62.0%) vs -High (63.2%)」，標籤核對把 `vs` 後的方法當成表格的配對對象，而 Table 2 把兩者都配 NaiveRAG。事實塊鼓勵的正是這種間接比較，所以 A1 的 `analysis_status` 一律被標成 FACTUALLY_INCORRECT——**開啟 inject 的同時，標籤核對的配對條件要放寬，否則 UI 會把正確答案標成錯**。另外「16、13、15」等計數被列為「無法核對的數字」，因為它們不在原文裡，是事實塊算出來的。
- **A2（replace）在 Q3 上有設計缺陷（程式碼可證）**：最小表只保留「問題點名的欄位」。Q3 的問題「Performance of ablated versions of LightRAG」只點名 LightRAG，沒有 -High／-Low／-Origin，所以 Table 2 被縮成只剩 LightRAG 對 NaiveRAG 那一區塊（見 `A2-Q3-1.json` 的 sources[1]），三個變體的列從 prompt 消失，模型只剩事實塊可依。4.3 節的定義 chunk 其實還在 sources[6]，但模型這次完全沒用它。對 Q2（問題點名兩個方法）replace 沒有這個問題，而且省 569 tokens。
- **代價（實測）**：A1 的 Q2 prompt 多 508 tokens、Q3 多 548；完成 tokens Q3 從 342 增至 794–944；A2 的 Q2 prompt 少 569、Q3 少 515；回答時間相近；呼叫數不變（1 次）。
- **A 的結論**：採 A1（inject）進 2×2。A2 對 Q2 等效且更省，但對沒點名變體的問題會丟掉表格的列，不能作為預設。

## 實驗 B：Ingestion-time Summary Repair

（待填）

## 2×2 整合與回歸

（待填）

## 任務書的十個問題

（待填）
