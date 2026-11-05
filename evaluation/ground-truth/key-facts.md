# 關鍵事實清單：三個必答題的標準答案

狀態：**草稿，待使用者確認**（2026-11-05）。確認後才作為 AC-12、AC-13、AC-14 的判定依據。

- 文件：`sample-documents/2410.05779v3.pdf`（LightRAG 論文，16 頁）。頁碼是 PDF 的頁序，與頁尾印的頁碼相同。
- 「原文依據」是該頁的原文（pypdf 抽出），可用來核對回答有沒有來源。
- 機器可讀版：`key-facts.json`，內容與本檔一致；P3 的驗收與 P4 的評測腳本讀它。
- Table 2 的 128 格標準答案在同資料夾的 `paper-structure.json`（取自論文的 LaTeX 原始檔）。

## 判定方式

每一題分三類：

| 類別 | 意義 | 判定 |
|---|---|---|
| **必要** | 缺任何一項，這一題不通過 | 回答有表達這個事實（用詞可以不同，意思要對）；有數字的，數字必須一字不差 |
| **加分** | 不要求，但出現且正確時記錄 | 同上 |
| **不應出現** | 出現任何一項，這一題不通過 | 人工判讀；數字類可由腳本比對 |

共同規則（三題都適用）：

- 回答中出現的每個數字，都必須能在所引用的頁面原文中找到（AC-26）。
- 每個論點都要有來源編號，來源指向的頁必須真的含有該論點（AC-05）。
- 回答的語言與問題相同；中文問題以繁體回答。

---

## 問題 1：`summary this document.`（AC-12）

類型：摘要類。預期走入庫時建好的章節與全文摘要，不做向量檢索。

### 必要

| 編號 | 事實 | 頁 | 原文依據 |
|---|---|---|---|
| S1 | 要解決的問題：現有 RAG 依賴平面的資料表示、缺乏上下文的關聯意識，導致回答片段化、抓不到實體之間的相互依賴 | 1 | "existing RAG systems have significant limitations, including reliance on flat data representations and inadequate contextual awareness, which can lead to fragmented answers that fail to capture complex inter-dependencies" |
| S2 | 提出的方法：LightRAG，把圖結構加進文本索引與檢索 | 1 | "we propose LightRAG, which incorporates graph structures into text indexing and retrieval processes" |
| S3 | 方法的核心：雙層檢索（低層針對特定實體與關係，高層針對較廣的主題） | 1、2 | "a dual-level retrieval system … from both low-level and high-level knowledge discovery"；"low-level retrieval, which focuses on precise information about specific entities and their relationships, and high-level retrieval, which encompasses broader topics and themes" |
| S4 | 方法的特點：增量更新，新資料加入時不必重建整個索引 | 1、2 | "an incremental update algorithm that ensures the timely integration of new data"；"By eliminating the need to rebuild the entire index" |
| S5 | 主要結果：實驗顯示在檢索準確度與效率上優於既有方法（NaiveRAG、RQ-RAG、HyDE、GraphRAG） | 1、7 | "Extensive experimental validation demonstrates considerable improvements in retrieval accuracy and efficiency compared to existing approaches"；Table 1 |

### 加分

| 編號 | 事實 | 頁 | 原文依據 |
|---|---|---|---|
| S6 | 圖結構與向量表示結合，加快相關實體與關係的檢索 | 1 | "the integration of graph structures with vector representations facilitates efficient retrieval of related entities and their relationships" |
| S7 | 實驗在四個領域的資料集（Agriculture、CS、Legal、Mix）、四個評估面向（Comprehensiveness、Diversity、Empowerment、Overall）上進行 | 6、7 | 第 6 頁的資料集與評估面向說明；Table 1 |
| S8 | 成本：檢索階段 LightRAG 用不到 100 個 token、1 次 API 呼叫；GraphRAG 約 610,000 個 token、數百次呼叫 | 9 | 見問題 2 的 C3 |
| S9 | 程式碼開源：https://github.com/HKUDS/LightRAG | 1 | "We have made our LightRAG open-source and available at the link" |
| S10 | 三個要克服的挑戰：全面的資訊檢索、提高檢索效率、快速適應新資料 | 2 | "three key challenges: i) Comprehensive Information Retrieval … ii) Enhanced Retrieval Efficiency … iii) Rapid Adaptation to New Data" |

### 不應出現

