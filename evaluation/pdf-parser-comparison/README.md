# PDF 解析器比較

比較 PyMuPDF、pypdf、pdfplumber 三個本地 PDF 解析套件，決定專案採用哪一個。只比較解析層：不切塊、不嵌入、不呼叫 LLM。

- 實驗日期：2026-11-05
- 受測文件：`sample-documents/2410.05779v3.pdf`（LightRAG 論文，16 頁，單欄）
- 補充文件：arXiv:1810.04805v2（BERT 論文，16 頁，雙欄），只用來測雙欄的閱讀順序，不放進專案
- 完整數據：每個比較對象一個檔，`<套件>/<設定>.json`（`pymupdf/default.json`、`pymupdf/sorted.json`、`pypdf/default.json`、`pypdf/layout.json`、`pdfplumber/default.json`、`pdfplumber/x-tolerance-1.json`）。檔內先是 `config`（套件、版本、呼叫方式、授權、相依），再是單欄論文與雙欄論文的結果

## 為什麼做這個實驗

規格原本指定 PyMuPDF。它的授權是 AGPL-3.0 或商業授權；專案若公開散布，需要以 AGPL 相容的方式開源。另外兩個候選的授權較寬鬆（pypdf：BSD-3-Clause；pdfplumber：MIT），但抽取品質需要實測，尤其是題目指定的 Table 2。

## 方法

**標準答案與受測的解析器無關。** 取自 arXiv 提供的同一版論文的 LaTeX 原始檔，由 `../ground-truth/build_paper_structure.py` 產生 `../ground-truth/paper-structure.json`：

| 項目 | 內容 | 數量 |
|---|---|---|
| Table 2 | 每一格的區塊、指標、資料集、系統、數值 | 128 格（4 區塊 × 4 指標 × 8 欄） |
| 標題 | 章與節的標題，依文件順序，含編號 | 22 個 |
| 段落錨點 | 每個內文段落取一段連續 8 個單字，依文件順序 | 70 個 |

**每個套件測兩種設定**：預設呼叫，以及一個合理的調整：

| 設定 | 呼叫方式 |
|---|---|
| `pymupdf/default` | `page.get_text()` |
| `pymupdf/sorted` | `page.get_text(sort=True)` |
| `pypdf/default` | `page.extract_text()` |
| `pypdf/layout` | `page.extract_text(extraction_mode="layout")` |
| `pdfplumber/default` | `page.extract_text()` |
| `pdfplumber/x-tolerance-1` | `page.extract_text(x_tolerance=1)` |

**檢查項目**

| 檢查 | 判定方式 |
|---|---|
| 段落找得到 | 錨點在抽出的文字中出現（忽略空白、換行、連字號） |
| 單字邊界完整 | 錨點的 8 個單字以完整單字的形式依序出現（單字沒有黏在一起或被拆開） |
| 閱讀順序 | 錨點出現的先後與 LaTeX 中的先後一致；不一致的數量即「順序錯置」 |
| 標題 | 帶編號的標題找得到；標題的單字完整 |
| 頁碼 | 頁數；頁尾印的頁碼與頁序相符；每個標題在各設定中落在同一頁 |
| Table 2 | 表格標題之後的文字切成字串，**每個數值必須出現在它的列標籤與欄順序所指定的位置**才算正確，不只是出現在頁面上 |
| 文字品質 | 無法解碼的字元、未展開的連字、`(cid:)` 佔位、超過 30 字元的字串（單字黏在一起的徵兆） |
| 解析時間 | 開檔並抽出全部頁面，重複 5 次取中位數 |
| 授權與大小 | 套件與其相依的授權、安裝後的大小 |

## 結果摘要

### LightRAG 論文（單欄）

