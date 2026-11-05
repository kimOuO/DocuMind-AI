# PDF 解析器比較：實驗結果

由 `compare_parsers.py` 產生。文件：`2410.05779v3.pdf`（16 頁）。
標準答案來自論文的 LaTeX 原始檔，與受測的解析器無關。

## 受測設定

| 設定 | 呼叫方式 | 套件版本 |
|---|---|---|
| pymupdf-default | `page.get_text()` | pymupdf 2.1 |
| pymupdf-sorted | `page.get_text(sort=True)` | pymupdf 2.1 |
| pypdf-default | `page.extract_text()` | pypdf 6.21.4 |
| pypdf-layout | `page.extract_text(extraction_mode="layout")` | pypdf 6.21.4 |
| pdfplumber-default | `page.extract_text()` | pdfplumber 0.11.10 |
| pdfplumber-xtol1 | `page.extract_text(x_tolerance=1)` | pdfplumber 0.11.10 |

## 內文：段落是否完整、順序是否正確

| 設定 | 段落找得到 | 單字邊界完整 | 順序錯置 | 標題找得到 | 標題文字完整 |
|---|---|---|---|---|---|
| pymupdf-default | 70/70 | 69/70 | 0 | 22/22 | 22/22 |
| pymupdf-sorted | 69/70 | 68/70 | 0 | 22/22 | 22/22 |
| pypdf-default | 70/70 | 69/70 | 0 | 22/22 | 0/22 |
| pypdf-layout | 68/70 | 67/70 | 0 | 22/22 | 21/22 |
| pdfplumber-default | 69/70 | 11/70 | 0 | 22/22 | 7/22 |
| pdfplumber-xtol1 | 69/70 | 68/70 | 0 | 22/22 | 22/22 |

## Table 2：數值與列、欄的對應

| 設定 | 頁碼 | 數值出現在頁面上 | 數值在正確的列與欄位置 | 完整的列 | 整列在同一行 | 區塊標題正確 | 資料集標題正確 | 整張表順序完全正確 |
|---|---|---|---|---|---|---|---|---|
| pymupdf-default | 8 | 128/128 | 128/128 | 16/16 | 0/16 | 4/4 | 是 | 是 |
| pymupdf-sorted | 8 | 128/128 | 128/128 | 16/16 | 16/16 | 4/4 | 是 | 是 |
| pypdf-default | 8 | 128/128 | 128/128 | 16/16 | 16/16 | 4/4 | 是 | 是 |
| pypdf-layout | 8 | 128/128 | 61/128 | 7/16 | 7/16 | 2/4 | 否 | 否 |
| pdfplumber-default | 8 | 128/128 | 128/128 | 16/16 | 16/16 | 4/4 | 是 | 是 |
| pdfplumber-xtol1 | 8 | 128/128 | 128/128 | 16/16 | 16/16 | 4/4 | 是 | 是 |

## 頁碼

| 設定 | 頁數 | 頁尾印的頁碼與頁序相符 | 不相符的頁 |
|---|---|---|---|
| pymupdf-default | 16 | 15/16 | [1] |
| pymupdf-sorted | 16 | 16/16 | 無 |
| pypdf-default | 16 | 15/16 | [1] |
| pypdf-layout | 16 | 12/16 | [7, 8, 9, 16] |
| pdfplumber-default | 16 | 15/16 | [1] |
| pdfplumber-xtol1 | 16 | 15/16 | [1] |

## 文字品質與解析時間

| 設定 | 字元數 | 無法解碼的字元 | 未展開的連字 | (cid:) 佔位 | 超過 30 字元的字串 | 解析時間中位數（毫秒） | 最短–最長 |
|---|---|---|---|---|---|---|---|
| pymupdf-default | 61133 | 0 | 0 | 0 | 0 | 47.6 | 46.6–53.8 |
| pymupdf-sorted | 90850 | 0 | 0 | 0 | 0 | 398.0 | 394.4–415.6 |
| pypdf-default | 61179 | 0 | 0 | 0 | 0 | 487.9 | 472.3–505.1 |
| pypdf-layout | 70096 | 0 | 0 | 0 | 0 | 476.9 | 458.0–481.9 |
| pdfplumber-default | 56253 | 0 | 0 | 4 | 577 | 1722.4 | 1712.1–1756.7 |
| pdfplumber-xtol1 | 62235 | 0 | 0 | 4 | 0 | 1785.2 | 1753.6–1834.0 |

## 表格偵測 API（補充）

