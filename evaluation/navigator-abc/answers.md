# navigator-abc — 45 次執行的完整回答

由 `analyse.py` 從 `runs/*.json` 產生。每則列出：來源（頁碼與來路）、B 臂的閱讀計畫、最終回答全文、確定性檢查的結果。人工判定在 `README.md`。

## A-Q1-1

- 問題：`summary this document.`；模式 `roles`；28.8 秒；1 次呼叫；tokens 4928
- 來源：[1] p1 summary, [2] p1 summary, [3] p1 summary, [4] p2 summary, [5] p3 summary, [6] p5 summary, [7] p10 summary, [8] p10 summary, [9] p13 summary
- 檢查：標籤不符 ['54.4%']；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 ['13,990,000']

```text
Navigator: The document's Front matter, INTRODUCTION, RETRIEVAL-AUGMENTED GENERATION, THE LIGHT RAG ARCHITECTURE, and EVALUATION sections bear on the question. These sections describe the problem addressed, the proposed solution, and the evaluation of LightRAG.

Analyst: The document introduces LightRAG, a novel Retrieval-Augmented Generation (RAG) system designed to improve the accuracy and efficiency of large language models by integrating external knowledge sources through graph-based indexing [1]. The problem addressed is the limitations of existing RAG systems, such as flat data representations and inadequate contextual awareness, which lead to fragmented and incomplete responses [1]. LightRAG addresses this by using a dual-level retrieval framework that captures both specific and abstract information and supports fast adaptation to new data [1]. 

The system segments documents into manageable chunks, uses an LLM to extract entities and relationships, and builds a knowledge graph. This graph structure enhances keyword matching and captures high-order relatedness from neighboring nodes [5]. The dual-level retrieval mechanism enables low-level retrieval of specific entities and high-level retrieval of broader topics [1]. During answer generation, the LLM integrates the retrieved information to produce contextually relevant responses [5].

Experiments conducted across four datasets—Agriculture, CS, Legal, and Mix—show that LightRAG outperforms existing RAG methods such as NaiveRAG, RQ-RAG, HyDE, and GraphRAG in four evaluation dimensions: Comprehensiveness, Diversity, Empowerment, and Overall [6]. For example, in the Legal dataset, LightRAG achieves an 83.6% win rate in Comprehensiveness, significantly higher than NaiveRAG’s 16.4% [6]. In the Agriculture dataset, LightRAG achieves 67.6% in Comprehensiveness compared to GraphRAG’s 54.4% [6]. Ablation studies show that both -High and -Low variants of LightRAG, which remove one level of retrieval, perform worse than the full version, confirming the importance of the dual-level retrieval mechanism [6].

LightRAG is more efficient than GraphRAG, using fewer than 100 tokens and a single API call during retrieval, compared to GraphRAG’s 610,000 tokens and hundreds of API calls [6]. It also integrates new data seamlessly during incremental updates, whereas GraphRAG must reconstruct its entire structure, incurring a token cost of around 13,990,000 for 1,399 communities [6]. The document concludes that LightRAG excels in both efficiency and effectiveness, significantly improving the speed and quality of information retrieval and generation while reducing costs for LLM inference [8].

Numbers that could not be checked against the cited pages of the original text: 13,990,000.

Figures whose labels differ from the source table: 54.4% (answer: Comprehensiveness, Agriculture, GraphRAG; source: Comprehensiveness, Agriculture, LightRAG, vs GraphRAG).
```

## A-Q1-2

- 問題：`summary this document.`；模式 `roles`；17.7 秒；1 次呼叫；tokens 4763
- 來源：[1] p1 summary, [2] p1 summary, [3] p1 summary, [4] p2 summary, [5] p3 summary, [6] p5 summary, [7] p10 summary, [8] p10 summary, [9] p13 summary
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 1；找不到的數字 []

```text
Navigator: The sections "INTRODUCTION" (pages 1-2), "THE LIGHT RAG ARCHITECTURE" (pages 3-5), and "EVALUATION" (pages 5-10) provide the necessary information for a summary of the document. The "CONCLUSION" (page 10) also offers a concise overview of the work and its contributions.

Analyst: The document introduces LightRAG, a novel Retrieval-Augmented Generation (RAG) system designed to improve the accuracy and efficiency of large language models (LLMs) by using graph-based indexing [3]. Current RAG systems are limited by flat data representations and a lack of contextual awareness, leading to fragmented responses [2]. LightRAG addresses these limitations by integrating graph structures into text indexing and retrieval, enabling a dual-level retrieval mechanism to capture both specific and abstract information [5]. The system segments documents into chunks, uses an LLM to extract entities and relationships, and builds a knowledge graph to enhance keyword matching and contextual relevance [1]. 

The evaluation section compares LightRAG with existing RAG methods, including NaiveRAG, RQ-RAG, HyDE, and GraphRAG, across four datasets—Agriculture, CS, Legal, and Mix—and four evaluation dimensions: Comprehensiveness, Diversity, Empowerment, and Overall [6]. LightRAG consistently outperforms these baselines, with, for example, an 83.6% win rate in Comprehensiveness for the Legal dataset compared to NaiveRAG’s 16.4% [6]. Ablation studies confirm the importance of the dual-level retrieval mechanism, as variants that remove either level perform worse than the full version [6]. LightRAG is also more efficient in terms of token usage and API calls during retrieval and incremental updates compared to GraphRAG [1]. The conclusion summarizes LightRAG’s contributions, emphasizing its efficiency, effectiveness, and ability to adapt to new information [8].
```

## A-Q1-3

- 問題：`summary this document.`；模式 `roles`；18.9 秒；1 次呼叫；tokens 4792
- 來源：[1] p1 summary, [2] p1 summary, [3] p1 summary, [4] p2 summary, [5] p3 summary, [6] p5 summary, [7] p10 summary, [8] p10 summary, [9] p13 summary
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 1；找不到的數字 []

```text
Navigator: The sections bearing on the question are: INTRODUCTION (pages 1-2), RETRIEVAL-AUGMENTED GENERATION (pages 2-3), THE LIGHT RAG ARCHITECTURE (pages 3-5), EVALUATION (pages 5-10), CONCLUSION (page 10), and the summary in the Front matter (page 1).

Analyst: The document introduces LightRAG, a novel Retrieval-Augmented Generation (RAG) system designed to enhance the accuracy and efficiency of large language models by using graph-based indexing to better represent relationships among entities [1]. Current RAG systems are limited by flat data representations and a lack of contextual awareness, which leads to fragmented and incomplete responses [1]. LightRAG addresses these limitations through a dual-level retrieval framework, enabling both low-level retrieval of specific entities and high-level retrieval of broader topics [2]. It uses an LLM to extract entities and relationships from document chunks, building a knowledge graph that enhances keyword matching and captures high-order relatedness [3].

The system is evaluated across four datasets—Agriculture, CS, Legal, and Mix—and outperforms existing RAG methods such as NaiveRAG, RQ-RAG, HyDE, and GraphRAG in four evaluation dimensions: Comprehensiveness, Diversity, Empowerment, and Overall [4]. For example, in the Legal dataset, LightRAG achieves an 83.6% win rate in Comprehensiveness, significantly higher than NaiveRAG’s 16.4% [6]. Ablation studies confirm the importance of the dual-level retrieval mechanism [6]. LightRAG is also more efficient in terms of cost and adaptability, using fewer than 100 tokens and a single API call during retrieval, compared to GraphRAG’s 610,000 tokens and hundreds of API calls [6]. An incremental update algorithm ensures seamless integration of new data [1].

Overall, LightRAG improves both the efficiency and effectiveness of RAG systems, offering a more comprehensive and context-aware approach to information retrieval and generation [8].
```

## B-Q1-1

- 問題：`summary this document.`；模式 `navigate`；32.8 秒；2 次呼叫；tokens 6669
- 來源：[1] p1 summary, [2] p1 summary, [3] p1 summary, [4] p2 summary, [5] p3 summary, [6] p5 summary, [7] p10 summary, [8] p10 summary, [9] p13 summary, [10] p1 navigation, [11] p1 navigation, [12] p1 navigation, [13] p2 navigation
- 閱讀計畫（定位 6/6，保留 4，超預算 20）：
  - ✓ Section: INTRODUCTION (pages 1-2): Provides the background and objectives of the study.
  - ✓ Section: RETRIEVAL-AUGMENTED GENERATION (pages 2-3): Describes the general concept and methodology.
  - ✓ Section: THE LIGHT RAG ARCHITECTURE (pages 3-5): Explains the specific framework proposed in the document.
  - ✓ Figure 1 (page 3): Visualizes the LightRAG framework.
  - ✓ Section: EVALUATION (pages 5-10): Details how the framework was tested and compared.
  - ✓ Section: CONCLUSION (page 10): Summarizes the findings and implications.
- 檢查：標籤不符 ['54.4%']；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 ['13,990,000']

```text
The document introduces LightRAG, a novel Retrieval-Augmented Generation (RAG) system designed to enhance the accuracy and efficiency of large language models (LLMs) by integrating graph-based indexing [1]. Current RAG systems are limited by flat data representations and a lack of contextual awareness, leading to fragmented and incomplete responses [3]. LightRAG addresses these issues by using graph structures to represent interdependencies among entities, enabling more nuanced and contextually rich responses [3]. The system employs a dual-level retrieval framework, combining low-level retrieval of specific entities with high-level retrieval of broader topics [5]. This approach allows for efficient and comprehensive information retrieval, significantly improving response times and maintaining contextual relevance [5]. 

Experiments across four datasets—Agriculture, CS, Legal, and Mix—demonstrate that LightRAG outperforms existing RAG methods such as NaiveRAG, RQ-RAG, HyDE, and GraphRAG in four evaluation dimensions: Comprehensiveness, Diversity, Empowerment, and Overall [6]. For instance, in the Legal dataset, LightRAG achieves an 83.6% win rate in Comprehensiveness, significantly higher than NaiveRAG’s 16.4% [6]. In the Agriculture dataset, LightRAG achieves 67.6% in Comprehensiveness compared to GraphRAG’s 54.4% [6]. Ablation studies confirm the importance of the dual-level retrieval mechanism, as variants that remove one level of retrieval perform worse than the full version [6].

LightRAG is more efficient than GraphRAG, using fewer than 100 tokens and a single API call during retrieval, compared to GraphRAG’s 610,000 tokens and hundreds of API calls [6]. Additionally, LightRAG supports fast adaptation to new data through an incremental update algorithm, whereas GraphRAG must reconstruct its entire structure, incurring a token cost of around 13,990,000 for 1,399 communities [6]. The document concludes by summarizing the key contributions of LightRAG, emphasizing its efficiency, effectiveness, and ability to maintain contextual relevance and adaptability [8]. The framework is open-source and available at https://github.com/HKUDS/LightRAG [1].

Numbers that could not be checked against the cited pages of the original text: 13,990,000.

Figures whose labels differ from the source table: 54.4% (answer: Comprehensiveness, Agriculture, GraphRAG; source: Comprehensiveness, Agriculture, LightRAG, vs GraphRAG).
```

## B-Q1-2

- 問題：`summary this document.`；模式 `navigate`；29.9 秒；2 次呼叫；tokens 6595
- 來源：[1] p1 summary, [2] p1 summary, [3] p1 summary, [4] p2 summary, [5] p3 summary, [6] p5 summary, [7] p10 summary, [8] p10 summary, [9] p13 summary, [10] p1 navigation, [11] p1 navigation, [12] p1 navigation, [13] p2 navigation
- 閱讀計畫（定位 6/6，保留 4，超預算 20）：
  - ✓ Section: INTRODUCTION (pages 1-2): Provides background and objectives of the document.
  - ✓ Section: RETRIEVAL-AUGMENTED GENERATION (pages 2-3): Explains the foundational concept of RAG.
  - ✓ Section: THE LIGHT RAG ARCHITECTURE (pages 3-5): Describes the proposed framework.
  - ✓ Figure 1 (page 3): Visualizes the LightRAG framework.
  - ✓ Section: EVALUATION (pages 5-10): Details how the framework was assessed.
  - ✓ Section: CONCLUSION (page 10): Summarizes findings and implications.
- 檢查：標籤不符 ['54.4%']；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
This document introduces LightRAG, a novel Retrieval-Augmented Generation (RAG) system designed to improve the accuracy and efficiency of large language models by integrating external knowledge sources through graph-based indexing [1]. Current RAG systems are limited by flat data representations and a lack of contextual awareness, leading to fragmented and incomplete responses [1]. LightRAG addresses these issues by using graph structures to represent interdependencies among entities, enabling a more nuanced understanding of relationships [1]. The system employs a dual-level retrieval framework, combining low-level retrieval for specific entities and high-level retrieval for broader topics [1]. This approach enhances the system's ability to provide contextually relevant and comprehensive responses [1]. 

Experiments across four datasets—Agriculture, CS, Legal, and Mix—show that LightRAG outperforms existing RAG methods like NaiveRAG, RQ-RAG, HyDE, and GraphRAG in terms of Comprehensiveness, Diversity, Empowerment, and Overall performance [1]. For example, in the Legal dataset, LightRAG achieves an 83.6% win rate in Comprehensiveness, significantly higher than NaiveRAG’s 16.4% [1]. In the Agriculture dataset, LightRAG achieves 67.6% in Comprehensiveness compared to GraphRAG’s 54.4% [1]. Ablation studies confirm the importance of the dual-level retrieval mechanism, showing that variants removing one level of retrieval perform worse [1]. 

LightRAG is also more efficient than GraphRAG, using fewer than 100 tokens and a single API call during retrieval, compared to GraphRAG’s 610,000 tokens and hundreds of API calls [1]. It supports fast adaptation to new data through an incremental update algorithm, allowing seamless integration of new information without reconstructing the entire graph structure [1]. The document concludes by summarizing the key contributions of LightRAG, including its enhanced efficiency, comprehensive information retrieval, and rapid adaptation to new data [1].

Figures whose labels differ from the source table: 54.4% (answer: Comprehensiveness, Agriculture, GraphRAG; source: Comprehensiveness, Agriculture, LightRAG, vs GraphRAG).
```

## B-Q1-3

- 問題：`summary this document.`；模式 `navigate`；30.4 秒；2 次呼叫；tokens 6611
- 來源：[1] p1 summary, [2] p1 summary, [3] p1 summary, [4] p2 summary, [5] p3 summary, [6] p5 summary, [7] p10 summary, [8] p10 summary, [9] p13 summary, [10] p1 navigation, [11] p1 navigation, [12] p1 navigation, [13] p2 navigation
- 閱讀計畫（定位 6/6，保留 4，超預算 20）：
  - ✓ Section: INTRODUCTION (pages 1-2): Provides the background and objectives of the document.
  - ✓ Section: RETRIEVAL-AUGMENTED GENERATION (pages 2-3): Describes the foundational concepts of RAG.
  - ✓ Section: THE LIGHT RAG ARCHITECTURE (pages 3-5): Explains the proposed architecture in detail.
  - ✓ Figure 1 (page 3): Visualizes the LightRAG framework.
  - ✓ Section: EVALUATION (pages 5-10): Outlines how the framework was evaluated.
  - ✓ Section: CONCLUSION (page 10): Summarizes the findings and implications.
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 ['13,990,000']

```text
This document introduces LightRAG, a novel Retrieval-Augmented Generation (RAG) system designed to improve the accuracy and efficiency of large language models (LLMs) by incorporating external knowledge sources through graph-based indexing [1]. Current RAG systems are limited by flat data representations and a lack of contextual awareness, leading to fragmented and incomplete responses [1]. LightRAG addresses these issues by using a dual-level retrieval framework that captures both specific and abstract information, and by integrating graph structures into text indexing and retrieval [1]. The system uses an LLM to extract entities and relationships, building a knowledge graph that enhances keyword matching and captures high-order relatedness from neighboring nodes [5]. 

LightRAG was evaluated across four datasets—Agriculture, CS, Legal, and Mix—and it outperformed existing RAG methods such as NaiveRAG, RQ-RAG, HyDE, and GraphRAG in four evaluation dimensions: Comprehensiveness, Diversity, Empowerment, and Overall [6]. For example, in the Legal dataset, LightRAG achieved an 83.6% win rate in Comprehensiveness, significantly higher than NaiveRAG’s 16.4% [6]. Ablation studies confirmed the importance of the dual-level retrieval mechanism, as variants that removed one level of retrieval performed worse than the full version [6]. 

In terms of efficiency, LightRAG is more cost-effective than GraphRAG, using fewer than 100 tokens and a single API call during retrieval, compared to GraphRAG’s 610,000 tokens and hundreds of API calls [6]. LightRAG also supports fast adaptation to new data through an incremental update algorithm, whereas GraphRAG must reconstruct its entire structure, incurring a token cost of around 13,990,000 for 1,399 communities [6]. 

The document concludes by summarizing the key contributions of LightRAG, including its ability to enhance both efficiency and effectiveness in information retrieval and generation, and its open-source availability [8].

Numbers that could not be checked against the cited pages of the original text: 13,990,000.
```

## B2-Q1-1

- 問題：`summary this document.`；模式 `navigate`；33.1 秒；2 次呼叫；tokens 7301
- 來源：[1] p1 summary, [2] p1 summary, [3] p1 summary, [4] p2 summary, [5] p3 summary, [6] p5 summary, [7] p10 summary, [8] p10 summary, [9] p13 summary, [10] p6 navigation, [11] p5 navigation, [12] p11 navigation, [13] p2 navigation, [14] p2 navigation
- 閱讀計畫（定位 6/6，保留 5，超預算 22）：
  - ✓ Section 1 INTRODUCTION | need: overview of the document | priority: required | status: missing → 候選 5，納入 [4]，排除 [(1, 'low relevance'), (2, 'low relevance'), (0, 'over the evidence budget'), (3, 'over the evidence budget')]
  - ✓ Section 2 RETRIEVAL-AUGMENTED GENERATION | need: background on RAG | priority: required | status: missing → 候選 4，納入 [5]，排除 [(6, 'low relevance'), (4, 'already selected for another target'), (7, 'over the evidence budget')]
  - ✓ Section 3 THE LIGHT RAG ARCHITECTURE | need: description of the framework | priority: required | status: missing → 候選 8，納入 [14]，排除 [(11, 'low relevance'), (10, 'low relevance'), (12, 'low relevance'), (9, 'low relevance'), (13, 'over the evidence budget'), (7, 'over the evidence budget'), (8, 'over the evidence budget')]
  - ✓ Section 4 EVALUATION | need: evaluation methodology and results | priority: required | status: missing → 候選 9，納入 [18]，排除 [(26, 'over the evidence budget'), (27, 'over the evidence budget'), (25, 'over the evidence budget'), (24, 'over the evidence budget'), (17, 'over the evidence budget'), (23, 'over the evidence budget'), (14, 'already selected for another target'), (16, 'over the evidence budget')]
  - ✓ Section 5 RELATED WORK | need: related research context | priority: supplementary | status: missing → 候選 3，納入 [30]，排除 [(29, 'over the evidence budget'), (31, 'over the evidence budget')]
  - ✓ Section 6 CONCLUSION | need: summary of findings and future work | priority: required | status: missing → 候選 7，納入 [34, 37]，排除 [(32, 'over the evidence budget'), (33, 'over the evidence budget'), (35, 'over the evidence budget'), (36, 'over the evidence budget'), (31, 'over the evidence budget')]
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 1；找不到的數字 []

```text
The document addresses the limitations of existing Retrieval-Augmented Generation (RAG) systems, which often rely on flat data representations and lack contextual awareness, leading to fragmented responses for complex queries. It introduces LightRAG, a RAG system that incorporates graph structures into text indexing and retrieval, enabling more comprehensive and contextually rich responses. LightRAG features a dual-level retrieval system that supports both low-level retrieval of specific entities and high-level retrieval of broader topics, enhancing the system's ability to capture complex dependencies [1].

LightRAG enhances retrieval by segmenting documents into smaller chunks, extracting entities and relationships to build a knowledge graph, and using a deduplication process to improve efficiency. The system also supports fast adaptation to new data through an incremental update algorithm. Evaluations on the UltraDomain benchmark across four domains show that LightRAG outperforms existing approaches. For example, in the Agriculture dataset, LightRAG achieved a 67.6% win rate in Comprehensiveness against Naive RAG's 32.4% (p. 7), and in the Legal dataset, it achieved 83.6% in Comprehensiveness against Naive RAG's 16.4% (p. 7). Compared to GraphRAG, LightRAG showed a 54.4% win rate in Comprehensiveness (p. 7). Ablation studies confirm the importance of the dual-level retrieval paradigm, with performance declining when either level is removed (p. 8) [1].

The document also highlights the importance of integrating graph structures with vector representations to facilitate efficient retrieval and enhance result comprehensiveness through structural information from the knowledge graph. The experimental findings demonstrate significant improvements over baseline methods in retrieval accuracy, model ablation, response efficiency, and adaptability to new information [1].

In conclusion, LightRAG is a highly effective RAG system that improves both the efficiency and effectiveness of information retrieval and generation. Its dual-level retrieval paradigm allows for the extraction of both specific and abstract information, catering to diverse user needs. Additionally, LightRAG’s incremental update capability ensures that the system remains current and responsive to new information, maintaining its effectiveness over time [8].
```

## B2-Q1-2

- 問題：`summary this document.`；模式 `navigate`；32.4 秒；2 次呼叫；tokens 7428
- 來源：[1] p1 summary, [2] p1 summary, [3] p1 summary, [4] p2 summary, [5] p3 summary, [6] p5 summary, [7] p10 summary, [8] p10 summary, [9] p13 summary, [10] p8 navigation, [11] p12 navigation, [12] p4 navigation
- 閱讀計畫（定位 6/6，保留 3，超預算 18）：
  - ✓ Section 1 INTRODUCTION | need: overview and purpose | priority: required | status: missing → 候選 5，納入 []，排除 [(4, 'low relevance'), (2, 'low relevance'), (1, 'low relevance'), (3, 'low relevance'), (0, 'low relevance')]
  - ✓ Section 2 RETRIEVAL-AUGMENTED GENERATION | need: concept explanation | priority: required | status: missing → 候選 4，納入 [4]，排除 [(5, 'low relevance'), (7, 'low relevance'), (6, 'over the evidence budget')]
  - ✓ Section 3 THE LIGHT RAG ARCHITECTURE | need: architecture summary | priority: required | status: missing → 候選 8，納入 [10]，排除 [(7, 'low relevance'), (13, 'low relevance'), (14, 'low relevance'), (8, 'low relevance'), (12, 'low relevance'), (9, 'low relevance'), (11, 'over the evidence budget')]
  - ✓ Section 4 EVALUATION | need: experimental results | priority: required | status: missing → 候選 9，納入 [22]，排除 [(14, 'low relevance'), (19, 'over the evidence budget'), (18, 'over the evidence budget'), (27, 'over the evidence budget'), (28, 'over the evidence budget'), (24, 'over the evidence budget'), (21, 'over the evidence budget'), (26, 'over the evidence budget')]
  - ✓ Section 5 RELATED WORK | need: related research | priority: supplementary | status: missing → 候選 3，納入 []，排除 [(30, 'over the evidence budget'), (29, 'over the evidence budget'), (31, 'over the evidence budget')]
  - ✓ Section 6 CONCLUSION | need: main findings and future work | priority: required | status: missing → 候選 7，納入 [37]，排除 [(31, 'low relevance'), (34, 'over the evidence budget'), (32, 'over the evidence budget'), (33, 'over the evidence budget'), (35, 'over the evidence budget'), (36, 'over the evidence budget')]
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 2；找不到的數字 []

```text
The document addresses the limitations of existing Retrieval-Augmented Generation (RAG) systems, which often rely on flat data representations and lack contextual awareness, leading to fragmented responses for complex queries [1]. It introduces LightRAG, a novel RAG system that integrates graph structures into text indexing and retrieval, enabling more comprehensive and contextually rich responses [1]. LightRAG features a dual-level retrieval system that supports both low-level retrieval of specific entities and high-level retrieval of broader topics, improving the system's ability to capture complex dependencies and provide coherent answers [1].

The system enhances retrieval by segmenting documents into smaller chunks, extracting entities and relationships to build a knowledge graph, and using a deduplication process to improve efficiency [1]. It also supports fast adaptation to new data through an incremental update algorithm [1]. Experimental evaluations on the UltraDomain benchmark across four domains—Agriculture, CS, Legal, and Mix—show that LightRAG outperforms existing approaches. For example, in the Agriculture dataset, LightRAG achieved a 67.6% win rate in Comprehensiveness against Naive RAG's 32.4% [1]. In the Legal dataset, it achieved 83.6% in Comprehensiveness against Naive RAG's 16.4% [1]. Compared to GraphRAG, LightRAG showed a 54.4% win rate in Comprehensiveness [1]. Ablation studies confirm the importance of the dual-level retrieval paradigm, with performance declining when either level is removed [1]. In terms of efficiency, LightRAG used fewer than 100 tokens and a single API call for retrieval in the Legal dataset, compared to GraphRAG's 610,000 tokens and hundreds of API calls [1].

LightRAG is open-source and available at https://github.com/HKUDS/LightRAG [2]. The document also discusses related work, highlighting the limitations of current RAG methods and the benefits of integrating graph structures for dynamic updates and efficient search [7]. It concludes by emphasizing LightRAG's contributions to enhancing both efficiency and effectiveness in information retrieval and generation [8].
```

## B2-Q1-3

- 問題：`summary this document.`；模式 `navigate`；34.7 秒；2 次呼叫；tokens 7391
- 來源：[1] p1 summary, [2] p1 summary, [3] p1 summary, [4] p2 summary, [5] p3 summary, [6] p5 summary, [7] p10 summary, [8] p10 summary, [9] p13 summary, [10] p5 navigation, [11] p9 navigation, [12] p2 navigation, [13] p10 navigation, [14] p2 navigation
- 閱讀計畫（定位 6/6，保留 5，超預算 12）：
  - ✓ Section 1 INTRODUCTION | need: overview and purpose | priority: required | status: missing → 候選 5，納入 []，排除 [(4, 'low relevance'), (2, 'low relevance'), (1, 'low relevance'), (3, 'low relevance'), (0, 'low relevance')]
  - ✓ Section 2 RETRIEVAL-AUGMENTED GENERATION | need: background on RAG | priority: required | status: missing → 候選 4，納入 [5, 4]，排除 [(6, 'low relevance'), (7, 'over the evidence budget')]
  - ✓ Section 3 THE LIGHT RAG ARCHITECTURE | need: framework description | priority: required | status: missing → 候選 8，納入 [14, 13]，排除 [(11, 'low relevance'), (10, 'low relevance'), (12, 'low relevance'), (9, 'low relevance'), (7, 'over the evidence budget'), (8, 'over the evidence budget')]
  - ✓ Section 4 EVALUATION | need: results and analysis | priority: required | status: missing → 候選 9，納入 [27]，排除 [(19, 'over the evidence budget'), (22, 'over the evidence budget'), (18, 'over the evidence budget'), (24, 'over the evidence budget'), (26, 'over the evidence budget'), (17, 'over the evidence budget'), (23, 'over the evidence budget'), (21, 'over the evidence budget')]
  - ✓ Section 5 RELATED WORK | need: context in literature | priority: supplementary | status: missing → 候選 3，納入 [30]，排除 [(29, 'low relevance'), (31, 'low relevance')]
  - ✓ Section 6 CONCLUSION | need: summary and implications | priority: required | status: missing → 候選 7，納入 []，排除 [(32, 'low relevance'), (34, 'low relevance'), (33, 'low relevance'), (31, 'low relevance'), (37, 'low relevance'), (35, 'low relevance'), (36, 'low relevance')]
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 1；找不到的數字 []

```text
The document addresses the limitations of existing Retrieval-Augmented Generation (RAG) systems, which often rely on flat data representations and lack contextual awareness, leading to fragmented responses for complex queries [1]. To overcome these issues, the authors propose LightRAG, a RAG system that integrates graph structures into text indexing and retrieval, enabling more comprehensive and contextually rich responses [1]. LightRAG introduces a dual-level retrieval system that supports both low-level retrieval of specific entities and high-level retrieval of broader topics, improving the system's ability to capture complex dependencies and provide coherent answers [1]. The system enhances retrieval by segmenting documents into smaller chunks, extracting entities and relationships to build a knowledge graph, and using a deduplication process to improve efficiency [1]. It also supports fast adaptation to new data through an incremental update algorithm [1]. Experimental evaluations on the UltraDomain benchmark across four domains show that LightRAG outperforms existing approaches in terms of comprehensiveness, diversity, empowerment, and overall performance [1]. For example, in the Agriculture dataset, LightRAG achieved a 67.6% win rate in Comprehensiveness against Naive RAG's 32.4% [1], and in the Legal dataset, it achieved 83.6% in Comprehensiveness against Naive RAG's 16.4% [1]. Compared to GraphRAG, LightRAG showed a 54.4% win rate in Comprehensiveness [1]. Ablation studies confirm the importance of the dual-level retrieval paradigm, with performance declining when either level is removed [1]. In terms of efficiency, LightRAG used fewer than 100 tokens and a single API call for retrieval in the Legal dataset, compared to GraphRAG's 610,000 tokens and hundreds of API calls [1]. The document also discusses the integration of graph structures with vector representations to enhance retrieval and the system's ability to adapt to new data [1]. The key contributions of this work include emphasizing the importance of graph-empowered RAG systems, proposing LightRAG with a dual-level retrieval paradigm, and demonstrating experimental improvements over baseline methods in retrieval accuracy, model ablation, response efficiency, and adaptability [1]. The document concludes by summarizing the implications of the work and highlighting the effectiveness of LightRAG in improving the speed and quality of information retrieval and generation while reducing costs for LLM inference [8].
```

## B3-Q1-1

- 問題：`summary this document.`；模式 `navigate`；30.6 秒；2 次呼叫；tokens 7384
- 來源：[1] p1 summary, [2] p1 summary, [3] p1 summary, [4] p2 summary, [5] p3 summary, [6] p5 summary, [7] p10 summary, [8] p10 summary, [9] p13 summary, [10] p11 navigation, [11] p8 navigation
- 閱讀計畫（定位 6/6，保留 2，超預算 16）：
  - ✓ Section 1 INTRODUCTION | need: overview and purpose | priority: required | status: missing → 候選 5，納入 []，排除 [(4, 'low relevance'), (2, 'low relevance'), (1, 'low relevance'), (3, 'low relevance'), (0, 'low relevance')]
  - ✓ Section 2 RETRIEVAL-AUGMENTED GENERATION | need: background context | priority: required | status: missing → 候選 4，納入 []，排除 [(4, 'low relevance'), (7, 'low relevance'), (6, 'low relevance'), (5, 'low relevance')]
  - ✓ Section 3 THE LIGHT RAG ARCHITECTURE | need: framework structure | priority: required | status: missing → 候選 8，納入 [14]，排除 [(8, 'low relevance'), (13, 'low relevance'), (10, 'low relevance'), (11, 'low relevance'), (12, 'low relevance'), (9, 'low relevance'), (7, 'over the evidence budget')]
  - ✓ Section 4 EVALUATION | need: experimental results | priority: required | status: missing → 候選 9，納入 [22]，排除 [(14, 'low relevance'), (19, 'over the evidence budget'), (18, 'over the evidence budget'), (27, 'over the evidence budget'), (28, 'over the evidence budget'), (24, 'over the evidence budget'), (21, 'over the evidence budget'), (26, 'over the evidence budget')]
  - ✓ Section 5 RELATED WORK | need: prior research context | priority: supplementary | status: missing → 候選 3，納入 []，排除 [(29, 'low relevance'), (30, 'over the evidence budget'), (31, 'over the evidence budget')]
  - ✓ Section 6 CONCLUSION | need: summary of findings | priority: required | status: missing → 候選 7，納入 [32]，排除 [(31, 'low relevance'), (33, 'over the evidence budget'), (34, 'over the evidence budget'), (37, 'over the evidence budget'), (36, 'over the evidence budget'), (35, 'over the evidence budget')]
- 分析狀態：UNCERTAIN；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 涵蓋判定：Section 1 INTRODUCTION→missing；Section 2 RETRIEVAL-AUGMENTED GENERATION→missing；Section 3 THE LIGHT RAG ARCHITECTURE→missing；Section 4 EVALUATION→missing；Section 5 RELATED WORK→missing；Section 6 CONCLUSION→missing；required 未納入 ['Section 1 INTRODUCTION', 'Section 2 RETRIEVAL-AUGMENTED GENERATION']；supplementary 用 0；Matrix None
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 2；找不到的數字 []

```text
The document "LightRAG: Simple and Fast Retrieval-Augmented Generation" addresses limitations in existing Retrieval-Augmented Generation (RAG) systems, which often rely on flat data representations and lack sufficient contextual awareness, leading to fragmented answers [1]. The authors propose LightRAG, a framework that integrates graph structures into text indexing and retrieval processes, enabling dual-level retrieval for both low-level and high-level knowledge discovery [2]. LightRAG combines graph structures with vector representations to efficiently retrieve related entities and their relationships, improving response times and maintaining contextual relevance [1]. An incremental update algorithm ensures timely integration of new data, making the system effective in rapidly changing environments [1].

Extensive experiments on four datasets—Agriculture, CS, Legal, and Mix—show that LightRAG outperforms state-of-the-art methods such as Naive RAG, RQ-RAG, HyDE, and GraphRAG [1]. On the Legal dataset, LightRAG achieves 83.6% comprehensiveness, 86.4% diversity, and 83.6% empowerment compared to Naive RAG [6]. Ablation studies confirm the importance of the dual-level retrieval paradigm, with a variant removing high-order retrieval showing a significant drop in comprehensiveness (23.6% vs. 83.6%) in the Legal dataset [6]. LightRAG also demonstrates cost efficiency, using fewer than 100 tokens and a single API call for retrieval in the Legal dataset, compared to 610,000 tokens and hundreds of API calls for GraphRAG [6].

The document concludes that LightRAG excels in both efficiency and effectiveness, significantly improving the speed and quality of information retrieval and generation while reducing costs for LLM inference [8]. The LightRAG code is open-sourced and available at https://github.com/HKUDS/LightRAG [1].
```

## B3-Q1-2

- 問題：`summary this document.`；模式 `navigate`；28.7 秒；2 次呼叫；tokens 6026
- 來源：[1] p1 summary, [2] p1 summary, [3] p1 summary, [4] p2 summary, [5] p3 summary, [6] p5 summary, [7] p10 summary, [8] p10 summary, [9] p13 summary, [10] p5 navigation, [11] p12 navigation
- 閱讀計畫（定位 6/6，保留 2，超預算 21）：
  - ✓ Section 1 INTRODUCTION | need: overview of the document | priority: required | status: missing → 候選 5，納入 []，排除 [(1, 'low relevance'), (2, 'low relevance'), (4, 'over the evidence budget'), (0, 'over the evidence budget'), (3, 'over the evidence budget')]
  - ✓ Section 2 RETRIEVAL-AUGMENTED GENERATION | need: definition and context | priority: required | status: missing → 候選 4，納入 []，排除 [(6, 'low relevance'), (5, 'low relevance'), (4, 'low relevance'), (7, 'low relevance')]
  - ✓ Section 3 THE LIGHT RAG ARCHITECTURE | need: framework description | priority: required | status: missing → 候選 8，納入 [14]，排除 [(11, 'low relevance'), (10, 'low relevance'), (12, 'low relevance'), (9, 'low relevance'), (13, 'over the evidence budget'), (7, 'over the evidence budget'), (8, 'over the evidence budget')]
  - ✓ Section 4 EVALUATION | need: experimental results summary | priority: required | status: missing → 候選 9，納入 [22, 24]，排除 [(19, 'over the evidence budget'), (18, 'over the evidence budget'), (14, 'already selected for another target'), (27, 'over the evidence budget'), (23, 'over the evidence budget'), (26, 'over the evidence budget'), (21, 'over the evidence budget')]
  - ✓ Section 5 RELATED WORK | need: background and prior research | priority: supplementary | status: missing → 候選 3，納入 []，排除 [(29, 'low relevance'), (31, 'over the evidence budget'), (30, 'over the evidence budget')]
  - ✓ Section 6 CONCLUSION | need: summary of contributions and findings | priority: required | status: missing → 候選 7，納入 [37]，排除 [(31, 'low relevance'), (32, 'over the evidence budget'), (36, 'over the evidence budget'), (34, 'over the evidence budget'), (33, 'over the evidence budget'), (35, 'over the evidence budget')]
- 分析狀態：UNCERTAIN；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 涵蓋判定：Section 1 INTRODUCTION→missing；Section 2 RETRIEVAL-AUGMENTED GENERATION→missing；Section 3 THE LIGHT RAG ARCHITECTURE→missing；Section 4 EVALUATION→missing；Section 5 RELATED WORK→missing；Section 6 CONCLUSION→missing；required 未納入 ['Section 1 INTRODUCTION', 'Section 2 RETRIEVAL-AUGMENTED GENERATION']；supplementary 用 0；Matrix None
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 2；找不到的數字 []

```text
The document "LightRAG: Simple and Fast Retrieval-Augmented Generation" addresses the limitations of existing Retrieval-Augmented Generation (RAG) systems, which often rely on flat data representations and lack sufficient contextual awareness, leading to fragmented answers [3]. To overcome these issues, the authors propose LightRAG, a framework that integrates graph structures into text indexing and retrieval, enabling dual-level retrieval for both low-level and high-level knowledge discovery [1]. LightRAG combines graph structures with vector representations to efficiently retrieve related entities and their relationships, improving response times and maintaining contextual relevance. An incremental update algorithm ensures timely integration of new data, making the system effective in rapidly changing environments [1].

The framework is evaluated across four datasets—Agriculture, CS, Legal, and Mix—showing significant improvements in retrieval accuracy and efficiency compared to existing approaches such as Naive RAG, RQ-RAG, HyDE, and GraphRAG. On the Legal dataset, LightRAG achieves 83.6% comprehensiveness, 86.4% diversity, and 83.6% empowerment against Naive RAG [6]. Ablation studies confirm the importance of the dual-level retrieval paradigm, with a variant removing high-order retrieval showing a significant drop in comprehensiveness (23.6% vs. 83.6%) in the Legal dataset [6]. 

Additionally, LightRAG demonstrates cost efficiency. In the Legal dataset, it uses fewer than 100 tokens and a single API call for retrieval, compared to 610,000 tokens and hundreds of API calls for GraphRAG [6]. The system is open-sourced at https://github.com/HKUDS/LightRAG [1]. The document concludes that LightRAG excels in both efficiency and effectiveness, significantly improving the speed and quality of information retrieval and generation while reducing costs for LLM inference [8].
```

## B3-Q1-3

- 問題：`summary this document.`；模式 `navigate`；27.9 秒；2 次呼叫；tokens 7192
- 來源：[1] p1 summary, [2] p1 summary, [3] p1 summary, [4] p2 summary, [5] p3 summary, [6] p5 summary, [7] p10 summary, [8] p10 summary, [9] p13 summary, [10] p6 navigation, [11] p11 navigation, [12] p2 navigation, [13] p9 navigation, [14] p12 navigation
- 閱讀計畫（定位 6/6，保留 5，超預算 18）：
  - ✓ Section 1 INTRODUCTION | need: overview of the document | priority: required | status: missing → 候選 5，納入 [4, 0]，排除 [(1, 'low relevance'), (2, 'low relevance'), (3, 'over the evidence budget')]
  - ✓ Section 3 THE LIGHT RAG ARCHITECTURE | need: description of the architecture | priority: required | status: missing → 候選 8，納入 []，排除 [(7, 'low relevance'), (11, 'low relevance'), (10, 'low relevance'), (8, 'low relevance'), (13, 'low relevance'), (14, 'low relevance'), (12, 'low relevance'), (9, 'low relevance')]
  - ✓ Section 4 EVALUATION | need: evaluation methodology and results | priority: required | status: missing → 候選 9，納入 [18, 26]，排除 [(27, 'over the evidence budget'), (25, 'over the evidence budget'), (24, 'over the evidence budget'), (17, 'over the evidence budget'), (23, 'over the evidence budget'), (14, 'over the evidence budget'), (16, 'over the evidence budget')]
  - ✓ Section 5 RELATED WORK | need: context and prior work | priority: supplementary | status: missing → 候選 3，納入 []，排除 [(31, 'low relevance'), (29, 'low relevance'), (30, 'over the evidence budget')]
  - ✓ Section 6 CONCLUSION | need: summary of findings and future work | priority: required | status: missing → 候選 7，納入 [34, 37, 35]，排除 [(32, 'over the evidence budget'), (33, 'over the evidence budget'), (36, 'target quota reached'), (31, 'target quota reached')]
  - ✓ Section 7 APPENDIX | need: additional details and examples | priority: supplementary | status: missing → 候選 8，納入 []，排除 [(39, 'low relevance'), (41, 'low relevance'), (43, 'low relevance'), (38, 'over the evidence budget'), (40, 'over the evidence budget'), (44, 'over the evidence budget'), (45, 'over the evidence budget'), (42, 'over the evidence budget')]
- 分析狀態：UNCERTAIN；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 涵蓋判定：Section 1 INTRODUCTION→missing；Section 3 THE LIGHT RAG ARCHITECTURE→missing；Section 4 EVALUATION→missing；Section 5 RELATED WORK→missing；Section 6 CONCLUSION→missing；Section 7 APPENDIX→missing；required 未納入 ['Section 3 THE LIGHT RAG ARCHITECTURE']；supplementary 用 0；Matrix None
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
The document presents LightRAG, a novel Retrieval-Augmented Generation (RAG) framework that addresses limitations in existing RAG systems, such as the use of flat data representations and insufficient contextual awareness, which often lead to fragmented answers [1]. LightRAG integrates graph structures into text indexing and retrieval, enabling dual-level retrieval for both low-level and high-level knowledge discovery [3]. This integration of graph structures with vector representations allows for efficient retrieval of related entities and relationships, improving response times while maintaining contextual relevance [1]. The framework also includes an incremental update algorithm to efficiently integrate new data, making it suitable for dynamic environments [1].

LightRAG is evaluated on four datasets—Agriculture, CS, Legal, and Mix—demonstrating significant improvements in retrieval accuracy and efficiency compared to existing methods such as Naive RAG, RQ-RAG, HyDE, and GraphRAG [1]. For instance, in the Legal dataset, LightRAG achieves 83.6% comprehensiveness, 86.4% diversity, and 83.6% empowerment compared to Naive RAG [6]. The framework also shows cost efficiency, using fewer than 100 tokens and a single API call for retrieval, compared to hundreds of thousands of tokens and multiple API calls for GraphRAG [1]. 

The document concludes by highlighting LightRAG's contributions, including a general framework for graph-empowered RAG, the development of a dual-level retrieval paradigm, and experimental validation showing significant improvements in retrieval accuracy, response efficiency, and adaptability [8]. The system is open-sourced at https://github.com/HKUDS/LightRAG [1].
```

## B4-Q1-1

- 問題：`summary this document.`；模式 `navigate`；32.6 秒；2 次呼叫；tokens 7278
- 來源：[1] p1 summary, [2] p1 summary, [3] p1 summary, [4] p2 summary, [5] p3 summary, [6] p5 summary, [7] p10 summary, [8] p10 summary, [9] p13 summary, [10] p5 navigation, [11] p9 navigation, [12] p2 navigation, [13] p1 navigation
- 閱讀計畫（定位 6/6，保留 4，超預算 15）：
  - ✓ Section 1 INTRODUCTION | need: overview of the document | priority: required | status: missing → 候選 5，納入 [4, 0]，排除 [(1, 'low relevance'), (2, 'low relevance'), (3, 'over the evidence budget')]
  - ✓ Section 2 RETRIEVAL-AUGMENTED GENERATION | need: background context | priority: required | status: missing → 候選 4，納入 []，排除 [(4, 'low relevance'), (7, 'low relevance'), (6, 'low relevance'), (5, 'low relevance')]
  - ✓ Section 3 THE LIGHT RAG ARCHITECTURE | need: description of the framework | priority: required | status: missing → 候選 8，納入 [14, 13]，排除 [(11, 'low relevance'), (10, 'low relevance'), (12, 'low relevance'), (9, 'low relevance'), (7, 'over the evidence budget'), (8, 'over the evidence budget')]
  - ✓ Section 4 EVALUATION | need: results and analysis | priority: required | status: missing → 候選 9，納入 [27]，排除 [(19, 'over the evidence budget'), (22, 'over the evidence budget'), (18, 'over the evidence budget'), (24, 'over the evidence budget'), (26, 'over the evidence budget'), (17, 'over the evidence budget'), (23, 'over the evidence budget'), (21, 'over the evidence budget')]
  - ✓ Section 5 RELATED WORK | need: related research context | priority: supplementary | status: missing → 候選 3，納入 []，排除 [(30, 'over the evidence budget'), (29, 'over the evidence budget'), (31, 'over the evidence budget')]
  - ✓ Section 6 CONCLUSION | need: summary and implications | priority: required | status: missing → 候選 7，納入 []，排除 [(32, 'low relevance'), (34, 'low relevance'), (33, 'low relevance'), (31, 'low relevance'), (37, 'low relevance'), (35, 'low relevance'), (36, 'low relevance')]
- 分析狀態：UNCERTAIN；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 修正：[]；刪除 []；仍不符 []；方向待定 []
- 涵蓋判定：Section 1 INTRODUCTION→missing；Section 2 RETRIEVAL-AUGMENTED GENERATION→missing；Section 3 THE LIGHT RAG ARCHITECTURE→missing；Section 4 EVALUATION→missing；Section 5 RELATED WORK→missing；Section 6 CONCLUSION→missing；required 未納入 ['Section 2 RETRIEVAL-AUGMENTED GENERATION', 'Section 6 CONCLUSION']；supplementary 用 0；Matrix None
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 9；找不到的數字 []

```text
The document introduces LightRAG, a new Retrieval-Augmented Generation (RAG) framework designed to enhance large language models (LLMs) by integrating external knowledge sources to provide more accurate and contextually relevant responses [1]. Current RAG systems face limitations such as flat data representations and inadequate contextual awareness, leading to fragmented responses [1]. LightRAG addresses these issues by incorporating graph structures into text indexing and retrieval processes, enabling a more nuanced understanding of entity relationships [1]. The framework features a dual-level retrieval system for both low-level and high-level knowledge discovery, improving retrieval comprehensiveness and efficiency [1]. An incremental update algorithm ensures the system can adapt to new data efficiently [1].

LightRAG was evaluated across four datasets (Agriculture, CS, Legal, and Mix) from the UltraDomain benchmark, showing significant improvements over existing methods [1]. For example, in the Legal dataset, LightRAG achieved an 83.6% win rate in Comprehensiveness against Naive RAG (16.4%) and an 84.8% win rate in Overall against RQ-RAG (15.2%) [1]. In the Agriculture dataset, it achieved 67.6% win rates in Comprehensiveness, Diversity, and Empowerment against Naive RAG [1]. Ablation studies showed that removing high-level retrieval led to performance drops in Comprehensiveness (65.2% vs. 67.6%) and Diversity (72.8% vs. 76.4%), while removing low-level retrieval affected Comprehensiveness (64.0% vs. 67.6%) and Empowerment (65.2% vs. 67.6%) [1]. LightRAG is more efficient than GraphRAG in terms of token and API usage, using fewer than 100 tokens and one API call during retrieval, compared to GraphRAG's 610,000 tokens and hundreds of API calls [1]. The system is open-source and available at https://github.com/HKUDS/LightRAG [1].
```

## B4-Q1-2

- 問題：`summary this document.`；模式 `navigate`；31.4 秒；2 次呼叫；tokens 7260
- 來源：[1] p1 summary, [2] p1 summary, [3] p1 summary, [4] p2 summary, [5] p3 summary, [6] p5 summary, [7] p10 summary, [8] p10 summary, [9] p13 summary, [10] p5 navigation, [11] p11 navigation, [12] p2 navigation, [13] p11 navigation
- 閱讀計畫（定位 6/6，保留 4，超預算 16）：
  - ✓ Section 1 INTRODUCTION | need: overview of the document | priority: required | status: missing → 候選 5，納入 [4, 0]，排除 [(1, 'low relevance'), (2, 'low relevance'), (3, 'over the evidence budget')]
  - ✓ Section 2 RETRIEVAL-AUGMENTED GENERATION | need: background context | priority: required | status: missing → 候選 4，納入 []，排除 [(4, 'low relevance'), (7, 'low relevance'), (6, 'low relevance'), (5, 'low relevance')]
  - ✓ Section 3 THE LIGHT RAG ARCHITECTURE | need: framework description | priority: required | status: missing → 候選 8，納入 [14]，排除 [(11, 'low relevance'), (10, 'low relevance'), (12, 'low relevance'), (9, 'low relevance'), (13, 'over the evidence budget'), (7, 'over the evidence budget'), (8, 'over the evidence budget')]
  - ✓ Section 4 EVALUATION | need: experimental results summary | priority: required | status: missing → 候選 9，納入 []，排除 [(22, 'over the evidence budget'), (19, 'over the evidence budget'), (24, 'over the evidence budget'), (18, 'over the evidence budget'), (14, 'already selected for another target'), (27, 'over the evidence budget'), (23, 'over the evidence budget'), (26, 'over the evidence budget'), (21, 'over the evidence budget')]
  - ✓ Section 5 RELATED WORK | need: related research overview | priority: supplementary | status: missing → 候選 3，納入 []，排除 [(30, 'low relevance'), (31, 'low relevance'), (29, 'over the evidence budget')]
  - ✓ Section 6 CONCLUSION | need: summary of findings | priority: required | status: missing → 候選 7，納入 [32, 33, 37]，排除 [(31, 'low relevance'), (34, 'over the evidence budget'), (36, 'target quota reached'), (35, 'target quota reached')]
- 分析狀態：UNCERTAIN；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 修正：[]；刪除 []；仍不符 []；方向待定 []
- 涵蓋判定：Section 1 INTRODUCTION→missing；Section 2 RETRIEVAL-AUGMENTED GENERATION→missing；Section 3 THE LIGHT RAG ARCHITECTURE→missing；Section 4 EVALUATION→missing；Section 5 RELATED WORK→missing；Section 6 CONCLUSION→missing；required 未納入 ['Section 2 RETRIEVAL-AUGMENTED GENERATION', 'Section 4 EVALUATION']；supplementary 用 0；Matrix None
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
The document introduces LightRAG, a new Retrieval-Augmented Generation (RAG) framework designed to improve the performance of large language models (LLMs) by integrating external knowledge sources through a graph-based approach. Current RAG systems are limited by flat data representations and insufficient contextual awareness, leading to fragmented responses. LightRAG addresses these limitations by incorporating graph structures into text indexing and retrieval, enabling a more nuanced understanding of entity relationships [1].

The framework features a dual-level retrieval system, combining low-level retrieval (for precise entity relationships) and high-level retrieval (for broader topics), which enhances retrieval comprehensiveness and efficiency [3]. An incremental update algorithm allows LightRAG to adapt quickly to new data, making it effective in dynamic environments [1]. 

The evaluation of LightRAG across four datasets (Agriculture, CS, Legal, and Mix) from the UltraDomain benchmark shows significant improvements over existing methods like Naive RAG, RQ-RAG, and GraphRAG. For instance, in the Legal dataset, LightRAG achieves 83.6% win rate in Comprehensiveness against Naive RAG (16.4%) and 84.8% in Overall against RQ-RAG (15.2%). Ablation studies demonstrate the importance of both retrieval levels, with performance drops observed when either is removed [6].

LightRAG is also more efficient in terms of token and API usage compared to GraphRAG. During retrieval, LightRAG uses fewer than 100 tokens and one API call, while GraphRAG consumes 610,000 tokens and hundreds of API calls. Additionally, LightRAG integrates new data without full reconstruction, unlike GraphRAG, which requires rebuilding 1,399 communities [1]. 

The document concludes by summarizing the key contributions of LightRAG, including its graph-based indexing, dual-level retrieval paradigm, and efficient incremental update algorithm. These features enable LightRAG to provide more accurate, contextually rich, and cost-effective responses compared to existing RAG systems [8].
```

## B4-Q1-3

- 問題：`summary this document.`；模式 `navigate`；31.1 秒；2 次呼叫；tokens 7489
- 來源：[1] p1 summary, [2] p1 summary, [3] p1 summary, [4] p2 summary, [5] p3 summary, [6] p5 summary, [7] p10 summary, [8] p10 summary, [9] p13 summary, [10] p11 navigation, [11] p8 navigation
- 閱讀計畫（定位 6/6，保留 2，超預算 19）：
  - ✓ Section 1 INTRODUCTION | need: overview of the document | priority: required | status: missing → 候選 5，納入 []，排除 [(1, 'low relevance'), (2, 'low relevance'), (4, 'over the evidence budget'), (0, 'over the evidence budget'), (3, 'over the evidence budget')]
  - ✓ Section 2 RETRIEVAL-AUGMENTED GENERATION | need: definition and context | priority: required | status: missing → 候選 4，納入 []，排除 [(6, 'low relevance'), (5, 'low relevance'), (4, 'low relevance'), (7, 'low relevance')]
  - ✓ Section 3 THE LIGHT RAG ARCHITECTURE | need: framework structure | priority: required | status: missing → 候選 8，納入 []，排除 [(8, 'low relevance'), (13, 'low relevance'), (10, 'low relevance'), (11, 'low relevance'), (12, 'low relevance'), (9, 'low relevance'), (14, 'over the evidence budget'), (7, 'over the evidence budget')]
  - ✓ Section 4 EVALUATION | need: experimental results | priority: required | status: missing → 候選 9，納入 [22]，排除 [(14, 'low relevance'), (19, 'over the evidence budget'), (18, 'over the evidence budget'), (27, 'over the evidence budget'), (28, 'over the evidence budget'), (24, 'over the evidence budget'), (21, 'over the evidence budget'), (26, 'over the evidence budget')]
  - ✓ Section 5 RELATED WORK | need: related research context | priority: supplementary | status: missing → 候選 3，納入 []，排除 [(30, 'over the evidence budget'), (29, 'over the evidence budget'), (31, 'over the evidence budget')]
  - ✓ Section 6 CONCLUSION | need: summary of findings and future work | priority: required | status: missing → 候選 7，納入 [34, 37, 35]，排除 [(32, 'over the evidence budget'), (33, 'over the evidence budget'), (36, 'target quota reached'), (31, 'target quota reached')]
- 分析狀態：UNCERTAIN；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 修正：[]；刪除 []；仍不符 []；方向待定 []
- 涵蓋判定：Section 1 INTRODUCTION→missing；Section 2 RETRIEVAL-AUGMENTED GENERATION→missing；Section 3 THE LIGHT RAG ARCHITECTURE→missing；Section 4 EVALUATION→missing；Section 5 RELATED WORK→missing；Section 6 CONCLUSION→missing；required 未納入 ['Section 1 INTRODUCTION', 'Section 2 RETRIEVAL-AUGMENTED GENERATION', 'Section 3 THE LIGHT RAG ARCHITECTURE']；supplementary 用 0；Matrix None
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 4；找不到的數字 []

```text
This document introduces LightRAG, a novel Retrieval-Augmented Generation (RAG) framework designed to enhance the performance of large language models (LLMs) by integrating external knowledge sources using graph-based indexing and dual-level retrieval [1]. Traditional RAG systems suffer from limitations such as flat data representations and insufficient contextual awareness, leading to fragmented and incomplete responses [1]. LightRAG addresses these issues by incorporating graph structures into text indexing, allowing for more nuanced understanding of entity relationships and improving retrieval comprehensiveness and efficiency [1]. The framework features a dual-level retrieval system for low-level and high-level knowledge discovery, as well as an incremental update algorithm to adapt to new data efficiently [1].

LightRAG is evaluated across four datasets (Agriculture, CS, Legal, and Mix) from the UltraDomain benchmark, where it demonstrates significant improvements over existing methods such as Naive RAG, RQ-RAG, and GraphRAG [1]. For example, in the Legal dataset, LightRAG achieves an 83.6% win rate in Comprehensiveness compared to 16.4% for Naive RAG and an 84.8% win rate in Overall compared to 15.2% for RQ-RAG [1]. Ablation studies confirm the effectiveness of the dual-level retrieval paradigm, showing performance drops when either low-level or high-level retrieval is removed [6].

In terms of efficiency, LightRAG is more cost-effective than GraphRAG, using fewer than 100 tokens and one API call during retrieval, compared to 610,000 tokens and hundreds of API calls for GraphRAG [1]. LightRAG is also more adaptable to new data, as it integrates new information without full reconstruction [1]. The system is open-source and available at https://github.com/HKUDS/LightRAG [1]. The document concludes by summarizing LightRAG’s contributions, including its enhanced efficiency, effectiveness, and adaptability [8].
```

## B4b-Q1-1

- 問題：`summary this document.`；模式 `navigate`；26.3 秒；2 次呼叫；tokens 7110
- 來源：[1] p1 summary, [2] p1 summary, [3] p1 summary, [4] p2 summary, [5] p3 summary, [6] p5 summary, [7] p10 summary, [8] p10 summary, [9] p13 summary, [10] p9 navigation, [11] p5 navigation, [12] p9 navigation, [13] p5 navigation, [14] p9 navigation
- 閱讀計畫（定位 6/6，保留 5，超預算 2）：
  - ✓ Section 1 INTRODUCTION | need: overview and purpose | priority: required | status: missing → 候選 5，納入 []，排除 [(4, 'low relevance'), (2, 'low relevance'), (1, 'low relevance'), (3, 'low relevance'), (0, 'low relevance')]
  - ✓ Section 2 RETRIEVAL-AUGMENTED GENERATION | need: background context | priority: required | status: missing → 候選 4，納入 []，排除 [(4, 'low relevance'), (7, 'low relevance'), (6, 'low relevance'), (5, 'low relevance')]
  - ✓ Section 3 THE LIGHT RAG ARCHITECTURE | need: framework description | priority: required | status: missing → 候選 8，納入 [14, 13, 7]，排除 [(11, 'low relevance'), (10, 'low relevance'), (12, 'low relevance'), (9, 'low relevance'), (8, 'target quota reached')]
  - ✓ Section 4 EVALUATION | need: performance analysis | priority: required | status: missing → 候選 9，納入 [25, 26, 27]，排除 [(18, 'target quota reached'), (24, 'target quota reached'), (23, 'target quota reached'), (20, 'target quota reached'), (17, 'target quota reached'), (14, 'target quota reached')]
  - ✓ Section 5 RELATED WORK | need: literature context | priority: supplementary | status: missing → 候選 3，納入 []，排除 [(29, 'low relevance'), (31, 'low relevance'), (30, 'over the evidence budget')]
  - ✓ Section 6 CONCLUSION | need: summary and implications | priority: required | status: missing → 候選 7，納入 []，排除 [(32, 'low relevance'), (34, 'low relevance'), (33, 'low relevance'), (31, 'low relevance'), (37, 'low relevance'), (35, 'low relevance'), (36, 'low relevance')]
- 分析狀態：UNCERTAIN；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 修正：[]；刪除 []；仍不符 []；方向待定 []
- 涵蓋判定：Section 1 INTRODUCTION→missing；Section 2 RETRIEVAL-AUGMENTED GENERATION→missing；Section 3 THE LIGHT RAG ARCHITECTURE→missing；Section 4 EVALUATION→missing；Section 5 RELATED WORK→missing；Section 6 CONCLUSION→missing；required 未納入 ['Section 1 INTRODUCTION', 'Section 2 RETRIEVAL-AUGMENTED GENERATION', 'Section 6 CONCLUSION']；supplementary 用 0；Matrix None
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
The document introduces LightRAG, a Retrieval-Augmented Generation (RAG) system designed to overcome limitations in existing RAG systems, such as flat data representations and poor contextual awareness, which lead to fragmented and less accurate responses [1]. LightRAG integrates graph structures into text indexing and retrieval, enabling the system to better represent interdependencies among entities and improve the synthesis of related information [3]. It features a dual-level retrieval framework that enhances both low-level and high-level knowledge discovery [5]. The system also includes an incremental update algorithm to adapt to new data efficiently [1].

Experiments on benchmark datasets from the UltraDomain benchmark show that LightRAG significantly outperforms baseline methods like NaiveRAG, RQ-RAG, HyDE, and GraphRAG in terms of retrieval accuracy and efficiency [6]. Ablation studies confirm the importance of the dual-level retrieval paradigm, and cost analysis reveals that LightRAG is more efficient in token and API usage, using fewer than 100 tokens and a single API call compared to hundreds of thousands of tokens and hundreds of API calls required by GraphRAG [1].

The document also places LightRAG in the context of related work, highlighting its improvements over traditional RAG approaches that rely on fragmented text chunks and brute-force search methods [7]. Finally, the conclusion summarizes LightRAG’s contributions, including its graph-based indexing, dual-level retrieval, and incremental update capabilities, which together enhance retrieval efficiency and comprehensiveness [8].
```

## B4b-Q1-2

- 問題：`summary this document.`；模式 `navigate`；28.6 秒；2 次呼叫；tokens 7406
- 來源：[1] p1 summary, [2] p1 summary, [3] p1 summary, [4] p2 summary, [5] p3 summary, [6] p5 summary, [7] p10 summary, [8] p10 summary, [9] p13 summary, [10] p5 navigation, [11] p8 navigation, [12] p5 navigation
- 閱讀計畫（定位 6/6，保留 3，超預算 10）：
  - ✓ Section 1 INTRODUCTION | need: overview and objectives | priority: required | status: missing → 候選 5，納入 []，排除 [(4, 'low relevance'), (1, 'low relevance'), (0, 'low relevance'), (3, 'low relevance'), (2, 'low relevance')]
  - ✓ Section 2 RETRIEVAL-AUGMENTED GENERATION | need: background context | priority: required | status: missing → 候選 4，納入 []，排除 [(4, 'low relevance'), (7, 'low relevance'), (6, 'low relevance'), (5, 'low relevance')]
  - ✓ Section 3 THE LIGHT RAG ARCHITECTURE | need: framework description | priority: required | status: missing → 候選 8，納入 [14, 13]，排除 [(11, 'low relevance'), (10, 'low relevance'), (12, 'low relevance'), (9, 'low relevance'), (7, 'over the evidence budget'), (8, 'over the evidence budget')]
  - ✓ Section 4 EVALUATION | need: experimental results | priority: required | status: missing → 候選 9，納入 [22, 18]，排除 [(14, 'low relevance'), (19, 'over the evidence budget'), (27, 'over the evidence budget'), (28, 'over the evidence budget'), (24, 'over the evidence budget'), (21, 'over the evidence budget'), (26, 'over the evidence budget')]
  - ✓ Section 5 RELATED WORK | need: literature context | priority: supplementary | status: missing → 候選 3，納入 []，排除 [(29, 'low relevance'), (31, 'low relevance'), (30, 'over the evidence budget')]
  - ✓ Section 6 CONCLUSION | need: summary and implications | priority: required | status: missing → 候選 7，納入 []，排除 [(32, 'low relevance'), (34, 'low relevance'), (33, 'low relevance'), (31, 'low relevance'), (37, 'low relevance'), (35, 'low relevance'), (36, 'low relevance')]
- 分析狀態：UNCERTAIN；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 修正：[]；刪除 []；仍不符 []；方向待定 []
- 涵蓋判定：Section 1 INTRODUCTION→missing；Section 2 RETRIEVAL-AUGMENTED GENERATION→missing；Section 3 THE LIGHT RAG ARCHITECTURE→missing；Section 4 EVALUATION→missing；Section 5 RELATED WORK→missing；Section 6 CONCLUSION→missing；required 未納入 ['Section 1 INTRODUCTION', 'Section 2 RETRIEVAL-AUGMENTED GENERATION', 'Section 6 CONCLUSION']；supplementary 用 0；Matrix None
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
The document addresses limitations in existing Retrieval-Augmented Generation (RAG) systems, particularly their reliance on flat data representations and poor contextual awareness, which hinder the synthesis of inter-related information and lead to fragmented, less accurate responses. The authors propose LightRAG, a system that integrates graph structures into text indexing and retrieval, featuring a dual-level retrieval framework to enhance both low-level and high-level knowledge discovery. The system combines graph structures with vector representations to improve retrieval efficiency and result comprehensiveness, and includes an incremental update algorithm to adapt quickly to new data [1].

LightRAG uses a dual-level retrieval paradigm that supports the extraction of both specific and abstract information, addressing diverse user needs. It also includes a seamless incremental update capability, ensuring it stays current and responsive to new information [8]. Experiments on benchmark datasets from the UltraDomain benchmark show that LightRAG significantly outperforms baseline methods across four evaluation dimensions: Comprehensiveness, Diversity, Empowerment, and Overall. Ablation studies confirm the dual-level retrieval paradigm is critical to performance, with the hybrid mode achieving balanced results. Cost analysis reveals LightRAG is more efficient in token and API usage, using fewer than 100 tokens and a single API call during retrieval and data updates, compared to 610,000 tokens and hundreds of API calls for GraphRAG [1].

The authors have made LightRAG open-source and available at https://github.com/HKUDS/LightRAG [2]. Key contributions include emphasizing the importance of graph-empowered RAG systems, proposing LightRAG with dual-level retrieval and graph-enhanced indexing, and presenting experimental findings showing significant improvements over baseline methods in retrieval accuracy, response efficiency, and adaptability [3].
```

## B4b-Q1-3

- 問題：`summary this document.`；模式 `navigate`；33.8 秒；2 次呼叫；tokens 7260
- 來源：[1] p1 summary, [2] p1 summary, [3] p1 summary, [4] p2 summary, [5] p3 summary, [6] p5 summary, [7] p10 summary, [8] p10 summary, [9] p13 summary, [10] p5 navigation, [11] p12 navigation, [12] p8 navigation
- 閱讀計畫（定位 6/6，保留 3，超預算 27）：
  - ✓ Section 1 INTRODUCTION | need: overview of the document | priority: required | status: missing → 候選 5，納入 [4]，排除 [(1, 'low relevance'), (2, 'low relevance'), (0, 'over the evidence budget'), (3, 'over the evidence budget')]
  - ✓ Section 3 THE LIGHT RAG ARCHITECTURE | need: description of the framework | priority: required | status: missing → 候選 8，納入 [14]，排除 [(11, 'low relevance'), (10, 'low relevance'), (12, 'low relevance'), (9, 'low relevance'), (13, 'over the evidence budget'), (7, 'over the evidence budget'), (8, 'over the evidence budget')]
  - ✓ Section 4 EVALUATION | need: experimental results and analysis | priority: required | status: missing → 候選 9，納入 [22]，排除 [(18, 'over the evidence budget'), (19, 'over the evidence budget'), (24, 'over the evidence budget'), (27, 'over the evidence budget'), (21, 'over the evidence budget'), (26, 'over the evidence budget'), (23, 'over the evidence budget'), (15, 'over the evidence budget')]
  - ✓ Section 5 RELATED WORK | need: context in prior research | priority: supplementary | status: missing → 候選 3，納入 []，排除 [(30, 'over the evidence budget'), (31, 'over the evidence budget'), (29, 'over the evidence budget')]
  - ✓ Section 6 CONCLUSION | need: summary of contributions and findings | priority: required | status: missing → 候選 7，納入 [37, 35]，排除 [(31, 'low relevance'), (32, 'over the evidence budget'), (36, 'over the evidence budget'), (34, 'over the evidence budget'), (33, 'over the evidence budget')]
  - ✓ Section 7 APPENDIX | need: additional details and examples | priority: supplementary | status: missing → 候選 8，納入 []，排除 [(39, 'low relevance'), (41, 'low relevance'), (43, 'low relevance'), (38, 'over the evidence budget'), (40, 'over the evidence budget'), (44, 'over the evidence budget'), (45, 'over the evidence budget'), (42, 'over the evidence budget')]
- 分析狀態：UNCERTAIN；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 修正：[]；刪除 []；仍不符 []；方向待定 []
- 涵蓋判定：Section 1 INTRODUCTION→missing；Section 3 THE LIGHT RAG ARCHITECTURE→missing；Section 4 EVALUATION→missing；Section 5 RELATED WORK→missing；Section 6 CONCLUSION→missing；Section 7 APPENDIX→missing；required 未納入 []；supplementary 用 0；Matrix None
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
This document addresses limitations in Retrieval-Augmented Generation (RAG) systems, particularly their reliance on flat data representations and inadequate contextual awareness, which hinder the synthesis of inter-related information and lead to fragmented, less accurate responses. The authors propose LightRAG, a system that integrates graph structures into text indexing and retrieval, featuring a dual-level retrieval framework to enhance both low-level and high-level knowledge discovery. LightRAG combines graph structures with vector representations to improve retrieval efficiency and result comprehensiveness, and includes an incremental update algorithm to adapt quickly to new data [1].

The document outlines the LightRAG architecture, which segments documents into manageable pieces and leverages LLMs to extract entities and their relationships, forming a knowledge graph. This method offers two advantages: comprehensive information understanding through multi-hop subgraphs and enhanced retrieval performance via key-value data structures [5]. The dual-level retrieval paradigm handles both specific and abstract queries, using low-level and high-level strategies to retrieve detailed or conceptual information [5].

Extensive experiments using benchmark datasets from the UltraDomain benchmark demonstrate that LightRAG significantly outperforms baseline methods across four evaluation dimensions: Comprehensiveness, Diversity, Empowerment, and Overall. Ablation studies confirm the dual-level retrieval paradigm is critical to performance, with the hybrid mode achieving balanced results. Cost analysis reveals LightRAG is more efficient in token and API usage, using fewer than 100 tokens and a single API call during retrieval and data updates, compared to 610,000 tokens and hundreds of API calls for GraphRAG [6].

The document situates LightRAG in the context of prior research, noting that current RAG approaches typically embed queries in a vector space to find the nearest context vectors but often rely on fragmented text chunks and only retrieve the top-k contexts, limiting their ability to capture comprehensive global information. LightRAG overcomes these limitations by enabling dynamic updates and expansions of the knowledge graph and facilitating rapid retrieval of relevant information through the dual-level retrieval paradigm [7].

In conclusion, LightRAG introduces an advancement in RAG by integrating a graph-based indexing approach, which improves both efficiency and comprehension in information retrieval. It features a dual-level retrieval paradigm that supports the extraction of both specific and abstract information, addressing diverse user needs. The system also includes a seamless incremental update capability, ensuring it stays current and responsive to new information [8].
```

## C-Q1-1

- 問題：`summary this document.`；模式 `single`；24.8 秒；1 次呼叫；tokens 4371
- 來源：[1] p1 summary, [2] p1 summary, [3] p1 summary, [4] p2 summary, [5] p3 summary, [6] p5 summary, [7] p10 summary, [8] p10 summary, [9] p13 summary
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
The document "LightRAG: Simple and Fast Retrieval-Augmented Generation" introduces a novel Retrieval-Augmented Generation (RAG) system called LightRAG, designed to improve the accuracy, efficiency, and adaptability of large language models (LLMs) by incorporating external knowledge sources through graph-based indexing [1]. Current RAG systems are limited by flat data representations and a lack of contextual awareness, leading to fragmented responses [2]. LightRAG addresses these issues by using graph structures to represent interdependencies among entities, enabling a dual-level retrieval mechanism that captures both specific and abstract information [3].

The system segments documents into chunks, extracts entities and relationships using an LLM, and builds a knowledge graph. This graph structure enhances keyword matching and captures high-order relatedness from neighboring nodes. The dual-level retrieval framework allows for low-level retrieval of specific entities and high-level retrieval of broader topics [5]. During answer generation, the LLM integrates the retrieved information to produce contextually relevant responses [1].

Experiments across four datasets—Agriculture, CS, Legal, and Mix—demonstrate that LightRAG outperforms existing RAG methods such as NaiveRAG, RQ-RAG, HyDE, and GraphRAG in four evaluation dimensions: Comprehensiveness, Diversity, Empowerment, and Overall. For example, in the Legal dataset, LightRAG achieves an 83.6% win rate in Comprehensiveness, significantly higher than NaiveRAG’s 16.4% [6]. Ablation studies confirm the importance of the dual-level retrieval mechanism, showing that variants lacking either level perform worse than the full version [8].

LightRAG is more efficient than GraphRAG, using fewer than 100 tokens and a single API call during retrieval, compared to GraphRAG’s 610,000 tokens and hundreds of API calls [6]. It also supports fast adaptation to new data through incremental updates, whereas GraphRAG must reconstruct its entire structure, incurring a high token cost [10].

The document concludes that LightRAG excels in both efficiency and effectiveness, significantly improving the speed and quality of information retrieval and generation while reducing costs for LLM inference [10]. The system is open-source and available at https://github.com/HKUDS/LightRAG [2].
```

## C-Q1-2

- 問題：`summary this document.`；模式 `single`；14.5 秒；1 次呼叫；tokens 4224
- 來源：[1] p1 summary, [2] p1 summary, [3] p1 summary, [4] p2 summary, [5] p3 summary, [6] p5 summary, [7] p10 summary, [8] p10 summary, [9] p13 summary
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
The document introduces LightRAG, a novel Retrieval-Augmented Generation (RAG) system designed to improve the accuracy and efficiency of large language models (LLMs) by incorporating graph-based indexing and a dual-level retrieval framework. Current RAG systems are limited by flat data representations and a lack of contextual awareness, leading to fragmented and incomplete responses [1]. LightRAG addresses these limitations by constructing a knowledge graph from documents, using an LLM to extract entities and relationships, and implementing a dual-level retrieval mechanism to capture both specific and abstract information [1]. 

Experiments conducted across four datasets—Agriculture, CS, Legal, and Mix—demonstrate that LightRAG outperforms existing RAG methods such as NaiveRAG, RQ-RAG, HyDE, and GraphRAG in four evaluation dimensions: Comprehensiveness, Diversity, Empowerment, and Overall [1]. For instance, in the Legal dataset, LightRAG achieves an 83.6% win rate in Comprehensiveness compared to NaiveRAG’s 16.4% [1]. Additionally, LightRAG is more efficient, using fewer than 100 tokens and a single API call during retrieval, compared to GraphRAG’s 610,000 tokens and hundreds of API calls [1]. It also supports fast adaptation to new data through an incremental update algorithm, unlike GraphRAG, which requires reconstructing its entire structure [1]. 

Overall, LightRAG enhances information retrieval by leveraging graph structures and dual-level retrieval, improving response quality while reducing computational costs and enabling seamless integration of new information [1].
```

## C-Q1-3

- 問題：`summary this document.`；模式 `single`；21.6 秒；1 次呼叫；tokens 4395
- 來源：[1] p1 summary, [2] p1 summary, [3] p1 summary, [4] p2 summary, [5] p3 summary, [6] p5 summary, [7] p10 summary, [8] p10 summary, [9] p13 summary
- 檢查：標籤不符 ['54.4%']；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 ['13,990,000']

```text
The document introduces LightRAG, a novel Retrieval-Augmented Generation (RAG) system designed to improve the accuracy and efficiency of large language models (LLMs) by incorporating external knowledge sources through graph-based indexing [1]. Current RAG systems are limited by flat data representations and a lack of contextual awareness, leading to fragmented and incomplete responses [1]. LightRAG addresses these issues by integrating graph structures into text indexing and retrieval, using a dual-level retrieval framework to capture both specific and abstract information [1]. The system segments documents into manageable chunks, extracts entities and relationships using an LLM, and builds a knowledge graph to enhance keyword matching and capture high-order relatedness [1]. 

The dual-level retrieval mechanism in LightRAG enables low-level retrieval of specific entities and high-level retrieval of broader topics, allowing the system to produce contextually relevant responses [1]. Experiments across four datasets—Agriculture, CS, Legal, and Mix—show that LightRAG outperforms existing RAG methods such as NaiveRAG, RQ-RAG, HyDE, and GraphRAG in four evaluation dimensions: Comprehensiveness, Diversity, Empowerment, and Overall [1]. For instance, in the Legal dataset, LightRAG achieves an 83.6% win rate in Comprehensiveness, significantly higher than NaiveRAG’s 16.4% [1]. In the Agriculture dataset, LightRAG achieves 67.6% in Comprehensiveness compared to GraphRAG’s 54.4% [1]. Ablation studies confirm the importance of the dual-level retrieval mechanism, as variants that remove one level of retrieval perform worse than the full version [1].

LightRAG is more efficient than GraphRAG, using fewer than 100 tokens and a single API call during retrieval, compared to GraphRAG’s 610,000 tokens and hundreds of API calls [1]. It also integrates new data seamlessly during incremental updates, whereas GraphRAG must reconstruct its entire structure, incurring a token cost of around 13,990,000 for 1,399 communities [1]. The system is open-source and available at https://github.com/HKUDS/LightRAG [2]. Overall, LightRAG excels in both efficiency and effectiveness, significantly improving the speed and quality of information retrieval and generation while reducing costs for LLM inference [8].

Numbers that could not be checked against the cited pages of the original text: 13,990,000.

Figures whose labels differ from the source table: 54.4% (answer: Comprehensiveness, Agriculture, GraphRAG; source: Comprehensiveness, Agriculture, LightRAG, vs GraphRAG).
```

## A-Q2-1

- 問題：`compare lightRAG with GraphRAG`；模式 `roles`；16.1 秒；1 次呼叫；tokens 2973
- 來源：[1] p7 retrieval, [2] p7 retrieval, [3] p9 retrieval, [4] p8 retrieval, [5] p10 retrieval
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
Navigator:  
The comparison between LightRAG and GraphRAG is discussed in Section: EVALUATION (pages 5-10), Table 1 (page 7), Table 3 (page 9), and Section: CONCLUSION (page 10).  

Analyst:  
The main findings indicate that LightRAG outperforms GraphRAG in several aspects, particularly in larger datasets with complex language contexts. For instance, in the Agriculture, CS, and Legal datasets—each containing millions of tokens—LightRAG shows a clear advantage, significantly surpassing GraphRAG [1]. This is attributed to LightRAG’s dual-level retrieval paradigm, which combines low-level retrieval of specific entities with high-level retrieval of broader topics [2].  

In a case study presented in Table 3, LightRAG outperforms GraphRAG in all evaluation dimensions assessed by the LLM judge, including comprehensiveness, diversity, empowerment, and overall quality [4].  

Additionally, in terms of cost and adaptability, LightRAG demonstrates superior efficiency. While both models exhibit similar overhead for entity and relationship extraction during the incremental data update phase, GraphRAG shows significant inefficiency in managing newly added data. In contrast, LightRAG seamlessly integrates newly extracted entities and relationships into the existing graph without the need for full reconstruction, resulting in significantly lower overhead [5].  

However, no explicit results in the provided sources contradict this trend.  

In conclusion, LightRAG demonstrates superior performance over GraphRAG in handling complex queries, providing diverse and comprehensive responses, and maintaining efficiency during incremental updates.
```

## A-Q2-2

- 問題：`compare lightRAG with GraphRAG`；模式 `roles`；18.1 秒；1 次呼叫；tokens 3072
- 來源：[1] p7 retrieval, [2] p7 retrieval, [3] p9 retrieval, [4] p8 retrieval, [5] p10 retrieval
- 檢查：標籤不符 []；全稱宣稱 1；引用可疑 []；未解析 0；找不到的數字 []

```text
**Navigator:**  
The sections, tables, and figures relevant to comparing LightRAG with GraphRAG include:  
- Section: EVALUATION (pages 5-10)  
- Table 1 (page 7): Win rates (%) of baselines v.s. LightRAG across four datasets and four evaluation dimensions.  
- Table 2 (page 8): Performance of ablated versions of LightRAG, using NaiveRAG as reference.  
- Table 3 (page 9): Case Study: Comparison Between LightRAG and the Baseline Method GraphRAG.  
- Figure 2 (page 9): Comparison of Cost in Terms of Tokens and API Calls for GraphRAG and LightRAG on the Legal Dataset.  
- Section: CONCLUSION (page 10)  

**Analyst:**  
LightRAG consistently outperforms GraphRAG in multiple evaluation dimensions. In particular, in the Agriculture, CS, and Legal datasets—each containing millions of tokens—LightRAG shows a clear advantage, significantly surpassing GraphRAG and highlighting its strength in comprehensive information understanding within diverse environments [1]. In the case study presented in Table 3, LightRAG outperforms in all evaluation dimensions assessed by the LLM judge, including comprehensiveness, diversity, empowerment, and overall quality [4].  

LightRAG also demonstrates superior efficiency in the incremental data update phase. When new data is introduced, GraphRAG must dismantle its existing community structure to incorporate new entities and relationships, which incurs a substantial token cost. In contrast, LightRAG seamlessly integrates newly extracted entities and relationships into the existing graph without the need for full reconstruction, resulting in significantly lower overhead [5]. This cost difference is visualized in Figure 2, which compares the token and API call costs of GraphRAG and LightRAG on the Legal dataset [3].  

There are no explicitly noted results that go against this trend. In conclusion, LightRAG offers both superior performance and cost efficiency over GraphRAG in the datasets and evaluation dimensions examined.

A claim the source table does not bear out: "LightRAG consistently outperforms GraphRAG in multiple evaluation dimensions." — LightRAG is above the compared methods in 61 cells and below in 3, for example Comprehensiveness / Mix: LightRAG 49.6% vs GraphRAG 50.4% (p. 7); Empowerment / Mix: LightRAG 49.2% vs GraphRAG 50.8% (p. 7); Overall / Mix: LightRAG 49.6% vs GraphRAG 50.4% (p. 7).
```

## A-Q2-3

- 問題：`compare lightRAG with GraphRAG`；模式 `roles`；18.5 秒；1 次呼叫；tokens 3081
- 來源：[1] p7 retrieval, [2] p7 retrieval, [3] p9 retrieval, [4] p8 retrieval, [5] p10 retrieval
- 檢查：標籤不符 []；全稱宣稱 1；引用可疑 [([3], [5]), ([3], [5])]；未解析 0；找不到的數字 ['10']

```text
**Navigator:**  
The sections, tables, and figures relevant to comparing LightRAG with GraphRAG are:  
- Section: EVALUATION (pages 5-10)  
- Table 1 (page 7): Win rates (%) of baselines v.s. LightRAG across four datasets and four evaluation dimensions.  
- Table 3 (page 9): Case Study: Comparison Between LightRAG and the Baseline Method GraphRAG.  
- Figure 2 (page 9): Comparison of Cost in Terms of Tokens and API Calls for GraphRAG and LightRAG on the Legal Dataset.  
- Section: CONCLUSION (page 10)  

---

**Analyst:**  
LightRAG consistently outperforms GraphRAG in several key areas. First, in larger datasets with complex language contexts such as Agriculture, CS, and Legal, LightRAG shows a clear advantage, significantly surpassing GraphRAG [1]. This is attributed to its dual-level retrieval paradigm, which integrates low-level retrieval of specific entities with high-level retrieval of broader topics, thereby improving response diversity and comprehensiveness [2]. 

In the case study presented in Table 3, LightRAG outperforms GraphRAG in all evaluation dimensions assessed, including comprehensiveness, diversity, empowerment, and overall quality [4]. Specifically, LightRAG covers a broader range of relevant information and provides more diverse and empowering content, which is linked to its hierarchical retrieval mechanism and effective graph-based indexing [4].

Additionally, LightRAG demonstrates superior efficiency and cost-effectiveness during incremental data updates. As shown in Figure 2, GraphRAG must reconstruct its community structure when new data is added, leading to significantly higher token and API call costs compared to LightRAG, which seamlessly integrates new information without full reconstruction [3].

However, there are no explicit results in the sources provided that contradict this trend. Therefore, the conclusion is that LightRAG outperforms GraphRAG in performance, diversity, comprehensiveness, and cost-efficiency, especially in large-scale and complex datasets [1][2][3][4].

Numbers that could not be checked against the cited pages of the original text: 10.

A claim the source table does not bear out: "LightRAG consistently outperforms GraphRAG in several key areas." — LightRAG is above the compared methods in 61 cells and below in 3, for example Comprehensiveness / Mix: LightRAG 49.6% vs GraphRAG 50.4% (p. 7); Empowerment / Mix: LightRAG 49.2% vs GraphRAG 50.8% (p. 7); Overall / Mix: LightRAG 49.6% vs GraphRAG 50.4% (p. 7).
```

## B-Q2-1

- 問題：`compare lightRAG with GraphRAG`；模式 `navigate`；29.9 秒；2 次呼叫；tokens 7182
- 來源：[1] p7 retrieval, [2] p7 retrieval, [3] p9 retrieval, [4] p8 retrieval, [5] p10 retrieval, [6] p7 navigation, [7] p9 navigation, [8] p9 navigation, [9] p9 navigation, [10] p5 navigation, [11] p5 navigation
- 閱讀計畫（定位 6/6，保留 7，超預算 16）：
  - ✓ Table 1 (page 7): Win rates (%) of baselines v.s. LightRAG across four datasets and four evaluation dimensions.
  - ✓ Table 3 (page 9): Case Study: Comparison Between LightRAG and the Baseline Method GraphRAG.
  - ✓ Section: EVALUATION (pages 5-10): General context for evaluating LightRAG and GraphRAG.
  - ✓ Section: THE LIGHT RAG ARCHITECTURE (pages 3-5): Describes LightRAG's design compared to alternatives like GraphRAG.
  - ✓ Section: CONCLUSION (page 10): Summary of LightRAG's performance relative to other methods.
  - ✓ Figure 1 (page 3): Overall architecture of the proposed LightRAG framework.
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
LightRAG consistently outperforms GraphRAG, particularly in larger datasets with complex language contexts, such as Agriculture, CS, and Legal [1]. For example, in the Legal dataset, LightRAG achieves a win rate of 83.6% in comprehensiveness compared to 48.4% for GraphRAG [6]. Similarly, in the Diversity metric, LightRAG achieves 86.4% in the Legal dataset, while GraphRAG only reaches 26.4% [6]. 

In a case study, LightRAG outperforms GraphRAG in all evaluation dimensions, including comprehensiveness, diversity, empowerment, and overall quality [7]. LightRAG provides a broader array of metrics and includes nuanced explanations, whereas GraphRAG focuses primarily on standard metrics without much exploration of potential nuances [8].

In terms of cost and adaptability, LightRAG demonstrates superior efficiency. While GraphRAG requires significant token consumption and numerous API calls, LightRAG uses fewer than 100 tokens for keyword generation and retrieval, requiring only a single API call for the entire process [9]. This efficiency is achieved through an optimized retrieval mechanism that integrates newly extracted entities and relationships into the existing graph without the need for full reconstruction [5].

However, there are some cases where GraphRAG performs comparably to LightRAG. For instance, in the Mix dataset, GraphRAG achieves 50.4% in comprehensiveness, while LightRAG reaches 49.6% [6]. This slight difference suggests that the performance advantage of LightRAG is not universal and can vary depending on the dataset. 

In conclusion, LightRAG generally outperforms GraphRAG in most evaluation metrics and scenarios, particularly in larger and more complex datasets, but there are exceptions where the performance is closely matched.
```

## B-Q2-2

- 問題：`compare lightRAG with GraphRAG`；模式 `navigate`；32.1 秒；2 次呼叫；tokens 7226
- 來源：[1] p7 retrieval, [2] p7 retrieval, [3] p9 retrieval, [4] p8 retrieval, [5] p10 retrieval, [6] p7 navigation, [7] p9 navigation, [8] p9 navigation, [9] p9 navigation, [10] p5 navigation, [11] p5 navigation
- 閱讀計畫（定位 6/6，保留 7，超預算 16）：
  - ✓ Table 1 (page 7): Win rates (%) of baselines v.s. LightRAG across four datasets and four evaluation dimensions.
  - ✓ Table 3 (page 9): Case Study: Comparison Between LightRAG and the Baseline Method GraphRAG.
  - ✓ Section: EVALUATION (pages 5-10): General context for comparing LightRAG with GraphRAG.
  - ✓ Section: THE LIGHT RAG ARCHITECTURE (pages 3-5): Describes LightRAG's design, relevant for contrast.
  - ✓ Section: RELATED WORK (page 10): May reference GraphRAG and its context.
  - ✓ Figure 1 (page 3): Overall architecture of the proposed LightRAG framework.
- 檢查：標籤不符 ['51.6%', '73.6%', '26.4%', '43.6%']；全稱宣稱 0；引用可疑 [([6], [3])]；未解析 2；找不到的數字 []

```text
LightRAG consistently outperforms GraphRAG, particularly in larger datasets with complex language contexts. For instance, in the Agriculture, CS, and Legal datasets—each containing millions of tokens—LightRAG shows a clear advantage over GraphRAG, highlighting its strength in comprehensive information understanding within diverse environments [2]. 

In terms of evaluation metrics, LightRAG demonstrates superior performance in comprehensiveness, diversity, and empowerment. For example, in the Agriculture dataset, LightRAG achieved a 54.4% win rate in comprehensiveness against GraphRAG's 45.6%, and a 77.2% win rate in diversity compared to GraphRAG's 22.8% [6]. Similarly, in the Legal dataset, LightRAG's win rates in comprehensiveness, diversity, and empowerment were 51.6%, 73.6%, and 56.4%, respectively, compared to GraphRAG's 48.4%, 26.4%, and 43.6% [6].

A case study further illustrates LightRAG's superiority. When responding to a query on normalizing feature values for effective machine learning, LightRAG provided a broader array of metrics and more nuanced explanations, covering topics such as Mean Average Precision at K (MAPK), Area Under the Curve (AUC), and user engagement metrics. In contrast, GraphRAG's response was more focused on traditional metrics like precision, recall, and F1 score, lacking the depth and diversity of LightRAG's answer [7].

However, there are instances where GraphRAG performs relatively better. For example, in the Mix dataset, GraphRAG achieved a 50.4% win rate in comprehensiveness compared to LightRAG's 49.6% [6]. This suggests that while LightRAG generally outperforms GraphRAG, there are specific scenarios where GraphRAG may offer competitive results.

Overall, LightRAG's dual-level retrieval paradigm and efficient graph-based indexing contribute to its superior performance in handling complex queries and diverse datasets [2].

Figures whose labels differ from the source table: 51.6% (answer: Empowerment, Legal, LightRAG; source: Comprehensiveness, CS, LightRAG, vs GraphRAG / Comprehensiveness, Legal, LightRAG, vs GraphRAG); 73.6% (answer: Empowerment, Legal, LightRAG; source: Overall, Legal, LightRAG, vs HyDE / Diversity, Legal, LightRAG, vs GraphRAG); 26.4% (answer: Legal, LightRAG; source: Overall, Legal, HyDE, vs LightRAG / Diversity, Legal, GraphRAG, vs LightRAG); 43.6% (answer: Legal, LightRAG; source: Empowerment, Legal, GraphRAG, vs LightRAG).
```

## B-Q2-3

- 問題：`compare lightRAG with GraphRAG`；模式 `navigate`；43.8 秒；2 次呼叫；tokens 7497
- 來源：[1] p7 retrieval, [2] p7 retrieval, [3] p9 retrieval, [4] p8 retrieval, [5] p10 retrieval, [6] p7 navigation, [7] p9 navigation, [8] p9 navigation, [9] p9 navigation, [10] p16 navigation, [11] p16 navigation
- 閱讀計畫（定位 6/6，保留 7，超預算 18）：
  - ✓ Table 1 (page 7): Win rates (%) of baselines v.s. LightRAG across four datasets and four evaluation dimensions.
  - ✓ Table 3 (page 9): Case Study: Comparison Between LightRAG and the Baseline Method GraphRAG.
  - ✓ Table 5 (page 16): Case Study: Comparison Between LightRAG and the Baseline NaiveRAG.
  - ✓ Section: EVALUATION (pages 5-10): General context for comparative analysis.
  - ✓ Figure 1 (page 3): Overall architecture of the proposed LightRAG framework.
  - ✓ Section: THE LIGHT RAG ARCHITECTURE (pages 3-5): Describes the design differences.
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 12；找不到的數字 []

```text
LightRAG consistently outperforms GraphRAG across multiple evaluation dimensions, particularly in larger datasets with complex language contexts. For example, in the Agriculture dataset, LightRAG achieves a 54.4% win rate in comprehensiveness compared to GraphRAG’s 45.6%. In the CS dataset, LightRAG achieves a 51.6% win rate in comprehensiveness compared to GraphRAG’s 48.4%. In the Legal dataset, LightRAG achieves a 51.6% win rate in comprehensiveness compared to GraphRAG’s 48.4%. In the Mix dataset, LightRAG achieves a 49.6% win rate in comprehensiveness compared to GraphRAG’s 50.4%. These results demonstrate that LightRAG generally outperforms GraphRAG in comprehensiveness, with the exception of the Mix dataset, where GraphRAG slightly outperforms LightRAG [6]. 

In terms of diversity, LightRAG significantly outperforms GraphRAG in all datasets. For instance, in the Agriculture dataset, LightRAG achieves a 77.2% win rate in diversity compared to GraphRAG’s 22.8%. In the CS dataset, LightRAG achieves a 59.2% win rate in diversity compared to GraphRAG’s 40.8%. In the Legal dataset, LightRAG achieves a 73.6% win rate in diversity compared to GraphRAG’s 26.4%. In the Mix dataset, LightRAG achieves a 64.0% win rate in diversity compared to GraphRAG’s 36.0%. These results show that LightRAG consistently outperforms GraphRAG in diversity [6].

In terms of empowerment, LightRAG outperforms GraphRAG in the Agriculture dataset (58.8% win rate for LightRAG vs. 41.2% for GraphRAG), the CS dataset (54.8% win rate for LightRAG vs. 45.2% for GraphRAG), and the Legal dataset (56.4% win rate for LightRAG vs. 43.6% for GraphRAG). However, in the Mix dataset, GraphRAG slightly outperforms LightRAG (49.2% win rate for LightRAG vs. 50.8% for GraphRAG) [6].

In terms of overall performance, LightRAG outperforms GraphRAG in the Agriculture dataset (54.8% win rate for LightRAG vs. 45.2% for GraphRAG), the CS dataset (52.0% win rate for LightRAG vs. 48.0% for GraphRAG), and the Legal dataset (52.8% win rate for LightRAG vs. 47.2% for GraphRAG). However, in the Mix dataset, GraphRAG slightly outperforms LightRAG (49.6% win rate for LightRAG vs. 50.4% for GraphRAG) [6].

Overall, LightRAG demonstrates superior performance compared to GraphRAG in most evaluation dimensions and datasets, with the exception of the Mix dataset in comprehensiveness, empowerment, and overall performance, where GraphRAG slightly outperforms LightRAG [6].
```

## B2-Q2-1

- 問題：`compare lightRAG with GraphRAG`；模式 `navigate`；27.3 秒；2 次呼叫；tokens 7734
- 來源：[1] p7 retrieval, [2] p7 retrieval, [3] p9 retrieval, [4] p8 retrieval, [5] p10 retrieval, [6] p9 navigation, [7] p16 navigation, [8] p16 navigation, [9] p9 navigation, [10] p8 navigation, [11] p16 navigation
- 閱讀計畫（定位 6/6，保留 7，超預算 2）：
  - ✓ Section 4.2 COMPARISON OF LIGHT RAG WITH EXISTING RAG METHODS (RQ1) | need: comparison with GraphRAG in datasets | priority: required | status: covered → 候選 4，納入 []，排除 [(20, 'already among the retrieved sources'), (21, 'already among the retrieved sources'), (19, 'over the evidence budget'), (18, 'over the evidence budget')]
  - ✓ Section 4.3 ABLATION STUDIES (RQ2) | need: ablation results related to GraphRAG | priority: required | status: covered → 候選 3，納入 [22, 23]，排除 [(21, 'already among the retrieved sources')]
  - ✓ Section 4.4 CASE STUDY (RQ3) | need: case study comparison with GraphRAG | priority: required | status: missing → 候選 5，納入 []，排除 [(27, 'already among the retrieved sources'), (24, 'already among the retrieved sources'), (25, 'already selected for another target'), (23, 'already selected for another target'), (26, 'already selected for another target')]
  - ✓ Table 3 (page 9) | need: case study comparison data with GraphRAG | priority: required | status: missing → 候選 3，納入 [25, 26]，排除 [(27, 'already among the retrieved sources')]
  - ✓ Section 7.4 CASE STUDY: COMPARISON BETWEEN LIGHT RAG AND THE BASELINE NAIVE RAG | need: additional comparative insights | priority: supplementary | status: missing → 候選 2，納入 [44, 45]，排除 []
  - ✓ Table 5 (page 16) | need: case study comparison data with baseline (indirect context for GraphRAG) | priority: supplementary | status: missing → 候選 2，納入 [43]，排除 [(44, 'already selected for another target')]
- 檢查：標籤不符 []；全稱宣稱 1；引用可疑 []；未解析 0；找不到的數字 []

```text
LightRAG consistently outperforms GraphRAG, particularly in larger datasets with complex language contexts. For instance, in the Agriculture, CS, and Legal datasets—each containing millions of tokens—LightRAG shows a clear advantage, significantly surpassing GraphRAG and highlighting its strength in comprehensive information understanding within diverse environments [2]. 

In terms of response diversity, LightRAG’s dual-level retrieval paradigm allows it to generate a wider range of responses, especially in scenarios where diverse content is essential. This is particularly evident in the Legal dataset, where LightRAG demonstrates a significant lead in diversity metrics [1].

In a case study comparing LightRAG and GraphRAG, LightRAG outperformed GraphRAG in all evaluation dimensions assessed by the LLM judge, including comprehensiveness, diversity, empowerment, and overall quality. Specifically, LightRAG covered a broader range of machine learning metrics and provided more empowering content due to its hierarchical retrieval paradigm [4].

However, there are no explicit results provided that contradict this trend in the given sources. Therefore, based on the data presented, LightRAG appears to consistently outperform GraphRAG across various metrics and datasets.

A claim the source table does not bear out: "Therefore, based on the data presented, LightRAG appears to consistently outperform GraphRAG across various metrics and datasets." — LightRAG is above the compared methods in 61 cells and below in 3, for example Comprehensiveness / Mix: LightRAG 49.6% vs GraphRAG 50.4% (p. 7); Empowerment / Mix: LightRAG 49.2% vs GraphRAG 50.8% (p. 7); Overall / Mix: LightRAG 49.6% vs GraphRAG 50.4% (p. 7).
```

## B2-Q2-2

- 問題：`compare lightRAG with GraphRAG`；模式 `navigate`；33.0 秒；2 次呼叫；tokens 7849
- 來源：[1] p7 retrieval, [2] p7 retrieval, [3] p9 retrieval, [4] p8 retrieval, [5] p10 retrieval, [6] p7 navigation, [7] p9 navigation, [8] p4 navigation, [9] p9 navigation, [10] p4 navigation, [11] p5 navigation
- 閱讀計畫（定位 6/6，保留 7，超預算 2）：
  - ✓ Section 4.2 COMPARISON OF LIGHT RAG WITH EXISTING RAG METHODS (RQ1) | need: comparison with GraphRAG | priority: required | status: missing → 候選 4，納入 []，排除 [(20, 'already among the retrieved sources'), (21, 'already among the retrieved sources'), (19, 'already selected for another target'), (18, 'over the evidence budget')]
  - ✓ Table 1 (page 7) | need: win rates comparison with GraphRAG | priority: required | status: missing → 候選 3，納入 [19]，排除 [(20, 'already among the retrieved sources'), (21, 'already among the retrieved sources')]
  - ✓ Section 4.4 CASE STUDY (RQ3) | need: case study comparison with GraphRAG | priority: required | status: missing → 候選 5，納入 []，排除 [(27, 'already among the retrieved sources'), (24, 'already among the retrieved sources'), (25, 'already selected for another target'), (23, 'already selected for another target'), (26, 'already selected for another target')]
  - ✓ Table 3 (page 9) | need: case study comparison data with GraphRAG | priority: required | status: missing → 候選 3，納入 [25, 26]，排除 [(27, 'already among the retrieved sources')]
  - ✓ Section 4.3 ABLATION STUDIES (RQ2) | need: mention of GraphRAG in ablation context | priority: supplementary | status: missing → 候選 3，納入 [23]，排除 [(21, 'already among the retrieved sources'), (22, 'over the evidence budget')]
  - ✓ Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM | need: architectural differences from GraphRAG | priority: supplementary | status: missing → 候選 3，納入 [11, 12, 13]，排除 []
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
LightRAG consistently outperforms GraphRAG, particularly in larger datasets with complex language contexts. In the Agriculture, CS, and Legal datasets—each containing millions of tokens—LightRAG shows a clear advantage, significantly surpassing GraphRAG [1]. 

In terms of win rates across four evaluation dimensions, LightRAG achieves higher percentages than GraphRAG in most cases. For example, in the Legal dataset, LightRAG has a 52.8% win rate in the Overall category compared to GraphRAG’s 47.2% [6]. In the Diversity category, LightRAG achieves 73.6% in the Legal dataset compared to GraphRAG’s 26.4% [6]. 

A case study further supports this comparison. When answering a question about methods to normalize feature values for effective machine learning, LightRAG provides a broader array of metrics and more nuanced explanations compared to GraphRAG. LightRAG’s response is judged as superior in comprehensiveness, diversity, and empowerment [7].

The architectural differences between the two methods also contribute to LightRAG’s performance. LightRAG employs a dual-level retrieval paradigm that integrates both low-level and high-level retrieval strategies, allowing it to address both detailed and abstract queries effectively [8]. This approach enables LightRAG to capture a comprehensive global perspective of the knowledge domain, contributing to better RAG performance [7]. 

However, in the Mix dataset, GraphRAG achieves a slightly higher win rate in the Overall category (50.4%) compared to LightRAG (49.6%) [6]. This suggests that while LightRAG generally performs better, there may be specific contexts where GraphRAG is competitive. 

In conclusion, LightRAG demonstrates superior performance over GraphRAG in most scenarios, particularly in larger and more complex datasets, though there are exceptions in certain cases.
```

## B2-Q2-3

- 問題：`compare lightRAG with GraphRAG`；模式 `navigate`；28.6 秒；2 次呼叫；tokens 7851
- 來源：[1] p7 retrieval, [2] p7 retrieval, [3] p9 retrieval, [4] p8 retrieval, [5] p10 retrieval, [6] p9 navigation, [7] p10 navigation, [8] p4 navigation, [9] p9 navigation, [10] p8 navigation, [11] p10 navigation
- 閱讀計畫（定位 6/6，保留 6，超預算 7）：
  - ✓ Section 4.2 COMPARISON OF LIGHT RAG WITH EXISTING RAG METHODS (RQ1) | need: comparison with GraphRAG | priority: required | status: covered → 候選 4，納入 []，排除 [(20, 'already among the retrieved sources'), (21, 'already among the retrieved sources'), (19, 'over the evidence budget'), (18, 'over the evidence budget')]
  - ✓ Section 4.3 ABLATION STUDIES (RQ2) | need: ablation results involving GraphRAG | priority: required | status: covered → 候選 3，納入 [22]，排除 [(21, 'already among the retrieved sources'), (23, 'over the evidence budget')]
  - ✓ Section 4.4 CASE STUDY (RQ3) | need: case study comparison with GraphRAG | priority: required | status: missing → 候選 5，納入 []，排除 [(27, 'already among the retrieved sources'), (24, 'already among the retrieved sources'), (25, 'already selected for another target'), (23, 'over the evidence budget'), (26, 'already selected for another target')]
  - ✓ Table 3 (page 9) | need: case study comparison data | priority: required | status: missing → 候選 3，納入 [25, 26]，排除 [(27, 'already among the retrieved sources')]
  - ✓ Section 3.1 GRAPH-BASED TEXT INDEXING | need: graph-based methods context | priority: supplementary | status: missing → 候選 5，納入 [10]，排除 [(9, 'low relevance'), (8, 'over the evidence budget'), (11, 'over the evidence budget'), (7, 'over the evidence budget')]
  - ✓ Section 5.2 LARGE LANGUAGE MODEL FOR GRAPHS | need: related work on graphs | priority: supplementary | status: missing → 候選 2，納入 [31, 30]，排除 []
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
LightRAG consistently outperforms GraphRAG, particularly in larger datasets with complex language contexts. For example, in the Agriculture, CS, and Legal datasets—each containing millions of tokens—LightRAG shows a clear advantage over GraphRAG, demonstrating its strength in comprehensive information understanding within diverse environments [2]. 

In terms of response diversity, LightRAG integrates low-level retrieval of specific entities with high-level retrieval of broader topics, which effectively addresses both detailed and abstract queries [2]. This dual-level retrieval mechanism contributes to a broader range of responses, especially in larger datasets such as Legal, where diversity is essential [1].

From a cost and adaptability perspective, LightRAG is significantly more efficient. While GraphRAG requires the complete regeneration of community structures when new data is introduced, LightRAG seamlessly integrates newly extracted entities and relationships into the existing graph without full reconstruction. This leads to significantly lower overhead during incremental updates [5].

In case studies, LightRAG outperforms GraphRAG in all evaluation dimensions assessed by the LLM judge, including comprehensiveness, diversity, empowerment, and overall quality. For instance, in a machine learning question case study, LightRAG provides a broader array of metrics and more nuanced explanations compared to GraphRAG [6].

In summary, LightRAG demonstrates superior performance in diverse environments, enhanced response variety, improved efficiency in incremental updates, and better case study outcomes compared to GraphRAG.
```

## B3-Q2-1

- 問題：`compare lightRAG with GraphRAG`；模式 `navigate`；43.9 秒；2 次呼叫；tokens 7716
- 來源：[1] p7 retrieval, [2] p7 retrieval, [3] p9 retrieval, [4] p8 retrieval, [5] p10 retrieval, [6] p7 navigation, [7] p6 navigation, [8] p9 navigation, [9] p4 navigation
- 閱讀計畫（定位 6/6，保留 4，超預算 0）：
  - ✓ Section 4.2 COMPARISON OF LIGHT RAG WITH EXISTING RAG METHODS (RQ1) | need: comparison with GraphRAG | priority: required | status: missing → 候選 4，納入 [18]，排除 [(20, 'already among the retrieved sources'), (21, 'already among the retrieved sources'), (19, 'already selected for another target')]
  - ✓ Section 4.3 ABLATION STUDIES (RQ2) | need: ablation results involving GraphRAG | priority: supplementary | status: missing → 候選 3，納入 []，排除 [(21, 'already among the retrieved sources'), (22, 'supplementary cap reached'), (23, 'supplementary cap reached')]
  - ✓ Section 4.4 CASE STUDY (RQ3) | need: case study comparison with GraphRAG | priority: supplementary | status: missing → 候選 5，納入 []，排除 [(27, 'already among the retrieved sources'), (24, 'supplementary cap reached'), (25, 'supplementary cap reached'), (23, 'supplementary cap reached'), (26, 'supplementary cap reached')]
  - ✓ Table 1 (page 7) | need: quantitative comparison with GraphRAG | priority: required | status: missing → 候選 3，納入 [19]，排除 [(20, 'already among the retrieved sources'), (21, 'already among the retrieved sources')]
  - ✓ Table 3 (page 9) | need: case study comparison data | priority: supplementary | status: missing → 候選 3，納入 [25]，排除 [(26, 'supplementary cap reached'), (27, 'supplementary cap reached')]
  - ✓ Section 3.1 GRAPH-BASED TEXT INDEXING | need: architecture differences | priority: supplementary | status: missing → 候選 5，納入 [10]，排除 [(9, 'low relevance'), (11, 'supplementary cap reached'), (8, 'supplementary cap reached'), (7, 'supplementary cap reached')]
- 分析狀態：UNCERTAIN；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 涵蓋判定：Section 4.2 COMPARISON OF LIGHT RAG WITH EXISTING RAG METHODS (RQ1)→partial；Section 4.3 ABLATION STUDIES (RQ2)→partial；Section 4.4 CASE STUDY (RQ3)→partial；Table 1 (page 7)→missing；Table 3 (page 9)→missing；Section 3.1 GRAPH-BASED TEXT INDEXING→missing；required 未納入 []；supplementary 用 2；Matrix {'cells': 128, 'tables': ['Table 1 [6]'], 'definitions': ['LightRAG']}
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
(1) The question asks to compare LightRAG with GraphRAG, including datasets, evaluation dimensions, and metrics. The datasets used are Agriculture, CS, Legal, and Mix. The evaluation dimensions are Comprehensiveness, Diversity, Empowerment, and Overall. Metrics are based on win rates (%) from Table 1.

(2) Method definitions:
- LightRAG: A graph-based RAG system using a dual-level retrieval paradigm and graph-based text indexing [2].
- GraphRAG: Not defined in the sources but described as a graph-based RAG system.

(3) Comparison of LightRAG and GraphRAG based on the same datasets, evaluation dimensions, and metrics from Table 1 [6]:

| Dataset | Evaluation Dimension | GraphRAG Win Rate (%) | LightRAG Win Rate (%) |
|---------|----------------------|------------------------|------------------------|
| Agriculture | Comprehensiveness | 45.6 | 54.4 |
| Agriculture | Diversity | 22.8 | 77.2 |
| Agriculture | Empowerment | 41.2 | 58.8 |
| Agriculture | Overall | 45.2 | 54.8 |
| CS | Comprehensiveness | 48.4 | 51.6 |
| CS | Diversity | 40.8 | 59.2 |
| CS | Empowerment | 45.2 | 54.8 |
| CS | Overall | 48.0 | 52.0 |
| Legal | Comprehensiveness | 48.4 | 51.6 |
| Legal | Diversity | 26.4 | 73.6 |
| Legal | Empowerment | 43.6 | 56.4 |
| Legal | Overall | 47.2 | 52.8 |
| Mix | Comprehensiveness | 50.4 | 49.6 |
| Mix | Diversity | 36.0 | 64.0 |
| Mix | Empowerment | 50.8 | 49.2 |
| Mix | Overall | 50.4 | 49.6 |

(4) Improvements:
- LightRAG outperforms GraphRAG in Comprehensiveness in Agriculture and CS.
- LightRAG significantly outperforms GraphRAG in Diversity in Agriculture, CS, and Legal.
- LightRAG outperforms GraphRAG in Empowerment in Agriculture and CS.
- LightRAG outperforms GraphRAG in Overall in Agriculture and CS.

Exceptions:
- In Mix, GraphRAG outperforms LightRAG in Comprehensiveness and Empowerment.
- In Mix, GraphRAG and LightRAG are nearly equal in Overall.

(5) These findings are consistent with the data in Table 1 [6], where LightRAG's win rates are higher than GraphRAG in most cases, particularly in the Diversity dimension.

(6) The comparison is based on Table 1 [6], and the definition of LightRAG is based on [2].

(7) The requested comparison is fully addressed.
```

## B3-Q2-2

- 問題：`compare lightRAG with GraphRAG`；模式 `navigate`；46.8 秒；2 次呼叫；tokens 8549
- 來源：[1] p7 retrieval, [2] p7 retrieval, [3] p9 retrieval, [4] p8 retrieval, [5] p10 retrieval, [6] p7 navigation, [7] p8 navigation, [8] p8 navigation
- 閱讀計畫（定位 6/6，保留 4，超預算 8）：
  - ✓ Section 4.2 COMPARISON OF LIGHT RAG WITH EXISTING RAG METHODS (RQ1) | need: comparison with GraphRAG | priority: required | status: missing → 候選 4，納入 [18]，排除 [(20, 'already among the retrieved sources'), (21, 'already among the retrieved sources'), (19, 'already selected for another target')]
  - ✓ Section 4.3 ABLATION STUDIES (RQ2) | need: performance comparison with GraphRAG | priority: required | status: missing → 候選 3，納入 [23, 22]，排除 [(21, 'already among the retrieved sources')]
  - ✓ Table 1 (page 7) | need: quantitative comparison with GraphRAG | priority: required | status: missing → 候選 3，納入 [19]，排除 [(20, 'already among the retrieved sources'), (21, 'already among the retrieved sources')]
  - ✓ Section 4.4 CASE STUDY (RQ3) | need: case study comparison with GraphRAG | priority: required | status: missing → 候選 5，納入 []，排除 [(27, 'already among the retrieved sources'), (24, 'already among the retrieved sources'), (25, 'over the evidence budget'), (23, 'already selected for another target'), (26, 'over the evidence budget')]
  - ✓ Table 3 (page 9) | need: case study comparison with GraphRAG | priority: supplementary | status: missing → 候選 3，納入 []，排除 [(25, 'over the evidence budget'), (26, 'over the evidence budget'), (27, 'already among the retrieved sources')]
  - ✓ Section 3.1 GRAPH-BASED TEXT INDEXING | need: architectural basis for comparison | priority: supplementary | status: missing → 候選 5，納入 []，排除 [(9, 'low relevance'), (10, 'over the evidence budget'), (11, 'over the evidence budget'), (8, 'over the evidence budget'), (7, 'over the evidence budget')]
- 分析狀態：UNCERTAIN；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 涵蓋判定：Section 4.2 COMPARISON OF LIGHT RAG WITH EXISTING RAG METHODS (RQ1)→partial；Section 4.3 ABLATION STUDIES (RQ2)→partial；Table 1 (page 7)→missing；Section 4.4 CASE STUDY (RQ3)→partial；Table 3 (page 9)→missing；Section 3.1 GRAPH-BASED TEXT INDEXING→missing；required 未納入 ['Section 4.4 CASE STUDY (RQ3)']；supplementary 用 0；Matrix {'cells': 256, 'tables': ['Table 1 [6]', 'Table 2 [8]'], 'definitions': ['LightRAG', '-High', 'NaiveRAG']}
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 [([6], [3])]；未解析 0；找不到的數字 []

```text
The question asks to compare LightRAG with GraphRAG, focusing on their performance across different datasets and evaluation metrics.

### Evidence and Definitions

- LightRAG is described as a graph-based RAG system that uses a dual-level retrieval paradigm combining low-level and high-level retrieval mechanisms to enhance response diversity and comprehensiveness [2].  
- GraphRAG is another graph-based RAG system, but it is not explicitly defined in the sources. Its performance is analyzed in comparison to LightRAG in the datasets and metrics described below.

### Performance Comparison

From **Table 1 (page 7)**, the win rates of LightRAG versus GraphRAG across four datasets (Agriculture, CS, Legal, Mix) and four evaluation dimensions (Comprehensiveness, Diversity, Empowerment, Overall) are as follows:

| Dataset | Metric        | LightRAG Win Rate (%) | GraphRAG Win Rate (%) |
|---------|---------------|------------------------|------------------------|
| Agriculture | Comprehensiveness | 54.4 | 45.6 |
| Agriculture | Diversity | 77.2 | 22.8 |
| Agriculture | Empowerment | 58.8 | 41.2 |
| Agriculture | Overall | 54.8 | 45.2 |
| CS        | Comprehensiveness | 51.6 | 48.4 |
| CS        | Diversity | 59.2 | 40.8 |
| CS        | Empowerment | 54.8 | 45.2 |
| CS        | Overall | 52.0 | 48.0 |
| Legal     | Comprehensiveness | 51.6 | 48.4 |
| Legal     | Diversity | 73.6 | 26.4 |
| Legal     | Empowerment | 56.4 | 43.6 |
| Legal     | Overall | 52.8 | 47.2 |
| Mix       | Comprehensiveness | 49.6 | 50.4 |
| Mix       | Diversity | 64.0 | 36.0 |
| Mix       | Empowerment | 49.2 | 50.8 |
| Mix       | Overall | 49.6 | 50.4 |

### Analysis

- **Comprehensiveness**: LightRAG outperforms GraphRAG in all datasets except for Mix, where both achieve nearly equal performance.
- **Diversity**: LightRAG significantly outperforms GraphRAG in all four datasets, with the largest margin in Agriculture and Legal.
- **Empowerment**: LightRAG performs better than GraphRAG in Agriculture, CS, and Legal, but GraphRAG slightly outperforms LightRAG in Mix.
- **Overall**: LightRAG outperforms GraphRAG in Agriculture, CS, and Legal, but GraphRAG slightly outperforms LightRAG in Mix.

### Conclusion

LightRAG demonstrates a consistent advantage over GraphRAG in most metrics and datasets, particularly in diversity and comprehensiveness. However, GraphRAG performs slightly better in the Mix dataset for empowerment and overall performance. This suggests that while LightRAG is generally superior, the performance may vary depending on the specific dataset and evaluation metric [6].
```

## B3-Q2-3

- 問題：`compare lightRAG with GraphRAG`；模式 `navigate`；41.6 秒；2 次呼叫；tokens 8537
- 來源：[1] p7 retrieval, [2] p7 retrieval, [3] p9 retrieval, [4] p8 retrieval, [5] p10 retrieval, [6] p9 navigation, [7] p9 navigation, [8] p8 navigation, [9] p8 navigation, [10] p6 navigation, [11] p10 navigation
- 閱讀計畫（定位 6/6，保留 7，超預算 1）：
  - ✓ Section 4.2 COMPARISON OF LIGHT RAG WITH EXISTING RAG METHODS (RQ1) | need: comparison results with GraphRAG | priority: required | status: covered → 候選 4，納入 [18]，排除 [(20, 'already among the retrieved sources'), (21, 'already among the retrieved sources'), (19, 'over the evidence budget')]
  - ✓ Section 4.3 ABLATION STUDIES (RQ2) | need: ablation results involving GraphRAG | priority: required | status: covered → 候選 3，納入 [22, 23]，排除 [(21, 'already among the retrieved sources')]
  - ✓ Section 4.4 CASE STUDY (RQ3) | need: case study comparison with GraphRAG | priority: required | status: missing → 候選 5，納入 []，排除 [(27, 'already among the retrieved sources'), (24, 'already among the retrieved sources'), (25, 'already selected for another target'), (23, 'already selected for another target'), (26, 'already selected for another target')]
  - ✓ Table 3 (page 9) | need: case study comparison data with GraphRAG | priority: required | status: missing → 候選 3，納入 [25, 26]，排除 [(27, 'already among the retrieved sources')]
  - ✓ Section 5.2 LARGE LANGUAGE MODEL FOR GRAPHS | need: background on GraphRAG | priority: supplementary | status: missing → 候選 2，納入 [30]，排除 [(31, 'supplementary cap reached')]
  - ✓ Section 7.4 CASE STUDY: COMPARISON BETWEEN LIGHT RAG AND THE BASELINE NAIVE RAG | need: additional comparative context | priority: supplementary | status: missing → 候選 2，納入 [45]，排除 [(44, 'supplementary cap reached')]
- 分析狀態：FACTUALLY_INCORRECT；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 涵蓋判定：Section 4.2 COMPARISON OF LIGHT RAG WITH EXISTING RAG METHODS (RQ1)→partial；Section 4.3 ABLATION STUDIES (RQ2)→partial；Section 4.4 CASE STUDY (RQ3)→partial；Table 3 (page 9)→missing；Section 5.2 LARGE LANGUAGE MODEL FOR GRAPHS→missing；Section 7.4 CASE STUDY: COMPARISON BETWEEN LIGHT RAG AND THE BASELINE NAIVE RAG→missing；required 未納入 []；supplementary 用 2；Matrix {'cells': 128, 'tables': ['Table 2 [8]'], 'definitions': ['LightRAG', 'NaiveRAG', '-High']}
- 檢查：標籤不符 ['16.4%', '13.6%', '16.4%', '15.2%', '16.4%', '13.6%', '15.2%']；全稱宣稱 0；引用可疑 []；未解析 3；找不到的數字 []

```text
(1) The question asks for a comparison between LightRAG and GraphRAG, including the datasets and evaluation metrics used. The methods compared are LightRAG and GraphRAG. The datasets involved are Agriculture, CS, Legal, and Mix. The metrics used are Comprehensiveness, Diversity, Empowerment, and Overall.

(2) Evidence matrix and method definitions:
- LightRAG [2]: Dual-level retrieval paradigm combining low-level and high-level retrieval to enhance response diversity and comprehensiveness.
- GraphRAG [1]: Graph-based retrieval mechanism, compared to LightRAG in datasets and metrics.
- Table 3 [6]: Case study comparison between LightRAG and GraphRAG on a machine learning question, with evaluation dimensions of Comprehensiveness, Diversity, Empowerment, and Overall.

(3) Comparison of figures with the same dataset, metric, and pairing:
- Comprehensiveness (Legal dataset): LightRAG has 83.6% win rate versus 16.4% for GraphRAG [8].
- Diversity (Legal dataset): LightRAG has 86.4% win rate versus 13.6% for GraphRAG [8].
- Empowerment (Legal dataset): LightRAG has 83.6% win rate versus 16.4% for GraphRAG [8].
- Overall (Legal dataset): LightRAG has 84.8% win rate versus 15.2% for GraphRAG [8].

(4) Improvements, regressions, and exceptions:
- LightRAG outperforms GraphRAG in all four evaluation dimensions on the Legal dataset, with substantial margins.
- No regression or exception is noted in the comparison.

(5) Verifications:
- "LightRAG outperforms" is supported by the win rates of 83.6%, 86.4%, 83.6%, and 84.8% in Comprehensiveness, Diversity, Empowerment, and Overall, respectively [8].
- "GraphRAG" win rates of 16.4%, 13.6%, 16.4%, and 15.2% are significantly lower than those of LightRAG [8].

(6) Citations:
- The win rates and evaluation dimensions are cited from Table 2 [8].
- Definitions and background are cited from the source descriptions of LightRAG [2] and GraphRAG [1].

(7) Completeness:
- The requested comparison between LightRAG and GraphRAG is addressed with the specific datasets and metrics required.
- The response includes representative figures and a conclusion based on the figures provided, without overgeneralization.

Figures whose labels differ from the source table: 16.4% (answer: Comprehensiveness, Legal, GraphRAG; source: Comprehensiveness, Legal, NaiveRAG, vs LightRAG / Empowerment, Legal, NaiveRAG, vs LightRAG / Empowerment, Legal, NaiveRAG, vs -Low / Comprehensiveness, Legal, NaiveRAG, vs -Origin); 13.6% (answer: Diversity, Legal, GraphRAG; source: Diversity, Legal, NaiveRAG, vs LightRAG / Diversity, Legal, NaiveRAG, vs -Low); 16.4% (answer: Empowerment, Legal, GraphRAG; source: Comprehensiveness, Legal, NaiveRAG, vs LightRAG / Empowerment, Legal, NaiveRAG, vs LightRAG / Empowerment, Legal, NaiveRAG, vs -Low / Comprehensiveness, Legal, NaiveRAG, vs -Origin); 15.2% (answer: Overall, Legal, GraphRAG; source: Overall, Legal, NaiveRAG, vs LightRAG / Comprehensiveness, Legal, RQ-RAG, vs LightRAG / Empowerment, Legal, RQ-RAG, vs LightRAG); 16.4% (answer: GraphRAG; source: Comprehensiveness, Legal, NaiveRAG, vs LightRAG / Empowerment, Legal, NaiveRAG, vs LightRAG / Empowerment, Legal, NaiveRAG, vs -Low / Comprehensiveness, Legal, NaiveRAG, vs -Origin); 13.6% (answer: GraphRAG; source: Diversity, Legal, NaiveRAG, vs LightRAG / Diversity, Legal, NaiveRAG, vs -Low); 15.2% (answer: LightRAG; source: Overall, Legal, NaiveRAG, vs LightRAG / Comprehensiveness, Legal, RQ-RAG, vs LightRAG / Empowerment, Legal, RQ-RAG, vs LightRAG).
```

## B4-Q2-1

- 問題：`compare lightRAG with GraphRAG`；模式 `navigate`；43.5 秒；2 次呼叫；tokens 8511
- 來源：[1] p7 retrieval, [2] p7 retrieval, [3] p9 retrieval, [4] p8 retrieval, [5] p10 retrieval, [6] p7 navigation, [7] p8 navigation, [8] p8 navigation
- 閱讀計畫（定位 6/6，保留 4，超預算 8）：
  - ✓ Section 4.2 COMPARISON OF LIGHT RAG WITH EXISTING RAG METHODS (RQ1) | need: comparison with GraphRAG | priority: required | status: missing → 候選 4，納入 [18]，排除 [(20, 'already among the retrieved sources'), (21, 'already among the retrieved sources'), (19, 'already selected for another target')]
  - ✓ Section 4.3 ABLATION STUDIES (RQ2) | need: performance comparison with GraphRAG | priority: required | status: missing → 候選 3，納入 [23, 22]，排除 [(21, 'already among the retrieved sources')]
  - ✓ Table 1 (page 7) | need: win rate comparison with GraphRAG | priority: required | status: missing → 候選 3，納入 [19]，排除 [(20, 'already among the retrieved sources'), (21, 'already among the retrieved sources')]
  - ✓ Section 4.4 CASE STUDY (RQ3) | need: case study comparison with GraphRAG | priority: supplementary | status: missing → 候選 5，納入 []，排除 [(27, 'already among the retrieved sources'), (24, 'already among the retrieved sources'), (25, 'over the evidence budget'), (23, 'already selected for another target'), (26, 'over the evidence budget')]
  - ✓ Table 3 (page 9) | need: case study comparison with GraphRAG | priority: supplementary | status: missing → 候選 3，納入 []，排除 [(25, 'over the evidence budget'), (26, 'over the evidence budget'), (27, 'already among the retrieved sources')]
  - ✓ Section 3.1 GRAPH-BASED TEXT INDEXING | need: architecture differences | priority: supplementary | status: missing → 候選 5，納入 []，排除 [(9, 'low relevance'), (10, 'over the evidence budget'), (11, 'over the evidence budget'), (8, 'over the evidence budget'), (7, 'over the evidence budget')]
- 分析狀態：FACTUALLY_INCORRECT；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 修正：[]；刪除 []；仍不符 []；方向待定 []
- 涵蓋判定：Section 4.2 COMPARISON OF LIGHT RAG WITH EXISTING RAG METHODS (RQ1)→partial；Section 4.3 ABLATION STUDIES (RQ2)→partial；Table 1 (page 7)→missing；Section 4.4 CASE STUDY (RQ3)→partial；Table 3 (page 9)→missing；Section 3.1 GRAPH-BASED TEXT INDEXING→missing；required 未納入 []；supplementary 用 0；Matrix {'cells': 256, 'tables': ['Table 1 [6]', 'Table 2 [8]'], 'definitions': ['LightRAG', '-High', 'NaiveRAG']}
- 檢查：標籤不符 ['49.6%']；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
The question asks to compare LightRAG with GraphRAG across datasets and metrics.

Evidence from the sources indicates that LightRAG consistently outperforms GraphRAG in larger datasets with complex language contexts, particularly in the Agriculture, CS, and Legal datasets [1]. The comparison is based on four evaluation dimensions: Comprehensiveness, Diversity, Empowerment, and Overall. 

From Table 1 [6], the win rates of LightRAG over GraphRAG are as follows:
- **Agriculture**:
  - Comprehensiveness: LightRAG 54.4% vs. GraphRAG 45.6%
  - Diversity: LightRAG 77.2% vs. GraphRAG 22.8%
  - Empowerment: LightRAG 58.8% vs. GraphRAG 41.2%
  - Overall: LightRAG 54.8% vs. GraphRAG 45.2%
- **CS**:
  - Comprehensiveness: LightRAG 51.6% vs. GraphRAG 48.4%
  - Diversity: LightRAG 59.2% vs. GraphRAG 40.8%
  - Empowerment: LightRAG 54.8% vs. GraphRAG 45.2%
  - Overall: LightRAG 52.0% vs. GraphRAG 48.0%
- **Legal**:
  - Comprehensiveness: LightRAG 51.6% vs. GraphRAG 48.4%
  - Diversity: LightRAG 73.6% vs. GraphRAG 26.4%
  - Empowerment: LightRAG 56.4% vs. GraphRAG 43.6%
  - Overall: LightRAG 52.8% vs. GraphRAG 47.2%
- **Mix**:
  - Comprehensiveness: LightRAG 49.6% vs. GraphRAG 50.4%
  - Diversity: LightRAG 64.0% vs. GraphRAG 36.0%
  - Empowerment: LightRAG 49.2% vs. GraphRAG 50.8%
  - Overall: LightRAG 49.6% vs. GraphRAG 50.4%

Across all datasets and metrics, LightRAG shows consistent improvements over GraphRAG in Comprehensiveness, Diversity, and Empowerment. The only exception is the Mix dataset in the Overall category, where GraphRAG achieves a slightly higher win rate (50.4% vs. 49.6%) [6]. However, in all other categories and datasets, LightRAG demonstrates a clear advantage [1]. The trend underscores the benefits of LightRAG's dual-level retrieval paradigm and graph-based text indexing [2].

Figures whose labels differ from the source table: 49.6% (answer: Overall, Mix, GraphRAG; source: Comprehensiveness, Mix, LightRAG, vs GraphRAG / Overall, Mix, LightRAG, vs GraphRAG).
```

## B4-Q2-2

- 問題：`compare lightRAG with GraphRAG`；模式 `navigate`；46.8 秒；2 次呼叫；tokens 8673
- 來源：[1] p7 retrieval, [2] p7 retrieval, [3] p9 retrieval, [4] p8 retrieval, [5] p10 retrieval, [6] p9 navigation, [7] p9 navigation, [8] p8 navigation, [9] p8 navigation, [10] p6 navigation, [11] p3 navigation
- 閱讀計畫（定位 6/6，保留 7，超預算 6）：
  - ✓ Section 4.2 COMPARISON OF LIGHT RAG WITH EXISTING RAG METHODS (RQ1) | need: comparison with GraphRAG | priority: required | status: covered → 候選 4，納入 [18]，排除 [(20, 'already among the retrieved sources'), (21, 'already among the retrieved sources'), (19, 'over the evidence budget')]
  - ✓ Section 4.3 ABLATION STUDIES (RQ2) | need: ablation results involving GraphRAG | priority: required | status: covered → 候選 3，納入 [22, 23]，排除 [(21, 'already among the retrieved sources')]
  - ✓ Section 4.4 CASE STUDY (RQ3) | need: case study comparison with GraphRAG | priority: required | status: missing → 候選 5，納入 []，排除 [(27, 'already among the retrieved sources'), (24, 'already among the retrieved sources'), (25, 'already selected for another target'), (23, 'already selected for another target'), (26, 'already selected for another target')]
  - ✓ Table 3 (page 9) | need: case study comparison data | priority: required | status: missing → 候選 3，納入 [25, 26]，排除 [(27, 'already among the retrieved sources')]
  - ✓ Section 3.1 GRAPH-BASED TEXT INDEXING | need: graph-based method description | priority: supplementary | status: missing → 候選 5，納入 [9]，排除 [(10, 'over the evidence budget'), (8, 'over the evidence budget'), (11, 'over the evidence budget'), (7, 'over the evidence budget')]
  - ✓ Figure 1 (page 3) | need: architecture comparison context | priority: supplementary | status: missing → 候選 2，納入 [6]，排除 [(7, 'over the evidence budget')]
- 分析狀態：FACTUALLY_INCORRECT；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 修正：[]；刪除 []；仍不符 []；方向待定 []
- 涵蓋判定：Section 4.2 COMPARISON OF LIGHT RAG WITH EXISTING RAG METHODS (RQ1)→partial；Section 4.3 ABLATION STUDIES (RQ2)→partial；Section 4.4 CASE STUDY (RQ3)→partial；Table 3 (page 9)→missing；Section 3.1 GRAPH-BASED TEXT INDEXING→missing；Figure 1 (page 3)→missing；required 未納入 []；supplementary 用 2；Matrix {'cells': 128, 'tables': ['Table 2 [8]'], 'definitions': ['LightRAG', 'NaiveRAG', '-High']}
- 檢查：標籤不符 []；全稱宣稱 3；引用可疑 [([2], [9])]；未解析 0；找不到的數字 []

```text
LightRAG is compared with GraphRAG across multiple datasets and evaluation dimensions, including Comprehensiveness, Diversity, Empowerment, and Overall. The datasets used in the comparisons include Agriculture, CS, Legal, and Mix. These metrics are evaluated in the case study presented in Table 3 [6], and the ablation studies in Table 2 [8] also indirectly support these comparisons by highlighting the performance of variants of LightRAG against baselines such as NaiveRAG, which serves as a reference point.

From Table 3 [6], LightRAG consistently outperforms GraphRAG in all four evaluation dimensions: Comprehensiveness, Diversity, Empowerment, and Overall. For example, in the Comprehensiveness category, LightRAG is rated as the winner over GraphRAG, with the explanation that it provides a broader array of metrics and a fuller view of the evaluation context. In Diversity, LightRAG again wins, attributed to its nuanced explanations and inclusion of a wider variety of metrics. Empowerment also favors LightRAG, with its ability to detail how each metric functions and its importance in evaluating systems. Finally, the Overall winner is LightRAG, as it excels in comprehensiveness, diversity, and empowerment, making it more informative for readers [6].

Table 2 [8] supports the superiority of LightRAG by showing the performance of ablated versions of LightRAG (e.g., -High, -Low, -Origin) compared to NaiveRAG. While these ablated versions of LightRAG show varying degrees of performance, they consistently outperform NaiveRAG, which serves as a baseline. The full version of LightRAG, combining low-level and high-level retrieval, performs the best. This dual-level retrieval paradigm is described in Section 4.3 [2], where it is stated that the integration of low-level retrieval of specific entities with high-level retrieval of broader topics enhances response diversity and enables LightRAG to handle complex queries effectively. 

Section 4.2 [10] discusses the comparison of LightRAG with existing RAG methods, including GraphRAG, and highlights the performance gap between graph-based RAG systems and chunk-based methods such as NaiveRAG, HyDE, and RQRAG. This performance gap is most pronounced in the largest dataset (Legal), where baseline methods achieve only about 20% win rates compared to LightRAG. This underscores the advantages of graph-based retrieval mechanisms, with LightRAG demonstrating a clear advantage over GraphRAG in larger datasets with complex language contexts [2].

There are no exceptions or conflicting results in the provided sources that contradict the consistent superiority of LightRAG over GraphRAG. The ablation studies in Table 2 [8] further confirm the robustness of LightRAG's design, as the full version of LightRAG consistently outperforms its ablated versions, which either remove high-level retrieval (-High), low-level retrieval (-Low), or use the original text (-Origin) [9]. 

The conclusion is that LightRAG consistently outperforms GraphRAG across all evaluation dimensions and datasets, demonstrating the effectiveness of its dual-level retrieval paradigm and graph-based text indexing. The evidence from Table 3 [6] and Table 2 [8], along with the explanations provided in Sections 4.2 [10] and 4.3 [2], supports this conclusion without any conflicting data.

A claim the source table does not bear out: "From Table 3, LightRAG consistently outperforms GraphRAG in all four evaluation dimensions: Comprehensiveness, Diversity, Empowerment, and Overall." — LightRAG is above the compared methods in 61 cells and below in 3, for example Comprehensiveness / Mix: LightRAG 49.6% vs GraphRAG 50.4% (p. 7); Empowerment / Mix: LightRAG 49.2% vs GraphRAG 50.8% (p. 7); Overall / Mix: LightRAG 49.6% vs GraphRAG 50.4% (p. 7) / "The ablation studies in Table 2 further confirm the robustness of LightRAG's design, as the full version of LightRAG consistently outperforms its ablated versions, which either remove high-level retrieval (-High), low-level retrieval (-Low), or use the original text (-Origin)." — LightRAG is above the compared methods in 37 cells and below in 8, for example Comprehensiveness / Agriculture: LightRAG 67.6% vs -Origin 75.2% (p. 8); Comprehensiveness / Mix: LightRAG 61.2% vs -Low 64.0% (p. 8); Diversity / CS: LightRAG 62.0% vs -High 63.2% (p. 8) / "The conclusion is that LightRAG consistently outperforms GraphRAG across all evaluation dimensions and datasets, demonstrating the effectiveness of its dual-level retrieval paradigm and graph-based text indexing." — LightRAG is above the compared methods in 61 cells and below in 3, for example Comprehensiveness / Mix: LightRAG 49.6% vs GraphRAG 50.4% (p. 7); Empowerment / Mix: LightRAG 49.2% vs GraphRAG 50.8% (p. 7); Overall / Mix: LightRAG 49.6% vs GraphRAG 50.4% (p. 7).
```

## B4-Q2-3

- 問題：`compare lightRAG with GraphRAG`；模式 `navigate`；37.5 秒；2 次呼叫；tokens 8442
- 來源：[1] p7 retrieval, [2] p7 retrieval, [3] p9 retrieval, [4] p8 retrieval, [5] p10 retrieval, [6] p9 navigation, [7] p9 navigation, [8] p8 navigation, [9] p7 navigation, [10] p6 navigation, [11] p10 navigation
- 閱讀計畫（定位 6/6，保留 7，超預算 3）：
  - ✓ Section 4.2 COMPARISON OF LIGHT RAG WITH EXISTING RAG METHODS (RQ1) | need: comparison details with GraphRAG | priority: required | status: covered → 候選 4，納入 [19, 18]，排除 [(20, 'already among the retrieved sources'), (21, 'already among the retrieved sources')]
  - ✓ Section 4.3 ABLATION STUDIES (RQ2) | need: performance differences with GraphRAG | priority: required | status: covered → 候選 3，納入 [23]，排除 [(21, 'already among the retrieved sources'), (22, 'over the evidence budget')]
  - ✓ Section 4.4 CASE STUDY (RQ3) | need: case-based comparison with GraphRAG | priority: required | status: missing → 候選 5，納入 []，排除 [(27, 'already among the retrieved sources'), (24, 'already among the retrieved sources'), (23, 'already selected for another target'), (25, 'already selected for another target'), (26, 'already selected for another target')]
  - ✓ Table 3 (page 9) | need: case study comparison data with GraphRAG | priority: required | status: missing → 候選 3，納入 [25, 26]，排除 [(27, 'already among the retrieved sources')]
  - ✓ Section 7.4 CASE STUDY: COMPARISON BETWEEN LIGHT RAG AND THE BASELINE NAIVE RAG | need: additional comparative insights | priority: supplementary | status: missing → 候選 2，納入 [45]，排除 [(44, 'over the evidence budget')]
  - ✓ Section 5.2 LARGE LANGUAGE MODEL FOR GRAPHS | need: contextual background on GraphRAG | priority: supplementary | status: missing → 候選 2，納入 [30]，排除 [(31, 'over the evidence budget')]
- 分析狀態：FACTUALLY_INCORRECT；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 修正：[('figure', '86.4%', '73.6%')]；刪除 []；仍不符 []；方向待定 []
- 涵蓋判定：Section 4.2 COMPARISON OF LIGHT RAG WITH EXISTING RAG METHODS (RQ1)→partial；Section 4.3 ABLATION STUDIES (RQ2)→partial；Section 4.4 CASE STUDY (RQ3)→partial；Table 3 (page 9)→missing；Section 7.4 CASE STUDY: COMPARISON BETWEEN LIGHT RAG AND THE BASELINE NAIVE RAG→missing；Section 5.2 LARGE LANGUAGE MODEL FOR GRAPHS→missing；required 未納入 []；supplementary 用 2；Matrix {'cells': 128, 'tables': ['Table 1 [9]'], 'definitions': ['LightRAG']}
- 檢查：標籤不符 []；全稱宣稱 3；引用可疑 [([7], [4, 10])]；未解析 0；找不到的數字 []

```text
The question asks to compare LightRAG with GraphRAG in terms of performance, datasets, and metrics. LightRAG and GraphRAG are graph-based RAG systems evaluated on four datasets: Agriculture, CS, Legal, and Mix. The evaluation dimensions are Comprehensiveness, Diversity, Empowerment, and Overall. The win rate metric is used to quantify the performance of each method.

LightRAG consistently outperforms GraphRAG in all datasets and evaluation dimensions. For example, in the Legal dataset, LightRAG achieves a 51.6% win rate over GraphRAG in Comprehensiveness, and an 73.6% win rate in Diversity. In the Agriculture dataset, LightRAG wins 54.4% in Comprehensiveness and 77.2% in Diversity. These results indicate that LightRAG provides more comprehensive and diverse responses compared to GraphRAG. 

In the CS dataset, LightRAG achieves a 51.6% win rate in Comprehensiveness and 59.2% in Diversity. In the Mix dataset, LightRAG wins 49.6% in Comprehensiveness and 64.0% in Diversity. These consistent improvements across all datasets and evaluation dimensions highlight LightRAG's superior performance. 

The case study in Table 3 further supports these findings. LightRAG outperforms GraphRAG in all evaluation dimensions assessed by the LLM judge, including comprehensiveness, diversity, empowerment, and overall quality. LightRAG provides a broader array of metrics and more nuanced explanations, enhancing user understanding and engagement [7].

An ablation study in Section 4.3 shows that the dual-level retrieval paradigm in LightRAG contributes to its superior performance. The hybrid mode, combining low-level and high-level retrieval, ensures both breadth and depth in information retrieval. This dual-level approach enables LightRAG to effectively handle complex queries and provide comprehensive responses [2].

The results indicate that LightRAG consistently outperforms GraphRAG in all evaluation dimensions across all datasets. The improvements in comprehensiveness, diversity, and empowerment highlight LightRAG's strengths in capturing complex semantic dependencies and providing contextually relevant answers [1][2][4][6][7][9].

A claim the source table does not bear out: "LightRAG consistently outperforms GraphRAG in all datasets and evaluation dimensions." — LightRAG is above the compared methods in 61 cells and below in 3, for example Comprehensiveness / Mix: LightRAG 49.6% vs GraphRAG 50.4% (p. 7); Empowerment / Mix: LightRAG 49.2% vs GraphRAG 50.8% (p. 7); Overall / Mix: LightRAG 49.6% vs GraphRAG 50.4% (p. 7) / "These consistent improvements across all datasets and evaluation dimensions highlight LightRAG's superior performance." — LightRAG is above the compared methods in 306 cells and below in 11, for example Comprehensiveness / Mix: LightRAG 49.6% vs GraphRAG 50.4% (p. 7); Comprehensiveness / Agriculture: LightRAG 67.6% vs -Origin 75.2% (p. 8); Empowerment / Mix: LightRAG 49.2% vs GraphRAG 50.8% (p. 7) / "The results indicate that LightRAG consistently outperforms GraphRAG in all evaluation dimensions across all datasets." — LightRAG is above the compared methods in 61 cells and below in 3, for example Comprehensiveness / Mix: LightRAG 49.6% vs GraphRAG 50.4% (p. 7); Empowerment / Mix: LightRAG 49.2% vs GraphRAG 50.8% (p. 7); Overall / Mix: LightRAG 49.6% vs GraphRAG 50.4% (p. 7).
```

## B4b-Q2-1

- 問題：`compare lightRAG with GraphRAG`；模式 `navigate`；37.2 秒；2 次呼叫；tokens 8456
- 來源：[1] p7 retrieval, [2] p7 retrieval, [3] p9 retrieval, [4] p8 retrieval, [5] p10 retrieval, [6] p9 navigation, [7] p9 navigation, [8] p8 navigation, [9] p8 navigation, [10] p6 navigation, [11] p16 navigation
- 閱讀計畫（定位 6/6，保留 7，超預算 1）：
  - ✓ Section 4.2 COMPARISON OF LIGHT RAG WITH EXISTING RAG METHODS (RQ1) | need: comparison with GraphRAG | priority: required | status: covered → 候選 4，納入 [18]，排除 [(20, 'already among the retrieved sources'), (21, 'already among the retrieved sources'), (19, 'over the evidence budget')]
  - ✓ Section 4.3 ABLATION STUDIES (RQ2) | need: ablation results involving GraphRAG | priority: required | status: covered → 候選 3，納入 [22, 23]，排除 [(21, 'already among the retrieved sources')]
  - ✓ Section 4.4 CASE STUDY (RQ3) | need: case study comparing LightRAG and GraphRAG | priority: required | status: missing → 候選 5，納入 []，排除 [(27, 'already among the retrieved sources'), (24, 'already among the retrieved sources'), (25, 'already selected for another target'), (23, 'already selected for another target'), (26, 'already selected for another target')]
  - ✓ Table 3 | need: case study comparison data | priority: required | status: missing → 候選 3，納入 [25, 26]，排除 [(27, 'already among the retrieved sources')]
  - ✓ Section 7.4 CASE STUDY: COMPARISON BETWEEN LIGHT RAG AND THE BASELINE NAIVE RAG | need: additional comparative context | priority: supplementary | status: missing → 候選 2，納入 [45]，排除 [(44, 'supplementary cap reached')]
  - ✓ Table 5 | need: detailed case study comparison | priority: supplementary | status: missing → 候選 2，納入 [43]，排除 [(44, 'supplementary cap reached')]
- 分析狀態：UNCERTAIN；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 修正：[]；刪除 []；仍不符 []；方向待定 []
- 涵蓋判定：Section 4.2 COMPARISON OF LIGHT RAG WITH EXISTING RAG METHODS (RQ1)→partial；Section 4.3 ABLATION STUDIES (RQ2)→partial；Section 4.4 CASE STUDY (RQ3)→partial；Table 3→missing；Section 7.4 CASE STUDY: COMPARISON BETWEEN LIGHT RAG AND THE BASELINE NAIVE RAG→missing；Table 5→missing；required 未納入 []；supplementary 用 2；Matrix {'cells': 128, 'tables': ['Table 2 [8]'], 'definitions': ['LightRAG', 'NaiveRAG', '-High']}
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
LightRAG and GraphRAG are both graph-based retrieval-augmented generation (RAG) systems, but LightRAG consistently outperforms GraphRAG in several key evaluation dimensions, particularly in larger datasets with complex language contexts [1]. The comparison involves three main datasets: Agriculture, CS, and Legal, and the evaluation metrics include comprehensiveness, diversity, empowerment, and overall quality [10].

In a case study comparing the two systems, LightRAG outperformed GraphRAG in all evaluation dimensions assessed by the LLM judge. For instance, in the case study on machine learning normalization methods, LightRAG provided a broader range of metrics and more nuanced explanations, including additional metrics such as Mean Average Precision at K (MAPK), Area Under the Curve (AUC), and user engagement metrics, which were not as thoroughly covered by GraphRAG [6]. LightRAG’s response was deemed more comprehensive, diverse, and empowering, as it provided context on trade-offs between metrics and emphasized user engagement [7].

The ablation studies further support these findings. While the source does not directly compare LightRAG and GraphRAG in Table 2, the table highlights the performance of LightRAG and its variants (such as -High and -Low) against NaiveRAG. These results indirectly support the superiority of LightRAG's dual-level retrieval paradigm over systems that rely on a single retrieval level, which is a core design principle of GraphRAG [2].

LightRAG's performance advantage is attributed to its dual-level retrieval paradigm, which combines low-level retrieval of specific entities with high-level retrieval of broader topics, effectively leveraging graph-based text indexing to capture the full context in response to queries [1]. In contrast, GraphRAG, while also graph-based, does not incorporate the same level of detail in its retrieval process, leading to less comprehensive and diverse responses [1].

An exception to this trend is the -Low variant of LightRAG, which prioritizes high-level retrieval and offers a broader range of content but struggles with tasks requiring precise, detailed answers [9]. However, this variant is not directly compared to GraphRAG in the sources provided.

Overall, LightRAG demonstrates a clear advantage over GraphRAG in terms of performance across larger datasets and complex queries, particularly in comprehensiveness, diversity, and empowerment [1].
```

## B4b-Q2-2

- 問題：`compare lightRAG with GraphRAG`；模式 `navigate`；29.0 秒；2 次呼叫；tokens 8263
- 來源：[1] p7 retrieval, [2] p7 retrieval, [3] p9 retrieval, [4] p8 retrieval, [5] p10 retrieval, [6] p9 navigation, [7] p9 navigation, [8] p8 navigation, [9] p8 navigation, [10] p6 navigation, [11] p3 navigation
- 閱讀計畫（定位 6/6，保留 7，超預算 6）：
  - ✓ Section 4.2 COMPARISON OF LIGHT RAG WITH EXISTING RAG METHODS (RQ1) | need: comparison with GraphRAG | priority: required | status: covered → 候選 4，納入 [18]，排除 [(20, 'already among the retrieved sources'), (21, 'already among the retrieved sources'), (19, 'over the evidence budget')]
  - ✓ Section 4.3 ABLATION STUDIES (RQ2) | need: ablation results involving GraphRAG | priority: required | status: covered → 候選 3，納入 [22, 23]，排除 [(21, 'already among the retrieved sources')]
  - ✓ Section 4.4 CASE STUDY (RQ3) | need: case study comparison with GraphRAG | priority: required | status: missing → 候選 5，納入 []，排除 [(27, 'already among the retrieved sources'), (24, 'already among the retrieved sources'), (25, 'already selected for another target'), (23, 'already selected for another target'), (26, 'already selected for another target')]
  - ✓ Table 3 (page 9) | need: case study comparison data with GraphRAG | priority: required | status: missing → 候選 3，納入 [25, 26]，排除 [(27, 'already among the retrieved sources')]
  - ✓ Section 3.1 GRAPH-BASED TEXT INDEXING | need: graph-based indexing details | priority: supplementary | status: missing → 候選 5，納入 [9]，排除 [(10, 'over the evidence budget'), (8, 'over the evidence budget'), (11, 'over the evidence budget'), (7, 'over the evidence budget')]
  - ✓ Figure 1 (page 3) | need: architecture overview for comparison context | priority: supplementary | status: missing → 候選 2，納入 [6]，排除 [(7, 'over the evidence budget')]
- 分析狀態：FACTUALLY_INCORRECT；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 修正：[]；刪除 []；仍不符 []；方向待定 []
- 涵蓋判定：Section 4.2 COMPARISON OF LIGHT RAG WITH EXISTING RAG METHODS (RQ1)→partial；Section 4.3 ABLATION STUDIES (RQ2)→partial；Section 4.4 CASE STUDY (RQ3)→partial；Table 3 (page 9)→missing；Section 3.1 GRAPH-BASED TEXT INDEXING→missing；Figure 1 (page 3)→missing；required 未納入 []；supplementary 用 2；Matrix {'cells': 128, 'tables': ['Table 2 [8]'], 'definitions': ['LightRAG', 'NaiveRAG', '-High']}
- 檢查：標籤不符 []；全稱宣稱 2；引用可疑 []；未解析 0；找不到的數字 []

```text
The question asks for a comparison of LightRAG with GraphRAG across datasets and metrics. Evidence is drawn from ablation studies, case studies, and comparisons in the datasets Agriculture, CS, Legal, and Mix, focusing on metrics such as Comprehensiveness, Diversity, Empowerment, and Overall performance.

LightRAG consistently outperforms GraphRAG in the datasets Agriculture, CS, Legal, and Mix. In the Legal dataset, the disparity in performance is particularly notable, with baseline methods achieving only about 20% win rates compared to LightRAG [1]. This trend is supported by ablation studies, where LightRAG demonstrates a significant advantage in response diversity and comprehensiveness [2]. In the case study presented in Table 3, LightRAG outperforms GraphRAG in all evaluation dimensions assessed by the LLM judge, including comprehensiveness, diversity, empowerment, and overall quality [4]. For example, in the evaluation of comprehensiveness, LightRAG provides a broader array of metrics, including MAPK, AUC, and user engagement metrics, compared to GraphRAG, which focuses primarily on traditional metrics [7].

There are no exceptions noted in the datasets or metrics evaluated, and all comparisons align with the figures provided. The conclusion is that LightRAG outperforms GraphRAG across all datasets and metrics evaluated. [1][2][4][7]

A claim the source table does not bear out: "LightRAG consistently outperforms GraphRAG in the datasets Agriculture, CS, Legal, and Mix." — LightRAG is above the compared methods in 61 cells and below in 3, for example Comprehensiveness / Mix: LightRAG 49.6% vs GraphRAG 50.4% (p. 7); Empowerment / Mix: LightRAG 49.2% vs GraphRAG 50.8% (p. 7); Overall / Mix: LightRAG 49.6% vs GraphRAG 50.4% (p. 7) / "The conclusion is that LightRAG outperforms GraphRAG across all datasets and metrics evaluated." — LightRAG is above the compared methods in 61 cells and below in 3, for example Comprehensiveness / Mix: LightRAG 49.6% vs GraphRAG 50.4% (p. 7); Empowerment / Mix: LightRAG 49.2% vs GraphRAG 50.8% (p. 7); Overall / Mix: LightRAG 49.6% vs GraphRAG 50.4% (p. 7).
```

## B4b-Q2-3

- 問題：`compare lightRAG with GraphRAG`；模式 `navigate`；41.0 秒；2 次呼叫；tokens 8444
- 來源：[1] p7 retrieval, [2] p7 retrieval, [3] p9 retrieval, [4] p8 retrieval, [5] p10 retrieval, [6] p7 navigation, [7] p8 navigation, [8] p8 navigation
- 閱讀計畫（定位 6/6，保留 4，超預算 5）：
  - ✓ Section 4.2 COMPARISON OF LIGHT RAG WITH EXISTING RAG METHODS (RQ1) | need: comparison with GraphRAG | priority: required | status: missing → 候選 4，納入 [18]，排除 [(20, 'already among the retrieved sources'), (21, 'already among the retrieved sources'), (19, 'already selected for another target')]
  - ✓ Section 4.3 ABLATION STUDIES (RQ2) | need: ablation results for GraphRAG | priority: required | status: missing → 候選 3，納入 [22]，排除 [(21, 'already among the retrieved sources'), (23, 'already selected for another target')]
  - ✓ Section 4.4 CASE STUDY (RQ3) | need: case study comparison | priority: required | status: missing → 候選 5，納入 [23]，排除 [(27, 'already among the retrieved sources'), (24, 'already among the retrieved sources'), (25, 'over the evidence budget'), (26, 'over the evidence budget')]
  - ✓ Table 1 (page 7) | need: win rates comparison data | priority: required | status: missing → 候選 3，納入 [19]，排除 [(20, 'already among the retrieved sources'), (21, 'already among the retrieved sources')]
  - ✓ Table 3 (page 9) | need: case study comparison details | priority: supplementary | status: missing → 候選 3，納入 []，排除 [(25, 'over the evidence budget'), (26, 'over the evidence budget'), (27, 'already among the retrieved sources')]
  - ✓ Section 4.5 MODEL COST AND ADAPTABILITY ANALYSIS (RQ4) | need: cost comparison context | priority: supplementary | status: missing → 候選 3，納入 []，排除 [(27, 'already among the retrieved sources'), (28, 'over the evidence budget'), (29, 'already among the retrieved sources')]
- 分析狀態：UNCERTAIN；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 修正：[]；刪除 []；仍不符 []；方向待定 []
- 涵蓋判定：Section 4.2 COMPARISON OF LIGHT RAG WITH EXISTING RAG METHODS (RQ1)→partial；Section 4.3 ABLATION STUDIES (RQ2)→partial；Section 4.4 CASE STUDY (RQ3)→partial；Table 1 (page 7)→missing；Table 3 (page 9)→missing；Section 4.5 MODEL COST AND ADAPTABILITY ANALYSIS (RQ4)→partial；required 未納入 []；supplementary 用 0；Matrix {'cells': 256, 'tables': ['Table 1 [6]', 'Table 2 [7]'], 'definitions': ['LightRAG', 'NaiveRAG', '-High']}
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 [([3], [5]), ([3], [5])]；未解析 31；找不到的數字 []

```text
LightRAG is compared with GraphRAG in terms of performance across four datasets (Agriculture, CS, Legal, and Mix) and four evaluation dimensions (Comprehensiveness, Diversity, Empowerment, and Overall). The results are derived from win rates in Table 1 [6].

In the Agriculture dataset, LightRAG outperforms GraphRAG in Comprehensiveness (54.4% vs. 45.6%), Diversity (77.2% vs. 22.8%), Empowerment (58.8% vs. 41.2%), and Overall (54.8% vs. 45.2%). In the CS dataset, LightRAG also outperforms GraphRAG in Comprehensiveness (51.6% vs. 48.4%), Diversity (59.2% vs. 40.8%), Empowerment (54.8% vs. 45.2%), and Overall (52.0% vs. 48.0%). In the Legal dataset, LightRAG outperforms GraphRAG in Comprehensiveness (51.6% vs. 48.4%), Diversity (73.6% vs. 26.4%), Empowerment (56.4% vs. 43.6%), and Overall (52.8% vs. 47.2%). In the Mix dataset, LightRAG outperforms GraphRAG in Comprehensiveness (49.6% vs. 50.4%), Diversity (64.0% vs. 36.0%), Empowerment (49.2% vs. 50.8%), and Overall (49.6% vs. 50.4%).

The case study in Section 4.4 [4] further supports these findings, showing that LightRAG outperforms GraphRAG in comprehensiveness, diversity, and empowerment in a specific example involving a machine learning question. The document attributes this superior performance to LightRAG's dual-level retrieval paradigm, which combines low-level retrieval of specific entities with high-level retrieval of broader topics, providing a more comprehensive and diverse set of responses [1].

Regarding model cost and adaptability, Section 4.5 [3] indicates that LightRAG is more efficient in incremental data updates compared to GraphRAG. LightRAG integrates new entities and relationships into the existing graph without full reconstruction, resulting in significantly lower overhead and token costs compared to GraphRAG, which must dismantle its community structure and regenerate it for new data. This efficiency underscores LightRAG's superior adaptability and cost-effectiveness in dynamic environments [3].
```

## C-Q2-1

- 問題：`compare lightRAG with GraphRAG`；模式 `single`；14.0 秒；1 次呼叫；tokens 2462
- 來源：[1] p7 retrieval, [2] p7 retrieval, [3] p9 retrieval, [4] p8 retrieval, [5] p10 retrieval
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 [([3], [5])]；未解析 0；找不到的數字 []

```text
LightRAG consistently outperforms GraphRAG, particularly in larger datasets with complex language contexts. In the Agriculture, CS, and Legal datasets—each containing millions of tokens—LightRAG shows a clear advantage, significantly surpassing GraphRAG and highlighting its strength in comprehensive information understanding within diverse environments [2]. This superiority is attributed to LightRAG's dual-level retrieval paradigm, which integrates low-level retrieval of specific entities with high-level retrieval of broader topics, thereby enhancing response diversity and comprehensiveness [1]. 

In terms of cost and adaptability, LightRAG is more efficient during incremental data updates. While GraphRAG must dismantle and regenerate its community structure when new data is introduced, incurring a high token cost, LightRAG seamlessly integrates new entities and relationships into the existing graph without full reconstruction, resulting in significantly lower overhead [3]. 

However, in some cases, the variant of LightRAG that omits one module (either low-level or high-level retrieval) even shows improvements in certain datasets, such as Agriculture and Mix. This suggests that while the dual-level retrieval paradigm is generally beneficial, there may be exceptions where a simplified approach can be effective [4]. 

In conclusion, LightRAG generally outperforms GraphRAG in both performance and efficiency, particularly in large-scale and complex datasets, although there are specific cases where a simplified variant may perform well.
```

## C-Q2-2

- 問題：`compare lightRAG with GraphRAG`；模式 `single`；13.4 秒；1 次呼叫；tokens 2498
- 來源：[1] p7 retrieval, [2] p7 retrieval, [3] p9 retrieval, [4] p8 retrieval, [5] p10 retrieval
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 [([3], [5]), ([3], [5])]；未解析 0；找不到的數字 []

```text
LightRAG consistently outperforms GraphRAG, particularly in larger datasets with complex language contexts. In the Agriculture, CS, and Legal datasets—each containing millions of tokens—LightRAG shows a clear advantage, significantly surpassing GraphRAG and highlighting its strength in comprehensive information understanding within diverse environments [2].

LightRAG’s dual-level retrieval paradigm, which integrates low-level retrieval of specific entities with high-level retrieval of broader topics, enhances response diversity. This approach effectively addresses both detailed and abstract queries, ensuring a thorough grasp of information [2]. In a case study, LightRAG outperformed GraphRAG in all evaluation dimensions assessed by the LLM judge, including comprehensiveness, diversity, empowerment, and overall quality [4].

In terms of cost and adaptability, LightRAG is more efficient and cost-effective. During the incremental data update phase, LightRAG seamlessly integrates newly extracted entities and relationships into the existing graph without the need for full reconstruction. In contrast, GraphRAG must dismantle its existing community structure to incorporate new entities and relationships, followed by complete regeneration. This process incurs a substantial token cost of approximately 5,000 tokens per community report. Given 1,399 communities, GraphRAG would require around 1,399 × 2 × 5,000 tokens to reconstruct both the original and new community reports [3].

Overall, LightRAG demonstrates superior performance in terms of response diversity, comprehensive information understanding, and cost-effectiveness during incremental updates compared to GraphRAG.
```

## C-Q2-3

- 問題：`compare lightRAG with GraphRAG`；模式 `single`；13.6 秒；1 次呼叫；tokens 2501
- 來源：[1] p7 retrieval, [2] p7 retrieval, [3] p9 retrieval, [4] p8 retrieval, [5] p10 retrieval
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 [([3], [5]), ([3], [5])]；未解析 0；找不到的數字 []

```text
LightRAG consistently outperforms GraphRAG, particularly in larger datasets with complex language contexts. In the Agriculture, CS, and Legal datasets—each containing millions of tokens—LightRAG shows a clear advantage, significantly surpassing GraphRAG and highlighting its strength in comprehensive information understanding within diverse environments [2]. 

LightRAG's superiority is supported by its dual-level retrieval paradigm, which integrates low-level retrieval of specific entities with high-level retrieval of broader topics. This approach enhances response diversity and ensures a thorough grasp of information [2]. For example, in a case study involving a machine learning question, LightRAG outperforms GraphRAG in all evaluation dimensions assessed by the LLM judge, including comprehensiveness, diversity, empowerment, and overall quality [4].

In terms of cost and adaptability, LightRAG demonstrates superior efficiency during incremental data updates. Unlike GraphRAG, which must dismantle its existing community structure to incorporate new entities and relationships, LightRAG seamlessly integrates newly extracted entities into the existing graph without full reconstruction. This results in significantly lower overhead and token costs. Specifically, in the incremental data update phase on the Legal dataset, GraphRAG requires around 1,399 × 2 × 5,000 tokens to reconstruct community reports, while LightRAG achieves the same with much lower overhead [3].

Despite these advantages, there are no explicit results in the provided sources that contradict LightRAG's superiority over GraphRAG. However, the conclusion is drawn based on the evidence presented and does not claim universal consistency without verification.
```

## A-Q3-1

- 問題：`Performance of ablated versions of LightRAG`；模式 `roles`；25.9 秒；1 次呼叫；tokens 4691
- 來源：[1] p8 retrieval, [2] p7 retrieval, [3] p1 retrieval, [4] p8 retrieval, [5] p1 retrieval, [6] p8 table_context
- 檢查：標籤不符 ['80.8%']；全稱宣稱 0；引用可疑 []；未解析 3；找不到的數字 ['10']

```text
Navigator: The sections and tables that bear on the question include the "EVALUATION" section (pages 5-10) and Table 2 (page 8), which presents the performance of ablated versions of LightRAG using NaiveRAG as a reference.

Analyst: The ablated versions of LightRAG were evaluated against the full version, with NaiveRAG as a baseline. The ablated variants include -High (removing high-level retrieval), -Low (removing low-level retrieval), and -Origin (removing the use of original text in retrieval). 

- The -High variant, which removes high-level retrieval, shows a significant performance decline across most datasets and metrics. For example, in the Agriculture dataset, its comprehensiveness drops from 67.6% (LightRAG) to 65.2% (-High). This decline is attributed to an overemphasis on specific entities and their immediate neighbors, limiting the ability to address complex queries requiring broader insights [1].

- The -Low variant, which removes low-level retrieval, achieves high comprehensiveness scores (e.g., 80.8% in Agriculture) but struggles with providing detailed insights. For instance, in the Legal dataset, its comprehensiveness is 80.8% (-Low) versus 83.6% (LightRAG). However, this variant lacks depth in examining specific entities, which can limit its effectiveness for tasks requiring precise answers [1].

- The -Origin variant, which excludes the use of original text in retrieval, does not show significant performance declines and, in some cases, even improves. For example, in the Agriculture dataset, its overall score improves from 67.6% (LightRAG) to 74.4% (-Origin). This is attributed to the effective extraction of key information during graph-based indexing, which reduces noise from irrelevant text [1].

- The full version of LightRAG (hybrid mode) combines low-level and high-level retrieval methods, achieving balanced performance across all dimensions. For example, in the Agriculture dataset, it achieves 67.6% comprehensiveness, 76.4% diversity, and 67.6% empowerment, outperforming the ablated versions in most cases [1].

In conclusion, the hybrid mode of LightRAG offers the best balance between breadth and depth in retrieval, outperforming the ablated versions in most scenarios. However, some ablated variants, such as -Origin, perform comparably well in specific cases [1].

Numbers that could not be checked against the cited pages of the original text: 10.

Figures whose labels differ from the source table: 80.8% (answer: Comprehensiveness, Agriculture, -Low; source: Comprehensiveness, Legal, -Low, vs NaiveRAG).
```

## A-Q3-2

- 問題：`Performance of ablated versions of LightRAG`；模式 `roles`；20.8 秒；1 次呼叫；tokens 4649
- 來源：[1] p8 retrieval, [2] p7 retrieval, [3] p1 retrieval, [4] p8 retrieval, [5] p1 retrieval, [6] p8 table_context
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
Navigator:  
The question concerns the performance of ablated versions of LightRAG. The relevant content is in Section 4.3 "Ablation Studies (RQ2)" on page 8, particularly Table 2, which provides the performance metrics of the ablated models compared to the full LightRAG.  

Analyst:  
The ablation studies evaluate the performance of LightRAG variants that omit either low-level or high-level retrieval modules. The -High variant, which removes high-level retrieval, shows a significant performance decline across most datasets and metrics [1]. This is attributed to its focus on specific entities and their immediate neighbors, which limits its ability to handle complex queries requiring broader insights [6]. The -Low variant, which removes low-level retrieval, prioritizes broader content by leveraging entity-wise relationships but struggles with providing detailed insights, leading to reduced depth in specific entity analysis [6].  

The hybrid mode of LightRAG, combining both low-level and high-level retrieval, achieves balanced performance by ensuring breadth and depth in the retrieval process [6]. The -Origin variant, which eliminates the original text in retrieval, does not exhibit significant performance declines and even shows improvements in some cases, such as in the Agriculture and Mix datasets. This is attributed to the effective extraction of key information during graph-based indexing and the removal of irrelevant text noise [6].  

Representative results from Table 2 show that in the Agriculture dataset, the -High variant achieves 65.2% comprehensiveness compared to NaiveRAG's 34.8%, while the -Low variant achieves 64.0% comprehensiveness compared to NaiveRAG's 36.0%. The -Origin variant achieves 75.2% comprehensiveness in Agriculture compared to NaiveRAG's 24.8% [1].  

In contrast, the -High variant shows a decline in the Legal dataset, achieving 76.4% comprehensiveness compared to NaiveRAG's 23.6% [1]. These results indicate that while the hybrid mode performs best overall, the ablated versions have specific strengths and weaknesses depending on the dataset and evaluation metric.  

In conclusion, the full LightRAG hybrid mode achieves the most balanced performance, combining the strengths of both low-level and high-level retrieval while mitigating their individual limitations [6].
```

## A-Q3-3

- 問題：`Performance of ablated versions of LightRAG`；模式 `roles`；9.8 秒；1 次呼叫；tokens 4385
- 來源：[1] p8 retrieval, [2] p7 retrieval, [3] p1 retrieval, [4] p8 retrieval, [5] p1 retrieval, [6] p8 table_context
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 ['10']

```text
Navigator: The sections and tables that bear on the question are: Section: EVALUATION (pages 5-10), Table 2 (page 8): Performance of ablated versions of LightRAG, using NaiveRAG as reference.

Analyst: The ablated versions of LightRAG include variants that omit either the high-level or low-level retrieval modules. The -High variant, which removes high-order retrieval, experiences a significant performance decline across nearly all datasets and metrics due to its focus on specific information and entities [1]. The -Low variant, which prioritizes high-level retrieval, offers advantages in comprehensiveness by capturing a broader range of content but sacrifices depth in examining specific entities [1]. The hybrid mode, combining both low-level and high-level retrieval, achieves balanced performance across multiple dimensions by retrieving a broader set of relationships while conducting an in-depth exploration of specific entities [1]. The -Origin variant, which eliminates the use of original text in retrieval, does not show significant performance declines and even shows improvements in some cases, such as in Agriculture and Mix [1].

Numbers that could not be checked against the cited pages of the original text: 10.
```

## B-Q3-1

- 問題：`Performance of ablated versions of LightRAG`；模式 `navigate`；19.1 秒；2 次呼叫；tokens 4896
- 來源：[1] p8 retrieval, [2] p7 retrieval, [3] p1 retrieval, [4] p8 retrieval, [5] p1 retrieval, [6] p8 table_context
- 閱讀計畫（定位 1/1，保留 0，超預算 0）：
  - ✓ Table 2 (page 8): Performance of ablated versions of LightRAG, using NaiveRAG as reference.
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
The ablated versions of LightRAG were evaluated, and the results show the impact of different retrieval paradigms and configurations. The main findings are as follows:

1. **Low-level-only Retrieval (-High variant)**: This variant removes high-order retrieval, leading to a significant performance decline across nearly all datasets and metrics. It focuses on specific entities and their immediate neighbors, which limits its ability to provide comprehensive insights for complex queries [6].

2. **High-level-only Retrieval (-Low variant)**: This variant prioritizes capturing a broader range of content by leveraging entity-wise relationships. It performs well in terms of comprehensiveness but struggles with providing detailed insights, as it lacks the depth of low-level retrieval [6].

3. **Hybrid Mode (Full version of LightRAG)**: This mode combines both low-level and high-level retrieval methods. It achieves balanced performance by retrieving a broader set of relationships while also conducting in-depth exploration of specific entities [6].

4. **Semantic Graph-based Retrieval (-Origin variant)**: This variant eliminates the use of original text in the retrieval process. Surprisingly, it does not exhibit significant performance declines and even shows improvements in some cases, such as in the Agriculture and Mix datasets. This is attributed to the effective extraction of key information during the graph-based indexing process, which reduces noise from irrelevant information [6].

These results highlight the importance of the dual-level retrieval paradigm in LightRAG, where both low-level and high-level retrieval contribute to achieving balanced performance across multiple dimensions.
```

## B-Q3-2

- 問題：`Performance of ablated versions of LightRAG`；模式 `navigate`；32.4 秒；2 次呼叫；tokens 7221
- 來源：[1] p8 retrieval, [2] p7 retrieval, [3] p1 retrieval, [4] p8 retrieval, [5] p1 retrieval, [6] p8 table_context, [7] p3 navigation, [8] p3 navigation, [9] p3 navigation, [10] p3 navigation, [11] p4 navigation
- 閱讀計畫（定位 6/6，保留 6，超預算 21）：
  - ✓ Table 2 (page 8): Performance of ablated versions of LightRAG, using NaiveRAG as reference.
  - ✓ Section: THE LIGHT RAG ARCHITECTURE (pages 3-5): Describes the components that may be ablated.
  - ✓ Section: EVALUATION (pages 5-10): Contains the evaluation methodology and context for the ablation study.
  - ✓ Figure 1 (page 3): Overall architecture of the proposed LightRAG framework.
  - ✓ Section: APPENDIX (pages 13-16): May provide additional details about the ablation experiments.
  - ✓ Table 5 (page 16): Case Study: Comparison Between LightRAG and the Baseline NaiveRAG.
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
The performance of ablated versions of LightRAG was evaluated using NaiveRAG as a reference, and the results are presented in Table 2 [1]. The ablated versions include the -High variant, the -Low variant, and the -Origin variant.

1. **-High Variant**: This variant removes high-order retrieval, leading to a significant performance decline across nearly all datasets and metrics. For example, in the Agriculture dataset, the Comprehensiveness score for -High is 65.2% compared to NaiveRAG's 34.8%, indicating a performance drop. However, in the Mix dataset, the Comprehensiveness score for -High is 59.6%, which is slightly higher than NaiveRAG's 40.4%, showing an improvement in this specific case [1].

2. **-Low Variant**: This variant prioritizes capturing a broader range of content by leveraging entity-wise relationships rather than focusing on specific entities. In the Agriculture dataset, the Comprehensiveness score for -Low is 64.0%, which is higher than NaiveRAG's 36.0%. However, in the Legal dataset, the Comprehensiveness score for -Low is 80.8%, which is higher than NaiveRAG's 19.2%, indicating a significant improvement. However, in tasks requiring precise, detailed answers, the -Low variant may struggle due to its reduced depth in examining specific entities [1].

3. **-Origin Variant**: This variant eliminates the use of original text in the retrieval process. Surprisingly, the -Origin variant does not exhibit significant performance declines across all four datasets. In some cases, such as the Agriculture and Mix datasets, this variant even shows improvements. For example, in the Agriculture dataset, the Comprehensiveness score for -Origin is 75.2%, which is higher than NaiveRAG's 24.8% [1].

The hybrid mode, or the full version of LightRAG, combines the strengths of both low-level and high-level retrieval methods, achieving balanced performance across multiple dimensions [6].
```

## B-Q3-3

- 問題：`Performance of ablated versions of LightRAG`；模式 `navigate`；53.9 秒；2 次呼叫；tokens 7788
- 來源：[1] p8 retrieval, [2] p7 retrieval, [3] p1 retrieval, [4] p8 retrieval, [5] p1 retrieval, [6] p8 table_context, [7] p5 navigation, [8] p5 navigation, [9] p5 navigation, [10] p6 navigation, [11] p6 navigation
- 閱讀計畫（定位 6/6，保留 6，超預算 9）：
  - ✓ Table 2 (page 8): Performance of ablated versions of LightRAG, using NaiveRAG as reference.
  - ✓ Section: EVALUATION (pages 5-10): General context for evaluation details.
  - ✓ Section: THE LIGHT RAG ARCHITECTURE (pages 3-5): Background on LightRAG components.
  - ✓ [1] 2410.05779v3.pdf, page 8: Specific ablation results mentioned in retrieved source.
  - ✓ [4] 2410.05779v3.pdf, page 8: Additional details on variant improvements.
  - ✓ [6] 2410.05779v3.pdf, page 8: Description of ablation variant configurations.
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 25；找不到的數字 []

```text
The performance of ablated versions of LightRAG was evaluated using four datasets: Agriculture, CS (Computer Science), Legal, and Mix. These versions include -High (removing high-level retrieval), -Low (removing low-level retrieval), and -Origin (using only the graph-based indexing without original text). The results are compared against the full LightRAG and the NaiveRAG baseline.

### Main Findings:
- **-High (High-level-only retrieval)**: This variant performs significantly worse than LightRAG across all datasets and metrics. It excels in capturing broader content and comprehensiveness but lacks depth in specific entity exploration. This leads to a reduced ability to provide detailed insights, especially for complex queries [6].
  - Example: On the Legal dataset, the -High variant shows 76.4% comprehensiveness compared to LightRAG's 83.6%, but its empowerment score drops to 77.2% from LightRAG's 83.6% [1].

- **-Low (Low-level-only retrieval)**: This variant shows a strong focus on specific entities and their neighbors, enabling detailed exploration. However, it struggles with complex queries requiring broader insights.
  - Example: On the Agriculture dataset, the -Low variant achieves 64.0% comprehensiveness compared to LightRAG's 67.6%, but its diversity score is 72.0% versus LightRAG's 76.4% [1].

- **-Origin (Graph-based indexing without original text)**: This variant surprisingly does not show significant performance decline and even shows improvements in some cases (e.g., in Agriculture and Mix). This is attributed to the effective extraction of key information during graph-based indexing and the removal of noise from the original text [6].
  - Example: On the CS dataset, the -Origin variant achieves 60.8% comprehensiveness, slightly better than LightRAG's 61.6% [1].

- **Hybrid Mode (Full LightRAG)**: This combines the strengths of both low-level and high-level retrieval, achieving a balanced performance across all metrics and datasets [6].
  - Example: On the Mix dataset, LightRAG achieves 60.0% overall performance, significantly better than -High's 57.6% and -Low's 64.8% [1].

### Representative Figures:
- **Agriculture Dataset**:
  - Comprehensiveness: LightRAG (67.6%) vs. -High (65.2%) vs. -Low (64.0%) vs. -Origin (75.2%) [1].
  - Diversity: LightRAG (76.4%) vs. -High (72.8%) vs. -Low (72.0%) vs. -Origin (73.6%) [1].

- **Legal Dataset**:
  - Empowerment: LightRAG (83.6%) vs. -High (77.2%) vs. -Low (83.6%) vs. -Origin (82.8%) [1].
  - Overall: LightRAG (84.8%) vs. -High (78.0%) vs. -Low (81.2%) vs. -Origin (84.4%) [1].

- **Mix Dataset**:
  - Comprehensiveness: LightRAG (61.2%) vs. -High (59.6%) vs. -Low (64.0%) vs. -Origin (55.6%) [1].
  - Diversity: LightRAG (67.6%) vs. -High (64.0%) vs. -Low (66.8%) vs. -Origin (74.4%) [1].

### Results Against the Trend:
- The -Origin variant shows improvements in some cases, such as in the Agriculture dataset's comprehensiveness and Mix dataset's diversity, which goes against the expectation of performance decline [6].

### Conclusion:
The ablation studies show that the hybrid mode of LightRAG, combining low-level and high-level retrieval, achieves the best overall performance. Variants that remove one retrieval level or rely solely on graph-based indexing without original text show mixed results, with some metrics performing worse and others slightly better. The -Origin variant demonstrates that graph-based indexing can effectively capture key information, but its success is dataset-dependent.
```

## B2-Q3-1

- 問題：`Performance of ablated versions of LightRAG`；模式 `navigate`；38.7 秒；2 次呼叫；tokens 8085
- 來源：[1] p8 retrieval, [2] p7 retrieval, [3] p1 retrieval, [4] p8 retrieval, [5] p1 retrieval, [6] p8 table_context, [7] p16 navigation, [8] p4 navigation, [9] p16 navigation, [10] p16 navigation, [11] p9 navigation
- 閱讀計畫（定位 6/6，保留 6，超預算 3）：
  - ✓ Section 4.3 ABLATION STUDIES (RQ2) | need: overview of ablation studies | priority: required | status: covered → 候選 3，納入 []，排除 [(22, 'already among the retrieved sources'), (21, 'already among the retrieved sources'), (23, 'already among the retrieved sources')]
  - ✓ Table 2 | need: performance metrics of ablated versions | priority: required | status: covered → 候選 2，納入 []，排除 [(22, 'already among the retrieved sources'), (23, 'already among the retrieved sources')]
  - ✓ Section 4.4 CASE STUDY (RQ3) | need: case study on ablation effects | priority: supplementary | status: covered → 候選 5，納入 [27]，排除 [(24, 'already among the retrieved sources'), (23, 'already among the retrieved sources'), (26, 'over the evidence budget'), (25, 'over the evidence budget')]
  - ✓ Section 7.4 CASE STUDY: COMPARISON BETWEEN LIGHT RAG AND THE BASELINE NAIVE RAG | need: further case study on ablation | priority: supplementary | status: missing → 候選 2，納入 [45]，排除 [(44, 'already selected for another target')]
  - ✓ Table 5 | need: case study comparison data | priority: supplementary | status: missing → 候選 2，納入 [43, 44]，排除 []
  - ✓ Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM | need: methodological basis of ablation | priority: supplementary | status: missing → 候選 3，納入 [11, 13]，排除 [(12, 'over the evidence budget')]
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
The ablation studies evaluate the performance of different versions of LightRAG, including variants that omit either the low-level or high-level retrieval components. The main findings from the ablation studies are as follows:

1. **Low-level-only Retrieval (-High variant)**: This variant, which removes high-level retrieval, shows a significant performance decline across nearly all datasets and metrics. The drop in performance is mainly due to the variant's focus on specific entities and their immediate neighbors, which limits its ability to handle complex queries that require broader insights [6].

2. **High-level-only Retrieval (-Low variant)**: This variant prioritizes capturing a broader range of content by leveraging entity-wise relationships rather than focusing on specific entities. While it performs well in comprehensiveness, it struggles with depth in examining specific entities, which can limit its ability to provide highly detailed insights [6].

3. **Hybrid Mode (Full LightRAG)**: The hybrid mode combines the strengths of both low-level and high-level retrieval methods. It retrieves a broader set of relationships while conducting an in-depth exploration of specific entities, ensuring both breadth and depth in the retrieval process [6].

4. **Semantic Graph Excels in RAG (-Origin variant)**: The -Origin variant, which eliminates the use of original text in retrieval, does not exhibit significant performance declines across all four datasets. In some cases, such as in Agriculture and Mix, it even shows improvements. This is attributed to the effective extraction of key information during the graph-based indexing process [6].

**Representative Figures Supporting These Findings**:
- **Comprehensiveness - Agriculture**: NaiveRAG 32.4%, LightRAG 67.6% [1].
- **Diversity - Agriculture**: NaiveRAG 23.6%, LightRAG 76.4% [1].
- **Empowerment - Agriculture**: NaiveRAG 32.4%, LightRAG 67.6% [1].
- **Overall - Agriculture**: NaiveRAG 32.4%, LightRAG 67.6% [1].

**Results That Go Against the Trend**:
- The -Origin variant shows improvements in some cases (e.g., in Agriculture and Mix) despite eliminating the use of original text [6].

**Conclusion**:
The hybrid mode of LightRAG, which combines low-level and high-level retrieval, provides balanced performance across multiple dimensions. Variants that omit either low-level or high-level retrieval show significant performance declines, while the -Origin variant demonstrates that graph-based indexing can effectively capture key information for answering queries [6].
```

## B2-Q3-2

- 問題：`Performance of ablated versions of LightRAG`；模式 `navigate`；42.0 秒；2 次呼叫；tokens 8146
- 來源：[1] p8 retrieval, [2] p7 retrieval, [3] p1 retrieval, [4] p8 retrieval, [5] p1 retrieval, [6] p8 table_context, [7] p4 navigation, [8] p5 navigation, [9] p9 navigation, [10] p4 navigation, [11] p9 navigation
- 閱讀計畫（定位 6/6，保留 6，超預算 0）：
  - ✓ Section 4.3 ABLATION STUDIES (RQ2) | need: description of ablation studies | priority: required | status: covered → 候選 3，納入 []，排除 [(22, 'already among the retrieved sources'), (21, 'already among the retrieved sources'), (23, 'already among the retrieved sources')]
  - ✓ Table 2 | need: quantitative performance results | priority: required | status: covered → 候選 2，納入 []，排除 [(22, 'already among the retrieved sources'), (23, 'already among the retrieved sources')]
  - ✓ Section 4.4 CASE STUDY (RQ3) | need: additional context on ablated variants | priority: supplementary | status: covered → 候選 5，納入 [27, 26, 25]，排除 [(24, 'already among the retrieved sources'), (23, 'already among the retrieved sources')]
  - ✓ Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM | need: method description of ablated components | priority: supplementary | status: missing → 候選 3，納入 [11, 13, 12]，排除 []
  - ✓ Section 7.3.1 PROMPTS FOR GRAPH GENERATION | need: implementation details of ablated variants | priority: supplementary | status: missing → 候選 1，納入 []，排除 [(41, 'low relevance')]
  - ✓ Section 7.3.2 PROMPTS FOR QUERY GENERATION | need: implementation details of ablated variants | priority: supplementary | status: missing → 候選 1，納入 []，排除 [(41, 'low relevance')]
- 檢查：標籤不符 []；全稱宣稱 1；引用可疑 [([1], [2])]；未解析 11；找不到的數字 []

```text
The ablation studies in Table 2 compare the performance of different variants of LightRAG against the baseline NaiveRAG and other ablated versions. The evaluation is based on four dimensions: Comprehensiveness, Diversity, Empowerment, and Overall. The results are presented across four datasets: Agriculture, CS, Legal, and Mix.

1. **Comprehensiveness**:
   - In all datasets, LightRAG significantly outperforms NaiveRAG. For example, in the Agriculture dataset, LightRAG achieves 67.6% versus NaiveRAG's 32.4% [1].
   - The -High variant (which removes high-level retrieval) shows a significant performance drop compared to the full version of LightRAG. For example, in the Agriculture dataset, it achieves 65.2% versus LightRAG's 67.6% [1].
   - The -Low variant (which removes low-level retrieval) also shows a performance decline, with 64.0% in the Agriculture dataset versus LightRAG's 67.6% [1].

2. **Diversity**:
   - LightRAG outperforms NaiveRAG in all datasets. For example, in the Agriculture dataset, LightRAG achieves 76.4% versus NaiveRAG's 23.6% [1].
   - The -High variant performs slightly worse than the full version, achieving 72.8% in the Agriculture dataset [1].
   - The -Low variant performs worse than the full version, with 72.0% in the Agriculture dataset [1].

3. **Empowerment**:
   - LightRAG significantly outperforms NaiveRAG across all datasets. For example, in the Agriculture dataset, LightRAG achieves 67.6% versus NaiveRAG's 32.4% [1].
   - The -High variant performs slightly worse than the full version, with 64.0% in the Agriculture dataset [1].
   - The -Low variant performs worse than the full version, with 65.2% in the Agriculture dataset [1].

4. **Overall**:
   - LightRAG outperforms NaiveRAG in all datasets. For example, in the Agriculture dataset, LightRAG achieves 67.6% versus NaiveRAG's 32.4% [1].
   - The -High variant performs slightly worse than the full version, with 64.8% in the Agriculture dataset [1].
   - The -Low variant performs worse than the full version, with 65.2% in the Agriculture dataset [1].

The full version of LightRAG, which combines both low-level and high-level retrieval methods, achieves the best performance across all metrics and datasets. This indicates that the dual-level retrieval paradigm is effective in enhancing the performance of the LightRAG system [6].

A claim the source table does not bear out: "The full version of LightRAG, which combines both low-level and high-level retrieval methods, achieves the best performance across all metrics and datasets." — LightRAG is above the compared methods in 53 cells and below in 8, for example Comprehensiveness / Agriculture: LightRAG 67.6% vs -Origin 75.2% (p. 8); Comprehensiveness / Mix: LightRAG 61.2% vs -Low 64.0% (p. 8); Diversity / CS: LightRAG 62.0% vs -High 63.2% (p. 8).
```

## B2-Q3-3

- 問題：`Performance of ablated versions of LightRAG`；模式 `navigate`；34.1 秒；2 次呼叫；tokens 7975
- 來源：[1] p8 retrieval, [2] p7 retrieval, [3] p1 retrieval, [4] p8 retrieval, [5] p1 retrieval, [6] p8 table_context, [7] p16 navigation, [8] p4 navigation, [9] p16 navigation, [10] p16 navigation, [11] p5 navigation
- 閱讀計畫（定位 6/6，保留 6，超預算 3）：
  - ✓ Section 4.3 ABLATION STUDIES (RQ2) | need: description of ablation studies | priority: required | status: covered → 候選 3，納入 []，排除 [(22, 'already among the retrieved sources'), (21, 'already among the retrieved sources'), (23, 'already among the retrieved sources')]
  - ✓ Table 2 | need: quantitative results of ablated versions | priority: required | status: covered → 候選 2，納入 []，排除 [(22, 'already among the retrieved sources'), (23, 'already among the retrieved sources')]
  - ✓ Section 4.4 CASE STUDY (RQ3) | need: case study on ablated variants | priority: supplementary | status: covered → 候選 5，納入 [27]，排除 [(24, 'already among the retrieved sources'), (23, 'already among the retrieved sources'), (26, 'over the evidence budget'), (25, 'over the evidence budget')]
  - ✓ Section 7.4 CASE STUDY: COMPARISON BETWEEN LIGHT RAG AND THE BASELINE NAIVE RAG | need: additional case study on ablated variants | priority: supplementary | status: missing → 候選 2，納入 [45]，排除 [(44, 'already selected for another target')]
  - ✓ Table 5 | need: case study comparison results | priority: supplementary | status: missing → 候選 2，納入 [43, 44]，排除 []
  - ✓ Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM | need: design rationale for ablated components | priority: supplementary | status: missing → 候選 3，納入 [11, 13]，排除 [(12, 'over the evidence budget')]
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
The performance of ablated versions of LightRAG was evaluated against the full model and baseline methods, revealing the impact of different retrieval strategies. Key findings from the ablation studies include:

1. **Low-Level-Only Retrieval (-High variant)**: Removing high-order retrieval significantly reduced performance across most datasets and metrics. This variant focuses on specific entities and their immediate neighbors, which limits its ability to handle complex queries requiring broader insights [6].

2. **High-Level-Only Retrieval (-Low variant)**: This variant, which emphasizes broader content through entity-wise relationships, showed improved comprehensiveness but reduced depth in specific entity analysis. While it gathers more extensive information, it may struggle with tasks requiring detailed answers [6].

3. **Hybrid Mode (Full LightRAG)**: Combining low-level and high-level retrieval strategies, the full version of LightRAG achieved balanced performance across multiple dimensions. It effectively retrieves a broad set of relationships while also conducting in-depth exploration of specific entities [6].

4. **Semantic Graph-Based Retrieval (-Origin variant)**: This variant, which eliminates the use of original text in the retrieval process, did not show significant performance declines and even showed improvements in some cases (e.g., Agriculture and Mix). The graph-based indexing process effectively extracts key information, providing sufficient context for answering queries [6].

Supporting these findings, quantitative results in Table 2 show the performance of ablated versions of LightRAG using NaiveRAG as a reference. For example, in the Agriculture dataset, the -High variant showed 65.2% comprehensiveness compared to NaiveRAG's 34.8%, while the -Low variant showed 64.0% comprehensiveness compared to NaiveRAG's 36.0% [1].

In contrast, the -Origin variant demonstrated 75.2% comprehensiveness in the Agriculture dataset compared to NaiveRAG's 24.8% [1].

These results indicate that the dual-level retrieval paradigm in LightRAG contributes to its superior performance across various datasets and metrics.
```

## B3-Q3-1

- 問題：`Performance of ablated versions of LightRAG`；模式 `navigate`；59.6 秒；2 次呼叫；tokens 7028
- 來源：[1] p8 retrieval, [2] p7 retrieval, [3] p1 retrieval, [4] p8 retrieval, [5] p1 retrieval, [6] p8 table_context
- 閱讀計畫（定位 6/6，保留 0，超預算 0）：
  - ✓ Section 4.3 ABLATION STUDIES (RQ2) | need: ablation study description | priority: required | status: covered → 候選 0，納入 []，排除 []
  - ✓ Table 2 | need: quantitative performance comparison | priority: required | status: covered → 候選 0，納入 []，排除 []
  - ✓ Section 4.4 CASE STUDY (RQ3) | need: additional context on ablation effects | priority: supplementary | status: covered → 候選 0，納入 []，排除 []
  - ✓ Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM | need: methodology background | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
  - ✓ Section 7.3.1 PROMPTS FOR GRAPH GENERATION | need: generation methodology details | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
  - ✓ Section 7.3.2 PROMPTS FOR QUERY GENERATION | need: retrieval methodology details | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
- 分析狀態：SUPPORTED_AND_COMPLETE；完整性 complete（required ['-High', '-Low', '-Origin', 'LightRAG']，缺 []，條件 Agriculture / Comprehensiveness）；方向核對 [('uncertain', '65.2%', '67.6%')]
- 涵蓋判定：Section 4.3 ABLATION STUDIES (RQ2)→covered；Table 2→covered；Section 4.4 CASE STUDY (RQ3)→partial；Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM→missing；Section 7.3.1 PROMPTS FOR GRAPH GENERATION→missing；Section 7.3.2 PROMPTS FOR QUERY GENERATION→missing；required 未納入 []；supplementary 用 0；Matrix {'cells': 128, 'tables': ['Table 2 [1]'], 'definitions': ['NaiveRAG', 'LightRAG', '-High']}
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
The question asks for the performance of ablated versions of LightRAG compared to the full model and the reference model, NaiveRAG, across different datasets and metrics.

### Compact Comparison Table

| Method            | Dataset  | Metric         | Score (%) |
|-------------------|----------|----------------|-----------|
| NaiveRAG          | Agriculture | Comprehensiveness | 32.4      |
| LightRAG          | Agriculture | Comprehensiveness | 67.6      |
| NaiveRAG -High    | Agriculture | Comprehensiveness | 34.8      |
| -High             | Agriculture | Comprehensiveness | 65.2      |
| NaiveRAG -Low     | Agriculture | Comprehensiveness | 36.0      |
| -Low              | Agriculture | Comprehensiveness | 64.0      |
| NaiveRAG -Origin  | Agriculture | Comprehensiveness | 24.8      |
| -Origin           | Agriculture | Comprehensiveness | 75.2      |
| NaiveRAG          | CS        | Comprehensiveness | 38.4      |
| LightRAG          | CS        | Comprehensiveness | 61.6      |
| NaiveRAG -High    | CS        | Comprehensiveness | 42.8      |
| -High             | CS        | Comprehensiveness | 57.2      |
| NaiveRAG -Low     | CS        | Comprehensiveness | 43.2      |
| -Low              | CS        | Comprehensiveness | 56.8      |
| NaiveRAG -Origin  | CS        | Comprehensiveness | 39.2      |
| -Origin           | CS        | Comprehensiveness | 60.8      |
| NaiveRAG          | Legal     | Comprehensiveness | 16.4      |
| LightRAG          | Legal     | Comprehensiveness | 83.6      |
| NaiveRAG -High    | Legal     | Comprehensiveness | 23.6      |
| -High             | Legal     | Comprehensiveness | 76.4      |
| NaiveRAG -Low     | Legal     | Comprehensiveness | 19.2      |
| -Low              | Legal     | Comprehensiveness | 80.8      |
| NaiveRAG -Origin  | Legal     | Comprehensiveness | 16.4      |
| -Origin           | Legal     | Comprehensiveness | 83.6      |
| NaiveRAG          | Mix       | Comprehensiveness | 38.8      |
| LightRAG          | Mix       | Comprehensiveness | 61.2      |
| NaiveRAG -High    | Mix       | Comprehensiveness | 40.4      |
| -High             | Mix       | Comprehensiveness | 59.6      |
| NaiveRAG -Low     | Mix       | Comprehensiveness | 36.0      |
| -Low              | Mix       | Comprehensiveness | 64.0      |
| NaiveRAG -Origin  | Mix       | Comprehensiveness | 44.4      |
| -Origin           | Mix       | Comprehensiveness | 55.6      |

### Analysis

LightRAG consistently outperforms NaiveRAG across all datasets and metrics, demonstrating the effectiveness of the dual-level retrieval paradigm. For example, in the Agriculture dataset, LightRAG achieves 67.6% in comprehensiveness, while NaiveRAG scores 32.4% [1]. Similar improvements are observed in the CS, Legal, and Mix datasets.

Ablation studies show that removing either the high-level or low-level retrieval leads to performance degradation compared to the full LightRAG model. The -High variant, which removes high-order retrieval, shows a significant drop in performance across nearly all datasets and metrics [6]. For example, in the Agriculture dataset, -High scores 65.2% in comprehensiveness, which is lower than LightRAG's 67.6% [1].

The -Low variant, which removes low-level retrieval, also performs worse than the full model. In the Agriculture dataset, -Low scores 64.0% in comprehensiveness, compared to LightRAG's 67.6% [1].

The -Origin variant, which eliminates the use of original text in retrieval, performs better than NaiveRAG in some cases but worse than LightRAG. For example, in the Agriculture dataset, -Origin scores 75.2% in comprehensiveness, which is better than NaiveRAG's 32.4% but worse than LightRAG's 67.6% [1].

In conclusion, the full LightRAG model outperforms its ablated variants and the baseline NaiveRAG across most datasets and metrics, demonstrating the importance of the dual-level retrieval paradigm [1][6].
```

## B3-Q3-2

- 問題：`Performance of ablated versions of LightRAG`；模式 `navigate`；85.6 秒；2 次呼叫；tokens 7657
- 來源：[1] p8 retrieval, [2] p7 retrieval, [3] p1 retrieval, [4] p8 retrieval, [5] p1 retrieval, [6] p8 table_context
- 閱讀計畫（定位 6/6，保留 0，超預算 0）：
  - ✓ Section 4.3 ABLATION STUDIES (RQ2) | need: description of ablation studies | priority: required | status: covered → 候選 0，納入 []，排除 []
  - ✓ Table 2 | need: quantitative results of ablated versions | priority: required | status: covered → 候選 0，納入 []，排除 []
  - ✓ Section 4.4 CASE STUDY (RQ3) | need: additional context on ablation impact | priority: supplementary | status: covered → 候選 0，納入 []，排除 []
  - ✓ Section 7.4 CASE STUDY: COMPARISON BETWEEN LIGHT RAG AND THE BASELINE NAIVE RAG | need: further analysis of ablation effects | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
  - ✓ Table 5 | need: comparative data from case study | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
  - ✓ Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM | need: methodological basis for ablations | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
- 分析狀態：SUPPORTED_AND_COMPLETE；完整性 complete（required ['-High', '-Low', '-Origin', 'LightRAG']，缺 []，條件 Agriculture / Comprehensiveness）；方向核對 []
- 涵蓋判定：Section 4.3 ABLATION STUDIES (RQ2)→covered；Table 2→covered；Section 4.4 CASE STUDY (RQ3)→partial；Section 7.4 CASE STUDY: COMPARISON BETWEEN LIGHT RAG AND THE BASELINE NAIVE RAG→missing；Table 5→missing；Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM→missing；required 未納入 []；supplementary 用 0；Matrix {'cells': 128, 'tables': ['Table 2 [1]'], 'definitions': ['NaiveRAG', 'LightRAG', '-High']}
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 118；找不到的數字 []

```text
The question asks for the performance of ablated versions of LightRAG, including which methods were tested, the datasets used, and the metrics evaluated.

### Compact Comparison Table of the Figures Used
| Method | Dataset | Metric | LightRAG Score | NaiveRAG Score | -High Score | -Low Score | -Origin Score |
|--------|---------|--------|----------------|----------------|-------------|------------|---------------|
| Comprehensiveness | Agriculture | % | 67.6% | 32.4% | 65.2% | 64.0% | 75.2% |
| Comprehensiveness | CS | % | 61.6% | 38.4% | 57.2% | 56.8% | 60.8% |
| Comprehensiveness | Legal | % | 83.6% | 16.4% | 76.4% | 80.8% | 83.6% |
| Comprehensiveness | Mix | % | 61.2% | 38.8% | 59.6% | 64.0% | 55.6% |
| Diversity | Agriculture | % | 76.4% | 23.6% | 72.8% | 72.0% | 73.6% |
| Diversity | CS | % | 62.0% | 38.0% | 63.2% | 60.4% | 55.2% |
| Diversity | Legal | % | 86.4% | 13.6% | 83.2% | 86.4% | 85.6% |
| Diversity | Mix | % | 67.6% | 32.4% | 64.0% | 66.8% | 74.4% |
| Empowerment | Agriculture | % | 67.6% | 32.4% | 64.0% | 65.2% | 68.0% |
| Empowerment | CS | % | 61.2% | 38.8% | 57.6% | 57.2% | 56.8% |
| Empowerment | Legal | % | 83.6% | 16.4% | 77.2% | 83.6% | 82.8% |
| Empowerment | Mix | % | 57.2% | 42.8% | 52.4% | 64.8% | 54.8% |
| Overall | Agriculture | % | 67.6% | 32.4% | 64.8% | 65.2% | 74.4% |
| Overall | CS | % | 61.2% | 38.8% | 56.0% | 56.4% | 60.8% |
| Overall | Legal | % | 84.8% | 15.2% | 78.0% | 81.2% | 84.4% |
| Overall | Mix | % | 60.0% | 40.0% | 57.6% | 64.8% | 55.6% |

### Analysis

#### -High variant (removes high-order retrieval)
- **Comprehensiveness**: Performance drops across all datasets compared to LightRAG. The most significant drop is in the Legal dataset (83.6% for LightRAG vs 76.4% for -High) [6].
- **Diversity**: Performance drops in Agriculture (76.4% vs 72.8%), CS (62.0% vs 63.2%), and Mix (67.6% vs 64.0%), but slightly improves in Legal (86.4% vs 83.2%) [1].
- **Empowerment**: Performance drops in Agriculture (67.6% vs 64.0%), CS (61.2% vs 57.6%), and Mix (57.2% vs 52.4%), but slightly improves in Legal (83.6% vs 77.2%) [1].
- **Overall**: Performance drops in all datasets, with the most significant drop in Legal (84.8% vs 78.0%) [1].

#### -Low variant (removes low-level retrieval)
- **Comprehensiveness**: Performance drops in Agriculture (67.6% vs 64.0%), CS (61.6% vs 56.8%), and Mix (61.2% vs 64.0%), but slightly improves in Legal (83.6% vs 80.8%) [1].
- **Diversity**: Performance drops in Agriculture (76.4% vs 72.0%) and CS (62.0% vs 60.4%), but slightly improves in Legal (86.4% vs 86.4%) and Mix (67.6% vs 66.8%) [1].
- **Empowerment**: Performance drops in Agriculture (67.6% vs 65.2%), CS (61.2% vs 57.2%), and Mix (57.2% vs 64.8%), but slightly improves in Legal (83.6% vs 83.6%) [1].
- **Overall**: Performance drops in Agriculture (67.6% vs 65.2%), CS (61.2% vs 56.4%), and Mix (60.0% vs 64.8%), but slightly improves in Legal (84.8% vs 81.2%) [1].

#### -Origin variant (removes original text)
- **Comprehensiveness**: Performance improves in Agriculture (32.4% vs 75.2%), Mix (38.8% vs 55.6%), and Legal (16.4% vs 83.6%), but drops in CS (38.4% vs 60.8%) [1].
- **Diversity**: Performance improves in Agriculture (23.6% vs 73.6%), Mix (32.4% vs 74.4%), and Legal (13.6% vs 85.6%), but drops in CS (38.0% vs 55.2%) [1].
- **Empowerment**: Performance improves in Agriculture (32.4% vs 68.0%), CS (38.8% vs 56.8%), and Legal (16.4% vs 82.8%), but drops in Mix (42.8% vs 54.8%) [1].
- **Overall**: Performance improves in Agriculture (32.4% vs 74.4%), Legal (15.2% vs 84.4%), and Mix (40.0% vs 55.6%), but drops in CS (38.8% vs 60.8%) [1].

### Conclusions
- **-High variant** generally regresses across all metrics and datasets, with some exceptions in Legal for Diversity and Empowerment.
- **-Low variant** shows mixed results, with performance drops in most cases but slight improvements in Legal for Comprehensiveness, Diversity, and Empowerment.
- **-Origin variant** shows significant improvements in Agriculture and Legal across all metrics, but performance drops in CS and Mix in some cases.
```

## B3-Q3-3

- 問題：`Performance of ablated versions of LightRAG`；模式 `navigate`；72.5 秒；2 次呼叫；tokens 7345
- 來源：[1] p8 retrieval, [2] p7 retrieval, [3] p1 retrieval, [4] p8 retrieval, [5] p1 retrieval, [6] p8 table_context
- 閱讀計畫（定位 6/6，保留 0，超預算 0）：
  - ✓ Section 4.3 ABLATION STUDIES (RQ2) | need: overview of ablation study | priority: required | status: missing → 候選 0，納入 []，排除 []
  - ✓ Table 2 | need: performance comparison data | priority: required | status: covered → 候選 0，納入 []，排除 []
  - ✓ Section 4.4 CASE STUDY (RQ3) | need: case study context | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
  - ✓ Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM | need: retrieval paradigm description | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
  - ✓ Section 3.3 RETRIEVAL-AUGMENTED ANSWER GENERATION | need: answer generation process | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
  - ✓ Section 7.2 CASE EXAMPLE OF RETRIEVAL-AUGMENTED GENERATION IN LIGHT RAG | need: generation example | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
- 分析狀態：FACTUALLY_INCORRECT；完整性 complete（required ['-High', '-Low', '-Origin', 'LightRAG']，缺 []，條件 Agriculture / Comprehensiveness）；方向核對 []
- 涵蓋判定：Section 4.3 ABLATION STUDIES (RQ2)→covered；Table 2→covered；Section 4.4 CASE STUDY (RQ3)→partial；Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM→missing；Section 3.3 RETRIEVAL-AUGMENTED ANSWER GENERATION→missing；Section 7.2 CASE EXAMPLE OF RETRIEVAL-AUGMENTED GENERATION IN LIGHT RAG→missing；required 未納入 []；supplementary 用 0；Matrix {'cells': 128, 'tables': ['Table 2 [1]'], 'definitions': ['NaiveRAG', 'LightRAG', '-High']}
- 檢查：標籤不符 ['65.2%', '67.6%', '56.8%', '61.6%']；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
The question asks for a comparison of the performance of ablated versions of LightRAG, including the methods, datasets, and metrics used.

| Method         | Dataset    | Metric           | Performance (LightRAG baseline) |
|----------------|------------|------------------|---------------------------------|
| -High          | Agriculture| Comprehensiveness| 65.2%                           |
| -High          | Agriculture| Diversity        | 72.8%                           |
| -High          | Agriculture| Empowerment      | 64.0%                           |
| -High          | Agriculture| Overall          | 64.8%                           |
| -High          | CS         | Comprehensiveness| 57.2%                           |
| -High          | CS         | Diversity        | 63.2%                           |
| -High          | CS         | Empowerment      | 57.6%                           |
| -High          | CS         | Overall          | 56.0%                           |
| -High          | Legal      | Comprehensiveness| 76.4%                           |
| -High          | Legal      | Diversity        | 83.2%                           |
| -High          | Legal      | Empowerment      | 77.2%                           |
| -High          | Legal      | Overall          | 78.0%                           |
| -High          | Mix        | Comprehensiveness| 59.6%                           |
| -High          | Mix        | Diversity        | 64.0%                           |
| -High          | Mix        | Empowerment      | 52.4%                           |
| -High          | Mix        | Overall          | 57.6%                           |
| -Low           | Agriculture| Comprehensiveness| 64.0%                           |
| -Low           | Agriculture| Diversity        | 72.0%                           |
| -Low           | Agriculture| Empowerment      | 65.2%                           |
| -Low           | Agriculture| Overall          | 65.2%                           |
| -Low           | CS         | Comprehensiveness| 56.8%                           |
| -Low           | CS         | Diversity        | 60.4%                           |
| -Low           | CS         | Empowerment      | 57.2%                           |
| -Low           | CS         | Overall          | 56.4%                           |
| -Low           | Legal      | Comprehensiveness| 80.8%                           |
| -Low           | Legal      | Diversity        | 86.4%                           |
| -Low           | Legal      | Empowerment      | 83.6%                           |
| -Low           | Legal      | Overall          | 81.2%                           |
| -Low           | Mix        | Comprehensiveness| 64.0%                           |
| -Low           | Mix        | Diversity        | 66.8%                           |
| -Low           | Mix        | Empowerment      | 64.8%                           |
| -Low           | Mix        | Overall          | 64.8%                           |
| -Origin        | Agriculture| Comprehensiveness| 75.2%                           |
| -Origin        | Agriculture| Diversity        | 73.6%                           |
| -Origin        | Agriculture| Empowerment      | 68.0%                           |
| -Origin        | Agriculture| Overall          | 74.4%                           |
| -Origin        | CS         | Comprehensiveness| 60.8%                           |
| -Origin        | CS         | Diversity        | 55.2%                           |
| -Origin        | CS         | Empowerment      | 56.8%                           |
| -Origin        | CS         | Overall          | 60.8%                           |
| -Origin        | Legal      | Comprehensiveness| 83.6%                           |
| -Origin        | Legal      | Diversity        | 85.6%                           |
| -Origin        | Legal      | Empowerment      | 82.8%                           |
| -Origin        | Legal      | Overall          | 84.4%                           |
| -Origin        | Mix        | Comprehensiveness| 55.6%                           |
| -Origin        | Mix        | Diversity        | 74.4%                           |
| -Origin        | Mix        | Empowerment      | 54.8%                           |
| -Origin        | Mix        | Overall          | 55.6%                           |

The ablated versions of LightRAG show varied performance compared to the full LightRAG model. 

- The -High variant, which removes high-order retrieval, shows a significant performance decline across nearly all datasets and metrics, especially in the CS and Mix datasets. For example, in the CS dataset, the -High variant performs at 57.2% in Comprehensiveness, compared to 61.6% in LightRAG [1]. However, in the Agriculture dataset, -High performs slightly better than LightRAG in some metrics, such as Comprehensiveness at 65.2% versus 67.6% in LightRAG [1].

- The -Low variant, which removes low-level retrieval, performs better than -High in most cases, particularly in the Legal and Mix datasets. For example, in the Legal dataset, the -Low variant performs at 80.8% in Comprehensiveness, compared to 76.4% in -High [1]. However, in the CS dataset, the -Low variant performs worse than LightRAG in most metrics, such as Comprehensiveness at 56.8% versus 61.6% in LightRAG [1].

- The -Origin variant, which eliminates the use of original text, performs surprisingly well in some cases, such as in the Agriculture and Mix datasets, where it shows improvements in some metrics. For example, in the Agriculture dataset, -Origin performs at 75.2% in Comprehensiveness, compared to 67.6% in LightRAG [1]. However, in the Mix dataset, -Origin performs worse in Comprehensiveness at 55.6% versus 61.2% in LightRAG [1].

The full version of LightRAG combines the strengths of both low-level and high-level retrieval methods, achieving balanced performance across multiple dimensions [6].

Figures whose labels differ from the source table: 65.2% (answer: Comprehensiveness, Agriculture, -High, vs LightRAG; source: Comprehensiveness, Agriculture, -High, vs NaiveRAG / Empowerment, Agriculture, -Low, vs NaiveRAG / Overall, Agriculture, -Low, vs NaiveRAG); 67.6% (answer: Comprehensiveness, Agriculture, LightRAG, vs LightRAG; source: Comprehensiveness, Agriculture, LightRAG, vs NaiveRAG / Diversity, Mix, LightRAG, vs NaiveRAG / Empowerment, Agriculture, LightRAG, vs NaiveRAG / Overall, Agriculture, LightRAG, vs NaiveRAG); 56.8% (answer: Comprehensiveness, CS, -Low, vs LightRAG; source: Comprehensiveness, CS, -Low, vs NaiveRAG / Empowerment, CS, -Origin, vs NaiveRAG); 61.6% (answer: Comprehensiveness, CS, LightRAG, vs LightRAG; source: Comprehensiveness, CS, LightRAG, vs NaiveRAG).
```

## B4-Q3-1

- 問題：`Performance of ablated versions of LightRAG`；模式 `navigate`；52.9 秒；2 次呼叫；tokens 6903
- 來源：[1] p8 retrieval, [2] p7 retrieval, [3] p1 retrieval, [4] p8 retrieval, [5] p1 retrieval, [6] p8 table_context
- 閱讀計畫（定位 6/6，保留 0，超預算 0）：
  - ✓ Section 4.3 ABLATION STUDIES (RQ2) | need: ablation study description | priority: required | status: covered → 候選 0，納入 []，排除 []
  - ✓ Table 2 | need: ablation results | priority: required | status: covered → 候選 0，納入 []，排除 []
  - ✓ Section 4.4 CASE STUDY (RQ3) | need: additional context on variants | priority: supplementary | status: covered → 候選 0，納入 []，排除 []
  - ✓ Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM | need: method description for variants | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
  - ✓ Section 7.3.1 PROMPTS FOR GRAPH GENERATION | need: implementation details | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
  - ✓ Section 7.3.2 PROMPTS FOR QUERY GENERATION | need: implementation details | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
- 分析狀態：SUPPORTED_AND_COMPLETE；完整性 complete（required ['-High', '-Low', '-Origin', 'LightRAG']，缺 []，條件 Agriculture / Comprehensiveness）；方向核對 []
- 修正：[]；刪除 []；仍不符 []；方向待定 []
- 涵蓋判定：Section 4.3 ABLATION STUDIES (RQ2)→covered；Table 2→covered；Section 4.4 CASE STUDY (RQ3)→partial；Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM→missing；Section 7.3.1 PROMPTS FOR GRAPH GENERATION→missing；Section 7.3.2 PROMPTS FOR QUERY GENERATION→missing；required 未納入 []；supplementary 用 0；Matrix {'cells': 128, 'tables': ['Table 2 [1]'], 'definitions': ['NaiveRAG', 'LightRAG', '-High']}
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
The question asks for the performance of ablated versions of LightRAG, including the datasets and metrics used. The ablated versions considered are NaiveRAG -High, NaiveRAG -Low, and NaiveRAG -Origin. The datasets used are Agriculture, CS, Legal, and Mix. The metrics are Comprehensiveness, Diversity, Empowerment, and Overall. The performance is compared against the baseline method NaiveRAG and the full version LightRAG [1].

| Method | Dataset | Metric | Score |
|--------|---------|--------|-------|
| NaiveRAG | Agriculture | Comprehensiveness | 32.4% |
| LightRAG | Agriculture | Comprehensiveness | 67.6% |
| -High | Agriculture | Comprehensiveness | 65.2% |
| -Low | Agriculture | Comprehensiveness | 64.0% |
| -Origin | Agriculture | Comprehensiveness | 75.2% |
| NaiveRAG | CS | Comprehensiveness | 38.4% |
| LightRAG | CS | Comprehensiveness | 61.6% |
| -High | CS | Comprehensiveness | 57.2% |
| -Low | CS | Comprehensiveness | 56.8% |
| -Origin | CS | Comprehensiveness | 60.8% |
| NaiveRAG | Legal | Comprehensiveness | 16.4% |
| LightRAG | Legal | Comprehensiveness | 83.6% |
| -High | Legal | Comprehensiveness | 76.4% |
| -Low | Legal | Comprehensiveness | 80.8% |
| -Origin | Legal | Comprehensiveness | 83.6% |
| NaiveRAG | Mix | Comprehensiveness | 38.8% |
| LightRAG | Mix | Comprehensiveness | 61.2% |
| -High | Mix | Comprehensiveness | 59.6% |
| -Low | Mix | Comprehensiveness | 64.0% |
| -Origin | Mix | Comprehensiveness | 55.6% |

The ablation study results show that the -High variant, which removes high-order retrieval, experiences a significant performance decline across nearly all datasets and metrics. For example, in the Agriculture dataset, the Comprehensiveness score of -High is 65.2%, which is lower than LightRAG's 67.6% and higher than NaiveRAG's 32.4%. Similarly, in the CS dataset, the Comprehensiveness score of -High is 57.2%, which is lower than LightRAG's 61.6% and higher than NaiveRAG's 38.4% [1].

The -Low variant, which prioritizes capturing a broader range of content by leveraging entity-wise relationships, shows improvements in comprehensiveness but a reduced depth in examining specific entities. For example, in the Agriculture dataset, the Comprehensiveness score of -Low is 64.0%, which is lower than LightRAG's 67.6% and higher than NaiveRAG's 32.4%. In the CS dataset, the Comprehensiveness score of -Low is 56.8%, which is lower than LightRAG's 61.6% and higher than NaiveRAG's 38.4% [1].

The -Origin variant, which eliminates the use of original text in the retrieval process, does not exhibit significant performance declines across all four datasets. In some cases, this variant even shows improvements. For example, in the Agriculture dataset, the Comprehensiveness score of -Origin is 75.2%, which is higher than LightRAG's 67.6% and significantly higher than NaiveRAG's 32.4%. In the Mix dataset, the Comprehensiveness score of -Origin is 55.6%, which is lower than LightRAG's 61.2% and higher than NaiveRAG's 38.8% [1].

These results indicate that the hybrid mode, or the full version of LightRAG, combines the strengths of both low-level and high-level retrieval methods, achieving balanced performance across multiple dimensions [6].
```

## B4-Q3-2

- 問題：`Performance of ablated versions of LightRAG`；模式 `navigate`；51.4 秒；2 次呼叫；tokens 6870
- 來源：[1] p8 retrieval, [2] p7 retrieval, [3] p1 retrieval, [4] p8 retrieval, [5] p1 retrieval, [6] p8 table_context
- 閱讀計畫（定位 6/6，保留 0，超預算 0）：
  - ✓ Section 4.3 ABLATION STUDIES (RQ2) | need: ablation study description | priority: required | status: covered → 候選 0，納入 []，排除 []
  - ✓ Table 2 | need: ablation performance data | priority: required | status: covered → 候選 0，納入 []，排除 []
  - ✓ Section 4.4 CASE STUDY (RQ3) | need: additional context on ablation effects | priority: supplementary | status: covered → 候選 0，納入 []，排除 []
  - ✓ Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM | need: method description | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
  - ✓ Section 7.3.1 PROMPTS FOR GRAPH GENERATION | need: implementation details | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
  - ✓ Section 7.3.2 PROMPTS FOR QUERY GENERATION | need: implementation details | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
- 分析狀態：SUPPORTED_AND_COMPLETE；完整性 complete（required ['-High', '-Low', '-Origin', 'LightRAG']，缺 []，條件 Legal / Comprehensiveness）；方向核對 []
- 修正：[]；刪除 []；仍不符 []；方向待定 []
- 涵蓋判定：Section 4.3 ABLATION STUDIES (RQ2)→covered；Table 2→covered；Section 4.4 CASE STUDY (RQ3)→partial；Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM→missing；Section 7.3.1 PROMPTS FOR GRAPH GENERATION→missing；Section 7.3.2 PROMPTS FOR QUERY GENERATION→missing；required 未納入 []；supplementary 用 0；Matrix {'cells': 128, 'tables': ['Table 2 [1]'], 'definitions': ['NaiveRAG', 'LightRAG', '-High']}
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 22；找不到的數字 []

```text
The question asks for the performance of ablated versions of LightRAG, including the methods (LightRAG, NaiveRAG, -High, -Low, -Origin), the datasets (Agriculture, CS, Legal, Mix), and the metrics (Comprehensiveness, Diversity, Empowerment, Overall).

From Table 2 in source [1], the performance of ablated versions of LightRAG is compared against NaiveRAG across these four datasets and four metrics. Each ablation variant is evaluated to assess the impact of removing specific components of the dual-level retrieval paradigm.

For Comprehensiveness in the Agriculture dataset, -High achieves 65.2% versus NaiveRAG’s 34.8% [1], while -Low achieves 64.0% versus NaiveRAG’s 36.0% [1], and -Origin achieves 75.2% versus NaiveRAG’s 24.8% [1]. For Diversity in the Agriculture dataset, -High achieves 72.8% versus NaiveRAG’s 27.2% [1], -Low achieves 72.0% versus NaiveRAG’s 28.0% [1], and -Origin achieves 73.6% versus NaiveRAG’s 26.4% [1]. For Empowerment in the Agriculture dataset, -High achieves 64.0% versus NaiveRAG’s 36.0% [1], -Low achieves 65.2% versus NaiveRAG’s 34.8% [1], and -Origin achieves 68.0% versus NaiveRAG’s 32.0% [1]. For Overall in the Agriculture dataset, -High achieves 64.8% versus NaiveRAG’s 35.2% [1], -Low achieves 65.2% versus NaiveRAG’s 34.8% [1], and -Origin achieves 74.4% versus NaiveRAG’s 25.6% [1].

Across all four metrics, the -Origin variant performs the best in the Agriculture dataset, followed closely by -Low and -High, with NaiveRAG performing the worst. The same pattern is generally observed in the CS, Legal, and Mix datasets, with -Origin and -Low showing improvements in most cases, while -High and NaiveRAG show lower performance.

In the Legal dataset, -High achieves 76.4% for Comprehensiveness [1], -Low achieves 80.8% [1], and -Origin achieves 83.6% [1], with NaiveRAG at 19.2% [1]. For Diversity, -High achieves 83.2% [1], -Low achieves 86.4% [1], and -Origin achieves 85.6% [1], with NaiveRAG at 13.6% [1]. For Empowerment, -High achieves 77.2% [1], -Low achieves 83.6% [1], and -Origin achieves 82.8% [1], with NaiveRAG at 16.4% [1]. For Overall, -High achieves 78.0% [1], -Low achieves 81.2% [1], and -Origin achieves 84.4% [1], with NaiveRAG at 15.6% [1].

These results indicate that the ablated versions of LightRAG, particularly -Origin and -Low, generally outperform NaiveRAG and -High in most datasets and metrics. The -High variant, which removes high-order retrieval, shows a significant performance decline, especially in metrics requiring broader information gathering. The -Origin variant, which eliminates the use of original text, performs better in some datasets, suggesting that the graph-based indexing process effectively extracts key information and reduces noise from irrelevant text. The -Low variant, which focuses on low-level retrieval, also shows improvements in most cases, highlighting the importance of specific entity retrieval for detailed insights. The hybrid mode, or the full version of LightRAG, combines the strengths of both low-level and high-level retrieval, achieving balanced performance across multiple dimensions [6].
```

## B4-Q3-3

- 問題：`Performance of ablated versions of LightRAG`；模式 `navigate`；74.8 秒；2 次呼叫；tokens 7439
- 來源：[1] p8 retrieval, [2] p7 retrieval, [3] p1 retrieval, [4] p8 retrieval, [5] p1 retrieval, [6] p8 table_context
- 閱讀計畫（定位 6/6，保留 0，超預算 0）：
  - ✓ Section 4.3 ABLATION STUDIES (RQ2) | need: overview of ablation studies | priority: required | status: covered → 候選 0，納入 []，排除 []
  - ✓ Table 2 | need: performance metrics of ablated versions | priority: required | status: covered → 候選 0，納入 []，排除 []
  - ✓ Section 4.4 CASE STUDY (RQ3) | need: case study impact on ablated versions | priority: supplementary | status: covered → 候選 0，納入 []，排除 []
  - ✓ Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM | need: description of ablation components | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
  - ✓ Section 7.3.1 PROMPTS FOR GRAPH GENERATION | need: prompt details for ablated variants | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
  - ✓ Section 7.3.2 PROMPTS FOR QUERY GENERATION | need: prompt details for ablated variants | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
- 分析狀態：SUPPORTED_AND_COMPLETE；完整性 complete（required ['-High', '-Low', '-Origin', 'LightRAG']，缺 []，條件 Agriculture / Comprehensiveness）；方向核對 []
- 修正：[]；刪除 []；仍不符 []；方向待定 []
- 涵蓋判定：Section 4.3 ABLATION STUDIES (RQ2)→covered；Table 2→covered；Section 4.4 CASE STUDY (RQ3)→partial；Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM→missing；Section 7.3.1 PROMPTS FOR GRAPH GENERATION→missing；Section 7.3.2 PROMPTS FOR QUERY GENERATION→missing；required 未納入 []；supplementary 用 0；Matrix {'cells': 128, 'tables': ['Table 2 [1]'], 'definitions': ['NaiveRAG', 'LightRAG', '-High']}
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 8；找不到的數字 []

```text
The question asks for the performance of ablated versions of LightRAG, including the methods, datasets, and metrics used. The evidence comes from Table 2 in [1], which compares the performance of several ablated versions of LightRAG (including -High, -Low, and -Origin) using NaiveRAG as a reference. The datasets are Agriculture, CS, Legal, and Mix. The metrics are Comprehensiveness, Diversity, Empowerment, and Overall.

| Method        | Dataset    | Metric         | Score (%) |
|---------------|------------|----------------|-----------|
| NaiveRAG      | Agriculture| Comprehensiveness | 32.4     |
| LightRAG      | Agriculture| Comprehensiveness | 67.6     |
| NaiveRAG -High| Agriculture| Comprehensiveness | 34.8     |
| -High         | Agriculture| Comprehensiveness | 65.2     |
| NaiveRAG -Low | Agriculture| Comprehensiveness | 36.0     |
| -Low          | Agriculture| Comprehensiveness | 64.0     |
| NaiveRAG -Origin| Agriculture| Comprehensiveness | 24.8     |
| -Origin       | Agriculture| Comprehensiveness | 75.2     |
| NaiveRAG      | CS         | Diversity       | 38.0     |
| LightRAG      | CS         | Diversity       | 62.0     |
| NaiveRAG -High| CS         | Diversity       | 36.8     |
| -High         | CS         | Diversity       | 63.2     |
| NaiveRAG -Low | CS         | Diversity       | 39.6     |
| -Low          | CS         | Diversity       | 60.4     |
| NaiveRAG -Origin| CS        | Diversity       | 44.8     |
| -Origin       | CS         | Diversity       | 55.2     |
| NaiveRAG      | Legal      | Empowerment     | 16.4     |
| LightRAG      | Legal      | Empowerment     | 83.6     |
| NaiveRAG -High| Legal      | Empowerment     | 22.8     |
| -High         | Legal      | Empowerment     | 77.2     |
| NaiveRAG -Low | Legal      | Empowerment     | 16.4     |
| -Low          | Legal      | Empowerment     | 83.6     |
| NaiveRAG -Origin| Legal     | Empowerment     | 17.2     |
| -Origin       | Legal      | Empowerment     | 82.8     |
| NaiveRAG      | Mix        | Overall         | 40.0     |
| LightRAG      | Mix        | Overall         | 60.0     |
| NaiveRAG -High| Mix        | Overall         | 42.4     |
| -High         | Mix        | Overall         | 57.6     |
| NaiveRAG -Low | Mix        | Overall         | 35.2     |
| -Low          | Mix        | Overall         | 64.8     |
| NaiveRAG -Origin| Mix       | Overall         | 44.4     |
| -Origin       | Mix        | Overall         | 55.6     |

LightRAG consistently outperforms NaiveRAG in all metrics and datasets. For instance, in the Agriculture dataset, LightRAG achieves 67.6% in Comprehensiveness compared to NaiveRAG's 32.4% [1]. Similarly, in the CS dataset, LightRAG scores 62.0% in Diversity, while NaiveRAG scores 38.0% [1]. In the Legal dataset, LightRAG achieves 83.6% in Empowerment compared to NaiveRAG's 16.4% [1]. In the Mix dataset, LightRAG scores 60.0% in Overall compared to NaiveRAG's 40.0% [1].

The -High variant, which removes high-order retrieval, shows a significant performance decline across nearly all datasets and metrics compared to LightRAG. For example, in the Agriculture dataset, -High scores 65.2% in Comprehensiveness compared to LightRAG's 67.6% [1]. In the CS dataset, -High scores 63.2% in Diversity compared to LightRAG's 62.0% [1]. In the Legal dataset, -High scores 77.2% in Empowerment compared to LightRAG's 83.6% [1]. In the Mix dataset, -High scores 57.6% in Overall compared to LightRAG's 60.0% [1].

The -Low variant, which removes low-level retrieval, also shows a performance decline in most metrics and datasets compared to LightRAG. For example, in the Agriculture dataset, -Low scores 64.0% in Comprehensiveness compared to LightRAG's 67.6% [1]. In the CS dataset, -Low scores 60.4% in Diversity compared to LightRAG's 62.0% [1]. In the Legal dataset, -Low scores 83.6% in Empowerment compared to LightRAG's 83.6% [1]. In the Mix dataset, -Low scores 64.8% in Overall compared to LightRAG's 60.0% [1].

The -Origin variant, which eliminates the use of original text in retrieval, shows mixed results. It performs better in the Agriculture dataset for Comprehensiveness (75.2% vs. 67.6% for LightRAG) [1] and in the Mix dataset for Overall (55.6% vs. 60.0% for LightRAG) [1]. However, it performs worse in the CS dataset for Diversity (55.2% vs. 62.0% for LightRAG) [1] and in the Legal dataset for Empowerment (82.8% vs. 83.6% for LightRAG) [1].

In conclusion, the ablated versions of LightRAG show varying degrees of performance compared to the full version. The -High and -Low variants generally perform worse, while the -Origin variant shows mixed results [1]. The full version of LightRAG achieves balanced performance across multiple dimensions [6].
```

## B4b-Q3-1

- 問題：`Performance of ablated versions of LightRAG`；模式 `navigate`；89.2 秒；2 次呼叫；tokens 7807
- 來源：[1] p8 retrieval, [2] p7 retrieval, [3] p1 retrieval, [4] p8 retrieval, [5] p1 retrieval, [6] p8 table_context
- 閱讀計畫（定位 6/6，保留 0，超預算 0）：
  - ✓ Section 4.3 ABLATION STUDIES (RQ2) | need: overview of ablation studies | priority: required | status: covered → 候選 0，納入 []，排除 []
  - ✓ Table 2 | need: performance metrics of ablated versions | priority: required | status: covered → 候選 0，納入 []，排除 []
  - ✓ Section 4.2 COMPARISON OF LIGHT RAG WITH EXISTING RAG METHODS (RQ1) | need: baseline comparison context | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
  - ✓ Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM | need: description of ablated components | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
  - ✓ Section 7.2 CASE EXAMPLE OF RETRIEVAL-AUGMENTED GENERATION IN LIGHT RAG | need: example of full vs. ablated generation | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
  - ✓ Section 7.4 CASE STUDY: COMPARISON BETWEEN LIGHT RAG AND THE BASELINE NAIVE RAG | need: additional ablation context | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
- 分析狀態：SUPPORTED_AND_COMPLETE；完整性 complete（required ['-High', '-Low', '-Origin', 'LightRAG']，缺 []，條件 Legal / Comprehensiveness）；方向核對 []
- 修正：[('figure', '32.4%', '65.2%'), ('figure', '38.4%', '57.2%'), ('figure', '16.4%', '76.4%'), ('figure', '38.8%', '59.6%'), ('figure', '23.6%', '72.8%'), ('figure', '38.0%', '63.2%'), ('figure', '13.6%', '83.2%'), ('figure', '32.4%', '64.0%'), ('figure', '32.4%', '64.0%'), ('figure', '38.8%', '57.6%'), ('figure', '16.4%', '77.2%'), ('figure', '42.8%', '52.4%'), ('figure', '32.4%', '64.8%'), ('figure', '38.8%', '56.0%'), ('figure', '15.2%', '78.0%'), ('figure', '40.0%', '57.6%'), ('figure', '32.4%', '64.0%'), ('figure', '38.4%', '56.8%'), ('figure', '16.4%', '80.8%'), ('figure', '38.8%', '64.0%'), ('figure', '23.6%', '72.0%'), ('figure', '38.0%', '60.4%'), ('figure', '13.6%', '86.4%'), ('figure', '32.4%', '66.8%'), ('figure', '32.4%', '65.2%'), ('figure', '38.8%', '57.2%'), ('figure', '16.4%', '83.6%'), ('figure', '42.8%', '64.8%'), ('figure', '32.4%', '65.2%'), ('figure', '38.8%', '56.4%'), ('figure', '15.2%', '81.2%'), ('figure', '40.0%', '64.8%'), ('figure', '32.4%', '75.2%'), ('figure', '38.4%', '60.8%'), ('figure', '16.4%', '83.6%'), ('figure', '38.8%', '55.6%'), ('figure', '23.6%', '73.6%'), ('figure', '38.0%', '55.2%'), ('figure', '13.6%', '85.6%'), ('figure', '32.4%', '74.4%'), ('figure', '32.4%', '68.0%'), ('figure', '38.8%', '56.8%'), ('figure', '16.4%', '82.8%'), ('figure', '42.8%', '54.8%'), ('figure', '32.4%', '74.4%'), ('figure', '38.8%', '60.8%'), ('figure', '15.2%', '84.4%'), ('figure', '40.0%', '55.6%')]；刪除 []；仍不符 []；方向待定 []
- 涵蓋判定：Section 4.3 ABLATION STUDIES (RQ2)→covered；Table 2→covered；Section 4.2 COMPARISON OF LIGHT RAG WITH EXISTING RAG METHODS (RQ1)→partial；Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM→missing；Section 7.2 CASE EXAMPLE OF RETRIEVAL-AUGMENTED GENERATION IN LIGHT RAG→missing；Section 7.4 CASE STUDY: COMPARISON BETWEEN LIGHT RAG AND THE BASELINE NAIVE RAG→missing；required 未納入 []；supplementary 用 0；Matrix {'cells': 128, 'tables': ['Table 2 [1]'], 'definitions': ['LightRAG', 'NaiveRAG', '-High']}
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
The question asks for the performance of ablated versions of LightRAG, specifically how they compare to the original NaiveRAG in terms of datasets (Agriculture, CS, Legal, Mix) and metrics (Comprehensiveness, Diversity, Empowerment, Overall). The ablated variants under consideration are -High, -Low, -Origin.

| Method        | Dataset  | Metric         | NaiveRAG | Ablated Variant | Performance Change |
|---------------|----------|----------------|----------|------------------|--------------------|
| -High         | Agriculture | Comprehensiveness | 65.2%    | 65.2%            | Higher             |
| -High         | CS        | Comprehensiveness | 57.2%    | 57.2%            | Higher             |
| -High         | Legal     | Comprehensiveness | 76.4%    | 76.4%            | Higher             |
| -High         | Mix       | Comprehensiveness | 59.6%    | 59.6%            | Higher             |
| -High         | Agriculture | Diversity       | 72.8%    | 72.8%            | Higher             |
| -High         | CS        | Diversity       | 63.2%    | 63.2%            | Higher             |
| -High         | Legal     | Diversity       | 83.2%    | 83.2%            | Higher             |
| -High         | Mix       | Diversity       | 64.0%    | 64.0%            | Higher             |
| -High         | Agriculture | Empowerment   | 64.0%    | 64.0%            | Higher             |
| -High         | CS        | Empowerment   | 57.6%    | 57.6%            | Higher             |
| -High         | Legal     | Empowerment   | 77.2%    | 77.2%            | Higher             |
| -High         | Mix       | Empowerment   | 52.4%    | 52.4%            | Higher             |
| -High         | Agriculture | Overall       | 64.8%    | 64.8%            | Higher             |
| -High         | CS        | Overall       | 56.0%    | 56.0%            | Higher             |
| -High         | Legal     | Overall       | 78.0%    | 78.0%            | Higher             |
| -High         | Mix       | Overall       | 57.6%    | 57.6%            | Higher             |
| -Low          | Agriculture | Comprehensiveness | 64.0%    | 64.0%            | Higher             |
| -Low          | CS        | Comprehensiveness | 56.8%    | 56.8%            | Higher             |
| -Low          | Legal     | Comprehensiveness | 80.8%    | 80.8%            | Higher             |
| -Low          | Mix       | Comprehensiveness | 64.0%    | 64.0%            | Higher             |
| -Low          | Agriculture | Diversity       | 72.0%    | 72.0%            | Higher             |
| -Low          | CS        | Diversity       | 60.4%    | 60.4%            | Higher             |
| -Low          | Legal     | Diversity       | 86.4%    | 86.4%            | Higher             |
| -Low          | Mix       | Diversity       | 66.8%    | 66.8%            | Higher             |
| -Low          | Agriculture | Empowerment   | 65.2%    | 65.2%            | Higher             |
| -Low          | CS        | Empowerment   | 57.2%    | 57.2%            | Higher             |
| -Low          | Legal     | Empowerment   | 83.6%    | 83.6%            | Higher             |
| -Low          | Mix       | Empowerment   | 64.8%    | 64.8%            | Higher             |
| -Low          | Agriculture | Overall       | 65.2%    | 65.2%            | Higher             |
| -Low          | CS        | Overall       | 56.4%    | 56.4%            | Higher             |
| -Low          | Legal     | Overall       | 81.2%    | 81.2%            | Higher             |
| -Low          | Mix       | Overall       | 64.8%    | 64.8%            | Higher             |
| -Origin       | Agriculture | Comprehensiveness | 75.2%    | 75.2%            | Higher             |
| -Origin       | CS        | Comprehensiveness | 60.8%    | 60.8%            | Higher             |
| -Origin       | Legal     | Comprehensiveness | 83.6%    | 83.6%            | Higher             |
| -Origin       | Mix       | Comprehensiveness | 55.6%    | 55.6%            | Higher             |
| -Origin       | Agriculture | Diversity       | 73.6%    | 73.6%            | Higher             |
| -Origin       | CS        | Diversity       | 55.2%    | 55.2%            | Higher             |
| -Origin       | Legal     | Diversity       | 85.6%    | 85.6%            | Higher             |
| -Origin       | Mix       | Diversity       | 74.4%    | 74.4%            | Higher             |
| -Origin       | Agriculture | Empowerment   | 68.0%    | 68.0%            | Higher             |
| -Origin       | CS        | Empowerment   | 56.8%    | 56.8%            | Higher             |
| -Origin       | Legal     | Empowerment   | 82.8%    | 82.8%            | Higher             |
| -Origin       | Mix       | Empowerment   | 54.8%    | 54.8%            | Higher             |
| -Origin       | Agriculture | Overall       | 74.4%    | 74.4%            | Higher             |
| -Origin       | CS        | Overall       | 60.8%    | 60.8%            | Higher             |
| -Origin       | Legal     | Overall       | 84.4%    | 84.4%            | Higher             |
| -Origin       | Mix       | Overall       | 55.6%    | 55.6%            | Higher             |

The ablated versions of LightRAG show consistent improvements over NaiveRAG in most datasets and metrics. For instance, the -High variant, which removes high-order retrieval, still performs better than NaiveRAG in all datasets and metrics, indicating that even the low-level retrieval alone is effective [1]. The -Low variant, which removes low-level retrieval, also outperforms NaiveRAG in most metrics, though it shows a slight drop in the Mix dataset for Empowerment and Overall metrics [1]. The -Origin variant, which uses semantic graph without original text, performs well across all datasets and metrics, with notable improvements in Agriculture and Mix datasets [1]. The -High variant, however, experiences a significant performance decline compared to the full version of LightRAG, highlighting the importance of combining both low-level and high-level retrieval for comprehensive and detailed information retrieval [6].
```

## B4b-Q3-2

- 問題：`Performance of ablated versions of LightRAG`；模式 `navigate`；73.3 秒；2 次呼叫；tokens 7405
- 來源：[1] p8 retrieval, [2] p7 retrieval, [3] p1 retrieval, [4] p8 retrieval, [5] p1 retrieval, [6] p8 table_context
- 閱讀計畫（定位 6/6，保留 0，超預算 0）：
  - ✓ Section 4.3 ABLATION STUDIES (RQ2) | need: overview of ablation studies | priority: required | status: covered → 候選 0，納入 []，排除 []
  - ✓ Table 2 | need: performance metrics of ablated versions | priority: required | status: covered → 候選 0，納入 []，排除 []
  - ✓ Section 4.4 CASE STUDY (RQ3) | need: case study context on ablated versions | priority: supplementary | status: covered → 候選 0，納入 []，排除 []
  - ✓ Section 7.4 CASE STUDY: COMPARISON BETWEEN LIGHT RAG AND THE BASELINE NAIVE RAG | need: additional case study details | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
  - ✓ Table 5 | need: case study comparison data | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
  - ✓ Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM | need: methodological basis for ablation | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
- 分析狀態：SUPPORTED_AND_COMPLETE；完整性 complete（required ['-High', '-Low', '-Origin', 'LightRAG']，缺 []，條件 Agriculture / Comprehensiveness）；方向核對 []
- 修正：[]；刪除 ['Overall, LightRAG scores 60.0% for Mix, higher than NaiveRAG at 40.0%, NaiveRAG -High at 57.6%, NaiveRAG -Low at 64.8%, and NaiveRAG -Origin at 55.6% [1].', 'Empowerment for Mix is 57.2% for LightRAG, higher than NaiveRAG at 42.8%, NaiveRAG -High at 52.4%, NaiveRAG -Low at 64.8%, and NaiveRAG -Origin at 54.8%.', 'Diversity for Mix is 67.6% for LightRAG, higher than NaiveRAG at 32.4%, NaiveRAG -High at 64.0%, NaiveRAG -Low at 66.8%, and NaiveRAG -Origin at 74.4%.', 'In the Mix dataset, LightRAG scores 61.2% for Comprehensiveness, higher than NaiveRAG at 38.8%, NaiveRAG -High at 59.6%, NaiveRAG -Low at 64.0%, and NaiveRAG -Origin at 55.6%.', 'Overall, LightRAG scores 84.8% for Legal, higher than NaiveRAG at 15.2%, NaiveRAG -High at 78.0%, NaiveRAG -Low at 81.2%, and NaiveRAG -Origin at 84.4% [1].', 'Empowerment for Legal is 83.6% for LightRAG, higher than NaiveRAG at 16.4%, NaiveRAG -High at 77.2%, NaiveRAG -Low at 83.6%, and NaiveRAG -Origin at 82.8%.', 'Diversity for Legal is 86.4% for LightRAG, higher than NaiveRAG at 13.6%, NaiveRAG -High at 83.2%, NaiveRAG -Low at 86.4%, and NaiveRAG -Origin at 85.6%.', 'For the Legal dataset, LightRAG scores 83.6% for Comprehensiveness, higher than NaiveRAG at 16.4%, NaiveRAG -High at 76.4%, NaiveRAG -Low at 80.8%, and NaiveRAG -Origin at 83.6%.', 'Overall, LightRAG scores 61.2% for CS, higher than NaiveRAG at 38.8%, NaiveRAG -High at 56.0%, NaiveRAG -Low at 56.4%, and NaiveRAG -Origin at 60.8% [1].', 'Empowerment for CS is 61.2% for LightRAG, higher than NaiveRAG at 38.8%, NaiveRAG -High at 57.6%, NaieRAG -Low at 57.2%, and NaiveRAG -Origin at 56.8%.', 'Diversity for CS is 62.0% for LightRAG, higher than NaiveRAG at 38.0%, NaiveRAG -High at 63.2%, NaiveRAG -Low at 60.4%, and NaiveRAG -Origin at 55.2%.', 'In the CS dataset, LightRAG scores 61.6% for Comprehensiveness, higher than NaiveRAG at 38.4%, NaiveRAG -High at 57.2%, NaiveRAG -Low at 56.8%, and NaiveRAG -Origin at 60.8%.', 'Overall, LightRAG scores 67.6% for Agriculture, higher than NaiveRAG at 32.4%, NaiveRAG -High at 64.8%, NaiveRAG -Low at 65.2%, and NaiveRAG -Origin at 74.4% [1].', 'Empowerment for Agriculture is 67.6% for LightRAG, higher than NaiveRAG at 32.4%, NaiveRAG -High at 64.0%, NaiveRAG -Low at 65.2%, and NaiveRAG -Origin at 68.0%.', 'For the same dataset, Diversity is 76.4% for LightRAG, higher than NaiveRAG at 23.6%, NaiveRAG -High at 72.8%, NaiveRAG -Low at 72.0%, and NaiveRAG -Origin at 73.6%.']；仍不符 []；方向待定 []
- 涵蓋判定：Section 4.3 ABLATION STUDIES (RQ2)→covered；Table 2→covered；Section 4.4 CASE STUDY (RQ3)→partial；Section 7.4 CASE STUDY: COMPARISON BETWEEN LIGHT RAG AND THE BASELINE NAIVE RAG→missing；Table 5→missing；Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM→missing；required 未納入 []；supplementary 用 0；Matrix {'cells': 128, 'tables': ['Table 2 [1]'], 'definitions': ['LightRAG', 'NaiveRAG', '-High']}
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 4；找不到的數字 []

```text
The question asks for the performance of ablated versions of LightRAG, comparing the metrics (Comprehensiveness, Diversity, Empowerment, Overall) across different datasets (Agriculture, CS, Legal, Mix) and variants (NaiveRAG -High, NaiveRAG -Low, NaiveRAG -Origin, LightRAG). The evidence matrix in Table 2 provides the required data [1].

The ablated versions of LightRAG include NaiveRAG -High, NaiveRAG -Low, and NaiveRAG -Origin. The -High variant removes high-order retrieval, leading to a significant performance decline across nearly all datasets and metrics. The -Low variant removes low-level retrieval, prioritizing broader content but reducing depth. The -Origin variant eliminates the use of original text, retaining only the semantic graph. LightRAG is the full version, combining both low-level and high-level retrieval [6].

Comparing the Comprehensiveness metric for the Agriculture dataset, LightRAG scores 67.6%, outperforming NaiveRAG at 32.4%, NaiveRAG -High at 65.2%, NaiveRAG -Low at 64.0%, and NaiveRAG -Origin at 75.2%. The -High variant shows a significant performance drop compared to LightRAG, especially in Comprehensiveness and Diversity metrics. The -Low variant performs better in some metrics but worse in others, indicating a trade-off between breadth and depth. The -Origin variant, which uses only the semantic graph, performs comparably to or slightly better than LightRAG in some cases, suggesting that the graph-based indexing process is effective in extracting key information [6].
```

## B4b-Q3-3

- 問題：`Performance of ablated versions of LightRAG`；模式 `navigate`；71.8 秒；2 次呼叫；tokens 7367
- 來源：[1] p8 retrieval, [2] p7 retrieval, [3] p1 retrieval, [4] p8 retrieval, [5] p1 retrieval, [6] p8 table_context
- 閱讀計畫（定位 6/6，保留 0，超預算 0）：
  - ✓ Section 4.3 ABLATION STUDIES (RQ2) | need: overview of ablation studies | priority: required | status: missing → 候選 0，納入 []，排除 []
  - ✓ Table 2 | need: performance metrics of ablated versions | priority: required | status: covered → 候選 0，納入 []，排除 []
  - ✓ Section 4.4 CASE STUDY (RQ3) | need: case study on ablated variants | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
  - ✓ Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM | need: description of retrieval paradigm | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
  - ✓ Section 7.3.1 PROMPTS FOR GRAPH GENERATION | need: prompts used in ablated versions | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
  - ✓ Section 7.3.2 PROMPTS FOR QUERY GENERATION | need: prompts used in ablated versions | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
- 分析狀態：SUPPORTED_AND_COMPLETE；完整性 complete（required ['-High', '-Low', '-Origin', 'LightRAG']，缺 []，條件 Agriculture / Comprehensiveness）；方向核對 []
- 修正：[]；刪除 []；仍不符 []；方向待定 []
- 涵蓋判定：Section 4.3 ABLATION STUDIES (RQ2)→covered；Table 2→covered；Section 4.4 CASE STUDY (RQ3)→partial；Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM→missing；Section 7.3.1 PROMPTS FOR GRAPH GENERATION→missing；Section 7.3.2 PROMPTS FOR QUERY GENERATION→missing；required 未納入 []；supplementary 用 0；Matrix {'cells': 128, 'tables': ['Table 2 [1]'], 'definitions': ['LightRAG', 'NaiveRAG', '-High']}
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 16；找不到的數字 []

```text
The question asks for the performance of ablated versions of LightRAG, comparing different variants (NaiveRAG, -High, -Low, -Origin) across the datasets (Agriculture, CS, Legal, Mix) and metrics (Comprehensiveness, Diversity, Empowerment, Overall).

From Table 2, we observe the following performance metrics for each variant and metric:

| Variant        | Dataset   | Metric         | LightRAG | -High   | -Low    | -Origin |
|----------------|-----------|----------------|----------|---------|---------|---------|
| Agriculture    | Comp.     | 67.6% [1]      | 65.2% [1] | 64.0% [1] | 75.2% [1] |
| Agriculture    | Div.      | 76.4% [1]      | 72.8% [1] | 72.0% [1] | 73.6% [1] |
| Agriculture    | Emp.      | 67.6% [1]      | 64.0% [1] | 65.2% [1] | 68.0% [1] |
| Agriculture    | Overall   | 67.6% [1]      | 64.8% [1] | 65.2% [1] | 74.4% [1] |
| CS             | Comp.     | 61.6% [1]      | 57.2% [1] | 56.8% [1] | 60.8% [1] |
| CS             | Div.      | 62.0% [1]      | 63.2% [1] | 60.4% [1] | 55.2% [1] |
| CS             | Emp.      | 61.2% [1]      | 57.6% [1] | 57.2% [1] | 56.8% [1] |
| CS             | Overall   | 61.2% [1]      | 56.0% [1] | 56.4% [1] | 60.8% [1] |
| Legal          | Comp.     | 83.6% [1]      | 76.4% [1] | 80.8% [1] | 83.6% [1] |
| Legal          | Div.      | 86.4% [1]      | 83.2% [1] | 86.4% [1] | 85.6% [1] |
| Legal          | Emp.      | 83.6% [1]      | 77.2% [1] | 83.6% [1] | 82.8% [1] |
| Legal          | Overall   | 84.8% [1]      | 78.0% [1] | 81.2% [1] | 84.4% [1] |
| Mix            | Comp.     | 61.2% [1]      | 59.6% [1] | 64.0% [1] | 55.6% [1] |
| Mix            | Div.      | 67.6% [1]      | 64.0% [1] | 66.8% [1] | 74.4% [1] |
| Mix            | Emp.      | 57.2% [1]      | 52.4% [1] | 64.8% [1] | 54.8% [1] |
| Mix            | Overall   | 60.0% [1]      | 57.6% [1] | 64.8% [1] | 55.6% [1] |

The ablated versions of LightRAG exhibit varying performance across datasets and metrics. The -High variant, which removes high-order retrieval, shows a significant performance decline across nearly all datasets and metrics compared to LightRAG [6]. For example, in the Agriculture dataset, the -High variant has a Comprehensiveness of 65.2% compared to LightRAG’s 67.6% [1]. Similarly, in the CS dataset, the -High variant has a Comprehensiveness of 57.2% compared to LightRAG’s 61.6% [1].

The -Low variant, which prioritizes capturing a broader range of content by leveraging entity-wise relationships, shows mixed performance. It performs better than -High in some metrics but worse than LightRAG in most. For example, in the Agriculture dataset, the -Low variant has a Comprehensiveness of 64.0% compared to LightRAG’s 67.6% [1]. In the Legal dataset, it performs better than -High in Comprehensiveness but slightly worse than LightRAG [1].

The -Origin variant, which eliminates the use of original text in the retrieval process, surprisingly does not exhibit significant performance declines and even shows improvements in some cases. For example, in the Agriculture dataset, the -Origin variant has a Comprehensiveness of 75.2% compared to LightRAG’s 67.6% [1]. In the Mix dataset, it has an Overall score of 55.6% compared to LightRAG’s 60.0% [1].

The -Origin variant’s performance is attributed to the effective extraction of key information during the graph-based indexing process, which provides sufficient context for answering queries [6]. However, it is important to note that the original text often contains irrelevant information that can introduce noise in the response [6].

In conclusion, the ablated versions of LightRAG exhibit varying performance across different datasets and metrics. The -High variant shows significant performance declines, the -Low variant shows mixed results, and the -Origin variant performs comparably to or better than LightRAG in some cases. The hybrid mode, or the full version of LightRAG, combines the strengths of both low-level and high-level retrieval methods, ensuring balanced performance across multiple dimensions [6].
```

## C-Q3-1

- 問題：`Performance of ablated versions of LightRAG`；模式 `single`；20.4 秒；1 次呼叫；tokens 4100
- 來源：[1] p8 retrieval, [2] p7 retrieval, [3] p1 retrieval, [4] p8 retrieval, [5] p1 retrieval, [6] p8 table_context
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 [([1], [2])]；未解析 0；找不到的數字 []

```text
The ablated versions of LightRAG were analyzed to evaluate the impact of the dual-level retrieval paradigm and the effectiveness of the graph-based text indexing. The results, as presented in Table 2, show the performance of different variants: NaiveRAG -High, NaiveRAG -Low, and NaiveRAG -Origin, each omitting one module of the full LightRAG system [1].

1. **Low-level-only Retrieval (-High variant)**: This variant removes high-order retrieval and experiences a significant performance decline across nearly all datasets and metrics. The focus on specific information and entities leads to an inability to gather comprehensive insights for complex queries [6].

2. **High-level-only Retrieval (-Low variant)**: This variant prioritizes a broader range of content by leveraging entity-wise relationships rather than focusing on specific entities. While this approach offers an advantage in comprehensiveness, it sacrifices depth in examining specific entities, limiting its ability to provide highly detailed insights [6].

3. **Semantic Graph-based Retrieval (-Origin variant)**: The variant that eliminates the use of original text in the retrieval process does not show significant performance declines across all four datasets. Surprisingly, it even shows improvements in some cases, such as in Agriculture and Mix. This is attributed to the effective extraction of key information during the graph-based indexing process, which provides sufficient context for answering queries and avoids noise from irrelevant information in the original text [6].

4. **Hybrid Mode (Full LightRAG)**: The full version of LightRAG combines the strengths of both low-level and high-level retrieval methods. It retrieves a broader set of relationships while simultaneously conducting an in-depth exploration of specific entities. This dual-level approach ensures both breadth in the retrieval process and depth in the analysis, providing a balanced performance across multiple dimensions [6]. 

Overall, these ablation studies highlight the importance of the dual-level retrieval system and the graph-based indexing in the performance of LightRAG [2].
```

## C-Q3-2

- 問題：`Performance of ablated versions of LightRAG`；模式 `single`；20.4 秒；1 次呼叫；tokens 4178
- 來源：[1] p8 retrieval, [2] p7 retrieval, [3] p1 retrieval, [4] p8 retrieval, [5] p1 retrieval, [6] p8 table_context
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
The performance of ablated versions of LightRAG was evaluated using NaiveRAG as a reference. The ablated models include variants that omit either low-level or high-level retrieval modules, as well as a variant that uses only the semantic graph representation without the original text. The results are presented in Table 2 of the document [1].

1. **Low-level-only Retrieval (LightRAG -High)**: This variant removes high-level retrieval and shows a significant performance decline across nearly all datasets and metrics. The drop is mainly due to an overemphasis on specific information, focusing excessively on entities and their immediate neighbors. While this approach enables deeper exploration of directly related entities, it struggles with complex queries that require comprehensive insights [6].

2. **High-level-only Retrieval (LightRAG -Low)**: This variant prioritizes capturing a broader range of content by leveraging entity-wise relationships. It offers a significant advantage in comprehensiveness but has reduced depth in examining specific entities. This trade-off limits its ability to provide highly detailed insights, making it less suitable for tasks requiring precise answers [6].

3. **Semantic Graph-only Retrieval (LightRAG -Origin)**: This variant eliminates the use of original text in the retrieval process. Surprisingly, it does not exhibit significant performance declines across all four datasets and even shows improvements in some cases (e.g., Agriculture and Mix). This is attributed to the effective extraction of key information during the graph-based indexing process, which provides sufficient context for answering queries. Additionally, the original text often contains irrelevant information that can introduce noise in the response [6].

4. **Hybrid Mode (Full LightRAG)**: The hybrid mode combines the strengths of both low-level and high-level retrieval methods. It retrieves a broader set of relationships while simultaneously conducting an in-depth exploration of specific entities. This dual-level approach ensures both breadth in the retrieval process and depth in the analysis, providing a comprehensive view of the data. As a result, LightRAG achieves balanced performance across multiple dimensions [6].

In summary, the ablation studies demonstrate that the full version of LightRAG, with its dual-level retrieval system, outperforms the ablated variants in most cases. The semantic graph-only variant, however, shows surprising robustness in some scenarios, suggesting that the graph-based indexing effectively captures key information for query answering [6].
```

## C-Q3-3

- 問題：`Performance of ablated versions of LightRAG`；模式 `single`；16.2 秒；1 次呼叫；tokens 4077
- 來源：[1] p8 retrieval, [2] p7 retrieval, [3] p1 retrieval, [4] p8 retrieval, [5] p1 retrieval, [6] p8 table_context
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
The performance of ablated versions of LightRAG is analyzed in the study, with results summarized in Table 2 [1]. The ablated models include variants that remove either the low-level or high-level retrieval modules, as well as a variant that uses semantic graphs instead of the original text for retrieval.

1. **Low-level-only Retrieval (LightRAG -High)**: Removing high-level retrieval leads to a significant performance decline across nearly all datasets and metrics. This variant emphasizes specific information about entities and their immediate neighbors, which allows for deeper exploration of directly related entities. However, it struggles with complex queries that require comprehensive insights [6].

2. **High-level-only Retrieval (LightRAG -Low)**: This variant prioritizes capturing broader content by leveraging entity-wise relationships. It performs well in terms of comprehensiveness but shows reduced depth in examining specific entities. As a result, it may struggle with tasks requiring precise, detailed answers [6].

3. **Hybrid Mode (Full LightRAG)**: The hybrid mode combines the strengths of both low-level and high-level retrieval methods. It retrieves a broader set of relationships while also conducting in-depth exploration of specific entities. This dual-level approach ensures balanced performance across multiple dimensions [6].

4. **Semantic Graph Retrieval (LightRAG -Origin)**: This variant eliminates the use of original text in the retrieval process. Surprisingly, it does not exhibit significant performance declines across all four datasets. In some cases, such as the Agriculture and Mix datasets, it even shows improvements. The graph-based indexing process effectively extracts key information, providing sufficient context for answering queries. Additionally, the original text often contains irrelevant information that can introduce noise in responses [6].

These findings highlight the importance of the dual-level retrieval paradigm in LightRAG, which contributes to its overall performance improvements compared to ablated versions [2].
```

## A-G1-1

- 問題：`How many context units and tokens do the root-level community summaries (C0) and the source-text summarization (TS) use on the Podcast and News datasets?`；模式 `roles`；11.0 秒；1 次呼叫；tokens 3670
- 來源：[1] p10 retrieval, [2] p10 retrieval, [3] p8 retrieval, [4] p10 retrieval, [5] p11 retrieval, [6] p11 table_context, [7] p11 table_context
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
Navigator: The relevant sections for the question are Table 2 (page 10) which provides data on the number of context units and corresponding token counts for different conditions including C0 and TS on the Podcast and News datasets.

Analyst: On the Podcast dataset, root-level community summaries (C0) use 34 context units and source-text summarization (TS) uses 1669 context units. Correspondingly, C0 requires 26,657 tokens while TS requires 1,014,611 tokens. On the News dataset, C0 uses 55 context units and TS uses 3197 context units. The token counts for C0 and TS on the News dataset are 39,770 and 1,707,694, respectively [1].
```

## A-G1-2

- 問題：`How many context units and tokens do the root-level community summaries (C0) and the source-text summarization (TS) use on the Podcast and News datasets?`；模式 `roles`；7.3 秒；1 次呼叫；tokens 3659
- 來源：[1] p10 retrieval, [2] p10 retrieval, [3] p8 retrieval, [4] p10 retrieval, [5] p11 retrieval, [6] p11 table_context, [7] p11 table_context
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
Navigator: The relevant parts are Table 2 on page 10, which provides the number of context units and tokens for different conditions including C0 and TS for both the Podcast and News datasets.

Analyst: For the Podcast dataset, root-level community summaries (C0) use 34 context units and 26,657 tokens, whereas source-text summarization (TS) uses 1,669 context units and 1,014,611 tokens. For the News dataset, root-level community summaries (C0) use 55 context units and 39,770 tokens, and source-text summarization (TS) uses 3,197 context units and 1,707,694 tokens [1].
```

## A-G1-3

- 問題：`How many context units and tokens do the root-level community summaries (C0) and the source-text summarization (TS) use on the Podcast and News datasets?`；模式 `roles`；9.3 秒；1 次呼叫；tokens 3709
- 來源：[1] p10 retrieval, [2] p10 retrieval, [3] p8 retrieval, [4] p10 retrieval, [5] p11 retrieval, [6] p11 table_context, [7] p11 table_context
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
Navigator: The question is about the number of context units and tokens used by root-level community summaries (C0) and source-text summarization (TS) on the Podcast and News datasets. The relevant section is Table 2, which provides the number of context units and tokens for different conditions and datasets [1].

Analyst: The root-level community summaries (C0) and source-text summarization (TS) use the following context units and tokens on the Podcast and News datasets:

- **Podcast Transcripts**:
  - **C0**: 34 context units, 26,657 tokens [1].
  - **TS**: 1,669 context units, 1,014,611 tokens [1].
- **News Articles**:
  - **C0**: 55 context units, 39,770 tokens [1].
  - **TS**: 3,197 context units, 1,707,694 tokens [1].
```

## B-G1-1

- 問題：`How many context units and tokens do the root-level community summaries (C0) and the source-text summarization (TS) use on the Podcast and News datasets?`；模式 `navigate`；24.7 秒；2 次呼叫；tokens 7045
- 來源：[1] p10 retrieval, [2] p10 retrieval, [3] p8 retrieval, [4] p10 retrieval, [5] p11 retrieval, [6] p11 table_context, [7] p11 table_context, [8] p10 navigation, [9] p10 navigation, [10] p10 navigation, [11] p4 navigation, [12] p4 navigation, [13] p5 navigation
- 閱讀計畫（定位 6/6，保留 8，超預算 7）：
  - ✓ Table 2 (page 10): Number of context units (community summaries for C0-C3 and text chunks for TS), corre-
  - ✓ Section: Methods (pages 4-8): Corpus division into text chunks and token overlaps
  - ✓ Table 1 (page 7): Examples of potential users, tasks, and questions generated by the LLM based
  - ✓ Page 10 (source [2]): For root-level summaries. Intermediate-level summaries in the Podcast dataset an
  - ✓ Page 10 (source [1]): Token count. Map-reduce summarization of source texts is the most resource-inten
  - ✓ Page 8 (source [3]): Corpus was divided into 1669 × 600-token text chunks, with 100-token overlaps be
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 ['38.5', '58.1']

```text
For the Podcast and News datasets, the root-level community summaries (C0) and source-text summarization (TS) use the following context units and tokens:

- **Podcast Transcripts**:
  - **C0 (Root-level community summaries)**:
    - Context units: 34
    - Tokens: 26,657
  - **TS (Source-text summarization)**:
    - Context units: 1,669
    - Tokens: 1,014,611
  - This results in a significant difference, with TS requiring 38.5x more context units and 38x more tokens than C0 [4].

- **News Articles**:
  - **C0 (Root-level community summaries)**:
    - Context units: 55
    - Tokens: 39,770
  - **TS (Source-text summarization)**:
    - Context units: 3,197
    - Tokens: 1,707,694
  - This results in a significant difference, with TS requiring 58.1x more context units and 43x more tokens than C0 [4].

Numbers that could not be checked against the cited pages of the original text: 38.5, 58.1.
```

## B-G1-2

- 問題：`How many context units and tokens do the root-level community summaries (C0) and the source-text summarization (TS) use on the Podcast and News datasets?`；模式 `navigate`；21.2 秒；2 次呼叫；tokens 6966
- 來源：[1] p10 retrieval, [2] p10 retrieval, [3] p8 retrieval, [4] p10 retrieval, [5] p11 retrieval, [6] p11 table_context, [7] p11 table_context, [8] p10 navigation, [9] p10 navigation, [10] p10 navigation, [11] p4 navigation, [12] p4 navigation, [13] p5 navigation
- 閱讀計畫（定位 6/6，保留 8，超預算 10）：
  - ✓ Table 2 (page 10): Provides the number of context units for C0 and TS conditions across datasets.
  - ✓ Section: Methods (pages 4-8): Explains how source texts are divided into tokens and overlaps.
  - ✓ Table 1 (page 7): May reference potential user tasks and conditions including C0 and TS.
  - ✓ Section: Results (pages 9-11): Likely includes details on token counts and context units for different conditions.
  - ✓ [3] 2404.16130v2.pdf, page 8: Mentions token chunks and overlaps relevant to TS.
  - ✓ [1] 2404.16130v2.pdf, page 10: Refers to context units and resource intensity for root-level summaries.
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
The root-level community summaries (C0) and the source-text summarization (TS) use the following context units and tokens on the Podcast and News datasets:

- **Podcast Transcripts**:
  - **C0 (Root-level community summaries)**: 34 context units and 26,657 tokens.
  - **TS (Source-text summarization)**: 1,669 context units and 1,014,611 tokens [1].

- **News Articles**:
  - **C0 (Root-level community summaries)**: 55 context units and 39,770 tokens.
  - **TS (Source-text summarization)**: 3,197 context units and 1,707,694 tokens [1].
```

## B-G1-3

- 問題：`How many context units and tokens do the root-level community summaries (C0) and the source-text summarization (TS) use on the Podcast and News datasets?`；模式 `navigate`；20.2 秒；2 次呼叫；tokens 6936
- 來源：[1] p10 retrieval, [2] p10 retrieval, [3] p8 retrieval, [4] p10 retrieval, [5] p11 retrieval, [6] p11 table_context, [7] p11 table_context, [8] p10 navigation, [9] p10 navigation, [10] p10 navigation, [11] p4 navigation, [12] p4 navigation, [13] p5 navigation
- 閱讀計畫（定位 6/6，保留 8，超預算 10）：
  - ✓ Table 2 (page 10): Provides the number of context units for C0 and TS across datasets.
  - ✓ Section: Methods (pages 4-8): Explains how text chunks and tokens were processed, relevant for understanding context unit definitions.
  - ✓ Figure 2 (page 10): May provide comparative context for C0 and TS in different datasets.
  - ✓ Section: Results (pages 9-11): Likely contains data on the use of tokens and context units in different conditions.
  - ✓ Table 1 (page 7): May clarify the nature of context units used in different conditions.
  - ✓ [3] 2404.16130v2.pdf, page 8: Mentions token chunk sizes and overlaps, relevant for understanding token counts.
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
The root-level community summaries (C0) and the source-text summarization (TS) use the following context units and tokens on the Podcast and News datasets:

- **Podcast Transcripts:**
  - **C0:** 34 context units, 26,657 tokens [1].
  - **TS:** 1,669 context units, 1,014,611 tokens [1].

- **News Articles:**
  - **C0:** 55 context units, 39,770 tokens [1].
  - **TS:** 3,197 context units, 1,707,694 tokens [1].
```

## B2-G1-1

- 問題：`How many context units and tokens do the root-level community summaries (C0) and the source-text summarization (TS) use on the Podcast and News datasets?`；模式 `navigate`；22.9 秒；2 次呼叫；tokens 7697
- 來源：[1] p10 retrieval, [2] p10 retrieval, [3] p8 retrieval, [4] p10 retrieval, [5] p11 retrieval, [6] p11 table_context, [7] p11 table_context, [8] p8 navigation, [9] p8 navigation, [10] p9 navigation, [11] p10 navigation, [12] p9 navigation, [13] p10 navigation, [14] p10 navigation
- 閱讀計畫（定位 6/6，保留 7，超預算 0）：
  - ✓ Section 4.1.1 Datasets | need: dataset descriptions | priority: required | status: missing → 候選 2，納入 [20]，排除 [(21, 'already among the retrieved sources')]
  - ✓ Section 4.1.2 Conditions | need: text chunking details | priority: required | status: covered → 候選 2，納入 [22]，排除 [(21, 'already among the retrieved sources')]
  - ✓ Section 5.1 Experiment 1 | need: context unit counts for C0 and TS | priority: required | status: missing → 候選 9，納入 [27]，排除 [(30, 'already among the retrieved sources'), (29, 'already among the retrieved sources'), (32, 'already among the retrieved sources'), (31, 'already among the retrieved sources'), (25, 'already selected for another target'), (26, 'already selected for another target'), (24, 'already selected for another target'), (28, 'already selected for another target')]
  - ✓ Section 5.1 Experiment 1 | need: token usage for C0 and TS | priority: required | status: missing → 候選 9，納入 [26, 28]，排除 [(30, 'already among the retrieved sources'), (29, 'already among the retrieved sources'), (32, 'already among the retrieved sources'), (31, 'already among the retrieved sources'), (25, 'already selected for another target'), (24, 'already selected for another target'), (27, 'already selected for another target')]
  - ✓ Table 2 | need: context unit numbers by condition | priority: required | status: missing → 候選 3，納入 []，排除 [(29, 'already among the retrieved sources'), (30, 'already among the retrieved sources'), (31, 'already among the retrieved sources')]
  - ✓ Section 5.1 Experiment 1 | need: mention of Podcast and News datasets | priority: supplementary | status: missing → 候選 9，納入 [25, 24]，排除 [(27, 'low relevance'), (28, 'low relevance'), (30, 'already among the retrieved sources'), (31, 'already among the retrieved sources'), (32, 'already among the retrieved sources'), (29, 'already among the retrieved sources'), (26, 'already selected for another target')]
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
The root-level community summaries (C0) and the source-text summarization (TS) use the following context units and tokens on the Podcast and News datasets:

- **Podcast Transcripts**:
  - **C0 (Root-level community summaries)**:
    - Context Units: 34
    - Tokens: 26,657
  - **TS (Source-text summarization)**:
    - Context Units: 1,669
    - Tokens: 1,014,611
[1]

- **News Articles**:
  - **C0 (Root-level community summaries)**:
    - Context Units: 55
    - Tokens: 39,770
  - **TS (Source-text summarization)**:
    - Context Units: 3,197
    - Tokens: 1,707,694
[1]
```

## B2-G1-2

- 問題：`How many context units and tokens do the root-level community summaries (C0) and the source-text summarization (TS) use on the Podcast and News datasets?`；模式 `navigate`；22.3 秒；2 次呼叫；tokens 7720
- 來源：[1] p10 retrieval, [2] p10 retrieval, [3] p8 retrieval, [4] p10 retrieval, [5] p11 retrieval, [6] p11 table_context, [7] p11 table_context, [8] p7 navigation, [9] p6 navigation, [10] p8 navigation, [11] p7 navigation, [12] p6 navigation, [13] p8 navigation, [14] p10 navigation
- 閱讀計畫（定位 6/6，保留 8，超預算 6）：
  - ✓ Section 4.1.2 Conditions | need: dataset descriptions | priority: required | status: covered → 候選 2，納入 [22]，排除 [(21, 'already among the retrieved sources')]
  - ✓ Section 5.1 Experiment 1 | need: context units for C0 and TS | priority: required | status: missing → 候選 9，納入 [25]，排除 [(30, 'already among the retrieved sources'), (29, 'already among the retrieved sources'), (32, 'already among the retrieved sources'), (31, 'already among the retrieved sources'), (26, 'already selected for another target'), (28, 'over the evidence budget'), (24, 'over the evidence budget'), (27, 'over the evidence budget')]
  - ✓ Table 2 | need: context units for C0 and TS | priority: required | status: missing → 候選 3，納入 []，排除 [(29, 'already among the retrieved sources'), (30, 'already among the retrieved sources'), (31, 'already among the retrieved sources')]
  - ✓ Section 5.1 Experiment 1 | need: token usage for C0 and TS | priority: required | status: missing → 候選 9，納入 [26]，排除 [(30, 'already among the retrieved sources'), (29, 'already among the retrieved sources'), (32, 'already among the retrieved sources'), (31, 'already among the retrieved sources'), (25, 'already selected for another target'), (28, 'over the evidence budget'), (24, 'over the evidence budget'), (27, 'over the evidence budget')]
  - ✓ Table 1 | need: task descriptions | priority: supplementary | status: missing → 候選 3，納入 [18, 19, 20]，排除 []
  - ✓ Section 3.1.5 Graph Communities → Community Summaries | need: summary level definitions | priority: supplementary | status: missing → 候選 2，納入 [16, 15]，排除 []
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
The root-level community summaries (C0) and the source-text summarization (TS) use the following context units and tokens on the Podcast and News datasets:

- **Podcast Transcripts:**
  - **C0 (Root-level community summaries):**
    - Units: 34
    - Tokens: 26,657
  - **TS (Source-text summarization):**
    - Units: 1,669
    - Tokens: 1,014,611 [1]

- **News Articles:**
  - **C0 (Root-level community summaries):**
    - Units: 34
    - Tokens: 39,770
  - **TS (Source-text summarization):**
    - Units: 3,197
    - Tokens: 1,707,694 [1]
```

## B2-G1-3

- 問題：`How many context units and tokens do the root-level community summaries (C0) and the source-text summarization (TS) use on the Podcast and News datasets?`；模式 `navigate`；22.3 秒；2 次呼叫；tokens 7605
- 來源：[1] p10 retrieval, [2] p10 retrieval, [3] p8 retrieval, [4] p10 retrieval, [5] p11 retrieval, [6] p11 table_context, [7] p11 table_context, [8] p7 navigation, [9] p8 navigation, [10] p7 navigation, [11] p8 navigation, [12] p10 navigation, [13] p9 navigation, [14] p10 navigation
- 閱讀計畫（定位 6/6，保留 8，超預算 1）：
  - ✓ Section 4.1.2 Conditions | need: dataset descriptions | priority: required | status: covered → 候選 2，納入 [22]，排除 [(21, 'already among the retrieved sources')]
  - ✓ Section 5.1 Experiment 1 | need: context units for C0 and TS | priority: required | status: missing → 候選 9，納入 [24]，排除 [(30, 'already among the retrieved sources'), (29, 'already among the retrieved sources'), (32, 'already among the retrieved sources'), (31, 'already among the retrieved sources'), (26, 'already selected for another target'), (25, 'already selected for another target'), (28, 'already selected for another target'), (27, 'over the evidence budget')]
  - ✓ Table 2 | need: context units by condition | priority: required | status: missing → 候選 3，納入 []，排除 [(29, 'already among the retrieved sources'), (30, 'already among the retrieved sources'), (31, 'already among the retrieved sources')]
  - ✓ Section 5.1 Experiment 1 | need: token counts for C0 and TS | priority: required | status: covered → 候選 9，納入 [26, 25, 28]，排除 [(30, 'already among the retrieved sources'), (29, 'already among the retrieved sources'), (32, 'already among the retrieved sources'), (31, 'already among the retrieved sources'), (24, 'target quota reached'), (27, 'target quota reached')]
  - ✓ Section 4.1.1 Datasets | need: dataset specifics | priority: supplementary | status: missing → 候選 2，納入 [20]，排除 [(21, 'already among the retrieved sources')]
  - ✓ Table 1 | need: example user tasks | priority: supplementary | status: missing → 候選 3，納入 [18, 19]，排除 [(20, 'already selected for another target')]
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
The root-level community summaries (C0) and the source-text summarization (TS) use the following context units and tokens on the Podcast and News datasets:

- **Podcast Transcripts:**
  - **C0 (Root-level community summaries):**
    - Units: 34
    - Tokens: 26,657
  - **TS (Source-text summarization):**
    - Units: 1,669
    - Tokens: 1,014,611

- **News Articles:**
  - **C0 (Root-level community summaries):**
    - Units: 34
    - Tokens: 39,770
  - **TS (Source-text summarization):**
    - Units: 3,197
    - Tokens: 1,707,694

These values are provided in Table 2 of the document [1].
```

## B3-G1-1

- 問題：`How many context units and tokens do the root-level community summaries (C0) and the source-text summarization (TS) use on the Podcast and News datasets?`；模式 `navigate`；26.9 秒；2 次呼叫；tokens 8033
- 來源：[1] p10 retrieval, [2] p10 retrieval, [3] p8 retrieval, [4] p10 retrieval, [5] p11 retrieval, [6] p11 table_context, [7] p11 table_context, [8] p8 navigation, [9] p10 navigation, [10] p9 navigation, [11] p9 navigation, [12] p10 navigation, [13] p10 navigation, [14] p6 navigation
- 閱讀計畫（定位 6/6，保留 8，超預算 0）：
  - ✓ Section 4.1.2 Conditions | need: dataset details | priority: required | status: covered → 候選 2，納入 [22]，排除 [(21, 'already among the retrieved sources')]
  - ✓ Section 5.1 Experiment 1 | need: context units and tokens for C0 and TS | priority: required | status: missing → 候選 9，納入 [25, 24]，排除 [(30, 'already among the retrieved sources'), (29, 'already among the retrieved sources'), (32, 'already among the retrieved sources'), (31, 'already among the retrieved sources'), (26, 'already selected for another target'), (28, 'already selected for another target'), (27, 'already selected for another target')]
  - ✓ Table 2 | need: context units for C0 and TS | priority: required | status: missing → 候選 3，納入 []，排除 [(29, 'already among the retrieved sources'), (30, 'already among the retrieved sources'), (31, 'already among the retrieved sources')]
  - ✓ Section 5.1 Experiment 1 | need: tokens for C0 and TS | priority: required | status: missing → 候選 9，納入 [26, 28, 27]，排除 [(30, 'already among the retrieved sources'), (29, 'already among the retrieved sources'), (31, 'already among the retrieved sources'), (32, 'already among the retrieved sources'), (25, 'already selected for another target'), (24, 'target quota reached')]
  - ✓ Section 3.1.5 Graph Communities → Community Summaries | need: definition of root-level summaries | priority: supplementary | status: missing → 候選 2，納入 [15]，排除 [(16, 'supplementary cap reached')]
  - ✓ Section 3.1.1 Source Documents → Text Chunks | need: definition of source-text summarization | priority: supplementary | status: missing → 候選 1，納入 [11]，排除 []
- 分析狀態：UNCERTAIN；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 涵蓋判定：Section 4.1.2 Conditions→partial；Section 5.1 Experiment 1→partial；Table 2→partial；Section 5.1 Experiment 1→partial；Section 3.1.5 Graph Communities → Community Summaries→missing；Section 3.1.1 Source Documents → Text Chunks→missing；required 未納入 []；supplementary 用 2；Matrix {'cells': 0, 'tables': [], 'definitions': []}
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
The question asks for the number of context units and tokens used by root-level community summaries (C0) and source-text summarization (TS) on the Podcast and News datasets.

| Dataset         | Method | Context Units | Tokens     |
|-----------------|--------|---------------|------------|
| Podcast         | C0     | 34            | 26,657     |
| Podcast         | TS     | 1,669         | 1,014,611  |
| News            | C0     | 55            | 39,770     |
| News            | TS     | 3,197         | 1,707,694  |

Root-level community summaries (C0) use 34 context units and 26,657 tokens for the Podcast dataset [1]. In comparison, source-text summarization (TS) uses 1,669 context units and 1,014,611 tokens for the same dataset [1]. For the News dataset, C0 uses 55 context units and 39,770 tokens [1], while TS uses 3,197 context units and 1,707,694 tokens [1].
```

## B3-G1-2

- 問題：`How many context units and tokens do the root-level community summaries (C0) and the source-text summarization (TS) use on the Podcast and News datasets?`；模式 `navigate`；26.8 秒；2 次呼叫；tokens 8008
- 來源：[1] p10 retrieval, [2] p10 retrieval, [3] p8 retrieval, [4] p10 retrieval, [5] p11 retrieval, [6] p11 table_context, [7] p11 table_context, [8] p8 navigation, [9] p10 navigation, [10] p9 navigation, [11] p10 navigation, [12] p9 navigation, [13] p10 navigation, [14] p7 navigation
- 閱讀計畫（定位 6/6，保留 8，超預算 0）：
  - ✓ Section 4.1.2 Conditions | need: dataset descriptions | priority: required | status: covered → 候選 2，納入 [22]，排除 [(21, 'already among the retrieved sources')]
  - ✓ Section 5.1 Experiment 1 | need: context units for C0 and TS | priority: required | status: missing → 候選 9，納入 [25, 28, 24]，排除 [(30, 'already among the retrieved sources'), (29, 'already among the retrieved sources'), (32, 'already among the retrieved sources'), (31, 'already among the retrieved sources'), (26, 'already selected for another target'), (27, 'target quota reached')]
  - ✓ Table 2 | need: context units for C0 and TS | priority: required | status: missing → 候選 3，納入 []，排除 [(29, 'already among the retrieved sources'), (30, 'already among the retrieved sources'), (31, 'already among the retrieved sources')]
  - ✓ Section 5.1 Experiment 1 | need: token usage for C0 and TS | priority: required | status: missing → 候選 9，納入 [26, 27]，排除 [(30, 'already among the retrieved sources'), (29, 'already among the retrieved sources'), (32, 'already among the retrieved sources'), (31, 'already among the retrieved sources'), (25, 'already selected for another target'), (28, 'already selected for another target'), (24, 'already selected for another target')]
  - ✓ Section 4.1.2 Conditions | need: token chunking details | priority: supplementary | status: covered → 候選 2，納入 []，排除 [(21, 'already among the retrieved sources'), (22, 'supplementary cap reached')]
  - ✓ Table 1 | need: example user tasks | priority: supplementary | status: missing → 候選 3，納入 [18, 19]，排除 [(20, 'supplementary cap reached')]
- 分析狀態：UNCERTAIN；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 涵蓋判定：Section 4.1.2 Conditions→partial；Section 5.1 Experiment 1→partial；Table 2→partial；Section 5.1 Experiment 1→partial；Section 4.1.2 Conditions→partial；Table 1→missing；required 未納入 []；supplementary 用 2；Matrix {'cells': 0, 'tables': [], 'definitions': []}
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
The question asks for the number of context units and tokens used by the root-level community summaries (C0) and the source-text summarization (TS) on the Podcast and News datasets.

| Dataset           | Method | Context Units | Tokens   |
|-------------------|--------|----------------|----------|
| Podcast Transcripts | C0     | 34             | 26657    |
| Podcast Transcripts | TS     | 1669           | 1014611  |
| News Articles      | C0     | 55             | 39770    |
| News Articles      | TS     | 3197           | 1707694  |

From the data:
- For the Podcast Transcripts dataset, C0 uses 34 context units and 26,657 tokens, while TS uses 1,669 context units and 1,014,611 tokens [1].
- For the News Articles dataset, C0 uses 55 context units and 39,770 tokens, while TS uses 3,197 context units and 1,707,694 tokens [1].

These figures demonstrate that C0 requires significantly fewer context units and tokens compared to TS for both the Podcast Transcripts and News Articles datasets [1].
```

## B3-G1-3

- 問題：`How many context units and tokens do the root-level community summaries (C0) and the source-text summarization (TS) use on the Podcast and News datasets?`；模式 `navigate`；32.0 秒；2 次呼叫；tokens 8136
- 來源：[1] p10 retrieval, [2] p10 retrieval, [3] p8 retrieval, [4] p10 retrieval, [5] p11 retrieval, [6] p11 table_context, [7] p11 table_context, [8] p8 navigation, [9] p10 navigation, [10] p9 navigation, [11] p10 navigation, [12] p9 navigation, [13] p10 navigation, [14] p7 navigation
- 閱讀計畫（定位 6/6，保留 8，超預算 0）：
  - ✓ Section 4.1.2 Conditions | need: dataset descriptions | priority: required | status: covered → 候選 2，納入 [22]，排除 [(21, 'already among the retrieved sources')]
  - ✓ Section 5.1 Experiment 1 | need: context units for C0 and TS | priority: required | status: missing → 候選 9，納入 [25, 28, 24]，排除 [(30, 'already among the retrieved sources'), (29, 'already among the retrieved sources'), (32, 'already among the retrieved sources'), (31, 'already among the retrieved sources'), (26, 'already selected for another target'), (27, 'target quota reached')]
  - ✓ Section 5.1 Experiment 1 | need: token usage for C0 and TS | priority: required | status: missing → 候選 9，納入 [26, 27]，排除 [(30, 'already among the retrieved sources'), (29, 'already among the retrieved sources'), (32, 'already among the retrieved sources'), (31, 'already among the retrieved sources'), (25, 'already selected for another target'), (28, 'already selected for another target'), (24, 'already selected for another target')]
  - ✓ Table 2 | need: context units for C0 and TS | priority: required | status: missing → 候選 3，納入 []，排除 [(29, 'already among the retrieved sources'), (30, 'already among the retrieved sources'), (31, 'already among the retrieved sources')]
  - ✓ Section 5.1 Experiment 1 | need: dataset-specific context units | priority: supplementary | status: missing → 候選 9，納入 []，排除 [(28, 'low relevance'), (27, 'low relevance'), (30, 'already among the retrieved sources'), (29, 'supplementary cap reached'), (31, 'supplementary cap reached'), (32, 'supplementary cap reached'), (25, 'supplementary cap reached'), (24, 'supplementary cap reached'), (26, 'supplementary cap reached')]
  - ✓ Table 1 | need: task examples for context units | priority: supplementary | status: missing → 候選 3，納入 [18, 19]，排除 [(20, 'supplementary cap reached')]
- 分析狀態：UNCERTAIN；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 涵蓋判定：Section 4.1.2 Conditions→partial；Section 5.1 Experiment 1→partial；Section 5.1 Experiment 1→partial；Table 2→partial；Section 5.1 Experiment 1→partial；Table 1→missing；required 未納入 []；supplementary 用 2；Matrix {'cells': 0, 'tables': [], 'definitions': []}
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 ['98%', '97.4%', '98.3%', '97.5%']

```text
The question asks for the number of context units and tokens used by root-level community summaries (C0) and source-text summarization (TS) on the Podcast and News datasets.

### Comparison Table of the Figures
| Dataset           | Method | Context Units | Tokens     |
|-------------------|--------|----------------|------------|
| Podcast Transcripts | C0     | 34             | 26,657     |
| Podcast Transcripts | TS     | 1,669          | 1,014,611  |
| News Articles     | C0     | 55             | 39,770     |
| News Articles     | TS     | 3,197          | 1,707,694  |

### Analysis

Root-level community summaries (C0) use significantly fewer context units and tokens compared to source-text summarization (TS) in both the Podcast and News datasets.

- **Podcast Transcripts**: 
  - C0 uses 34 context units and 26,657 tokens, while TS uses 1,669 context units and 1,014,611 tokens [1].
  - This represents a reduction of approximately 98% in context units and 97.4% in tokens for C0 compared to TS.

- **News Articles**: 
  - C0 uses 55 context units and 39,770 tokens, while TS uses 3,197 context units and 1,707,694 tokens [1].
  - This represents a reduction of approximately 98.3% in context units and 97.5% in tokens for C0 compared to TS.

### Conclusion

Root-level community summaries (C0) require dramatically fewer context units and tokens than source-text summarization (TS) for both the Podcast and News datasets, as stated in the document [1].

Numbers that could not be checked against the cited pages of the original text: 98%, 97.4%, 98.3%, 97.5%.
```

## B4-G1-1

- 問題：`How many context units and tokens do the root-level community summaries (C0) and the source-text summarization (TS) use on the Podcast and News datasets?`；模式 `navigate`；25.1 秒；2 次呼叫；tokens 7573
- 來源：[1] p10 retrieval, [2] p10 retrieval, [3] p8 retrieval, [4] p10 retrieval, [5] p11 retrieval, [6] p11 table_context, [7] p11 table_context, [8] p8 navigation, [9] p10 navigation, [10] p9 navigation, [11] p9 navigation, [12] p6 navigation, [13] p4 navigation
- 閱讀計畫（定位 6/6，保留 6，超預算 0）：
  - ✓ Section 4.1.2 Conditions | need: dataset descriptions | priority: required | status: covered → 候選 2，納入 [22]，排除 [(21, 'already among the retrieved sources')]
  - ✓ Section 5.1 Experiment 1 | need: context units and tokens for C0 and TS | priority: required | status: missing → 候選 9，納入 [26, 25, 24]，排除 [(30, 'already among the retrieved sources'), (29, 'already among the retrieved sources'), (32, 'already among the retrieved sources'), (31, 'already among the retrieved sources'), (28, 'target quota reached'), (27, 'target quota reached')]
  - ✓ Table 2 | need: context units for C0 and TS | priority: required | status: missing → 候選 3，納入 []，排除 [(29, 'already among the retrieved sources'), (30, 'already among the retrieved sources'), (31, 'already among the retrieved sources')]
  - ✓ Section 5.2 Experiment 2 | need: context units and tokens for C0 and TS in News dataset | priority: supplementary | status: missing → 候選 3，納入 []，排除 [(32, 'already among the retrieved sources'), (33, 'supplementary cap reached'), (34, 'supplementary cap reached')]
  - ✓ Section 3.1.5 Graph Communities → Community Summaries | need: definition of root-level summaries | priority: supplementary | status: missing → 候選 2，納入 [15]，排除 [(16, 'supplementary cap reached')]
  - ✓ Section 3.1.1 Source Documents → Text Chunks | need: definition of source-text summarization | priority: supplementary | status: missing → 候選 1，納入 [11]，排除 []
- 分析狀態：UNCERTAIN；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 修正：[]；刪除 []；仍不符 []；方向待定 []
- 涵蓋判定：Section 4.1.2 Conditions→partial；Section 5.1 Experiment 1→partial；Table 2→partial；Section 5.2 Experiment 2→covered；Section 3.1.5 Graph Communities → Community Summaries→missing；Section 3.1.1 Source Documents → Text Chunks→missing；required 未納入 []；supplementary 用 2；Matrix {'cells': 0, 'tables': [], 'definitions': []}
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
The question asks for the number of context units and tokens used by root-level community summaries (C0) and source-text summarization (TS) on the Podcast and News datasets.

From the data provided in Table 2 [4], the number of context units and corresponding tokens for C0 and TS are as follows:

**Podcast Transcripts:**
- C0: 34 units, 26,657 tokens.
- TS: 1,669 units, 1,014,611 tokens.

**News Articles:**
- C0: 55 units, 39,770 tokens.
- TS: 3,197 units, 1,707,694 tokens.

The root-level community summaries (C0) require significantly fewer context units and tokens compared to the source-text summarization (TS) on both datasets. For the Podcast dataset, C0 uses approximately 9x fewer units and 38x fewer tokens than TS. For the News dataset, C0 uses approximately 6x fewer units and 43x fewer tokens than TS [1].
```

## B4-G1-2

- 問題：`How many context units and tokens do the root-level community summaries (C0) and the source-text summarization (TS) use on the Podcast and News datasets?`；模式 `navigate`；23.2 秒；2 次呼叫；tokens 7983
- 來源：[1] p10 retrieval, [2] p10 retrieval, [3] p8 retrieval, [4] p10 retrieval, [5] p11 retrieval, [6] p11 table_context, [7] p11 table_context, [8] p8 navigation, [9] p10 navigation, [10] p9 navigation, [11] p10 navigation, [12] p9 navigation, [13] p10 navigation, [14] p6 navigation
- 閱讀計畫（定位 6/6，保留 8，超預算 0）：
  - ✓ Section 4.1.2 Conditions | need: dataset descriptions | priority: required | status: covered → 候選 2，納入 [22]，排除 [(21, 'already among the retrieved sources')]
  - ✓ Section 5.1 Experiment 1 | need: context unit comparison for C0 and TS | priority: required | status: missing → 候選 9，納入 [25, 24, 27]，排除 [(30, 'already among the retrieved sources'), (29, 'already among the retrieved sources'), (32, 'already among the retrieved sources'), (31, 'already among the retrieved sources'), (26, 'already selected for another target'), (28, 'already selected for another target')]
  - ✓ Section 5.1 Experiment 1 | need: token usage comparison for C0 and TS | priority: required | status: missing → 候選 9，納入 [26, 28]，排除 [(27, 'low relevance'), (30, 'already among the retrieved sources'), (29, 'already among the retrieved sources'), (32, 'already among the retrieved sources'), (31, 'already among the retrieved sources'), (25, 'already selected for another target'), (24, 'already selected for another target')]
  - ✓ Table 2 | need: context unit numbers for C0 and TS | priority: required | status: missing → 候選 3，納入 []，排除 [(29, 'already among the retrieved sources'), (30, 'already among the retrieved sources'), (31, 'already among the retrieved sources')]
  - ✓ Section 3.1.5 Graph Communities → Community Summaries | need: definition of root-level summaries | priority: supplementary | status: missing → 候選 2，納入 [15]，排除 [(16, 'supplementary cap reached')]
  - ✓ Section 3.1.1 Source Documents → Text Chunks | need: source-text summarization process | priority: supplementary | status: missing → 候選 1，納入 [11]，排除 []
- 分析狀態：UNCERTAIN；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 修正：[]；刪除 []；仍不符 []；方向待定 []
- 涵蓋判定：Section 4.1.2 Conditions→partial；Section 5.1 Experiment 1→partial；Section 5.1 Experiment 1→partial；Table 2→partial；Section 3.1.5 Graph Communities → Community Summaries→missing；Section 3.1.1 Source Documents → Text Chunks→missing；required 未納入 []；supplementary 用 2；Matrix {'cells': 0, 'tables': [], 'definitions': []}
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
The question asks for the number of context units and tokens used by the root-level community summaries (C0) and the source-text summarization (TS) on the Podcast and News datasets.

For the Podcast dataset, the number of context units for root-level community summaries (C0) is 34, and for source-text summarization (TS), it is 1669. The corresponding token counts are 26,657 for C0 and 1,014,611 for TS [1].

For the News dataset, the number of context units for root-level community summaries (C0) is 55, and for source-text summarization (TS), it is 3197. The corresponding token counts are 39,770 for C0 and 1,707,694 for TS [1].
```

## B4-G1-3

- 問題：`How many context units and tokens do the root-level community summaries (C0) and the source-text summarization (TS) use on the Podcast and News datasets?`；模式 `navigate`；28.3 秒；2 次呼叫；tokens 8093
- 來源：[1] p10 retrieval, [2] p10 retrieval, [3] p8 retrieval, [4] p10 retrieval, [5] p11 retrieval, [6] p11 table_context, [7] p11 table_context, [8] p8 navigation, [9] p9 navigation, [10] p10 navigation, [11] p9 navigation, [12] p10 navigation, [13] p10 navigation, [14] p7 navigation
- 閱讀計畫（定位 6/6，保留 8，超預算 0）：
  - ✓ Section 4.1.2 Conditions | need: dataset descriptions | priority: required | status: covered → 候選 2，納入 [22]，排除 [(21, 'already among the retrieved sources')]
  - ✓ Section 5.1 Experiment 1 | need: context unit counts for C0 and TS | priority: required | status: missing → 候選 9，納入 [27]，排除 [(30, 'already among the retrieved sources'), (29, 'already among the retrieved sources'), (32, 'already among the retrieved sources'), (31, 'already among the retrieved sources'), (25, 'already selected for another target'), (26, 'already selected for another target'), (24, 'already selected for another target'), (28, 'already selected for another target')]
  - ✓ Section 5.1 Experiment 1 | need: token usage for C0 and TS | priority: required | status: missing → 候選 9，納入 [26, 28]，排除 [(30, 'already among the retrieved sources'), (29, 'already among the retrieved sources'), (32, 'already among the retrieved sources'), (31, 'already among the retrieved sources'), (25, 'already selected for another target'), (24, 'already selected for another target'), (27, 'already selected for another target')]
  - ✓ Table 2 | need: context unit counts for C0 and TS | priority: required | status: missing → 候選 3，納入 []，排除 [(29, 'already among the retrieved sources'), (30, 'already among the retrieved sources'), (31, 'already among the retrieved sources')]
  - ✓ Section 5.1 Experiment 1 | need: dataset-specific results (Podcast, News) | priority: required | status: missing → 候選 9，納入 [25, 24]，排除 [(27, 'low relevance'), (28, 'low relevance'), (30, 'already among the retrieved sources'), (31, 'already among the retrieved sources'), (32, 'already among the retrieved sources'), (29, 'already among the retrieved sources'), (26, 'already selected for another target')]
  - ✓ Table 1 | need: task examples for Podcast and News | priority: supplementary | status: missing → 候選 3，納入 [18, 19]，排除 [(20, 'supplementary cap reached')]
- 分析狀態：UNCERTAIN；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 修正：[]；刪除 []；仍不符 []；方向待定 []
- 涵蓋判定：Section 4.1.2 Conditions→partial；Section 5.1 Experiment 1→partial；Section 5.1 Experiment 1→partial；Table 2→partial；Section 5.1 Experiment 1→partial；Table 1→missing；required 未納入 []；supplementary 用 2；Matrix {'cells': 0, 'tables': [], 'definitions': []}
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
The question asks for the number of context units and tokens used by the root-level community summaries (C0) and the source-text summarization (TS) on the Podcast and News datasets.

From the evidence provided in the sources, we can read the following figures for the number of context units and tokens used by C0 and TS on the Podcast and News datasets [1]:

- Podcast Transcripts:
  - C0 (root-level community summaries): 34 units and 26,657 tokens.
  - TS (source-text summarization): 367 units and 225,756 tokens.

- News Articles:
  - C0 (root-level community summaries): 55 units and 39,770 tokens.
  - TS (source-text summarization): 555 units and 352,641 tokens.

These figures indicate that for both the Podcast and News datasets, the root-level community summaries (C0) use fewer context units and tokens compared to the source-text summarization (TS). Specifically, C0 uses 34 units and 26,657 tokens for Podcast transcripts, which is significantly fewer than the 367 units and 225,756 tokens used by TS. Similarly, for News articles, C0 uses 55 units and 39,770 tokens, which is fewer than the 555 units and 352,641 tokens used by TS [1].
```

## B4b-G1-1

- 問題：`How many context units and tokens do the root-level community summaries (C0) and the source-text summarization (TS) use on the Podcast and News datasets?`；模式 `navigate`；23.5 秒；2 次呼叫；tokens 7562
- 來源：[1] p10 retrieval, [2] p10 retrieval, [3] p8 retrieval, [4] p10 retrieval, [5] p11 retrieval, [6] p11 table_context, [7] p11 table_context, [8] p8 navigation, [9] p10 navigation, [10] p9 navigation, [11] p10 navigation, [12] p9 navigation, [13] p10 navigation
- 閱讀計畫（定位 6/6，保留 6，超預算 0）：
  - ✓ Section 4.1.2 Conditions | need: dataset descriptions | priority: required | status: covered → 候選 2，納入 [22]，排除 [(21, 'already among the retrieved sources')]
  - ✓ Section 5.1 Experiment 1 | need: context units for C0 and TS | priority: required | status: missing → 候選 9，納入 [25, 28, 24]，排除 [(30, 'already among the retrieved sources'), (29, 'already among the retrieved sources'), (32, 'already among the retrieved sources'), (31, 'already among the retrieved sources'), (26, 'already selected for another target'), (27, 'target quota reached')]
  - ✓ Section 5.1 Experiment 1 | need: token usage for C0 and TS | priority: required | status: missing → 候選 9，納入 [26, 27]，排除 [(30, 'already among the retrieved sources'), (29, 'already among the retrieved sources'), (32, 'already among the retrieved sources'), (31, 'already among the retrieved sources'), (25, 'already selected for another target'), (28, 'already selected for another target'), (24, 'already selected for another target')]
  - ✓ Table 2 | need: context units by condition | priority: required | status: missing → 候選 3，納入 []，排除 [(29, 'already among the retrieved sources'), (30, 'already among the retrieved sources'), (31, 'already among the retrieved sources')]
  - ✓ Section 5.1 Experiment 1 | need: dataset-specific context units | priority: supplementary | status: missing → 候選 9，納入 []，排除 [(28, 'low relevance'), (27, 'low relevance'), (30, 'already among the retrieved sources'), (29, 'already among the retrieved sources'), (31, 'already among the retrieved sources'), (32, 'already among the retrieved sources'), (25, 'already selected for another target'), (24, 'already selected for another target'), (26, 'already selected for another target')]
  - ✓ Section 5.1 Experiment 1 | need: dataset-specific tokens | priority: supplementary | status: missing → 候選 9，納入 []，排除 [(28, 'low relevance'), (27, 'low relevance'), (30, 'already among the retrieved sources'), (29, 'already among the retrieved sources'), (31, 'already among the retrieved sources'), (32, 'already among the retrieved sources'), (25, 'already selected for another target'), (24, 'already selected for another target'), (26, 'already selected for another target')]
- 分析狀態：UNCERTAIN；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 修正：[]；刪除 []；仍不符 []；方向待定 []
- 涵蓋判定：Section 4.1.2 Conditions→partial；Section 5.1 Experiment 1→partial；Section 5.1 Experiment 1→partial；Table 2→partial；Section 5.1 Experiment 1→partial；Section 5.1 Experiment 1→partial；required 未納入 []；supplementary 用 0；Matrix {'cells': 0, 'tables': [], 'definitions': []}
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
The question asks for the number of context units and tokens used by root-level community summaries (C0) and source-text summarization (TS) on the Podcast and News datasets.

From the provided sources, the context units and tokens for C0 and TS are as follows:

- For the Podcast dataset:
  - C0: 34 context units, 26,657 tokens [1]
  - TS: 1,669 context units, 1,014,611 tokens [1]
- For the News dataset:
  - C0: 55 context units, 39,770 tokens [1]
  - TS: 3,197 context units, 1,707,694 tokens [1]

The comparison shows that C0 uses significantly fewer context units and tokens than TS for both datasets. On the Podcast dataset, C0 uses 9x fewer context units and tokens than TS. On the News dataset, C0 uses 43x fewer context units and tokens than TS.
```

## B4b-G1-2

- 問題：`How many context units and tokens do the root-level community summaries (C0) and the source-text summarization (TS) use on the Podcast and News datasets?`；模式 `navigate`；21.7 秒；2 次呼叫；tokens 7929
- 來源：[1] p10 retrieval, [2] p10 retrieval, [3] p8 retrieval, [4] p10 retrieval, [5] p11 retrieval, [6] p11 table_context, [7] p11 table_context, [8] p8 navigation, [9] p8 navigation, [10] p10 navigation, [11] p9 navigation, [12] p10 navigation, [13] p9 navigation, [14] p10 navigation
- 閱讀計畫（定位 6/6，保留 7，超預算 0）：
  - ✓ Section 4.1.1 Datasets | need: dataset descriptions | priority: required | status: missing → 候選 2，納入 [20]，排除 [(21, 'already among the retrieved sources')]
  - ✓ Section 4.1.2 Conditions | need: text chunking details | priority: required | status: covered → 候選 2，納入 [22]，排除 [(21, 'already among the retrieved sources')]
  - ✓ Section 5.1 Experiment 1 | need: context units for C0 and TS | priority: required | status: missing → 候選 9，納入 [25, 28, 24]，排除 [(30, 'already among the retrieved sources'), (29, 'already among the retrieved sources'), (32, 'already among the retrieved sources'), (31, 'already among the retrieved sources'), (26, 'already selected for another target'), (27, 'target quota reached')]
  - ✓ Section 5.1 Experiment 1 | need: token usage for C0 and TS | priority: required | status: missing → 候選 9，納入 [26, 27]，排除 [(30, 'already among the retrieved sources'), (29, 'already among the retrieved sources'), (32, 'already among the retrieved sources'), (31, 'already among the retrieved sources'), (25, 'already selected for another target'), (28, 'already selected for another target'), (24, 'already selected for another target')]
  - ✓ Table 2 | need: context units by condition | priority: required | status: missing → 候選 3，納入 []，排除 [(29, 'already among the retrieved sources'), (30, 'already among the retrieved sources'), (31, 'already among the retrieved sources')]
  - ✓ Section 5.2 Experiment 2 | need: token usage comparison | priority: supplementary | status: missing → 候選 3，納入 []，排除 [(32, 'already among the retrieved sources'), (33, 'already among the retrieved sources'), (34, 'already among the retrieved sources')]
- 分析狀態：UNCERTAIN；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 修正：[]；刪除 []；仍不符 []；方向待定 []
- 涵蓋判定：Section 4.1.1 Datasets→partial；Section 4.1.2 Conditions→partial；Section 5.1 Experiment 1→partial；Section 5.1 Experiment 1→partial；Table 2→partial；Section 5.2 Experiment 2→covered；required 未納入 []；supplementary 用 0；Matrix {'cells': 0, 'tables': [], 'definitions': []}
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
The question asks for the number of context units and tokens used by the root-level community summaries (C0) and the source-text summarization (TS) on the Podcast and News datasets.

For the Podcast dataset, the root-level community summaries (C0) use 34 context units and 26,657 tokens, while the source-text summarization (TS) uses 1,669 context units and 1,014,611 tokens [1]. For the News dataset, the root-level community summaries (C0) use 55 context units and 39,770 tokens, while the source-text summarization (TS) uses 3,197 context units and 1,707,694 tokens [1].
```

## B4b-G1-3

- 問題：`How many context units and tokens do the root-level community summaries (C0) and the source-text summarization (TS) use on the Podcast and News datasets?`；模式 `navigate`；27.8 秒；2 次呼叫；tokens 7673
- 來源：[1] p10 retrieval, [2] p10 retrieval, [3] p8 retrieval, [4] p10 retrieval, [5] p11 retrieval, [6] p11 table_context, [7] p11 table_context, [8] p8 navigation, [9] p10 navigation, [10] p9 navigation, [11] p9 navigation, [12] p6 navigation, [13] p6 navigation
- 閱讀計畫（定位 6/6，保留 6，超預算 0）：
  - ✓ Section 4.1.2 Conditions | need: dataset descriptions | priority: required | status: covered → 候選 2，納入 [22]，排除 [(21, 'already among the retrieved sources')]
  - ✓ Section 5.1 Experiment 1 | need: context units and tokens for C0 and TS | priority: required | status: missing → 候選 9，納入 [26, 25, 24]，排除 [(30, 'already among the retrieved sources'), (29, 'already among the retrieved sources'), (32, 'already among the retrieved sources'), (31, 'already among the retrieved sources'), (28, 'target quota reached'), (27, 'target quota reached')]
  - ✓ Table 2 | need: context units for C0 and TS | priority: required | status: missing → 候選 3，納入 []，排除 [(29, 'already among the retrieved sources'), (30, 'already among the retrieved sources'), (31, 'already among the retrieved sources')]
  - ✓ Section 5.1 Experiment 1 | need: token usage details | priority: supplementary | status: covered → 候選 9，納入 []，排除 [(28, 'low relevance'), (27, 'low relevance'), (30, 'already among the retrieved sources'), (29, 'already among the retrieved sources'), (31, 'supplementary cap reached'), (32, 'supplementary cap reached'), (25, 'supplementary cap reached'), (24, 'supplementary cap reached'), (26, 'supplementary cap reached')]
  - ✓ Section 3.1.5 Graph Communities → Community Summaries | need: definition of root-level summaries | priority: supplementary | status: missing → 候選 2，納入 [15, 16]，排除 []
  - ✓ Section 4.1.1 Datasets | need: dataset specifics for Podcast and News | priority: supplementary | status: missing → 候選 2，納入 []，排除 [(21, 'already among the retrieved sources'), (20, 'supplementary cap reached')]
- 分析狀態：UNCERTAIN；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 修正：[]；刪除 []；仍不符 []；方向待定 []
- 涵蓋判定：Section 4.1.2 Conditions→partial；Section 5.1 Experiment 1→partial；Table 2→partial；Section 5.1 Experiment 1→partial；Section 3.1.5 Graph Communities → Community Summaries→missing；Section 4.1.1 Datasets→partial；required 未納入 []；supplementary 用 2；Matrix {'cells': 0, 'tables': [], 'definitions': []}
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 ['49.09', '38.08', '58.13', '43.00']

```text
The question asks for the number of context units and tokens used by root-level community summaries (C0) and source-text summarization (TS) on the Podcast and News datasets.

From the data provided in the documents, the number of context units and tokens for C0 and TS is detailed for both the Podcast and News datasets. For the Podcast dataset, C0 uses 34 context units and 26,657 tokens, while TS uses 1,669 context units and 1,014,611 tokens. For the News dataset, C0 uses 55 context units and 39,770 tokens, while TS uses 3,197 context units and 1,707,694 tokens [4]. 

These figures show a clear difference in the number of context units and tokens used between C0 and TS for both datasets, with TS requiring significantly more context units and tokens compared to C0. Specifically, for the Podcast dataset, TS uses 49.09 times more context units and 38.08 times more tokens than C0. For the News dataset, TS uses 58.13 times more context units and 43.00 times more tokens than C0 [4]. 

The data supports the conclusion that root-level community summaries (C0) are significantly more efficient in terms of context units and tokens compared to source-text summarization (TS) for both the Podcast and News datasets [4].

Numbers that could not be checked against the cited pages of the original text: 49.09, 38.08, 58.13, 43.00.
```

## C-G1-1

- 問題：`How many context units and tokens do the root-level community summaries (C0) and the source-text summarization (TS) use on the Podcast and News datasets?`；模式 `single`；10.2 秒；1 次呼叫；tokens 3141
- 來源：[1] p10 retrieval, [2] p10 retrieval, [3] p8 retrieval, [4] p10 retrieval, [5] p11 retrieval, [6] p11 table_context, [7] p11 table_context
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
The root-level community summaries (C0) and the source-text summarization (TS) use the following context units and tokens on the Podcast and News datasets:

For Podcast Transcripts:
- **C0** (root-level community summaries): 34 units and 26,657 tokens.
- **TS** (source-text summarization): 1,669 units and 1,014,611 tokens.

For News Articles:
- **C0** (root-level community summaries): 55 units and 39,770 tokens.
- **TS** (source-text summarization): 3,197 units and 1,707,694 tokens.

These figures show that root-level community summaries require dramatically fewer tokens per query compared to source-text summarization [1].
```

## C-G1-2

- 問題：`How many context units and tokens do the root-level community summaries (C0) and the source-text summarization (TS) use on the Podcast and News datasets?`；模式 `single`；9.3 秒；1 次呼叫；tokens 3182
- 來源：[1] p10 retrieval, [2] p10 retrieval, [3] p8 retrieval, [4] p10 retrieval, [5] p11 retrieval, [6] p11 table_context, [7] p11 table_context
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
For the Podcast and News datasets, the root-level community summaries (C0) and the source-text summarization (TS) use the following context units and tokens:

### Podcast Dataset:
- **C0 (Root-level community summaries):**
  - **Units:** 34
  - **Tokens:** 26,657 [1]
- **TS (Source-text summarization):**
  - **Units:** 1,669
  - **Tokens:** 1,014,611 [1]

### News Dataset:
- **C0 (Root-level community summaries):**
  - **Units:** 55
  - **Tokens:** 39,770 [1]
- **TS (Source-text summarization):**
  - **Units:** 3,197
  - **Tokens:** 1,707,694 [1]

These figures illustrate the significant reduction in context tokens when using root-level community summaries compared to source-text summarization [1].
```

## C-G1-3

- 問題：`How many context units and tokens do the root-level community summaries (C0) and the source-text summarization (TS) use on the Podcast and News datasets?`；模式 `single`；7.4 秒；1 次呼叫；tokens 3135
- 來源：[1] p10 retrieval, [2] p10 retrieval, [3] p8 retrieval, [4] p10 retrieval, [5] p11 retrieval, [6] p11 table_context, [7] p11 table_context
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
The root-level community summaries (C0) and the source-text summarization (TS) use the following context units and tokens on the Podcast and News datasets:

- **Podcast Transcripts:**
  - **C0 (Root-level community summaries):** 34 units, 26,657 tokens [1].
  - **TS (Source-text summarization):** 1,669 units, 1,014,611 tokens [1].

- **News Articles:**
  - **C0 (Root-level community summaries):** 55 units, 39,770 tokens [1].
  - **TS (Source-text summarization):** 3,197 units, 1,707,694 tokens [1].
```

## A-G2-1

- 問題：`Compare condition C2 with vector RAG (SS) on comprehensiveness in the Podcast and News datasets`；模式 `roles`；12.8 秒；1 次呼叫；tokens 2945
- 來源：[1] p9 retrieval, [2] p11 retrieval, [3] p10 retrieval, [4] p11 retrieval, [5] p10 retrieval
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
Navigator: The sections and tables that bear on the question are the Analysis (pages 8-9), Results (pages 9-11), Table 2 (page 10), Table 3 (page 11), and Table 4 (page 11).

Analyst: Condition C2 outperformed vector RAG (SS) in comprehensiveness for both the Podcast and News datasets. In the Podcast dataset, comprehensiveness win rates for C2 were 72-83% (p<.001) [1]. Similarly, for the News dataset, comprehensiveness win rates for C2 were 72-80% (p <.001) [1]. These findings are supported by Table 3, which shows that all global search conditions (C0-C3) and source text summarization (TS) had greater comprehensiveness than vector RAG (SS) for both datasets, with statistically significant differences (p <.05) in all cases [2]. No exceptions to this trend are explicitly named in the provided sources. Therefore, condition C2 significantly outperformed vector RAG (SS) in comprehensiveness for both the Podcast and News datasets.
```

## A-G2-2

- 問題：`Compare condition C2 with vector RAG (SS) on comprehensiveness in the Podcast and News datasets`；模式 `roles`；9.1 秒；1 次呼叫；tokens 2898
- 來源：[1] p9 retrieval, [2] p11 retrieval, [3] p10 retrieval, [4] p11 retrieval, [5] p10 retrieval
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
Navigator: The relevant sections for this question are the Analysis (page 8-9), Results (pages 9-11), Table 2 (page 10), and Table 3 (page 11).

Analyst: On the Podcast dataset, condition C2 outperformed vector RAG (SS) in comprehensiveness, with a win rate of 72-83% (p<.001) [1]. Similarly, for the News dataset, condition C2 also achieved comprehensiveness win rates of 72-80% (p <.001) compared to vector RAG (SS) [1]. These results are supported by Table 3, which shows that all global search conditions, including C2, had higher average numbers of extracted claims than vector RAG (SS) for both datasets, with statistically significant differences (p <.05) in all cases [2]. No explicit exceptions for C2 are mentioned in the provided sources.
```

## A-G2-3

- 問題：`Compare condition C2 with vector RAG (SS) on comprehensiveness in the Podcast and News datasets`；模式 `roles`；7.4 秒；1 次呼叫；tokens 2857
- 來源：[1] p9 retrieval, [2] p11 retrieval, [3] p10 retrieval, [4] p11 retrieval, [5] p10 retrieval
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
Navigator: The relevant sections for the question are in the "Results" section (pages 9-11), particularly the discussion on comprehensiveness and diversity in [1], and the data in Table 3 (page 11) [2].

Analyst: In the Podcast dataset, condition C2 outperformed vector RAG (SS) in comprehensiveness, with a statistically significant difference (p < .05) [2]. Similarly, in the News dataset, condition C2 also outperformed vector RAG (SS) in comprehensiveness, with a statistically significant difference (p < .05) [2]. These results align with the overall finding that global approaches (including C2) significantly outperformed vector RAG (SS) in comprehensiveness across datasets [1].
```

## B-G2-1

- 問題：`Compare condition C2 with vector RAG (SS) on comprehensiveness in the Podcast and News datasets`；模式 `navigate`；22.6 秒；2 次呼叫；tokens 6925
- 來源：[1] p9 retrieval, [2] p11 retrieval, [3] p10 retrieval, [4] p11 retrieval, [5] p10 retrieval, [6] p11 navigation, [7] p10 navigation, [8] p10 navigation, [9] p10 navigation, [10] p10 navigation, [11] p8 navigation, [12] p8 navigation, [13] p8 navigation, [14] p9 navigation
- 閱讀計畫（定位 6/6，保留 10，超預算 11）：
  - ✓ Table 3 (page 11): Average number of extracted claims, reported by condition and dataset type.
  - ✓ Table 2 (page 10): Number of context units (community summaries for C0-C3 and text chunks for SS), corre-
  - ✓ Section: Analysis (pages 8-9)
  - ✓ Section: Results (pages 9-11)
  - ✓ Table 4 (page 12): Average number of clusters across different distance thresholds, reported by condition and
  - ✓ Table 6 (page 26): Pairwise comparisons of six conditions on four metrics across 125 questions and two
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
For the Podcast dataset, condition C2 significantly outperformed vector RAG (SS) in comprehensiveness, with a win rate of 72% (p<.001) [1]. Similarly, for the News dataset, condition C2 also outperformed SS in comprehensiveness, with a win rate of 72% (p<.001) [1]. 

In terms of the average number of extracted claims, for the Podcast dataset, C2 had an average of 32.46 claims, while SS had 26.50 claims [2]. For the News dataset, C2 had an average of 31.62 claims, while SS had 33.14 claims. However, the difference in the News dataset was not as large as in the Podcast dataset [2].

There were no statistically significant differences observed among the global search conditions or between global search and TS for comprehensiveness [4].

In conclusion, condition C2 outperformed vector RAG (SS) in comprehensiveness for both the Podcast and News datasets, but the difference was more pronounced in the Podcast dataset.
```

## B-G2-2

- 問題：`Compare condition C2 with vector RAG (SS) on comprehensiveness in the Podcast and News datasets`；模式 `navigate`；27.5 秒；2 次呼叫；tokens 7064
- 來源：[1] p9 retrieval, [2] p11 retrieval, [3] p10 retrieval, [4] p11 retrieval, [5] p10 retrieval, [6] p11 navigation, [7] p10 navigation, [8] p10 navigation, [9] p10 navigation, [10] p10 navigation, [11] p8 navigation, [12] p8 navigation, [13] p8 navigation, [14] p9 navigation
- 閱讀計畫（定位 6/6，保留 10，超預算 8）：
  - ✓ Table 3 (page 11): Average number of extracted claims, reported by condition and dataset type.
  - ✓ Table 2 (page 10): Number of context units (community summaries for C0-C3 and text chunks for SS), corre-
  - ✓ Section: Analysis (pages 8-9): Likely contains discussion of comprehensiveness measures.
  - ✓ Section: Results (pages 9-11): Likely includes results comparing C2 and SS.
  - ✓ Table 6 (page 26): Pairwise comparisons of six conditions on four metrics across 125 questions and two
  - ✓ Figure 2 (page 10): Head-to-head win rate percentages of (row condition) over (column condition) across two
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 [([1], [2, 4])]；未解析 0；找不到的數字 []

```text
Condition C2 was compared with vector RAG (SS) on comprehensiveness in both the Podcast and News datasets. For the Podcast dataset, all global search conditions, including C2, showed greater comprehensiveness than SS, with statistically significant differences in all cases (p <.05). The comprehensiveness win rates for global approaches, including C2, ranged from 72-83% for Podcast transcripts [1]. In terms of the average number of extracted claims, a claim-based measure of comprehensiveness, C2 for the Podcast dataset recorded 32.46 average claims, while SS had 26.50 average claims [2]. This indicates a clear advantage for C2 over SS in comprehensiveness for the Podcast dataset.

For the News dataset, the results were similar. All global search conditions, including C2, had greater comprehensiveness than SS, and the differences were statistically significant in all cases (p <.05) [2]. The comprehensiveness win rates for global approaches, including C2, ranged from 72-80% for News articles [1]. In terms of the average number of extracted claims, C2 for the News dataset recorded 31.62 average claims, while SS had 25.23 average claims [2]. This also indicates a clear advantage for C2 over SS in comprehensiveness for the News dataset.

Therefore, across both the Podcast and News datasets, condition C2 demonstrated significantly better comprehensiveness than vector RAG (SS), as evidenced by the higher win rates and average number of extracted claims.
```

## B-G2-3

- 問題：`Compare condition C2 with vector RAG (SS) on comprehensiveness in the Podcast and News datasets`；模式 `navigate`；20.5 秒；2 次呼叫；tokens 7137
- 來源：[1] p9 retrieval, [2] p11 retrieval, [3] p10 retrieval, [4] p11 retrieval, [5] p10 retrieval, [6] p11 navigation, [7] p10 navigation, [8] p10 navigation, [9] p10 navigation, [10] p10 navigation, [11] p9 navigation, [12] p9 navigation, [13] p12 navigation, [14] p12 navigation
- 閱讀計畫（定位 6/6，保留 10，超預算 8）：
  - ✓ Table 3 (page 11): Average number of extracted claims, reported by condition and dataset type.
  - ✓ Table 2 (page 10): Number of context units (community summaries for C0-C3 and text chunks for SS), corresponding to each condition.
  - ✓ Section: Results (pages 9-11): General discussion of results including comprehensiveness across conditions.
  - ✓ Table 4 (page 12): Average number of clusters across different distance thresholds, reported by condition and dataset type.
  - ✓ Table 6 (page 26): Pairwise comparisons of six conditions on four metrics across 125 questions and two datasets.
  - ✓ Section: Discussion (pages 11-12): Interpretation of results including comparisons between conditions.
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
For the Podcast dataset, condition C2 achieved an average number of claims of 32.46, while vector RAG (SS) had an average of 26.50 [2]. This indicates that C2 outperformed SS in comprehensiveness for the Podcast dataset. 

For the News dataset, condition C2 had an average number of claims of 31.62, while vector RAG (SS) had an average of 31.39 [2]. This suggests that C2 slightly outperformed SS in comprehensiveness for the News dataset as well.

Overall, condition C2 showed better performance in comprehensiveness compared to vector RAG (SS) for both the Podcast and News datasets.
```

## B2-G2-1

- 問題：`Compare condition C2 with vector RAG (SS) on comprehensiveness in the Podcast and News datasets`；模式 `navigate`；23.7 秒；2 次呼叫；tokens 7724
- 來源：[1] p9 retrieval, [2] p11 retrieval, [3] p10 retrieval, [4] p11 retrieval, [5] p10 retrieval, [6] p10 navigation, [7] p26 navigation, [8] p26 navigation, [9] p11 navigation, [10] p26 navigation, [11] p10 navigation, [12] p9 navigation, [13] p10 navigation, [14] p10 navigation
- 閱讀計畫（定位 6/6，保留 9，超預算 0）：
  - ✓ Section 5.1 Experiment 1 | need: comprehensiveness results for C2 and SS in Podcast dataset | priority: required | status: missing → 候選 9，納入 [26, 24, 28]，排除 [(25, 'already among the retrieved sources'), (32, 'already among the retrieved sources'), (31, 'already among the retrieved sources'), (30, 'already among the retrieved sources'), (29, 'already selected for another target'), (27, 'target quota reached')]
  - ✓ Section 5.1 Experiment 1 | need: comprehensiveness results for C2 and SS in News dataset | priority: required | status: missing → 候選 9，納入 [27]，排除 [(25, 'already among the retrieved sources'), (32, 'already among the retrieved sources'), (31, 'already among the retrieved sources'), (30, 'already among the retrieved sources'), (29, 'already selected for another target'), (26, 'already selected for another target'), (24, 'already selected for another target'), (28, 'already selected for another target')]
  - ✓ Table 2 | need: context units for C2 and SS in both datasets | priority: supplementary | status: missing → 候選 3，納入 [29]，排除 [(30, 'already among the retrieved sources'), (31, 'already among the retrieved sources')]
  - ✓ Section 5.2 Experiment 2 | need: comparison of C2 and SS on extracted claims in both datasets | priority: supplementary | status: missing → 候選 3，納入 []，排除 [(32, 'already among the retrieved sources'), (33, 'already among the retrieved sources'), (34, 'already selected for another target')]
  - ✓ Table 3 | need: average number of extracted claims for C2 and SS in both datasets | priority: supplementary | status: missing → 候選 3，納入 [34]，排除 [(32, 'already among the retrieved sources'), (33, 'already among the retrieved sources')]
  - ✓ Table 6 | need: pairwise comparisons of C2 and SS on relevant metrics | priority: supplementary | status: missing → 候選 3，納入 [74, 75, 76]，排除 []
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
In the comparison between condition C2 and vector RAG (SS) on comprehensiveness, the results for both the Podcast and News datasets show that C2 significantly outperformed SS. 

For the Podcast dataset, C2 achieved a comprehensiveness win rate of 77.76%, with a statistically significant difference indicated by a Z-value of -8.17 and a p-value < 0.001 [7]. Similarly, in the News dataset, C2 had a comprehensiveness win rate of 79.2%, with a Z-value of -8.34 and a p-value < 0.001, also indicating a statistically significant difference [7].

There were no specific exceptions reported in the data for comprehensiveness under these conditions.

In conclusion, C2 significantly outperformed SS in comprehensiveness for both the Podcast and News datasets, with strong statistical support for these findings.
```

## B2-G2-2

- 問題：`Compare condition C2 with vector RAG (SS) on comprehensiveness in the Podcast and News datasets`；模式 `navigate`；23.9 秒；2 次呼叫；tokens 7719
- 來源：[1] p9 retrieval, [2] p11 retrieval, [3] p10 retrieval, [4] p11 retrieval, [5] p10 retrieval, [6] p10 navigation, [7] p26 navigation, [8] p26 navigation, [9] p11 navigation, [10] p26 navigation, [11] p10 navigation, [12] p10 navigation, [13] p10 navigation, [14] p9 navigation
- 閱讀計畫（定位 6/6，保留 9，超預算 0）：
  - ✓ Section 5.1 Experiment 1 | need: comprehensiveness results for C2 and SS in Podcast | priority: required | status: missing → 候選 9，納入 [26, 24]，排除 [(32, 'already among the retrieved sources'), (25, 'already among the retrieved sources'), (29, 'already selected for another target'), (31, 'already among the retrieved sources'), (30, 'already among the retrieved sources'), (28, 'already selected for another target'), (27, 'already selected for another target')]
  - ✓ Section 5.1 Experiment 1 | need: comprehensiveness results for C2 and SS in News | priority: required | status: missing → 候選 9，納入 [28, 27]，排除 [(32, 'already among the retrieved sources'), (25, 'already among the retrieved sources'), (29, 'already selected for another target'), (31, 'already among the retrieved sources'), (30, 'already among the retrieved sources'), (26, 'already selected for another target'), (24, 'already selected for another target')]
  - ✓ Table 2 | need: context units for C2 and SS in Podcast and News | priority: supplementary | status: covered → 候選 3，納入 [29]，排除 [(30, 'already among the retrieved sources'), (31, 'already among the retrieved sources')]
  - ✓ Section 5.2 Experiment 2 | need: additional evaluation of C2 vs SS on comprehensiveness | priority: supplementary | status: missing → 候選 3，納入 []，排除 [(32, 'already among the retrieved sources'), (33, 'already among the retrieved sources'), (34, 'already selected for another target')]
  - ✓ Table 3 | need: extracted claims for C2 and SS in Podcast and News | priority: supplementary | status: covered → 候選 3，納入 [34]，排除 [(32, 'already among the retrieved sources'), (33, 'already among the retrieved sources')]
  - ✓ Table 6 | need: pairwise comparisons including C2 and SS | priority: supplementary | status: missing → 候選 3，納入 [74, 75, 76]，排除 []
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 [([7], [2, 4])]；未解析 0；找不到的數字 []

```text
Condition C2 significantly outperformed vector RAG (SS) in comprehensiveness for both the Podcast and News datasets. In the Podcast dataset, C2 had a comprehensiveness win rate of 77.76% (p < 0.001), while in the News dataset, the win rate was 79.2% (p < 0.001) [7]. Additionally, the average number of extracted claims for C2 was 31.62 for Podcast transcripts and 31.62 for News articles, compared to 25.23 for Podcast and 26.50 for News in SS [2]. These results indicate that C2 provides a more comprehensive extraction of claims than SS in both datasets. There are no explicitly reported results in the provided sources that contradict this trend. Therefore, the conclusion is that C2 consistently outperformed SS in comprehensiveness in both the Podcast and News datasets.
```

## B2-G2-3

- 問題：`Compare condition C2 with vector RAG (SS) on comprehensiveness in the Podcast and News datasets`；模式 `navigate`；22.7 秒；2 次呼叫；tokens 7201
- 來源：[1] p9 retrieval, [2] p11 retrieval, [3] p10 retrieval, [4] p11 retrieval, [5] p10 retrieval, [6] p10 navigation, [7] p8 navigation, [8] p7 navigation, [9] p11 navigation, [10] p10 navigation, [11] p9 navigation, [12] p10 navigation, [13] p10 navigation
- 閱讀計畫（定位 6/6，保留 8，超預算 0）：
  - ✓ Section 5.1 Experiment 1 | need: comprehensiveness results for Podcast dataset | priority: required | status: covered → 候選 9，納入 [26]，排除 [(25, 'already among the retrieved sources'), (32, 'already among the retrieved sources'), (31, 'already among the retrieved sources'), (30, 'already among the retrieved sources'), (29, 'already selected for another target'), (24, 'already selected for another target'), (28, 'already selected for another target'), (27, 'already selected for another target')]
  - ✓ Section 5.1 Experiment 1 | need: comprehensiveness results for News dataset | priority: required | status: covered → 候選 9，納入 [24, 28, 27]，排除 [(25, 'already among the retrieved sources'), (32, 'already among the retrieved sources'), (31, 'already among the retrieved sources'), (30, 'already among the retrieved sources'), (29, 'already selected for another target'), (26, 'already selected for another target')]
  - ✓ Section 5.2 Experiment 2 | need: C2 vs SS comparison on comprehensiveness | priority: required | status: missing → 候選 3，納入 [34]，排除 [(32, 'already among the retrieved sources'), (33, 'already among the retrieved sources')]
  - ✓ Table 3 | need: extracted claims data by condition and dataset | priority: supplementary | status: covered → 候選 3，納入 []，排除 [(32, 'already among the retrieved sources'), (33, 'already among the retrieved sources'), (34, 'already selected for another target')]
  - ✓ Table 2 | need: context units used for C2 and SS | priority: supplementary | status: covered → 候選 3，納入 [29]，排除 [(30, 'already among the retrieved sources'), (31, 'already among the retrieved sources')]
  - ✓ Section 3.3 Criteria for Evaluating Global Sensemaking | need: definition of comprehensiveness | priority: supplementary | status: missing → 候選 3，納入 [20, 19]，排除 [(18, 'low relevance')]
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
For the Podcast dataset, condition C2 achieved a comprehensiveness win rate of 72-83% over vector RAG (SS) (p<.001) [1]. In the News dataset, condition C2 had a comprehensiveness win rate of 72-80% over SS (p <.001) [1]. Additionally, in terms of the average number of extracted claims for the Podcast dataset, C2 had 32.46 claims, compared to SS with 26.50 claims [2]. For the News dataset, C2 had 31.62 claims, compared to SS with 25.23 claims [2]. These results indicate that C2 outperformed SS in comprehensiveness for both datasets. No results contradict this trend in the provided sources. Therefore, the conclusion is that C2 significantly outperformed SS in comprehensiveness for both the Podcast and News datasets.
```

## B3-G2-1

- 問題：`Compare condition C2 with vector RAG (SS) on comprehensiveness in the Podcast and News datasets`；模式 `navigate`；29.6 秒；2 次呼叫；tokens 6849
- 來源：[1] p9 retrieval, [2] p11 retrieval, [3] p10 retrieval, [4] p11 retrieval, [5] p10 retrieval, [6] p10 navigation, [7] p10 navigation, [8] p9 navigation, [9] p10 navigation, [10] p10 navigation, [11] p11 navigation
- 閱讀計畫（定位 6/6，保留 6，超預算 0）：
  - ✓ Section 5.1 Experiment 1 | need: comprehensiveness results for C2 and SS in Podcast dataset | priority: required | status: missing → 候選 9，納入 [29, 26, 24]，排除 [(25, 'already among the retrieved sources'), (32, 'already among the retrieved sources'), (31, 'already among the retrieved sources'), (30, 'already among the retrieved sources'), (28, 'target quota reached'), (27, 'target quota reached')]
  - ✓ Section 5.1 Experiment 1 | need: comprehensiveness results for C2 and SS in News dataset | priority: required | status: missing → 候選 9，納入 [28, 27]，排除 [(25, 'already among the retrieved sources'), (32, 'already among the retrieved sources'), (31, 'already among the retrieved sources'), (30, 'already among the retrieved sources'), (29, 'already selected for another target'), (26, 'already selected for another target'), (24, 'already selected for another target')]
  - ✓ Table 2 | need: context units for C2 and SS in both datasets | priority: supplementary | status: covered → 候選 3，納入 []，排除 [(29, 'already selected for another target'), (30, 'already among the retrieved sources'), (31, 'already among the retrieved sources')]
  - ✓ Section 5.2 Experiment 2 | need: average cluster counts for C2 and SS | priority: supplementary | status: missing → 候選 3，納入 []，排除 [(32, 'already among the retrieved sources'), (33, 'already among the retrieved sources'), (34, 'already selected for another target')]
  - ✓ Table 3 | need: extracted claims for C2 and SS in both datasets | priority: supplementary | status: missing → 候選 3，納入 [34]，排除 [(32, 'already among the retrieved sources'), (33, 'already among the retrieved sources')]
  - ✓ Section 3.1.5 Graph Communities → Community Summaries | need: method description for C2 and SS | priority: supplementary | status: missing → 候選 2，納入 []，排除 [(16, 'low relevance'), (15, 'low relevance')]
- 分析狀態：UNCERTAIN；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 涵蓋判定：Section 5.1 Experiment 1→partial；Section 5.1 Experiment 1→partial；Table 2→missing；Section 5.2 Experiment 2→partial；Table 3→covered；Section 3.1.5 Graph Communities → Community Summaries→missing；required 未納入 []；supplementary 用 1；Matrix {'cells': 0, 'tables': [], 'definitions': []}
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 ['5.96', '6.39']

```text
The question asks to compare condition C2 with vector RAG (SS) on comprehensiveness in the Podcast and News datasets.

From Table 3, we observe the following average number of extracted claims (a measure of comprehensiveness):
- For the Podcast dataset, C2 had an average of 32.46 claims, while SS had 26.50 claims [2].
- For the News dataset, C2 had an average of 31.62 claims, while SS had 25.23 claims [2].

In both datasets, condition C2 outperformed vector RAG (SS) in terms of comprehensiveness. In the Podcast dataset, the average number of extracted claims for C2 was 32.46 compared to 26.50 for SS, representing an increase of 5.96 claims. In the News dataset, the average number of extracted claims for C2 was 31.62 compared to 25.23 for SS, representing an increase of 6.39 claims. These differences were statistically significant (p < .05) in all cases [2]. There are no exceptions mentioned in the given data.

| Dataset       | Method | Average Number of Claims |
|---------------|--------|--------------------------|
| Podcast       | C2     | 32.46                    |
| Podcast       | SS     | 26.50                    |
| News          | C2     | 31.62                    |
| News          | SS     | 25.23                    |

In conclusion, condition C2 outperforms vector RAG (SS) in comprehensiveness for both the Podcast and News datasets.

Numbers that could not be checked against the cited pages of the original text: 5.96, 6.39.
```

## B3-G2-2

- 問題：`Compare condition C2 with vector RAG (SS) on comprehensiveness in the Podcast and News datasets`；模式 `navigate`；34.2 秒；2 次呼叫；tokens 7520
- 來源：[1] p9 retrieval, [2] p11 retrieval, [3] p10 retrieval, [4] p11 retrieval, [5] p10 retrieval, [6] p10 navigation, [7] p10 navigation, [8] p9 navigation, [9] p10 navigation, [10] p10 navigation, [11] p26 navigation, [12] p26 navigation
- 閱讀計畫（定位 6/6，保留 7，超預算 0）：
  - ✓ Section 5.1 Experiment 1 | need: comprehensiveness comparison in Podcast dataset | priority: required | status: missing → 候選 9，納入 [29, 26]，排除 [(25, 'already among the retrieved sources'), (32, 'already among the retrieved sources'), (31, 'already among the retrieved sources'), (30, 'already among the retrieved sources'), (24, 'already selected for another target'), (28, 'already selected for another target'), (27, 'already selected for another target')]
  - ✓ Section 5.1 Experiment 1 | need: comprehensiveness comparison in News dataset | priority: required | status: missing → 候選 9，納入 [24, 28, 27]，排除 [(25, 'already among the retrieved sources'), (32, 'already among the retrieved sources'), (31, 'already among the retrieved sources'), (30, 'already among the retrieved sources'), (29, 'already selected for another target'), (26, 'already selected for another target')]
  - ✓ Section 5.2 Experiment 2 | need: C2 vs SS average cluster counts | priority: supplementary | status: missing → 候選 3，納入 []，排除 [(32, 'already among the retrieved sources'), (33, 'supplementary cap reached'), (34, 'supplementary cap reached')]
  - ✓ Table 2 | need: context units for C2 and SS | priority: supplementary | status: covered → 候選 3，納入 []，排除 [(29, 'already selected for another target'), (30, 'already among the retrieved sources'), (31, 'supplementary cap reached')]
  - ✓ Table 3 | need: extracted claims for C2 and SS | priority: supplementary | status: covered → 候選 3，納入 []，排除 [(32, 'already among the retrieved sources'), (33, 'already among the retrieved sources'), (34, 'supplementary cap reached')]
  - ✓ Table 6 | need: pairwise comparisons including C2 and SS | priority: supplementary | status: missing → 候選 3，納入 [74, 75]，排除 [(76, 'supplementary cap reached')]
- 分析狀態：UNCERTAIN；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 涵蓋判定：Section 5.1 Experiment 1→partial；Section 5.1 Experiment 1→partial；Section 5.2 Experiment 2→partial；Table 2→missing；Table 3→covered；Table 6→missing；required 未納入 []；supplementary 用 2；Matrix {'cells': 0, 'tables': [], 'definitions': []}
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
(1) The question asks to compare condition C2 with vector RAG (SS) on comprehensiveness in the Podcast and News datasets.

(2) Comprehensiveness is measured as the average number of claims extracted from the answers generated under each condition [8]. Table 3 shows the average number of extracted claims for each condition and dataset type [2]. Additionally, pairwise comparisons are presented in Table 6, which includes mean scores and p-values for the comprehensiveness metric [11].

(3) For the Podcast dataset, the average number of extracted claims for C2 is 32.46, and for SS, it is 26.50 [2]. In the News dataset, the average number of extracted claims for C2 is 31.62, and for SS, it is 25.23 [2]. In Table 6, the mean score for C2 over SS in the Podcast dataset is 77.76 for C2 and 22.24 for SS (p < 0.001), and in the News dataset, it is 79.2 for C2 and 20.8 for SS (p < 0.001) [11].

(4) In both the Podcast and News datasets, condition C2 outperforms SS in terms of comprehensiveness. The differences are statistically significant in both datasets. No exceptions are noted.

(5) The comprehensiveness scores for C2 are higher than those for SS in both datasets, and the p-values indicate that the differences are statistically significant [2][11].

(6) The figures and definitions are cited as follows:
- The average number of extracted claims for C2 and SS in the Podcast and News datasets are cited from Table 3 [2].
- The mean scores and p-values for C2 and SS in the Podcast and News datasets are cited from Table 6 [11].
- The definition of comprehensiveness is cited from the method description in the document [8].

(7) The comparison includes all the requested elements: the methods (C2 and SS), the datasets (Podcast and News), and the metric (comprehensiveness). The findings are supported by the figures from the sources. No relevant information is missing.
```

## B3-G2-3

- 問題：`Compare condition C2 with vector RAG (SS) on comprehensiveness in the Podcast and News datasets`；模式 `navigate`；27.4 秒；2 次呼叫；tokens 7001
- 來源：[1] p9 retrieval, [2] p11 retrieval, [3] p10 retrieval, [4] p11 retrieval, [5] p10 retrieval, [6] p10 navigation, [7] p10 navigation, [8] p10 navigation, [9] p10 navigation, [10] p9 navigation, [11] p5 navigation, [12] p11 navigation
- 閱讀計畫（定位 6/6，保留 7，超預算 0）：
  - ✓ Section 5.1 Experiment 1 | need: comprehensiveness results for C2 and SS in Podcast | priority: required | status: missing → 候選 9，納入 [29, 26, 24]，排除 [(32, 'already among the retrieved sources'), (25, 'already among the retrieved sources'), (31, 'already among the retrieved sources'), (30, 'already among the retrieved sources'), (28, 'already selected for another target'), (27, 'already selected for another target')]
  - ✓ Section 5.1 Experiment 1 | need: comprehensiveness results for C2 and SS in News | priority: required | status: missing → 候選 9，納入 [28, 27]，排除 [(32, 'already among the retrieved sources'), (25, 'already among the retrieved sources'), (29, 'already selected for another target'), (31, 'already among the retrieved sources'), (30, 'already among the retrieved sources'), (26, 'already selected for another target'), (24, 'already selected for another target')]
  - ✓ Table 2 | need: context units for C2 and SS in Podcast and News | priority: supplementary | status: covered → 候選 3，納入 []，排除 [(29, 'already selected for another target'), (30, 'already among the retrieved sources'), (31, 'already among the retrieved sources')]
  - ✓ Section 5.2 Experiment 2 | need: comparison of C2 and SS on cluster counts in Podcast and News | priority: supplementary | status: missing → 候選 3，納入 []，排除 [(32, 'already among the retrieved sources'), (33, 'already among the retrieved sources'), (34, 'supplementary cap reached')]
  - ✓ Table 3 | need: extracted claims for C2 and SS in Podcast and News | priority: supplementary | status: missing → 候選 3，納入 [34]，排除 [(32, 'already among the retrieved sources'), (33, 'already among the retrieved sources')]
  - ✓ Section 3.1.4 Knowledge Graph → Graph Communities | need: description of community clustering for C2 and SS | priority: supplementary | status: missing → 候選 3，納入 [14]，排除 [(15, 'low relevance'), (13, 'low relevance')]
- 分析狀態：UNCERTAIN；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 涵蓋判定：Section 5.1 Experiment 1→partial；Section 5.1 Experiment 1→partial；Table 2→missing；Section 5.2 Experiment 2→partial；Table 3→covered；Section 3.1.4 Knowledge Graph → Graph Communities→missing；required 未納入 []；supplementary 用 2；Matrix {'cells': 0, 'tables': [], 'definitions': []}
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
The question asks to compare condition C2 with vector RAG (SS) on comprehensiveness in the Podcast and News datasets. The relevant metric is comprehensiveness, defined as the average number of claims extracted from the answers generated under each condition [10].

### Comparison Table
| Dataset        | Method | Comprehensiveness |
|----------------|--------|-------------------|
| Podcast        | C2     | 32.46             |
| Podcast        | SS     | 26.50             |
| News           | C2     | 31.62             |
| News           | SS     | 25.23             |

### Analysis
For the **Podcast dataset**, condition C2 achieved a comprehensiveness score of 32.46, while vector RAG (SS) achieved a score of 26.50. This indicates that C2 outperformed SS in comprehensiveness for the Podcast dataset [2].

For the **News dataset**, condition C2 achieved a comprehensiveness score of 31.62, while vector RAG (SS) achieved a score of 25.23. This indicates that C2 outperformed SS in comprehensiveness for the News dataset as well [2].

There are no exceptions to the trend of C2 outperforming SS in comprehensiveness for either dataset. The conclusions are supported directly by the figures provided.
```

## B4-G2-1

- 問題：`Compare condition C2 with vector RAG (SS) on comprehensiveness in the Podcast and News datasets`；模式 `navigate`；25.6 秒；2 次呼叫；tokens 7375
- 來源：[1] p9 retrieval, [2] p11 retrieval, [3] p10 retrieval, [4] p11 retrieval, [5] p10 retrieval, [6] p10 navigation, [7] p10 navigation, [8] p10 navigation, [9] p10 navigation, [10] p9 navigation, [11] p8 navigation, [12] p8 navigation
- 閱讀計畫（定位 6/6，保留 7，超預算 0）：
  - ✓ Section 5.1 Experiment 1 | need: comprehensiveness results for C2 and SS in Podcast | priority: required | status: covered → 候選 9，納入 [29, 26, 24]，排除 [(32, 'already among the retrieved sources'), (25, 'already among the retrieved sources'), (31, 'already among the retrieved sources'), (30, 'already among the retrieved sources'), (28, 'already selected for another target'), (27, 'already selected for another target')]
  - ✓ Section 5.1 Experiment 1 | need: comprehensiveness results for C2 and SS in News | priority: required | status: covered → 候選 9，納入 [28, 27]，排除 [(32, 'already among the retrieved sources'), (25, 'already among the retrieved sources'), (29, 'already selected for another target'), (31, 'already among the retrieved sources'), (30, 'already among the retrieved sources'), (26, 'already selected for another target'), (24, 'already selected for another target')]
  - ✓ Table 2 | need: context units for C2 and SS in Podcast and News | priority: supplementary | status: covered → 候選 3，納入 []，排除 [(29, 'already selected for another target'), (30, 'already among the retrieved sources'), (31, 'supplementary cap reached')]
  - ✓ Section 5.2 Experiment 2 | need: additional evaluation metrics for C2 and SS | priority: supplementary | status: missing → 候選 3，納入 []，排除 [(32, 'already among the retrieved sources'), (33, 'already among the retrieved sources'), (34, 'supplementary cap reached')]
  - ✓ Table 3 | need: extracted claims for C2 and SS in Podcast and News | priority: supplementary | status: missing → 候選 3，納入 []，排除 [(32, 'already among the retrieved sources'), (33, 'already among the retrieved sources'), (34, 'supplementary cap reached')]
  - ✓ Section 4.1.1 Datasets | need: dataset descriptions for Podcast and News | priority: supplementary | status: missing → 候選 2，納入 [21, 20]，排除 []
- 分析狀態：UNCERTAIN；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 修正：[]；刪除 []；仍不符 []；方向待定 []
- 涵蓋判定：Section 5.1 Experiment 1→partial；Section 5.1 Experiment 1→partial；Table 2→missing；Section 5.2 Experiment 2→partial；Table 3→covered；Section 4.1.1 Datasets→missing；required 未納入 []；supplementary 用 2；Matrix {'cells': 0, 'tables': [], 'definitions': []}
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 ['5.96', '6.39']

```text
The question asks to compare condition C2 with vector RAG (SS) on the comprehensiveness metric for the Podcast and News datasets. 

From the data in Table 3, the average number of extracted claims for condition C2 in the Podcast dataset is 32.46, and for the News dataset is 31.62 [2]. For vector RAG (SS), the average number of extracted claims for the Podcast dataset is 26.50, and for the News dataset is 25.23 [2]. These figures indicate that condition C2 outperforms vector RAG (SS) in comprehensiveness for both datasets. Specifically, in the Podcast dataset, the comprehensiveness of C2 is higher by 5.96 claims compared to SS, and in the News dataset, the comprehensiveness of C2 is higher by 6.39 claims compared to SS [2]. 

There are no exceptions reported for these comparisons, and the differences were statistically significant (p < .05) in all cases [2]. Therefore, condition C2 demonstrates a consistent improvement in comprehensiveness over vector RAG (SS) in both the Podcast and News datasets.

Numbers that could not be checked against the cited pages of the original text: 5.96, 6.39.
```

## B4-G2-2

- 問題：`Compare condition C2 with vector RAG (SS) on comprehensiveness in the Podcast and News datasets`；模式 `navigate`；23.1 秒；2 次呼叫；tokens 7534
- 來源：[1] p9 retrieval, [2] p11 retrieval, [3] p10 retrieval, [4] p11 retrieval, [5] p10 retrieval, [6] p11 navigation, [7] p10 navigation, [8] p10 navigation, [9] p9 navigation, [10] p10 navigation, [11] p10 navigation, [12] p26 navigation, [13] p26 navigation
- 閱讀計畫（定位 6/6，保留 8，超預算 0）：
  - ✓ Section 5.1 Experiment 1 | need: comprehensiveness results for Podcast dataset | priority: required | status: missing → 候選 9，納入 [29, 26]，排除 [(25, 'already among the retrieved sources'), (32, 'already among the retrieved sources'), (31, 'already among the retrieved sources'), (30, 'already among the retrieved sources'), (24, 'already selected for another target'), (28, 'already selected for another target'), (27, 'already selected for another target')]
  - ✓ Section 5.1 Experiment 1 | need: comprehensiveness results for News dataset | priority: required | status: missing → 候選 9，納入 [24, 28, 27]，排除 [(25, 'already among the retrieved sources'), (32, 'already among the retrieved sources'), (31, 'already among the retrieved sources'), (30, 'already among the retrieved sources'), (29, 'already selected for another target'), (26, 'already selected for another target')]
  - ✓ Section 5.2 Experiment 2 | need: C2 vs SS comparison on comprehensiveness | priority: required | status: missing → 候選 3，納入 [34]，排除 [(32, 'already among the retrieved sources'), (33, 'already among the retrieved sources')]
  - ✓ Table 2 | need: context units for C2 and SS | priority: supplementary | status: missing → 候選 3，納入 []，排除 [(29, 'already selected for another target'), (30, 'already among the retrieved sources'), (31, 'supplementary cap reached')]
  - ✓ Table 3 | need: average extracted claims for C2 and SS | priority: supplementary | status: missing → 候選 3，納入 []，排除 [(32, 'already among the retrieved sources'), (33, 'already among the retrieved sources'), (34, 'supplementary cap reached')]
  - ✓ Table 6 | need: pairwise comparisons for C2 and SS | priority: supplementary | status: missing → 候選 3，納入 [74, 75]，排除 [(76, 'supplementary cap reached')]
- 分析狀態：UNCERTAIN；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 修正：[]；刪除 []；仍不符 []；方向待定 []
- 涵蓋判定：Section 5.1 Experiment 1→partial；Section 5.1 Experiment 1→partial；Section 5.2 Experiment 2→partial；Table 2→missing；Table 3→covered；Table 6→missing；required 未納入 []；supplementary 用 2；Matrix {'cells': 0, 'tables': [], 'definitions': []}
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
The question asks to compare condition C2 with vector RAG (SS) on comprehensiveness in the Podcast and News datasets.

For the Podcast dataset, condition C2 achieved comprehensiveness win rates of 77.76% over SS, with a statistically significant difference (p < 0.001) as shown in Table 6 [12]. The mean score for C2 was 77.76, while for SS it was 22.24 [12].

For the News dataset, condition C2 achieved comprehensiveness win rates of 79.2% over SS, with a statistically significant difference (p < 0.001) as shown in Table 6 [12]. The mean score for C2 was 79.2, while for SS it was 20.8 [12].

In both datasets, condition C2 outperformed vector RAG (SS) in comprehensiveness.
```

## B4-G2-3

- 問題：`Compare condition C2 with vector RAG (SS) on comprehensiveness in the Podcast and News datasets`；模式 `navigate`；22.0 秒；2 次呼叫；tokens 6698
- 來源：[1] p9 retrieval, [2] p11 retrieval, [3] p10 retrieval, [4] p11 retrieval, [5] p10 retrieval, [6] p10 navigation, [7] p10 navigation, [8] p10 navigation, [9] p10 navigation, [10] p9 navigation, [11] p11 navigation
- 閱讀計畫（定位 6/6，保留 6，超預算 0）：
  - ✓ Section 5.1 Experiment 1 | need: comprehensiveness results for C2 and SS in Podcast | priority: required | status: missing → 候選 9，納入 [29, 26, 24]，排除 [(32, 'already among the retrieved sources'), (25, 'already among the retrieved sources'), (31, 'already among the retrieved sources'), (30, 'already among the retrieved sources'), (28, 'already selected for another target'), (27, 'already selected for another target')]
  - ✓ Section 5.1 Experiment 1 | need: comprehensiveness results for C2 and SS in News | priority: required | status: missing → 候選 9，納入 [28, 27]，排除 [(32, 'already among the retrieved sources'), (25, 'already among the retrieved sources'), (29, 'already selected for another target'), (31, 'already among the retrieved sources'), (30, 'already among the retrieved sources'), (26, 'already selected for another target'), (24, 'already selected for another target')]
  - ✓ Table 2 | need: context units for C2 and SS in Podcast | priority: supplementary | status: missing → 候選 3，納入 []，排除 [(29, 'already selected for another target'), (30, 'already among the retrieved sources'), (31, 'already among the retrieved sources')]
  - ✓ Table 2 | need: context units for C2 and SS in News | priority: supplementary | status: missing → 候選 3，納入 []，排除 [(29, 'already selected for another target'), (30, 'already among the retrieved sources'), (31, 'already among the retrieved sources')]
  - ✓ Section 5.1 Experiment 1 | need: token usage for C2 and SS | priority: supplementary | status: covered → 候選 9，納入 []，排除 [(32, 'already among the retrieved sources'), (29, 'already selected for another target'), (30, 'already among the retrieved sources'), (25, 'already among the retrieved sources'), (26, 'already selected for another target'), (31, 'already among the retrieved sources'), (28, 'already selected for another target'), (27, 'already selected for another target'), (24, 'already selected for another target')]
  - ✓ Section 5.2 Experiment 2 | need: cluster counts for C2 and SS | priority: supplementary | status: missing → 候選 3，納入 [34]，排除 [(32, 'already among the retrieved sources'), (33, 'already among the retrieved sources')]
- 分析狀態：UNCERTAIN；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 修正：[]；刪除 []；仍不符 []；方向待定 []
- 涵蓋判定：Section 5.1 Experiment 1→partial；Section 5.1 Experiment 1→partial；Table 2→missing；Table 2→missing；Section 5.1 Experiment 1→partial；Section 5.2 Experiment 2→partial；required 未納入 []；supplementary 用 1；Matrix {'cells': 0, 'tables': [], 'definitions': []}
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
Condition C2 and vector RAG (SS) were compared on the comprehensiveness metric for both the Podcast and News datasets. 

For the Podcast dataset, comprehensiveness win rates for C2 over SS were 72-83% (p<.001) [1]. The average number of extracted claims for C2 was 32.46, compared to 25.23 for SS, showing a clear improvement [2].

For the News dataset, comprehensiveness win rates for C2 over SS were 72-80% (p<.001) [1]. The average number of extracted claims for C2 was 31.62, compared to 25.23 for SS, also indicating a clear improvement [2].

In both datasets, the comprehensiveness of C2 was significantly higher than that of SS [1].
```

## B4b-G2-1

- 問題：`Compare condition C2 with vector RAG (SS) on comprehensiveness in the Podcast and News datasets`；模式 `navigate`；32.3 秒；2 次呼叫；tokens 6948
- 來源：[1] p9 retrieval, [2] p11 retrieval, [3] p10 retrieval, [4] p11 retrieval, [5] p10 retrieval, [6] p10 navigation, [7] p10 navigation, [8] p10 navigation, [9] p10 navigation, [10] p9 navigation, [11] p11 navigation
- 閱讀計畫（定位 6/6，保留 6，超預算 0）：
  - ✓ Section 5.1 Experiment 1 | need: comprehensiveness results for C2 and SS in Podcast | priority: required | status: missing → 候選 9，納入 [29, 26, 24]，排除 [(32, 'already among the retrieved sources'), (25, 'already among the retrieved sources'), (31, 'already among the retrieved sources'), (30, 'already among the retrieved sources'), (28, 'already selected for another target'), (27, 'already selected for another target')]
  - ✓ Section 5.1 Experiment 1 | need: comprehensiveness results for C2 and SS in News | priority: required | status: missing → 候選 9，納入 [28, 27]，排除 [(32, 'already among the retrieved sources'), (25, 'already among the retrieved sources'), (29, 'already selected for another target'), (31, 'already among the retrieved sources'), (30, 'already among the retrieved sources'), (26, 'already selected for another target'), (24, 'already selected for another target')]
  - ✓ Table 2 | need: context units used for C2 and SS in Podcast | priority: supplementary | status: missing → 候選 3，納入 []，排除 [(29, 'already selected for another target'), (30, 'already among the retrieved sources'), (31, 'already among the retrieved sources')]
  - ✓ Table 2 | need: context units used for C2 and SS in News | priority: supplementary | status: missing → 候選 3，納入 []，排除 [(29, 'already selected for another target'), (30, 'already among the retrieved sources'), (31, 'already among the retrieved sources')]
  - ✓ Section 5.1 Experiment 1 | need: token count comparison for C2 and SS | priority: supplementary | status: covered → 候選 9，納入 []，排除 [(32, 'already among the retrieved sources'), (29, 'already selected for another target'), (25, 'already among the retrieved sources'), (30, 'already among the retrieved sources'), (31, 'already among the retrieved sources'), (26, 'already selected for another target'), (28, 'already selected for another target'), (27, 'already selected for another target'), (24, 'already selected for another target')]
  - ✓ Section 5.2 Experiment 2 | need: additional cluster count data for C2 vs SS | priority: supplementary | status: missing → 候選 3，納入 [34]，排除 [(32, 'already among the retrieved sources'), (33, 'already among the retrieved sources')]
- 分析狀態：UNCERTAIN；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 修正：[]；刪除 []；仍不符 []；方向待定 []
- 涵蓋判定：Section 5.1 Experiment 1→partial；Section 5.1 Experiment 1→partial；Table 2→missing；Table 2→missing；Section 5.1 Experiment 1→partial；Section 5.2 Experiment 2→partial；required 未納入 []；supplementary 用 1；Matrix {'cells': 0, 'tables': [], 'definitions': []}
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
The question asks to compare condition C2 with vector RAG (SS) on the metric of comprehensiveness in the Podcast and News datasets.

The method for measuring comprehensiveness is defined as the average number of claims extracted from the answers generated under each condition [10]. The datasets in question are the Podcast and News datasets [1].

In the Podcast dataset, the comprehensiveness of condition C2 is reported as 72-83% win rate over SS (p<.001) [1]. In the News dataset, the comprehensiveness of condition C2 is reported as 72-80% win rate over SS (p <.001) [1]. Additionally, Table 3 shows that for the Podcast dataset, C2 had an average number of claims of 32.46, while SS had 26.50 [2]. For the News dataset, C2 had an average number of claims of 31.62, while SS had 25.23 [2].

The comparison shows that in both the Podcast and News datasets, condition C2 outperforms vector RAG (SS) in terms of comprehensiveness. In the Podcast dataset, the win rate of C2 over SS is 72-83% (p<.001) [1], and the average number of claims for C2 is 32.46 compared to 26.50 for SS [2]. In the News dataset, the win rate of C2 over SS is 72-80% (p <.001) [1], and the average number of claims for C2 is 31.62 compared to 25.23 for SS [2]. There are no results reported that contradict this trend for the specific pairing of C2 and SS in the given datasets and metric. Therefore, the conclusion is that condition C2 significantly outperforms vector RAG (SS) in comprehensiveness for both the Podcast and News datasets.
```

## B4b-G2-2

- 問題：`Compare condition C2 with vector RAG (SS) on comprehensiveness in the Podcast and News datasets`；模式 `navigate`；26.1 秒；2 次呼叫；tokens 7390
- 來源：[1] p9 retrieval, [2] p11 retrieval, [3] p10 retrieval, [4] p11 retrieval, [5] p10 retrieval, [6] p10 navigation, [7] p10 navigation, [8] p10 navigation, [9] p10 navigation, [10] p9 navigation, [11] p26 navigation, [12] p26 navigation
- 閱讀計畫（定位 6/6，保留 7，超預算 0）：
  - ✓ Section 5.1 Experiment 1 | need: comprehensiveness results for C2 and SS in Podcast | priority: required | status: missing → 候選 9，納入 [29, 26, 24]，排除 [(32, 'already among the retrieved sources'), (25, 'already among the retrieved sources'), (31, 'already among the retrieved sources'), (30, 'already among the retrieved sources'), (28, 'already selected for another target'), (27, 'already selected for another target')]
  - ✓ Section 5.1 Experiment 1 | need: comprehensiveness results for C2 and SS in News | priority: required | status: missing → 候選 9，納入 [28, 27]，排除 [(32, 'already among the retrieved sources'), (25, 'already among the retrieved sources'), (29, 'already selected for another target'), (31, 'already among the retrieved sources'), (30, 'already among the retrieved sources'), (26, 'already selected for another target'), (24, 'already selected for another target')]
  - ✓ Table 2 | need: context units for C2 and SS in Podcast and News | priority: supplementary | status: covered → 候選 3，納入 []，排除 [(29, 'already selected for another target'), (30, 'already among the retrieved sources'), (31, 'supplementary cap reached')]
  - ✓ Section 5.2 Experiment 2 | need: cluster counts for C2 and SS in Podcast and News | priority: supplementary | status: missing → 候選 3，納入 []，排除 [(32, 'already among the retrieved sources'), (33, 'supplementary cap reached'), (34, 'supplementary cap reached')]
  - ✓ Table 3 | need: extracted claims for C2 and SS in Podcast and News | priority: supplementary | status: covered → 候選 3，納入 []，排除 [(32, 'already among the retrieved sources'), (33, 'already among the retrieved sources'), (34, 'supplementary cap reached')]
  - ✓ Table 6 | need: pairwise comparisons for C2 vs SS on comprehensiveness | priority: supplementary | status: missing → 候選 3，納入 [74, 75]，排除 [(76, 'supplementary cap reached')]
- 分析狀態：UNCERTAIN；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 修正：[]；刪除 []；仍不符 []；方向待定 []
- 涵蓋判定：Section 5.1 Experiment 1→partial；Section 5.1 Experiment 1→partial；Table 2→missing；Section 5.2 Experiment 2→partial；Table 3→covered；Table 6→missing；required 未納入 []；supplementary 用 2；Matrix {'cells': 0, 'tables': [], 'definitions': []}
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
The question asks to compare condition C2 with vector RAG (SS) on comprehensiveness in the Podcast and News datasets. The metric is comprehensiveness, measured as the average number of extracted claims or the win rate in pairwise comparisons, and the methods are condition C2 and vector RAG (SS).

In the Podcast dataset, condition C2 outperformed SS in comprehensiveness. The pairwise comparison win rate for C2 over SS was 77.76% (p < 0.001) [11]. Additionally, the average number of extracted claims for C2 was 31.62, while for SS it was 25.23, indicating a higher comprehensiveness for C2 [2].

In the News dataset, condition C2 similarly outperformed SS in comprehensiveness. The pairwise comparison win rate for C2 over SS was 79.2% (p < 0.001) [11]. The average number of extracted claims for C2 was 31.62, while for SS it was 25.23, showing a higher comprehensiveness for C2 [2].

No exceptions or conflicting results were observed for this comparison in the given datasets.
```

## B4b-G2-3

- 問題：`Compare condition C2 with vector RAG (SS) on comprehensiveness in the Podcast and News datasets`；模式 `navigate`；23.4 秒；2 次呼叫；tokens 7325
- 來源：[1] p9 retrieval, [2] p11 retrieval, [3] p10 retrieval, [4] p11 retrieval, [5] p10 retrieval, [6] p10 navigation, [7] p10 navigation, [8] p9 navigation, [9] p10 navigation, [10] p10 navigation, [11] p26 navigation, [12] p26 navigation
- 閱讀計畫（定位 6/6，保留 7，超預算 0）：
  - ✓ Section 5.1 Experiment 1 | need: comprehensiveness results for C2 and SS in Podcast dataset | priority: required | status: missing → 候選 9，納入 [29, 26, 24]，排除 [(25, 'already among the retrieved sources'), (32, 'already among the retrieved sources'), (31, 'already among the retrieved sources'), (30, 'already among the retrieved sources'), (28, 'target quota reached'), (27, 'target quota reached')]
  - ✓ Section 5.1 Experiment 1 | need: comprehensiveness results for C2 and SS in News dataset | priority: required | status: missing → 候選 9，納入 [28, 27]，排除 [(25, 'already among the retrieved sources'), (32, 'already among the retrieved sources'), (31, 'already among the retrieved sources'), (30, 'already among the retrieved sources'), (29, 'already selected for another target'), (26, 'already selected for another target'), (24, 'already selected for another target')]
  - ✓ Table 2 | need: context units for C2 and SS in both datasets | priority: supplementary | status: missing → 候選 3，納入 []，排除 [(29, 'already selected for another target'), (30, 'already among the retrieved sources'), (31, 'supplementary cap reached')]
  - ✓ Section 5.2 Experiment 2 | need: additional context on C2 performance vs SS | priority: supplementary | status: missing → 候選 3，納入 []，排除 [(32, 'already among the retrieved sources'), (33, 'supplementary cap reached'), (34, 'supplementary cap reached')]
  - ✓ Table 3 | need: average extracted claims for C2 and SS in both datasets | priority: supplementary | status: missing → 候選 3，納入 []，排除 [(32, 'already among the retrieved sources'), (33, 'already among the retrieved sources'), (34, 'supplementary cap reached')]
  - ✓ Table 6 | need: pairwise comparisons including C2 and SS on relevant metrics | priority: supplementary | status: missing → 候選 3，納入 [74, 75]，排除 [(76, 'supplementary cap reached')]
- 分析狀態：UNCERTAIN；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 修正：[]；刪除 []；仍不符 []；方向待定 []
- 涵蓋判定：Section 5.1 Experiment 1→partial；Section 5.1 Experiment 1→partial；Table 2→missing；Section 5.2 Experiment 2→partial；Table 3→covered；Table 6→missing；required 未納入 []；supplementary 用 2；Matrix {'cells': 0, 'tables': [], 'definitions': []}
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
Condition C2 was compared with vector RAG (SS) on comprehensiveness in both the Podcast and News datasets. The results showed that C2 outperformed SS in comprehensiveness for both datasets. In the Podcast dataset, C2 achieved a comprehensiveness win rate of 77.76%, with a mean score of 77.76 compared to SS's mean score of 22.24 (Z-value = -8.17, p < 0.001) [11]. Similarly, in the News dataset, C2 achieved a comprehensiveness win rate of 79.2%, with a mean score of 79.2 compared to SS's mean score of 20.8 (Z-value = -8.34, p < 0.001) [11]. These results indicate a statistically significant and consistent improvement of C2 over SS in comprehensiveness for both datasets.
```

## C-G2-1

- 問題：`Compare condition C2 with vector RAG (SS) on comprehensiveness in the Podcast and News datasets`；模式 `single`；12.4 秒；1 次呼叫；tokens 2411
- 來源：[1] p9 retrieval, [2] p11 retrieval, [3] p10 retrieval, [4] p11 retrieval, [5] p10 retrieval
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
Condition C2 was compared to vector RAG (SS) on comprehensiveness in both the Podcast and News datasets. For the Podcast dataset, all global search conditions, including C2, had significantly greater comprehensiveness than SS (p < .05) [2]. Similarly, for the News dataset, all global search conditions, including C2, had greater comprehensiveness than SS, and the differences were statistically significant in all cases (p < .05) [2]. However, the specific win rate for comprehensiveness for C2 is not explicitly provided in the sources. 

Additionally, in the broader comparison of global approaches to SS, comprehensiveness win rates for global approaches ranged between 72-83% (p < .001) for Podcast transcripts and 72-80% (p < .001) for News articles [1]. While these win rates include C2 as part of the global conditions, the exact win rate for C2 is not specified.

In conclusion, C2 outperformed SS in comprehensiveness for both datasets, with statistically significant differences. However, the exact comprehensiveness win rate for C2 is not provided in the sources.
```

## C-G2-2

- 問題：`Compare condition C2 with vector RAG (SS) on comprehensiveness in the Podcast and News datasets`；模式 `single`；7.9 秒；1 次呼叫；tokens 2344
- 來源：[1] p9 retrieval, [2] p11 retrieval, [3] p10 retrieval, [4] p11 retrieval, [5] p10 retrieval
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
Condition C2 was compared with vector RAG (SS) on comprehensiveness in both the Podcast and News datasets. For the Podcast dataset, all global search conditions, including C2, had greater comprehensiveness than vector RAG (SS), with statistically significant differences (p < .05) in all cases [2]. Similarly, for the News dataset, all global search conditions, including C2, outperformed vector RAG (SS) in comprehensiveness, and the differences were statistically significant (p < .05) in all cases [2]. 

There were no statistically significant differences observed among the global search conditions or between global search and source text summarization (TS) in terms of comprehensiveness [4]. 

In summary, condition C2 showed better comprehensiveness than vector RAG (SS) in both the Podcast and News datasets, with statistically significant results.
```

## C-G2-3

- 問題：`Compare condition C2 with vector RAG (SS) on comprehensiveness in the Podcast and News datasets`；模式 `single`；8.7 秒；1 次呼叫；tokens 2364
- 來源：[1] p9 retrieval, [2] p11 retrieval, [3] p10 retrieval, [4] p11 retrieval, [5] p10 retrieval
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
Condition C2 was compared with vector RAG (SS) on comprehensiveness in both the Podcast and News datasets. In the Podcast dataset, all global search conditions, including C2, had greater comprehensiveness than vector RAG (SS), and the differences were statistically significant (p < .05) in all cases [2]. Similarly, in the News dataset, all global search conditions, including C2, had greater comprehensiveness than vector RAG (SS), and the differences were also statistically significant (p < .05) in all cases [2]. 

However, there were no statistically significant differences observed among the global search conditions or between global search and source text summarization (TS) for comprehensiveness [4]. 

In conclusion, while condition C2 outperformed vector RAG (SS) in comprehensiveness for both datasets, there were no statistically significant differences between C2 and other global search conditions or between C2 and source text summarization (TS).
```
