# 表格模組的泛化驗證（D87 後續，2026-11-07）

使用者：「泛化那個我認為要做 不然就是對這篇論文的過擬和」。本資料夾記錄表格偵測→逐列改寫→矩陣這條線在**第二篇論文**上的逐格驗證。

- `check_cells.py`：解析兩篇 PDF、偵測表格、逐列改寫、以 `cells_of` 讀回每一格，與 LaTeX 原始檔建的 ground truth 逐格比對（`ground-truth/paper-structure.json`、`ground-truth/graphrag-structure.json`，後者由 `ground-truth/build_graphrag_structure.py` 從 arXiv e-print 2404.16130v2 產生）。寫 `results.json`。
- 比對的是 (表、列、群組、欄、值) 的集合；同值同標籤的重複格只算一次（LightRAG 兩表 128 格各有 3 格重複，所以是 125）。

## 修正前（commit `b8d95ea`）

逐列改寫只處理「兩層欄頭、每群恰好兩個子欄」：

| 表 | 形狀 | 矩陣格數 |
|---|---|---|
| LightRAG Table 1、2 | 兩層欄頭、每群 2 子欄、多區塊 | 128、128 |
| LightRAG Table 4 | 單層欄頭、首欄名在表頭 | 8 |
| GraphRAG Table 2 | 兩層欄頭、**群組名兩個字**、每群 5 子欄 | **0** |
| GraphRAG Table 3 | **跨欄總標題**＋兩個字的欄名 | **0** |
| GraphRAG Table 4 | 6 欄、**數值列標籤**（0.5…）、**分段列**（News Articles） | **0** |
| GraphRAG Table 6 | 成對比較：**兩個列標籤欄**（Condition 1／2）、每群 4 子欄（Mean 1、Mean 2、Z、p）、指標分段列、`<0.001` | **0** |

## 修正後（`app/ingestion/tables.py`）

- 欄位配置由**列**決定（最常見的數字個數），不只看表頭字數。
- 兩層欄頭：子欄名在每群重複一次（「NaiveRAG LightRAG」×4、「Mean 1 Mean 2 Z p」×2），用重複性判定群數，群組名可多字；子欄行前面多出的名字（「Condition 1 Condition 2」）是列標籤欄，數量須等於列的標籤字數。
- 單層欄頭：欄名可多字（字數是數字個數的倍數時等分）；跨欄總標題（「Condition | Average Number of Claims」）不當群組。
- 數值列標籤：整行皆數字且比欄數多一個時，第一個是列標籤。
- 分段列：列之間只有文字的短行（≤ 6 字）是其下各列的群組（單層表）或列標籤前綴（兩層表，「Comprehensiveness / C0 TS」）。緊鄰第一列的表頭行若無法當欄名，也視為分段列。
- 表頭裡的純整數接在前一個字後面（「Mean 1」），`<0.001` 算數字。

## 逐格結果（`check_cells.py`）

| 論文 | 表 | ground truth 格 | 解析得到 | 相符 | 漏 | 錯／多 |
|---|---|---|---|---|---|---|
| LightRAG | Table 1 | 125 | 125 | **125** | 0 | 0 |
| LightRAG | Table 2 | 125 | 125 | **125** | 0 | 0 |
| GraphRAG | Table 2 | 30 | 30 | **30** | 0 | 0 |
| GraphRAG | Table 3 | 12 | 12 | **12** | 0 | 0 |
| GraphRAG | Table 4 | 48 | 48 | **48** | 0 | 0 |
| GraphRAG | Table 6 | 480 | 480 | **480** | 0 | 0 |

LightRAG Table 4（8 格）沒有 LaTeX ground truth，未列。單元測試新增四種形狀各一條（`tests/unit/test_tables.py`）；原有測試全部維持。

## 比較事實與核對（`app/chat/evidence.py`、`verification.py`）

- 每群三欄以上的列沒有「配對」：只有在問題點名其中一欄時，才把該欄與同列其他欄比較（setting「same row」）。不點名就不比，因為同列的欄可能是不同量（Mean 1 與 Z-value）。
- 問題點名資料集（群組）或指標（列）時，事實縮到那個條件（R1 的 T3 退步：176 條事實→1 條）。點名要用表格的寫法（「Podcast Transcripts」而非「Podcast」），三個字元以下與純數字的標籤不比對。
- 標籤核對對多欄列沒有配對條件，只核對列、群、欄三個標籤。

## 仍不支援或未驗證（誠實陳述）

- 合併儲存格、超過兩層的欄頭、多層列名、跨頁表、沒有「Table N」標題的表、PyMuPDF 抽字時欄位順序被打亂的表、圖片表。
- Table 6 的「Mean 1 對 Mean 2」是同列不同欄的比較，沒有被當成一對（兩欄名不同），所以沒有方向與例外事實；G2 這類題仍靠模型讀表。
- 驗證範圍是兩篇論文六張表、五種形狀；「泛化」指的是這五種形狀，不是任意表格。
