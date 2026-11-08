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

| 組 | `SUMMARY_REPAIR` | 行為 |
|---|---|---|
| B0 | false | D76：摘要核對出矛盾只標記，不改 |
| B1 | true | 矛盾時給模型表格的真實數字重寫一次，再核對；仍矛盾的句子刪除；紀錄在 `summaries.verification.repair` |

每組一次入庫（LightRAG 與 GraphRAG 兩篇都重新摘要）＋ Q1 一次。摘要本身不是 temperature 0，所以兩組的摘要文字不同，比較的是「核對→修復」這段機制，不是通過率。

### B0（基線，16:06–16:13）

- Q1 回答（prompt 3,865、completion 449）：S1–S5 都有；數字 83.6%（Legal／Comprehensiveness 對 NaiveRAG）、52.8%（Legal／Overall 對 GraphRAG）、610,000、100、1,399 × 2 × 5,000、600,000–5,000,000 全部對；「in most evaluation dimensions」沒有全稱錯。**人工判定通過**（S3 只說「dual-level」，沒有展開低層＝實體關係、高層＝主題，算弱項）。
- 這次入庫的摘要核對：EVALUATION 與全文摘要被標 CONTRADICTED，矛盾數字 52.8%。**這是誤報**：摘要句「It also outperforms GraphRAG in most cases, particularly in the Legal dataset, where it achieves a 52.8% win rate in the Overall dimension (p. 7)」是對的（Table 1 第 7 頁：GraphRAG 47.2%、LightRAG 52.8%）；標籤核對把離數字最近的方法名「GraphRAG」當成歸屬，而句子的主詞是「it」（LightRAG）。離線重現：`verify_numbers` 對這一句回報 mislabelled 52.8%（answer: Overall, Legal, GraphRAG；source: LightRAG vs GraphRAG）。
- 影響：**B1 的修復是否觸發，取決於核對器的精確度**。這次入庫若開 B1，會被誤報觸發；重寫後再核對若仍誤報，正確的句子會被刪掉。B1 的結果要對照這一點看。

### B1（修復開，16:13–16:21）

這次入庫的摘要與 B0 不同（摘要不是 temperature 0）。觸發兩次修復，一真一假：

| 摘要 | 觸發句 | 真錯？ | 修復結果 |
|---|---|---|---|
| EVALUATION | 「In Diversity, LightRAG outperforms HyDE by 76.0% in the Legal dataset.」 | **真錯**：76.0% 是 Agriculture／Diversity 對 HyDE；Legal／Diversity 對 HyDE 是 80.0% | 證據列出 Legal／Diversity 整列（HyDE 20.0%、LightRAG 80.0% …）；模型重寫後出現 80.0%，再核對從 CONTRADICTED 變 UNCERTAIN（80.0% 標籤未完全解析，但不再矛盾）。**修對了。** |
| document | 「It also outperforms GraphRAG in most cases, achieving 51.6% win rate in Comprehensiveness in the Legal dataset versus 48.4% for GraphRAG.」 | **假錯（誤報）**：Legal／Comprehensiveness 的 GraphRAG 區塊正是 GraphRAG 48.4%、LightRAG 51.6%；核對器把最近的方法名 GraphRAG 當歸屬 | 模型改寫成「in the CS dataset」（CS 那格也恰是 48.4／51.6，仍對），再核對仍誤報，**正確的句子被刪除**。 |

- 證據品質（程式碼可證）：第二條的「Differences」把 GraphRAG 48.4% 與 NaiveRAG、RQ-RAG、HyDE 等不同配對的數字相減（+195.1% relative 之類），是把被誤判的方法當成錨點造成的噪音；真錯那條沒有 Differences 行，因為摘要給的標籤裡沒有任何一個欄名能當錨點。
- Q1 回答（prompt 3,807、completion 399）：S1–S5 都有（這次 S3 有展開低層實體關係／高層主題）；83.6% 對 16.4% 對；UltraDomain 18 個領域、428 本教科書對；「in most datasets and evaluation dimensions」無全稱錯。**人工判定通過。** 兩次修復的句子都沒進入 Q1 的回答，所以這次 Q1 的通過與修復無關。
- **B 的結論（實測一次）**：機制如設計運作——觸發、給可追溯證據、重寫、再核對、刪句，每步都有紀錄；但它的價值完全受限於核對器：一次真錯修好，一次誤報刪掉正確句。在標籤核對的「最近方法名」誤報修好之前，B1 不應預設開啟。

## 2×2 整合與回歸

