# 關鍵事實清單：三個必答題的標準答案

狀態：**已確認**（2026-11-05，使用者審閱後修正八點，決策日誌 D60）。是 AC-12、AC-13、AC-14 的判定依據，也是 P4 題庫中這三題的標準答案。

- 文件：`sample-documents/2410.05779v3.pdf`（LightRAG 論文，16 頁）。頁碼是 PDF 的頁序，與頁尾印的頁碼相同。
- 「原文依據」是該頁的原文（pypdf 抽出），用來核對回答的來源。
- 機器可讀版：`key-facts.json`，內容與本檔一致；P3 的驗收與 P4 的評測腳本讀它。
- Table 2 的 128 格標準答案在同資料夾的 `paper-structure.json`（取自論文的 LaTeX 原始檔）。
- **標準在評測前固定**：修改本清單要同步修改 `key-facts.json`，並在決策日誌記一筆；不依模型的回答結果事後調整。

## 判定方式

每一題的判定結果分四類，分開記錄，不混為一談：

| 類別 | 意義 | 對通過的影響 |
|---|---|---|
| **缺少加分內容** | 「加分」清單中的事實沒有出現 | 不影響通過，只記錄涵蓋了幾項 |
| **必要內容不足** | 「必要」清單中有事實沒有表達到（用詞可以不同，意思要對），或沒有達到該題的最低要求 | 不通過 |
| **事實性錯誤** | 回答出現「事實性錯誤」清單中的內容，或與論文矛盾的陳述、不存在的數字 | 不通過，另計件數 |
| **引用不支持答案** | 某個論點的來源編號指向的頁面不含該論點；或回答中的數字在所引用的頁面原文找不到（AC-26） | 不通過，另計件數 |

共同規則（三題都適用）：

- 每個論點都要有來源編號（AC-05）。
- 回答的語言與問題相同；中文問題以繁體回答。
- Table 1 與 Table 2 的數值是**成對比較的勝率**（LLM 評審在兩個回答中選一個，某方被選中的百分比），不是模型的準確率。回答把它說成準確率，算事實性錯誤。

## 論文本身的已知問題

- 第 9 頁 4.5 節的成本比較（token 數與 API 呼叫數）是 **Figure 2**（以表格形式呈現的圖），但內文誤寫為「presented in Table 2」。Table 2 是第 8 頁的消融實驗。評測時兩者不得混用：成本數字（610,000、1,399、5,000、<100）不是消融結果。

---

## 問題 1：`summary this document.`（AC-12）

類型：摘要類。預期走入庫時建好的章節與全文摘要，不做向量檢索。

### 必要（全部）

| 編號 | 事實 | 頁 | 原文依據 |
|---|---|---|---|
| S1 | 要解決的問題：現有 RAG 依賴平面的資料表示、缺乏上下文的關聯意識，導致回答片段化、抓不到實體之間的相互依賴 | 1 | "existing RAG systems have significant limitations, including reliance on flat data representations and inadequate contextual awareness, which can lead to fragmented answers that fail to capture complex inter-dependencies" |
| S2 | 提出的方法：LightRAG，把圖結構加進文本索引與檢索 | 1 | "we propose LightRAG, which incorporates graph structures into text indexing and retrieval processes" |
| S3 | 方法的核心：雙層檢索（低層針對特定實體與關係，高層針對較廣的主題） | 1、2 | "a dual-level retrieval system … from both low-level and high-level knowledge discovery"；"low-level retrieval, which focuses on precise information about specific entities and their relationships, and high-level retrieval, which encompasses broader topics and themes" |
| S4 | 方法的特點：增量更新，新資料加入時不必重建整個索引 | 1、2 | "an incremental update algorithm that ensures the timely integration of new data"；"By eliminating the need to rebuild the entire index" |
| S5 | 主要結果：**至少指出一項具體的比較面向**（Comprehensiveness、Diversity、Empowerment、Overall、檢索成本）**或比較對象**（NaiveRAG、RQ-RAG、HyDE、GraphRAG）；只說「效能較佳」「優於既有方法」不算 | 1、7、9 | "Extensive experimental validation demonstrates considerable improvements in retrieval accuracy and efficiency compared to existing approaches"；Table 1；第 9 頁的成本比較 |

