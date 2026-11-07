# P4 題庫（AC-18）

共 19 題：必答 3、細節 4、表格數字 3、GraphRAG 4（含 G1、G2）、跨文件 2、無答案 3。證據為原始文件的逐字原文（pypdf 抽取、空白正規化），以文件與頁碼標註，不用切塊編號。`keyword_type` 標記含專有名詞、表格標題或精確數字的題目，Hybrid 實驗另外統計。機器可讀版：`question-set.json`。

| 編號 | 類型 | 問題 | 文件 | 關鍵字型 | 證據（文件 p頁：原文開頭…） | 預期 |
|---|---|---|---|---|---|---|
| Q1 | required | summary this document. | lightrag |  | lightrag p1：To address these challenges, we propose LightRAG, which incorporates g… | 依 key-facts.md 的 Q1 標準（S1–S5）；檢索指標不適用，走摘要路徑 |
| Q2 | required | compare lightRAG with GraphRAG | lightrag |  | lightrag p7：GraphRAG LightRAG GraphRAG LightRAG GraphRAG LightRAG GraphRAG LightRA…<br>lightrag p7：LightRAG’s Superiority over GraphRAG: While both LightRAG and GraphRAG…<br>lightrag p9：In the retrieval phase, GraphRAG generates 1,399 communities, with 610…<br>lightrag p10：When a new dataset of the same size as the legal dataset is introduced… | 依 key-facts.md 的 Q2 標準（C1–C7） |
| Q3 | required | Performance of ablated versions of LightRAG | lightrag |  | lightrag p8：Table 2: Performance of ablated versions of LightRAG, using NaiveRAG a…<br>lightrag p8：• Low-level-only Retrieval: The -High variant removes high-order retri… | 依 key-facts.md 的 Q3 標準（A1–A6） |
| D1 | detail | LightRAG 的實驗用了哪些資料集？它們來自哪個 benchmark？ | lightrag | 是 | lightrag p5：we selected four datasets from the UltraDomain benchmark (Qian et al.,… | UltraDomain benchmark（428 本大學教科書、18 個領域）；Agriculture、CS、Legal、Mix 四個資料集 |
| D2 | detail | Which LLM and chunk size does LightRAG use in its experiments? | lightrag | 是 | lightrag p6：For all LLM-based operations in LightRAG, we default to using GPT-4o-m… | GPT-4o-mini；chunk size 1200；gleaning 1 |
| D3 | detail | LightRAG 用哪四個評估面向比較回答品質？各是什麼意思？ | lightrag |  | lightrag p6：In total, we utilize four evaluation dimensions, including: i) Compreh… | Comprehensiveness、Diversity、Empowerment、Overall，各附論文的定義 |
| D4 | detail | Why is GraphRAG inefficient at incorporating newly added data, and how does LightRAG handle incremental updates? | lightrag |  | lightrag p10：However, GraphRAG shows significant inefficiency in managing newly add… | GraphRAG 須拆掉社群結構重建，約 1,399 × 2 × 5,000 tokens；LightRAG 把新實體與關係併入既有圖，不必重建 |
| T1 | table | Legal 資料集總共有多少 tokens？有幾份文件？ | lightrag | 是 | lightrag p13：Statistics Agriculture CS Legal Mix Total Documents 12 10 94 61 Total … | 5,081,069 tokens；94 份文件 |
| T2 | table | In the Legal dataset, what are the Diversity win rates of NaiveRAG versus LightRAG? | lightrag | 是 | lightrag p7：NaiveRAG LightRAG NaiveRAG LightRAG NaiveRAG LightRAG NaiveRAG LightRA… | NaiveRAG 13.6%、LightRAG 86.4%（Legal 是第三個資料集欄） |
| T3 | table | CS 資料集上 -High 變體與 NaiveRAG 的 Overall 勝率各是多少？ | lightrag | 是 | lightrag p8：NaiveRAG -High NaiveRAG -High NaiveRAG -High NaiveRAG -High Comprehens… | NaiveRAG 44.0%、-High 56.0% |
| G1 | detail | How many context units and tokens do the root-level community summaries (C0) and the source-text summarization (TS) use on the Podcast and News datasets? | graphrag | 是 | graphrag p10：TS Units 34 367 969 1310 1669 55 555 1797 2142 3197 Tokens 26657 22575… | 依 graphrag-key-facts.md 的 G1 標準：Podcast C0 34／26,657、TS 1,669／1,014,611；News C0 55／39,770、TS 3,197／1,707,694 |
| G2 | detail | Compare condition C2 with vector RAG (SS) on comprehensiveness in the Podcast and News datasets | graphrag |  | graphrag p26：77.76…<br>graphrag p9：global approaches signifi- cantly outperformed conventional vector RAG… | 依 graphrag-key-facts.md 的 G2 標準 |
| G3 | table | GraphRAG 論文中，Podcast 與 News 資料集建出的圖各有多少節點與邊？ | graphrag | 是 | graphrag p9：The indexing process resulted in a graph consisting of 8,564 nodes and… | Podcast 8,564 節點、20,691 邊；News 15,754 節點、19,520 邊 |
| G4 | detail | What six conditions does the GraphRAG paper compare, and what does each use to answer queries? | graphrag |  | graphrag p8：We compared six conditions including GraphRAG at four different graph … | C0–C3 四個社群層級的摘要、TS 對原文做 map-reduce、SS 向量檢索 |
| X1 | cross | 兩篇論文各用哪個 LLM 做實驗？ | lightrag, graphrag | 是 | lightrag p6：For all LLM-based operations in LightRAG, we default to using GPT-4o-m…<br>graphrag p9：using a public OpenAI endpoint for gpt-4-turbo (2M TPM, 10k RPM).… | LightRAG 論文：GPT-4o-mini；GraphRAG 論文：gpt-4-turbo。兩份文件都要引用 |
| X2 | cross | How large (in tokens) are the corpora each paper evaluates on? | lightrag, graphrag | 是 | lightrag p5：Each dataset contains between 600,000 and 5,000,000 tokens…<br>graphrag p8：This corpus was divided into 1669 × 600-token text chunks, with 100-to…<br>graphrag p8：The corpus is divided into 3197 × 600-token text chunks, with 100-toke… | LightRAG：每個資料集 60 萬到 500 萬 tokens（Table 4 有各別數字）；GraphRAG：Podcast 約 100 萬、News 約 170 萬。兩份文件都要引用 |
| N1 | none | LightRAG 在 MS MARCO 上的 BLEU 分數是多少？ | lightrag |  | （無；預期拒答） | 文件沒有 MS MARCO 或 BLEU；應回覆找不到，不給數字 |
| N2 | none | What does GPT-4o-mini cost per million tokens according to the paper? | lightrag |  | （無；預期拒答） | 論文沒有價格；應回覆找不到 |
| N3 | none | 如何在家烤酸種麵包？ | lightrag, graphrag |  | （無；預期拒答） | 與文件無關；應回覆找不到（AC-15 的既有例題） |

備註：D4 原本的英文問法會讓 Ollama 的 bge-m3 回傳 NaN（HTTP 500），系統端以 EmbeddingInputError 回報；題庫改用另一種問法，原句記在 JSON 的 `note`。