| | 摘要修正關 | 摘要修正開 |
|---|---|---|
| 事實注入關 | C0 ＝ A0（Q2、Q3）＋ B0（Q1） | C2 ＝ B1（Q1）；Q2、Q3 不受摘要影響，同 A0 |
| 事實注入開（inject） | C1 | C3 |

C1、C3 用的事實塊說明比 A1 多一句（16:19 改，使用者核准：「好可以修改prompt在測試一次Q3 順便測試Q2是否受影響」）：
「These facts cover only the figures: what each method or variant is and what the authors observe about them are in the text passages among the sources — state those from the passages, citing them.」

### C1n（inject ＋ 新句，修復關，16:21–16:31；新句已退回，記錄改名 C1n）

| 題 | 機械判定 | 人工判定 | 原因 |
|---|---|---|---|
| Q1 | 2 個表格數字全對；無矛盾摘要 | **不通過** | 「Across all datasets, LightRAG maintains win rates above 60% in all evaluation metrics」是錯的（對 GraphRAG 的 Mix 三格是 49.6／49.2／49.6，CS 的 Comprehensiveness 51.6）。這句**來自 EVALUATION 章節摘要**（「win rates above 60% in all metrics (p. 6)」），回答照抄。摘要核對沒抓到：60% 不是表格值，全稱檢查只看「某方法全贏」的句型，不看「門檻式」的句子。B1 在這裡也不會觸發。**Q1 摘要層的第三種錯型**（前兩種：數字歸錯對象、全稱優勢句）。 |
| Q2 | 8 個數字、3 條標籤報錯（1 真 2 誤報）、Mix 三例外 3/3 | **不通過** | 13／3 計數與三個例外都對；新句的效果出現了（最後一段引用 4.2 節講雙層檢索）。但多了一句錯的：「In the Agriculture dataset, GraphRAG shows a slight advantage in Diversity (22.8% vs 23.6%) when compared indirectly」——22.8% 是 GraphRAG、23.6% 是 NaiveRAG（各自對 LightRAG），方向也反（22.8 < 23.6）。A1 把同一條間接事實寫對了（「GraphRAG 對 NaiveRAG 15 of 16，例外 Agriculture／Diversity 23.6 vs 22.8」）。標籤核對這次對 23.6% 的報錯是**真報**。回答短了（229 tokens 對 A1 的 301）。 |
| Q3 | 26 個數字全對；22 條標籤報錯全誤報；定義 0/3 | **不通過** | 數字、計數、例外全對，與 A1 同；但**整篇沒有任何變體的定義與 4.3 節觀察**——比 A1（有定義）更差，新句要的效果完全沒出現。A6 仍未達。 |

- **新句的實測結果是負的**：Q3 的定義不但沒穩定出現反而消失，Q2 多了一句錯的間接比較，Q1 的錯與新句無關（inject 在摘要路線沒有事實可注入，`facts: None`）。單次、temperature 0；A1 與 C1 的差別只有這一句（prompt 多 38 tokens）。
- **核對器**：Q3 的 22 條標籤報錯全是「vs 後的方法被當成配對對象」的誤報（同 A1）；Q2 的 3 條裡 1 條是真的。

### C3n（inject ＋ 新句，修復開，16:31–16:41；記錄改名 C3n）

- Q2、Q3 的回答與 C1n **一字不差**（同 prompt、temperature 0、證據全是原文 chunk）：實測確認摘要修復不影響 Q2、Q3。
- Q1（prompt 3,538、completion 641）：S1–S5 都有（S3 展開低層／高層）；數字 83.6%／86.4%／83.6%（Legal 對 NaiveRAG 三格）、-High 65.2%、-Low 64.0%（Agriculture／Comprehensiveness）、100、610,000、600,000–5,000,000 全對；「across most datasets and dimensions」無全稱錯。**人工判定通過。**
- 這次入庫的修復：EVALUATION 摘要寫「LightRAG surpasses GraphRAG in all four dimensions on the Legal dataset, achieving 54.4% in Comprehensiveness and 77.2% in Diversity」——54.4%、77.2% 是 **Agriculture** 對 GraphRAG 的數字（Legal 是 51.6%、73.6%），**真錯**。修復證據列出 Legal 整列，模型重寫後再核對 **VERIFIED**，沒有刪句。這是 B1 機制第二次修對真錯、且第一次達到 VERIFIED。全文摘要沒被觸發。
- 2×2 中「注入開＋修復開」這格沒有互相干擾：Q1 走摘要路線，inject 無事實可注入（`facts: None`）；修復只動摘要。