### 加分

| 編號 | 事實 | 頁 | 原文依據 |
|---|---|---|---|
| S6 | 圖結構與向量表示結合，加快相關實體與關係的檢索 | 1 | "the integration of graph structures with vector representations facilitates efficient retrieval of related entities and their relationships" |
| S7 | 實驗在四個領域的資料集（Agriculture、CS、Legal、Mix）、四個評估面向（Comprehensiveness、Diversity、Empowerment、Overall）上以成對勝率比較 | 6、7 | 第 6 頁的資料集與評估面向說明；Table 1 |
| S8 | 成本：檢索階段 LightRAG 用不到 100 個 token、1 次 API 呼叫；GraphRAG 約 610,000 個 token、數百次呼叫 | 9 | Figure 2 與內文（見問題 2 的 C3） |
| S9 | 程式碼開源：https://github.com/HKUDS/LightRAG | 1 | "We have made our LightRAG open-source and available at the link" |
| S10 | 三個要克服的挑戰：全面的資訊檢索、提高檢索效率、快速適應新資料 | 2 | "three key challenges: i) Comprehensive Information Retrieval … ii) Enhanced Retrieval Efficiency … iii) Rapid Adaptation to New Data" |

### 事實性錯誤

| 編號 | 內容 | 說明 |
|---|---|---|
| S-X1 | 把論文引用的其他研究當成本論文的貢獻（例如 R-Eval、GraphRAG、RQ-RAG、HyDE 的方法） | P2 的實測發生過：回答說「論文提出了 R-eval」，R-Eval 是被引用的工作 |
| S-X2 | 宣稱 LightRAG 在所有情況下全面領先 | Table 1 在 Mix 資料集對 GraphRAG 有三個面向落後（見 C7）；「整體表現較佳」是對的，「全面領先」是錯的 |
| S-X3 | 論文中沒有的數字或結論 | |

另記（必要內容不足，不是事實性錯誤）：只涵蓋論文的前半（只有問題與方法，沒有結果）或只涵蓋後半，代表摘要的來源不完整。

---

## 問題 2：`compare lightRAG with GraphRAG`（AC-13）

類型：一般檢索。

### 必要（C1–C5 至少兩項）

通過條件維持 AC-13 的「至少兩項論文中寫到的具體差異」，不強制成本或增量更新一定要出現。**算得上一項差異的，必須是真正把兩個方法放在一起比的陳述**（在什麼面向、誰如何、誰如何）；「LightRAG 比較好」「GraphRAG 比較慢」這種沒有比較面向的優劣描述不算一項。引用數字時必須正確。

| 編號 | 差異 | 頁 | 原文依據 |
|---|---|---|---|
| C1 | **效果**：兩者都是圖結構的 RAG，LightRAG 整體勝率較高，尤其在較大、語言脈絡較複雜的資料集（Agriculture、CS、Legal，各含數百萬 token） | 7 | "While both LightRAG and GraphRAG use graph-based retrieval mechanisms, LightRAG consistently outperforms GraphRAG, particularly in larger datasets with complex language contexts. In the Agriculture, CS, and Legal datasets—each containing millions of tokens—LightRAG shows a clear advantage" |
| C2 | **多樣性**：LightRAG 在 Diversity 面向的優勢最明顯，論文歸因於雙層檢索 | 7 | "LightRAG demonstrates a significant advantage in the Diversity metric … We attribute this advantage to LightRAG's dual-level retrieval paradigm" |
| C3 | **檢索成本**：GraphRAG 產生 1,399 個社群，檢索時用到 610 個第 2 層社群，每份報告約 1,000 token，合計約 610,000 token，且要逐一走訪社群、數百次 API 呼叫；LightRAG 關鍵字產生與檢索用不到 100 個 token、只需 1 次 API 呼叫 | 9 | Figure 2 與內文："GraphRAG generates 1,399 communities, with 610 level-2 communities actively utilized … total token consumption of 610,000 tokens … hundreds of API calls … LightRAG … using fewer than 100 tokens … requiring only a single API call" |
| C4 | **增量更新**：新增一份與 Legal 同大小的資料時，GraphRAG 必須拆掉既有的社群結構並全部重建，約需 1,399 × 2 × 5,000 個 token；LightRAG 把新的實體與關係併入既有的圖，不需重建 | 10 | "GraphRAG must dismantle its existing community structure … approximately 5,000 tokens per community report. Given 1,399 communities, GraphRAG would require around 1,399 × 2 × 5,000 tokens … LightRAG seamlessly integrates newly extracted entities and relationships into the existing graph without the need for full reconstruction" |
| C5 | **檢索機制**：GraphRAG 以 LLM 抽出實體與關係後產生社群報告，查詢時逐一走訪社群（brute-force）；LightRAG 用雙層檢索（低層實體、高層主題）結合圖與向量表示 | 6、10 | 第 6 頁 GraphRAG 的基準說明；"existing methods often rely on brute-force searches for each generated community … Our LightRAG framework overcomes this limitation … through our proposed dual-level retrieval paradigm" |