| 編號 | 內容 | 說明 |
|---|---|---|
| S-X1 | 把論文引用的其他研究當成本論文的貢獻（例如 R-Eval、GraphRAG、RQ-RAG、HyDE 的方法） | P2 的實測發生過：回答說「論文提出了 R-eval」，R-Eval 是被引用的工作 |
| S-X2 | 只涵蓋論文的前半（只有問題與方法，沒有結果），或只涵蓋後半 | 代表摘要的來源不完整 |
| S-X3 | 論文中沒有的數字或結論 | |

---

## 問題 2：`compare lightRAG with GraphRAG`（AC-13）

類型：一般檢索。驗收條件要求至少兩項論文中寫到的具體差異；下面 C1–C5 任兩項即可，引用數字時必須正確。

### 必要（至少兩項）

| 編號 | 差異 | 頁 | 原文依據 |
|---|---|---|---|
| C1 | **效果**：兩者都是圖結構的 RAG，但 LightRAG 整體勝過 GraphRAG，尤其在較大、語言脈絡較複雜的資料集（Agriculture、CS、Legal，各含數百萬 token）| 7 | "While both LightRAG and GraphRAG use graph-based retrieval mechanisms, LightRAG consistently outperforms GraphRAG, particularly in larger datasets with complex language contexts. In the Agriculture, CS, and Legal datasets—each containing millions of tokens—LightRAG shows a clear advantage" |
| C2 | **多樣性**：LightRAG 在 Diversity 面向的優勢最明顯，論文歸因於雙層檢索 | 7 | "LightRAG demonstrates a significant advantage in the Diversity metric … We attribute this advantage to LightRAG's dual-level retrieval paradigm" |
| C3 | **檢索成本**：GraphRAG 產生 1,399 個社群，檢索時用到 610 個第 2 層社群，每份報告約 1,000 token，合計約 610,000 token，且要逐一走訪社群、數百次 API 呼叫；LightRAG 關鍵字產生與檢索用不到 100 個 token、只需 1 次 API 呼叫 | 9 | "GraphRAG generates 1,399 communities, with 610 level-2 communities actively utilized … total token consumption of 610,000 tokens … hundreds of API calls … LightRAG … using fewer than 100 tokens … requiring only a single API call" |
| C4 | **增量更新**：新增一份與 Legal 同大小的資料時，GraphRAG 必須拆掉既有的社群結構並全部重建，約需 1,399 × 2 × 5,000 個 token；LightRAG 把新的實體與關係併入既有的圖，不需重建 | 10 | "GraphRAG must dismantle its existing community structure … approximately 5,000 tokens per community report. Given 1,399 communities, GraphRAG would require around 1,399 × 2 × 5,000 tokens … LightRAG seamlessly integrates newly extracted entities and relationships into the existing graph without the need for full reconstruction" |
| C5 | **檢索機制**：GraphRAG 以 LLM 抽出實體與關係後產生社群報告，查詢時逐一走訪社群（brute-force）；LightRAG 用雙層檢索（低層實體、高層主題）結合圖與向量表示 | 6、10 | 第 6 頁 GraphRAG 的基準說明；"existing methods often rely on brute-force searches for each generated community … Our LightRAG framework overcomes this limitation … through our proposed dual-level retrieval paradigm" |

### 加分

| 編號 | 事實 | 頁 | 原文依據 |
|---|---|---|---|
| C6 | Table 1 中 GraphRAG 對 LightRAG 的 Overall 勝率：Agriculture 45.2% 對 54.8%、CS 48.0% 對 52.0%、Legal 47.2% 對 52.8%、Mix 50.4% 對 49.6% | 7 | Table 1 最後一個區塊 |
| C7 | **例外**：在 Mix 資料集，GraphRAG 在 Comprehensiveness（50.4% 對 49.6%）、Empowerment（50.8% 對 49.2%）與 Overall 略勝 LightRAG；完整的回答應提到 LightRAG 不是全面領先 | 7 | Table 1 |
| C8 | 案例研究（Table 3）：對一個機器學習問題，LLM 評審在四個面向都判 LightRAG 勝過 GraphRAG | 8、9 | "LightRAG outperforms in all evaluation dimensions assessed by the LLM judge" |
| C9 | 兩者在增量更新時，實體與關係抽取的開銷相近 | 10 | "both models exhibit similar overhead for entity and relationship extraction" |

### 不應出現

| 編號 | 內容 |
|---|---|
| C-X1 | 說 LightRAG 在所有資料集、所有面向都勝過 GraphRAG（Mix 有例外） |
| C-X2 | 把 NaiveRAG、RQ-RAG 或 HyDE 的數字當成 GraphRAG 的 |
| C-X3 | 論文沒有的比較（例如兩者的程式語言、授權、記憶體用量） |