## F1：核對器修正後的完整測試（17:56–18:05 之前；inject＋修復開，Q1–Q3 各一次，commit `d14229e`）

| 題 | 正式判定 | 寬標準 | 程式判定 | 說明 |
|---|---|---|---|---|
| Q1 | **通過** | 通過 | UNCERTAIN | S1–S5 都有；83.6% 對 16.4%、100、610,000 全對；「consistently outperforms … in most cases」有限定。這次入庫 EVALUATION 摘要有**真錯**：「LightRAG 67.6% comprehensiveness in Agriculture versus 34.8% for the -High variant」——34.8% 是 -High 區塊裡 **NaiveRAG** 的數字（-High 是 65.2%），**正是任務書點名的錯型（把基準的數字當成變體的）**；同一摘要還有一句被表格反證的全稱句。修復：重寫一次仍矛盾 → 該句刪除 → 再核對 VERIFIED。刪掉的句子確實是錯的。 |
| Q2 | **通過** | 通過 | FACTUALLY_INCORRECT | 回答與 A1 一字不差（14 個數字、13／3、三個例外全對）。程式仍標 6 條標籤不符，**全是誤報**，是第三種句型：「GraphRAG performs better … Comprehensiveness (50.4% vs 49.6%)」只點名一個方法，括號裡第二個數字是對方的，核對器把它也歸給 GraphRAG；「(23.6% vs 22.8%)」兩個方法都點名但數字順序是「贏者 vs 輸者」，核對器照主詞順序配。 |
| Q3 | 不通過（A6） | 通過 | FACTUALLY_CORRECT_BUT_INCOMPLETE | 與 A1-Q3-1 一字不差：16 個數字、計數、例外、三個定義（-Origin 這次對）全對；標籤誤報 0（第二種句型已修）；缺四版本並列。 |

核對器第一、二種誤報（比較動詞、間接比較）在 F1 沒再出現；第三種（括號成對數字）接著修。

## R1：題庫其餘 16 題的回歸（inject＋修復開，各一次，commit `b8d95ea`，18:04–18:19）

對照 D85 的 single 基線（`retrieval-parameters/README.md`）：

| 題型 | 題 | D85 single | R1 | 說明 |
|---|---|---|---|---|
| 細節 | D1–D4 | ✓✓✓✓ | ✓✓✓✓ | 事實塊為空（`facts: 0`），prompt 2,000–2,400 |
| GraphRAG | G1、G3、G4 | ✓✓✓ | ✓✓✓ | — |
| GraphRAG | G2 | ✗ | **✓** | 77.76 對 22.24、79.2 對 20.8、p<0.001 全對。Table 6 仍無矩陣（`facts: 0`），這次是模型自己讀對（temperature 0；D85 是預設溫度），不能歸功於注入 |
| 表格數字 | T1、T2 | ✓✓ | ✓✓ | T2 注入 224 條事實，prompt 5,533（問題點名兩個方法，事實塊把 16 個條件全給了） |
| 表格數字 | T3 | ✓ | **✗** | 答 40.4／59.6（Mix／Comprehensiveness），應為 44.0／56.0（CS／Overall）。注入 176 條事實（-High 對 NaiveRAG 的全部條件），模型取錯條件。**標籤核對抓到了**（FACTUALLY_INCORRECT，註記列出正確標籤），但回答本身錯。單次，無法排除噪音；但 D85 同題 single 答對，而本次 prompt 多了 176 條只差資料集與指標的事實行，是合理的可疑原因 |
| 跨文件 | X1 | ✗ | ✗ | 同 D85：第二篇的 gpt-4-turbo 句排不進前五（檢索名額） |
| 跨文件 | X2 | ✓ | ✓ | 引述論文「each in the region of 1 million tokens」與 Table 4 四個數字 |
| 無答案 | N1–N3 | ✓✓✓ | ✓✓✓ | 零次模型呼叫 |
| 合計（13 題可答） | | 10 | 11 | G2 得、T3 失 |

- **要改的（進泛化第 2 項）**：`comparison_facts` 只依問題點名的**方法**過濾；問題同時點名資料集或指標時（T3：「CS」「Overall」），應把事實縮到那個條件。這不寫死名稱——用問題字面比對表格的群組與列標籤，與現在比對欄名的做法相同。縮完 T3 的事實是 1 條而不是 176 條，prompt 也會從 5,201 回到 2,000 左右。
- 非表格題、拒答題沒有退步；注入對它們是空操作。

## V1：泛化後的驗證批次（commit `bcaf07d`，18:45–17:45 記錄時間；inject＋修復開，各一次）