### 加分

| 編號 | 事實 | 頁 | 原文依據 |
|---|---|---|---|
| C6 | Table 1 中 GraphRAG 對 LightRAG 的 Overall 勝率：Agriculture 45.2% 對 54.8%、CS 48.0% 對 52.0%、Legal 47.2% 對 52.8%、Mix 50.4% 對 49.6% | 7 | Table 1 最後一個區塊 |
| C7 | **例外**：在 Mix 資料集，GraphRAG 在 Comprehensiveness（50.4% 對 49.6%）、Empowerment（50.8% 對 49.2%）與 Overall（50.4% 對 49.6%）略勝 LightRAG；提到這個例外表示回答看懂了表格 | 7 | Table 1 |
| C8 | 案例研究（Table 3）：對一個機器學習問題，LLM 評審在四個面向都判 LightRAG 勝過 GraphRAG | 8、9 | "LightRAG outperforms in all evaluation dimensions assessed by the LLM judge" |
| C9 | 兩者在增量更新時，實體與關係抽取的開銷相近 | 10 | "both models exhibit similar overhead for entity and relationship extraction" |

### 事實性錯誤

| 編號 | 內容 | 說明 |
|---|---|---|
| C-X1 | 說 LightRAG 在所有資料集、所有面向都勝過 GraphRAG（全面領先） | Mix 有三個面向是 GraphRAG 略勝。**「整體表現較佳」「在大多數資料集勝出」是對的**，不算錯誤；只有宣稱「全部」「所有」才算 |
| C-X2 | 把 NaiveRAG、RQ-RAG 或 HyDE 的數字當成 GraphRAG 的 | Table 1 有四個區塊，GraphRAG 是最後一個 |
| C-X3 | 把 Table 1 的勝率說成模型的準確率 | 數值是成對比較的勝率 |
| C-X4 | 論文沒有的比較（例如兩者的程式語言、授權、記憶體用量） | |

---

## 問題 3：`Performance of ablated versions of LightRAG`（AC-14）

類型：一般檢索。答案在第 8 頁的 Table 2 與 4.3 節。**這一題必須在 P3 通過。**

### 必要（全部）

**最低要求**：(a) 解釋三個消融版本各移除什麼，以及各自的主要觀察結果（A1–A5）；(b) **至少選一個資料集、同一項評估指標，完整列出 LightRAG、-High、-Low、-Origin 四個版本的數字**，且每個數字都與 Table 2 的對應格（資料集 × 指標 × 版本）一致（A6）。只列數字沒有分析，或只有分析沒有數字，都是必要內容不足。