| 方法 | 偵測到的表格數 | 還原成「指標＋8 個數值」的列 |
|---|---|---|
| pdfplumber extract_tables() [lines] | 0 | 0/16 |
| pdfplumber extract_tables() [text] | 1 | 16/16 |
| pymupdf find_tables() [lines] | 1 | 0/16 |
| pymupdf find_tables() [text] | 1 | 0/16 |
| pypdf | — | no table detection API |

## 授權與安裝大小

| 套件 | 版本 | 授權 | 連同相依的安裝大小（MB） | 相依套件（授權） |
|---|---|---|---|---|
| pymupdf | 2.1 | Dual Licensed - GNU AFFERO GPL 3.0 or Artifex Commercial License | 283.4 | networkx 3.7（BSD-3-Clause）；numpy 2.5.4（BSD-3-Clause AND 0BSD AND MIT AND Zlib AND CC0-1.0）；onnxruntime 1.31.1（MIT License）；PyYAML 6.0.3（MIT License）；pymupdf_layout 2.1（unknown）；psutil 7.2.2（BSD-3-Clause）；tabulate 0.10.0（MIT）；pymupdf4llm 2.1（unknown）；flatbuffers 25.12.19（Apache Software License）；packaging 26.3（Apache-2.0 OR BSD-2-Clause）；protobuf 7.36.2（3-Clause BSD License） |
| pypdf | 6.21.4 | BSD-3-Clause | 4.2 | typing_extensions 4.16.0（PSF-2.0） |
| pdfplumber | 0.11.10 | MIT License | 58.9 | pdfminer.six 20260107（MIT）；pillow 13.0.0（MIT-CMU）；pypdfium2 5.14.0（BSD-3-Clause, Apache-2.0, dependency licenses）；charset-normalizer 3.5.2（MIT）；cryptography 50.0.2（Apache-2.0 OR BSD-3-Clause）；cffi 2.1.1（MIT-0）；typing_extensions 4.16.0（PSF-2.0）；pycparser 3.12（BSD-3-Clause） |

## 各設定的細節

### pymupdf-default

- 找不到的段落（0）：無
- 單字邊界不完整的段落（1）：`further gathers neighboring nodes within the local subgraphs`
- 文字不完整的標題（0）：無

### pymupdf-sorted

- 找不到的段落（1）：`we examine the number of tokens and API`
- 單字邊界不完整的段落（1）：`further gathers neighboring nodes within the local subgraphs`
- 文字不完整的標題（0）：無

### pypdf-default

- 找不到的段落（0）：無
- 單字邊界不完整的段落（1）：`further gathers neighboring nodes within the local subgraphs`
- 文字不完整的標題（22）：`1 Introduction`；`2 Retrieval-Augmented Generation`；`3 The LightRAG Architecture`；`3.1 Graph-based Text Indexing`；`3.2 Dual-level Retrieval Paradigm`；`3.3 Retrieval-Augmented Answer Generation`

### pypdf-layout

- 找不到的段落（2）：`we examine the number of tokens and API`；`communities actively utilized for retrieval in this experiment`
- 單字邊界不完整的段落（1）：`further gathers neighboring nodes within the local subgraphs`
- 文字不完整的標題（1）：`7.4 Case Study: Comparison Between LightRAG and the Baseline NaiveRAG`
- Table 2 第一個不符的位置：第 0 個字串，預期 `Agriculture`，實際 `•`

### pdfplumber-default

- 找不到的段落（1）：`we examine the number of tokens and API`
- 單字邊界不完整的段落（58）：`systems have been developed to enhance large language`；`existing RAG systems have key limitations that hinder`；`a model that seamlessly integrates a graph-based text`；`the key contributions of this work are highlighted`；`We emphasize the importance of developing a graph-empowered`
- 文字不完整的標題（15）：`3.1 Graph-based Text Indexing`；`3.2 Dual-level Retrieval Paradigm`；`3.3 Retrieval-Augmented Answer Generation`；`3.4 Complexity Analysis of the LightRAG Framework`；`4.1 Experimental Settings`；`4.2 Comparison of LightRAG with Existing RAG Methods (RQ1)`
- 過長字串的例子：`culturalsignificance,collaboration,andlegalframeworks,includ`；`Thisdual-levelretrievalparadigmnotonlyfacilitatesefficientre`；`partnerships.Corporationsmustadoptrespectful,inclusivepracti`

### pdfplumber-xtol1

- 找不到的段落（1）：`we examine the number of tokens and API`
- 單字邊界不完整的段落（1）：`further gathers neighboring nodes within the local subgraphs`
- 文字不完整的標題（0）：無

## 各設定之間的頁碼一致性

每個找得到的標題，在所有設定中都落在同一頁。

## 排除的錨點

0 個錨點在所有設定中都找不到，視為 LaTeX 原始檔中有、但未出現在 PDF 內文的文字，不列入計分：無