| 題 | 判定 | 說明 |
|---|---|---|
| G1 | ✓ | Table 2 的四組數字全對；問題點名 C0、TS → 注入 28 條「same row」事實（新形狀的多欄列） |
| G2 | ✓ | 77.76／22.24、79.2／20.8、Z 與 p 全對；Table 6 沒有配對事實（`facts: 0`），模型自己讀對 |
| G3 | **✗** | 「564 個節點」，應為 8,564。**成因是切塊器**：「8,564」被切成上一塊結尾的「8」與下一塊開頭的「,564」；R1 時含完整數字的另一塊也在前五名，這次沒進（GraphRAG 的 chunk 集合因表格改寫而變動），模型只看到「,564」。數字核對把 564 標為無法核對。修法：切塊邊界不落在字或數字中間（`chunking.py` `_splits_a_word`，已修，待 V2 確認） |
| G4 | ✓ | 六個條件的定義全對 |
| T3 | **✓**（R1 ✗） | 44.0／56.0 對。事實從 176 條縮到 44 條（「Overall」列有被比對；「CS」兩個字母原本不比對，已放寬為全大寫兩字母可比對，待 V2 看是否縮到 10 條以內） |
| Q2 | ✓ | 與 F1 同（一個代表數字換成 Legal／Diversity 73.6 對 26.4，對） |
| Q3 | 不通過（A6）／寬標準通過 | 與 F1 一字不差 |

LightRAG 的兩題在新入庫下沒有變化；GraphRAG 四題 3 對 1 錯，錯的那題是切塊問題不是表格問題。

### V2（commit `4df38d0`，切塊邊界修正後；G3、T3 各一次）

| 題 | 判定 | 說明 |
|---|---|---|
| G3 | **✓** | 8,564／20,691／15,754／19,520 全對；來源塊現在以「8,564 nodes」完整開頭 |
| T3 | ✓ | 44.0／56.0；事實 176（R1）→ 44（V1）→ **11**（「CS」兩字母大寫標籤可比對後，縮到 CS／Overall 一個條件） |

至此 D85 的 19 題在 inject＋修復開啟下：Q1、Q2 過，Q3 正式標準差 A6，D1–D4、T1–T3、G1–G4、X2 過，X1 仍錯（跨文件檢索名額），N1–N3 拒答。可答的 16 題對 14 題；D85 基線是 14/19 含 Q 題 0/3。

## 寬標準的判定（使用者 16:40：「如果寬標準 (錯誤資訊除外) 但全部等等論文提到的 是可以接受的」）

寬標準＝回答裡沒有錯誤資訊，且內容都出自論文；不要求 key-facts 的每一項都到齊。正式判定仍是 key-facts 標準（A6 維持，D87）。

| 記錄 | 正式（key-facts） | 寬標準 | 寬標準不過的原因 |
|---|---|---|---|
| A0-Q2 | 不通過 | **不通過** | 「consistently outperforms … across multiple datasets and evaluation dimensions」在 Mix 三格不成立，是錯誤資訊 |
| A0-Q3 | 不通過 | 通過 | 定義與觀察全對、無數字；沒有錯 |
| A1-Q2 | 通過 | 通過 | — |
| A1-Q3-1 | 不通過 | 通過 | 定義、數字、計數全對；只差 A6 的並列 |
| A1-Q3-2／3／4 | 不通過 | **不通過** | -Origin 定義寫反 |
| A2-Q2 | 通過 | 通過 | — |
| A2-Q3 | 不通過 | 通過（薄） | 數字全對、無錯；但沒有定義與觀察，只回答了「數字如何」 |
| B0-Q1 | 通過 | 通過 | — |
| B1-Q1 | 通過 | 通過 | — |
| C1n-Q1 | 不通過 | **不通過** | 「above 60% in all metrics」錯 |
| C1n-Q2 | 不通過 | **不通過** | Agriculture／Diversity 那句方向與對象都錯 |
| C1n-Q3 | 不通過 | 通過（薄） | 數字全對、無錯；沒有定義 |

寬標準下：Q1 2/3、Q2 2/4、Q3 4/7（其中 2 份只有數字）。錯誤資訊的來源全部是三種：全稱句（A0-Q2）、定義讀反（A1-Q3 ×3）、摘要層門檻句（C1n-Q1）、間接比較寫反（C1n-Q2）。

## 成本（實測；每格 n 次平均）