| 編號 | 事實 | 頁 | 原文依據 |
|---|---|---|---|
| A1 | 三個消融版本各代表什麼：`-High` 移除高層檢索（只剩低層）；`-Low` 移除低層檢索（只剩高層）；`-Origin` 檢索時不使用原文 | 8 | "Low-level-only Retrieval: The -High variant removes high-order retrieval"；"High-level-only Retrieval: The -Low variant"；"We eliminated the use of original text in our retrieval process … the resulting variant, -Origin" |
| A2 | `-High`：幾乎所有資料集與指標都明顯下降；原因是過度聚焦於特定實體及其鄰居，難以回答需要全面洞察的複雜問題 | 8 | "leading to a significant performance decline across nearly all datasets and metrics … focuses excessively on entities and their immediate neighbors" |
| A3 | `-Low`：在 Comprehensiveness 有優勢，但對特定實體的深度不足，不利於需要精確細節的任務 | 8 | "offers a significant advantage in comprehensiveness … the trade-off is a reduced depth in examining specific entities" |
| A4 | `-Origin`：**沒有明顯下降，在部分資料集與指標甚至優於完整版**（論文點名 Agriculture 與 Mix）；論文歸因於圖索引已抽出關鍵資訊，而原文常含雜訊 | 8 | "does not exhibit significant performance declines across all four datasets. In some cases, this variant even shows improvements (e.g. in Agriculture and Mix)" |
| A5 | 完整版（hybrid）結合兩層檢索，兼顧廣度與深度，各面向表現平衡 | 8 | "The hybrid mode, or the full version of LightRAG, combines the strengths of both … achieves balanced performance across multiple dimensions" |
| A6 | **數字**：同一資料集、同一指標的四個版本完整列出，每個數字與 Table 2 一致 | 8 | Table 2（`paper-structure.json` 的 128 格） |

A6 的例子，Overall 一列、對 NaiveRAG 的勝率（與 Table 2 逐格核對，2026-11-05）；回答用其他指標的列也可以：

| 資料集 | LightRAG | -High | -Low | -Origin |
|---|---|---|---|---|
| Agriculture | 67.6% | 64.8% | 65.2% | 74.4% |
| CS | 61.2% | 56.0% | 56.4% | 60.8% |
| Legal | 84.8% | 78.0% | 81.2% | 84.4% |
| Mix | 60.0% | 57.6% | 64.8% | 55.6% |

-Origin 優於完整版的例子：Agriculture 的 Overall 74.4% 對 67.6%；Mix 的 Diversity 74.4% 對 67.6%。

### 加分

| 編號 | 事實 | 頁 | 原文依據 |
|---|---|---|---|
| A7 | 表格以 NaiveRAG 為對照（每格是對 NaiveRAG 的成對勝率），共四個資料集、四個指標 | 8 | "Table 2: Performance of ablated versions of LightRAG, using NaiveRAG as reference" |
| A8 | 列出不只一個資料集或不只一個指標的數字，且都與 Table 2 一致 | 8 | `paper-structure.json` 的 128 格 |

### 事實性錯誤

| 編號 | 內容 | 說明 |
|---|---|---|
| A-X1 | 數字張冠李戴：把某個資料集、指標或版本的數字寫到另一個 | P2 的切塊把 `-High` 區塊切成兩半、資料集標題只在第一塊，是這類錯誤的主要來源（見 `../table2-chunking/`） |
| A-X2 | 寫出 Table 2 中不存在的數字 | |
| A-X3 | 把第 9 頁 Figure 2 的成本數字（610,000、1,399、5,000、<100）當成消融實驗的結果 | 論文內文把 Figure 2 誤寫為「Table 2」，檢索時可能被拉進來 |
| A-X4 | 假設所有消融版本一定都比完整版差 | `-Origin` 在部分資料集與指標優於完整版 |
| A-X5 | 把勝率說成準確率 | |

另記（必要內容不足，不是事實性錯誤）：只描述趨勢而沒有數字；只回答完整版 LightRAG 對 NaiveRAG、沒有談三個消融版本（P2 的實測回答就是這樣）。

---

## 用法

- **P3 驗收**：對每一題的回答，人工逐項勾選必要與加分事實、判讀事實性錯誤；腳本比對數字（`key-facts.json` 的 `numbers`）與引用頁面。結果依四類分開記在 P3 階段紀錄。
- **P4 評測**：這三題納入題庫；本清單是它們的標準答案，評測腳本以此計算必要事實涵蓋率、加分事實涵蓋率、事實性錯誤數、引用不支持數。
- 本清單在 P4 評測前固定；修改要同步 `key-facts.json` 並在決策日誌記一筆。
