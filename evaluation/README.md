# evaluation — 評測程式

參數與做法的決定都以實測為依據（`CLAUDE.md`：參數類決定必須引用實驗數據）。這個資料夾在版控裡只放**評測程式**；題庫、標準答案、逐題的問答紀錄與各實驗的報告保留在開發機，未公開，需要時可另外提供。

| 程式 | 做什麼 |
|---|---|
| `ground-truth/build_paper_structure.py`、`build_graphrag_structure.py` | 從論文的 LaTeX 原始檔建立標準答案：表格每一格的方法、資料集、指標、數值，以及章節標題 |
| `pdf-parser-comparison/compare_parsers.py` | 比較三個 PDF 解析套件的抽取品質（ADR 0005） |
| `table2-chunking/measure_table2_rows.py` | 量切塊方法會不會把表格切散（ADR 0007） |
| `table-generalization/check_cells.py` | 把系統讀出的表格每一格對回標準答案，驗證表格改寫是否泛化到其他論文 |
| `retrieval-parameters/analyse.py` | 彙整切塊大小 × Top-K × 向量／混合檢索 × 相似度門檻的實驗（ADR 0010；`make eval`） |
| `number-check/replay.py`、`answer-checks/replay.py` | 用存下來的真實回答重放數字核對與句級檢查，量誤報與漏報 |
| `facts-ab/judge.py` | 事實塊開與關的對照實驗的機械檢查 |
| `navigator-abc/analyse.py` | 單輪與導航模式對照實驗的指標彙整 |
| `stability/judge.py`、`judge_conversation.py` | 同一題重複多次、同一對話多題的穩定性批次的機械檢查 |

這些程式讀寫的資料檔不在版控內，所以從 repo 取出後無法直接重跑；判定一律人工逐句對原文，程式只做機械檢查（數字是否出現、配對是否相加為 100 等）。