| 設定 | 段落找得到 | 單字完整 | 順序錯置 | 標題文字完整 | Table 2 數值位置正確 | Table 2 整列在同一行 | 時間（毫秒） |
|---|---|---|---|---|---|---|---|
| pymupdf/default | 70/70 | 69/70 | 0 | 22/22 | 128/128 | 0/16 | 48 |
| pymupdf/sorted | 69/70 | 68/70 | 0 | 22/22 | 128/128 | 16/16 | 398 |
| **pypdf/default** | **70/70** | **69/70** | **0** | **0/22** | **128/128** | **16/16** | **488** |
| pypdf/layout | 68/70 | 67/70 | 0 | 21/22 | 61/128 | 7/16 | 477 |
| pdfplumber/default | 69/70 | 11/70 | 0 | 7/22 | 128/128 | 16/16 | 1722 |
| pdfplumber/x-tolerance-1 | 69/70 | 68/70 | 0 | 22/22 | 128/128 | 16/16 | 1785 |

- **頁碼**：六種設定都是 16 頁，22 個標題在所有設定中都落在同一頁。第 1 頁頁尾的比對不符，是因為頁面側邊的 arXiv 浮水印被排在頁碼之後，不是頁碼錯誤。
- **所有設定都少 1 個「單字完整」**：`LightRAGfurther gathers…`。PDF 本身就少一個空白（LaTeX 巨集吃掉了空白），不是解析器的錯誤。
- **文字編碼**：三個套件都沒有無法解碼的字元或未展開的連字。pdfplumber 在數學式有 4 個 `(cid:)` 佔位，並把第 1 頁側邊的浮水印讀成倒過來的字串（`3v97750.0142:viXra`）。

### 雙欄論文（BERT）

| 設定 | 段落找得到 | 單字完整 | 順序錯置 |
|---|---|---|---|
| pymupdf/default | 66/66 | 66/66 | 2 |
| pymupdf/sorted | 17/66 | 15/66 | 4 |
| **pypdf/default** | **66/66** | **66/66** | **2** |
| pypdf/layout | 13/66 | 11/66 | 3 |
| pdfplumber/default | 16/66 | 6/66 | 4 |
| pdfplumber/x-tolerance-1 | 16/66 | 13/66 | 4 |

- PyMuPDF 與 pypdf 的預設模式依 PDF 內部的內容順序輸出，雙欄讀得正確。兩者錯置的是同樣的 2 個段落（都在第 5 頁）；原因沒有進一步查證。
- pdfplumber 與兩個「依位置排序」的模式是由上到下、由左到右逐行輸出，會把左右兩欄的同一行接在一起，段落因此被打散。

### 表格偵測 API（補充）

| 方法 | 還原出的列（指標＋8 個數值） |
|---|---|
| pdfplumber `extract_tables()`，以文字對齊偵測 | 16/16 |
| pdfplumber `extract_tables()`，以線條偵測（預設） | 0/16（沒有偵測到表格） |
| PyMuPDF `find_tables()`（兩種策略） | 0/16（偵測到表格，但數值被拆成 `324%` 與 `.` 兩行） |
| pypdf | 沒有表格偵測 API |

### 授權與安裝大小

| 套件 | 授權 | 連同相依的安裝大小 | 備註 |
|---|---|---|---|
| PyMuPDF 2.1 | AGPL-3.0 或商業授權 | 283.4 MB | 相依含 `onnxruntime`、`numpy`、`networkx`、`pymupdf_layout`、`pymupdf4llm`；後兩者的套件資料沒有標示授權 |
| pypdf 6.21.4 | BSD-3-Clause | 4.2 MB | 純 Python，唯一的相依是 `typing_extensions` |
| pdfplumber 0.11.10 | MIT | 58.9 MB | 相依含 `pdfminer.six`、`pillow`、`pypdfium2`、`cryptography` |

## 觀察