| 組-題 | n | prompt | completion | 秒 | 回答呼叫 |
|---|---|---|---|---|---|
| A0-Q2 | 6 | 3,267 | 279 | 12.5 | 1 |
| A1-Q2 | 6 | 3,775 | 301 | 13.6 | 1 |
| A2-Q2 | 1 | 2,698 | 579 | 26.9 | 1 |
| A0-Q3 | 6 | 3,697 | 342 | 15.4 | 1 |
| A1-Q3 | 4 | 4,245 | 906 | 39.4 | 1 |
| A2-Q3 | 1 | 3,182 | 678 | 31.4 | 1 |
| B0-Q1 | 1 | 3,865 | 449 | 24.4 | 1 |
| B1-Q1 | 1 | 3,807 | 399 | 22.2 | 1 |
| C1n-Q1／Q2／Q3 | 1 | 3,287／3,813／4,283 | 420／229／842 | 22.5／13.7／39.7 | 1 |
| C3n-Q1／Q2／Q3 | 1 | 3,538／3,813／4,283 | 641／229／842 | 32.0／13.7／39.7 | 1 |

入庫（兩篇論文的索引＋摘要，含 1 次 Q1 回答）：B0 438 秒、B1 436 秒（多 2 次修復呼叫）；C1n 448 秒、C3n 508 秒（多 1 次修復呼叫，三題回答）。修復呼叫每次 prompt 約 1,500–2,500 tokens（摘要＋證據＋節錄），每篇論文 0–2 次。所有呼叫 prompt＋completion ≤ 10,000（帳本）。

## 任務書的十個問題

標記：**實測**＝本資料夾的記錄；**程式碼**＝可在程式碼中查證；**推測**＝尚待驗證。

1. **加入 comparison_facts 後，Q2、Q3 的通過率是否提高？**
   實測：Q2 從 0/6（A0）到 6/6（A1）、1/1（A2），正式標準通過。Q3 正式標準 0→0（A6 的四版本並列沒有出現）；但數字層從「0 個數字」變成「16–26 個數字全對、三個變體的勝負計數與例外清單全對」；寬標準下 A1 四次中 1 次通過（其餘三次敗在 -Origin 定義寫反）。temperature 0 下六次重複幾乎相同，所以 6/6 的證據力接近 1/1。
2. **LLM 是否仍會忽略已提供的例外事實？**
   實測：沒有。A1、A2、C1n 的 Q2 全部點名三個 Mix 例外並附成對數字；Q3 的例外清單（1＋3＋4 格）全部列出。但它仍愛用「consistently」這個字，接「in most conditions」。另一方向的問題出現了：間接比較的事實（各自對 LightRAG 的趨勢）在 C1n 被寫反方向一次。
3. **Evidence Replacement 是否比單純 Facts Injection 更有效？**
   實測：Q2 等效（都通過），A2 省 1,077 tokens；Q3 A2 更差——問題沒點名變體，最小表只留 LightRAG 欄，三個變體的列從 prompt 消失，定義與觀察也沒寫。程式碼：`named_columns` 以問題字面比對欄名，這是 replace 的結構性限制，不寫死名稱就無法知道「ablated versions」指哪幾欄。結論：inject 作為可用版本，replace 不作預設。
4. **Query Input Tokens 是否真的降低？**
   實測：inject 增加（Q2 +508、Q3 +548）；replace 降低（Q2 −569、Q3 −515，相對 A0）。任務書預估的「約 2,000 tokens」沒有達到：A2-Q2 是 2,698，因為非表格 chunk（4.2 節、4.5 節）仍在。
5. **Q1 的 22.0% 錯誤是否能在摘要建立階段被正確辨識並修復？**
   實測：這次四次入庫（B0、B1、C1n、C3n）都沒有再出現 22.0% 那個錯；出現的是同類型的錯——數字歸到錯的資料集（B1：76.0% 應為 80.0%；C3n：54.4%／77.2% 是 Agriculture 的，寫成 Legal）。B1 機制對這兩條**都辨識並修復**（一次到 UNCERTAIN、一次到 VERIFIED），證據包含該條件整列數字；22.0% 那條屬於同一類（數字存在但歸屬錯誤），程式碼上走同一路徑，但**沒有實測到它本身**。任務書要求區分的六種錯型中，目前核對器能分辨「數字不存在」「歸屬錯誤」「被表格反證的全稱句」三種；「比較基準錯誤」「差值計算錯誤」「百分比／百分點混淆」沒有獨立的偵測。
