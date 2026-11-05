# 共用的標準答案

| 檔案 | 內容 | 來源 | 用在哪 |
|---|---|---|---|
| `paper-structure.json` | 論文 Table 2 的 128 格（區塊、指標、資料集、系統、數值）、22 個章節標題（依序）、70 個內文段落的錨點 | 論文的 LaTeX 原始檔（arXiv e-print 2410.05779v3），由 `build_paper_structure.py` 產生，與任何 PDF 解析器無關 | `pdf-parser-comparison/`、`table2-chunking/`、P3 的標題辨識測試（AC-53）、關鍵事實的 Table 2 數字 |
| `key-facts.md` | 三個必答題的關鍵事實：必要、加分、不應出現，各附頁碼與原文依據 | 依論文原文與 `docs/02-specs/04-use-cases.md` 整理 | AC-12、AC-13、AC-14 的判定；P4 的題庫 |
| `key-facts.json` | 同上的機器可讀版 | 同上 | P3 驗收與 P4 評測的腳本 |

`key-facts` 目前是草稿，待使用者確認後才作為驗收依據。

重新產生 `paper-structure.json`：

```bash
curl -L -o /tmp/lightrag-src.tar.gz https://arxiv.org/e-print/2410.05779v3
mkdir -p /tmp/lightrag-src && tar -xzf /tmp/lightrag-src.tar.gz -C /tmp/lightrag-src --wildcards '*.tex'
.venv/bin/python evaluation/ground-truth/build_paper_structure.py /tmp/lightrag-src
```
