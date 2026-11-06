# number-check — AC-26 數字標籤核對在真實回答上的回放（D67）

回答中的數字出現在引用頁面，不代表它掛對了方法、資料集與指標；核對說「標籤不符」，也不代表回答真的錯。這個實驗用保存下來的 25 份真實回答、人工逐格對照 Table 1 與 Table 2 的標準答案，量測數字標籤核對改版前後的誤報、漏報與未判定。

## 問題（2026-11-06，D66 重測的 Q1 回答）

| 案例 | 句子 | 原文 | 改版前的核對 |
|---|---|---|---|
| 誤報 | LightRAG achieved 83.6% win rate **over NaiveRAG** in Comprehensiveness, **86.4% in Diversity** | 86.4% 是 Legal／Diversity／LightRAG | 判為 NaiveRAG 的數字（取最近的方法名） |
| 漏報 | Against GraphRAG, LightRAG achieved 51.6% … and **64.0% in Diversity in the same dataset**（上文是 Legal） | Legal／Diversity／LightRAG 對 GraphRAG 是 73.6%；64.0% 是 Mix | 放行（句中沒寫資料集就不比對） |

## 方法

- **標準答案**：`answers.json` 收錄 25 份真實回答（Q1 ×7、Q2 ×5、Q3 ×13；條件見各筆 `condition`；A17–A19 是 D67 改版後的回歸，A20–A25 是 D68 的回歸），其中 312 個數字的值出現在 Table 1 或 Table 2。每個數字由人工對照 `../ground-truth/paper-structure.json`（`table1`、`table2`，取自論文 LaTeX 原始檔）判定該句給它的歸屬是否正確；錯的列在 `wrong_figures`（數字、第幾次出現、正確的格子），共 15 個。Q2 的 5 份回答沒有表格數字（引用的是 Figure 2 與內文）。
- **核對的輸入**：論文第 7–9 頁經入庫流程改寫後的文字（表格區域逐列線性化），與線上核對看到的相同。
- **改版前**：`app/backend/app/chat/verification.py` 在 commit `21752a2`（D64 規則：離數字最近的標籤、句中沒寫的類別不比對、二態）。回放時由 `git show` 載入，不保留舊程式碼的副本。
- **改版後**：工作樹中的同一檔案（D67：角色解析、比較對象、三態；清單標題「- Comprehensiveness:」為其下各項提供標籤）。
- **判定**：以人工標註為真值。TP＝錯的數字被判「不符」；FP＝對的數字被判「不符」；FN＝錯的數字被放行；TN＝對的數字被放行；UNRESOLVED＝改版後判「未能判定」，依真值再分對／錯。

## 結果

| | 改版前（D64） | 改版後（D67） |
|---|---|---|
| 真值為錯的數字 | 15 | 15 |
| TP（抓到） | 9 | 11 |
| FP（誤報） | 13 | 0 |
| FN（漏報） | 6 | 0 |
| TN | 284 | 204 |
| UNRESOLVED，真值錯 | — | 4 |
| UNRESOLVED，真值對 | — | 93 |
| Precision | 0.41 | 1.00 |
| Recall（FN 計為漏） | 0.60 | 1.00 |
| Recall（嚴格：未判定的錯也計為漏） | 0.60 | 0.73 |
| 未判定率 | — | 31.1%（86 缺標籤、11 歧義） |

兩個案例：86.4% 從誤報變成支持（不列出）；64.0% 從漏報變成「不符」（答案：Diversity、Legal、LightRAG、vs GraphRAG）。

**改版後未能判定的 4 個錯誤**（核對沒抓到，但也沒宣稱支持）：

| 回答 | 數字 | 句子 | 為什麼判不了 |
|---|---|---|---|
| A06 | 36.0% | …it achieves 65.2% comprehensiveness compared to NaiveRAG's 36.0%, and 72.8% diversity versus 27.2% | 36.0% 的指標沒寫（句中有 comprehensiveness 與 diversity 兩個，各貼著別的數字）；NaiveRAG 在 -High 區塊的 Agriculture Comprehensiveness 是 34.8%，36.0% 是 -Low 區塊的 |
| A10 | 60.0% | …improves performance in Agriculture (Overall: 67.6% (-Origin) vs. 60.0% (LightRAG)) and Mix (Overall: 55.6% (-Origin) vs. 60.0% (LightRAG)) | 同一子句有 Agriculture 與 Mix 兩個資料集、沒有貼著數字，核對不猜；第一個 60.0% 其實是 Mix 的數字被寫到 Agriculture |
| A24 | 74.4%、25.6% | - **Comprehensiveness:** In the Agriculture dataset, -High … 65.2% … In the Mix dataset, the -Origin variant achieves 74.4% compared to NaiveRAG's 25.6% | 指標寫在同一行開頭的粗體標題，句子切開後第二句沒有指標；清單標題規則只認整行只有標籤的行。74.4%／25.6% 是 Diversity／Mix 的，被寫在 Comprehensiveness 下 |

**改版前的 8 個誤報**都屬於同一類：方法名出現在比較語之後（over／compared to／versus）或與數字隔著其他字，核對取最近的名稱。**改版前的 4 個漏報**都是句中沒寫出某一類標籤。

## 結論

- 不以距離判定、把比較對象當成獨立角色之後，25 份回答上誤報歸零，15 個錯誤抓到 11 個，剩下 4 個誠實地標成未判定。D68 期間再補：每個比較對象只屬於它前面的那個數字（「83.6% against Naive RAG, 88.4% against RQ-RAG」）、camel-case 名稱容許空格（Naive RAG）。A21 的 88.4%（寫成 Comprehensiveness，實為 Diversity）就是這樣抓到的。
- 代價是近三分之一的表格數字判為「未能判定」，絕大多數（86/97）是答案沒寫全標籤——模型常省略方法（「it」「its」）或指標。改版後的 Q3 回歸回答以清單列出 80 個數字、指標寫在清單標題，第一版核對把它們全判為未判定；加上「清單標題為其下各項提供標籤」的規則後 80 個全部判為支持。這不是錯誤，介面上不以錯誤樣式顯示，回答下方也不附說明。
- 核對不知道不等於答案錯；核對沒列出也不等於答案全對（D67 任務書）。這份回放的真值由 AI 人工標註、使用者抽查，標註本身也可能錯：A03 的 60.0%／59.6% 一對、A10 的 61.2% 都在標註時改過判定，理由寫在 `answers.json`。

## 已知限制

- 只處理依第 5 節格式線性化的表格；比較對象只在同一組恰有兩格時才知道。
- 跨句只繼承兩種情況：寫明「the same …」／「同一」時繼承上一句；清單標題（整行只有標籤）為其下連續的清單項目提供標籤，遇到非清單句就停止。「its」「the former」不繼承。
- 比較語只認 over／against／than／versus／vs.／compared to／compared with／relative to 與中文 優於／勝過／相較於／對比。
- 「Naive RAG」（有空格）這類名稱變體不會被認出。
- 範圍「32.4%–38.8%」兩端共用標籤，但範圍本身的語意（是否涵蓋全部資料集）不檢查。

## 重現

```bash
.venv/bin/python evaluation/number-check/replay.py
```

需要 `sample-documents/2410.05779v3.pdf` 與 git 歷史（載入改版前的程式）。輸出 `before.results.json`、`after.results.json`（第一段 `config` 是設定，`summary` 是上表，`figures` 是每個數字的真值與判定）。