6. **Summary Repair 是否產生新的錯誤或誤報？**
   實測：有一次誤報造成傷害——B1 的全文摘要「Legal／Comprehensiveness 51.6% 對 GraphRAG 48.4%」本來是對的，標籤核對把句中最近的方法名當歸屬而報矛盾，模型改寫後仍被誤報，正確的句子被刪除。三次觸發（B1 兩次、C3n 一次）：2 真 1 假。誤報根源與 A1 的 11 條、C1n 的 22 條標籤誤報相同（最近方法名／vs 後的方法被當配對對象）。
7. **是否增加了過多 Ingestion 成本？**
   實測：每篇論文 0–2 次修復呼叫，入庫總時間差在量測噪音內（B0 438 秒、B1 436 秒；C1n 448、C3n 508）。不多。
8. **目前解析器對不同表格的既有限制是否仍然存在？**
   實測（18:40 更新）：原本存在而且比想像嚴重——GraphRAG 四張表矩陣全為 0 格，只有「每群兩子欄」的形狀被逐列改寫。使用者判定這是過擬合、要求泛化；改寫後兩篇六表與 LaTeX 原始檔逐格全符（`evaluation/table-generalization/`）。仍不支援：合併儲存格、三層以上欄頭、無標題表、跨頁表、圖片表；多欄列的比較事實只在問題點名欄位時產生。驗證範圍是五種形狀，不是任意表格。
9. **最終應該採用哪一組配置作為預設？**
   實測＋推測：`ANSWER_FACTS=inject` 可以開（Q2 由 0 變通過、Q3 數字全對、無已知傷害）。開之前要先修標籤核對的配對條件——**已修（`d14229e` 與後續）**：三種誤報句型修正後，A1／F1 的 Q2、Q3 標籤報錯歸零，標註集的精確率與召回率不變。`SUMMARY_REPAIR`：四次觸發裡三次修對真錯（76.0%、54.4%／77.2%、34.8%——最後一條是任務書點名的「基準數字當變體」錯型），一次因誤報刪掉正確句子（51.6%，已修的句型）；核對器修好後可開。兩者預設值的切換（`.env.sample`）留給使用者決定，本輪沒改。
10. **還有哪些改善值得留到 Future Work？**
   - 標籤核對：以句子主詞／動詞方向判斷歸屬，而不是最近的方法名；配對條件接受「各自對同一基準」的間接比較。
   - 事實塊加一行「同一條件四版本數字」（A6 需要；程式從矩陣算，不寫死名稱）。
   - 摘要層的「門檻式全稱句」（「above 60% in all metrics」）目前沒有檢查。
   - -Origin 定義讀反這類文字層錯誤沒有程式方法擋。
   - replace 模式要能把「一群方法」對應到欄名才可用。
   - 泛化（已做五種形狀）：下一步是第三篇論文的表格與合併儲存格；Table 6 類「Mean 1 對 Mean 2」的同列異名欄配對。
   - R1 回歸已跑（inject 開）：13 題可答 11 對，T3 的退步由事實縮到點名條件修正（待 V1 確認）。

### 正式 2×2（Q1；Q2、Q3 不受摘要修復影響，見 C3n）

| | 修復關 | 修復開 |
|---|---|---|
| 注入關 | B0-Q1 通過 | B1-Q1 通過（修 1 真錯、刪 1 正確句） |
| 注入開 | C1-Q1 通過 | C3-Q1 通過（無矛盾摘要，修復未觸發） |

- C1-Q1（16:38–16:45；prompt 3,654、completion 650）：S1–S5 都有；Legal 83.6／86.4／83.6、Agriculture 67.6／76.4／67.6、Overall Legal 52.8 對 GraphRAG 47.2 全對；附錄案例「LightRAG 對 NaiveRAG」對（Table 5，第 16 頁）。程式標 47.2% 標籤不符是**誤報**（「versus 47.2% for GraphRAG」把 GraphRAG 同時當主人與比較對象）；這次入庫的全文摘要也被同一誤報標 CONTRADICTED。inject 在摘要路線無事實可注入（`facts: None`）。
- C3-Q1（16:45–16:53；prompt 3,585、completion 667）：S1–S5 都有；83.6／86.4、100、610,000、1,399 × 2 × 5,000 全對；「outperforms existing RAG methods in all four evaluation dimensions」是對四個維度的總述，不是「每格全贏」，判通過但註記。這次入庫 20 份摘要沒有一份 CONTRADICTED，修復沒有觸發，等同基線。
- 2×2 結論（實測各一次）：Q1 四格都通過；Q2、Q3 只受注入影響（C3n 的 Q2、Q3 與 C1n 一字不差）；兩個開關同時開沒有互相干擾、沒有重複 context（Q1 路線不含表格 chunk，事實塊不會出現）。

