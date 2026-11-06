# 證據位置標準答案（D71 雙角色實驗的 Evidence Recall 真值）

只給獨立評測用，不進任何 prompt。對每題列出**回答必要內容所在的位置**（章節、表／圖、頁、原文依據），分兩層量：

- **Location Recall（位置找到）**：Navigator 的計畫（或 Top-K 的來源）有沒有指到這些位置——依頁碼或表／圖編號比對。
- **Evidence Coverage（內容進 Prompt）**：最終送進回答那次 LLM 呼叫的來源文字，是否真的含有該位置的必要內容——依「原文依據」欄的關鍵片段比對（機器可算），再由人工抽查。

原則：只列**回答必要內容**所在的位置；相關但非必要的段落不列（例如 Q2 的 Related Work）。機器可讀版在 `evidence-locations.json`。

## Q1 `summary this document.`（AC-12）

走摘要路線，三臂的基底證據都是預存的全文摘要與章節摘要（見 D71）。必要內容對應的原文位置：

| 編號 | 必要內容（對應 key-facts） | 位置 | 原文依據 |
|---|---|---|---|
| E1-1 | S1 問題、S2 方法、S3 雙層檢索、S4 增量更新 | Abstract，p1 | "existing RAG systems have significant limitations… dual-level retrieval system… incremental update algorithm" |
| E1-2 | S5 主要結果 | Table 1，p7；或 4.2 節文字 p6–7 | "Table 1: Win rates (%) of baselines v.s. LightRAG" |
| E1-3 | S5／S8 成本 | 4.5 節 Model Cost and Adaptability Analysis，p9 | "fewer than 100 tokens… 610,000 tokens" |

摘要路線的來源是摘要而非切塊：Coverage 以摘要文字是否含上述關鍵片段（或其數字）判定；B 臂補取的切塊另計為「補充」。

## Q2 `compare lightRAG with GraphRAG`（AC-13）

| 編號 | 必要內容 | 位置 | 原文依據 |
|---|---|---|---|
| E2-1 | C1 整體勝率（含 Mix 的例外） | Table 1 的 GraphRAG 區塊，p7 | "GraphRAG LightRAG GraphRAG LightRAG…" 列；Mix 欄 GraphRAG 50.4%／50.8%／50.4% 高於 LightRAG |
| E2-2 | C2 文字結論（較大資料集領先） | 4.2 節 "LightRAG's Superiority over GraphRAG"，p7 | "LightRAG consistently outperforms GraphRAG, particularly in larger datasets" |
| E2-3 | C3 檢索成本 | 4.5 節 ＋ Figure 2，p9 | "610,000 tokens… fewer than 100 tokens… single API call" |
| E2-4 | C4 增量更新機制 | 4.5 節後半，p10 | "GraphRAG must dismantle its existing community structure… LightRAG seamlessly integrates" |
| E2-5（加分） | C5 案例研究 | Table 3，p9 | "Table 3: Case Study: Comparison Between LightRAG and the Baseline Method GraphRAG" |

必要：E2-1 或 E2-2 至少一個（C1／C2），E2-3 或 E2-4 至少一個（成本或更新）。Recall 分母採全部四項（E2-1～E2-4），加分項另計。

## Q3 `Performance of ablated versions of LightRAG`（AC-14）

| 編號 | 必要內容 | 位置 | 原文依據 |
|---|---|---|---|
| E3-1 | A6 四版本數字 | Table 2，p8 | "Table 2: Performance of ablated versions of LightRAG, using NaiveRAG as reference" |
| E3-2 | A1–A3 三個版本的定義、A4 -Origin 例外、A5 主要觀察 | 4.3 節 Ablation Studies 的討論，p7 末–p8（表格之後的 bullets） | "• Low-level-only Retrieval: The -High variant removes high-order retrieval…"、"Surprisingly, the resulting variant, -Origin…" |

## G1（第二篇論文 Graph RAG）`How many context units and tokens do the root-level community summaries (C0) and the source-text summarization (TS) use on the Podcast and News datasets?`

| 編號 | 必要內容 | 位置 | 原文依據 |
|---|---|---|---|
| EG1-1 | G1-1、G1-2 的 units 與 tokens | Table 2，p10 | "Units 34 367 969 1310 1669 55 555 1797 2142 3197"、"Tokens 26657 … 1707694" |

注意：這張表沒有被偵測為表格切塊，數字以內文形式在第 10 頁的切塊裡；位置比對用頁碼與「Table 2」字樣。

## G2（第二篇論文）`Compare condition C2 with vector RAG (SS) on comprehensiveness in the Podcast and News datasets`

| 編號 | 必要內容 | 位置 | 原文依據 |
|---|---|---|---|
| EG2-1 | G2-1、G2-2 的成對比較分數 | Table 6，p26（附錄 G） | "C2 SS 77.76 22.24 … 79.2 20.8" |
| EG2-2（加分） | G2-3 文字範圍 | 5.1 節 Results，p9 | "comprehensiveness win rates between 72-83%… 72-80%" |
| EG2-3（加分） | Table 3 的 claims 數（替代的 comprehensiveness 量法） | Table 3，p11 | "C2 31.62 32.46 … SS 25.23 26.50" |

D69 的 A/B 中兩臂都沒檢索到 p26；這題是「位置在附錄、Top-5 拿不到」的典型，看 Navigator 能不能把它找出來。

## 位置比對規則（給 `evaluation/navigator-abc/`）

- 一個來源切塊「命中」某位置：切塊的頁在該位置的頁範圍內，且（若位置是表／圖）切塊含該標題字樣或該表的數值列；（若位置是章節文字）切塊含原文依據的任一關鍵片段。
- Location Recall ＝ 命中位置數 ÷ 必要位置數，分別算「Top-K 原始來源」「Navigator 計畫（定位成功者）」「最終送進 Analyst 的來源」。
- Evidence Coverage ＝ 最終來源文字含關鍵片段的必要位置數 ÷ 必要位置數。
- 另記：Navigator 計畫條目數、可定位條目數（有效定位率）、補取切塊數、補取中命中必要位置的數（有效補充）、未命中任何必要位置的補取數（多餘證據）、因預算被排除的切塊。
