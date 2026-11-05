# evaluation — 檢索與回答品質的評測

用一組標準問題量測系統回答得好不好，讓 chunk size、Top-K、是否用 Hybrid Search 等選擇有實驗數據依據。

目前有：

- `pdf-parser-comparison/`：PDF 解析套件的比較實驗（PyMuPDF、pypdf、pdfplumber），是選用 pypdf 的依據。
- `table2-chunking/`：目前的切塊方式如何切開論文的 Table 2，是 AC-14（P3）的比較基準。

P4 階段會加入：

- 題庫：必答三題、細節事實題、表格數字題、跨文件題、無答案題。
- 評測腳本與實驗設定。
- 實驗報告：Recall@K、來源命中率、回答正確性、拒答率、10K 合規率。