## 核對器修正（D87 後續，使用者 16:45：「好 先修核對器 然後修復完 在幫我測試一次完整的Q1 Q2 Q3」）

兩個誤報根源，`app/chat/verification.py`：

1. **比較動詞不在比較詞清單**：「It also outperforms GraphRAG … 52.8%」把 GraphRAG 當數字的主人。加入 outperform／surpass／exceed／beat／ahead of／behind／trail／lag（及 高於／低於／超過／領先／落後）為比較詞，其後的方法成為比較對象；主詞「it」未命名時結果是 unresolved（missing），不再是 contradicted。
2. **間接比較被當成配對錯誤**：「LightRAG (62.0%) is lower than -High (63.2%)」要求格子的配對對象＝句子的比較對象，而 Table 2 把兩者各自配 NaiveRAG。新規則（`_Pairing`）：句子**同時列出兩個表格數字**、且表格**沒有**該方法與該比較對象的直接配對、而比較對象在同一條件有自己的格子時，接受為間接比較；表格有直接配對時（Table 1 的 LightRAG 對 GraphRAG）仍要求數字來自該配對（B5 那種拿錯區塊的錯照抓）；只有一個數字的「67.6% against -High」仍視為宣稱配對、照抓。
3. **括號成對數字**（F1 之後補）：「GraphRAG performs better … (50.4% vs 49.6%)」只點名一個方法時，第一個數字是它的、第二個是對方的（方法留空，比較對象＝它）；「GraphRAG outperforms NaiveRAG … (23.6% vs 22.8%)」點名兩個時，第一個數字歸主詞（不在比較詞後的那個）、第二個歸比較對象，並保留「順序顛倒」的另一種讀法——只有顛倒讀法符合表格時判 unresolved（ambiguous），兩種都不符才判 contradicted。
4. 單元測試新增 7 條；`evaluation/number-check/replay.py` 的 D67 標註集：precision 1.0、recall 1.0、recall_strict 0.733，三次修正前後相同（沒有漏掉原本抓到的真錯）。
5. 以新核對器離線重判本資料夾全部記錄（`judge.py` 現場跑 `verify_numbers`）：A1-Q2 標籤報錯 14→0、A1-Q3-2 7→0、C1n-Q3 22→0、F1-Q2 6→0；C3n-Q2 3→1，留下的那 1 條（23.6% 被寫成 GraphRAG 的）是**真錯**。記錄裡的 `analysis_status` 欄位是當時舊核對器寫入的，沿用不改。


## D88：對話式助理與示範環境實測（2026-11-07 晚–11-08；記錄 `runs/demo-*.json`）

使用者在前端問「我想知道這個論文的的重點」「你能做到甚麼」都得到「找不到」，否決了「低於門檻就不呼叫模型」的設計（原話見決策日誌 D88）。改為：最相近的三段仍交給模型判斷；提示詞為對話助理（有來源就引用、沒有就明說文件沒提、問系統依描述回答）；prompt 加文件卡；摘要路線補「重點／主旨／講什麼」等問法。測試對象是 Docker 示範環境（兩篇論文都在範圍內，與前面只選一篇的實驗不同），九題各一次，`ANSWER_FACTS=inject`、`SUMMARY_REPAIR=true`。

| 題 | temperature 0（`5362f84`） | temperature 0.5（同版本） |
|---|---|---|
| Q1 摘要 | 兩篇都摘要；**錯**：「Diversity (71.2%)、Overall (71.5%)」不存在於論文（摘要層；程式標無法核對） | 同樣兩個數字（同一份摘要） |
| Q2 比較 | **通過**：13 of 16、三個 Mix 例外含 pp | **通過**：同；代表例改為 HyDE 26.0 對 LightRAG 74.0（對） |
| Q3 消融 | 數字、計數、例外全對；A6 未達 | 同 |
| U1 論文重點 | **走摘要路線**，兩篇各一段；全稱句被程式標註 | 同 |
| U2 你能做到什麼 | 依系統描述回答 | 同 |
| U3 你好 | 自我介紹並說能做什麼 | 同 |
| N3 烤酸種麵包 | 明說文件沒提，補一般步驟 | 明說文件沒提，提議可用一般知識 |
| U4 換句話問（傳統 RAG 比較） | 完整回答，五點 | 完整回答，三段 |
| G2 GraphRAG 表格題 | **error**：bge-m3 對原句算 NaN | 同 |

