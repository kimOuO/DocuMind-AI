# 關鍵事實：第二篇論文（Graph RAG，arXiv:2404.16130v2）的兩個表格比較題

用途：D69 的 A/B 實驗要確認方法不是只對 LightRAG 論文有效。這份清單只給獨立評測用，不進任何 prompt。
判定方式與 `key-facts.md` 相同：必要事實是否出現、數字歸屬是否正確、引用的來源頁是否含該陳述。

來源：論文第 10 頁 Table 2（context units、token 數、佔最大值百分比）與第 26 頁 Table 6（成對比較的平均分數）。**這兩張表現有的表格偵測沒有抓到**（它們沒有被切成表格切塊，數字以內文形式進切塊），所以數字標籤核對與全稱宣稱核對在這篇論文上不會啟動；這正是泛化測試要觀察的事，不為此加規則。

## G1：`How many context units and tokens do the root-level community summaries (C0) and the source-text summarization (TS) use on the Podcast and News datasets?`

| 編號 | 事實 | 頁 |
|---|---|---|
| G1-1 | Podcast：C0 34 個 units、26,657 tokens；TS 1,669 個 units、1,014,611 tokens | 10 |
| G1-2 | News：C0 55 個 units、39,770 tokens；TS 3,197 個 units、1,707,694 tokens | 10 |
| G1-3（加分） | C0 佔最大 token 數的 2.6%（Podcast）／2.3%（News）；TS 為 100% | 10 |
| 事實性錯誤 | 任何數字掛到別的條件（C1–C3）或別的資料集；把 units 與 tokens 互換 | |

## G2：`Compare condition C2 with vector RAG (SS) on comprehensiveness in the Podcast and News datasets`

| 編號 | 事實 | 頁 |
|---|---|---|
| G2-1 | Podcast：C2 平均 77.76 對 SS 22.24（p < 0.001） | 26 |
| G2-2 | News：C2 平均 79.2 對 SS 20.8（p < 0.001） | 26 |
| G2-3（加分） | 內文的範圍說法：global approaches 對 vector RAG 的 comprehensiveness 勝率 Podcast 72–83%、News 72–80% | 9 |
| 事實性錯誤 | 把 C2 的數字與其他條件（C0、C1、C3、TS）混用；方向寫反（說 SS 高於 C2） | |

## 無答案對照

`What is the capital of France?`：兩篇論文都不含答案，應在檢索前被拒答（相似度門檻），不呼叫 LLM；在所有實驗臂上行為相同。

## 一般事實題（LightRAG 論文）

`How many tokens does GraphRAG consume in the retrieval phase on the Legal dataset?`：610,000 tokens（第 9 頁）；加分：610 個社群報告 × 約 1,000 tokens、數百次 API 呼叫，對比 LightRAG 不到 100 tokens、1 次呼叫。