---

## 問題 3：`Performance of ablated versions of LightRAG`（AC-14）

類型：一般檢索。答案在第 8 頁的 Table 2 與 4.3 節。**這一題必須在 P3 通過。**

### 必要

| 編號 | 事實 | 頁 | 原文依據 |
|---|---|---|---|
| A1 | 三個消融版本各代表什麼：`-High` 移除高層檢索（只剩低層）；`-Low` 移除低層檢索（只剩高層）；`-Origin` 檢索時不使用原文 | 8 | "Low-level-only Retrieval: The -High variant removes high-order retrieval"；"High-level-only Retrieval: The -Low variant"；"We eliminated the use of original text in our retrieval process … the resulting variant, -Origin" |
| A2 | `-High`：幾乎所有資料集與指標都明顯下降；原因是過度聚焦於特定實體及其鄰居，難以回答需要全面洞察的複雜問題 | 8 | "leading to a significant performance decline across nearly all datasets and metrics … focuses excessively on entities and their immediate neighbors" |
| A3 | `-Low`：在 Comprehensiveness 有優勢，但對特定實體的深度不足，不利於需要精確細節的任務 | 8 | "offers a significant advantage in comprehensiveness … the trade-off is a reduced depth in examining specific entities" |
| A4 | `-Origin`：沒有明顯下降，在 Agriculture 與 Mix 甚至略有提升；論文歸因於圖索引已抽出關鍵資訊，而原文常含雜訊 | 8 | "does not exhibit significant performance declines across all four datasets. In some cases, this variant even shows improvements (e.g. in Agriculture and Mix)" |
| A5 | 完整版（hybrid）結合兩層檢索，兼顧廣度與深度，各面向表現平衡 | 8 | "The hybrid mode, or the full version of LightRAG, combines the strengths of both … achieves balanced performance across multiple dimensions" |
| A6 | **數字**：回答至少引用一組各版本的數字，且每個數字都與 Table 2 的對應格（資料集 × 指標 × 版本）完全一致。建議以 Overall 一列為準： | 8 | Table 2 |

Overall 一列，對 NaiveRAG 的勝率（與 Table 2 逐格核對，2026-11-05）：

| 資料集 | LightRAG | -High | -Low | -Origin |
|---|---|---|---|---|
| Agriculture | 67.6% | 64.8% | 65.2% | 74.4% |
| CS | 61.2% | 56.0% | 56.4% | 60.8% |
| Legal | 84.8% | 78.0% | 81.2% | 84.4% |
| Mix | 60.0% | 57.6% | 64.8% | 55.6% |

### 加分

| 編號 | 事實 | 頁 | 原文依據 |
|---|---|---|---|
| A7 | 表格以 NaiveRAG 為對照（每格是對 NaiveRAG 的勝率），共四個資料集、四個指標 | 8 | "Table 2: Performance of ablated versions of LightRAG, using NaiveRAG as reference" |
| A8 | 其他列的數字（Comprehensiveness、Diversity、Empowerment），同樣必須與 Table 2 一致 | 8 | `paper-structure.json` 的 128 格 |

### 不應出現

| 編號 | 內容 | 說明 |
|---|---|---|
| A-X1 | 數字張冠李戴：把某個資料集、指標或版本的數字寫到另一個 | P2 的切塊把 `-High` 區塊切成兩半、資料集標題只在第一塊，是這類錯誤的主要來源（見 `../table2-chunking/`） |
| A-X2 | 只描述趨勢而沒有任何數字 | |
| A-X3 | 寫出表格中不存在的數字 | |
| A-X4 | 把第 9 頁成本比較的數字（610,000、1,399、5,000）當成消融實驗的結果 | 論文第 9 頁的內文把成本比較誤寫成「presented in Table 2」，檢索時可能被拉進來 |
| A-X5 | 只回答完整版 LightRAG 對 NaiveRAG，沒有談三個消融版本 | P2 的實測回答就是這樣，不算通過 |

---

## 用法

- **P3 驗收**：對每一題的回答，人工逐項勾選必要事實，腳本比對數字（`key-facts.json` 的 `numbers`）。三題的結果記在 P3 階段紀錄。
- **P4 評測**：這三題納入題庫；本清單是它們的標準答案，評測腳本以此計算關鍵事實涵蓋率。
- 修改本清單要同步修改 `key-facts.json`，並在決策日誌記一筆。