1. **Table 2**：三個套件的預設模式都能讓 128 個數值落在正確的列與欄位置。差別在排版：pypdf 與 pdfplumber 一列一行（`Comprehensiveness 32.4% 67.6% …`）；PyMuPDF 預設是一格一行，順序正確但列的結構要靠順序推回來。
2. **pypdf 的弱點是小型大寫字的標題**：22 個標題與論文標題都被拆開（`1 I NTRODUCTION`、`3 T HE LIGHT RAG A RCHITECTURE`）。編號與標題所在的頁都正確，內文不受影響。只處理「編號開頭、全大寫」的行可以修回 15/22；剩下 7 個是 `LIGHT RAG`、`LLM S` 這類無法由規則判斷的拆分。
3. **pdfplumber 需要調整參數才可用**：預設會把單字黏在一起（577 個超過 30 字元的字串）；調整後內文正常，但雙欄的閱讀順序錯誤，而且最慢。
4. **「依位置排序」的模式不適合當預設**：在雙欄文件與文字繞圖的區域（LightRAG 論文第 9 頁）都會把左右的內容交錯。
5. **解析時間都不是瓶頸**：最慢的也在 2 秒內解析完 16 頁。

## 建議

採用 **pypdf 的預設模式**。

- 內文、閱讀順序（單欄與雙欄）、頁碼、Table 2 的列欄對應都達標，Table 2 還保留一列一行的結構。
- 授權是 BSD-3-Clause，沒有散布上的限制；安裝大小 4.2 MB，是三者中最小的。
- 代價：標題的文字不完整（見觀察 2）、沒有表格偵測 API、比 PyMuPDF 慢約 10 倍（16 頁 0.5 秒）。
- 不選 pdfplumber：雙欄的閱讀順序錯誤。
- 不選 PyMuPDF：品質最好的是標題與速度，但這兩項不足以抵過 AGPL 與 283 MB 的相依。

## 決定

採用 pypdf（使用者決定，2026-11-05）。標題被拆開的限制列入架構決策紀錄 `docs/03-decisions/0005-pdf-parser-pypdf.md`；章節摘要實作前要先有標題辨識與正規化的測試（驗收條件 AC-53）。

## 限制

- 只測了兩份文件，都是以 LaTeX 產生、內嵌文字的學術論文。掃描檔（圖片）三個套件都抽不出文字，不在這次比較範圍。
- LightRAG 論文附錄中以圖片呈現的 prompt（Figure 4–7）三個套件都抽不到，屬於已知限制。
- 沒有評估解析結果對檢索與回答品質的影響；那是 P3、P4 的工作。

## 重現方式

```bash
# 三個套件裝到獨立的目錄，不裝進專案的 venv
.venv/bin/pip install --target /tmp/pdf-libs -r evaluation/pdf-parser-comparison/requirements.txt

# 標準答案已附在 ../ground-truth/paper-structure.json；重新產生的方式見 ../ground-truth/README.md

# 比較（只有單欄論文）
.venv/bin/python evaluation/pdf-parser-comparison/compare_parsers.py sample-documents/2410.05779v3.pdf --libs /tmp/pdf-libs

# 加上雙欄論文的閱讀順序檢查：另外下載該論文的 PDF 與 LaTeX 原始檔，依 main.tex 的 \\input 順序列出內文的 .tex
curl -L -o /tmp/bert.pdf https://arxiv.org/pdf/1810.04805v2
curl -L -o /tmp/bert-src.tar.gz https://arxiv.org/e-print/1810.04805v2
mkdir -p /tmp/bert-src && tar -xzf /tmp/bert-src.tar.gz -C /tmp/bert-src --wildcards '*.tex'
.venv/bin/python evaluation/pdf-parser-comparison/compare_parsers.py sample-documents/2410.05779v3.pdf --libs /tmp/pdf-libs \\
  --two-column-pdf /tmp/bert.pdf \\
  --two-column-tex /tmp/bert-src/intro.tex /tmp/bert-src/related.tex /tmp/bert-src/bert.tex /tmp/bert-src/experiment.tex /tmp/bert-src/ablation.tex /tmp/bert-src/conclusion.tex
```