- 0 與 0.5 的差別只在措辭與代表例的選擇，判定結果一題不差。
- 這兩輪之前還有一輪被作廢：compose 沒把設定傳進容器，實際是注入關、修復關、預設溫度（Q2、Q3 回到 A0 型的錯）。修於 `3e8a24e`。
- Q1 的 71.2／71.5：摘要層寫出論文沒有的數字，原修復只對「歸錯對象」觸發；`a17381e` 起對「頁面上不存在的數字」也觸發。G2 的 NaN：句尾句點造成，`a17381e` 起依序試去句點、正規化、小寫。最後一輪（重新入庫後，0.5）結果見下。

### 最後一輪（`a17381e`，重新入庫，temperature 0.5；`runs/demo-final-t05.json`）

| 題 | 結果 | 說明 |
|---|---|---|
| Q1 | **通過** | 71.2／71.5 消失（摘要修復對不存在的數字觸發）；兩篇摘要的數字全部核對得到（83.6／16.4、Podcast 約 100 萬、News 約 170 萬、72–83%、75–82%） |
| Q2 | 內容通過，**一句措辭錯** | 13 of 16、三個例外含 pp、代表例全對；但有一句「在 Mix 資料集 LightRAG achieves higher scores in Comprehensiveness (49.6% vs 50.4%)」方向寫反，下一句與例外清單又寫對。方向核對沒抓到（句型是「higher scores in X (a vs b)」）。temperature 0.5 的代價：三輪裡只有這輪出現 |
| Q3 | 數字、計數、例外全對；A6 未達。**更正（11-08 D93 複查）**：0.5 的兩輪（`demo-t05`、`demo-final-t05`）後者把 -High／-Low 寫成 high-level-only／low-level-only，前者與 0 那輪沒寫定義；當時判「定義全對」是漏算 | 程式標 FACTUALLY_INCORRECT 是**誤報**：結論核對把「對 -High 的唯一例外是 CS／Diversity」拿去和對 -Low 的三個例外比。核對器已知缺口（例外句的比較對象範圍） |
| U1 論文重點 | 通過 | 兩篇各一段；程式標「100」標籤不符是**誤報**（「不到 100 個 token」被當成 Table 2 的 % Max 100） |
| U2、U3 | 通過 | 依系統描述回答、打招呼 |
| N3 | 通過 | 明說文件沒提 |
| U4 | 通過 | 五點完整回答 |
| G2 | **通過** | NaN 重試生效；77.76／22.24、79.2／20.8、Z、p 全對 |

三輪合計（0、0.5、修正後 0.5）：對話行為九題一致；差異只在 Q1 的摘要數字（修正後消失）、Q2 一句措辭（0.5 一輪）、G2 的 NaN（修正後消失）。


## D92：使用者實測抓到 Q3 例外方向寫反（2026-11-08 03:00–03:40）

使用者在前端問 Q3，貼回答問「寫錯了嗎」：數字全對，但三個變體的例外全寫成「變體表現較差」（實際是變體較好）、-Origin 的一個例外資料集寫錯、-Origin 定義反。成因：事實行「LightRAG lower in: CS / Diversity: 62.0% vs 63.2%」只點一個主詞，模型改寫時換成變體卻保留「較差」。方向核對器沒抓到「X performs worse (a vs b)」句型（缺口）。

修正（`5026ba2`、`715fa9c`）：例外改寫成「CS / Diversity: -High 63.2% above LightRAG 62.0% (+1.2 pp, +1.9% relative)」；問題點名兩個以上方法時只給它們之間的配對（Q2 曾被給 LightRAG 對所有基準的配對，把 HyDE 的 26.0% 當成 GraphRAG 的）；放不下的配對改成一行計數（模型曾照抄「因篇幅省略」）；事實預算 500 → 800。

| 回合 | Q3 | Q2 |
|---|---|---|
| 修正前（使用者貼的） | 三個變體方向全反；-Origin 例外資料集錯；定義反 | — |
| 只改例外寫法（`demo-d92-before.json`） | 方向對；-Origin 那組因預算被略過，模型寫「因篇幅省略」；-High 定義仍反 | 13 of 16、三例外對；代表例多了一個 HyDE 的 26.0% 被當成 GraphRAG（核對器抓到） |
| 再縮配對、提預算（`demo-d92-after.json`） | 方向全對、四組都在、數字全對；**仍把 -High 寫成「high-level-only」**（望文生義，4.3 節定義段在來源 [6] 裡沒照抄）；A6 未達 | 乾淨：16 條事實、13 of 16、三例外，無標籤報錯 |

剩下的 Q3 問題只有兩個：變體定義望文生義（模型層；F1 那次是對的，0.5 下不穩）、A6 並列格式（使用者決定維持）。
