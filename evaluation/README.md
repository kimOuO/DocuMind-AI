# evaluation — 實驗、標準答案與評測

讓參數與選型的決定有實驗數據可引用（`CLAUDE.md`：參數類決定必須引用這裡的數據）。

## 內容

| 資料夾 | 是什麼 | 結論／用途 | 依據 |
|---|---|---|---|
| `ground-truth/` | 共用的標準答案：論文的 Table 2（128 格）與 22 個章節標題；三個必答題的關鍵事實 | 所有實驗與 P3、P4 的驗收都對照它 | 取自論文的 LaTeX 原始檔；關鍵事實待使用者確認 |
| `pdf-parser-comparison/` | 實驗：三個 PDF 解析套件、六種設定的抽取品質 | 採用 pypdf 預設模式 | ADR 0005、決策日誌 D54 |
| `table2-chunking/` | 實驗：切塊方法對 Table 2 的影響 | 目前的固定長度切塊是 AC-14 的比較基準；P3 的新方法在這裡對照 | 決策日誌 D57 |

P4 會加入：題庫與評測腳本（`retrieval-parameters/`：chunk size × Top-K × Vector／Hybrid）。

## 命名規則

- **一個實驗一個資料夾**。資料夾內：`README.md`（方法、彙整表、結論）、一支統一的測試程式、`requirements.txt`（只有實驗用、不進專案的套件時）。
- **每個比較對象一個結果檔**，檔名說出比較對象：同一個套件的不同設定放在以套件命名的子資料夾（`pypdf/default.json`、`pypdf/layout.json`）；同一種量測、不同方法的結果用 `<方法>.<量測內容>.json`（`fixed-size-400-80.table2-rows.json`）。
- **結果檔自己說明自己**：第一段是設定（`config` 或 `method`：套件、版本、呼叫方式或參數），之後才是數據。
- 結果檔都能由統一的測試程式重新產生；重現方式寫在各資料夾的 `README.md`。
- 標準答案放 `ground-truth/`，不放在任何實驗底下。
