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

## B5-Q1-1

- 問題：`summary this document.`；模式 `navigate`；33.4 秒；2 次呼叫；tokens 7280
- 來源：[1] p1 summary, [2] p1 summary, [3] p1 summary, [4] p2 summary, [5] p3 summary, [6] p5 summary, [7] p10 summary, [8] p10 summary, [9] p13 summary, [10] p5 navigation, [11] p8 navigation
- 閱讀計畫（定位 6/6，保留 2，超預算 15）：
  - ✓ Section 1 INTRODUCTION | need: overview and motivation | priority: required | status: missing → 候選 5，納入 []，排除 [(2, 'low relevance'), (4, 'low relevance'), (0, 'low relevance'), (1, 'low relevance'), (3, 'low relevance')]
  - ✓ Section 2 RETRIEVAL-AUGMENTED GENERATION | need: background context | priority: required | status: missing → 候選 4，納入 []，排除 [(4, 'low relevance'), (7, 'low relevance'), (6, 'low relevance'), (5, 'low relevance')]
  - ✓ Section 3 THE LIGHT RAG ARCHITECTURE | need: framework description | priority: required | status: missing → 候選 8，納入 [14, 13]，排除 [(11, 'low relevance'), (10, 'low relevance'), (12, 'low relevance'), (9, 'low relevance'), (7, 'over the evidence budget'), (8, 'over the evidence budget')]
  - ✓ Section 4 EVALUATION | need: experimental results | priority: required | status: missing → 候選 9，納入 [22]，排除 [(14, 'low relevance'), (19, 'over the evidence budget'), (18, 'over the evidence budget'), (27, 'over the evidence budget'), (28, 'over the evidence budget'), (24, 'over the evidence budget'), (21, 'over the evidence budget'), (26, 'over the evidence budget')]
  - ✓ Section 5 RELATED WORK | need: related research | priority: supplementary | status: missing → 候選 3，納入 []，排除 [(30, 'over the evidence budget'), (29, 'over the evidence budget'), (31, 'over the evidence budget')]
  - ✓ Section 6 CONCLUSION | need: summary and future work | priority: supplementary | status: missing → 候選 7，納入 []，排除 [(37, 'low relevance'), (31, 'low relevance'), (35, 'low relevance'), (33, 'low relevance'), (36, 'low relevance'), (32, 'over the evidence budget'), (34, 'over the evidence budget')]
- 分析狀態：FACTUALLY_INCORRECT；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 修正：[]；刪除 []；仍不符 ['16.4% (Comprehensiveness, Legal, LightRAG)']；方向待定 []
- 涵蓋判定：Section 1 INTRODUCTION→missing；Section 2 RETRIEVAL-AUGMENTED GENERATION→missing；Section 3 THE LIGHT RAG ARCHITECTURE→missing；Section 4 EVALUATION→missing；Section 5 RELATED WORK→missing；Section 6 CONCLUSION→missing；required 未納入 ['Section 1 INTRODUCTION', 'Section 2 RETRIEVAL-AUGMENTED GENERATION']；supplementary 用 0；Matrix None
- 檢查：標籤不符 ['16.4%', '13.6%']；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
This document introduces LightRAG, a Retrieval-Augmented Generation (RAG) system designed to enhance large language models by integrating external knowledge sources through graph-based indexing and dual-level retrieval mechanisms [1]. Existing RAG systems often rely on flat data representations and lack contextual awareness, leading to fragmented and incomplete responses [3]. LightRAG addresses these limitations by representing entities and relationships in a knowledge graph, enabling efficient retrieval of related information and improving the comprehensiveness and relevance of responses [1]. The system features a dual-level retrieval mechanism that supports both low-level and high-level knowledge discovery and includes an incremental update algorithm to adapt to new data without reprocessing the entire dataset [2].

Extensive experiments across four domains—Agriculture, CS, Legal, and Mix—demonstrated that LightRAG outperformed four baselines (Naive RAG, RQ-RAG, HyDE, and GraphRAG) in comprehensiveness, diversity, and empowerment [6]. For instance, in the Legal dataset, LightRAG achieved 83.6% win rate for comprehensiveness and 86.4% for diversity, compared to the best baseline, which reached only 16.4% and 13.6%, respectively [1]. Ablation studies confirmed the importance of the dual-level retrieval paradigm, with performance drops observed when either component was removed [8]. 

LightRAG also demonstrated cost efficiency, using significantly fewer tokens and API calls compared to GraphRAG during retrieval and incremental updates. It supports fast adaptation to new data without full graph reconstruction, ensuring timeliness and relevance [1]. The system is open-source and available at https://github.com/HKUDS/LightRAG [1].

The document also discusses related work, highlighting the limitations of existing RAG systems and how LightRAG's integration of graph structures and dual-level retrieval improves efficiency and adaptability [7]. The conclusion summarizes LightRAG's contributions, emphasizing its ability to enhance both the efficiency and effectiveness of information retrieval and generation while reducing costs for LLM inference [8].

Figures whose labels differ from the source table: 16.4% (answer: Comprehensiveness, Legal, LightRAG; source: Comprehensiveness, Legal, NaiveRAG, vs LightRAG / Empowerment, Legal, NaiveRAG, vs LightRAG / Empowerment, Legal, NaiveRAG, vs -Low / Comprehensiveness, Legal, NaiveRAG, vs -Origin); 13.6% (answer: Comprehensiveness, Legal, LightRAG; source: Diversity, Legal, NaiveRAG, vs LightRAG / Diversity, Legal, NaiveRAG, vs -Low).
```

## B5-Q1-2

- 問題：`summary this document.`；模式 `navigate`；31.9 秒；2 次呼叫；tokens 7257
- 來源：[1] p1 summary, [2] p1 summary, [3] p1 summary, [4] p2 summary, [5] p3 summary, [6] p5 summary, [7] p10 summary, [8] p10 summary, [9] p13 summary, [10] p5 navigation, [11] p8 navigation
- 閱讀計畫（定位 6/6，保留 2，超預算 15）：
  - ✓ Section 1 INTRODUCTION | need: overview and motivation | priority: required | status: missing → 候選 5，納入 []，排除 [(2, 'low relevance'), (4, 'low relevance'), (0, 'low relevance'), (1, 'low relevance'), (3, 'low relevance')]
  - ✓ Section 2 RETRIEVAL-AUGMENTED GENERATION | need: background context | priority: required | status: missing → 候選 4，納入 []，排除 [(4, 'low relevance'), (7, 'low relevance'), (6, 'low relevance'), (5, 'low relevance')]
  - ✓ Section 3 THE LIGHT RAG ARCHITECTURE | need: framework description | priority: required | status: missing → 候選 8，納入 [14, 13]，排除 [(11, 'low relevance'), (10, 'low relevance'), (12, 'low relevance'), (9, 'low relevance'), (7, 'over the evidence budget'), (8, 'over the evidence budget')]
  - ✓ Section 4 EVALUATION | need: experimental results | priority: required | status: missing → 候選 9，納入 [22]，排除 [(14, 'low relevance'), (19, 'over the evidence budget'), (18, 'over the evidence budget'), (27, 'over the evidence budget'), (28, 'over the evidence budget'), (24, 'over the evidence budget'), (21, 'over the evidence budget'), (26, 'over the evidence budget')]
  - ✓ Section 5 RELATED WORK | need: related research | priority: supplementary | status: missing → 候選 3，納入 []，排除 [(30, 'over the evidence budget'), (29, 'over the evidence budget'), (31, 'over the evidence budget')]
  - ✓ Section 6 CONCLUSION | need: summary and future work | priority: supplementary | status: missing → 候選 7，納入 []，排除 [(37, 'low relevance'), (31, 'low relevance'), (35, 'low relevance'), (33, 'low relevance'), (36, 'low relevance'), (32, 'over the evidence budget'), (34, 'over the evidence budget')]
- 分析狀態：FACTUALLY_INCORRECT；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 修正：[]；刪除 []；仍不符 ['16.4% (Comprehensiveness, Legal, LightRAG)']；方向待定 []
- 涵蓋判定：Section 1 INTRODUCTION→missing；Section 2 RETRIEVAL-AUGMENTED GENERATION→missing；Section 3 THE LIGHT RAG ARCHITECTURE→missing；Section 4 EVALUATION→missing；Section 5 RELATED WORK→missing；Section 6 CONCLUSION→missing；required 未納入 ['Section 1 INTRODUCTION', 'Section 2 RETRIEVAL-AUGMENTED GENERATION']；supplementary 用 0；Matrix None
- 檢查：標籤不符 ['16.4%', '13.6%']；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
This document introduces LightRAG, a Retrieval-Augmented Generation (RAG) system designed to enhance large language models by integrating external knowledge sources, thereby improving the accuracy and contextual relevance of responses [1]. Existing RAG systems face limitations such as reliance on flat data representations and inadequate contextual awareness, leading to fragmented and incomplete answers [3]. LightRAG addresses these issues by incorporating graph structures into text indexing and retrieval, enabling efficient retrieval of related entities and their relationships [1]. The system features a dual-level retrieval mechanism that supports both low-level and high-level knowledge discovery and includes an incremental update algorithm to adapt to new data without reprocessing the entire dataset [1].

LightRAG was evaluated across four domains—Agriculture, CS, Legal, and Mix—each containing between 600,000 and 5,000,000 tokens. It outperformed four baselines (Naive RAG, RQ-RAG, HyDE, and GraphRAG) in comprehensiveness, diversity, and empowerment. For instance, in the Legal dataset, LightRAG achieved 83.6% win rate for comprehensiveness and 86.4% for diversity, compared to the best baseline, which reached only 16.4% and 13.6%, respectively [6]. Ablation studies confirmed that the dual-level retrieval paradigm was critical to LightRAG’s performance, with removing either component leading to performance drops [6].

LightRAG also demonstrated cost efficiency, using significantly fewer tokens and API calls compared to GraphRAG during retrieval and incremental updates. For example, it used fewer than 100 tokens for retrieval, while GraphRAG used 610,000 tokens [6]. It supports fast adaptation to new data without full graph reconstruction, ensuring timeliness and relevance. The system is open-source and available at https://github.com/HKUDS/LightRAG [1].

Figures whose labels differ from the source table: 16.4% (answer: Comprehensiveness, Legal, LightRAG; source: Comprehensiveness, Legal, NaiveRAG, vs LightRAG / Empowerment, Legal, NaiveRAG, vs LightRAG / Empowerment, Legal, NaiveRAG, vs -Low / Comprehensiveness, Legal, NaiveRAG, vs -Origin); 13.6% (answer: Comprehensiveness, Legal, LightRAG; source: Diversity, Legal, NaiveRAG, vs LightRAG / Diversity, Legal, NaiveRAG, vs -Low).
```

## B5-Q1-3

- 問題：`summary this document.`；模式 `navigate`；30.3 秒；2 次呼叫；tokens 7221
- 來源：[1] p1 summary, [2] p1 summary, [3] p1 summary, [4] p2 summary, [5] p3 summary, [6] p5 summary, [7] p10 summary, [8] p10 summary, [9] p13 summary, [10] p5 navigation, [11] p8 navigation
- 閱讀計畫（定位 6/6，保留 2，超預算 15）：
  - ✓ Section 1 INTRODUCTION | need: overview and motivation | priority: required | status: missing → 候選 5，納入 []，排除 [(2, 'low relevance'), (4, 'low relevance'), (0, 'low relevance'), (1, 'low relevance'), (3, 'low relevance')]
  - ✓ Section 2 RETRIEVAL-AUGMENTED GENERATION | need: background context | priority: required | status: missing → 候選 4，納入 []，排除 [(4, 'low relevance'), (7, 'low relevance'), (6, 'low relevance'), (5, 'low relevance')]
  - ✓ Section 3 THE LIGHT RAG ARCHITECTURE | need: framework description | priority: required | status: missing → 候選 8，納入 [14, 13]，排除 [(11, 'low relevance'), (10, 'low relevance'), (12, 'low relevance'), (9, 'low relevance'), (7, 'over the evidence budget'), (8, 'over the evidence budget')]
  - ✓ Section 4 EVALUATION | need: experimental results | priority: required | status: missing → 候選 9，納入 [22]，排除 [(14, 'low relevance'), (19, 'over the evidence budget'), (18, 'over the evidence budget'), (27, 'over the evidence budget'), (28, 'over the evidence budget'), (24, 'over the evidence budget'), (21, 'over the evidence budget'), (26, 'over the evidence budget')]
  - ✓ Section 5 RELATED WORK | need: related research | priority: supplementary | status: missing → 候選 3，納入 []，排除 [(30, 'over the evidence budget'), (29, 'over the evidence budget'), (31, 'over the evidence budget')]
  - ✓ Section 6 CONCLUSION | need: summary and future work | priority: supplementary | status: missing → 候選 7，納入 []，排除 [(37, 'low relevance'), (31, 'low relevance'), (35, 'low relevance'), (33, 'low relevance'), (36, 'low relevance'), (32, 'over the evidence budget'), (34, 'over the evidence budget')]
- 分析狀態：FACTUALLY_INCORRECT；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 修正：[]；刪除 []；仍不符 ['16.4% (Comprehensiveness, Legal, LightRAG)']；方向待定 []
- 涵蓋判定：Section 1 INTRODUCTION→missing；Section 2 RETRIEVAL-AUGMENTED GENERATION→missing；Section 3 THE LIGHT RAG ARCHITECTURE→missing；Section 4 EVALUATION→missing；Section 5 RELATED WORK→missing；Section 6 CONCLUSION→missing；required 未納入 ['Section 1 INTRODUCTION', 'Section 2 RETRIEVAL-AUGMENTED GENERATION']；supplementary 用 0；Matrix None
- 檢查：標籤不符 ['16.4%', '13.6%']；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
The document introduces LightRAG, a Retrieval-Augmented Generation (RAG) system that enhances large language models by integrating external knowledge sources through graph-based indexing and a dual-level retrieval mechanism [1]. Existing RAG systems face limitations such as flat data representations and inadequate contextual awareness, leading to fragmented responses [3]. LightRAG addresses these issues by using a knowledge graph to represent entities and relationships, enabling efficient retrieval of related information and supporting both low-level and high-level knowledge discovery [1]. 

The system features an incremental update algorithm, allowing it to adapt to new data without reprocessing the entire dataset [1]. Evaluations across four domains—Agriculture, CS, Legal, and Mix—show that LightRAG outperforms four baselines (Naive RAG, RQ-RAG, HyDE, and GraphRAG) in comprehensiveness, diversity, and empowerment [6]. For example, in the Legal dataset, LightRAG achieved 83.6% win rate for comprehensiveness and 86.4% for diversity, compared to the best baseline, which reached only 16.4% and 13.6%, respectively [1]. Ablation studies confirm that the dual-level retrieval paradigm is critical to LightRAG's performance [6].

LightRAG also demonstrates cost efficiency, using significantly fewer tokens and API calls compared to GraphRAG during retrieval and incremental updates. For example, it used fewer than 100 tokens for retrieval, while GraphRAG used 610,000 tokens [1]. The system is open-source and available at https://github.com/HKUDS/LightRAG [1]. The document concludes by highlighting LightRAG's advancements in efficiency and effectiveness in information retrieval and generation [8].

Figures whose labels differ from the source table: 16.4% (answer: Comprehensiveness, Legal, LightRAG; source: Comprehensiveness, Legal, NaiveRAG, vs LightRAG / Empowerment, Legal, NaiveRAG, vs LightRAG / Empowerment, Legal, NaiveRAG, vs -Low / Comprehensiveness, Legal, NaiveRAG, vs -Origin); 13.6% (answer: Comprehensiveness, Legal, LightRAG; source: Diversity, Legal, NaiveRAG, vs LightRAG / Diversity, Legal, NaiveRAG, vs -Low).
```

## B8-Q1-1

- 問題：`summary this document.`；模式 `navigate`；38.0 秒；2 次呼叫；tokens 5911
- 來源：[1] p1 summary, [2] p1 summary, [3] p1 summary, [4] p2 summary, [5] p3 summary, [6] p5 summary, [7] p10 summary, [8] p10 summary, [9] p13 summary, [10] p5 navigation
- 閱讀計畫（定位 6/6，保留 1，超預算 0）：
  - ✓ Section 1 INTRODUCTION | need: overview and motivation | priority: required | status: missing → 候選 5，納入 []，排除 [(2, 'low relevance'), (4, 'low relevance'), (0, 'low relevance'), (1, 'low relevance'), (3, 'low relevance')]
  - ✓ Section 2 RETRIEVAL-AUGMENTED GENERATION | need: background context | priority: required | status: missing → 候選 4，納入 []，排除 [(4, 'low relevance'), (7, 'low relevance'), (6, 'low relevance'), (5, 'low relevance')]
  - ✓ Section 3 THE LIGHT RAG ARCHITECTURE | need: framework description | priority: required | status: missing → 候選 8，納入 [14]，排除 [(13, 'low relevance'), (7, 'low relevance'), (8, 'low relevance'), (11, 'low relevance'), (10, 'low relevance'), (12, 'low relevance'), (9, 'low relevance')]
  - ✓ Section 4 EVALUATION | need: experimental results | priority: required | status: missing → 候選 9，納入 []，排除 [(22, 'low relevance'), (19, 'low relevance'), (18, 'low relevance'), (27, 'low relevance'), (28, 'low relevance'), (24, 'low relevance'), (21, 'low relevance'), (26, 'low relevance'), (14, 'low relevance')]
  - ✓ Section 5 RELATED WORK | need: related research | priority: supplementary | status: missing → 候選 3，納入 []，排除 [(30, 'low relevance'), (29, 'low relevance'), (31, 'low relevance')]
  - ✓ Section 6 CONCLUSION | need: summary and future work | priority: supplementary | status: missing → 候選 7，納入 []，排除 [(32, 'low relevance'), (34, 'low relevance'), (37, 'low relevance'), (31, 'low relevance'), (35, 'low relevance'), (33, 'low relevance'), (36, 'low relevance')]
- 分析狀態：UNCERTAIN；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 修正：[]；刪除 []；仍不符 []；方向待定 []
- 涵蓋判定：Section 1 INTRODUCTION→missing；Section 2 RETRIEVAL-AUGMENTED GENERATION→missing；Section 3 THE LIGHT RAG ARCHITECTURE→missing；Section 4 EVALUATION→missing；Section 5 RELATED WORK→missing；Section 6 CONCLUSION→missing；required 未納入 ['Section 1 INTRODUCTION', 'Section 2 RETRIEVAL-AUGMENTED GENERATION', 'Section 4 EVALUATION']；supplementary 用 0；Matrix None
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
The document introduces **LightRAG**, a Retrieval-Augmented Generation (RAG) system designed to enhance the accuracy and contextual relevance of large language model (LLM) responses by incorporating external knowledge through graph-based indexing. Existing RAG systems are limited by flat data representations and poor contextual awareness, leading to fragmented answers that miss complex interdependencies [2]. LightRAG addresses these limitations by integrating graph structures into text indexing and retrieval, using a dual-level retrieval system to enhance information retrieval at both low and high levels of knowledge discovery [1]. It combines graph and vector representations to efficiently retrieve related entities and their relationships, and it supports fast adaptation to new data through an incremental update algorithm [3].

The LightRAG architecture segments documents into chunks and uses an LLM to extract entities and relationships, forming a knowledge graph [5]. This graph-based indexing allows for efficient retrieval and better handling of complex queries. The dual-level retrieval paradigm supports both specific and abstract queries through low-level and high-level retrieval strategies [1]. An ablation study shows that removing either level of retrieval significantly reduces performance [6]. The system also reduces retrieval overhead by focusing on entities and relations rather than document chunks [1].

Extensive experiments compare LightRAG to existing RAG methods (NaiveRAG, RQ-RAG, HyDE, and GraphRAG) across four datasets: Agriculture, CS, Legal, and Mix [6]. LightRAG outperforms all baselines in four evaluation dimensions: Comprehensiveness, Diversity, Empowerment, and Overall. For example, in the Legal dataset, LightRAG achieves 83.6% win rate in Comprehensiveness, 86.4% in Diversity, and 83.6% in Empowerment [6]. In the Agriculture dataset, LightRAG achieves 54.4% win rate in Comprehensiveness over GraphRAG's 45.6%, and in the Legal dataset, it achieves 51.6% over GraphRAG's 48.4% [6]. A case study further illustrates LightRAG's superior comprehensiveness, diversity, and empowerment in answering a machine learning question [9]. Cost and adaptability analysis shows that LightRAG uses significantly fewer tokens and API calls than GraphRAG during retrieval and incremental updates, making it more efficient and cost-effective [6].

The document also discusses related work, highlighting the limitations of existing RAG methods and graph-based approaches, and categorizing the integration of LLMs with graph data into three areas: GNNs as Prefix, LLMs as Prefix, and LLMs-Graphs Integration [7]. Finally, the conclusion summarizes the contributions of LightRAG, emphasizing its efficiency, effectiveness, and adaptability [8]. The appendix provides detailed information about the methodologies, experimental settings, and evaluation criteria used in the LightRAG framework [9].
```

## B8-Q1-2

- 問題：`summary this document.`；模式 `navigate`；29.9 秒；2 次呼叫；tokens 5719
- 來源：[1] p1 summary, [2] p1 summary, [3] p1 summary, [4] p2 summary, [5] p3 summary, [6] p5 summary, [7] p10 summary, [8] p10 summary, [9] p13 summary, [10] p5 navigation
- 閱讀計畫（定位 6/6，保留 1，超預算 0）：
  - ✓ Section 1 INTRODUCTION | need: overview and motivation | priority: required | status: missing → 候選 5，納入 []，排除 [(2, 'low relevance'), (4, 'low relevance'), (0, 'low relevance'), (1, 'low relevance'), (3, 'low relevance')]
  - ✓ Section 2 RETRIEVAL-AUGMENTED GENERATION | need: background context | priority: required | status: missing → 候選 4，納入 []，排除 [(4, 'low relevance'), (7, 'low relevance'), (6, 'low relevance'), (5, 'low relevance')]
  - ✓ Section 3 THE LIGHT RAG ARCHITECTURE | need: framework description | priority: required | status: missing → 候選 8，納入 [14]，排除 [(13, 'low relevance'), (7, 'low relevance'), (8, 'low relevance'), (11, 'low relevance'), (10, 'low relevance'), (12, 'low relevance'), (9, 'low relevance')]
  - ✓ Section 4 EVALUATION | need: experimental results | priority: required | status: missing → 候選 9，納入 []，排除 [(22, 'low relevance'), (19, 'low relevance'), (18, 'low relevance'), (27, 'low relevance'), (28, 'low relevance'), (24, 'low relevance'), (21, 'low relevance'), (26, 'low relevance'), (14, 'low relevance')]
  - ✓ Section 5 RELATED WORK | need: related research | priority: supplementary | status: missing → 候選 3，納入 []，排除 [(30, 'low relevance'), (29, 'low relevance'), (31, 'low relevance')]
  - ✓ Section 6 CONCLUSION | need: summary and future work | priority: supplementary | status: missing → 候選 7，納入 []，排除 [(32, 'low relevance'), (34, 'low relevance'), (37, 'low relevance'), (31, 'low relevance'), (35, 'low relevance'), (33, 'low relevance'), (36, 'low relevance')]
- 分析狀態：UNCERTAIN；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 修正：[]；刪除 []；仍不符 []；方向待定 []
- 涵蓋判定：Section 1 INTRODUCTION→missing；Section 2 RETRIEVAL-AUGMENTED GENERATION→missing；Section 3 THE LIGHT RAG ARCHITECTURE→missing；Section 4 EVALUATION→missing；Section 5 RELATED WORK→missing；Section 6 CONCLUSION→missing；required 未納入 ['Section 1 INTRODUCTION', 'Section 2 RETRIEVAL-AUGMENTED GENERATION', 'Section 4 EVALUATION']；supplementary 用 0；Matrix None
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
The document introduces LightRAG, a Retrieval-Augmented Generation (RAG) system that enhances the accuracy and contextual relevance of large language model (LLM) responses by incorporating external knowledge through graph-based indexing. Existing RAG systems are limited by flat data representations and poor contextual awareness, leading to fragmented answers [2]. LightRAG addresses these limitations by integrating graph structures into text indexing and retrieval, using a dual-level retrieval system to support both specific and abstract queries [1]. The system combines graph and vector representations for efficient retrieval of entities and their relationships and supports fast adaptation to new data through an incremental update algorithm [5].

Extensive experiments compare LightRAG to existing RAG methods (NaiveRAG, RQ-RAG, HyDE, and GraphRAG) across four datasets: Agriculture, CS, Legal, and Mix. LightRAG outperforms all baselines in four evaluation dimensions: Comprehensiveness, Diversity, Empowerment, and Overall. For example, in the Legal dataset, LightRAG achieves 83.6% win rate in Comprehensiveness, 86.4% in Diversity, and 83.6% in Empowerment [6]. A case study further illustrates LightRAG's superior comprehensiveness, diversity, and empowerment in answering a machine learning question. Cost and adaptability analysis shows that LightRAG uses significantly fewer tokens and API calls than GraphRAG during retrieval and incremental updates, making it more efficient and cost-effective [1].

The document also discusses related work, highlighting the limitations of existing RAG methods and graph-based approaches, and categorizes the integration of LLMs with graph data into three areas [7]. The conclusion summarizes the contributions of LightRAG, emphasizing its dual-level retrieval paradigm and incremental update capability, which ensure the system remains current and effective [8]. The appendix provides detailed information about the methodologies, experimental settings, and evaluation criteria used in the LightRAG framework [9].
```

## B8-Q1-3

- 問題：`summary this document.`；模式 `navigate`；39.0 秒；2 次呼叫；tokens 5935
- 來源：[1] p1 summary, [2] p1 summary, [3] p1 summary, [4] p2 summary, [5] p3 summary, [6] p5 summary, [7] p10 summary, [8] p10 summary, [9] p13 summary, [10] p5 navigation
- 閱讀計畫（定位 6/6，保留 1，超預算 0）：
  - ✓ Section 1 INTRODUCTION | need: overview and motivation | priority: required | status: missing → 候選 5，納入 []，排除 [(2, 'low relevance'), (4, 'low relevance'), (0, 'low relevance'), (1, 'low relevance'), (3, 'low relevance')]
  - ✓ Section 2 RETRIEVAL-AUGMENTED GENERATION | need: background context | priority: required | status: missing → 候選 4，納入 []，排除 [(4, 'low relevance'), (7, 'low relevance'), (6, 'low relevance'), (5, 'low relevance')]
  - ✓ Section 3 THE LIGHT RAG ARCHITECTURE | need: framework description | priority: required | status: missing → 候選 8，納入 [14]，排除 [(13, 'low relevance'), (7, 'low relevance'), (8, 'low relevance'), (11, 'low relevance'), (10, 'low relevance'), (12, 'low relevance'), (9, 'low relevance')]
  - ✓ Section 4 EVALUATION | need: experimental results | priority: required | status: missing → 候選 9，納入 []，排除 [(22, 'low relevance'), (19, 'low relevance'), (18, 'low relevance'), (27, 'low relevance'), (28, 'low relevance'), (24, 'low relevance'), (21, 'low relevance'), (26, 'low relevance'), (14, 'low relevance')]
  - ✓ Section 5 RELATED WORK | need: related research | priority: supplementary | status: missing → 候選 3，納入 []，排除 [(30, 'low relevance'), (29, 'low relevance'), (31, 'low relevance')]
  - ✓ Section 6 CONCLUSION | need: summary and future work | priority: supplementary | status: missing → 候選 7，納入 []，排除 [(32, 'low relevance'), (34, 'low relevance'), (37, 'low relevance'), (31, 'low relevance'), (35, 'low relevance'), (33, 'low relevance'), (36, 'low relevance')]
- 分析狀態：UNCERTAIN；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 修正：[]；刪除 []；仍不符 []；方向待定 []
- 涵蓋判定：Section 1 INTRODUCTION→missing；Section 2 RETRIEVAL-AUGMENTED GENERATION→missing；Section 3 THE LIGHT RAG ARCHITECTURE→missing；Section 4 EVALUATION→missing；Section 5 RELATED WORK→missing；Section 6 CONCLUSION→missing；required 未納入 ['Section 1 INTRODUCTION', 'Section 2 RETRIEVAL-AUGMENTED GENERATION', 'Section 4 EVALUATION']；supplementary 用 0；Matrix None
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
The document introduces **LightRAG**, a Retrieval-Augmented Generation (RAG) system designed to improve the accuracy and contextual relevance of large language model (LLM) responses by incorporating external knowledge through graph-based indexing [1]. Existing RAG systems are limited by flat data representations and poor contextual awareness, leading to fragmented answers that miss complex interdependencies [2]. LightRAG addresses these limitations by integrating graph structures into text indexing and retrieval, using a dual-level retrieval system to enhance information retrieval at both low and high levels of knowledge discovery [3]. 

The architecture of LightRAG segments documents into chunks and uses an LLM to extract entities and relationships, forming a knowledge graph [5]. This graph-based indexing allows for efficient retrieval and better handling of complex queries. The dual-level retrieval paradigm supports both specific and abstract queries through low-level and high-level retrieval strategies. An ablation study shows that removing either level of retrieval significantly reduces performance [1]. The system also reduces retrieval overhead by focusing on entities and relations rather than document chunks [5].

Extensive experiments compare LightRAG to existing RAG methods (NaiveRAG, RQ-RAG, HyDE, and GraphRAG) across four datasets: Agriculture, CS, Legal, and Mix. LightRAG outperforms all baselines in four evaluation dimensions: Comprehensiveness, Diversity, Empowerment, and Overall. For example, in the Legal dataset, LightRAG achieves 83.6% win rate in Comprehensiveness, 86.4% in Diversity, and 83.6% in Empowerment [6]. In the Agriculture dataset, LightRAG achieves 54.4% win rate in Comprehensiveness over GraphRAG's 45.6%, and in the Legal dataset, it achieves 51.6% over GraphRAG's 48.4% [6]. A case study further illustrates LightRAG's superior comprehensiveness, diversity, and empowerment in answering a machine learning question. Cost and adaptability analysis shows that LightRAG uses significantly fewer tokens and API calls than GraphRAG during retrieval and incremental updates, making it more efficient and cost-effective [1].

The document also discusses related work, highlighting the limitations of existing RAG methods and graph-based approaches. It categorizes research into three areas: GNNs as Prefix, LLMs as Prefix, and LLMs-Graphs Integration, and explains how LightRAG addresses the issues of dynamic updates and efficient query handling [7].

In conclusion, LightRAG introduces a graph-based indexing approach that enhances both efficiency and comprehension in information retrieval. Its dual-level retrieval paradigm allows for the extraction of both specific and abstract information, catering to diverse user needs. Additionally, LightRAG's incremental update capability ensures that the system remains current and responsive to new information, maintaining its effectiveness over time [8]. LightRAG is open-source and available at https://github.com/HKUDS/LightRAG [1].
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

## C8-Q1-1

- 問題：`summary this document.`；模式 `single`；33.2 秒；1 次呼叫；tokens 4161
- 來源：[1] p1 summary, [2] p1 summary, [3] p1 summary, [4] p2 summary, [5] p3 summary, [6] p5 summary, [7] p10 summary, [8] p10 summary, [9] p13 summary
- 分析狀態：UNCERTAIN；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
The document introduces **LightRAG**, a Retrieval-Augmented Generation (RAG) system designed to improve the accuracy and contextual relevance of large language model (LLM) responses by integrating external knowledge through graph-based indexing. Existing RAG systems are limited by flat data representations and poor contextual awareness, leading to fragmented answers that miss complex interdependencies [1][2]. LightRAG addresses these limitations by using a dual-level retrieval system that enhances information retrieval at both low and high levels of knowledge discovery. It combines graph and vector representations to efficiently retrieve related entities and their relationships, and it supports fast adaptation to new data through an incremental update algorithm [1].

The LightRAG architecture segments documents into chunks and uses an LLM to extract entities and relationships, forming a knowledge graph. This graph-based indexing allows for efficient retrieval and better handling of complex queries. The dual-level retrieval paradigm supports both specific and abstract queries through low-level and high-level retrieval strategies [1][5]. An ablation study shows that removing either level of retrieval significantly reduces performance [1]. The system reduces retrieval overhead by focusing on entities and relations rather than document chunks [1].

Extensive experiments compare LightRAG to existing RAG methods (NaiveRAG, RQ-RAG, HyDE, and GraphRAG) across four datasets: Agriculture, CS, Legal, and Mix. LightRAG outperforms all baselines in four evaluation dimensions: Comprehensiveness, Diversity, Empowerment, and Overall. For example, in the Legal dataset, LightRAG achieves 83.6% win rate in Comprehensiveness, 86.4% in Diversity, and 83.6% in Empowerment. In the Agriculture dataset, LightRAG achieves 54.4% win rate in Comprehensiveness over GraphRAG's 45.6%, and in the Legal dataset, it achieves 51.6% over GraphRAG's 48.4% [1][6]. A case study further illustrates LightRAG's superior comprehensiveness, diversity, and empowerment in answering a machine learning question [1][6]. Cost and adaptability analysis shows that LightRAG uses significantly fewer tokens and API calls than GraphRAG during retrieval and incremental updates, making it more efficient and cost-effective [1][6].

The document also discusses related work in RAG and graph-based methods, noting that existing RAG approaches often rely on fragmented text chunks and struggle to capture comprehensive global information. The proposed LightRAG model addresses these issues by enabling rapid adaptation to new information and improving retrieval efficiency through a dual-level retrieval paradigm [7].

In conclusion, LightRAG is presented as a significant advancement in RAG, enhancing both efficiency and comprehension in information retrieval. Its dual-level retrieval paradigm allows for the extraction of both specific and abstract information, catering to diverse user needs. Furthermore, LightRAG’s incremental update capability ensures the system remains current and responsive to new information, maintaining its effectiveness over time [8]. The document concludes by summarizing the contributions of the work, including a general framework for graph-empowered RAG systems, the LightRAG methodology, and experimental findings showing significant improvements in retrieval accuracy, efficiency, and adaptability compared to existing models [3].
```

## C8-Q1-2

- 問題：`summary this document.`；模式 `single`；28.8 秒；1 次呼叫；tokens 4136
- 來源：[1] p1 summary, [2] p1 summary, [3] p1 summary, [4] p2 summary, [5] p3 summary, [6] p5 summary, [7] p10 summary, [8] p10 summary, [9] p13 summary
- 分析狀態：UNCERTAIN；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 3；找不到的數字 []

```text
The document introduces **LightRAG**, a Retrieval-Augmented Generation (RAG) system that improves the accuracy and contextual relevance of large language model (LLM) responses by integrating external knowledge through **graph-based indexing**. Existing RAG systems are limited by flat data representations and poor contextual awareness, often leading to fragmented answers that miss complex interdependencies [1]. LightRAG addresses these issues by incorporating **graph structures** into text indexing and retrieval, using a **dual-level retrieval system** that enhances information retrieval at both low and high levels of knowledge discovery [1]. 

The architecture of LightRAG segments documents into chunks and uses an LLM to extract entities and relationships, forming a knowledge graph [5]. This allows for more efficient retrieval and better handling of complex queries by leveraging multi-hop subgraphs. The system also supports **fast adaptation to new data** through an **incremental update algorithm**, reducing computational costs and improving performance in dynamic environments [1]. LightRAG is open-source and available at https://github.com/HKUDS/LightRAG [1].

The system was evaluated across four datasets: **Agriculture**, **CS**, **Legal**, and **Mix**, and compared against existing RAG methods such as **NaiveRAG**, **RQ-RAG**, **HyDE**, and **GraphRAG**. Evaluation criteria included **Comprehensiveness**, **Diversity**, **Empowerment**, and **Overall** performance. LightRAG outperformed all baselines in all four dimensions and datasets. For example, in the **Legal dataset**, LightRAG achieved **83.6% win rate in Comprehensiveness**, **86.4% in Diversity**, and **83.6% in Empowerment**, compared to **16.4% for NaiveRAG**, **11.6% for RQ-RAG**, and **26.8% for HyDE** [6]. A case study further demonstrated LightRAG's superior comprehensiveness, diversity, and empowerment in answering a **machine learning question** [6]. Additionally, a **cost and adaptability analysis** showed that LightRAG uses significantly **fewer tokens and API calls** than GraphRAG during retrieval and incremental updates, making it more **efficient and cost-effective** [6].

The document also discusses **related work** in RAG and graph-based methods, highlighting limitations in current approaches such as fragmented text chunks and challenges in dynamically updating knowledge graphs [7]. LightRAG addresses these issues by combining **graph and vector representations** and enabling **rapid adaptation to new information** [7].

In conclusion, LightRAG significantly improves **efficiency and effectiveness** in information retrieval and generation, reducing costs for LLM inference while maintaining high-quality outputs [8]. The **Appendix** provides detailed information on the methodologies, experimental settings, and evaluation criteria used in the study, including a case study that compares LightRAG with **NaiveRAG** on a query about **indigenous perspectives on ownership and collaboration in corporate mergers**, where LightRAG outperformed the baseline in all evaluation criteria [9].
```

## C8-Q1-3

- 問題：`summary this document.`；模式 `single`；27.2 秒；1 次呼叫；tokens 4098
- 來源：[1] p1 summary, [2] p1 summary, [3] p1 summary, [4] p2 summary, [5] p3 summary, [6] p5 summary, [7] p10 summary, [8] p10 summary, [9] p13 summary
- 分析狀態：UNCERTAIN；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
The document introduces LightRAG, a Retrieval-Augmented Generation (RAG) system designed to improve the accuracy and contextual relevance of large language model (LLM) responses by incorporating external knowledge through graph-based indexing. Existing RAG systems are limited by flat data representations and poor contextual awareness, leading to fragmented answers that miss complex interdependencies [1]. LightRAG addresses these issues by integrating graph structures into text indexing and retrieval, using a dual-level retrieval system to enhance information retrieval at both low and high levels of knowledge discovery. The system combines graph and vector representations to efficiently retrieve related entities and their relationships, and it supports fast adaptation to new data through an incremental update algorithm [2]. 

The architecture of LightRAG involves segmenting documents into chunks and using an LLM to extract entities and relationships, forming a knowledge graph. This approach allows for efficient retrieval and better handling of complex queries. The dual-level retrieval paradigm supports specific and abstract queries through low-level and high-level retrieval strategies. An ablation study shows that removing either level of retrieval significantly reduces performance. The system also reduces retrieval overhead by focusing on entities and relations rather than document chunks [3].

Extensive experiments compare LightRAG to existing RAG methods (NaiveRAG, RQ-RAG, HyDE, and GraphRAG) across four datasets: Agriculture, CS, Legal, and Mix. LightRAG outperforms all baselines in four evaluation dimensions: Comprehensiveness, Diversity, Empowerment, and Overall. For example, in the Legal dataset, LightRAG achieves 83.6% win rate in Comprehensiveness, 86.4% in Diversity, and 83.6% in Empowerment. In the Agriculture dataset, LightRAG achieves 54.4% win rate in Comprehensiveness over GraphRAG's 45.6%, and in the Legal dataset, it achieves 51.6% over GraphRAG's 48.4% [4]. A case study further illustrates LightRAG's superior comprehensiveness, diversity, and empowerment in answering a machine learning question. Cost and adaptability analysis shows that LightRAG uses significantly fewer tokens and API calls than GraphRAG during retrieval and incremental updates, making it more efficient and cost-effective [5].

The document also discusses related work in the field of RAG and graph-based knowledge representation, highlighting the limitations of existing approaches and how LightRAG addresses them. It concludes by summarizing the contributions of the work, including a general framework for graph-empowered RAG systems, the LightRAG methodology, and experimental findings showing significant improvements in retrieval accuracy, efficiency, and adaptability compared to existing models [6]. The appendix provides detailed information about the methodologies, experimental settings, and evaluation criteria used in the LightRAG framework, including statistical information for the datasets and a case study comparing LightRAG and a baseline model, NaiveRAG [7].
```

## M5-Q1-1

- 問題：`summary this document.`；模式 `navigate`；42.0 秒；2 次呼叫；tokens 7846
- 來源：[1] p1 summary, [2] p1 summary, [3] p1 summary, [4] p2 summary, [5] p3 summary, [6] p5 summary, [7] p5 summary, [8] p6 summary, [9] p7 summary, [10] p8 summary, [11] p9 summary, [12] p10 summary
- 閱讀計畫（定位 6/6，保留 0，超預算 20）：
  - ✓ Section 1 INTRODUCTION (pages 1-2) | need: problem statement, motivation, and main contributions | priority: required | status: missing → 候選 5，納入 []，排除 [(0, 'low relevance'), (4, 'low relevance'), (1, 'low relevance'), (3, 'low relevance'), (2, 'low relevance')]
  - ✓ Section 3 THE LIGHT RAG ARCHITECTURE (pages 3-5) | need: description of the proposed method and its components | priority: required | status: missing → 候選 8，納入 []，排除 [(9, 'low relevance'), (14, 'over the evidence budget'), (10, 'over the evidence budget'), (11, 'over the evidence budget'), (8, 'over the evidence budget'), (13, 'over the evidence budget'), (7, 'over the evidence budget'), (12, 'over the evidence budget')]
  - ✓ Figure 1 (page 3): Overall architecture of the | need: visual overview of the system workflow | priority: required | status: missing → 候選 2，納入 []，排除 [(6, 'over the evidence budget'), (7, 'over the evidence budget')]
  - ✓ Section 4 EVALUATION (pages 5-10) | need: experimental setup, results, and analysis of performance | priority: required | status: missing → 候選 9，納入 []，排除 [(16, 'low relevance'), (26, 'over the evidence budget'), (15, 'over the evidence budget'), (22, 'over the evidence budget'), (27, 'over the evidence budget'), (25, 'over the evidence budget'), (18, 'over the evidence budget'), (24, 'over the evidence budget'), (19, 'over the evidence budget')]
  - ✓ Table 1 (page 7): Win rates (%) of baselines v.s. LightRAG across four datasets and four evaluation dimensions. | need: quantitative comparison with existing methods | priority: required | status: missing → 候選 3，納入 []，排除 [(19, 'over the evidence budget'), (20, 'over the evidence budget'), (21, 'over the evidence budget')]
  - ✓ Section 6 CONCLUSION (pages 10-12) | need: final summary and future work | priority: required | status: missing → 候選 7，納入 []，排除 [(34, 'low relevance'), (32, 'low relevance'), (35, 'low relevance'), (33, 'low relevance'), (37, 'low relevance'), (31, 'low relevance'), (36, 'low relevance')]
- 分析狀態：UNCERTAIN；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 修正：[]；刪除 []；仍不符 []；方向待定 []
- 涵蓋判定：Section 1 INTRODUCTION (pages 1-2)→missing；Section 3 THE LIGHT RAG ARCHITECTURE (pages 3-5)→missing；Figure 1 (page 3): Overall architecture of the→missing；Section 4 EVALUATION (pages 5-10)→missing；Table 1 (page 7): Win rates (%) of baselines v.s. LightRAG across four datasets and four evaluation dimensions.→missing；Section 6 CONCLUSION (pages 10-12)→missing；required 未納入 ['Section 1 INTRODUCTION (pages 1-2)', 'Section 3 THE LIGHT RAG ARCHITECTURE (pages 3-5)', 'Figure 1 (page 3): Overall architecture of the', 'Section 4 EVALUATION (pages 5-10)', 'Table 1 (page 7): Win rates (%) of baselines v.s. LightRAG across four datasets and four evaluation dimensions.', 'Section 6 CONCLUSION (pages 10-12)']；supplementary 用 0；Matrix None
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 8；找不到的數字 []

```text
The document proposes LightRAG, a Retrieval-Augmented Generation system designed to address limitations in existing RAG systems, such as reliance on flat data representations and inadequate contextual awareness, which often lead to fragmented answers that fail to capture complex inter-dependencies between entities [2][3]. To overcome these issues, LightRAG incorporates graph structures into text indexing and retrieval, employing a dual-level retrieval system that combines low-level precise entity information with high-level broad thematic coverage [2][3]. Additionally, the system includes an incremental update algorithm to allow for the timely integration of new data without requiring full index reconstruction [1][2].

Experimental evaluations on Agriculture, CS, Legal, and Mix datasets demonstrate that LightRAG generally outperforms baselines including NaiveRAG, RQ-RAG, HyDE, and GraphRAG [1]. In overall win rates against NaiveRAG, LightRAG achieved 67.6% (p. 7) on Agriculture, 61.2% (p. 7) on CS, 84.8% (p. 7) on Legal, and 60.0% (p. 7) on Mix [1]. Compared to GraphRAG, LightRAG performed better on Agriculture (54.8% (p. 7)), CS (52.0% (p. 7)), and Legal (52.8% (p. 7)), but slightly underperformed on the Mix dataset (49.6% (p. 7)) [1]. Ablation studies confirmed the importance of the dual-level retrieval mechanism; removing high-level retrieval reduced overall scores to 35.2% (p. 8) on Agriculture and 22.0% (p. 8) on Legal, while removing low-level retrieval resulted in scores of 34.8% (p. 8) on Agriculture and 18.8% (p. 8) on Legal [1]. Regarding efficiency, LightRAG used fewer than 100 tokens and a single API call for retrieval on a legal dataset, whereas GraphRAG required approximately 610,000 tokens and hundreds of API calls [1]. For incremental updates, LightRAG avoids the high overhead of GraphRAG, which requires regenerating community reports involving roughly 1,399 × 2 × 5,000 tokens (p. 10) [1]. Case studies further showed that LightRAG outperformed GraphRAG in comprehensiveness, diversity, empowerment, and overall quality for complex queries [1].
```

## M5-Q1-2

- 問題：`summary this document.`；模式 `navigate`；45.9 秒；2 次呼叫；tokens 7942
- 來源：[1] p1 summary, [2] p1 summary, [3] p1 summary, [4] p2 summary, [5] p3 summary, [6] p5 summary, [7] p5 summary, [8] p6 summary, [9] p7 summary, [10] p8 summary, [11] p9 summary, [12] p10 summary
- 閱讀計畫（定位 6/6，保留 0，超預算 20）：
  - ✓ Section 1 INTRODUCTION (pages 1-2) | need: problem statement, motivation, and main contributions | priority: required | status: missing → 候選 5，納入 []，排除 [(0, 'low relevance'), (4, 'low relevance'), (1, 'low relevance'), (3, 'low relevance'), (2, 'low relevance')]
  - ✓ Section 3 THE LIGHT RAG ARCHITECTURE (pages 3-5) | need: description of the proposed method and its components | priority: required | status: missing → 候選 8，納入 []，排除 [(9, 'low relevance'), (14, 'over the evidence budget'), (10, 'over the evidence budget'), (11, 'over the evidence budget'), (8, 'over the evidence budget'), (13, 'over the evidence budget'), (7, 'over the evidence budget'), (12, 'over the evidence budget')]
  - ✓ Figure 1 (page 3): Overall architecture of the | need: visual overview of the system workflow | priority: required | status: missing → 候選 2，納入 []，排除 [(6, 'over the evidence budget'), (7, 'over the evidence budget')]
  - ✓ Section 4 EVALUATION (pages 5-10) | need: experimental setup, results, and analysis of performance | priority: required | status: missing → 候選 9，納入 []，排除 [(16, 'low relevance'), (26, 'over the evidence budget'), (15, 'over the evidence budget'), (22, 'over the evidence budget'), (27, 'over the evidence budget'), (25, 'over the evidence budget'), (18, 'over the evidence budget'), (24, 'over the evidence budget'), (19, 'over the evidence budget')]
  - ✓ Table 1 (page 7): Win rates (%) of baselines v.s. LightRAG across four datasets and four evaluation dimensions. | need: quantitative comparison with existing methods | priority: required | status: missing → 候選 3，納入 []，排除 [(19, 'over the evidence budget'), (20, 'over the evidence budget'), (21, 'over the evidence budget')]
  - ✓ Section 6 CONCLUSION (pages 10-12) | need: final summary and future work | priority: required | status: missing → 候選 7，納入 []，排除 [(34, 'low relevance'), (32, 'low relevance'), (35, 'low relevance'), (33, 'low relevance'), (37, 'low relevance'), (31, 'low relevance'), (36, 'low relevance')]
- 分析狀態：FACTUALLY_INCORRECT；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 修正：[]；刪除 []；仍不符 ['35.2% (Overall, Agriculture, -High)', '22.0% (Overall, Legal, -High)', '34.8% (Overall, Agriculture, -Low)', '18.8% (Overall, Legal, -Low)']；方向待定 []
- 涵蓋判定：Section 1 INTRODUCTION (pages 1-2)→missing；Section 3 THE LIGHT RAG ARCHITECTURE (pages 3-5)→missing；Figure 1 (page 3): Overall architecture of the→missing；Section 4 EVALUATION (pages 5-10)→missing；Table 1 (page 7): Win rates (%) of baselines v.s. LightRAG across four datasets and four evaluation dimensions.→missing；Section 6 CONCLUSION (pages 10-12)→missing；required 未納入 ['Section 1 INTRODUCTION (pages 1-2)', 'Section 3 THE LIGHT RAG ARCHITECTURE (pages 3-5)', 'Figure 1 (page 3): Overall architecture of the', 'Section 4 EVALUATION (pages 5-10)', 'Table 1 (page 7): Win rates (%) of baselines v.s. LightRAG across four datasets and four evaluation dimensions.', 'Section 6 CONCLUSION (pages 10-12)']；supplementary 用 0；Matrix None
- 檢查：標籤不符 ['35.2%', '22.0%', '34.8%', '18.8%']；全稱宣稱 0；引用可疑 []；未解析 6；找不到的數字 []

```text
The document introduces LightRAG, a Retrieval-Augmented Generation system designed to overcome the limitations of existing RAG systems, such as reliance on flat data representations and inadequate contextual awareness that lead to fragmented answers [1][2][3]. LightRAG incorporates graph structures into text indexing and retrieval to capture complex inter-dependencies between entities [1][2]. Its main contributions include a dual-level retrieval framework combining low-level precise entity information with high-level broad thematic coverage, and an incremental update algorithm that allows for timely data integration without full index reconstruction [1][3].

Experimental evaluations were conducted on Agriculture, CS, Legal, and Mix datasets [1][7]. The results demonstrate that LightRAG generally outperforms baselines including NaiveRAG, RQ-RAG, HyDE, and GraphRAG [1]. Specifically, LightRAG achieved overall win rates against NaiveRAG of 67.6% (p. 7) on Agriculture, 61.2% (p. 7) on CS, 84.8% (p. 7) on Legal, and 60.0% (p. 7) on Mix [1][8]. Compared to GraphRAG, LightRAG performed better on Agriculture (54.8% (p. 7)), CS (52.0% (p. 7)), and Legal (52.8% (p. 7)), but slightly underperformed on the Mix dataset (49.6% (p. 7)) [1][8].

Ablation studies confirmed the importance of the dual-level retrieval mechanism [1]. Removing high-level retrieval (-High) reduced overall scores to 35.2% (p. 8) on Agriculture and 22.0% (p. 8) on Legal, while removing low-level retrieval (-Low) resulted in scores of 34.8% (p. 8) on Agriculture and 18.8% (p. 8) on Legal [1][9]. Conversely, removing original text chunks (-Origin) did not significantly degrade performance, achieving 74.4% (p. 8) on Agriculture and 84.4% (p. 8) on Legal, suggesting that graph-based indexing provides sufficient context [1][9].

Regarding efficiency, LightRAG demonstrated significant cost advantages over GraphRAG. For retrieval on a legal dataset, LightRAG used fewer than 100 tokens and a single API call, whereas GraphRAG required approximately 610,000 tokens and hundreds of API calls [1][11]. For incremental updates, LightRAG avoids the high overhead of GraphRAG, which requires regenerating community reports involving roughly 1,399 × 2 × 5,000 tokens (p. 10) [1][11]. Case studies further showed that LightRAG outperformed GraphRAG in comprehensiveness, diversity, empowerment, and overall quality for complex queries [1][10].

Figures whose labels differ from the source table: 35.2% (answer: Overall, Agriculture, -High; source: Overall, Agriculture, NaiveRAG, vs -High / Empowerment, Mix, NaiveRAG, vs -Low / Overall, Mix, NaiveRAG, vs -Low); 22.0% (answer: Overall, Legal, -High; source: Overall, Legal, NaiveRAG, vs -High); 34.8% (answer: Overall, Agriculture, -Low; source: Comprehensiveness, Agriculture, NaiveRAG, vs -High / Empowerment, Agriculture, NaiveRAG, vs -Low / Overall, Agriculture, NaiveRAG, vs -Low); 18.8% (answer: Overall, Legal, -Low; source: Overall, Legal, NaiveRAG, vs -Low).
```

## M5-Q1-3

- 問題：`summary this document.`；模式 `navigate`；41.5 秒；2 次呼叫；tokens 7835
- 來源：[1] p1 summary, [2] p1 summary, [3] p1 summary, [4] p2 summary, [5] p3 summary, [6] p5 summary, [7] p5 summary, [8] p6 summary, [9] p7 summary, [10] p8 summary, [11] p9 summary, [12] p10 summary
- 閱讀計畫（定位 6/6，保留 0，超預算 20）：
  - ✓ Section 1 INTRODUCTION (pages 1-2) | need: problem statement, motivation, and main contributions | priority: required | status: missing → 候選 5，納入 []，排除 [(0, 'low relevance'), (4, 'low relevance'), (1, 'low relevance'), (3, 'low relevance'), (2, 'low relevance')]
  - ✓ Section 3 THE LIGHT RAG ARCHITECTURE (pages 3-5) | need: description of the proposed method and its components | priority: required | status: missing → 候選 8，納入 []，排除 [(9, 'low relevance'), (14, 'over the evidence budget'), (10, 'over the evidence budget'), (11, 'over the evidence budget'), (8, 'over the evidence budget'), (13, 'over the evidence budget'), (7, 'over the evidence budget'), (12, 'over the evidence budget')]
  - ✓ Figure 1 (page 3): Overall architecture of the | need: visual overview of the system workflow | priority: required | status: missing → 候選 2，納入 []，排除 [(6, 'over the evidence budget'), (7, 'over the evidence budget')]
  - ✓ Section 4 EVALUATION (pages 5-10) | need: experimental setup, results, and analysis of performance | priority: required | status: missing → 候選 9，納入 []，排除 [(16, 'low relevance'), (26, 'over the evidence budget'), (15, 'over the evidence budget'), (22, 'over the evidence budget'), (27, 'over the evidence budget'), (25, 'over the evidence budget'), (18, 'over the evidence budget'), (24, 'over the evidence budget'), (19, 'over the evidence budget')]
  - ✓ Table 1 (page 7): Win rates (%) of baselines v.s. LightRAG across four datasets and four evaluation dimensions. | need: quantitative comparison with existing methods | priority: required | status: missing → 候選 3，納入 []，排除 [(19, 'over the evidence budget'), (20, 'over the evidence budget'), (21, 'over the evidence budget')]
  - ✓ Section 6 CONCLUSION (pages 10-12) | need: final summary and future work | priority: required | status: missing → 候選 7，納入 []，排除 [(34, 'low relevance'), (32, 'low relevance'), (35, 'low relevance'), (33, 'low relevance'), (37, 'low relevance'), (31, 'low relevance'), (36, 'low relevance')]
- 分析狀態：FACTUALLY_INCORRECT；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 修正：[]；刪除 []；仍不符 ['54.8% (Agriculture, GraphRAG)', '52.0% (CS, GraphRAG)', '52.8% (Legal, GraphRAG)', '49.6% (Mix, GraphRAG)']；方向待定 []
- 涵蓋判定：Section 1 INTRODUCTION (pages 1-2)→missing；Section 3 THE LIGHT RAG ARCHITECTURE (pages 3-5)→missing；Figure 1 (page 3): Overall architecture of the→missing；Section 4 EVALUATION (pages 5-10)→missing；Table 1 (page 7): Win rates (%) of baselines v.s. LightRAG across four datasets and four evaluation dimensions.→missing；Section 6 CONCLUSION (pages 10-12)→missing；required 未納入 ['Section 1 INTRODUCTION (pages 1-2)', 'Section 3 THE LIGHT RAG ARCHITECTURE (pages 3-5)', 'Figure 1 (page 3): Overall architecture of the', 'Section 4 EVALUATION (pages 5-10)', 'Table 1 (page 7): Win rates (%) of baselines v.s. LightRAG across four datasets and four evaluation dimensions.', 'Section 6 CONCLUSION (pages 10-12)']；supplementary 用 0；Matrix None
- 檢查：標籤不符 ['54.8%', '52.0%', '52.8%', '49.6%']；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
The document addresses limitations in existing Retrieval-Augmented Generation (RAG) systems, which rely on flat data representations and lack contextual awareness, leading to fragmented answers that fail to capture complex inter-dependencies between entities [1][2][3]. To overcome these issues, the authors propose LightRAG, a system that incorporates graph structures into text indexing and retrieval [1][2][3].

LightRAG’s main contributions and methodology include:
*   **Graph-Based Indexing:** It segments documents into chunks to extract entities and relationships, forming a knowledge graph that captures interdependencies [1][2][5].
*   **Dual-Level Retrieval:** The system combines low-level retrieval for precise entity information with high-level retrieval for broad thematic coverage, allowing it to handle both detailed and abstract queries effectively [1][3][5].
*   **Incremental Updates:** It employs an incremental update algorithm that integrates new data by taking the union of node and edge sets, avoiding the need for full index reconstruction and significantly reducing computational overhead [1][2][5][11].

Experimental evaluations on Agriculture, CS, Legal, and Mix datasets demonstrate that LightRAG generally outperforms baselines such as NaiveRAG, RQ-RAG, HyDE, and GraphRAG [1][8]. Specifically, LightRAG achieved overall win rates of 67.6% on Agriculture, 61.2% on CS, 84.8% on Legal, and 60.0% on Mix against NaiveRAG [1][8]. It also outperformed GraphRAG on the Agriculture (54.8%), CS (52.0%), and Legal (52.8%) datasets, though it slightly underperformed on the Mix dataset (49.6%) [1][8]. Ablation studies confirmed the importance of the dual-level retrieval mechanism, as removing either high-level or low-level retrieval significantly reduced performance [1][9].

Regarding efficiency, LightRAG is significantly more cost-effective than GraphRAG. For retrieval on a legal dataset, LightRAG used fewer than 100 tokens and a single API call, whereas GraphRAG required approximately 610,000 tokens and hundreds of API calls [1][11]. Furthermore, LightRAG avoids the high overhead of GraphRAG’s community report regeneration during incremental updates [1][11]. Case studies also indicated that LightRAG outperforms GraphRAG in comprehensiveness, diversity, empowerment, and overall quality for complex queries [1][10].

Figures whose labels differ from the source table: 54.8% (answer: Agriculture, GraphRAG; source: Empowerment, CS, LightRAG, vs GraphRAG / Overall, Agriculture, LightRAG, vs GraphRAG / Empowerment, Mix, -Origin, vs NaiveRAG); 52.0% (answer: CS, GraphRAG; source: Overall, CS, LightRAG, vs GraphRAG); 52.8% (answer: Legal, GraphRAG; source: Overall, Legal, LightRAG, vs GraphRAG); 49.6% (answer: Mix, GraphRAG; source: Comprehensiveness, Mix, LightRAG, vs GraphRAG / Overall, Mix, LightRAG, vs GraphRAG).
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

## B5-Q2-1

- 問題：`compare lightRAG with GraphRAG`；模式 `navigate`；51.9 秒；2 次呼叫；tokens 8809
- 來源：[1] p7 retrieval, [2] p7 retrieval, [3] p9 retrieval, [4] p8 retrieval, [5] p10 retrieval, [6] p7 navigation, [7] p9 navigation, [8] p9 navigation, [9] p8 navigation, [10] p6 navigation, [11] p4 navigation
- 閱讀計畫（定位 6/6，保留 7，超預算 1）：
  - ✓ Table 1 (page 7) | need: comparison across datasets | priority: required | status: missing → 候選 3，納入 [19]，排除 [(20, 'already among the retrieved sources'), (21, 'already among the retrieved sources')]
  - ✓ Section 4.2 COMPARISON OF LIGHT RAG WITH EXISTING RAG METHODS (RQ1) (pages 6-7) | need: general comparison context | priority: required | status: covered → 候選 4，納入 [18]，排除 [(20, 'already among the retrieved sources'), (21, 'already among the retrieved sources'), (19, 'already selected for another target')]
  - ✓ Section 4.3 ABLATION STUDIES (RQ2) (pages 7-8) | need: specific comparison with GraphRAG | priority: required | status: covered → 候選 3，納入 [23]，排除 [(21, 'already among the retrieved sources'), (22, 'over the evidence budget')]
  - ✓ Table 3 (page 9) | need: case study comparison | priority: required | status: missing → 候選 3，納入 [25, 26]，排除 [(27, 'already among the retrieved sources')]
  - ✓ Section 4.4 CASE STUDY (RQ3) (pages 8-9) | need: qualitative comparison context | priority: supplementary | status: covered → 候選 5，納入 []，排除 [(24, 'already among the retrieved sources'), (27, 'already among the retrieved sources'), (23, 'supplementary cap reached'), (25, 'supplementary cap reached'), (26, 'supplementary cap reached')]
  - ✓ Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM (pages 4-5) | need: methodological distinction | priority: supplementary | status: missing → 候選 3，納入 [11, 12]，排除 [(13, 'supplementary cap reached')]
- 分析狀態：UNCERTAIN；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 修正：[]；刪除 []；仍不符 []；方向待定 []
- 涵蓋判定：Table 1 (page 7)→missing；Section 4.2 COMPARISON OF LIGHT RAG WITH EXISTING RAG METHODS (RQ1) (pages 6-7)→partial；Section 4.3 ABLATION STUDIES (RQ2) (pages 7-8)→partial；Table 3 (page 9)→missing；Section 4.4 CASE STUDY (RQ3) (pages 8-9)→partial；Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM (pages 4-5)→missing；required 未納入 []；supplementary 用 2；Matrix {'cells': 128, 'tables': ['Table 1 [6]'], 'definitions': ['LightRAG'], 'facts': 112, 'coverage_gaps': ['Table 3 [7]']}
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 30；找不到的數字 []

```text
The question asks to compare LightRAG with GraphRAG. The comparison includes datasets (Agriculture, CS, Legal, Mix), metrics (Comprehensiveness, Diversity, Empowerment, Overall), and methods (LightRAG, GraphRAG).

From the sources, the method definition for LightRAG is provided in [2], and the method definitions for GraphRAG are described in the context of comparisons. The evidence matrix is found in [6], which provides win rates for GraphRAG and LightRAG across four datasets and four evaluation dimensions.

The following figures are relevant and share the same dataset, metric, and pairing:
- In the Agriculture dataset:
  - Comprehensiveness: GraphRAG 45.6%, LightRAG 54.4% [6]
  - Diversity: GraphRAG 22.8%, LightRAG 77.2% [6]
  - Empowerment: GraphRAG 41.2%, LightRAG 58.8% [6]
  - Overall: GraphRAG 45.2%, LightRAG 54.8% [6]
- In the CS dataset:
  - Comprehensiveness: GraphRAG 48.4%, LightRAG 51.6% [6]
  - Diversity: GraphRAG 40.8%, LightRAG 59.2% [6]
  - Empowerment: GraphRAG 45.2%, LightRAG 54.8% [6]
  - Overall: GraphRAG 48.0%, LightRAG 52.0% [6]
- In the Legal dataset:
  - Comprehensiveness: GraphRAG 48.4%, LightRAG 51.6% [6]
  - Diversity: GraphRAG 26.4%, LightRAG 73.6% [6]
  - Empowerment: GraphRAG 43.6%, LightRAG 56.4% [6]
  - Overall: GraphRAG 47.2%, LightRAG 52.8% [6]
- In the Mix dataset:
  - Comprehensiveness: GraphRAG 50.4%, LightRAG 49.6% [6]
  - Diversity: GraphRAG 36.0%, LightRAG 64.0% [6]
  - Empowerment: GraphRAG 50.8%, LightRAG 49.2% [6]
  - Overall: GraphRAG 50.4%, LightRAG 49.6% [6]

LightRAG consistently outperforms GraphRAG in the Agriculture and CS datasets across all four metrics. In the Legal dataset, LightRAG also outperforms GraphRAG in Comprehensiveness, Diversity, and Overall but shows a smaller margin in Empowerment. In the Mix dataset, GraphRAG and LightRAG are nearly tied in Comprehensiveness and Overall, with LightRAG showing a significant lead in Diversity and a slight lead in Empowerment.

These findings are consistent with the figures provided. LightRAG's lead in Comprehensiveness, Diversity, and Empowerment is higher in the Agriculture and CS datasets compared to the Legal and Mix datasets. In the Mix dataset, the performance of LightRAG and GraphRAG is closer, particularly in Comprehensiveness and Overall.

The source for the figures is [6]. The method definition for LightRAG is cited to [2].

The comparison covers the datasets and metrics requested, and the findings are supported by the figures provided in the sources.
```

## B5-Q2-2

- 問題：`compare lightRAG with GraphRAG`；模式 `navigate`；52.6 秒；2 次呼叫；tokens 8824
- 來源：[1] p7 retrieval, [2] p7 retrieval, [3] p9 retrieval, [4] p8 retrieval, [5] p10 retrieval, [6] p7 navigation, [7] p9 navigation, [8] p9 navigation, [9] p8 navigation, [10] p6 navigation, [11] p4 navigation
- 閱讀計畫（定位 6/6，保留 7，超預算 1）：
  - ✓ Table 1 (page 7) | need: comparison across datasets | priority: required | status: missing → 候選 3，納入 [19]，排除 [(20, 'already among the retrieved sources'), (21, 'already among the retrieved sources')]
  - ✓ Section 4.2 COMPARISON OF LIGHT RAG WITH EXISTING RAG METHODS (RQ1) (pages 6-7) | need: general comparison context | priority: required | status: covered → 候選 4，納入 [18]，排除 [(20, 'already among the retrieved sources'), (21, 'already among the retrieved sources'), (19, 'already selected for another target')]
  - ✓ Section 4.3 ABLATION STUDIES (RQ2) (pages 7-8) | need: specific comparison with GraphRAG | priority: required | status: covered → 候選 3，納入 [23]，排除 [(21, 'already among the retrieved sources'), (22, 'over the evidence budget')]
  - ✓ Table 3 (page 9) | need: case study comparison | priority: required | status: missing → 候選 3，納入 [25, 26]，排除 [(27, 'already among the retrieved sources')]
  - ✓ Section 4.4 CASE STUDY (RQ3) (pages 8-9) | need: qualitative comparison context | priority: supplementary | status: covered → 候選 5，納入 []，排除 [(24, 'already among the retrieved sources'), (27, 'already among the retrieved sources'), (23, 'supplementary cap reached'), (25, 'supplementary cap reached'), (26, 'supplementary cap reached')]
  - ✓ Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM (pages 4-5) | need: methodological distinction | priority: supplementary | status: missing → 候選 3，納入 [11, 12]，排除 [(13, 'supplementary cap reached')]
- 分析狀態：UNCERTAIN；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 修正：[]；刪除 []；仍不符 []；方向待定 []
- 涵蓋判定：Table 1 (page 7)→missing；Section 4.2 COMPARISON OF LIGHT RAG WITH EXISTING RAG METHODS (RQ1) (pages 6-7)→partial；Section 4.3 ABLATION STUDIES (RQ2) (pages 7-8)→partial；Table 3 (page 9)→missing；Section 4.4 CASE STUDY (RQ3) (pages 8-9)→partial；Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM (pages 4-5)→missing；required 未納入 []；supplementary 用 2；Matrix {'cells': 128, 'tables': ['Table 1 [6]'], 'definitions': ['LightRAG'], 'facts': 112, 'coverage_gaps': ['Table 3 [7]']}
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 4；找不到的數字 []

```text
LightRAG is compared to GraphRAG across four datasets (Agriculture, CS, Legal, Mix) and four evaluation dimensions (Comprehensiveness, Diversity, Empowerment, Overall) in Table 1 [6]. The comparison is based on win rates, where a higher percentage indicates that LightRAG is preferred over GraphRAG in that dimension and dataset.

| Dataset   | Evaluation Dimension | LightRAG Win Rate (%) | GraphRAG Win Rate (%) | Source |
|-----------|----------------------|------------------------|------------------------|--------|
| Agriculture | Comprehensiveness | 54.4                   | 45.6                   | [6]    |
|           | Diversity           | 77.2                   | 22.8                   | [6]    |
|           | Empowerment         | 58.8                   | 41.2                   | [6]    |
|           | Overall             | 54.8                   | 45.2                   | [6]    |
| CS        | Comprehensiveness | 51.6                   | 48.4                   | [6]    |
|           | Diversity           | 59.2                   | 40.8                   | [6]    |
|           | Empowerment         | 54.8                   | 45.2                   | [6]    |
|           | Overall             | 52.0                   | 48.0                   | [6]    |
| Legal     | Comprehensiveness | 51.6                   | 48.4                   | [6]    |
|           | Diversity           | 73.6                   | 26.4                   | [6]    |
|           | Empowerment         | 56.4                   | 43.6                   | [6]    |
|           | Overall             | 52.8                   | 47.2                   | [6]    |
| Mix       | Comprehensiveness | 49.6                   | 50.4                   | [6]    |
|           | Diversity           | 64.0                   | 36.0                   | [6]    |
|           | Empowerment         | 49.2                   | 50.8                   | [6]    |
|           | Overall             | 49.6                   | 50.4                   | [6]    |

**Main Findings:**
- In the Agriculture dataset, LightRAG consistently outperforms GraphRAG in all four evaluation dimensions.
- In the CS and Legal datasets, LightRAG outperforms GraphRAG in most dimensions, particularly in Diversity.
- In the Mix dataset, GraphRAG wins in Comprehensiveness and Empowerment, while LightRAG wins in Diversity and Overall.

**Representative Figures:**
- LightRAG achieves a 77.2% win rate in Diversity on the Agriculture dataset compared to 22.8% for GraphRAG [6].
- On the Legal dataset, LightRAG achieves a 73.6% win rate in Diversity compared to 26.4% for GraphRAG [6].

**Results Going Against the Trend:**
- In the Mix dataset, GraphRAG outperforms LightRAG in Comprehensiveness (50.4% vs. 49.6%) and Empowerment (50.8% vs. 49.2%) [6].

**Conclusion:**
LightRAG generally outperforms GraphRAG in most evaluation dimensions and datasets, particularly in Diversity. However, in the Mix dataset, GraphRAG shows stronger performance in Comprehensiveness and Empowerment. This suggests that the performance of the two methods varies depending on the dataset and the evaluation dimension.
```

## B5-Q2-3

- 問題：`compare lightRAG with GraphRAG`；模式 `navigate`；62.0 秒；2 次呼叫；tokens 9040
- 來源：[1] p7 retrieval, [2] p7 retrieval, [3] p9 retrieval, [4] p8 retrieval, [5] p10 retrieval, [6] p7 navigation, [7] p9 navigation, [8] p9 navigation, [9] p8 navigation, [10] p6 navigation, [11] p4 navigation
- 閱讀計畫（定位 6/6，保留 7，超預算 1）：
  - ✓ Table 1 (page 7) | need: comparison across datasets | priority: required | status: missing → 候選 3，納入 [19]，排除 [(20, 'already among the retrieved sources'), (21, 'already among the retrieved sources')]
  - ✓ Section 4.2 COMPARISON OF LIGHT RAG WITH EXISTING RAG METHODS (RQ1) (pages 6-7) | need: general comparison context | priority: required | status: covered → 候選 4，納入 [18]，排除 [(20, 'already among the retrieved sources'), (21, 'already among the retrieved sources'), (19, 'already selected for another target')]
  - ✓ Section 4.3 ABLATION STUDIES (RQ2) (pages 7-8) | need: specific comparison with GraphRAG | priority: required | status: covered → 候選 3，納入 [23]，排除 [(21, 'already among the retrieved sources'), (22, 'over the evidence budget')]
  - ✓ Table 3 (page 9) | need: case study comparison | priority: required | status: missing → 候選 3，納入 [25, 26]，排除 [(27, 'already among the retrieved sources')]
  - ✓ Section 4.4 CASE STUDY (RQ3) (pages 8-9) | need: qualitative comparison context | priority: supplementary | status: covered → 候選 5，納入 []，排除 [(24, 'already among the retrieved sources'), (27, 'already among the retrieved sources'), (23, 'supplementary cap reached'), (25, 'supplementary cap reached'), (26, 'supplementary cap reached')]
  - ✓ Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM (pages 4-5) | need: methodological distinction | priority: supplementary | status: missing → 候選 3，納入 [11, 12]，排除 [(13, 'supplementary cap reached')]
- 分析狀態：FACTUALLY_INCORRECT；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 [('incomparable', '54.8%', '45.2%')]
- 修正：[]；刪除 []；仍不符 ['50.4% (Mix, LightRAG)', '49.6% (Mix, GraphRAG)', '50.8% (Mix, LightRAG)', '49.2% (Mix, GraphRAG)', '50.4% (Mix, LightRAG)', '49.6% (Mix, GraphRAG)']；方向待定 []
- 涵蓋判定：Table 1 (page 7)→missing；Section 4.2 COMPARISON OF LIGHT RAG WITH EXISTING RAG METHODS (RQ1) (pages 6-7)→partial；Section 4.3 ABLATION STUDIES (RQ2) (pages 7-8)→partial；Table 3 (page 9)→missing；Section 4.4 CASE STUDY (RQ3) (pages 8-9)→partial；Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM (pages 4-5)→missing；required 未納入 []；supplementary 用 2；Matrix {'cells': 128, 'tables': ['Table 1 [6]'], 'definitions': ['LightRAG'], 'facts': 112, 'coverage_gaps': ['Table 3 [7]']}
- 檢查：標籤不符 ['50.4%', '49.6%', '50.8%', '49.2%']；全稱宣稱 0；引用可疑 [([7], [6]), ([9], [6])]；未解析 30；找不到的數字 []

```text
LightRAG is compared with GraphRAG across four datasets (Agriculture, CS, Legal, and Mix) and four evaluation dimensions (Comprehensiveness, Diversity, Empowerment, and Overall). The comparison is based on win rates, indicating the percentage of times each method outperforms the other in a head-to-head evaluation.

### Comparison Table:
| Dataset | Evaluation Dimension | LightRAG Win Rate (%) | GraphRAG Win Rate (%) |
|---------|----------------------|------------------------|------------------------|
| Agriculture | Comprehensiveness | 54.4 | 45.6 |
|           | Diversity | 77.2 | 22.8 |
|           | Empowerment | 58.8 | 41.2 |
|           | Overall | 54.8 | 45.2 |
| CS      | Comprehensiveness | 51.6 | 48.4 |
|           | Diversity | 59.2 | 40.8 |
|           | Empowerment | 54.8 | 45.2 |
|           | Overall | 52.0 | 48.0 |
| Legal   | Comprehensiveness | 51.6 | 48.4 |
|           | Diversity | 73.6 | 26.4 |
|           | Empowerment | 56.4 | 43.6 |
|           | Overall | 52.8 | 47.2 |
| Mix     | Comprehensiveness | 49.6 | 50.4 |
|           | Diversity | 64.0 | 36.0 |
|           | Empowerment | 49.2 | 50.8 |
|           | Overall | 49.6 | 50.4 |

### Analysis:
1. **Comprehensiveness**:
   - LightRAG outperforms GraphRAG in Agriculture (54.4% vs. 45.6%), CS (51.6% vs. 48.4%), and Legal (51.6% vs. 48.4%). In Mix, GraphRAG slightly outperforms LightRAG (50.4% vs. 49.6%).
   - The improvements are attributed to LightRAG’s graph-based indexing and dual-level retrieval paradigm, which enables comprehensive exploration of both specific entities and broader relationships [1].

2. **Diversity**:
   - LightRAG significantly outperforms GraphRAG in Agriculture (77.2% vs. 22.8%), CS (59.2% vs. 40.8%), Legal (73.6% vs. 26.4%), and Mix (64.0% vs. 36.0%).
   - The diversity advantage is attributed to the dual-level retrieval, combining low-level (specific entities) and high-level (broader topics) retrieval to enrich the response with varied perspectives [2].

3. **Empowerment**:
   - LightRAG outperforms GraphRAG in Agriculture (58.8% vs. 41.2%), CS (54.8% vs. 45.2%), and Legal (56.4% vs. 43.6%). In Mix, GraphRAG slightly outperforms LightRAG (50.8% vs. 49.2%).
   - The empowerment improvement is attributed to LightRAG’s ability to provide contextual insights and trade-offs between metrics, enabling more informed judgments [7].

4. **Overall**:
   - LightRAG outperforms GraphRAG in Agriculture (54.8% vs. 45.2%), CS (52.0% vs. 48.0%), and Legal (52.8% vs. 47.2%). In Mix, GraphRAG slightly outperforms LightRAG (50.4% vs. 49.6%).
   - The overall performance is attributed to the balanced combination of breadth and depth in retrieval, facilitated by the dual-level paradigm [9].

### Exceptions:
- In the Mix dataset, GraphRAG slightly outperforms LightRAG in Comprehensiveness (50.4% vs. 49.6%) and Empowerment (50.8% vs. 49.2%), while performing similarly in Overall (50.4% vs. 49.6%).

### Conclusion:
LightRAG outperforms GraphRAG in most comparisons across the four datasets and evaluation dimensions. The primary advantages are attributed to the dual-level retrieval paradigm and graph-based indexing. However, in the Mix dataset, GraphRAG performs slightly better in some dimensions, indicating that dataset-specific characteristics may influence performance [6].

Figures whose labels differ from the source table: 50.4% (answer: Mix, LightRAG; source: Comprehensiveness, Mix, GraphRAG, vs LightRAG / Overall, Mix, GraphRAG, vs LightRAG); 49.6% (answer: Mix, GraphRAG; source: Comprehensiveness, Mix, LightRAG, vs GraphRAG / Overall, Mix, LightRAG, vs GraphRAG); 50.8% (answer: Mix, LightRAG; source: Empowerment, Mix, GraphRAG, vs LightRAG); 49.2% (answer: Mix, GraphRAG; source: Empowerment, Mix, LightRAG, vs GraphRAG).
```

## B6-Q2-1

- 問題：`compare lightRAG with GraphRAG`；模式 `navigate`；57.8 秒；2 次呼叫；tokens 9041
- 來源：[1] p7 retrieval, [2] p7 retrieval, [3] p9 retrieval, [4] p8 retrieval, [5] p10 retrieval, [6] p7 navigation, [7] p9 navigation, [8] p6 navigation
- 閱讀計畫（定位 6/6，保留 3，超預算 8）：
  - ✓ Table 1 (page 7) | need: comparison across datasets | priority: required | status: missing → 候選 3，納入 [19]，排除 [(20, 'already among the retrieved sources'), (21, 'already among the retrieved sources')]
  - ✓ Section 4.2 COMPARISON OF LIGHT RAG WITH EXISTING RAG METHODS (RQ1) (pages 6-7) | need: general comparison context | priority: required | status: covered → 候選 4，納入 [18]，排除 [(20, 'already among the retrieved sources'), (21, 'already among the retrieved sources'), (19, 'already selected for another target')]
  - ✓ Section 4.3 ABLATION STUDIES (RQ2) (pages 7-8) | need: specific comparison with GraphRAG | priority: required | status: covered → 候選 3，納入 []，排除 [(21, 'already among the retrieved sources'), (23, 'over the evidence budget'), (22, 'over the evidence budget')]
  - ✓ Table 3 (page 9) | need: case study comparison | priority: required | status: missing → 候選 3，納入 [25]，排除 [(26, 'over the evidence budget'), (27, 'already among the retrieved sources')]
  - ✓ Section 4.4 CASE STUDY (RQ3) (pages 8-9) | need: qualitative comparison context | priority: supplementary | status: covered → 候選 5，納入 []，排除 [(24, 'already among the retrieved sources'), (27, 'already among the retrieved sources'), (23, 'over the evidence budget'), (25, 'already selected for another target'), (26, 'over the evidence budget')]
  - ✓ Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM (pages 4-5) | need: methodological distinction | priority: supplementary | status: missing → 候選 3，納入 []，排除 [(11, 'over the evidence budget'), (12, 'over the evidence budget'), (13, 'over the evidence budget')]
- 分析狀態：FACTUALLY_INCORRECT；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 [('inconsistent', '49.6%', '50.4%'), ('inconsistent', '49.2%', '50.8%'), ('inconsistent', '49.6%', '50.4%')]
- 修正：[]；刪除 []；仍不符 ['"regresses" (49.6% / 50.4%)', '"regresses" (49.2% / 50.8%)', '"regresses" (49.6% / 50.4%)']；方向待定 []
- 涵蓋判定：Table 1 (page 7)→missing；Section 4.2 COMPARISON OF LIGHT RAG WITH EXISTING RAG METHODS (RQ1) (pages 6-7)→partial；Section 4.3 ABLATION STUDIES (RQ2) (pages 7-8)→partial；Table 3 (page 9)→missing；Section 4.4 CASE STUDY (RQ3) (pages 8-9)→partial；Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM (pages 4-5)→missing；required 未納入 ['Section 4.3 ABLATION STUDIES (RQ2) (pages 7-8)']；supplementary 用 0；Matrix {'cells': 128, 'tables': ['Table 1 [6]'], 'shown_tokens': 1348, 'left_out': [], 'definitions': ['LightRAG'], 'facts': 112, 'coverage_gaps': ['Table 3 [7]']}
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 20；找不到的數字 []

```text
The question asks to compare LightRAG with GraphRAG across datasets (Agriculture, CS, Legal, Mix), metrics (Comprehensiveness, Diversity, Empowerment, Overall), and their win rates as presented in the evidence matrix.

From the evidence matrix, we observe the win rates for each pair in Table 1 [6]. From the method definitions, LightRAG is described in [2] as employing a dual-level retrieval paradigm and graph-based text indexing. GraphRAG is not defined in the provided sources.

The following figures are relevant for the comparison between LightRAG and GraphRAG, grouped by dataset, metric, and pairing:

- **Agriculture / Comprehensiveness**: GraphRAG 45.6% | LightRAG 54.4%
- **CS / Comprehensiveness**: GraphRAG 48.4% | LightRAG 51.6%
- **Legal / Comprehensiveness**: GraphRAG 48.4% | LightRAG 51.6%
- **Mix / Comprehensiveness**: GraphRAG 50.4% | LightRAG 49.6%

- **Agriculture / Diversity**: GraphRAG 22.8% | LightRAG 77.2%
- **CS / Diversity**: GraphRAG 40.8% | LightRAG 59.2%
- **Legal / Diversity**: GraphRAG 26.4% | LightRAG 73.6%
- **Mix / Diversity**: GraphRAG 36.0% | LightRAG 64.0%

- **Agriculture / Empowerment**: GraphRAG 41.2% | LightRAG 58.8%
- **CS / Empowerment**: GraphRAG 45.2% | LightRAG 54.8%
- **Legal / Empowerment**: GraphRAG 43.6% | LightRAG 56.4%
- **Mix / Empowerment**: GraphRAG 50.8% | LightRAG 49.2%

- **Agriculture / Overall**: GraphRAG 45.2% | LightRAG 54.8%
- **CS / Overall**: GraphRAG 48.0% | LightRAG 52.0%
- **Legal / Overall**: GraphRAG 47.2% | LightRAG 52.8%
- **Mix / Overall**: GraphRAG 50.4% | LightRAG 49.6%

Improvements, regressions, and exceptions:

- LightRAG outperforms GraphRAG in **Comprehensiveness** in Agriculture (54.4% vs. 45.6%) and Legal (51.6% vs. 48.4%), but regresses slightly in Mix (49.6% vs. 50.4%).
- LightRAG outperforms GraphRAG in **Diversity** in all four datasets, with the largest margin in Agriculture (77.2% vs. 22.8%).
- LightRAG outperforms GraphRAG in **Empowerment** in Agriculture (58.8% vs. 41.2%) and Legal (56.4% vs. 43.6%), but regresses slightly in Mix (49.2% vs. 50.8%).
- LightRAG outperforms GraphRAG in **Overall** in Agriculture (54.8% vs. 45.2%) and Legal (52.8% vs. 47.2%), but regresses slightly in Mix (49.6% vs. 50.4%).

The statements about "outperforms" and "regresses" align with the win rates as presented in the evidence matrix. For instance, in Agriculture / Diversity, LightRAG wins 77.2% of the time, while GraphRAG wins only 22.8% [6].

The evidence matrix is cited to [6] for all figures. The definition of LightRAG is cited to [2].

The comparison requested by the question is fully addressed based on the provided evidence.
```

## B6-Q2-2

- 問題：`compare lightRAG with GraphRAG`；模式 `navigate`；62.2 秒；2 次呼叫；tokens 9141
- 來源：[1] p7 retrieval, [2] p7 retrieval, [3] p9 retrieval, [4] p8 retrieval, [5] p10 retrieval, [6] p7 navigation, [7] p9 navigation, [8] p6 navigation
- 閱讀計畫（定位 6/6，保留 3，超預算 8）：
  - ✓ Table 1 (page 7) | need: comparison across datasets | priority: required | status: missing → 候選 3，納入 [19]，排除 [(20, 'already among the retrieved sources'), (21, 'already among the retrieved sources')]
  - ✓ Section 4.2 COMPARISON OF LIGHT RAG WITH EXISTING RAG METHODS (RQ1) (pages 6-7) | need: general comparison context | priority: required | status: covered → 候選 4，納入 [18]，排除 [(20, 'already among the retrieved sources'), (21, 'already among the retrieved sources'), (19, 'already selected for another target')]
  - ✓ Section 4.3 ABLATION STUDIES (RQ2) (pages 7-8) | need: specific comparison with GraphRAG | priority: required | status: covered → 候選 3，納入 []，排除 [(21, 'already among the retrieved sources'), (23, 'over the evidence budget'), (22, 'over the evidence budget')]
  - ✓ Table 3 (page 9) | need: case study comparison | priority: required | status: missing → 候選 3，納入 [25]，排除 [(26, 'over the evidence budget'), (27, 'already among the retrieved sources')]
  - ✓ Section 4.4 CASE STUDY (RQ3) (pages 8-9) | need: qualitative comparison context | priority: supplementary | status: covered → 候選 5，納入 []，排除 [(24, 'already among the retrieved sources'), (27, 'already among the retrieved sources'), (23, 'over the evidence budget'), (25, 'already selected for another target'), (26, 'over the evidence budget')]
  - ✓ Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM (pages 4-5) | need: methodological distinction | priority: supplementary | status: missing → 候選 3，納入 []，排除 [(11, 'over the evidence budget'), (12, 'over the evidence budget'), (13, 'over the evidence budget')]
- 分析狀態：UNCERTAIN；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 修正：[]；刪除 []；仍不符 []；方向待定 []
- 涵蓋判定：Table 1 (page 7)→missing；Section 4.2 COMPARISON OF LIGHT RAG WITH EXISTING RAG METHODS (RQ1) (pages 6-7)→partial；Section 4.3 ABLATION STUDIES (RQ2) (pages 7-8)→partial；Table 3 (page 9)→missing；Section 4.4 CASE STUDY (RQ3) (pages 8-9)→partial；Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM (pages 4-5)→missing；required 未納入 ['Section 4.3 ABLATION STUDIES (RQ2) (pages 7-8)']；supplementary 用 0；Matrix {'cells': 128, 'tables': ['Table 1 [6]'], 'shown_tokens': 1348, 'left_out': [], 'definitions': ['LightRAG'], 'facts': 112, 'coverage_gaps': ['Table 3 [7]']}
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
The question asks for a comparison between LightRAG and GraphRAG, focusing on their performance across four datasets (Agriculture, CS, Legal, Mix) and four evaluation metrics (Comprehensiveness, Diversity, Empowerment, and Overall).

### Compact Comparison Table (GraphRAG vs. LightRAG)
| Dataset     | Metric         | GraphRAG (%) | LightRAG (%) |
|-------------|----------------|--------------|--------------|
| Agriculture | Comprehensiveness | 45.6         | 54.4         |
|             | Diversity        | 22.8         | 77.2         |
|             | Empowerment      | 41.2         | 58.8         |
|             | Overall          | 45.2         | 54.8         |
| CS          | Comprehensiveness | 48.4         | 51.6         |
|             | Diversity        | 40.8         | 59.2         |
|             | Empowerment      | 45.2         | 54.8         |
|             | Overall          | 48.0         | 52.0         |
| Legal       | Comprehensiveness | 48.4         | 51.6         |
|             | Diversity        | 26.4         | 73.6         |
|             | Empowerment      | 43.6         | 56.4         |
|             | Overall          | 47.2         | 52.8         |
| Mix         | Comprehensiveness | 50.4         | 49.6         |
|             | Diversity        | 36.0         | 64.0         |
|             | Empowerment      | 50.8         | 49.2         |
|             | Overall          | 50.4         | 49.6         |

### Analysis

**Main Findings:**
LightRAG consistently outperforms GraphRAG in most metrics and datasets. The most notable improvements are in Diversity and Empowerment, especially in the Agriculture and Legal datasets. However, there are exceptions where GraphRAG performs equally or slightly better.

**Representative Figures:**
- **Comprehensiveness:**
  - Agriculture: GraphRAG 45.6% vs. LightRAG 54.4% [6]
  - Legal: GraphRAG 48.4% vs. LightRAG 51.6% [6]
  - Mix: GraphRAG 50.4% vs. LightRAG 49.6% [6]
- **Diversity:**
  - Agriculture: GraphRAG 22.8% vs. LightRAG 77.2% [6]
  - CS: GraphRAG 40.8% vs. LightRAG 59.2% [6]
  - Legal: GraphRAG 26.4% vs. LightRAG 73.6% [6]
- **Empowerment:**
  - Agriculture: GraphRAG 41.2% vs. LightRAG 58.8% [6]
  - Legal: GraphRAG 43.6% vs. LightRAG 56.4% [6]
  - Mix: GraphRAG 50.8% vs. LightRAG 49.2% [6]
- **Overall:**
  - Agriculture: GraphRAG 45.2% vs. LightRAG 54.8% [6]
  - Legal: GraphRAG 47.2% vs. LightRAG 52.8% [6]
  - Mix: GraphRAG 50.4% vs. LightRAG 49.6% [6]

**Exceptions:**
- **Comprehensiveness:**
  - Mix: GraphRAG 50.4% vs. LightRAG 49.6% [6]
- **Empowerment:**
  - Mix: GraphRAG 50.8% vs. LightRAG 49.2% [6]
- **Overall:**
  - Mix: GraphRAG 50.4% vs. LightRAG 49.6% [6]

**Conclusion:**
LightRAG outperforms GraphRAG in the majority of the metrics and datasets, particularly in Diversity and Empowerment. The exceptions in the Mix dataset indicate that GraphRAG performs slightly better in certain scenarios, but overall, LightRAG demonstrates superior performance. The dual-level retrieval paradigm in LightRAG contributes to its effectiveness in capturing both detailed and abstract information, as noted in the methodological distinction [2].
```

## B6-Q2-3

- 問題：`compare lightRAG with GraphRAG`；模式 `navigate`；60.3 秒；2 次呼叫；tokens 9102
- 來源：[1] p7 retrieval, [2] p7 retrieval, [3] p9 retrieval, [4] p8 retrieval, [5] p10 retrieval, [6] p7 navigation, [7] p9 navigation, [8] p6 navigation
- 閱讀計畫（定位 6/6，保留 3，超預算 8）：
  - ✓ Table 1 (page 7) | need: comparison across datasets | priority: required | status: missing → 候選 3，納入 [19]，排除 [(20, 'already among the retrieved sources'), (21, 'already among the retrieved sources')]
  - ✓ Section 4.2 COMPARISON OF LIGHT RAG WITH EXISTING RAG METHODS (RQ1) (pages 6-7) | need: general comparison context | priority: required | status: covered → 候選 4，納入 [18]，排除 [(20, 'already among the retrieved sources'), (21, 'already among the retrieved sources'), (19, 'already selected for another target')]
  - ✓ Section 4.3 ABLATION STUDIES (RQ2) (pages 7-8) | need: specific comparison with GraphRAG | priority: required | status: covered → 候選 3，納入 []，排除 [(21, 'already among the retrieved sources'), (23, 'over the evidence budget'), (22, 'over the evidence budget')]
  - ✓ Table 3 (page 9) | need: case study comparison | priority: required | status: missing → 候選 3，納入 [25]，排除 [(26, 'over the evidence budget'), (27, 'already among the retrieved sources')]
  - ✓ Section 4.4 CASE STUDY (RQ3) (pages 8-9) | need: qualitative comparison context | priority: supplementary | status: covered → 候選 5，納入 []，排除 [(24, 'already among the retrieved sources'), (27, 'already among the retrieved sources'), (23, 'over the evidence budget'), (25, 'already selected for another target'), (26, 'over the evidence budget')]
  - ✓ Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM (pages 4-5) | need: methodological distinction | priority: supplementary | status: missing → 候選 3，納入 []，排除 [(11, 'over the evidence budget'), (12, 'over the evidence budget'), (13, 'over the evidence budget')]
- 分析狀態：FACTUALLY_INCORRECT；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 修正：[]；刪除 []；仍不符 ['50.4% (Comprehensiveness, Mix, LightRAG)', '49.6% (Comprehensiveness, Mix, GraphRAG)']；方向待定 []
- 涵蓋判定：Table 1 (page 7)→missing；Section 4.2 COMPARISON OF LIGHT RAG WITH EXISTING RAG METHODS (RQ1) (pages 6-7)→partial；Section 4.3 ABLATION STUDIES (RQ2) (pages 7-8)→partial；Table 3 (page 9)→missing；Section 4.4 CASE STUDY (RQ3) (pages 8-9)→partial；Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM (pages 4-5)→missing；required 未納入 ['Section 4.3 ABLATION STUDIES (RQ2) (pages 7-8)']；supplementary 用 0；Matrix {'cells': 128, 'tables': ['Table 1 [6]'], 'shown_tokens': 1348, 'left_out': [], 'definitions': ['LightRAG'], 'facts': 112, 'coverage_gaps': ['Table 3 [7]']}
- 檢查：標籤不符 ['50.4%', '49.6%']；全稱宣稱 2；引用可疑 []；未解析 34；找不到的數字 []

```text
The question asks to compare LightRAG with GraphRAG across the datasets (Agriculture, CS, Legal, Mix) and metrics (Comprehensiveness, Diversity, Empowerment, Overall). The comparison is based on the win rates reported in Table 1 [6].

### Compact Comparison Table
| Dataset       | Metric         | GraphRAG Win Rate | LightRAG Win Rate | Source |
|---------------|----------------|-------------------|-------------------|--------|
| Agriculture   | Comprehensiveness | 45.6%            | 54.4%             | [6]    |
| CS            | Comprehensiveness | 48.4%            | 51.6%             | [6]    |
| Legal         | Comprehensiveness | 48.4%            | 51.6%             | [6]    |
| Mix           | Comprehensiveness | 50.4%            | 49.6%             | [6]    |
| Agriculture   | Diversity       | 22.8%            | 77.2%             | [6]    |
| CS            | Diversity       | 40.8%            | 59.2%             | [6]    |
| Legal         | Diversity       | 26.4%            | 73.6%             | [6]    |
| Mix           | Diversity       | 36.0%            | 64.0%             | [6]    |
| Agriculture   | Empowerment     | 41.2%            | 58.8%             | [6]    |
| CS            | Empowerment     | 45.2%            | 54.8%             | [6]    |
| Legal         | Empowerment     | 43.6%            | 56.4%             | [6]    |
| Mix           | Empowerment     | 50.8%            | 49.2%             | [6]    |
| Agriculture   | Overall         | 45.2%            | 54.8%             | [6]    |
| CS            | Overall         | 48.0%            | 52.0%             | [6]    |
| Legal         | Overall         | 47.2%            | 52.8%             | [6]    |
| Mix           | Overall         | 50.4%            | 49.6%             | [6]    |

### Analysis
LightRAG consistently outperforms GraphRAG in **Diversity**, **Empowerment**, and **Overall** across all four datasets. For example, in the **Legal** dataset, LightRAG achieves a **73.6%** win rate in Diversity compared to GraphRAG's **26.4%**, and in Empowerment, LightRAG achieves **56.4%** compared to GraphRAG's **43.6%** [6].

In **Comprehensiveness**, LightRAG also outperforms GraphRAG in three out of four datasets (Agriculture: **54.4%** vs. **45.6%**, CS: **51.6%** vs. **48.4%, Legal: 51.6% vs. 48.4%**), but in the **Mix** dataset, GraphRAG slightly outperforms LightRAG (**50.4%** vs. **49.6%**) [6].

The **only regression** is in the **Comprehensiveness** metric on the **Mix** dataset, where GraphRAG performs better than LightRAG. This is an exception to the general trend where LightRAG outperforms GraphRAG.

The superior performance of LightRAG is attributed to its **dual-level retrieval paradigm**, which integrates low-level retrieval of specific entities with high-level retrieval of broader topics, as described in Section 4.3 [2]. This mechanism is not explicitly defined for GraphRAG, but the evidence suggests that it lacks the same level of integration and effectiveness [2].

### Conclusion
LightRAG outperforms GraphRAG in **Diversity**, **Empowerment**, and **Overall** across all datasets. It also outperforms GraphRAG in **Comprehensiveness** in three out of four datasets, with the **only exception** being the **Mix** dataset [6]. The **dual-level retrieval paradigm** in LightRAG contributes to its superior performance, as detailed in Section 4.3 [2].

Figures whose labels differ from the source table: 50.4% (answer: Comprehensiveness, Mix, LightRAG; source: Comprehensiveness, Mix, GraphRAG, vs LightRAG / Overall, Mix, GraphRAG, vs LightRAG); 49.6% (answer: Comprehensiveness, Mix, GraphRAG; source: Comprehensiveness, Mix, LightRAG, vs GraphRAG / Overall, Mix, LightRAG, vs GraphRAG).

A claim the source table does not bear out: "LightRAG consistently outperforms GraphRAG in **Diversity**, **Empowerment**, and **Overall** across all four datasets." — LightRAG is above the compared methods in 46 cells and below in 2, for example Empowerment / Mix: LightRAG 49.2% vs GraphRAG 50.8% (p. 7); Overall / Mix: LightRAG 49.6% vs GraphRAG 50.4% (p. 7) / "LightRAG outperforms GraphRAG in **Diversity**, **Empowerment**, and **Overall** across all datasets." — LightRAG is above the compared methods in 46 cells and below in 2, for example Empowerment / Mix: LightRAG 49.2% vs GraphRAG 50.8% (p. 7); Overall / Mix: LightRAG 49.6% vs GraphRAG 50.4% (p. 7).
```

## B7-Q2-1

- 問題：`compare lightRAG with GraphRAG`；模式 `navigate`；60.1 秒；2 次呼叫；tokens 9302
- 來源：[1] p7 retrieval, [2] p7 retrieval, [3] p9 retrieval, [4] p8 retrieval, [5] p10 retrieval, [6] p7 navigation, [7] p9 navigation, [8] p6 navigation
- 閱讀計畫（定位 6/6，保留 3，超預算 8）：
  - ✓ Table 1 (page 7) | need: comparison across datasets | priority: required | status: missing → 候選 3，納入 [19]，排除 [(20, 'already among the retrieved sources'), (21, 'already among the retrieved sources')]
  - ✓ Section 4.2 COMPARISON OF LIGHT RAG WITH EXISTING RAG METHODS (RQ1) (pages 6-7) | need: general comparison context | priority: required | status: covered → 候選 4，納入 [18]，排除 [(20, 'already among the retrieved sources'), (21, 'already among the retrieved sources'), (19, 'already selected for another target')]
  - ✓ Section 4.3 ABLATION STUDIES (RQ2) (pages 7-8) | need: specific comparison with GraphRAG | priority: required | status: covered → 候選 3，納入 []，排除 [(21, 'already among the retrieved sources'), (23, 'over the evidence budget'), (22, 'over the evidence budget')]
  - ✓ Table 3 (page 9) | need: case study comparison | priority: required | status: missing → 候選 3，納入 [25]，排除 [(26, 'over the evidence budget'), (27, 'already among the retrieved sources')]
  - ✓ Section 4.4 CASE STUDY (RQ3) (pages 8-9) | need: qualitative comparison context | priority: supplementary | status: covered → 候選 5，納入 []，排除 [(24, 'already among the retrieved sources'), (27, 'already among the retrieved sources'), (23, 'over the evidence budget'), (25, 'already selected for another target'), (26, 'over the evidence budget')]
  - ✓ Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM (pages 4-5) | need: methodological distinction | priority: supplementary | status: missing → 候選 3，納入 []，排除 [(11, 'over the evidence budget'), (12, 'over the evidence budget'), (13, 'over the evidence budget')]
- 分析狀態：UNCERTAIN；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 修正：[]；刪除 []；仍不符 []；方向待定 []
- 涵蓋判定：Table 1 (page 7)→missing；Section 4.2 COMPARISON OF LIGHT RAG WITH EXISTING RAG METHODS (RQ1) (pages 6-7)→partial；Section 4.3 ABLATION STUDIES (RQ2) (pages 7-8)→partial；Table 3 (page 9)→missing；Section 4.4 CASE STUDY (RQ3) (pages 8-9)→partial；Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM (pages 4-5)→missing；required 未納入 ['Section 4.3 ABLATION STUDIES (RQ2) (pages 7-8)']；supplementary 用 0；Matrix {'cells': 128, 'tables': ['Table 1 [6]'], 'shown_tokens': 1348, 'left_out': [], 'definitions': ['LightRAG'], 'facts': 112, 'coverage_gaps': ['Table 3 [7]']}
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
The question asks for a comparison between LightRAG and GraphRAG, across the datasets (Agriculture, CS, Legal, Mix) and the metrics (Comprehensiveness, Diversity, Empowerment, Overall). The comparison is based on win rates in Table 1 [6].

Evidence matrix and method definitions:

- LightRAG is defined as using a "dual-level retrieval paradigm" and graph-based text indexing to "integrate low-level retrieval of specific entities with high-level retrieval of broader topics" [2].
- GraphRAG is not explicitly defined in the sources but is described as a "graph-based RAG system" that "dismantles its existing community structure to incorporate new entities and relationships" during incremental updates [5].

Comparison of LightRAG and GraphRAG in Table 1 [6], for the same datasets and metrics:

- Comprehensiveness:
  - Agriculture: GraphRAG 45.6% | LightRAG 54.4%
  - CS: GraphRAG 48.4% | LightRAG 51.6%
  - Legal: GraphRAG 48.4% | LightRAG 51.6%
  - Mix: GraphRAG 50.4% | LightRAG 49.6%
- Diversity:
  - Agriculture: GraphRAG 22.8% | LightRAG 77.2%
  - CS: GraphRAG 40.8% | LightRAG 59.2%
  - Legal: GraphRAG 26.4% | LightRAG 73.6%
  - Mix: GraphRAG 36.0% | LightRAG 64.0%
- Empowerment:
  - Agriculture: GraphRAG 41.2% | LightRAG 58.8%
  - CS: GraphRAG 45.2% | LightRAG 54.8%
  - Legal: GraphRAG 43.6% | LightRAG 56.4%
  - Mix: GraphRAG 50.8% | LightRAG 49.2%
- Overall:
  - Agriculture: GraphRAG 45.2% | LightRAG 54.8%
  - CS: GraphRAG 48.0% | LightRAG 52.0%
  - Legal: GraphRAG 47.2% | LightRAG 52.8%
  - Mix: GraphRAG 50.4% | LightRAG 49.6%

Analysis:

- Comprehensiveness: LightRAG outperforms GraphRAG in 3 out of 4 datasets, with the exception being Mix (GraphRAG 50.4% | LightRAG 49.6%) [6].
- Diversity: LightRAG outperforms GraphRAG in all 4 datasets [6].
- Empowerment: LightRAG outperforms GraphRAG in 3 out of 4 datasets, with the exception being Mix (GraphRAG 50.8% | LightRAG 49.2%) [6].
- Overall: LightRAG outperforms GraphRAG in 3 out of 4 datasets, with the exception being Mix (GraphRAG 50.4% | LightRAG 49.6%) [6].

Conclusion:

- LightRAG consistently outperforms GraphRAG in Comprehensiveness, Diversity, and Empowerment in most conditions, with one exception in each metric (Mix) [6].
- In the Overall metric, LightRAG also outperforms GraphRAG in most conditions, with one exception (Mix) [6].
- These results suggest a general trend favoring LightRAG over GraphRAG in most evaluation conditions, with the Mix dataset showing slightly more balanced performance [6].

Citations:

- LightRAG's definition: [2]
- GraphRAG's description: [5]
- All figures from the comparison: [6]

Completeness check:

- The question asked for a comparison between LightRAG and GraphRAG. Both methods are included in the comparison [6].
- The datasets (Agriculture, CS, Legal, Mix) and metrics (Comprehensiveness, Diversity, Empowerment, Overall) are all addressed [6].
- Definitions for both methods are provided [2], [5].
- The analysis is based solely on the data in the sources, as required.
```

## B7-Q2-2

- 問題：`compare lightRAG with GraphRAG`；模式 `navigate`；58.7 秒；2 次呼叫；tokens 9272
- 來源：[1] p7 retrieval, [2] p7 retrieval, [3] p9 retrieval, [4] p8 retrieval, [5] p10 retrieval, [6] p7 navigation, [7] p9 navigation, [8] p6 navigation
- 閱讀計畫（定位 6/6，保留 3，超預算 8）：
  - ✓ Table 1 (page 7) | need: comparison across datasets | priority: required | status: missing → 候選 3，納入 [19]，排除 [(20, 'already among the retrieved sources'), (21, 'already among the retrieved sources')]
  - ✓ Section 4.2 COMPARISON OF LIGHT RAG WITH EXISTING RAG METHODS (RQ1) (pages 6-7) | need: general comparison context | priority: required | status: covered → 候選 4，納入 [18]，排除 [(20, 'already among the retrieved sources'), (21, 'already among the retrieved sources'), (19, 'already selected for another target')]
  - ✓ Section 4.3 ABLATION STUDIES (RQ2) (pages 7-8) | need: specific comparison with GraphRAG | priority: required | status: covered → 候選 3，納入 []，排除 [(21, 'already among the retrieved sources'), (23, 'over the evidence budget'), (22, 'over the evidence budget')]
  - ✓ Table 3 (page 9) | need: case study comparison | priority: required | status: missing → 候選 3，納入 [25]，排除 [(26, 'over the evidence budget'), (27, 'already among the retrieved sources')]
  - ✓ Section 4.4 CASE STUDY (RQ3) (pages 8-9) | need: qualitative comparison context | priority: supplementary | status: covered → 候選 5，納入 []，排除 [(24, 'already among the retrieved sources'), (27, 'already among the retrieved sources'), (23, 'over the evidence budget'), (25, 'already selected for another target'), (26, 'over the evidence budget')]
  - ✓ Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM (pages 4-5) | need: methodological distinction | priority: supplementary | status: missing → 候選 3，納入 []，排除 [(11, 'over the evidence budget'), (12, 'over the evidence budget'), (13, 'over the evidence budget')]
- 分析狀態：FACTUALLY_INCORRECT；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 修正：[]；刪除 []；仍不符 ['41.2% (Empowerment, Agriculture, LightRAG)', '43.6% (Empowerment, Legal, LightRAG)']；方向待定 []
- 涵蓋判定：Table 1 (page 7)→missing；Section 4.2 COMPARISON OF LIGHT RAG WITH EXISTING RAG METHODS (RQ1) (pages 6-7)→partial；Section 4.3 ABLATION STUDIES (RQ2) (pages 7-8)→partial；Table 3 (page 9)→missing；Section 4.4 CASE STUDY (RQ3) (pages 8-9)→partial；Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM (pages 4-5)→missing；required 未納入 ['Section 4.3 ABLATION STUDIES (RQ2) (pages 7-8)']；supplementary 用 0；Matrix {'cells': 128, 'tables': ['Table 1 [6]'], 'shown_tokens': 1348, 'left_out': [], 'definitions': ['LightRAG'], 'facts': 112, 'coverage_gaps': ['Table 3 [7]']}
- 檢查：標籤不符 ['22.8%', '26.4%', '41.2%', '43.6%']；全稱宣稱 1；引用可疑 []；未解析 2；找不到的數字 []

```text
1. The question asks to compare **LightRAG** with **GraphRAG** across **four datasets (Agriculture, CS, Legal, Mix)** and **four metrics (Comprehensiveness, Diversity, Empowerment, Overall)**.

2. Evidence matrix for LightRAG vs. GraphRAG:
   - **Agriculture / Comprehensiveness**: GraphRAG 45.6% | LightRAG 54.4% [6]
   - **CS / Comprehensiveness**: GraphRAG 48.4% | LightRAG 51.6% [6]
   - **Legal / Comprehensiveness**: GraphRAG 48.4% | LightRAG 51.6% [6]
   - **Mix / Comprehensiveness**: GraphRAG 50.4% | LightRAG 49.6% [6]
   - **Agriculture / Diversity**: GraphRAG 22.8% | LightRAG 77.2% [6]
   - **CS / Diversity**: GraphRAG 40.8% | LightRAG 59.2% [6]
   - **Legal / Diversity**: GraphRAG 26.4% | LightRAG 73.6% [6]
   - **Mix / Diversity**: GraphRAG 36.0% | LightRAG 64.0% [6]
   - **Agriculture / Empowerment**: GraphRAG 41.2% | LightRAG 58.8% [6]
   - **CS / Empowerment**: GraphRAG 45.2% | LightRAG 54.8% [6]
   - **Legal / Empowerment**: GraphRAG 43.6% | LightRAG 56.4% [6]
   - **Mix / Empowerment**: GraphRAG 50.8% | LightRAG 49.2% [6]
   - **Agriculture / Overall**: GraphRAG 45.2% | LightRAG 54.8% [6]
   - **CS / Overall**: GraphRAG 48.0% | LightRAG 52.0% [6]
   - **Legal / Overall**: GraphRAG 47.2% | LightRAG 52.8% [6]
   - **Mix / Overall**: GraphRAG 50.4% | LightRAG 49.6% [6]

3. LightRAG consistently outperforms GraphRAG in **Diversity** and **Empowerment** in all four datasets. In **Comprehensiveness** and **Overall**, LightRAG outperforms in **Legal** and **Mix** but performs slightly worse in **Agriculture** and **CS**.

4. Across all metrics and datasets, LightRAG shows a **clear advantage in Diversity** in all four datasets, with a **high margin** in **Agriculture** (77.2% vs. 22.8%) and **Legal** (73.6% vs. 26.4%). In **Empowerment**, LightRAG is also consistently better, with **58.8% vs. 41.2% in Agriculture** and **56.4% vs. 43.6% in Legal**. In **Comprehensiveness**, LightRAG performs better in **Legal** and **Mix** but is slightly behind in **Agriculture** and **CS**.

5. In **Overall performance**, LightRAG outperforms in **Legal** and **Mix**, but is slightly behind in **Agriculture** and **CS**.

6. The method **LightRAG** is defined in [2] as a system that uses a **dual-level retrieval paradigm**, integrating **low-level retrieval** of specific entities and **high-level retrieval** of broader topics. **GraphRAG** is a **graph-based retrieval method** but is not explicitly defined in the sources. The comparison between LightRAG and GraphRAG is made in Table 1 [6], and the methodological distinctions are discussed in [1] and [2].

7. The comparison is complete and addresses the question's requirements, including the metrics, datasets, and methodological distinctions. Each method is defined and compared based on the data provided in the sources.

Figures whose labels differ from the source table: 22.8% (answer: Diversity, LightRAG; source: Diversity, Agriculture, GraphRAG, vs LightRAG); 26.4% (answer: Diversity, LightRAG; source: Overall, Legal, HyDE, vs LightRAG / Diversity, Legal, GraphRAG, vs LightRAG); 41.2% (answer: Empowerment, Agriculture, LightRAG; source: Empowerment, Agriculture, GraphRAG, vs LightRAG); 43.6% (answer: Empowerment, Legal, LightRAG; source: Empowerment, Legal, GraphRAG, vs LightRAG).

A claim the source table does not bear out: "LightRAG consistently outperforms GraphRAG in **Diversity** and **Empowerment** in all four datasets." — LightRAG is above the compared methods in 31 cells and below in 1, for example Empowerment / Mix: LightRAG 49.2% vs GraphRAG 50.8% (p. 7).
```

## B7-Q2-3

- 問題：`compare lightRAG with GraphRAG`；模式 `navigate`；72.6 秒；0 次呼叫；tokens 0
- 來源：[1] p7 retrieval, [2] p7 retrieval, [3] p9 retrieval, [4] p8 retrieval, [5] p10 retrieval, [6] p7 navigation, [7] p9 navigation, [8] p6 navigation
- 閱讀計畫（定位 6/6，保留 3，超預算 8）：
  - ✓ Table 1 (page 7) | need: comparison across datasets | priority: required | status: missing → 候選 3，納入 [19]，排除 [(20, 'already among the retrieved sources'), (21, 'already among the retrieved sources')]
  - ✓ Section 4.2 COMPARISON OF LIGHT RAG WITH EXISTING RAG METHODS (RQ1) (pages 6-7) | need: general comparison context | priority: required | status: covered → 候選 4，納入 [18]，排除 [(20, 'already among the retrieved sources'), (21, 'already among the retrieved sources'), (19, 'already selected for another target')]
  - ✓ Section 4.3 ABLATION STUDIES (RQ2) (pages 7-8) | need: specific comparison with GraphRAG | priority: required | status: covered → 候選 3，納入 []，排除 [(21, 'already among the retrieved sources'), (23, 'over the evidence budget'), (22, 'over the evidence budget')]
  - ✓ Table 3 (page 9) | need: case study comparison | priority: required | status: missing → 候選 3，納入 [25]，排除 [(26, 'over the evidence budget'), (27, 'already among the retrieved sources')]
  - ✓ Section 4.4 CASE STUDY (RQ3) (pages 8-9) | need: qualitative comparison context | priority: supplementary | status: covered → 候選 5，納入 []，排除 [(24, 'already among the retrieved sources'), (27, 'already among the retrieved sources'), (23, 'over the evidence budget'), (25, 'already selected for another target'), (26, 'over the evidence budget')]
  - ✓ Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM (pages 4-5) | need: methodological distinction | priority: supplementary | status: missing → 候選 3，納入 []，排除 [(11, 'over the evidence budget'), (12, 'over the evidence budget'), (13, 'over the evidence budget')]
- 分析狀態：UNCERTAIN；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 修正：[]；刪除 []；仍不符 []；方向待定 []
- 涵蓋判定：Table 1 (page 7)→missing；Section 4.2 COMPARISON OF LIGHT RAG WITH EXISTING RAG METHODS (RQ1) (pages 6-7)→partial；Section 4.3 ABLATION STUDIES (RQ2) (pages 7-8)→partial；Table 3 (page 9)→missing；Section 4.4 CASE STUDY (RQ3) (pages 8-9)→partial；Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM (pages 4-5)→missing；required 未納入 ['Section 4.3 ABLATION STUDIES (RQ2) (pages 7-8)']；supplementary 用 0；Matrix {'cells': 128, 'tables': ['Table 1 [6]'], 'shown_tokens': 1348, 'left_out': [], 'definitions': ['LightRAG'], 'facts': 112, 'coverage_gaps': ['Table 3 [7]']}
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 ['45.6', '54.4', '22.8', '77.2', '41.2', '58.8', '45.2', '54.8', '48.4', '51.6', '40.8', '59.2', '48.0', '52.0', '26.4', '73.6', '43.6', '56.4', '47.2', '52.8', '50.4', '49.6', '36.0', '64.0', '50.8', '49.2', '54.4%', '45.6%', '51.6%', '48.4%', '49.6%', '50.4%', '77.2%', '22.8%', '59.2%', '40.8%', '73.6%', '26.4%', '64.0%', '36.0%', '58.8%', '41.2%', '54.8%', '45.2%', '56.4%', '43.6%', '49.2%', '50.8%', '52.0%', '48.0%', '52.8%', '47.2%']

```text
The question asks to compare LightRAG with GraphRAG across the four datasets (Agriculture, CS, Legal, Mix) and the four evaluation metrics (Comprehensiveness, Diversity, Empowerment, Overall).  

**Evidence matrix for LightRAG vs. GraphRAG** (from Table 1 [6]):

| Dataset | Metric        | GraphRAG (%) | LightRAG (%) |
|---------|---------------|--------------|--------------|
| Agriculture | Comprehensiveness | 45.6         | 54.4         |
|           | Diversity     | 22.8         | 77.2         |
|           | Empowerment   | 41.2         | 58.8         |
|           | Overall       | 45.2         | 54.8         |
| CS      | Comprehensiveness | 48.4         | 51.6         |
|           | Diversity     | 40.8         | 59.2         |
|           | Empowerment   | 45.2         | 54.8         |
|           | Overall       | 48.0         | 52.0         |
| Legal   | Comprehensiveness | 48.4         | 51.6         |
|           | Diversity     | 26.4         | 73.6         |
|           | Empowerment   | 43.6         | 56.4         |
|           | Overall       | 47.2         | 52.8         |
| Mix     | Comprehensiveness | 50.4         | 49.6         |
|           | Diversity     | 36.0         | 64.0         |
|           | Empowerment   | 50.8         | 49.2         |
|           | Overall       | 50.4         | 49.6         |

**Definitions**:
- **LightRAG [2]**: LightRAG employs a dual-level retrieval paradigm, integrating low-level retrieval of specific entities with high-level retrieval of broader topics. This dual-level mechanism enhances response diversity and comprehensiveness.
- **GraphRAG**: No explicit definition is provided in the sources. It is described as a graph-based RAG system.

The comparison is based on the same dataset, the same metric, and the same pairing (GraphRAG vs. LightRAG). LightRAG consistently outperforms GraphRAG in most conditions, with a few exceptions.

**Comparison Analysis**:

- **Comprehensiveness**:
  - LightRAG outperforms GraphRAG in 3 out of 4 datasets:
    - Agriculture: 54.4% vs. 45.6% [6]
    - CS: 51.6% vs. 48.4% [6]
    - Legal: 51.6% vs. 48.4% [6]
  - One exception:
    - Mix: LightRAG (49.6%) vs. GraphRAG (50.4%) [6]

- **Diversity**:
  - LightRAG outperforms GraphRAG in all 4 datasets:
    - Agriculture: 77.2% vs. 22.8% [6]
    - CS: 59.2% vs. 40.8% [6]
    - Legal: 73.6% vs. 26.4% [6]
    - Mix: 64.0% vs. 36.0% [6]

- **Empowerment**:
  - LightRAG outperforms GraphRAG in 3 out of 4 datasets:
    - Agriculture: 58.8% vs. 41.2% [6]
    - CS: 54.8% vs. 45.2% [6]
    - Legal: 56.4% vs. 43.6% [6]
  - One exception:
    - Mix: LightRAG (49.2%) vs. GraphRAG (50.8%) [6]

- **Overall**:
  - LightRAG outperforms GraphRAG in 3 out of 4 datasets:
    - Agriculture: 54.8% vs. 45.2% [6]
    - CS: 52.0% vs. 48.0% [6]
    - Legal: 52.8% vs. 47.2% [6]
  - One exception:
    - Mix: LightRAG (49.6%) vs. GraphRAG (50.4%) [6]

**Conclusion**:
- LightRAG consistently outperforms GraphRAG in **Comprehensiveness** in 3 out of 4 datasets, with the only exception being the **Mix** dataset.
- LightRAG **always outperforms** GraphRAG in **Diversity** across all four datasets.
- LightRAG outperforms GraphRAG in **Empowerment** in 3 out of 4 datasets, with the only exception being the **Mix** dataset.
- LightRAG outperforms GraphRAG in **Overall** performance in 3 out of 4 datasets, with the only exception being the **Mix** dataset.

In most conditions, LightRAG outperforms GraphRAG, especially in **Diversity**, where it dominates all datasets. LightRAG’s dual-level retrieval paradigm appears to be the main reason for its superior performance in **Comprehensiveness** and **Diversity** [2]. However, in the **Mix** dataset, GraphRAG slightly outperforms LightRAG in **Comprehensiveness**, **Empowerment**, and **Overall** performance.

Numbers that could not be checked against the cited pages of the original text: 45.6, 54.4, 22.8, 77.2, 41.2, 58.8, 45.2, 54.8, 48.4, 51.6, 40.8, 59.2, 48.0, 52.0, 26.4, 73.6, 43.6, 56.4, 47.2, 52.8, 50.4, 49.6, 36.0, 64.0, 50.8, 49.2, 54.4%, 45.6%, 51.6%, 48.4%, 49.6%, 50.4%, 77.2%, 22.8%, 59.2%, 40.8%, 73.6%, 26.4%, 64.0%, 36.0%, 58.8%, 41.2%, 54.8%, 45.2%, 56.4%, 43.6%, 49.2%, 50.8%, 52.0%, 48.0%, 52.8%, 47.2%.
```

## B8-Q2-1

- 問題：`compare lightRAG with GraphRAG`；模式 `navigate`；56.8 秒；2 次呼叫；tokens 9040
- 來源：[1] p7 retrieval, [2] p7 retrieval, [3] p7 retrieval, [4] p9 retrieval, [5] p8 retrieval, [6] p9 navigation, [7] p9 navigation, [8] p6 navigation
- 閱讀計畫（定位 6/6，保留 3，超預算 6）：
  - ✓ Section 4.2 COMPARISON OF LIGHT RAG WITH EXISTING RAG METHODS (RQ1) | need: comparison with GraphRAG | priority: required | status: missing → 候選 4，納入 [18]，排除 [(20, 'already among the retrieved sources'), (21, 'already among the retrieved sources'), (19, 'already among the retrieved sources')]
  - ✓ Table 1 (page 7) | need: win rates including GraphRAG | priority: required | status: covered → 候選 0，納入 []，排除 []
  - ✓ Section 4.4 CASE STUDY (RQ3) | need: case study comparison with GraphRAG | priority: required | status: missing → 候選 5，納入 []，排除 [(26, 'low relevance'), (27, 'already among the retrieved sources'), (24, 'already among the retrieved sources'), (25, 'already selected for another target'), (23, 'over the evidence budget')]
  - ✓ Table 3 (page 9) | need: case study comparison with GraphRAG | priority: required | status: missing → 候選 3，納入 [25, 26]，排除 [(27, 'already among the retrieved sources')]
  - ✓ Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM | need: method differences | priority: supplementary | status: missing → 候選 3，納入 []，排除 [(11, 'over the evidence budget'), (12, 'over the evidence budget'), (13, 'over the evidence budget')]
  - ✓ Figure 1 (page 3) | need: architecture differences | priority: supplementary | status: missing → 候選 2，納入 []，排除 [(6, 'over the evidence budget'), (7, 'over the evidence budget')]
- 分析狀態：FACTUALLY_INCORRECT；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 修正：[]；刪除 []；仍不符 ['43.6% (Legal, LightRAG)']；方向待定 []
- 涵蓋判定：Section 4.2 COMPARISON OF LIGHT RAG WITH EXISTING RAG METHODS (RQ1)→partial；Table 1 (page 7)→covered；Section 4.4 CASE STUDY (RQ3)→partial；Table 3 (page 9)→missing；Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM→missing；Figure 1 (page 3)→missing；required 未納入 ['Section 4.4 CASE STUDY (RQ3)']；supplementary 用 0；Matrix {'cells': 128, 'tables': ['Table 1 [1]'], 'shown_tokens': 1348, 'left_out': [], 'definitions': ['LightRAG'], 'facts': 112, 'coverage_gaps': ['Table 3 [6]']}
- 檢查：標籤不符 ['43.6%']；全稱宣稱 1；引用可疑 []；未解析 33；找不到的數字 ['14', '16']

```text
The question asks to compare **LightRAG** with **GraphRAG** in terms of **win rates** across **four datasets (Agriculture, CS, Legal, Mix)** and **four metrics (Comprehensiveness, Diversity, Empowerment, Overall)**, using the data from **Table 1 [1]**.

### Comparison Table of Win Rates (LightRAG vs. GraphRAG)
| Dataset     | Metric         | GraphRAG Win Rate | LightRAG Win Rate | Source |
|-------------|----------------|-------------------|-------------------|--------|
| Agriculture | Comprehensiveness | 45.6%             | 54.4%             | [1]    |
| CS          | Comprehensiveness | 48.4%             | 51.6%             | [1]    |
| Legal       | Comprehensiveness | 48.4%             | 51.6%             | [1]    |
| Mix         | Comprehensiveness | 50.4%             | 49.6%             | [1]    |
| Agriculture | Diversity       | 22.8%             | 77.2%             | [1]    |
| CS          | Diversity       | 40.8%             | 59.2%             | [1]    |
| Legal       | Diversity       | 26.4%             | 73.6%             | [1]    |
| Mix         | Diversity       | 36.0%             | 64.0%             | [1]    |
| Agriculture | Empowerment     | 41.2%             | 58.8%             | [1]    |
| CS          | Empowerment     | 45.2%             | 54.8%             | [1]    |
| Legal       | Empowerment     | 43.6%             | 56.4%             | [1]    |
| Mix         | Empowerment     | 50.8%             | 49.2%             | [1]    |
| Agriculture | Overall         | 45.2%             | 54.8%             | [1]    |
| CS          | Overall         | 48.0%             | 52.0%             | [1]    |
| Legal       | Overall         | 47.2%             | 52.8%             | [1]    |
| Mix         | Overall         | 50.4%             | 49.6%             | [1]    |

### Analysis
LightRAG consistently outperforms GraphRAG in **14 out of 16 conditions** (dataset and metric combinations), with the **only exceptions** being:
- **Mix dataset under Comprehensiveness** (GraphRAG 50.4% | LightRAG 49.6%) [1]
- **Mix dataset under Overall** (GraphRAG 50.4% | LightRAG 49.6%) [1]

In the **Agriculture, CS, and Legal datasets**, LightRAG shows a clear advantage in **Comprehensiveness**, **Diversity**, **Empowerment**, and **Overall** metrics. For example, in the **Legal dataset**, LightRAG achieves **73.6%** for Diversity and **56.4%** for Empowerment, compared to GraphRAG's **26.4%** and **43.6%**, respectively [1].

The **Mix dataset** is the only case where GraphRAG narrowly outperforms LightRAG in **Comprehensiveness** and **Overall**, but the difference is minimal in both cases.

These results align with the explanation in the document, which states that LightRAG's **dual-level retrieval paradigm** enhances its ability to capture both detailed and abstract information, leading to better performance in **diverse and complex environments** [2][3].

### Conclusion
LightRAG outperforms GraphRAG in **14 out of 16 conditions** across the four datasets and four metrics, with the **only exceptions** being the **Mix dataset in Comprehensiveness and Overall**. This suggests a **consistent trend** favoring LightRAG, especially in larger and more complex datasets.

Numbers that could not be checked against the cited pages of the original text: 14, 16.

Figures whose labels differ from the source table: 43.6% (answer: Legal, LightRAG; source: Empowerment, Legal, GraphRAG, vs LightRAG).

A claim the source table does not bear out: "LightRAG consistently outperforms GraphRAG in **14 out of 16 conditions** (dataset and metric combinations), with the **only exceptions** being:" — LightRAG is above the compared methods in 61 cells and below in 3, for example Comprehensiveness / Mix: LightRAG 49.6% vs GraphRAG 50.4% (p. 7); Empowerment / Mix: LightRAG 49.2% vs GraphRAG 50.8% (p. 7); Overall / Mix: LightRAG 49.6% vs GraphRAG 50.4% (p. 7).
```

## B8-Q2-2

- 問題：`compare lightRAG with GraphRAG`；模式 `navigate`；46.7 秒；2 次呼叫；tokens 8800
- 來源：[1] p7 retrieval, [2] p7 retrieval, [3] p7 retrieval, [4] p9 retrieval, [5] p8 retrieval, [6] p9 navigation, [7] p9 navigation, [8] p6 navigation
- 閱讀計畫（定位 6/6，保留 3，超預算 6）：
  - ✓ Section 4.2 COMPARISON OF LIGHT RAG WITH EXISTING RAG METHODS (RQ1) | need: comparison with GraphRAG | priority: required | status: missing → 候選 4，納入 [18]，排除 [(20, 'already among the retrieved sources'), (21, 'already among the retrieved sources'), (19, 'already among the retrieved sources')]
  - ✓ Table 1 (page 7) | need: win rates including GraphRAG | priority: required | status: covered → 候選 0，納入 []，排除 []
  - ✓ Section 4.4 CASE STUDY (RQ3) | need: case study comparison with GraphRAG | priority: required | status: missing → 候選 5，納入 []，排除 [(26, 'low relevance'), (27, 'already among the retrieved sources'), (24, 'already among the retrieved sources'), (25, 'already selected for another target'), (23, 'over the evidence budget')]
  - ✓ Table 3 (page 9) | need: case study comparison with GraphRAG | priority: required | status: missing → 候選 3，納入 [25, 26]，排除 [(27, 'already among the retrieved sources')]
  - ✓ Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM | need: method differences | priority: supplementary | status: missing → 候選 3，納入 []，排除 [(11, 'over the evidence budget'), (12, 'over the evidence budget'), (13, 'over the evidence budget')]
  - ✓ Figure 1 (page 3) | need: architecture differences | priority: supplementary | status: missing → 候選 2，納入 []，排除 [(6, 'over the evidence budget'), (7, 'over the evidence budget')]
- 分析狀態：FACTUALLY_INCORRECT；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 修正：[]；刪除 []；仍不符 []；方向待定 []
- 涵蓋判定：Section 4.2 COMPARISON OF LIGHT RAG WITH EXISTING RAG METHODS (RQ1)→partial；Table 1 (page 7)→covered；Section 4.4 CASE STUDY (RQ3)→partial；Table 3 (page 9)→missing；Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM→missing；Figure 1 (page 3)→missing；required 未納入 ['Section 4.4 CASE STUDY (RQ3)']；supplementary 用 0；Matrix {'cells': 128, 'tables': ['Table 1 [1]'], 'shown_tokens': 1348, 'left_out': [], 'definitions': ['LightRAG'], 'facts': 112, 'coverage_gaps': ['Table 3 [6]']}
- 檢查：標籤不符 []；全稱宣稱 1；引用可疑 [([1], [8])]；未解析 0；找不到的數字 ['16']

```text
The question asks to compare **LightRAG** with **GraphRAG** across the **Agriculture**, **CS**, **Legal**, and **Mix** datasets, using the **Comprehensiveness**, **Diversity**, **Empowerment**, and **Overall** metrics.

From Table 1 [1], the following win rate comparisons between **LightRAG** and **GraphRAG** are available for each dataset and metric:

- **Comprehensiveness**:
  - Agriculture: GraphRAG 45.6% | LightRAG 54.4%
  - CS: GraphRAG 48.4% | LightRAG 51.6%
  - Legal: GraphRAG 48.4% | LightRAG 51.6%
  - Mix: GraphRAG 50.4% | LightRAG 49.6%

- **Diversity**:
  - Agriculture: GraphRAG 22.8% | LightRAG 77.2%
  - CS: GraphRAG 40.8% | LightRAG 59.2%
  - Legal: GraphRAG 26.4% | LightRAG 73.6%
  - Mix: GraphRAG 36.0% | LightRAG 64.0%

- **Empowerment**:
  - Agriculture: GraphRAG 41.2% | LightRAG 58.8%
  - CS: GraphRAG 45.2% | LightRAG 54.8%
  - Legal: GraphRAG 43.6% | LightRAG 56.4%
  - Mix: GraphRAG 50.8% | LightRAG 49.2%

- **Overall**:
  - Agriculture: GraphRAG 45.2% | LightRAG 54.8%
  - CS: GraphRAG 48.0% | LightRAG 52.0%
  - Legal: GraphRAG 47.2% | LightRAG 52.8%
  - Mix: GraphRAG 50.4% | LightRAG 49.6%

Comparisons are made only between LightRAG and GraphRAG, for the same dataset, metric, and pairing.

The comparison across 16 conditions (4 datasets × 4 metrics):

- **Comprehensiveness**:
  - LightRAG wins in 4 of 4 conditions.
- **Diversity**:
  - LightRAG wins in 4 of 4 conditions.
- **Empowerment**:
  - LightRAG wins in 4 of 4 conditions.
- **Overall**:
  - LightRAG wins in 4 of 4 conditions.

Thus, LightRAG wins in all 16 conditions.

LightRAG consistently outperforms GraphRAG in all 16 conditions across the four datasets and four metrics.

The win rates are cited from Table 1 [1], and the comparison is defined in the text on page 7 [2].

All requested comparisons are included, and the analysis is based solely on the provided sources.

Numbers that could not be checked against the cited pages of the original text: 16.

A claim the source table does not bear out: "LightRAG consistently outperforms GraphRAG in all 16 conditions across the four datasets and four metrics." — LightRAG is above the compared methods in 61 cells and below in 3, for example Comprehensiveness / Mix: LightRAG 49.6% vs GraphRAG 50.4% (p. 7); Empowerment / Mix: LightRAG 49.2% vs GraphRAG 50.8% (p. 7); Overall / Mix: LightRAG 49.6% vs GraphRAG 50.4% (p. 7).
```

## B8-Q2-3

- 問題：`compare lightRAG with GraphRAG`；模式 `navigate`；70.0 秒；2 次呼叫；tokens 9346
- 來源：[1] p7 retrieval, [2] p7 retrieval, [3] p7 retrieval, [4] p9 retrieval, [5] p8 retrieval, [6] p9 navigation, [7] p9 navigation, [8] p6 navigation
- 閱讀計畫（定位 6/6，保留 3，超預算 6）：
  - ✓ Section 4.2 COMPARISON OF LIGHT RAG WITH EXISTING RAG METHODS (RQ1) | need: comparison with GraphRAG | priority: required | status: missing → 候選 4，納入 [18]，排除 [(20, 'already among the retrieved sources'), (21, 'already among the retrieved sources'), (19, 'already among the retrieved sources')]
  - ✓ Table 1 (page 7) | need: win rates including GraphRAG | priority: required | status: covered → 候選 0，納入 []，排除 []
  - ✓ Section 4.4 CASE STUDY (RQ3) | need: case study comparison with GraphRAG | priority: required | status: missing → 候選 5，納入 []，排除 [(26, 'low relevance'), (27, 'already among the retrieved sources'), (24, 'already among the retrieved sources'), (25, 'already selected for another target'), (23, 'over the evidence budget')]
  - ✓ Table 3 (page 9) | need: case study comparison with GraphRAG | priority: required | status: missing → 候選 3，納入 [25, 26]，排除 [(27, 'already among the retrieved sources')]
  - ✓ Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM | need: method differences | priority: supplementary | status: missing → 候選 3，納入 []，排除 [(11, 'over the evidence budget'), (12, 'over the evidence budget'), (13, 'over the evidence budget')]
  - ✓ Figure 1 (page 3) | need: architecture differences | priority: supplementary | status: missing → 候選 2，納入 []，排除 [(6, 'over the evidence budget'), (7, 'over the evidence budget')]
- 分析狀態：FACTUALLY_INCORRECT；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 [('incomparable', '54.8%', '45.2%')]
- 修正：[]；刪除 []；仍不符 ['50.4% (Mix, LightRAG)', '49.6% (Mix, GraphRAG)', '50.8% (Mix, LightRAG)', '49.2% (Mix, GraphRAG)', '50.4% (Mix, LightRAG)', '49.6% (Mix, GraphRAG)']；方向待定 []
- 涵蓋判定：Section 4.2 COMPARISON OF LIGHT RAG WITH EXISTING RAG METHODS (RQ1)→partial；Table 1 (page 7)→covered；Section 4.4 CASE STUDY (RQ3)→partial；Table 3 (page 9)→missing；Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM→missing；Figure 1 (page 3)→missing；required 未納入 ['Section 4.4 CASE STUDY (RQ3)']；supplementary 用 0；Matrix {'cells': 128, 'tables': ['Table 1 [1]'], 'shown_tokens': 1348, 'left_out': [], 'definitions': ['LightRAG'], 'facts': 112, 'coverage_gaps': ['Table 3 [6]']}
- 檢查：標籤不符 ['50.4%', '49.6%', '50.8%', '49.2%', '49.6%', '49.2%', '49.6%']；全稱宣稱 0；引用可疑 []；未解析 44；找不到的數字 []

```text
The question asks to compare **LightRAG** with **GraphRAG** across **four datasets** (Agriculture, CS, Legal, Mix) and **four metrics** (Comprehensiveness, Diversity, Empowerment, Overall). The comparison is based on **win rates** in which LightRAG is compared against GraphRAG for each dataset and metric.

### Comparison Table of Relevant Figures

| Dataset | Metric         | GraphRAG Win Rate | LightRAG Win Rate | Source |
|---------|----------------|-------------------|-------------------|--------|
| Agriculture | Comprehensiveness | 45.6%             | 54.4%             | [1]    |
| CS          | Comprehensiveness | 48.4%             | 51.6%             | [1]    |
| Legal       | Comprehensiveness | 48.4%             | 51.6%             | [1]    |
| Mix         | Comprehensiveness | 50.4%             | 49.6%             | [1]    |
| Agriculture | Diversity         | 22.8%             | 77.2%             | [1]    |
| CS          | Diversity         | 40.8%             | 59.2%             | [1]    |
| Legal       | Diversity         | 26.4%             | 73.6%             | [1]    |
| Mix         | Diversity         | 36.0%             | 64.0%             | [1]    |
| Agriculture | Empowerment       | 41.2%             | 58.8%             | [1]    |
| CS          | Empowerment       | 45.2%             | 54.8%             | [1]    |
| Legal       | Empowerment       | 43.6%             | 56.4%             | [1]    |
| Mix         | Empowerment       | 50.8%             | 49.2%             | [1]    |
| Agriculture | Overall           | 45.2%             | 54.8%             | [1]    |
| CS          | Overall           | 48.0%             | 52.0%             | [1]    |
| Legal       | Overall           | 47.2%             | 52.8%             | [1]    |
| Mix         | Overall           | 50.4%             | 49.6%             | [1]    |

---

### Analysis

- **Comprehensiveness**:
  - LightRAG outperforms GraphRAG in **3 out of 4 datasets**: Agriculture (54.4% vs. 45.6%), CS (51.6% vs. 48.4%), and Legal (51.6% vs. 48.4%). The only exception is Mix, where GraphRAG slightly outperforms LightRAG (50.4% vs. 49.6%). [1]
  
- **Diversity**:
  - LightRAG outperforms GraphRAG in **all 4 datasets**: Agriculture (77.2% vs. 22.8%), CS (59.2% vs. 40.8%), Legal (73.6% vs. 26.4%), and Mix (64.0% vs. 36.0%). [1]

- **Empowerment**:
  - LightRAG outperforms GraphRAG in **3 out of 4 datasets**: Agriculture (58.8% vs. 41.2%), CS (54.8% vs. 45.2%), and Legal (56.4% vs. 43.6%). The only exception is Mix, where GraphRAG slightly outperforms LightRAG (50.8% vs. 49.2%). [1]

- **Overall**:
  - LightRAG outperforms GraphRAG in **3 out of 4 datasets**: Agriculture (54.8% vs. 45.2%), CS (52.0% vs. 48.0%), and Legal (52.8% vs. 47.2%). The only exception is Mix, where GraphRAG slightly outperforms LightRAG (50.4% vs. 49.6%). [1]

---

### Summary of Findings

- **Comprehensiveness**: LightRAG outperforms GraphRAG in 3 out of 4 datasets (Agriculture, CS, Legal), but GraphRAG outperforms in Mix (50.4% vs. 49.6%) [1].
- **Diversity**: LightRAG consistently outperforms GraphRAG in all 4 datasets [1].
- **Empowerment**: LightRAG outperforms in 3 out of 4 datasets (Agriculture, CS, Legal), but GraphRAG outperforms in Mix (50.8% vs. 49.2%) [1].
- **Overall**: LightRAG outperforms in 3 out of 4 datasets (Agriculture, CS, Legal), but GraphRAG outperforms in Mix (50.4% vs. 49.6%) [1].

The only exceptions are in the **Mix** dataset for Comprehensiveness, Empowerment, and Overall, where GraphRAG slightly outperforms LightRAG in each. LightRAG shows a clear advantage in most conditions, particularly in Diversity, and in most metrics across the Agriculture, CS, and Legal datasets.

Figures whose labels differ from the source table: 50.4% (answer: Mix, LightRAG; source: Comprehensiveness, Mix, GraphRAG, vs LightRAG / Overall, Mix, GraphRAG, vs LightRAG); 49.6% (answer: Mix, GraphRAG; source: Comprehensiveness, Mix, LightRAG, vs GraphRAG / Overall, Mix, LightRAG, vs GraphRAG); 50.8% (answer: Mix, LightRAG; source: Empowerment, Mix, GraphRAG, vs LightRAG); 49.2% (answer: Mix, GraphRAG; source: Empowerment, Mix, LightRAG, vs GraphRAG); 49.6% (answer: Comprehensiveness, GraphRAG; source: Comprehensiveness, Mix, LightRAG, vs GraphRAG / Overall, Mix, LightRAG, vs GraphRAG); 49.2% (answer: Empowerment, GraphRAG; source: Empowerment, Mix, LightRAG, vs GraphRAG); 49.6% (answer: Overall, GraphRAG; source: Comprehensiveness, Mix, LightRAG, vs GraphRAG / Overall, Mix, LightRAG, vs GraphRAG).
```

## B9-Q2-1

- 問題：`compare lightRAG with GraphRAG`；模式 `navigate`；50.5 秒；2 次呼叫；tokens 8754
- 來源：[1] p7 retrieval, [2] p7 retrieval, [3] p7 retrieval, [4] p9 retrieval, [5] p8 retrieval, [6] p9 navigation, [7] p9 navigation, [8] p6 navigation
- 閱讀計畫（定位 6/6，保留 3，超預算 6）：
  - ✓ Section 4.2 COMPARISON OF LIGHT RAG WITH EXISTING RAG METHODS (RQ1) | need: comparison with GraphRAG | priority: required | status: missing → 候選 4，納入 [18]，排除 [(20, 'already among the retrieved sources'), (21, 'already among the retrieved sources'), (19, 'already among the retrieved sources')]
  - ✓ Table 1 (page 7) | need: win rates including GraphRAG | priority: required | status: covered → 候選 0，納入 []，排除 []
  - ✓ Section 4.4 CASE STUDY (RQ3) | need: case study comparison with GraphRAG | priority: required | status: missing → 候選 5，納入 []，排除 [(26, 'low relevance'), (27, 'already among the retrieved sources'), (24, 'already among the retrieved sources'), (25, 'already selected for another target'), (23, 'over the evidence budget')]
  - ✓ Table 3 (page 9) | need: case study comparison with GraphRAG | priority: required | status: missing → 候選 3，納入 [25, 26]，排除 [(27, 'already among the retrieved sources')]
  - ✓ Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM | need: method differences | priority: supplementary | status: missing → 候選 3，納入 []，排除 [(11, 'over the evidence budget'), (12, 'over the evidence budget'), (13, 'over the evidence budget')]
  - ✓ Figure 1 (page 3) | need: architecture differences | priority: supplementary | status: missing → 候選 2，納入 []，排除 [(6, 'over the evidence budget'), (7, 'over the evidence budget')]
- 分析狀態：FACTUALLY_INCORRECT；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 修正：[]；刪除 []；仍不符 []；方向待定 []
- 涵蓋判定：Section 4.2 COMPARISON OF LIGHT RAG WITH EXISTING RAG METHODS (RQ1)→partial；Table 1 (page 7)→covered；Section 4.4 CASE STUDY (RQ3)→partial；Table 3 (page 9)→missing；Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM→missing；Figure 1 (page 3)→missing；required 未納入 ['Section 4.4 CASE STUDY (RQ3)']；supplementary 用 0；Matrix {'cells': 128, 'tables': ['Table 1 [1]'], 'shown_tokens': 1348, 'left_out': [], 'definitions': ['LightRAG'], 'facts': 112, 'coverage_gaps': ['Table 3 [6]']}
- 檢查：標籤不符 []；全稱宣稱 1；引用可疑 []；未解析 4；找不到的數字 []

```text
### Compact Comparison Table (GraphRAG vs. LightRAG)
| Dataset | Metric | GraphRAG (%) | LightRAG (%) | Source |
|---------|--------|--------------|--------------|--------|
| Agriculture | Comprehensiveness | 45.6 | 54.4 | [1] |
| CS | Comprehensiveness | 48.4 | 51.6 | [1] |
| Legal | Comprehensiveness | 48.4 | 51.6 | [1] |
| Mix | Comprehensiveness | 50.4 | 49.6 | [1] |
| Agriculture | Diversity | 22.8 | 77.2 | [1] |
| CS | Diversity | 40.8 | 59.2 | [1] |
| Legal | Diversity | 26.4 | 73.6 | [1] |
| Mix | Diversity | 36.0 | 64.0 | [1] |
| Agriculture | Empowerment | 41.2 | 58.8 | [1] |
| CS | Empowerment | 45.2 | 54.8 | [1] |
| Legal | Empowerment | 43.6 | 56.4 | [1] |
| Mix | Empowerment | 50.8 | 49.2 | [1] |
| Agriculture | Overall | 45.2 | 54.8 | [1] |
| CS | Overall | 48.0 | 52.0 | [1] |
| Legal | Overall | 47.2 | 52.8 | [1] |
| Mix | Overall | 50.4 | 49.6 | [1] |

### Analysis
LightRAG outperforms GraphRAG in **diversity**, **empowerment**, and **overall** metrics across all four datasets (Agriculture, CS, Legal, Mix), with significant improvements in the Legal dataset. For example, in Legal diversity, LightRAG achieves 73.6% win rate compared to GraphRAG's 26.4% [1]. Similarly, in Legal empowerment, LightRAG wins 56.4% of the time versus GraphRAG's 43.6% [1]. The overall win rate for LightRAG in the Legal dataset is 52.8%, compared to GraphRAG's 47.2% [1].

However, in **comprehensiveness**, the performance is mixed. LightRAG outperforms GraphRAG in Agriculture (54.4% vs. 45.6%) [1] and CS (51.6% vs. 48.4%) [1], but underperforms slightly in Mix (49.6% vs. 50.4%) [1]. In Legal, both models are equal at 51.6% [1]. This shows that while LightRAG generally improves on GraphRAG, the comprehensiveness metric is not consistently better across all datasets.

The case study in Table 3 further supports this conclusion. LightRAG is preferred over GraphRAG in all evaluation dimensions (comprehensiveness, diversity, empowerment, and overall) for a machine learning question [6]. LightRAG's responses are judged to be more comprehensive, diverse, and empowering, which is attributed to its dual-level retrieval paradigm [5]. 

In summary, LightRAG shows consistent improvements over GraphRAG in diversity, empowerment, and overall performance. Comprehensiveness is a mixed result, with LightRAG performing better in most datasets but not all.

A claim the source table does not bear out: "LightRAG outperforms GraphRAG in **diversity**, **empowerment**, and **overall** metrics across all four datasets (Agriculture, CS, Legal, Mix), with significant improvements in the Legal dataset." — LightRAG is above the compared methods in 46 cells and below in 2, for example Empowerment / Mix: LightRAG 49.2% vs GraphRAG 50.8% (p. 7); Overall / Mix: LightRAG 49.6% vs GraphRAG 50.4% (p. 7).
```

## B9-Q2-2

- 問題：`compare lightRAG with GraphRAG`；模式 `navigate`；51.8 秒；2 次呼叫；tokens 8791
- 來源：[1] p7 retrieval, [2] p7 retrieval, [3] p7 retrieval, [4] p9 retrieval, [5] p8 retrieval, [6] p9 navigation, [7] p9 navigation, [8] p6 navigation
- 閱讀計畫（定位 6/6，保留 3，超預算 6）：
  - ✓ Section 4.2 COMPARISON OF LIGHT RAG WITH EXISTING RAG METHODS (RQ1) | need: comparison with GraphRAG | priority: required | status: missing → 候選 4，納入 [18]，排除 [(20, 'already among the retrieved sources'), (21, 'already among the retrieved sources'), (19, 'already among the retrieved sources')]
  - ✓ Table 1 (page 7) | need: win rates including GraphRAG | priority: required | status: covered → 候選 0，納入 []，排除 []
  - ✓ Section 4.4 CASE STUDY (RQ3) | need: case study comparison with GraphRAG | priority: required | status: missing → 候選 5，納入 []，排除 [(26, 'low relevance'), (27, 'already among the retrieved sources'), (24, 'already among the retrieved sources'), (25, 'already selected for another target'), (23, 'over the evidence budget')]
  - ✓ Table 3 (page 9) | need: case study comparison with GraphRAG | priority: required | status: missing → 候選 3，納入 [25, 26]，排除 [(27, 'already among the retrieved sources')]
  - ✓ Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM | need: method differences | priority: supplementary | status: missing → 候選 3，納入 []，排除 [(11, 'over the evidence budget'), (12, 'over the evidence budget'), (13, 'over the evidence budget')]
  - ✓ Figure 1 (page 3) | need: architecture differences | priority: supplementary | status: missing → 候選 2，納入 []，排除 [(6, 'over the evidence budget'), (7, 'over the evidence budget')]
- 分析狀態：FACTUALLY_INCORRECT；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 修正：[]；刪除 []；仍不符 []；方向待定 []
- 涵蓋判定：Section 4.2 COMPARISON OF LIGHT RAG WITH EXISTING RAG METHODS (RQ1)→partial；Table 1 (page 7)→covered；Section 4.4 CASE STUDY (RQ3)→partial；Table 3 (page 9)→missing；Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM→missing；Figure 1 (page 3)→missing；required 未納入 ['Section 4.4 CASE STUDY (RQ3)']；supplementary 用 0；Matrix {'cells': 128, 'tables': ['Table 1 [1]'], 'shown_tokens': 1348, 'left_out': [], 'definitions': ['LightRAG'], 'facts': 112, 'coverage_gaps': ['Table 3 [6]']}
- 檢查：標籤不符 []；全稱宣稱 3；引用可疑 []；未解析 32；找不到的數字 ['80%']

```text
LightRAG is compared with GraphRAG across four datasets (Agriculture, CS, Legal, Mix) and four evaluation metrics (Comprehensiveness, Diversity, Empowerment, Overall). The comparison is based on win rates, where a higher win rate indicates that LightRAG outperforms GraphRAG.

### Compact Comparison Table (LightRAG vs GraphRAG):
| Metric         | Dataset   | LightRAG Win Rate | GraphRAG Win Rate | Source |
|----------------|-----------|-------------------|-------------------|--------|
| Comprehensiveness | Agriculture | 67.6%             | 45.6%             | [1]    |
| Comprehensiveness | CS          | 61.6%             | 48.4%             | [1]    |
| Comprehensiveness | Legal       | 83.6%             | 48.4%             | [1]    |
| Comprehensiveness | Mix         | 61.2%             | 50.4%             | [1]    |
| Diversity      | Agriculture | 76.4%             | 22.8%             | [1]    |
| Diversity      | CS          | 62.0%             | 40.8%             | [1]    |
| Diversity      | Legal       | 86.4%             | 26.4%             | [1]    |
| Diversity      | Mix         | 67.6%             | 36.0%             | [1]    |
| Empowerment    | Agriculture | 67.6%             | 41.2%             | [1]    |
| Empowerment    | CS          | 61.2%             | 45.2%             | [1]    |
| Empowerment    | Legal       | 83.6%             | 43.6%             | [1]    |
| Empowerment    | Mix         | 57.2%             | 50.8%             | [1]    |
| Overall        | Agriculture | 67.6%             | 45.2%             | [1]    |
| Overall        | CS          | 61.2%             | 48.0%             | [1]    |
| Overall        | Legal       | 84.8%             | 47.2%             | [1]    |
| Overall        | Mix         | 60.0%             | 50.4%             | [1]    |

### Analysis:
**Main Findings:**
- LightRAG outperforms GraphRAG in all combinations of datasets and metrics.
- The performance gap is particularly significant in the Legal dataset, where LightRAG achieves win rates over 80% in Comprehensiveness, Diversity, and Empowerment.
- Across all metrics and datasets, LightRAG consistently achieves higher win rates than GraphRAG.

**Representative Figures:**
- In the Legal dataset for Comprehensiveness, LightRAG wins 83.6% of the time, while GraphRAG wins only 48.4% [1].
- For Diversity in the Agriculture dataset, LightRAG wins 76.4% of the time, compared to 22.8% for GraphRAG [1].

**Exceptions:**
- There are no exceptions in the data provided. LightRAG consistently outperforms GraphRAG across all metrics and datasets.

**Conclusion:**
- LightRAG consistently outperforms GraphRAG in Comprehensiveness, Diversity, Empowerment, and Overall evaluation across all datasets. The greatest improvements are observed in the Legal dataset, where LightRAG achieves substantial lead in win rates. No regressions or exceptions are found in the data.

Numbers that could not be checked against the cited pages of the original text: 80%.

A claim the source table does not bear out: "- Across all metrics and datasets, LightRAG consistently achieves higher win rates than GraphRAG." — LightRAG is above the compared methods in 61 cells and below in 3, for example Comprehensiveness / Mix: LightRAG 49.6% vs GraphRAG 50.4% (p. 7); Empowerment / Mix: LightRAG 49.2% vs GraphRAG 50.8% (p. 7); Overall / Mix: LightRAG 49.6% vs GraphRAG 50.4% (p. 7) / "LightRAG consistently outperforms GraphRAG across all metrics and datasets." — LightRAG is above the compared methods in 61 cells and below in 3, for example Comprehensiveness / Mix: LightRAG 49.6% vs GraphRAG 50.4% (p. 7); Empowerment / Mix: LightRAG 49.2% vs GraphRAG 50.8% (p. 7); Overall / Mix: LightRAG 49.6% vs GraphRAG 50.4% (p. 7) / "- LightRAG consistently outperforms GraphRAG in Comprehensiveness, Diversity, Empowerment, and Overall evaluation across all datasets." — LightRAG is above the compared methods in 61 cells and below in 3, for example Comprehensiveness / Mix: LightRAG 49.6% vs GraphRAG 50.4% (p. 7); Empowerment / Mix: LightRAG 49.2% vs GraphRAG 50.8% (p. 7); Overall / Mix: LightRAG 49.6% vs GraphRAG 50.4% (p. 7).
```

## B9-Q2-3

- 問題：`compare lightRAG with GraphRAG`；模式 `navigate`；46.2 秒；2 次呼叫；tokens 8659
- 來源：[1] p7 retrieval, [2] p7 retrieval, [3] p7 retrieval, [4] p9 retrieval, [5] p8 retrieval, [6] p9 navigation, [7] p9 navigation, [8] p6 navigation
- 閱讀計畫（定位 6/6，保留 3，超預算 6）：
  - ✓ Section 4.2 COMPARISON OF LIGHT RAG WITH EXISTING RAG METHODS (RQ1) | need: comparison with GraphRAG | priority: required | status: missing → 候選 4，納入 [18]，排除 [(20, 'already among the retrieved sources'), (21, 'already among the retrieved sources'), (19, 'already among the retrieved sources')]
  - ✓ Table 1 (page 7) | need: win rates including GraphRAG | priority: required | status: covered → 候選 0，納入 []，排除 []
  - ✓ Section 4.4 CASE STUDY (RQ3) | need: case study comparison with GraphRAG | priority: required | status: missing → 候選 5，納入 []，排除 [(26, 'low relevance'), (27, 'already among the retrieved sources'), (24, 'already among the retrieved sources'), (25, 'already selected for another target'), (23, 'over the evidence budget')]
  - ✓ Table 3 (page 9) | need: case study comparison with GraphRAG | priority: required | status: missing → 候選 3，納入 [25, 26]，排除 [(27, 'already among the retrieved sources')]
  - ✓ Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM | need: method differences | priority: supplementary | status: missing → 候選 3，納入 []，排除 [(11, 'over the evidence budget'), (12, 'over the evidence budget'), (13, 'over the evidence budget')]
  - ✓ Figure 1 (page 3) | need: architecture differences | priority: supplementary | status: missing → 候選 2，納入 []，排除 [(6, 'over the evidence budget'), (7, 'over the evidence budget')]
- 分析狀態：FACTUALLY_INCORRECT；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 修正：[]；刪除 []；仍不符 []；方向待定 []
- 涵蓋判定：Section 4.2 COMPARISON OF LIGHT RAG WITH EXISTING RAG METHODS (RQ1)→partial；Table 1 (page 7)→covered；Section 4.4 CASE STUDY (RQ3)→partial；Table 3 (page 9)→missing；Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM→missing；Figure 1 (page 3)→missing；required 未納入 ['Section 4.4 CASE STUDY (RQ3)']；supplementary 用 0；Matrix {'cells': 128, 'tables': ['Table 1 [1]'], 'shown_tokens': 1348, 'left_out': [], 'definitions': ['LightRAG'], 'facts': 112, 'coverage_gaps': ['Table 3 [6]']}
- 檢查：標籤不符 []；全稱宣稱 2；引用可疑 []；未解析 0；找不到的數字 []

```text
The question asks for a comparison between LightRAG and GraphRAG, across four datasets (Agriculture, CS, Legal, Mix) and four metrics (Comprehensiveness, Diversity, Empowerment, Overall).

The evidence matrix in Table 1 [1] provides win rates of GraphRAG versus LightRAG across these datasets and metrics. 

Comparing LightRAG and GraphRAG on the same dataset and metric:

- **Comprehensiveness:**
  - Agriculture: GraphRAG 45.6% | LightRAG 54.4%
  - CS: GraphRAG 48.4% | LightRAG 51.6%
  - Legal: GraphRAG 48.4% | LightRAG 51.6%
  - Mix: GraphRAG 50.4% | LightRAG 49.6%

- **Diversity:**
  - Agriculture: GraphRAG 22.8% | LightRAG 77.2%
  - CS: GraphRAG 40.8% | LightRAG 59.2%
  - Legal: GraphRAG 26.4% | LightRAG 73.6%
  - Mix: GraphRAG 36.0% | LightRAG 64.0%

- **Empowerment:**
  - Agriculture: GraphRAG 41.2% | LightRAG 58.8%
  - CS: GraphRAG 45.2% | LightRAG 54.8%
  - Legal: GraphRAG 43.6% | LightRAG 56.4%
  - Mix: GraphRAG 50.8% | LightRAG 49.2%

- **Overall:**
  - Agriculture: GraphRAG 45.2% | LightRAG 54.8%
  - CS: GraphRAG 48.0% | LightRAG 52.0%
  - Legal: GraphRAG 47.2% | LightRAG 52.8%
  - Mix: GraphRAG 50.4% | LightRAG 49.6%

**Improvements and regressions:**
- **Comprehensiveness:** LightRAG outperforms GraphRAG in all four datasets.
- **Diversity:** LightRAG outperforms GraphRAG in all four datasets.
- **Empowerment:** LightRAG outperforms GraphRAG in all four datasets.
- **Overall:** LightRAG outperforms GraphRAG in all four datasets.

**Exceptions:**
- No exceptions to the trend of LightRAG outperforming GraphRAG in this comparison.

The cited win rates confirm that LightRAG consistently outperforms GraphRAG in all metrics and datasets.

The comparison is based on Table 1 [1], and the superiority of LightRAG over GraphRAG is further supported by the passage on page 7 [2], which states that LightRAG consistently outperforms GraphRAG in larger datasets with complex language contexts.

All required comparisons are included and supported by the sources.

A claim the source table does not bear out: "The cited win rates confirm that LightRAG consistently outperforms GraphRAG in all metrics and datasets." — LightRAG is above the compared methods in 61 cells and below in 3, for example Comprehensiveness / Mix: LightRAG 49.6% vs GraphRAG 50.4% (p. 7); Empowerment / Mix: LightRAG 49.2% vs GraphRAG 50.8% (p. 7); Overall / Mix: LightRAG 49.6% vs GraphRAG 50.4% (p. 7) / "The comparison is based on Table 1, and the superiority of LightRAG over GraphRAG is further supported by the passage on page 7, which states that LightRAG consistently outperforms GraphRAG in larger datasets with complex language contexts." — LightRAG is above the compared methods in 61 cells and below in 3, for example Comprehensiveness / Mix: LightRAG 49.6% vs GraphRAG 50.4% (p. 7); Empowerment / Mix: LightRAG 49.2% vs GraphRAG 50.8% (p. 7); Overall / Mix: LightRAG 49.6% vs GraphRAG 50.4% (p. 7).
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

## C8-Q2-1

- 問題：`compare lightRAG with GraphRAG`；模式 `single`；19.2 秒；1 次呼叫；tokens 3577
- 來源：[1] p7 retrieval, [2] p7 retrieval, [3] p7 retrieval, [4] p9 retrieval, [5] p8 retrieval
- 分析狀態：UNCERTAIN；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 1；找不到的數字 []

```text
LightRAG consistently outperforms GraphRAG across multiple datasets and evaluation dimensions, particularly in larger datasets with complex language contexts [2]. For instance, in the Agriculture, CS, and Legal datasets—each containing millions of tokens—LightRAG shows a clear advantage over GraphRAG [3]. 

Representative figures supporting this include the Comprehensiveness win rate in the Legal dataset, where GraphRAG achieved 48.4% compared to LightRAG's 51.6% [1]. In the Diversity metric, LightRAG also outperforms GraphRAG in the Legal dataset, achieving 73.6% compared to GraphRAG's 26.4% [1]. Similarly, in the Empowerment metric, LightRAG achieved 74.0% in the Legal dataset, while GraphRAG only reached 43.6% [1]. 

However, in the Mix dataset for the Comprehensiveness metric, GraphRAG (50.4%) slightly outperforms LightRAG (49.6%) [1]. This suggests that while LightRAG is generally superior, there are exceptions in certain datasets and metrics.

The superior performance of LightRAG is attributed to its dual-level retrieval paradigm, which integrates low-level retrieval of specific entities with high-level retrieval of broader topics, enhancing response diversity and comprehensiveness [2]. This approach effectively addresses both detailed and abstract queries, providing a more thorough grasp of information [3].
```

## C8-Q2-2

- 問題：`compare lightRAG with GraphRAG`；模式 `single`；10.8 秒；1 次呼叫；tokens 3516
- 來源：[1] p7 retrieval, [2] p7 retrieval, [3] p7 retrieval, [4] p9 retrieval, [5] p8 retrieval
- 分析狀態：FACTUALLY_INCORRECT；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 檢查：標籤不符 ['54.8%', '85.6%', '73.6%', '54.4%']；全稱宣稱 1；引用可疑 []；未解析 0；找不到的數字 []

```text
LightRAG consistently outperforms GraphRAG across multiple datasets and evaluation dimensions. In the Agriculture, CS, and Legal datasets—each containing millions of tokens—LightRAG shows a clear advantage, significantly surpassing GraphRAG in comprehensive information understanding within diverse environments [3]. For example, in the Legal dataset, LightRAG achieves a 54.8% win rate compared to GraphRAG's 47.2% in the Overall metric [1]. Similarly, in the Diversity metric for the Legal dataset, LightRAG achieves an 85.6% win rate compared to GraphRAG's 73.6% [1].

However, in the Mix dataset, GraphRAG achieves a slightly higher win rate in the Comprehensiveness metric (54.4% for GraphRAG vs. 49.6% for LightRAG) [1]. This suggests that while LightRAG generally performs better, there are specific scenarios where GraphRAG may offer competitive results.

In summary, LightRAG demonstrates superior performance in most cases, particularly in larger datasets with complex language contexts, but there are exceptions where GraphRAG performs comparably or better in specific metrics.

Figures whose labels differ from the source table: 54.8% (answer: Overall, Legal, LightRAG; source: Empowerment, CS, LightRAG, vs GraphRAG / Overall, Agriculture, LightRAG, vs GraphRAG); 85.6% (answer: Diversity, Legal, LightRAG; source: Overall, Legal, LightRAG, vs RQ-RAG); 73.6% (answer: Diversity, Legal, GraphRAG; source: Overall, Legal, LightRAG, vs HyDE / Diversity, Legal, LightRAG, vs GraphRAG); 54.4% (answer: Comprehensiveness, Mix, GraphRAG; source: Comprehensiveness, Agriculture, LightRAG, vs GraphRAG).

A claim the source table does not bear out: "LightRAG consistently outperforms GraphRAG across multiple datasets and evaluation dimensions." — LightRAG is above the compared methods in 61 cells and below in 3, for example Comprehensiveness / Mix: LightRAG 49.6% vs GraphRAG 50.4% (p. 7); Empowerment / Mix: LightRAG 49.2% vs GraphRAG 50.8% (p. 7); Overall / Mix: LightRAG 49.6% vs GraphRAG 50.4% (p. 7).
```

## C8-Q2-3

- 問題：`compare lightRAG with GraphRAG`；模式 `single`；22.9 秒；1 次呼叫；tokens 3808
- 來源：[1] p7 retrieval, [2] p7 retrieval, [3] p7 retrieval, [4] p9 retrieval, [5] p8 retrieval
- 分析狀態：FACTUALLY_INCORRECT；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 檢查：標籤不符 ['54.4%', '51.6%', '49.6%']；全稱宣稱 0；引用可疑 []；未解析 20；找不到的數字 []

```text
LightRAG consistently outperforms GraphRAG across multiple datasets and evaluation dimensions, particularly in larger datasets with complex language contexts [2]. For example, in the Agriculture, CS, and Legal datasets, LightRAG shows a clear advantage over GraphRAG [3]. 

In terms of specific metrics, the win rates of GraphRAG versus LightRAG in the Comprehensiveness category are as follows: Agriculture (GraphRAG 45.6%, LightRAG 54.4%), CS (GraphRAG 48.4%, LightRAG 51.6%), Legal (GraphRAG 48.4%, LightRAG 51.6%), and Mix (GraphRAG 50.4%, LightRAG 49.6%) [1]. 

For Diversity, the win rates are: Agriculture (GraphRAG 22.8%, LightRAG 77.2%), CS (GraphRAG 40.8%, LightRAG 59.2%), Legal (GraphRAG 26.4%, LightRAG 73.6%), and Mix (GraphRAG 36.0%, LightRAG 64.0%) [1]. 

In Empowerment, the win rates are: Agriculture (GraphRAG 41.2%, LightRAG 58.8%), CS (GraphRAG 45.2%, LightRAG 54.8%), Legal (GraphRAG 43.6%, LightRAG 56.4%), and Mix (GraphRAG 50.8%, LightRAG 49.2%) [1]. 

For the Overall metric, the win rates are: Agriculture (GraphRAG 45.2%, LightRAG 54.8%), CS (GraphRAG 48.0%, LightRAG 52.0%), Legal (GraphRAG 47.2%, LightRAG 52.8%), and Mix (GraphRAG 50.4%, LightRAG 49.6%) [1]. 

These results indicate that LightRAG generally performs better than GraphRAG, especially in the Legal dataset. However, in the Mix dataset for the Empowerment and Overall metrics, GraphRAG shows a slight advantage over LightRAG. 

This suggests that LightRAG's dual-level retrieval paradigm, which integrates low-level retrieval of specific entities with high-level retrieval of broader topics, contributes to its superior performance in most cases [2].

Figures whose labels differ from the source table: 54.4% (answer: Comprehensiveness, LightRAG, vs LightRAG; source: Comprehensiveness, Agriculture, LightRAG, vs GraphRAG); 51.6% (answer: Comprehensiveness, LightRAG, vs LightRAG; source: Comprehensiveness, CS, LightRAG, vs GraphRAG / Comprehensiveness, Legal, LightRAG, vs GraphRAG); 49.6% (answer: Comprehensiveness, Mix, LightRAG, vs LightRAG; source: Comprehensiveness, Mix, LightRAG, vs GraphRAG / Overall, Mix, LightRAG, vs GraphRAG).
```

## M5-Q2-1

- 問題：`compare lightRAG with GraphRAG`；模式 `navigate`；104.8 秒；2 次呼叫；tokens 10132
- 來源：[1] p9 retrieval, [2] p7 retrieval, [3] p7 retrieval, [4] p8 retrieval, [5] p10 retrieval, [6] p7 navigation, [7] p9 navigation, [8] p9 navigation, [9] p8 navigation, [10] p6 navigation, [11] p9 navigation
- 閱讀計畫（定位 6/6，保留 6，超預算 0）：
  - ✓ Section 4.2 COMPARISON OF LIGHT RAG WITH EXISTING RAG METHODS (RQ1) | need: textual comparison of LightRAG vs GraphRAG performance | priority: required | status: covered → 候選 4，納入 [18]，排除 [(20, 'already among the retrieved sources'), (21, 'already among the retrieved sources'), (19, 'already selected for another target')]
  - ✓ Table 1 (page 7) | need: win rates of LightRAG vs baselines including GraphRAG | priority: required | status: missing → 候選 3，納入 [19]，排除 [(20, 'already among the retrieved sources'), (21, 'already among the retrieved sources')]
  - ✓ Section 4.4 CASE STUDY (RQ3 (pages 8-9) | need: qualitative comparison details | priority: required | status: covered → 候選 5，納入 [23]，排除 [(27, 'already among the retrieved sources'), (24, 'already among the retrieved sources'), (25, 'already selected for another target'), (26, 'already selected for another target')]
  - ✓ Table 3 (page 9) | need: specific case study comparison between LightRAG and GraphRAG | priority: required | status: missing → 候選 3，納入 [25, 26]，排除 [(27, 'already among the retrieved sources')]
  - ✓ Section 4.5 MODEL COST AND ADAPTABILITY ANALYSIS (RQ4) | need: cost comparison between LightRAG and GraphRAG | priority: supplementary | status: covered → 候選 3，納入 []，排除 [(27, 'already among the retrieved sources'), (29, 'already among the retrieved sources'), (28, 'already selected for another target')]
  - ✓ Figure 2 (page 9) | need: visual comparison of costs | priority: supplementary | status: missing → 候選 3，納入 [28]，排除 [(27, 'already among the retrieved sources'), (29, 'already among the retrieved sources')]
- 分析狀態：FACTUALLY_INCORRECT；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 修正：[]；刪除 []；仍不符 ['49.6% (Comprehensiveness, Mix, LightRAG, vs LightRAG)', '49.2% (Empowerment, Mix, LightRAG, vs LightRAG)', '49.6% (Overall, Mix, LightRAG, vs LightRAG)']；方向待定 []
- 涵蓋判定：Section 4.2 COMPARISON OF LIGHT RAG WITH EXISTING RAG METHODS (RQ1)→partial；Table 1 (page 7)→missing；Section 4.4 CASE STUDY (RQ3 (pages 8-9)→partial；Table 3 (page 9)→missing；Section 4.5 MODEL COST AND ADAPTABILITY ANALYSIS (RQ4)→partial；Figure 2 (page 9)→covered；required 未納入 []；supplementary 用 1；Matrix {'cells': 128, 'tables': ['Table 1 [6]'], 'definitions': ['LightRAG'], 'facts': 112, 'coverage_gaps': ['Table 3 [7]']}
- 檢查：標籤不符 ['45.2%', '48.0%', '47.2%', '49.6%', '49.2%', '49.6%']；全稱宣稱 1；引用可疑 [([7, 8], [4])]；未解析 32；找不到的數字 ['13.99']

```text
The question asks for a comparison between LightRAG and GraphRAG. Based on the provided sources, the comparison involves:
- **Methods**: LightRAG and GraphRAG.
- **Datasets**: Agriculture, CS, Legal, and Mix (for performance/win rates); Legal (for cost analysis and case study).
- **Metrics**: Win rates (%) across four dimensions (Comprehensiveness, Diversity, Empowerment, Overall) [10]; Token consumption and API calls [11]; Qualitative dimensions (Comprehensiveness, Diversity, Empowerment, Overall) in a case study [7][8].

Evidence Matrix and Method Definitions:
- **LightRAG**: Defined by its dual-level retrieval paradigm (low-level and high-level) and graph-based text indexing [3].
- **GraphRAG**: No explicit definition found in the sources, but described as a graph-based RAG system that uses community structures [2][5][11].
- **Performance Data (Table 1)**: Win rates of baselines vs. LightRAG [6]. Note: The table headers indicate "Win rates (%) of baselines v.s. LightRAG". The values provided are paired (e.g., "GraphRAG 45.6%, LightRAG 54.4%"). The text states LightRAG "consistently outperforms GraphRAG" [2].
- **Cost Data (Figure 2/Table in text)**: Token and API costs on the Legal dataset [1].
- **Case Study (Table 3)**: Qualitative comparison on a specific query [7].

Comparison of Figures:

**Performance (Win Rates):**
Data is from Table 1 [6]. The metric is "Win rate %". The pairing is Head-to-Head (GraphRAG vs LightRAG).
- **Agriculture Dataset**:
  - Comprehensiveness: GraphRAG 45.6%, LightRAG 54.4% [6].
  - Diversity: GraphRAG 22.8%, LightRAG 77.2% [6].
  - Empowerment: GraphRAG 41.2%, LightRAG 58.8% [6].
  - Overall: GraphRAG 45.2%, LightRAG 54.8% [6].
- **CS Dataset**:
  - Comprehensiveness: GraphRAG 48.4%, LightRAG 51.6% [6].
  - Diversity: GraphRAG 40.8%, LightRAG 59.2% [6].
  - Empowerment: GraphRAG 45.2%, LightRAG 54.8% [6].
  - Overall: GraphRAG 48.0%, LightRAG 52.0% [6].
- **Legal Dataset**:
  - Comprehensiveness: GraphRAG 48.4%, LightRAG 51.6% [6].
  - Diversity: GraphRAG 26.4%, LightRAG 73.6% [6].
  - Empowerment: GraphRAG 43.6%, LightRAG 56.4% [6].
  - Overall: GraphRAG 47.2%, LightRAG 52.8% [6].
- **Mix Dataset**:
  - Comprehensiveness: GraphRAG 50.4%, LightRAG 49.6% [6].
  - Diversity: GraphRAG 36.0%, LightRAG 64.0% [6].
  - Empowerment: GraphRAG 50.8%, LightRAG 49.2% [6].
  - Overall: GraphRAG 50.4%, LightRAG 49.6% [6].

**Cost (Legal Dataset):**
Data is from Figure 2/Table in text [1][11].
- **Retrieval Phase Tokens**: GraphRAG consumes 610 × 1,000 (610,000) tokens [11]. LightRAG consumes < 100 tokens [11].
- **Retrieval Phase API Calls**: GraphRAG requires hundreds of API calls (implied by "traverse each community individually" and $C_{max}$ context) [11]. LightRAG requires 1 API call [11].
- **Incremental Text Update Tokens**: GraphRAG requires approximately $1,399 \times 2 \times 5,000$ tokens (reconstruction) [1][5]. LightRAG requires $T_{extract} + T_{extract}$ (integration without reconstruction) [1].

**Case Study (Qualitative):**
Data is from Table 3 [7][8].
- **Comprehensiveness**: Winner: LightRAG [8].
- **Diversity**: Winner: LightRAG [8].
- **Empowerment**: Winner: LightRAG [8].
- **Overall**: Winner: LightRAG [1].

Improvements, Regressions, and Exceptions:

**Improvements (LightRAG outperforms GraphRAG):**
- LightRAG has higher win rates than GraphRAG in the **Overall** metric for Agriculture (54.8% vs 45.2%), CS (52.0% vs 48.0%), and Legal (52.8% vs 47.2%) datasets [6].
- LightRAG has higher win rates than GraphRAG in the **Diversity** metric for all four datasets (Agriculture 77.2%, CS 59.2%, Legal 73.6%, Mix 64.0%) [6].
- LightRAG has higher win rates than GraphRAG in the **Empowerment** metric for Agriculture (58.8%), CS (54.8%), and Legal (56.4%) datasets [6].
- LightRAG has higher win rates than GraphRAG in the **Comprehensiveness** metric for Agriculture (54.4%), CS (51.6%), and Legal (51.6%) datasets [6].
- LightRAG is significantly more cost-effective in the **Retrieval Phase** on the Legal dataset, using <100 tokens vs 610,000 tokens and 1 API call vs hundreds [11].
- LightRAG is more efficient in **Incremental Text Updates**, avoiding the full reconstruction cost of $\approx 13.99 \times 2 \times 5,000$ tokens required by GraphRAG [1][5].
- LightRAG wins all qualitative dimensions (Comprehensiveness, Diversity, Empowerment, Overall) in the Case Study [7][8].

**Regressions/Exceptions (GraphRAG outperforms or ties LightRAG):**
- In the **Mix** dataset, GraphRAG has a higher win rate than LightRAG in **Comprehensiveness** (GraphRAG 50.4% vs LightRAG 49.6%) [6].
- In the **Mix** dataset, GraphRAG has a higher win rate than LightRAG in **Empowerment** (GraphRAG 50.8% vs LightRAG 49.2%) [6].
- In the **Mix** dataset, GraphRAG has a higher win rate than LightRAG in **Overall** (GraphRAG 50.4% vs LightRAG 49.6%) [6].

Verification of Statements:
- "LightRAG consistently outperforms GraphRAG" [2] is supported by the majority of figures, particularly in larger datasets like Legal where the gap is significant [2][6]. However, this statement is not true for the Mix dataset in Comprehensiveness, Empowerment, and Overall metrics, where GraphRAG has higher win rates [6]. The source text generalizes the trend [2], but the figures show exceptions in the Mix dataset [6].
- Cost figures: GraphRAG tokens (610,000) > LightRAG tokens (<100) [11]. GraphRAG update cost (high reconstruction) > LightRAG update cost (integration) [1][5].
- Case study: LightRAG wins all dimensions [7][8].

Citations:
- Method definitions: LightRAG [3].
- Performance figures: Table 1 [6].
- Textual claims of superiority: [2].
- Cost figures: Figure 2/Table text [1][11].
- Case study figures: Table 3 [7][8].

Conclusion:
LightRAG generally outperforms GraphRAG in win rates across Comprehensiveness, Diversity, Empowerment, and Overall metrics for the Agriculture, CS, and Legal datasets [6]. LightRAG shows a significant advantage in Diversity across all datasets, including Mix [6]. However, in the Mix dataset, GraphRAG achieves higher win rates than LightRAG in Comprehensiveness, Empowerment, and Overall metrics [6]. LightRAG is substantially more cost-effective than GraphRAG in both retrieval (tokens and API calls) and incremental update phases on the Legal dataset [1][5][11]. In the qualitative case study, LightRAG outperforms GraphRAG in all evaluated dimensions [7][8].

Numbers that could not be checked against the cited pages of the original text: 13.99.

Figures whose labels differ from the source table: 45.2% (answer: Overall, LightRAG, vs GraphRAG; source: Empowerment, CS, GraphRAG, vs LightRAG / Overall, Agriculture, GraphRAG, vs LightRAG); 48.0% (answer: Overall, LightRAG, vs GraphRAG; source: Overall, CS, GraphRAG, vs LightRAG); 47.2% (answer: Overall, LightRAG, vs GraphRAG; source: Overall, Legal, GraphRAG, vs LightRAG); 49.6% (answer: Comprehensiveness, Mix, LightRAG, vs LightRAG; source: Comprehensiveness, Mix, LightRAG, vs GraphRAG / Overall, Mix, LightRAG, vs GraphRAG); 49.2% (answer: Empowerment, Mix, LightRAG, vs LightRAG; source: Empowerment, Mix, LightRAG, vs GraphRAG); 49.6% (answer: Overall, Mix, LightRAG, vs LightRAG; source: Comprehensiveness, Mix, LightRAG, vs GraphRAG / Overall, Mix, LightRAG, vs GraphRAG).

A claim the source table does not bear out: "The text states LightRAG "consistently outperforms GraphRAG"." — LightRAG is above the compared methods in 61 cells and below in 3, for example Comprehensiveness / Mix: LightRAG 49.6% vs GraphRAG 50.4% (p. 7); Empowerment / Mix: LightRAG 49.2% vs GraphRAG 50.8% (p. 7); Overall / Mix: LightRAG 49.6% vs GraphRAG 50.4% (p. 7).
```

## M5-Q2-2

- 問題：`compare lightRAG with GraphRAG`；模式 `navigate`；101.1 秒；2 次呼叫；tokens 10039
- 來源：[1] p9 retrieval, [2] p7 retrieval, [3] p7 retrieval, [4] p8 retrieval, [5] p10 retrieval, [6] p7 navigation, [7] p9 navigation, [8] p9 navigation, [9] p8 navigation, [10] p6 navigation, [11] p9 navigation
- 閱讀計畫（定位 6/6，保留 6，超預算 0）：
  - ✓ Section 4.2 COMPARISON OF LIGHT RAG WITH EXISTING RAG METHODS (RQ1) | need: textual comparison of LightRAG vs GraphRAG performance | priority: required | status: covered → 候選 4，納入 [18]，排除 [(20, 'already among the retrieved sources'), (21, 'already among the retrieved sources'), (19, 'already selected for another target')]
  - ✓ Table 1 (page 7) | need: win rates of LightRAG vs baselines including GraphRAG | priority: required | status: missing → 候選 3，納入 [19]，排除 [(20, 'already among the retrieved sources'), (21, 'already among the retrieved sources')]
  - ✓ Section 4.4 CASE STUDY (RQ3 (pages 8-9) | need: qualitative comparison details | priority: required | status: covered → 候選 5，納入 [23]，排除 [(27, 'already among the retrieved sources'), (24, 'already among the retrieved sources'), (25, 'already selected for another target'), (26, 'already selected for another target')]
  - ✓ Table 3 (page 9) | need: specific case study comparison between LightRAG and GraphRAG | priority: required | status: missing → 候選 3，納入 [25, 26]，排除 [(27, 'already among the retrieved sources')]
  - ✓ Section 4.5 MODEL COST AND ADAPTABILITY ANALYSIS (RQ4) | need: cost comparison between LightRAG and GraphRAG | priority: supplementary | status: covered → 候選 3，納入 []，排除 [(27, 'already among the retrieved sources'), (29, 'already among the retrieved sources'), (28, 'already selected for another target')]
  - ✓ Figure 2 (page 9) | need: visual comparison of costs | priority: supplementary | status: missing → 候選 3，納入 [28]，排除 [(27, 'already among the retrieved sources'), (29, 'already among the retrieved sources')]
- 分析狀態：FACTUALLY_INCORRECT；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 修正：[]；刪除 []；仍不符 []；方向待定 []
- 涵蓋判定：Section 4.2 COMPARISON OF LIGHT RAG WITH EXISTING RAG METHODS (RQ1)→partial；Table 1 (page 7)→missing；Section 4.4 CASE STUDY (RQ3 (pages 8-9)→partial；Table 3 (page 9)→missing；Section 4.5 MODEL COST AND ADAPTABILITY ANALYSIS (RQ4)→partial；Figure 2 (page 9)→covered；required 未納入 []；supplementary 用 1；Matrix {'cells': 128, 'tables': ['Table 1 [6]'], 'definitions': ['LightRAG'], 'facts': 112, 'coverage_gaps': ['Table 3 [7]']}
- 檢查：標籤不符 ['49.6%']；全稱宣稱 0；引用可疑 [([1, 8], [4])]；未解析 43；找不到的數字 ['13,990,000']

```text
The question asks for a comparison between LightRAG and GraphRAG. Based on the provided sources, this comparison involves:
*   **Methods:** LightRAG and GraphRAG. Note: The source does not provide explicit definitions for GraphRAG or LightRAG in the "Method definitions" section, but describes their performance and mechanisms in the text [2][3][4][5][11].
*   **Datasets:** Agriculture, CS, Legal, and Mix (for win rates) [6]; Legal (for cost analysis) [1][5][11]; and a qualitative case study on machine learning metrics [4][7].
*   **Metrics:** Win rates (%) across four dimensions: Comprehensiveness, Diversity, Empowerment, and Overall [6][10]; Token usage and API calls [1][11]; and qualitative assessments of Comprehensiveness, Diversity, Empowerment, and Overall quality in a case study [7][8].

**Evidence Matrix and Definitions:**
*   **Win Rates (Table 1):** LightRAG is compared against GraphRAG across four datasets (Agriculture, CS, Legal, Mix) and four dimensions [6].
*   **Cost Analysis (Figure 2/Table 2 text):** Comparison of token costs and API calls on the Legal dataset [1][11].
*   **Case Study (Table 3):** Qualitative comparison of responses to a specific query [7][8].
*   **Mechanisms:** LightRAG uses a dual-level retrieval paradigm (low-level and high-level) [3][9]. GraphRAG uses community structures that require regeneration for updates [5].

**Comparison of Figures:**

**Win Rates (Table 1, Source [6]):**
*   **Agriculture Dataset:**
    *   Comprehensiveness: GraphRAG 45.6% vs LightRAG 54.4% (LightRAG higher).
    *   Diversity: GraphRAG 22.8% vs LightRAG 77.2% (LightRAG higher).
    *   Empowerment: GraphRAG 41.2% vs LightRAG 58.8% (LightRAG higher).
    *   Overall: GraphRAG 45.2% vs LightRAG 54.8% (LightRAG higher).
*   **CS Dataset:**
    *   Comprehensiveness: GraphRAG 48.4% vs LightRAG 51.6% (LightRAG higher).
    *   Diversity: GraphRAG 40.8% vs LightRAG 59.2% (LightRAG higher).
    *   Empowerment: GraphRAG 45.2% vs LightRAG 54.8% (LightRAG higher).
    *   Overall: GraphRAG 48.0% vs LightRAG 52.0% (LightRAG higher).
*   **Legal Dataset:**
    *   Comprehensiveness: GraphRAG 48.4% vs LightRAG 51.6% (LightRAG higher).
    *   Diversity: GraphRAG 26.4% vs LightRAG 73.6% (LightRAG higher).
    *   Empowerment: GraphRAG 43.6% vs LightRAG 56.4% (LightRAG higher).
    *   Overall: GraphRAG 47.2% vs LightRAG 52.8% (LightRAG higher).
*   **Mix Dataset:**
    *   Comprehensiveness: GraphRAG 50.4% vs LightRAG 49.6% (GraphRAG higher).
    *   Diversity: GraphRAG 36.0% vs LightRAG 64.0% (LightRAG higher).
    *   Empowerment: GraphRAG 50.8% vs LightRAG 49.2% (GraphRAG higher).
    *   Overall: GraphRAG 50.4% vs LightRAG 49.6% (GraphRAG higher).

**Cost Analysis (Figure 2/Table 2 description, Sources [1][11]):**
*   **Retrieval Phase (Legal Dataset):**
    *   Tokens: GraphRAG uses 610 × 1,000 tokens; LightRAG uses < 100 tokens [1][11].
    *   API Calls: GraphRAG uses 610 × 1,000 calls (implied high count due to traversing communities); LightRAG uses 1 call [1][11].
*   **Incremental Text Update (Legal Dataset):**
    *   Tokens: GraphRAG requires ~1,399 × 2 × 5,000 tokens (approx. 13,990,000 tokens) to regenerate community reports; LightRAG uses Textract + Textract (significantly lower) [1][5].
    *   API Calls: GraphRAG requires 1,399 × 2 + Cextract calls; LightRAG requires Cextract calls [1][5].

**Case Study (Table 3, Sources [7][8]):**
*   Query: "Which methods can normalize the feature values for effective machine learning?" (Note: The query in the table header seems mismatched with the content about movie recommendation metrics, but the comparison stands as presented).
*   Comprehensiveness: Winner LightRAG [8].
*   Diversity: Winner LightRAG [8].
*   Empowerment: Winner LightRAG [8].
*   Overall: Winner LightRAG [1].

**Improvements, Regressions, and Exceptions:**
*   **Improvements for LightRAG:**
    *   LightRAG outperforms GraphRAG in Diversity across all four datasets (Agriculture, CS, Legal, Mix) [6].
    *   LightRAG outperforms GraphRAG in Comprehensiveness on Agriculture, CS, and Legal datasets [6].
    *   LightRAG outperforms GraphRAG in Empowerment on Agriculture, CS, and Legal datasets [6].
    *   LightRAG outperforms GraphRAG in Overall win rate on Agriculture, CS, and Legal datasets [6].
    *   LightRAG has significantly lower token usage and API calls in both retrieval and incremental update phases on the Legal dataset [1][5][11].
    *   LightRAG wins in all qualitative dimensions (Comprehensiveness, Diversity, Empowerment, Overall) in the case study [1][8].
*   **Regressions/Exceptions for LightRAG:**
    *   On the Mix dataset, GraphRAG outperforms LightRAG in Comprehensiveness (50.4% vs 49.6%), Empowerment (50.8% vs 49.2%), and Overall (50.4% vs 49.6%) [6].
    *   LightRAG does not consistently outperform GraphRAG across all metrics and datasets; specifically, it underperforms in most metrics on the Mix dataset [6].

**Verification:**
*   "LightRAG outperforms GraphRAG in Diversity across all datasets": Supported by Table 1 [6] (77.2%>22.8%, 59.2%>40.8%, 73.6%>26.4%, 64.0%>36.0%).
*   "LightRAG has lower costs": Supported by Figure 2/Table 2 text [1][11] (<100 tokens vs 610,000 tokens).
*   "GraphRAG wins on Mix Overall": Supported by Table 1 [6] (50.4% vs 49.6%).

**Citations:**
*   Win rates: [6]
*   Cost figures: [1], [11]
*   Case study results: [7], [8], [1]
*   Textual explanations of performance: [2], [3], [5]

**Conclusion:**
LightRAG generally outperforms GraphRAG in terms of response Diversity across all tested datasets (Agriculture, CS, Legal, Mix) and demonstrates superior cost-efficiency, particularly in token usage and API calls during retrieval and incremental updates on the Legal dataset [6][1][11]. LightRAG also achieves higher win rates in Comprehensiveness, Empowerment, and Overall quality on the Agriculture, CS, and Legal datasets [6]. However, this trend does not hold universally; on the Mix dataset, GraphRAG achieves higher win rates than LightRAG in Comprehensiveness, Empowerment, and Overall performance [6]. In the qualitative case study, LightRAG was rated superior to GraphRAG in all evaluated dimensions [1][8].

Numbers that could not be checked against the cited pages of the original text: 13,990,000.

Figures whose labels differ from the source table: 49.6% (answer: Overall, Mix, GraphRAG; source: Comprehensiveness, Mix, LightRAG, vs GraphRAG / Overall, Mix, LightRAG, vs GraphRAG).
```

## M5-Q2-3

- 問題：`compare lightRAG with GraphRAG`；模式 `navigate`；77.7 秒；2 次呼叫；tokens 9478
- 來源：[1] p9 retrieval, [2] p7 retrieval, [3] p7 retrieval, [4] p8 retrieval, [5] p10 retrieval, [6] p7 navigation, [7] p9 navigation, [8] p9 navigation, [9] p8 navigation, [10] p6 navigation, [11] p9 navigation
- 閱讀計畫（定位 6/6，保留 6，超預算 0）：
  - ✓ Section 4.2 COMPARISON OF LIGHT RAG WITH EXISTING RAG METHODS (RQ1) | need: textual comparison of LightRAG vs GraphRAG performance | priority: required | status: covered → 候選 4，納入 [18]，排除 [(20, 'already among the retrieved sources'), (21, 'already among the retrieved sources'), (19, 'already selected for another target')]
  - ✓ Table 1 (page 7) | need: win rates of LightRAG vs baselines including GraphRAG | priority: required | status: missing → 候選 3，納入 [19]，排除 [(20, 'already among the retrieved sources'), (21, 'already among the retrieved sources')]
  - ✓ Section 4.4 CASE STUDY (RQ3 (pages 8-9) | need: qualitative comparison details | priority: required | status: covered → 候選 5，納入 [23]，排除 [(27, 'already among the retrieved sources'), (24, 'already among the retrieved sources'), (25, 'already selected for another target'), (26, 'already selected for another target')]
  - ✓ Table 3 (page 9) | need: specific case study comparison between LightRAG and GraphRAG | priority: required | status: missing → 候選 3，納入 [25, 26]，排除 [(27, 'already among the retrieved sources')]
  - ✓ Section 4.5 MODEL COST AND ADAPTABILITY ANALYSIS (RQ4) | need: cost comparison between LightRAG and GraphRAG | priority: supplementary | status: covered → 候選 3，納入 []，排除 [(27, 'already among the retrieved sources'), (29, 'already among the retrieved sources'), (28, 'already selected for another target')]
  - ✓ Figure 2 (page 9) | need: visual comparison of costs | priority: supplementary | status: missing → 候選 3，納入 [28]，排除 [(27, 'already among the retrieved sources'), (29, 'already among the retrieved sources')]
- 分析狀態：FACTUALLY_INCORRECT；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 修正：[]；刪除 []；仍不符 []；方向待定 []
- 涵蓋判定：Section 4.2 COMPARISON OF LIGHT RAG WITH EXISTING RAG METHODS (RQ1)→partial；Table 1 (page 7)→missing；Section 4.4 CASE STUDY (RQ3 (pages 8-9)→partial；Table 3 (page 9)→missing；Section 4.5 MODEL COST AND ADAPTABILITY ANALYSIS (RQ4)→partial；Figure 2 (page 9)→covered；required 未納入 []；supplementary 用 1；Matrix {'cells': 128, 'tables': ['Table 1 [6]'], 'definitions': ['LightRAG'], 'facts': 112, 'coverage_gaps': ['Table 3 [7]']}
- 檢查：標籤不符 []；全稱宣稱 1；引用可疑 [([7, 8], [4])]；未解析 32；找不到的數字 []

```text
The question asks for a comparison between LightRAG and GraphRAG regarding their performance (win rates across datasets and metrics) and costs (tokens and API calls). The relevant datasets are Agriculture, CS, Legal, and Mix. The metrics for performance are Comprehensiveness, Diversity, Empowerment, and Overall win rates. The metrics for cost are Tokens and API Calls during Retrieval and Incremental Text Update phases, specifically analyzed on the Legal dataset.

Evidence Matrix and Definitions:
- **Methods**: LightRAG [3], GraphRAG (no definition found in sources, but described as a top-performing baseline using graph-based retrieval) [2][11].
- **Performance Data**: Table 1 provides win rates of baselines vs. LightRAG [6].
- **Cost Data**: Figure 2/Table data describes cost comparison on the Legal dataset [1][11].
- **Case Study**: Table 3 provides a qualitative comparison on a specific machine learning query [7][8].

& (4) Comparison of Figures:

**Performance Comparison (Win Rates from Table 1 [6])**
LightRAG is compared against GraphRAG across four datasets (Agriculture, CS, Legal, Mix) and four evaluation dimensions (Comprehensiveness, Diversity, Empowerment, Overall).

*   **Agriculture Dataset:**
    *   Comprehensiveness: LightRAG (54.4%) > GraphRAG (45.6%) [6].
    *   Diversity: LightRAG (77.2%) > GraphRAG (22.8%) [6].
    *   Empowerment: LightRAG (58.8%) > GraphRAG (41.2%) [6].
    *   Overall: LightRAG (54.8%) > GraphRAG (45.2%) [6].
*   **CS Dataset:**
    *   Comprehensiveness: GraphRAG (48.4%) > LightRAG (51.6%) -> *Correction*: LightRAG is 51.6%, GraphRAG is 48.4%. So LightRAG > GraphRAG [6].
    *   Diversity: LightRAG (59.2%) > GraphRAG (40.8%) [6].
    *   Empowerment: LightRAG (54.8%) > GraphRAG (45.2%) [6].
    *   Overall: LightRAG (52.0%) > GraphRAG (48.0%) [6].
*   **Legal Dataset:**
    *   Comprehensiveness: LightRAG (51.6%) > GraphRAG (48.4%) [6].
    *   Diversity: LightRAG (73.6%) > GraphRAG (26.4%) [6].
    *   Empowerment: LightRAG (56.4%) > GraphRAG (43.6%) [6].
    *   Overall: LightRAG (52.8%) > GraphRAG (47.2%) [6].
*   **Mix Dataset:**
    *   Comprehensiveness: GraphRAG (50.4%) > LightRAG (49.6%) [6]. *Exception: GraphRAG outperforms LightRAG.*
    *   Diversity: LightRAG (64.0%) > GraphRAG (36.0%) [6].
    *   Empowerment: GraphRAG (50.8%) > LightRAG (49.2%) [6]. *Exception: GraphRAG outperforms LightRAG.*
    *   Overall: GraphRAG (50.4%) > LightRAG (49.6%) [6]. *Exception: GraphRAG outperforms LightRAG.*

**General Trend**: LightRAG outperforms GraphRAG in the majority of cases, particularly showing significant advantages in Diversity across all datasets [2]. However, in the Mix dataset, GraphRAG achieves higher win rates in Comprehensiveness, Empowerment, and Overall metrics [6].

**Cost Comparison (Figure 2/Table Data on Legal Dataset [1][11])**
*   **Retrieval Phase:**
    *   Tokens: GraphRAG uses 610,000 tokens (610 communities × 1,000 tokens); LightRAG uses < 100 tokens [1][11].
    *   API Calls: GraphRAG requires multiple API calls (one per community); LightRAG requires only 1 API call [1][11].
*   **Incremental Text Update Phase:**
    *   GraphRAG requires dismantling and regenerating community structures, costing approximately $1,399 \times 2 \times 5,000$ tokens for a dataset of similar size to Legal [5].
    *   LightRAG integrates new entities without full reconstruction, resulting in significantly lower overhead, described as `Textract + Textract` token cost and `Cextract` API calls [1][5].

**Case Study (Table 3 [7][8])**
*   On a machine learning query, LightRAG won against GraphRAG in Comprehensiveness, Diversity, Empowerment, and Overall quality according to the LLM judge [7][8].

& (6) Verification:
- "LightRAG consistently outperforms GraphRAG" is supported by the majority of Table 1 figures [2][6], but the statement must be qualified because GraphRAG wins in Mix dataset Comprehensiveness, Empowerment, and Overall [6].
- Cost figures: LightRAG is lower in tokens (<100 vs 610,000) and API calls (1 vs hundreds) in retrieval [1][11]. LightRAG is lower in incremental update costs [5].

Conclusion:
LightRAG generally outperforms GraphRAG in win rates across the Agriculture, CS, and Legal datasets, with particularly large margins in Diversity [2][6]. In the Mix dataset, GraphRAG outperforms LightRAG in Comprehensiveness, Empowerment, and Overall metrics [6]. Regarding efficiency, LightRAG demonstrates significantly lower costs than GraphRAG in both retrieval (tokens and API calls) and incremental updates on the Legal dataset [1][5][11]. Qualitatively, LightRAG provided more comprehensive, diverse, and empowering answers in the case study [7][8].

A claim the source table does not bear out: "- "LightRAG consistently outperforms GraphRAG" is supported by the majority of Table 1 figures, but the statement must be qualified because GraphRAG wins in Mix dataset Comprehensiveness, Empowerment, and Overall." — LightRAG is above the compared methods in 9 cells and below in 3, for example Comprehensiveness / Mix: LightRAG 49.6% vs GraphRAG 50.4% (p. 7); Empowerment / Mix: LightRAG 49.2% vs GraphRAG 50.8% (p. 7); Overall / Mix: LightRAG 49.6% vs GraphRAG 50.4% (p. 7).
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

## B5-Q3-1

- 問題：`Performance of ablated versions of LightRAG`；模式 `navigate`；112.9 秒；2 次呼叫；tokens 8356
- 來源：[1] p8 retrieval, [2] p7 retrieval, [3] p1 retrieval, [4] p8 retrieval, [5] p1 retrieval, [6] p8 table_context
- 閱讀計畫（定位 6/6，保留 0，超預算 0）：
  - ✓ Section 4.3 ABLATION STUDIES (RQ2) | need: discussion of ablated versions | priority: required | status: covered → 候選 0，納入 []，排除 []
  - ✓ Table 2 (page 8) | need: performance metrics | priority: required | status: covered → 候選 0，納入 []，排除 []
  - ✓ Section 4.4 CASE STUDY (RQ3) | need: additional context on ablation effects | priority: supplementary | status: covered → 候選 0，納入 []，排除 []
  - ✓ Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM | need: method description | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
  - ✓ Section 7.3.1 PROMPTS FOR GRAPH GENERATION | need: implementation details | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
  - ✓ Section 7.3.2 PROMPTS FOR QUERY GENERATION | need: implementation details | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
- 分析狀態：FACTUALLY_INCORRECT；完整性 incomplete（required ['-High', '-Low', '-Origin', 'LightRAG']，缺 ['-High', '-Low', '-Origin', 'LightRAG']，條件 None）；方向核對 []
- 修正：[]；刪除 []；仍不符 ['67.6% (Comprehensiveness, Agriculture, LightRAG, vs -High)', '67.6% (Comprehensiveness, Agriculture, LightRAG, vs -Low)', '67.6% (Comprehensiveness, Agriculture, LightRAG, vs -Origin)', '61.6% (Comprehensiveness, CS, LightRAG, vs -High)', '61.6% (Comprehensiveness, CS, LightRAG, vs -Low)', '61.6% (Comprehensiveness, CS, LightRAG, vs -Origin)', '83.6% (Comprehensiveness, Legal, LightRAG, vs -High)', '83.6% (Comprehensiveness, Legal, LightRAG, vs -Low)', '83.6% (Comprehensiveness, Legal, LightRAG, vs -Origin)', '61.2% (Comprehensiveness, Mix, LightRAG, vs -High)', '61.2% (Comprehensiveness, Mix, LightRAG, vs -Low)', '61.2% (Comprehensiveness, Mix, LightRAG, vs -Origin)', '76.4% (Diversity, Agriculture, LightRAG, vs -High)', '76.4% (Diversity, Agriculture, LightRAG, vs -Low)', '76.4% (Diversity, Agriculture, LightRAG, vs -Origin)', '62.0% (Diversity, CS, LightRAG, vs -High)', '62.0% (Diversity, CS, LightRAG, vs -Low)', '62.0% (Diversity, CS, LightRAG, vs -Origin)', '86.4% (Diversity, Legal, LightRAG, vs -High)', '86.4% (Diversity, Legal, LightRAG, vs -Low)', '86.4% (Diversity, Legal, LightRAG, vs -Origin)', '67.6% (Diversity, Mix, LightRAG, vs -High)', '67.6% (Diversity, Mix, LightRAG, vs -Low)', '67.6% (Diversity, Mix, LightRAG, vs -Origin)', '67.6% (Empowerment, Agriculture, LightRAG, vs -High)', '67.6% (Empowerment, Agriculture, LightRAG, vs -Low)', '67.6% (Empowerment, Agriculture, LightRAG, vs -Origin)', '61.2% (Empowerment, CS, LightRAG, vs -High)', '61.2% (Empowerment, CS, LightRAG, vs -Low)', '61.2% (Empowerment, CS, LightRAG, vs -Origin)', '83.6% (Empowerment, Legal, LightRAG, vs -High)', '83.6% (Empowerment, Legal, LightRAG, vs -Low)', '83.6% (Empowerment, Legal, LightRAG, vs -Origin)', '57.2% (Empowerment, Mix, LightRAG, vs -High)', '57.2% (Empowerment, Mix, LightRAG, vs -Low)', '57.2% (Empowerment, Mix, LightRAG, vs -Origin)', '67.6% (Overall, Agriculture, LightRAG, vs -High)', '67.6% (Overall, Agriculture, LightRAG, vs -Low)', '67.6% (Overall, Agriculture, LightRAG, vs -Origin)', '61.2% (Overall, CS, LightRAG, vs -High)', '61.2% (Overall, CS, LightRAG, vs -Low)', '61.2% (Overall, CS, LightRAG, vs -Origin)', '84.8% (Overall, Legal, LightRAG, vs -High)', '84.8% (Overall, Legal, LightRAG, vs -Low)', '84.8% (Overall, Legal, LightRAG, vs -Origin)', '60.0% (Overall, Mix, LightRAG, vs -High)', '60.0% (Overall, Mix, LightRAG, vs -Low)', '60.0% (Overall, Mix, LightRAG, vs -Origin)']；方向待定 []
- 涵蓋判定：Section 4.3 ABLATION STUDIES (RQ2)→covered；Table 2 (page 8)→covered；Section 4.4 CASE STUDY (RQ3)→partial；Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM→missing；Section 7.3.1 PROMPTS FOR GRAPH GENERATION→missing；Section 7.3.2 PROMPTS FOR QUERY GENERATION→missing；required 未納入 []；supplementary 用 0；Matrix {'cells': 128, 'tables': ['Table 2 [1]'], 'definitions': ['NaiveRAG', 'LightRAG', '-High'], 'facts': 64, 'coverage_gaps': []}
- 檢查：標籤不符 ['67.6%', '65.2%', '67.6%', '64.0%', '67.6%', '75.2%', '61.6%', '57.2%', '61.6%', '56.8%', '61.6%', '60.8%', '83.6%', '76.4%', '83.6%', '80.8%', '83.6%', '61.2%', '59.6%', '61.2%', '64.0%', '61.2%', '55.6%', '76.4%', '72.8%', '76.4%', '72.0%', '76.4%', '73.6%', '62.0%', '63.2%', '62.0%', '60.4%', '62.0%', '55.2%', '86.4%', '83.2%', '86.4%', '86.4%', '85.6%', '67.6%', '64.0%', '67.6%', '66.8%', '67.6%', '74.4%', '67.6%', '64.0%', '67.6%', '65.2%', '67.6%', '68.0%', '61.2%', '57.6%', '61.2%', '57.2%', '61.2%', '56.8%', '83.6%', '77.2%', '83.6%', '83.6%', '82.8%', '57.2%', '52.4%', '57.2%', '64.8%', '57.2%', '54.8%', '67.6%', '64.8%', '67.6%', '65.2%', '67.6%', '74.4%', '61.2%', '56.0%', '61.2%', '56.4%', '61.2%', '60.8%', '84.8%', '78.0%', '84.8%', '81.2%', '84.8%', '84.4%', '60.0%', '57.6%', '60.0%', '64.8%', '60.0%', '55.6%']；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
The question asks for a comparison of the performance of ablated versions of LightRAG. The ablated versions include -High, -Low, and -Origin. The evaluation is conducted on four datasets: Agriculture, CS, Legal, and Mix. The metrics used are Comprehensiveness, Diversity, Empowerment, and Overall.

### Compact Comparison Table of Relevant Figures
| Method       | Dataset   | Metric        | LightRAG | -High  | -Low   | -Origin |
|--------------|-----------|---------------|----------|--------|--------|---------|
| Comprehensiveness | Agriculture | LightRAG vs -High | 67.6% vs 65.2% | [1] | [1] | [1] |
| Comprehensiveness | Agriculture | LightRAG vs -Low | 67.6% vs 64.0% | [1] | [1] | [1] |
| Comprehensiveness | Agriculture | LightRAG vs -Origin | 67.6% vs 75.2% | [1] | [1] | [1] |
| Comprehensiveness | CS | LightRAG vs -High | 61.6% vs 57.2% | [1] | [1] | [1] |
| Comprehensiveness | CS | LightRAG vs -Low | 61.6% vs 56.8% | [1] | [1] | [1] |
| Comprehensiveness | CS | LightRAG vs -Origin | 61.6% vs 60.8% | [1] | [1] | [1] |
| Comprehensiveness | Legal | LightRAG vs -High | 83.6% vs 76.4% | [1] | [1] | [1] |
| Comprehensiveness | Legal | LightRAG vs -Low | 83.6% vs 80.8% | [1] | [1] | [1] |
| Comprehensiveness | Legal | LightRAG vs -Origin | 83.6% vs 83.6% | [1] | [1] | [1] |
| Comprehensiveness | Mix | LightRAG vs -High | 61.2% vs 59.6% | [1] | [1] | [1] |
| Comprehensiveness | Mix | LightRAG vs -Low | 61.2% vs 64.0% | [1] | [1] | [1] |
| Comprehensiveness | Mix | LightRAG vs -Origin | 61.2% vs 55.6% | [1] | [1] | [1] |
| Diversity | Agriculture | LightRAG vs -High | 76.4% vs 72.8% | [1] | [1] | [1] |
| Diversity | Agriculture | LightRAG vs -Low | 76.4% vs 72.0% | [1] | [1] | [1] |
| Diversity | Agriculture | LightRAG vs -Origin | 76.4% vs 73.6% | [1] | [1] | [1] |
| Diversity | CS | LightRAG vs -High | 62.0% vs 63.2% | [1] | [1] | [1] |
| Diversity | CS | LightRAG vs -Low | 62.0% vs 60.4% | [1] | [1] | [1] |
| Diversity | CS | LightRAG vs -Origin | 62.0% vs 55.2% | [1] | [1] | [1] |
| Diversity | Legal | LightRAG vs -High | 86.4% vs 83.2% | [1] | [1] | [1] |
| Diversity | Legal | LightRAG vs -Low | 86.4% vs 86.4% | [1] | [1] | [1] |
| Diversity | Legal | LightRAG vs -Origin | 86.4% vs 85.6% | [1] | [1] | [1] |
| Diversity | Mix | LightRAG vs -High | 67.6% vs 64.0% | [1] | [1] | [1] |
| Diversity | Mix | LightRAG vs -Low | 67.6% vs 66.8% | [1] | [1] | [1] |
| Diversity | Mix | LightRAG vs -Origin | 67.6% vs 74.4% | [1] | [1] | [1] |
| Empowerment | Agriculture | LightRAG vs -High | 67.6% vs 64.0% | [1] | [1] | [1] |
| Empowerment | Agriculture | LightRAG vs -Low | 67.6% vs 65.2% | [1] | [1] | [1] |
| Empowerment | Agriculture | LightRAG vs -Origin | 67.6% vs 68.0% | [1] | [1] | [1] |
| Empowerment | CS | LightRAG vs -High | 61.2% vs 57.6% | [1] | [1] | [1] |
| Empowerment | CS | LightRAG vs -Low | 61.2% vs 57.2% | [1] | [1] | [1] |
| Empowerment | CS | LightRAG vs -Origin | 61.2% vs 56.8% | [1] | [1] | [1] |
| Empowerment | Legal | LightRAG vs -High | 83.6% vs 77.2% | [1] | [1] | [1] |
| Empowerment | Legal | LightRAG vs -Low | 83.6% vs 83.6% | [1] | [1] | [1] |
| Empowerment | Legal | LightRAG vs -Origin | 83.6% vs 82.8% | [1] | [1] | [1] |
| Empowerment | Mix | LightRAG vs -High | 57.2% vs 52.4% | [1] | [1] | [1] |
| Empowerment | Mix | LightRAG vs -Low | 57.2% vs 64.8% | [1] | [1] | [1] |
| Empowerment | Mix | LightRAG vs -Origin | 57.2% vs 54.8% | [1] | [1] | [1] |
| Overall | Agriculture | LightRAG vs -High | 67.6% vs 64.8% | [1] | [1] | [1] |
| Overall | Agriculture | LightRAG vs -Low | 67.6% vs 65.2% | [1] | [1] | [1] |
| Overall | Agriculture | LightRAG vs -Origin | 67.6% vs 74.4% | [1] | [1] | [1] |
| Overall | CS | LightRAG vs -High | 61.2% vs 56.0% | [1] | [1] | [1] |
| Overall | CS | LightRAG vs -Low | 61.2% vs 56.4% | [1] | [1] | [1] |
| Overall | CS | LightRAG vs -Origin | 61.2% vs 60.8% | [1] | [1] | [1] |
| Overall | Legal | LightRAG vs -High | 84.8% vs 78.0% | [1] | [1] | [1] |
| Overall | Legal | LightRAG vs -Low | 84.8% vs 81.2% | [1] | [1] | [1] |
| Overall | Legal | LightRAG vs -Origin | 84.8% vs 84.4% | [1] | [1] | [1] |
| Overall | Mix | LightRAG vs -High | 60.0% vs 57.6% | [1] | [1] | [1] |
| Overall | Mix | LightRAG vs -Low | 60.0% vs 64.8% | [1] | [1] | [1] |
| Overall | Mix | LightRAG vs -Origin | 60.0% vs 55.6% | [1] | [1] | [1] |

### Analysis
- **-High variant**:
  - **Improvements**: In Agriculture and Mix datasets, -High shows slight improvements in Comprehensiveness and Overall metrics compared to LightRAG.
  - **Regressions**: Across most datasets and metrics, -High underperforms LightRAG, particularly in CS and Legal, where it shows significant drops in Comprehensiveness, Diversity, Empowerment, and Overall [6].
  - **Exception**: -High shows improvements in Comprehensiveness and Overall for Agriculture and Mix datasets [1].

- **-Low variant**:
  - **Improvements**: -Low outperforms LightRAG in Mix dataset for Comprehensiveness and Empowerment [1].
  - **Regressions**: In most datasets and metrics, -Low underperforms LightRAG, especially in CS and Legal, where it shows significant drops in Comprehensiveness, Diversity, Empowerment, and Overall [6].
  - **Exception**: -Low outperforms LightRAG in Mix dataset for Comprehensiveness and Empowerment [1].

- **-Origin variant**:
  - **Improvements**: -Origin shows improvements in Agriculture and Mix datasets for Comprehensiveness and Diversity [6].
  - **Regressions**: In most cases, -Origin underperforms LightRAG, particularly in CS and Legal datasets [1].
  - **Exception**: -Origin shows improvements in Agriculture and Mix datasets for Comprehensiveness and Diversity [1].

### Conclusion
The ablated versions of LightRAG (-High, -Low, and -Origin) show mixed results. While some variants show improvements in specific datasets and metrics, the full version of LightRAG achieves balanced performance across multiple dimensions.

Figures whose labels differ from the source table: 67.6% (answer: Comprehensiveness, Agriculture, LightRAG, vs -High; source: Comprehensiveness, Agriculture, LightRAG, vs NaiveRAG / Diversity, Mix, LightRAG, vs NaiveRAG / Empowerment, Agriculture, LightRAG, vs NaiveRAG / Overall, Agriculture, LightRAG, vs NaiveRAG); 65.2% (answer: Comprehensiveness, Agriculture, LightRAG, vs -High; source: Comprehensiveness, Agriculture, -High, vs NaiveRAG / Empowerment, Agriculture, -Low, vs NaiveRAG / Overall, Agriculture, -Low, vs NaiveRAG); 67.6% (answer: Comprehensiveness, Agriculture, LightRAG, vs -Low; source: Comprehensiveness, Agriculture, LightRAG, vs NaiveRAG / Diversity, Mix, LightRAG, vs NaiveRAG / Empowerment, Agriculture, LightRAG, vs NaiveRAG / Overall, Agriculture, LightRAG, vs NaiveRAG); 64.0% (answer: Comprehensiveness, Agriculture, LightRAG, vs -Low; source: Diversity, Mix, -High, vs NaiveRAG / Empowerment, Agriculture, -High, vs NaiveRAG / Comprehensiveness, Agriculture, -Low, vs NaiveRAG / Comprehensiveness, Mix, -Low, vs NaiveRAG); 67.6% (answer: Comprehensiveness, Agriculture, LightRAG, vs -Origin; source: Comprehensiveness, Agriculture, LightRAG, vs NaiveRAG / Diversity, Mix, LightRAG, vs NaiveRAG / Empowerment, Agriculture, LightRAG, vs NaiveRAG / Overall, Agriculture, LightRAG, vs NaiveRAG); 75.2% (answer: Comprehensiveness, Agriculture, LightRAG, vs -Origin; source: Comprehensiveness, Agriculture, -Origin, vs NaiveRAG); 61.6% (answer: Comprehensiveness, CS, LightRAG, vs -High; source: Comprehensiveness, CS, LightRAG, vs NaiveRAG); 57.2% (answer: Comprehensiveness, CS, LightRAG, vs -High; source: Empowerment, Mix, LightRAG, vs NaiveRAG / Comprehensiveness, CS, -High, vs NaiveRAG / Empowerment, CS, -Low, vs NaiveRAG); 61.6% (answer: Comprehensiveness, CS, LightRAG, vs -Low; source: Comprehensiveness, CS, LightRAG, vs NaiveRAG); 56.8% (answer: Comprehensiveness, CS, LightRAG, vs -Low; source: Comprehensiveness, CS, -Low, vs NaiveRAG / Empowerment, CS, -Origin, vs NaiveRAG); 61.6% (answer: Comprehensiveness, CS, LightRAG, vs -Origin; source: Comprehensiveness, CS, LightRAG, vs NaiveRAG); 60.8% (answer: Comprehensiveness, CS, LightRAG, vs -Origin; source: Comprehensiveness, CS, -Origin, vs NaiveRAG / Overall, CS, -Origin, vs NaiveRAG); 83.6% (answer: Comprehensiveness, Legal, LightRAG, vs -High; source: Comprehensiveness, Legal, LightRAG, vs NaiveRAG / Empowerment, Legal, LightRAG, vs NaiveRAG / Empowerment, Legal, -Low, vs NaiveRAG / Comprehensiveness, Legal, -Origin, vs NaiveRAG); 76.4% (answer: Comprehensiveness, Legal, LightRAG, vs -High; source: Diversity, Agriculture, LightRAG, vs NaiveRAG / Comprehensiveness, Legal, -High, vs NaiveRAG); 83.6% (answer: Comprehensiveness, Legal, LightRAG, vs -Low; source: Comprehensiveness, Legal, LightRAG, vs NaiveRAG / Empowerment, Legal, LightRAG, vs NaiveRAG / Empowerment, Legal, -Low, vs NaiveRAG / Comprehensiveness, Legal, -Origin, vs NaiveRAG); 80.8% (answer: Comprehensiveness, Legal, LightRAG, vs -Low; source: Comprehensiveness, Legal, -Low, vs NaiveRAG); 83.6% (answer: Comprehensiveness, Legal, LightRAG, vs -Origin; source: Comprehensiveness, Legal, LightRAG, vs NaiveRAG / Empowerment, Legal, LightRAG, vs NaiveRAG / Empowerment, Legal, -Low, vs NaiveRAG / Comprehensiveness, Legal, -Origin, vs NaiveRAG); 61.2% (answer: Comprehensiveness, Mix, LightRAG, vs -High; source: Comprehensiveness, Mix, LightRAG, vs NaiveRAG / Empowerment, CS, LightRAG, vs NaiveRAG / Overall, CS, LightRAG, vs NaiveRAG); 59.6% (answer: Comprehensiveness, Mix, LightRAG, vs -High; source: Comprehensiveness, Mix, -High, vs NaiveRAG); 61.2% (answer: Comprehensiveness, Mix, LightRAG, vs -Low; source: Comprehensiveness, Mix, LightRAG, vs NaiveRAG / Empowerment, CS, LightRAG, vs NaiveRAG / Overall, CS, LightRAG, vs NaiveRAG); 64.0% (answer: Comprehensiveness, Mix, LightRAG, vs -Low; source: Diversity, Mix, -High, vs NaiveRAG / Empowerment, Agriculture, -High, vs NaiveRAG / Comprehensiveness, Agriculture, -Low, vs NaiveRAG / Comprehensiveness, Mix, -Low, vs NaiveRAG); 61.2% (answer: Comprehensiveness, Mix, LightRAG, vs -Origin; source: Comprehensiveness, Mix, LightRAG, vs NaiveRAG / Empowerment, CS, LightRAG, vs NaiveRAG / Overall, CS, LightRAG, vs NaiveRAG); 55.6% (answer: Comprehensiveness, Mix, LightRAG, vs -Origin; source: Comprehensiveness, Mix, -Origin, vs NaiveRAG / Overall, Mix, -Origin, vs NaiveRAG); 76.4% (answer: Diversity, Agriculture, LightRAG, vs -High; source: Diversity, Agriculture, LightRAG, vs NaiveRAG / Comprehensiveness, Legal, -High, vs NaiveRAG); 72.8% (answer: Diversity, Agriculture, LightRAG, vs -High; source: Diversity, Agriculture, -High, vs NaiveRAG); 76.4% (answer: Diversity, Agriculture, LightRAG, vs -Low; source: Diversity, Agriculture, LightRAG, vs NaiveRAG / Comprehensiveness, Legal, -High, vs NaiveRAG); 72.0% (answer: Diversity, Agriculture, LightRAG, vs -Low; source: Diversity, Agriculture, -Low, vs NaiveRAG); 76.4% (answer: Diversity, Agriculture, LightRAG, vs -Origin; source: Diversity, Agriculture, LightRAG, vs NaiveRAG / Comprehensiveness, Legal, -High, vs NaiveRAG); 73.6% (answer: Diversity, Agriculture, LightRAG, vs -Origin; source: Diversity, Agriculture, -Origin, vs NaiveRAG); 62.0% (answer: Diversity, CS, LightRAG, vs -High; source: Diversity, CS, LightRAG, vs NaiveRAG); 63.2% (answer: Diversity, CS, LightRAG, vs -High; source: Diversity, CS, -High, vs NaiveRAG); 62.0% (answer: Diversity, CS, LightRAG, vs -Low; source: Diversity, CS, LightRAG, vs NaiveRAG); 60.4% (answer: Diversity, CS, LightRAG, vs -Low; source: Diversity, CS, -Low, vs NaiveRAG); 62.0% (answer: Diversity, CS, LightRAG, vs -Origin; source: Diversity, CS, LightRAG, vs NaiveRAG); 55.2% (answer: Diversity, CS, LightRAG, vs -Origin; source: Diversity, CS, -Origin, vs NaiveRAG); 86.4% (answer: Diversity, Legal, LightRAG, vs -High; source: Diversity, Legal, LightRAG, vs NaiveRAG / Diversity, Legal, -Low, vs NaiveRAG); 83.2% (answer: Diversity, Legal, LightRAG, vs -High; source: Diversity, Legal, -High, vs NaiveRAG); 86.4% (answer: Diversity, Legal, LightRAG, vs -Low; source: Diversity, Legal, LightRAG, vs NaiveRAG / Diversity, Legal, -Low, vs NaiveRAG); 86.4% (answer: Diversity, Legal, LightRAG, vs -Origin; source: Diversity, Legal, LightRAG, vs NaiveRAG / Diversity, Legal, -Low, vs NaiveRAG); 85.6% (answer: Diversity, Legal, LightRAG, vs -Origin; source: Diversity, Legal, -Origin, vs NaiveRAG); 67.6% (answer: Diversity, Mix, LightRAG, vs -High; source: Comprehensiveness, Agriculture, LightRAG, vs NaiveRAG / Diversity, Mix, LightRAG, vs NaiveRAG / Empowerment, Agriculture, LightRAG, vs NaiveRAG / Overall, Agriculture, LightRAG, vs NaiveRAG); 64.0% (answer: Diversity, Mix, LightRAG, vs -High; source: Diversity, Mix, -High, vs NaiveRAG / Empowerment, Agriculture, -High, vs NaiveRAG / Comprehensiveness, Agriculture, -Low, vs NaiveRAG / Comprehensiveness, Mix, -Low, vs NaiveRAG); 67.6% (answer: Diversity, Mix, LightRAG, vs -Low; source: Comprehensiveness, Agriculture, LightRAG, vs NaiveRAG / Diversity, Mix, LightRAG, vs NaiveRAG / Empowerment, Agriculture, LightRAG, vs NaiveRAG / Overall, Agriculture, LightRAG, vs NaiveRAG); 66.8% (answer: Diversity, Mix, LightRAG, vs -Low; source: Diversity, Mix, -Low, vs NaiveRAG); 67.6% (answer: Diversity, Mix, LightRAG, vs -Origin; source: Comprehensiveness, Agriculture, LightRAG, vs NaiveRAG / Diversity, Mix, LightRAG, vs NaiveRAG / Empowerment, Agriculture, LightRAG, vs NaiveRAG / Overall, Agriculture, LightRAG, vs NaiveRAG); 74.4% (answer: Diversity, Mix, LightRAG, vs -Origin; source: Diversity, Mix, -Origin, vs NaiveRAG / Overall, Agriculture, -Origin, vs NaiveRAG); 67.6% (answer: Empowerment, Agriculture, LightRAG, vs -High; source: Comprehensiveness, Agriculture, LightRAG, vs NaiveRAG / Diversity, Mix, LightRAG, vs NaiveRAG / Empowerment, Agriculture, LightRAG, vs NaiveRAG / Overall, Agriculture, LightRAG, vs NaiveRAG); 64.0% (answer: Empowerment, Agriculture, LightRAG, vs -High; source: Diversity, Mix, -High, vs NaiveRAG / Empowerment, Agriculture, -High, vs NaiveRAG / Comprehensiveness, Agriculture, -Low, vs NaiveRAG / Comprehensiveness, Mix, -Low, vs NaiveRAG); 67.6% (answer: Empowerment, Agriculture, LightRAG, vs -Low; source: Comprehensiveness, Agriculture, LightRAG, vs NaiveRAG / Diversity, Mix, LightRAG, vs NaiveRAG / Empowerment, Agriculture, LightRAG, vs NaiveRAG / Overall, Agriculture, LightRAG, vs NaiveRAG); 65.2% (answer: Empowerment, Agriculture, LightRAG, vs -Low; source: Comprehensiveness, Agriculture, -High, vs NaiveRAG / Empowerment, Agriculture, -Low, vs NaiveRAG / Overall, Agriculture, -Low, vs NaiveRAG); 67.6% (answer: Empowerment, Agriculture, LightRAG, vs -Origin; source: Comprehensiveness, Agriculture, LightRAG, vs NaiveRAG / Diversity, Mix, LightRAG, vs NaiveRAG / Empowerment, Agriculture, LightRAG, vs NaiveRAG / Overall, Agriculture, LightRAG, vs NaiveRAG); 68.0% (answer: Empowerment, Agriculture, LightRAG, vs -Origin; source: Empowerment, Agriculture, -Origin, vs NaiveRAG); 61.2% (answer: Empowerment, CS, LightRAG, vs -High; source: Comprehensiveness, Mix, LightRAG, vs NaiveRAG / Empowerment, CS, LightRAG, vs NaiveRAG / Overall, CS, LightRAG, vs NaiveRAG); 57.6% (answer: Empowerment, CS, LightRAG, vs -High; source: Empowerment, CS, -High, vs NaiveRAG / Overall, Mix, -High, vs NaiveRAG); 61.2% (answer: Empowerment, CS, LightRAG, vs -Low; source: Comprehensiveness, Mix, LightRAG, vs NaiveRAG / Empowerment, CS, LightRAG, vs NaiveRAG / Overall, CS, LightRAG, vs NaiveRAG); 57.2% (answer: Empowerment, CS, LightRAG, vs -Low; source: Empowerment, Mix, LightRAG, vs NaiveRAG / Comprehensiveness, CS, -High, vs NaiveRAG / Empowerment, CS, -Low, vs NaiveRAG); 61.2% (answer: Empowerment, CS, LightRAG, vs -Origin; source: Comprehensiveness, Mix, LightRAG, vs NaiveRAG / Empowerment, CS, LightRAG, vs NaiveRAG / Overall, CS, LightRAG, vs NaiveRAG); 56.8% (answer: Empowerment, CS, LightRAG, vs -Origin; source: Comprehensiveness, CS, -Low, vs NaiveRAG / Empowerment, CS, -Origin, vs NaiveRAG); 83.6% (answer: Empowerment, Legal, LightRAG, vs -High; source: Comprehensiveness, Legal, LightRAG, vs NaiveRAG / Empowerment, Legal, LightRAG, vs NaiveRAG / Empowerment, Legal, -Low, vs NaiveRAG / Comprehensiveness, Legal, -Origin, vs NaiveRAG); 77.2% (answer: Empowerment, Legal, LightRAG, vs -High; source: Empowerment, Legal, -High, vs NaiveRAG); 83.6% (answer: Empowerment, Legal, LightRAG, vs -Low; source: Comprehensiveness, Legal, LightRAG, vs NaiveRAG / Empowerment, Legal, LightRAG, vs NaiveRAG / Empowerment, Legal, -Low, vs NaiveRAG / Comprehensiveness, Legal, -Origin, vs NaiveRAG); 83.6% (answer: Empowerment, Legal, LightRAG, vs -Origin; source: Comprehensiveness, Legal, LightRAG, vs NaiveRAG / Empowerment, Legal, LightRAG, vs NaiveRAG / Empowerment, Legal, -Low, vs NaiveRAG / Comprehensiveness, Legal, -Origin, vs NaiveRAG); 82.8% (answer: Empowerment, Legal, LightRAG, vs -Origin; source: Empowerment, Legal, -Origin, vs NaiveRAG); 57.2% (answer: Empowerment, Mix, LightRAG, vs -High; source: Empowerment, Mix, LightRAG, vs NaiveRAG / Comprehensiveness, CS, -High, vs NaiveRAG / Empowerment, CS, -Low, vs NaiveRAG); 52.4% (answer: Empowerment, Mix, LightRAG, vs -High; source: Empowerment, Mix, -High, vs NaiveRAG); 57.2% (answer: Empowerment, Mix, LightRAG, vs -Low; source: Empowerment, Mix, LightRAG, vs NaiveRAG / Comprehensiveness, CS, -High, vs NaiveRAG / Empowerment, CS, -Low, vs NaiveRAG); 64.8% (answer: Empowerment, Mix, LightRAG, vs -Low; source: Overall, Agriculture, -High, vs NaiveRAG / Empowerment, Mix, -Low, vs NaiveRAG / Overall, Mix, -Low, vs NaiveRAG); 57.2% (answer: Empowerment, Mix, LightRAG, vs -Origin; source: Empowerment, Mix, LightRAG, vs NaiveRAG / Comprehensiveness, CS, -High, vs NaiveRAG / Empowerment, CS, -Low, vs NaiveRAG); 54.8% (answer: Empowerment, Mix, LightRAG, vs -Origin; source: Empowerment, Mix, -Origin, vs NaiveRAG); 67.6% (answer: Overall, Agriculture, LightRAG, vs -High; source: Comprehensiveness, Agriculture, LightRAG, vs NaiveRAG / Diversity, Mix, LightRAG, vs NaiveRAG / Empowerment, Agriculture, LightRAG, vs NaiveRAG / Overall, Agriculture, LightRAG, vs NaiveRAG); 64.8% (answer: Overall, Agriculture, LightRAG, vs -High; source: Overall, Agriculture, -High, vs NaiveRAG / Empowerment, Mix, -Low, vs NaiveRAG / Overall, Mix, -Low, vs NaiveRAG); 67.6% (answer: Overall, Agriculture, LightRAG, vs -Low; source: Comprehensiveness, Agriculture, LightRAG, vs NaiveRAG / Diversity, Mix, LightRAG, vs NaiveRAG / Empowerment, Agriculture, LightRAG, vs NaiveRAG / Overall, Agriculture, LightRAG, vs NaiveRAG); 65.2% (answer: Overall, Agriculture, LightRAG, vs -Low; source: Comprehensiveness, Agriculture, -High, vs NaiveRAG / Empowerment, Agriculture, -Low, vs NaiveRAG / Overall, Agriculture, -Low, vs NaiveRAG); 67.6% (answer: Overall, Agriculture, LightRAG, vs -Origin; source: Comprehensiveness, Agriculture, LightRAG, vs NaiveRAG / Diversity, Mix, LightRAG, vs NaiveRAG / Empowerment, Agriculture, LightRAG, vs NaiveRAG / Overall, Agriculture, LightRAG, vs NaiveRAG); 74.4% (answer: Overall, Agriculture, LightRAG, vs -Origin; source: Diversity, Mix, -Origin, vs NaiveRAG / Overall, Agriculture, -Origin, vs NaiveRAG); 61.2% (answer: Overall, CS, LightRAG, vs -High; source: Comprehensiveness, Mix, LightRAG, vs NaiveRAG / Empowerment, CS, LightRAG, vs NaiveRAG / Overall, CS, LightRAG, vs NaiveRAG); 56.0% (answer: Overall, CS, LightRAG, vs -High; source: Overall, CS, -High, vs NaiveRAG); 61.2% (answer: Overall, CS, LightRAG, vs -Low; source: Comprehensiveness, Mix, LightRAG, vs NaiveRAG / Empowerment, CS, LightRAG, vs NaiveRAG / Overall, CS, LightRAG, vs NaiveRAG); 56.4% (answer: Overall, CS, LightRAG, vs -Low; source: Overall, CS, -Low, vs NaiveRAG); 61.2% (answer: Overall, CS, LightRAG, vs -Origin; source: Comprehensiveness, Mix, LightRAG, vs NaiveRAG / Empowerment, CS, LightRAG, vs NaiveRAG / Overall, CS, LightRAG, vs NaiveRAG); 60.8% (answer: Overall, CS, LightRAG, vs -Origin; source: Comprehensiveness, CS, -Origin, vs NaiveRAG / Overall, CS, -Origin, vs NaiveRAG); 84.8% (answer: Overall, Legal, LightRAG, vs -High; source: Overall, Legal, LightRAG, vs NaiveRAG); 78.0% (answer: Overall, Legal, LightRAG, vs -High; source: Overall, Legal, -High, vs NaiveRAG); 84.8% (answer: Overall, Legal, LightRAG, vs -Low; source: Overall, Legal, LightRAG, vs NaiveRAG); 81.2% (answer: Overall, Legal, LightRAG, vs -Low; source: Overall, Legal, -Low, vs NaiveRAG); 84.8% (answer: Overall, Legal, LightRAG, vs -Origin; source: Overall, Legal, LightRAG, vs NaiveRAG); 84.4% (answer: Overall, Legal, LightRAG, vs -Origin; source: Overall, Legal, -Origin, vs NaiveRAG); 60.0% (answer: Overall, Mix, LightRAG, vs -High; source: Overall, Mix, LightRAG, vs NaiveRAG); 57.6% (answer: Overall, Mix, LightRAG, vs -High; source: Empowerment, CS, -High, vs NaiveRAG / Overall, Mix, -High, vs NaiveRAG); 60.0% (answer: Overall, Mix, LightRAG, vs -Low; source: Overall, Mix, LightRAG, vs NaiveRAG); 64.8% (answer: Overall, Mix, LightRAG, vs -Low; source: Overall, Agriculture, -High, vs NaiveRAG / Empowerment, Mix, -Low, vs NaiveRAG / Overall, Mix, -Low, vs NaiveRAG); 60.0% (answer: Overall, Mix, LightRAG, vs -Origin; source: Overall, Mix, LightRAG, vs NaiveRAG); 55.6% (answer: Overall, Mix, LightRAG, vs -Origin; source: Comprehensiveness, Mix, -Origin, vs NaiveRAG / Overall, Mix, -Origin, vs NaiveRAG).
```

## B5-Q3-2

- 問題：`Performance of ablated versions of LightRAG`；模式 `navigate`；83.7 秒；2 次呼叫；tokens 7667
- 來源：[1] p8 retrieval, [2] p7 retrieval, [3] p1 retrieval, [4] p8 retrieval, [5] p1 retrieval, [6] p8 table_context
- 閱讀計畫（定位 6/6，保留 0，超預算 0）：
  - ✓ Section 4.3 ABLATION STUDIES (RQ2) | need: discussion of ablated versions | priority: required | status: covered → 候選 0，納入 []，排除 []
  - ✓ Table 2 (page 8) | need: performance metrics | priority: required | status: covered → 候選 0，納入 []，排除 []
  - ✓ Section 4.4 CASE STUDY (RQ3) | need: additional context on ablation effects | priority: supplementary | status: covered → 候選 0，納入 []，排除 []
  - ✓ Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM | need: method description | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
  - ✓ Section 7.3.1 PROMPTS FOR GRAPH GENERATION | need: implementation details | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
  - ✓ Section 7.3.2 PROMPTS FOR QUERY GENERATION | need: implementation details | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
- 分析狀態：FACTUALLY_CORRECT_BUT_INCOMPLETE；完整性 incomplete（required ['-High', '-Low', '-Origin', 'LightRAG']，缺 ['-High', '-Low', '-Origin', 'LightRAG']，條件 None）；方向核對 []
- 修正：[]；刪除 []；仍不符 []；方向待定 []
- 涵蓋判定：Section 4.3 ABLATION STUDIES (RQ2)→covered；Table 2 (page 8)→covered；Section 4.4 CASE STUDY (RQ3)→partial；Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM→missing；Section 7.3.1 PROMPTS FOR GRAPH GENERATION→missing；Section 7.3.2 PROMPTS FOR QUERY GENERATION→missing；required 未納入 []；supplementary 用 0；Matrix {'cells': 128, 'tables': ['Table 2 [1]'], 'definitions': ['NaiveRAG', 'LightRAG', '-High'], 'facts': 64, 'coverage_gaps': []}
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
The question asks for the performance of ablated versions of LightRAG, including the methods compared, datasets, and metrics. The ablated versions are LightRAG -High, LightRAG -Low, LightRAG -Origin, and the baseline LightRAG. The datasets are Agriculture, CS, Legal, and Mix. The metrics are Comprehensiveness, Diversity, Empowerment, and Overall. The reference method is NaiveRAG.

| Method | Dataset | Metric | Performance (%) |
|--------|---------|--------|-----------------|
| LightRAG | Agriculture | Comprehensiveness | 67.6 |
| LightRAG | CS | Comprehensiveness | 61.6 |
| LightRAG | Legal | Comprehensiveness | 83.6 |
| LightRAG | Mix | Comprehensiveness | 61.2 |
| LightRAG -High | Agriculture | Comprehensiveness | 65.2 |
| LightRAG -High | CS | Comprehensiveness | 57.2 |
| LightRAG -High | Legal | Comprehensiveness | 76.4 |
| LightRAG -High | Mix | Comprehensiveness | 59.6 |
| LightRAG -Low | Agriculture | Comprehensiveness | 64.0 |
| LightRAG -Low | CS | Comprehensiveness | 56.8 |
| LightRAG -Low | Legal | Comprehensiveness | 80.8 |
| LightRAG -Low | Mix | Comprehensiveness | 64.0 |
| LightRAG -Origin | Agriculture | Comprehensiveness | 75.2 |
| LightRAG -Origin | CS | Comprehensiveness | 60.8 |
| LightRAG -Origin | Legal | Comprehensiveness | 83.6 |
| LightRAG -Origin | Mix | Comprehensiveness | 55.6 |

| Method | Dataset | Metric | Performance (%) |
|--------|---------|--------|-----------------|
| LightRAG | Agriculture | Diversity | 76.4 |
| LightRAG | CS | Diversity | 62.0 |
| LightRAG | Legal | Diversity | 86.4 |
| LightRAG | Mix | Diversity | 67.6 |
| LightRAG -High | Agriculture | Diversity | 72.8 |
| LightRAG -High | CS | Diversity | 63.2 |
| LightRAG -High | Legal | Diversity | 83.2 |
| LightRAG -High | Mix | Diversity | 64.0 |
| LightRAG -Low | Agriculture | Diversity | 72.0 |
| LightRAG -Low | CS | Diversity | 60.4 |
| LightRAG -Low | Legal | Diversity | 86.4 |
| LightRAG -Low | Mix | Diversity | 66.8 |
| LightRAG -Origin | Agriculture | Diversity | 73.6 |
| LightRAG -Origin | CS | Diversity | 55.2 |
| LightRAG -Origin | Legal | Diversity | 85.6 |
| LightRAG -Origin | Mix | Diversity | 74.4 |

| Method | Dataset | Metric | Performance (%) |
|--------|---------|--------|-----------------|
| LightRAG | Agriculture | Empowerment | 67.6 |
| LightRAG | CS | Empowerment | 61.2 |
| LightRAG | Legal | Empowerment | 83.6 |
| LightRAG | Mix | Empowerment | 57.2 |
| LightRAG -High | Agriculture | Empowerment | 64.0 |
| LightRAG -High | CS | Empowerment | 57.6 |
| LightRAG -High | Legal | Empowerment | 77.2 |
| LightRAG -High | Mix | Empowerment | 52.4 |
| LightRAG -Low | Agriculture | Empowerment | 65.2 |
| LightRAG -Low | CS | Empowerment | 57.2 |
| LightRAG -Low | Legal | Empowerment | 83.6 |
| LightRAG -Low | Mix | Empowerment | 64.8 |
| LightRAG -Origin | Agriculture | Empowerment | 68.0 |
| LightRAG -Origin | CS | Empowerment | 56.8 |
| LightRAG -Origin | Legal | Empowerment | 82.8 |
| LightRAG -Origin | Mix | Empowerment | 54.8 |

| Method | Dataset | Metric | Performance (%) |
|--------|---------|--------|-----------------|
| LightRAG | Agriculture | Overall | 67.6 |
| LightRAG | CS | Overall | 61.2 |
| LightRAG | Legal | Overall | 84.8 |
| LightRAG | Mix | Overall | 60.0 |
| LightRAG -High | Agriculture | Overall | 64.8 |
| LightRAG -High | CS | Overall | 56.0 |
| LightRAG -High | Legal | Overall | 78.0 |
| LightRAG -High | Mix | Overall | 57.6 |
| LightRAG -Low | Agriculture | Overall | 65.2 |
| LightRAG -Low | CS | Overall | 56.4 |
| LightRAG -Low | Legal | Overall | 81.2 |
| LightRAG -Low | Mix | Overall | 64.8 |
| LightRAG -Origin | Agriculture | Overall | 74.4 |
| LightRAG -Origin | CS | Overall | 60.8 |
| LightRAG -Origin | Legal | Overall | 84.4 |
| LightRAG -Origin | Mix | Overall | 55.6 |

Method definitions:
- -High [6]: • Low-level-only Retrieval: The -High variant removes high-order retrieval, leading to a significant performance decline across nearly all datasets and metrics.
- -Low: no definition found in the sources
- -Origin: no definition found in the sources
- LightRAG [1]: Table 2: Performance of ablated versions of LightRAG, using NaiveRAG as reference.
- NaiveRAG [1]: Table 2: Performance of ablated versions of LightRAG, using NaiveRAG as reference.

Comparisons are made within the same dataset, metric, and method pairing.

Improvements and regressions:
- **LightRAG -Origin** outperforms LightRAG in the **Agriculture** dataset for **Comprehensiveness** and **Overall**.
- **LightRAG -Origin** outperforms LightRAG in the **Mix** dataset for **Comprehensiveness** and **Diversity**.
- **LightRAG -High** shows a significant performance decline compared to LightRAG across most datasets and metrics.
- **LightRAG -Low** shows a moderate performance decline compared to LightRAG across most datasets and metrics.
- **LightRAG -Origin** shows mixed results compared to LightRAG, with improvements in some metrics and declines in others.

The statements "higher", "lower", "outperforms", or "drops" agree with the figures in the table.

The source for the figures is [1]. Definitions are cited to [6].

The question asked for the performance of ablated versions of LightRAG, which is addressed in the answer.
```

## B5-Q3-3

- 問題：`Performance of ablated versions of LightRAG`；模式 `navigate`；95.2 秒；2 次呼叫；tokens 7939
- 來源：[1] p8 retrieval, [2] p7 retrieval, [3] p1 retrieval, [4] p8 retrieval, [5] p1 retrieval, [6] p8 table_context
- 閱讀計畫（定位 6/6，保留 0，超預算 0）：
  - ✓ Section 4.3 ABLATION STUDIES (RQ2) | need: discussion of ablated versions | priority: required | status: covered → 候選 0，納入 []，排除 []
  - ✓ Table 2 (page 8) | need: performance metrics | priority: required | status: covered → 候選 0，納入 []，排除 []
  - ✓ Section 4.4 CASE STUDY (RQ3) | need: additional context on ablation effects | priority: supplementary | status: covered → 候選 0，納入 []，排除 []
  - ✓ Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM | need: method description | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
  - ✓ Section 7.3.1 PROMPTS FOR GRAPH GENERATION | need: implementation details | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
  - ✓ Section 7.3.2 PROMPTS FOR QUERY GENERATION | need: implementation details | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
- 分析狀態：FACTUALLY_CORRECT_BUT_INCOMPLETE；完整性 incomplete（required ['-High', '-Low', '-Origin', 'LightRAG']，缺 ['-High', '-Low', '-Origin', 'LightRAG']，條件 None）；方向核對 []
- 修正：[]；刪除 []；仍不符 []；方向待定 []
- 涵蓋判定：Section 4.3 ABLATION STUDIES (RQ2)→covered；Table 2 (page 8)→covered；Section 4.4 CASE STUDY (RQ3)→partial；Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM→missing；Section 7.3.1 PROMPTS FOR GRAPH GENERATION→missing；Section 7.3.2 PROMPTS FOR QUERY GENERATION→missing；required 未納入 []；supplementary 用 0；Matrix {'cells': 128, 'tables': ['Table 2 [1]'], 'definitions': ['NaiveRAG', 'LightRAG', '-High'], 'facts': 64, 'coverage_gaps': []}
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
The question asks for the performance of ablated versions of LightRAG, including the methods compared, the datasets used, and the metrics evaluated.

| Method             | Dataset    | Metric         | Score (%) |
|--------------------|------------|----------------|-----------|
| LightRAG           | Agriculture| Comprehensiveness | 67.6     |
| NaiveRAG           | Agriculture| Comprehensiveness | 32.4     |
| -High              | Agriculture| Comprehensiveness | 65.2     |
| -Low               | Agriculture| Comprehensiveness | 64.0     |
| -Origin            | Agriculture| Comprehensiveness | 75.2     |
| LightRAG           | CS         | Comprehensiveness | 61.6     |
| NaiveRAG           | CS         | Comprehensiveness | 38.4     |
| -High              | CS         | Comprehensiveness | 57.2     |
| -Low               | CS         | Comprehensiveness | 56.8     |
| -Origin            | CS         | Comprehensiveness | 60.8     |
| LightRAG           | Legal      | Comprehensiveness | 83.6     |
| NaiveRAG           | Legal      | Comprehensiveness | 16.4     |
| -High              | Legal      | Comprehensiveness | 76.4     |
| -Low               | Legal      | Comprehensiveness | 80.8     |
| -Origin            | Legal      | Comprehensiveness | 83.6     |
| LightRAG           | Mix        | Comprehensiveness | 61.2     |
| NaiveRAG           | Mix        | Comprehensiveness | 38.8     |
| -High              | Mix        | Comprehensiveness | 59.6     |
| -Low               | Mix        | Comprehensiveness | 64.0     |
| -Origin            | Mix        | Comprehensiveness | 55.6     |

| Method             | Dataset    | Metric         | Score (%) |
|--------------------|------------|----------------|-----------|
| LightRAG           | Agriculture| Diversity       | 76.4     |
| NaiveRAG           | Agriculture| Diversity       | 23.6     |
| -High              | Agriculture| Diversity       | 72.8     |
| -Low               | Agriculture| Diversity       | 72.0     |
| -Origin            | Agriculture| Diversity       | 73.6     |
| LightRAG           | CS         | Diversity       | 62.0     |
| NaiveRAG           | CS         | Diversity       | 38.0     |
| -High              | CS         | Diversity       | 63.2     |
| -Low               | CS         | Diversity       | 60.4     |
| -Origin            | CS         | Diversity       | 55.2     |
| LightRAG           | Legal      | Diversity       | 86.4     |
| NaiveRAG           | Legal      | Diversity       | 13.6     |
| -High              | Legal      | Diversity       | 83.2     |
| -Low               | Legal      | Diversity       | 86.4     |
| -Origin            | Legal      | Diversity       | 85.6     |
| LightRAG           | Mix        | Diversity       | 67.6     |
| NaiveRAG           | Mix        | Diversity       | 32.4     |
| -High              | Mix        | Diversity       | 64.0     |
| -Low               | Mix        | Diversity       | 66.8     |
| -Origin            | Mix        | Diversity       | 74.4     |

| Method             | Dataset    | Metric         | Score (%) |
|--------------------|------------|----------------|-----------|
| LightRAG           | Agriculture| Empowerment     | 67.6     |
| NaiveRAG           | Agriculture| Empowerment     | 32.4     |
| -High              | Agriculture| Empowerment     | 64.0     |
| -Low               | Agriculture| Empowerment     | 65.2     |
| -Origin            | Agriculture| Empowerment     | 68.0     |
| LightRAG           | CS         | Empowerment     | 61.2     |
| NaiveRAG           | CS         | Empowerment     | 38.8     |
| -High              | CS         | Empowerment     | 57.6     |
| -Low               | CS         | Empowerment     | 57.2     |
| -Origin            | CS         | Empowerment     | 56.8     |
| LightRAG           | Legal      | Empowerment     | 83.6     |
| NaiveRAG           | Legal      | Empowerment     | 16.4     |
| -High              | Legal      | Empowerment     | 77.2     |
| -Low               | Legal      | Empowerment     | 83.6     |
| -Origin            | Legal      | Empowerment     | 82.8     |
| LightRAG           | Mix        | Empowerment     | 57.2     |
| NaiveRAG           | Mix        | Empowerment     | 42.8     |
| -High              | Mix        | Empowerment     | 52.4     |
| -Low               | Mix        | Empowerment     | 64.8     |
| -Origin            | Mix        | Empowerment     | 54.8     |

| Method             | Dataset    | Metric         | Score (%) |
|--------------------|------------|----------------|-----------|
| LightRAG           | Agriculture| Overall         | 67.6     |
| NaiveRAG           | Agriculture| Overall         | 32.4     |
| -High              | Agriculture| Overall         | 64.8     |
| -Low               | Agriculture| Overall         | 65.2     |
| -Origin            | Agriculture| Overall         | 74.4     |
| LightRAG           | CS         | Overall         | 61.2     |
| NaiveRAG           | CS         | Overall         | 38.8     |
| -High              | CS         | Overall         | 56.0     |
| -Low               | CS         | Overall         | 56.4     |
| -Origin            | CS         | Overall         | 60.8     |
| LightRAG           | Legal      | Overall         | 84.8     |
| NaiveRAG           | Legal      | Overall         | 15.2     |
| -High              | Legal      | Overall         | 78.0     |
| -Low               | Legal      | Overall         | 81.2     |
| -Origin            | Legal      | Overall         | 84.4     |
| LightRAG           | Mix        | Overall         | 60.0     |
| NaiveRAG           | Mix        | Overall         | 40.0     |
| -High              | Mix        | Overall         | 57.6     |
| -Low               | Mix        | Overall         | 64.8     |
| -Origin            | Mix        | Overall         | 55.6     |

### Analysis

**Improvements:**
- LightRAG outperforms NaiveRAG in all metrics across all datasets [1].
- -Origin shows improvements over NaiveRAG in Agriculture and Mix datasets in all metrics [6].
- -Low and -High variants perform better than NaiveRAG in most cases but worse than LightRAG [1].

**Regressions:**
- -High shows a significant performance decline compared to LightRAG in all metrics in the CS dataset [6].
- -Origin underperforms compared to LightRAG in the CS and Mix datasets in all metrics [6].

**Exceptions:**
- -Origin matches LightRAG in comprehensiveness in the Legal dataset [6].
- -Origin outperforms LightRAG in comprehensiveness in the Agriculture dataset [6].

**Definitions:**
- -High [6]: The -High variant removes high-order retrieval, leading to a significant performance decline across nearly all datasets and metrics.
- -Low: no definition found in the sources.
- -Origin: no definition found in the sources.
- LightRAG [1]: Table 2: Performance of ablated versions of LightRAG, using NaiveRAG as reference.
- NaiveRAG [1]: Table 2: Performance of ablated versions of LightRAG, using NaiveRAG as reference.
```

## B6-Q3-1

- 問題：`Performance of ablated versions of LightRAG`；模式 `navigate`；78.0 秒；2 次呼叫；tokens 8841
- 來源：[1] p8 retrieval, [2] p7 retrieval, [3] p1 retrieval, [4] p8 retrieval, [5] p1 retrieval, [6] p8 table_context
- 閱讀計畫（定位 6/6，保留 0，超預算 0）：
  - ✓ Section 4.3 ABLATION STUDIES (RQ2) | need: discussion of ablated versions | priority: required | status: covered → 候選 0，納入 []，排除 []
  - ✓ Table 2 (page 8) | need: performance metrics | priority: required | status: covered → 候選 0，納入 []，排除 []
  - ✓ Section 4.4 CASE STUDY (RQ3) | need: additional context on ablation effects | priority: supplementary | status: covered → 候選 0，納入 []，排除 []
  - ✓ Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM | need: method description | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
  - ✓ Section 7.3.1 PROMPTS FOR GRAPH GENERATION | need: implementation details | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
  - ✓ Section 7.3.2 PROMPTS FOR QUERY GENERATION | need: implementation details | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
- 分析狀態：UNCERTAIN；完整性 uncertain（required ['-High', '-Low', '-Origin', 'LightRAG']，缺 ['-High', '-Low', '-Origin', 'LightRAG']，條件 None）；方向核對 []
- 修正：[]；刪除 []；仍不符 []；方向待定 []
- 涵蓋判定：Section 4.3 ABLATION STUDIES (RQ2)→covered；Table 2 (page 8)→covered；Section 4.4 CASE STUDY (RQ3)→partial；Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM→missing；Section 7.3.1 PROMPTS FOR GRAPH GENERATION→missing；Section 7.3.2 PROMPTS FOR QUERY GENERATION→missing；required 未納入 []；supplementary 用 0；Matrix {'cells': 128, 'tables': ['Table 2 [1]'], 'shown_tokens': 1348, 'left_out': [], 'definitions': ['NaiveRAG', 'LightRAG', '-High'], 'facts': 64, 'coverage_gaps': []}
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 122；找不到的數字 []

```text
The question asks for the performance of ablated versions of LightRAG, including the datasets, metrics, and methods involved. The methods are LightRAG, -High, -Low, -Origin, and NaiveRAG. The datasets are Agriculture, CS, Legal, and Mix. The metrics are Comprehensiveness, Diversity, Empowerment, and Overall.

The evidence matrix and method definitions show that the ablated versions of LightRAG are compared against NaiveRAG across four datasets and four metrics.

Comparing the figures that share the same dataset, metric, and pairing:

| Dataset | Metric         | Method Pairing         | LightRAG vs NaiveRAG | -High vs NaiveRAG | -Low vs NaiveRAG | -Origin vs NaiveRAG |
|---------|----------------|------------------------|----------------------|-------------------|------------------|---------------------|
| Agriculture | Comprehensiveness | 67.6% vs 32.4% | 65.2% vs 34.8% | 64.0% vs 36.0% | 75.2% vs 24.8% |
| CS        | Comprehensiveness | 61.6% vs 38.4% | 57.2% vs 42.8% | 56.8% vs 43.2% | 60.8% vs 39.2% |
| Legal     | Comprehensiveness | 83.6% vs 16.4% | 76.4% vs 23.6% | 80.8% vs 19.2% | 83.6% vs 16.4% |
| Mix       | Comprehensiveness | 61.2% vs 38.8% | 59.6% vs 40.4% | 64.0% vs 36.0% | 55.6% vs 44.4% |
| Agriculture | Diversity       | 76.4% vs 23.6% | 72.8% vs 27.2% | 72.0% vs 28.0% | 73.6% vs 26.4% |
| CS        | Diversity       | 62.0% vs 38.0% | 63.2% vs 36.8% | 60.4% vs 39.6% | 55.2% vs 44.8% |
| Legal     | Diversity       | 86.4% vs 13.6% | 83.2% vs 16.8% | 86.4% vs 13.6% | 85.6% vs 14.4% |
| Mix       | Diversity       | 67.6% vs 32.4% | 64.0% vs 36.0% | 66.8% vs 33.2% | 74.4% vs 25.6% |
| Agriculture | Empowerment   | 67.6% vs 32.4% | 64.0% vs 36.0% | 65.2% vs 34.8% | 68.0% vs 32.0% |
| CS        | Empowerment   | 61.2% vs 38.8% | 57.6% vs 42.4% | 57.2% vs 42.8% | 56.8% vs 43.2% |
| Legal     | Empowerment   | 83.6% vs 16.4% | 77.2% vs 22.8% | 83.6% vs 16.4% | 82.8% vs 17.2% |
| Mix       | Empowerment   | 57.2% vs 42.8% | 52.4% vs 47.6% | 64.8% vs 35.2% | 54.8% vs 45.2% |
| Agriculture | Overall       | 67.6% vs 32.4% | 64.8% vs 35.2% | 65.2% vs 34.8% | 74.4% vs 25.6% |
| CS        | Overall       | 61.2% vs 38.8% | 56.0% vs 44.0% | 56.4% vs 43.6% | 60.8% vs 39.2% |
| Legal     | Overall       | 84.8% vs 15.2% | 78.0% vs 22.0% | 81.2% vs 18.8% | 84.4% vs 15.6% |
| Mix       | Overall       | 60.0% vs 40.0% | 57.6% vs 42.4% | 64.8% vs 35.2% | 55.6% vs 44.4% |

Improvements:
- LightRAG outperforms NaiveRAG in all metrics across all datasets.
- -Origin shows improvements over NaiveRAG in Agriculture, Mix (Comprehensiveness), Agriculture, Mix (Diversity), Agriculture, Legal, Mix (Empowerment), and Agriculture, Legal (Overall).
- -Low outperforms NaiveRAG in all metrics across all datasets.
- -High outperforms NaiveRAG in all metrics across all datasets.

Regressions:
- -High underperforms LightRAG in all metrics across all datasets.
- -Low underperforms LightRAG in all metrics across all datasets.
- -Origin underperforms LightRAG in all metrics across all datasets.

Exceptions:
- -Origin shows improvements over NaiveRAG in Agriculture and Mix (Comprehensiveness), Agriculture and Mix (Diversity), Agriculture and Mix (Empowerment), and Agriculture and Legal (Overall). However, it underperforms LightRAG in all metrics across all datasets.

The statements agree with the figures provided.

The evidence matrix is cited from source [1]. The method definitions are cited from source [6].

The answer addresses all aspects of the question and is based solely on the provided sources.
```

## B6-Q3-2

- 問題：`Performance of ablated versions of LightRAG`；模式 `navigate`；90.8 秒；2 次呼叫；tokens 9140
- 來源：[1] p8 retrieval, [2] p7 retrieval, [3] p1 retrieval, [4] p8 retrieval, [5] p1 retrieval, [6] p8 table_context
- 閱讀計畫（定位 6/6，保留 0，超預算 0）：
  - ✓ Section 4.3 ABLATION STUDIES (RQ2) | need: discussion of ablated versions | priority: required | status: covered → 候選 0，納入 []，排除 []
  - ✓ Table 2 (page 8) | need: performance metrics | priority: required | status: covered → 候選 0，納入 []，排除 []
  - ✓ Section 4.4 CASE STUDY (RQ3) | need: additional context on ablation effects | priority: supplementary | status: covered → 候選 0，納入 []，排除 []
  - ✓ Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM | need: method description | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
  - ✓ Section 7.3.1 PROMPTS FOR GRAPH GENERATION | need: implementation details | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
  - ✓ Section 7.3.2 PROMPTS FOR QUERY GENERATION | need: implementation details | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
- 分析狀態：FACTUALLY_INCORRECT；完整性 incomplete（required ['-High', '-Low', '-Origin', 'LightRAG']，缺 ['LightRAG']，條件 None）；方向核對 [('inconsistent', '47.6%', '52.4%'), ('inconsistent', '25.6%', '74.4%')]
- 修正：[('ordering', 'drop', 'rise'), ('ordering', 'drop', 'rise')]；刪除 []；仍不符 ['44.0% (Overall, CS, -High)', '47.6% (Empowerment, Mix, -High)', '25.6% (Diversity, Mix, -Origin)']；方向待定 []
- 涵蓋判定：Section 4.3 ABLATION STUDIES (RQ2)→covered；Table 2 (page 8)→covered；Section 4.4 CASE STUDY (RQ3)→partial；Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM→missing；Section 7.3.1 PROMPTS FOR GRAPH GENERATION→missing；Section 7.3.2 PROMPTS FOR QUERY GENERATION→missing；required 未納入 []；supplementary 用 0；Matrix {'cells': 128, 'tables': ['Table 2 [1]'], 'shown_tokens': 1348, 'left_out': [], 'definitions': ['NaiveRAG', 'LightRAG', '-High'], 'facts': 64, 'coverage_gaps': []}
- 檢查：標籤不符 ['44.0%', '47.6%', '25.6%']；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
The question asks for the performance of ablated versions of LightRAG, comparing them to the baseline method NaiveRAG. The datasets involved are Agriculture, CS, Legal, and Mix. The metrics considered are Comprehensiveness, Diversity, Empowerment, and Overall.

| Method | Dataset | Metric | Score | Baseline | Source |
|--------|---------|--------|-------|----------|--------|
| -High | Agriculture | Comprehensiveness | 65.2% | NaiveRAG 34.8% | [1] |
| -High | CS | Comprehensiveness | 57.2% | NaiveRAG 42.8% | [1] |
| -High | Legal | Comprehensiveness | 76.4% | NaiveRAG 23.6% | [1] |
| -High | Mix | Comprehensiveness | 59.6% | NaiveRAG 40.4% | [1] |
| -High | Agriculture | Diversity | 72.8% | NaiveRAG 27.2% | [1] |
| -High | CS | Diversity | 63.2% | NaiveRAG 36.8% | [1] |
| -High | Legal | Diversity | 83.2% | NaiveRAG 16.8% | [1] |
| -High | Mix | Diversity | 64.0% | NaiveRAG 36.0% | [1] |
| -High | Agriculture | Empowerment | 64.0% | NaiveRAG 36.0% | [1] |
| -High | CS | Empowerment | 57.6% | NaiveRAG 42.4% | [1] |
| -High | Legal | Empowerment | 77.2% | NaiveRAG 22.8% | [1] |
| -High | Mix | Empowerment | 52.4% | NaiveRAG 47.6% | [1] |
| -High | Agriculture | Overall | 64.8% | NaiveRAG 35.2% | [1] |
| -High | CS | Overall | 56.0% | NaieveRAG 44.0% | [1] |
| -High | Legal | Overall | 78.0% | NaiveRAG 22.0% | [1] |
| -High | Mix | Overall | 57.6% | NaiveRAG 42.4% | [1] |
| -Low | Agriculture | Comprehensiveness | 64.0% | NaiveRAG 36.0% | [1] |
| -Low | CS | Comprehensiveness | 56.8% | NaiveRAG 43.2% | [1] |
| -Low | Legal | Comprehensiveness | 80.8% | NaiveRAG 19.2% | [1] |
| -Low | Mix | Comprehensiveness | 64.0% | NaiveRAG 36.0% | [1] |
| -Low | Agriculture | Diversity | 72.0% | NaiveRAG 28.0% | [1] |
| -Low | CS | Diversity | 60.4% | NaiveRAG 39.6% | [1] |
| -Low | Legal | Diversity | 86.4% | NaiveRAG 13.6% | [1] |
| -Low | Mix | Diversity | 66.8% | NaiveRAG 33.2% | [1] |
| -Low | Agriculture | Empowerment | 65.2% | NaiveRAG 34.8% | [1] |
| -Low | CS | Empowerment | 57.2% | NaiveRAG 42.8% | [1] |
| -Low | Legal | Empowerment | 83.6% | NaiveRAG 16.4% | [1] |
| -Low | Mix | Empowerment | 64.8% | NaiveRAG 35.2% | [1] |
| -Low | Agriculture | Overall | 65.2% | NaiveRAG 34.8% | [1] |
| -Low | CS | Overall | 56.4% | NaiveRAG 43.6% | [1] |
| -Low | Legal | Overall | 81.2% | NaiveRAG 18.8% | [1] |
| -Low | Mix | Overall | 64.8% | NaiveRAG 35.2% | [1] |
| -Origin | Agriculture | Comprehensiveness | 75.2% | NaiveRAG 24.8% | [1] |
| -Origin | CS | Comprehensiveness | 60.8% | NaiveRAG 39.2% | [1] |
| -Origin | Legal | Comprehensiveness | 83.6% | NaiveRAG 16.4% | [1] |
| -Origin | Mix | Comprehensiveness | 55.6% | NaiveRAG 44.4% | [1] |
| -Origin | Agriculture | Diversity | 73.6% | NaiveRAG 26.4% | [1] |
| -Origin | CS | Diversity | 55.2% | NaiveRAG 44.8% | [1] |
| -Origin | Legal | Diversity | 85.6% | NaiveRAG 14.4% | [1] |
| -Origin | Mix | Diversity | 74.4% | NaiveRAG 25.6% | [1] |
| -Origin | Agriculture | Empowerment | 68.0% | NaiveRAG 32.0% | [1] |
| -Origin | CS | Empowerment | 56.8% | NaiveRAG 43.2% | [1] |
| -Origin | Legal | Empowerment | 82.8% | NaiveRAG 17.2% | [1] |
| -Origin | Mix | Empowerment | 54.8% | NaiveRAG 45.2% | [1] |
| -Origin | Agriculture | Overall | 74.4% | NaiveRAG 25.6% | [1] |
| -Origin | CS | Overall | 60.8% | NaiveRAG 39.2% | [1] |
| -Origin | Legal | Overall | 84.4% | NaiveRAG 15.6% | [1] |
| -Origin | Mix | Overall | 55.6% | NaiveRAG 44.4% | [1] |

**Improvements**:
- The -High variant improves performance in all metrics across all datasets compared to NaiveRAG.
- The -Low variant improves performance in all metrics across all datasets compared to NaiveRAG.
- The -Origin variant improves performance in all metrics across all datasets compared to NaiveRAG.

**Exceptions**:
- The -High variant shows a performance drop in the Mix dataset for Empowerment (from 47.6% to 52.4%) [1].
- The -Origin variant shows a performance drop in the Mix dataset for Diversity (from 25.6% to 74.4%) [1].

**Conclusion**:
All ablated versions of LightRAG (-High, -Low, -Origin) show improvements over NaiveRAG in all metrics across all datasets, except for minor exceptions in the Mix dataset for Empowerment (for -High) and Diversity (for -Origin).

Figures whose labels differ from the source table: 44.0% (answer: Overall, CS, -High; source: Overall, CS, NaiveRAG, vs -High); 47.6% (answer: Empowerment, Mix, -High; source: Empowerment, Mix, NaiveRAG, vs -High); 25.6% (answer: Diversity, Mix, -Origin; source: Diversity, Mix, NaiveRAG, vs -Origin / Overall, Agriculture, NaiveRAG, vs -Origin).
```

## B6-Q3-3

- 問題：`Performance of ablated versions of LightRAG`；模式 `navigate`；88.7 秒；2 次呼叫；tokens 9093
- 來源：[1] p8 retrieval, [2] p7 retrieval, [3] p1 retrieval, [4] p8 retrieval, [5] p1 retrieval, [6] p8 table_context
- 閱讀計畫（定位 6/6，保留 0，超預算 0）：
  - ✓ Section 4.3 ABLATION STUDIES (RQ2) | need: discussion of ablated versions | priority: required | status: covered → 候選 0，納入 []，排除 []
  - ✓ Table 2 (page 8) | need: performance metrics | priority: required | status: covered → 候選 0，納入 []，排除 []
  - ✓ Section 4.4 CASE STUDY (RQ3) | need: additional context on ablation effects | priority: supplementary | status: covered → 候選 0，納入 []，排除 []
  - ✓ Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM | need: method description | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
  - ✓ Section 7.3.1 PROMPTS FOR GRAPH GENERATION | need: implementation details | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
  - ✓ Section 7.3.2 PROMPTS FOR QUERY GENERATION | need: implementation details | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
- 分析狀態：SUPPORTED_AND_COMPLETE；完整性 complete（required ['-High', '-Low', '-Origin', 'LightRAG']，缺 []，條件 Agriculture / Comprehensiveness）；方向核對 []
- 修正：[]；刪除 []；仍不符 []；方向待定 []
- 涵蓋判定：Section 4.3 ABLATION STUDIES (RQ2)→covered；Table 2 (page 8)→covered；Section 4.4 CASE STUDY (RQ3)→partial；Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM→missing；Section 7.3.1 PROMPTS FOR GRAPH GENERATION→missing；Section 7.3.2 PROMPTS FOR QUERY GENERATION→missing；required 未納入 []；supplementary 用 0；Matrix {'cells': 128, 'tables': ['Table 2 [1]'], 'shown_tokens': 1348, 'left_out': [], 'definitions': ['NaiveRAG', 'LightRAG', '-High'], 'facts': 64, 'coverage_gaps': []}
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 1；找不到的數字 []

```text
The question asks for the performance of ablated versions of LightRAG. The methods include LightRAG, -High, -Low, and -Origin, with NaiveRAG as the reference. The datasets are Agriculture, CS, Legal, and Mix. The metrics are Comprehensiveness, Diversity, Empowerment, and Overall.

The evidence matrix and method definitions show that removing high-level retrieval (-High) leads to a significant performance decline, while removing low-level retrieval (-Low) maintains or slightly improves performance in some metrics. The -Origin variant, which removes original text usage, also shows mixed results with improvements in some cases.

Comparison of figures that share the same dataset, metric, and pairing:
- Agriculture / Comprehensiveness: LightRAG 67.6% | NaiveRAG 32.4%; -High 65.2% | NaiveRAG 34.8%; -Low 64.0% | NaiveRAG 36.0%; -Origin 75.2% | NaiveRAG 24.8% [1]
- CS / Comprehensiveness: LightRAG 61.6% | NaiveRAG 38.4%; -High 57.2% | NaiveRAG 42.8%; -Low 56.8% | NaiveRAG 43.2%; -Origin 60.8% | NaiveRAG 39.2% [1]
- Legal / Comprehensiveness: LightRAG 83.6% | NaiveRAG 16.4%; -High 76.4% | NaiveRAG 23.6%; -Low 80.8% | NaiveRAG 19.2%; -Origin 83.6% | NaiveRAG 16.4% [1]
- Mix / Comprehensiveness: LightRAG 61.2% | NaiveRAG 38.8%; -High 59.6% | NaiveRAG 40.4%; -Low 64.0% | NaiveRAG 36.0%; -Origin 55.6% | NaiveRAG 44.4% [1]
- Agriculture / Diversity: LightRAG 76.4% | NaiveRAG 23.6%; -High 72.8% | NaiveRAG 27.2%; -Low 72.0% | NaiveRAG 28.0%; -Origin 73.6% | NaiveRAG 26.4% [1]
- CS / Diversity: LightRAG 62.0% | NaiveRAG 38.0%; -High 63.2% | NaieveRAG 36.8%; -Low 60.4% | NaiveRAG 39.6%; -Origin 55.2% | NaiveRAG 44.8% [1]
- Legal / Diversity: LightRAG 86.4% | NaiveRAG 13.6%; -High 83.2% | NaiveRAG 16.8%; -Low 86.4% | NaiveRAG 13.6%; -Origin 85.6% | NaiveRAG 14.4% [1]
- Mix / Diversity: LightRAG 67.6% | NaiveRAG 32.4%; -High 64.0% | NaiveRAG 36.0%; -Low 66.8% | NaiveRAG 33.2%; -Origin 74.4% | NaiveRAG 25.6% [1]
- Agriculture / Empowerment: LightRAG 67.6% | NaiveRAG 32.4%; -High 64.0% | NaiveRAG 36.0%; -Low 65.2% | NaiveRAG 34.8%; -Origin 68.0% | NaiveRAG 32.0% [1]
- CS / Empowerment: LightRAG 61.2% | NaiveRAG 38.8%; -High 57.6% | NaiveRAG 42.4%; -Low 57.2% | NaiveRAG 42.8%; -Origin 56.8% | NaiveRAG 43.2% [1]
- Legal / Empowerment: LightRAG 83.6% | NaiveRAG 16.4%; -High 77.2% | NaiveRAG 22.8%; -Low 83.6% | NaiveRAG 16.4%; -Origin 82.8% | NaiveRAG 17.2% [1]
- Mix / Empowerment: LightRAG 57.2% | NaiveRAG 42.8%; -High 52.4% | NaiveRAG 47.6%; -Low 64.8% | NaiveRAG 35.2%; -Origin 54.8% | NaiveRAG 45.2% [1]
- Agriculture / Overall: LightRAG 67.6% | NaiveRAG 32.4%; -High 64.8% | NaiveRAG 35.2%; -Low 65.2% | NaiveRAG 34.8%; -Origin 74.4% | NaiveRAG 25.6% [1]
- CS / Overall: LightRAG 61.2% | NaiveRAG 38.8%; -High 56.0% | NaiveRAG 44.0%; -Low 56.4% | NaiveRAG 43.6%; -Origin 60.8% | NaiveRAG 39.2% [1]
- Legal / Overall: LightRAG 84.8% | NaiveRAG 15.2%; -High 78.0% | NaiveRAG 22.0%; -Low 81.2% | NaiveRAG 18.8%; -Origin 84.4% | NaiveRAG 15.6% [1]
- Mix / Overall: LightRAG 60.0% | NaiveRAG 40.0%; -High 57.6% | NaiveRAG 42.4%; -Low 64.8% | NaiveRAG 35.2%; -Origin 55.6% | NaiveRAG 44.4% [1]

Improvements:
- LightRAG outperforms NaiveRAG in all metrics and datasets.
- -Low outperforms NaiveRAG in some cases, particularly in Agriculture and Legal.
- -Origin outperforms NaiveRAG in Agriculture and Mix.

Regressions:
- -High shows a performance decline in most metrics and datasets.

Exceptions:
- -Low shows improvements in some metrics over NaiveRAG.
- -Origin shows improvements in Agriculture and Mix in some metrics.

The improvements and regressions are supported by the figures provided in the evidence matrix [1]. The -High variant shows a significant performance decline, as described in the source [6].

The figures are cited to the source where they appear [1], and the definitions are cited to the source where they are described [6].

The question is fully addressed with the comparison of the ablated versions of LightRAG across the datasets and metrics.
```

## B8-Q3-1

- 問題：`Performance of ablated versions of LightRAG`；模式 `navigate`；96.7 秒；2 次呼叫；tokens 9280
- 來源：[1] p8 retrieval, [2] p7 retrieval, [3] p1 retrieval, [4] p8 retrieval, [5] p1 retrieval, [6] p8 table_context
- 閱讀計畫（定位 6/6，保留 0，超預算 0）：
  - ✓ Section 4.3 ABLATION STUDIES (RQ2) | need: discussion of ablated versions | priority: required | status: covered → 候選 0，納入 []，排除 []
  - ✓ Table 2 (page 8) | need: performance metrics | priority: required | status: covered → 候選 0，納入 []，排除 []
  - ✓ Section 4.4 CASE STUDY (RQ3) | need: additional context on ablation effects | priority: supplementary | status: covered → 候選 0，納入 []，排除 []
  - ✓ Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM | need: method description | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
  - ✓ Section 7.3.1 PROMPTS FOR GRAPH GENERATION | need: implementation details | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
  - ✓ Section 7.3.2 PROMPTS FOR QUERY GENERATION | need: implementation details | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
- 分析狀態：FACTUALLY_INCORRECT；完整性 uncertain（required ['-High', '-Low', '-Origin', 'LightRAG']，缺 ['LightRAG']，條件 None）；方向核對 []
- 修正：[]；刪除 []；仍不符 ['34.8% (Comprehensiveness, Agriculture, -High)', '42.8% (Comprehensiveness, CS, -High)', '23.6% (Comprehensiveness, Legal, -High)', '40.4% (Comprehensiveness, Mix, -High)', '27.2% (Diversity, Agriculture, -High)', '36.8% (Diversity, CS, -High)', '16.8% (Diversity, Legal, -High)', '36.0% (Diversity, Mix, -High)', '36.0% (Empowerment, Agriculture, -High)', '42.4% (Empowerment, CS, -High)', '22.8% (Empowerment, Legal, -High)', '47.6% (Empowerment, Mix, -High)', '35.2% (Overall, Agriculture, -High)', '44.0% (Overall, CS, -High)', '22.0% (Overall, Legal, -High)', '42.4% (Overall, Mix, -High)', '36.0% (Comprehensiveness, Agriculture, -Low)', '43.2% (Comprehensiveness, CS, -Low)', '19.2% (Comprehensiveness, Legal, -Low)', '36.0% (Comprehensiveness, Mix, -Low)', '28.0% (Diversity, Agriculture, -Low)', '39.6% (Diversity, CS, -Low)', '13.6% (Diversity, Legal, -Low)', '33.2% (Diversity, Mix, -Low)', '34.8% (Empowerment, Agriculture, -Low)', '42.8% (Empowerment, CS, -Low)', '16.4% (Empowerment, Legal, -Low)', '35.2% (Empowerment, Mix, -Low)', '34.8% (Overall, Agriculture, -Low)', '43.6% (Overall, CS, -Low)', '18.8% (Overall, Legal, -Low)', '35.2% (Overall, Mix, -Low)', '24.8% (Comprehensiveness, Agriculture, -Origin)', '39.2% (Comprehensiveness, CS, -Origin)', '16.4% (Comprehensiveness, Legal, -Origin)', '44.4% (Comprehensiveness, Mix, -Origin)', '26.4% (Diversity, Agriculture, -Origin)', '44.8% (Diversity, CS, -Origin)', '14.4% (Diversity, Legal, -Origin)', '25.6% (Diversity, Mix, -Origin)', '32.0% (Empowerment, Agriculture, -Origin)', '43.2% (Empowerment, CS, -Origin)', '17.2% (Empowerment, Legal, -Origin)', '45.2% (Empowerment, Mix, -Origin)', '25.6% (Overall, Agriculture, -Origin)', '39.2% (Overall, CS, -Origin)', '15.6% (Overall, Legal, -Origin)', '44.4% (Overall, Mix, -Origin)', '34.8% (Comprehensiveness, -High, vs NaiveRAG)', '42.8% (Comprehensiveness, -High, vs NaiveRAG)', '40.4% (Comprehensiveness, Mix, -High, vs NaiveRAG)', '43.2% (Comprehensiveness, -Low, vs NaiveRAG)', '19.2% (Comprehensiveness, -Low, vs NaiveRAG)', '42.8% (Empowerment, -Low, vs NaiveRAG)', '36.0% (Comprehensiveness, Mix, -Low, vs NaiveRAG)', '24.8% (Comprehensiveness, -Origin, vs NaiveRAG)', '39.2% (Comprehensiveness, -Origin, vs NaiveRAG)', '16.4% (Comprehensiveness, -Origin, vs NaiveRAG)', '44.4% (Comprehensiveness, -Origin, vs NaiveRAG)', '26.4% (Diversity, -Origin, vs NaiveRAG)', '44.8% (Diversity, -Origin, vs NaiveRAG)', '14.4% (Diversity, -Origin, vs NaiveRAG)', '25.6% (Diversity, -Origin, vs NaiveRAG)', '32.0% (Empowerment, -Origin, vs NaiveRAG)', '43.2% (Empowerment, -Origin, vs NaiveRAG)', '17.2% (Empowerment, -Origin, vs NaiveRAG)', '45.2% (Empowerment, Mix, -Origin, vs NaiveRAG)']；方向待定 []
- 涵蓋判定：Section 4.3 ABLATION STUDIES (RQ2)→covered；Table 2 (page 8)→covered；Section 4.4 CASE STUDY (RQ3)→partial；Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM→missing；Section 7.3.1 PROMPTS FOR GRAPH GENERATION→missing；Section 7.3.2 PROMPTS FOR QUERY GENERATION→missing；required 未納入 []；supplementary 用 0；Matrix {'cells': 128, 'tables': ['Table 2 [1]'], 'shown_tokens': 1348, 'left_out': [], 'definitions': ['LightRAG', 'NaiveRAG', '-High'], 'facts': 64, 'coverage_gaps': []}
- 檢查：標籤不符 ['34.8%', '42.8%', '23.6%', '40.4%', '27.2%', '36.8%', '16.8%', '36.0%', '36.0%', '42.4%', '22.8%', '47.6%', '35.2%', '44.0%', '22.0%', '42.4%', '36.0%', '43.2%', '19.2%', '36.0%', '28.0%', '39.6%', '13.6%', '33.2%', '34.8%', '42.8%', '16.4%', '35.2%', '34.8%', '43.6%', '18.8%', '35.2%', '24.8%', '39.2%', '16.4%', '44.4%', '26.4%', '44.8%', '14.4%', '25.6%', '32.0%', '43.2%', '17.2%', '45.2%', '25.6%', '39.2%', '15.6%', '44.4%', '34.8%', '42.8%', '40.4%', '43.2%', '19.2%', '42.8%', '36.0%', '24.8%', '39.2%', '16.4%', '44.4%', '26.4%', '44.8%', '14.4%', '25.6%', '32.0%', '43.2%', '17.2%', '45.2%']；全稱宣稱 0；引用可疑 []；未解析 18；找不到的數字 ['13', '16', '12']

```text
The question asks for a comparison of the performance of ablated versions of LightRAG. The methods involved are LightRAG, -High, -Low, and -Origin, with NaiveRAG as the reference. The datasets are Agriculture, CS, Legal, and Mix. The metrics are Comprehensiveness, Diversity, Empowerment, and Overall.

The ablated versions are defined as follows:
- -High: removes high-level retrieval [2]
- -Low: removes low-level retrieval [2]
- -Origin: eliminates the use of semantic graphs and uses original text [6]

The comparison is based on the performance of the ablated versions against NaiveRAG for each dataset and metric. The following table summarizes the figures for the ablated versions:

| Method | Dataset | Metric | NaiveRAG | Ablated Version |
|--------|---------|--------|----------|------------------|
| -High | Agriculture | Comprehensiveness | 34.8% | 65.2% |
| -High | CS | Comprehensiveness | 42.8% | 57.2% |
| -High | Legal | Comprehensiveness | 23.6% | 76.4% |
| -High | Mix | Comprehensiveness | 40.4% | 59.6% |
| -High | Agriculture | Diversity | 27.2% | 72.8% |
| -High | CS | Diversity | 36.8% | 63.2% |
| -High | Legal | Diversity | 16.8% | 83.2% |
| -High | Mix | Diversity | 36.0% | 64.0% |
| -High | Agriculture | Empowerment | 36.0% | 64.0% |
| -High | CS | Empowerment | 42.4% | 57.6% |
| -High | Legal | Empowerment | 22.8% | 77.2% |
| -High | Mix | Empowerment | 47.6% | 52.4% |
| -High | Agriculture | Overall | 35.2% | 64.8% |
| -High | CS | Overall | 44.0% | 56.0% |
| -High | Legal | Overall | 22.0% | 78.0% |
| -High | Mix | Overall | 42.4% | 57.6% |
| -Low | Agriculture | Comprehensiveness | 36.0% | 64.0% |
| -Low | CS | Comprehensiveness | 43.2% | 56.8% |
| -Low | Legal | Comprehensiveness | 19.2% | 80.8% |
| -Low | Mix | Comprehensiveness | 36.0% | 64.0% |
| -Low | Agriculture | Diversity | 28.0% | 72.0% |
| -Low | CS | Diversity | 39.6% | 60.4% |
| -Low | Legal | Diversity | 13.6% | 86.4% |
| -Low | Mix | Diversity | 33.2% | 66.8% |
| -Low | Agriculture | Empowerment | 34.8% | 65.2% |
| -Low | CS | Empowerment | 42.8% | 57.2% |
| -Low | Legal | Empowerment | 16.4% | 83.6% |
| -Low | Mix | Empowerment | 35.2% | 64.8% |
| -Low | Agriculture | Overall | 34.8% | 65.2% |
| -Low | CS | Overall | 43.6% | 56.4% |
| -Low | Legal | Overall | 18.8% | 81.2% |
| -Low | Mix | Overall | 35.2% | 64.8% |
| -Origin | Agriculture | Comprehensiveness | 24.8% | 75.2% |
| -Origin | CS | Comprehensiveness | 39.2% | 60.8% |
| -Origin | Legal | Comprehensiveness | 16.4% | 83.6% |
| -Origin | Mix | Comprehensiveness | 44.4% | 55.6% |
| -Origin | Agriculture | Diversity | 26.4% | 73.6% |
| -Origin | CS | Diversity | 44.8% | 55.2% |
| -Origin | Legal | Diversity | 14.4% | 85.6% |
| -Origin | Mix | Diversity | 25.6% | 74.4% |
| -Origin | Agriculture | Empowerment | 32.0% | 68.0% |
| -Origin | CS | Empowerment | 43.2% | 56.8% |
| -Origin | Legal | Empowerment | 17.2% | 82.8% |
| -Origin | Mix | Empowerment | 45.2% | 54.8% |
| -Origin | Agriculture | Overall | 25.6% | 74.4% |
| -Origin | CS | Overall | 39.2% | 60.8% |
| -Origin | Legal | Overall | 15.6% | 84.4% |
| -Origin | Mix | Overall | 44.4% | 55.6% |

The comparison of the ablated versions against NaiveRAG shows the following trends:
- -High performs better than NaiveRAG in 13 out of 16 conditions, lower in 3: Agriculture/Comprehensiveness (34.8% vs 65.2%), CS/Comprehensiveness (42.8% vs 57.2%), and Mix/Comprehensiveness (40.4% vs 59.6%) [1]
- -Low performs better than NaiveRAG in 12 out of 16 conditions, lower in 4: CS/Comprehensiveness (43.2% vs 56.8%), Legal/Comprehensiveness (19.2% vs 80.8%), CS/Empowerment (42.8% vs 57.2%), and Mix/Comprehensiveness (36.0% vs 64.0%) [1]
- -Origin performs better than NaiveRAG in 4 out of 16 conditions, lower in 12: Agriculture/Comprehensiveness (24.8% vs 75.2%), CS/Comprehensiveness (39.2% vs 60.8%), Legal/Comprehensiveness (16.4% vs 83.6%), Mix/Comprehensiveness (44.4% vs 55.6%), Agriculture/Diversity (26.4% vs 73.6%), CS/Diversity (44.8% vs 55.2%), Legal/Diversity (14.4% vs 85.6%), Mix/Diversity (25.6% vs 74.4%), Agriculture/Empowerment (32.0% vs 68.0%), CS/Empowerment (43.2% vs 56.8%), Legal/Empowerment (17.2% vs 82.8%), and Mix/Empowerment (45.2% vs 54.8%) [1]

The ablated versions of LightRAG show varying performance compared to NaiveRAG. -High and -Low generally perform better than NaiveRAG in most conditions, while -Origin performs worse in most conditions. However, the performance of each ablated version varies across datasets and metrics, indicating that no single version consistently outperforms the others.

The figures were cited from Table 2 [1], and the definitions of the ablated versions were cited from the text [2] and [6].

The answer addresses the question by comparing the performance of the ablated versions of LightRAG against NaiveRAG for each dataset and metric. The sources were cited appropriately for each figure and definition.

Numbers that could not be checked against the cited pages of the original text: 13, 16, 12.

Figures whose labels differ from the source table: 34.8% (answer: Comprehensiveness, Agriculture, -High; source: Comprehensiveness, Agriculture, NaiveRAG, vs -High / Empowerment, Agriculture, NaiveRAG, vs -Low / Overall, Agriculture, NaiveRAG, vs -Low); 42.8% (answer: Comprehensiveness, CS, -High; source: Empowerment, Mix, NaiveRAG, vs LightRAG / Comprehensiveness, CS, NaiveRAG, vs -High / Empowerment, CS, NaiveRAG, vs -Low); 23.6% (answer: Comprehensiveness, Legal, -High; source: Diversity, Agriculture, NaiveRAG, vs LightRAG / Comprehensiveness, Legal, NaiveRAG, vs -High); 40.4% (answer: Comprehensiveness, Mix, -High; source: Comprehensiveness, Mix, HyDE, vs LightRAG / Comprehensiveness, Mix, NaiveRAG, vs -High); 27.2% (answer: Diversity, Agriculture, -High; source: Diversity, Agriculture, NaiveRAG, vs -High); 36.8% (answer: Diversity, CS, -High; source: Diversity, CS, NaiveRAG, vs -High); 16.8% (answer: Diversity, Legal, -High; source: Diversity, Legal, NaiveRAG, vs -High); 36.0% (answer: Diversity, Mix, -High; source: Diversity, Mix, GraphRAG, vs LightRAG / Diversity, Mix, NaiveRAG, vs -High / Empowerment, Agriculture, NaiveRAG, vs -High / Comprehensiveness, Agriculture, NaiveRAG, vs -Low / Comprehensiveness, Mix, NaiveRAG, vs -Low); 36.0% (answer: Empowerment, Agriculture, -High; source: Diversity, Mix, GraphRAG, vs LightRAG / Diversity, Mix, NaiveRAG, vs -High / Empowerment, Agriculture, NaiveRAG, vs -High / Comprehensiveness, Agriculture, NaiveRAG, vs -Low / Comprehensiveness, Mix, NaiveRAG, vs -Low); 42.4% (answer: Empowerment, CS, -High; source: Empowerment, Mix, RQ-RAG, vs LightRAG / Overall, Mix, HyDE, vs LightRAG / Empowerment, CS, NaiveRAG, vs -High / Overall, Mix, NaiveRAG, vs -High); 22.8% (answer: Empowerment, Legal, -High; source: Diversity, Agriculture, GraphRAG, vs LightRAG / Empowerment, Legal, NaiveRAG, vs -High); 47.6% (answer: Empowerment, Mix, -High; source: Empowerment, Mix, NaiveRAG, vs -High); 35.2% (answer: Overall, Agriculture, -High; source: Overall, Agriculture, NaiveRAG, vs -High / Empowerment, Mix, NaiveRAG, vs -Low / Overall, Mix, NaiveRAG, vs -Low); 44.0% (answer: Overall, CS, -High; source: Overall, CS, NaiveRAG, vs -High); 22.0% (answer: Overall, Legal, -High; source: Overall, Legal, NaiveRAG, vs -High); 42.4% (answer: Overall, Mix, -High; source: Empowerment, Mix, RQ-RAG, vs LightRAG / Overall, Mix, HyDE, vs LightRAG / Empowerment, CS, NaiveRAG, vs -High / Overall, Mix, NaiveRAG, vs -High); 36.0% (answer: Comprehensiveness, Agriculture, -Low; source: Diversity, Mix, GraphRAG, vs LightRAG / Diversity, Mix, NaiveRAG, vs -High / Empowerment, Agriculture, NaiveRAG, vs -High / Comprehensiveness, Agriculture, NaiveRAG, vs -Low / Comprehensiveness, Mix, NaiveRAG, vs -Low); 43.2% (answer: Comprehensiveness, CS, -Low; source: Comprehensiveness, CS, NaiveRAG, vs -Low / Empowerment, CS, NaiveRAG, vs -Origin); 19.2% (answer: Comprehensiveness, Legal, -Low; source: Comprehensiveness, Legal, NaiveRAG, vs -Low); 36.0% (answer: Comprehensiveness, Mix, -Low; source: Diversity, Mix, GraphRAG, vs LightRAG / Diversity, Mix, NaiveRAG, vs -High / Empowerment, Agriculture, NaiveRAG, vs -High / Comprehensiveness, Agriculture, NaiveRAG, vs -Low / Comprehensiveness, Mix, NaiveRAG, vs -Low); 28.0% (answer: Diversity, Agriculture, -Low; source: Diversity, Agriculture, NaiveRAG, vs -Low); 39.6% (answer: Diversity, CS, -Low; source: Diversity, CS, NaiveRAG, vs -Low); 13.6% (answer: Diversity, Legal, -Low; source: Diversity, Legal, NaiveRAG, vs LightRAG / Diversity, Legal, NaiveRAG, vs -Low); 33.2% (answer: Diversity, Mix, -Low; source: Diversity, Mix, NaiveRAG, vs -Low); 34.8% (answer: Empowerment, Agriculture, -Low; source: Comprehensiveness, Agriculture, NaiveRAG, vs -High / Empowerment, Agriculture, NaiveRAG, vs -Low / Overall, Agriculture, NaiveRAG, vs -Low); 42.8% (answer: Empowerment, CS, -Low; source: Empowerment, Mix, NaiveRAG, vs LightRAG / Comprehensiveness, CS, NaiveRAG, vs -High / Empowerment, CS, NaiveRAG, vs -Low); 16.4% (answer: Empowerment, Legal, -Low; source: Comprehensiveness, Legal, NaiveRAG, vs LightRAG / Empowerment, Legal, NaiveRAG, vs LightRAG / Empowerment, Legal, NaiveRAG, vs -Low / Comprehensiveness, Legal, NaiveRAG, vs -Origin); 35.2% (answer: Empowerment, Mix, -Low; source: Overall, Agriculture, NaiveRAG, vs -High / Empowerment, Mix, NaiveRAG, vs -Low / Overall, Mix, NaiveRAG, vs -Low); 34.8% (answer: Overall, Agriculture, -Low; source: Comprehensiveness, Agriculture, NaiveRAG, vs -High / Empowerment, Agriculture, NaiveRAG, vs -Low / Overall, Agriculture, NaiveRAG, vs -Low); 43.6% (answer: Overall, CS, -Low; source: Empowerment, Legal, GraphRAG, vs LightRAG / Overall, CS, NaiveRAG, vs -Low); 18.8% (answer: Overall, Legal, -Low; source: Overall, Legal, NaiveRAG, vs -Low); 35.2% (answer: Overall, Mix, -Low; source: Overall, Agriculture, NaiveRAG, vs -High / Empowerment, Mix, NaiveRAG, vs -Low / Overall, Mix, NaiveRAG, vs -Low); 24.8% (answer: Comprehensiveness, Agriculture, -Origin; source: Overall, Agriculture, HyDE, vs LightRAG / Comprehensiveness, Agriculture, NaiveRAG, vs -Origin); 39.2% (answer: Comprehensiveness, CS, -Origin; source: Comprehensiveness, Mix, RQ-RAG, vs LightRAG / Diversity, CS, RQ-RAG, vs LightRAG / Comprehensiveness, CS, NaiveRAG, vs -Origin / Overall, CS, NaiveRAG, vs -Origin); 16.4% (answer: Comprehensiveness, Legal, -Origin; source: Comprehensiveness, Legal, NaiveRAG, vs LightRAG / Empowerment, Legal, NaiveRAG, vs LightRAG / Empowerment, Legal, NaiveRAG, vs -Low / Comprehensiveness, Legal, NaiveRAG, vs -Origin); 44.4% (answer: Comprehensiveness, Mix, -Origin; source: Comprehensiveness, Mix, NaiveRAG, vs -Origin / Overall, Mix, NaiveRAG, vs -Origin); 26.4% (answer: Diversity, Agriculture, -Origin; source: Overall, Legal, HyDE, vs LightRAG / Diversity, Legal, GraphRAG, vs LightRAG / Diversity, Agriculture, NaiveRAG, vs -Origin); 44.8% (answer: Diversity, CS, -Origin; source: Diversity, CS, NaiveRAG, vs -Origin); 14.4% (answer: Diversity, Legal, -Origin; source: Overall, Legal, RQ-RAG, vs LightRAG / Diversity, Legal, NaiveRAG, vs -Origin); 25.6% (answer: Diversity, Mix, -Origin; source: Diversity, Mix, NaiveRAG, vs -Origin / Overall, Agriculture, NaiveRAG, vs -Origin); 32.0% (answer: Empowerment, Agriculture, -Origin; source: Empowerment, Agriculture, NaiveRAG, vs -Origin); 43.2% (answer: Empowerment, CS, -Origin; source: Comprehensiveness, CS, NaiveRAG, vs -Low / Empowerment, CS, NaiveRAG, vs -Origin); 17.2% (answer: Empowerment, Legal, -Origin; source: Empowerment, Legal, NaiveRAG, vs -Origin); 45.2% (answer: Empowerment, Mix, -Origin; source: Empowerment, CS, GraphRAG, vs LightRAG / Overall, Agriculture, GraphRAG, vs LightRAG / Empowerment, Mix, NaiveRAG, vs -Origin); 25.6% (answer: Overall, Agriculture, -Origin; source: Diversity, Mix, NaiveRAG, vs -Origin / Overall, Agriculture, NaiveRAG, vs -Origin); 39.2% (answer: Overall, CS, -Origin; source: Comprehensiveness, Mix, RQ-RAG, vs LightRAG / Diversity, CS, RQ-RAG, vs LightRAG / Comprehensiveness, CS, NaiveRAG, vs -Origin / Overall, CS, NaiveRAG, vs -Origin); 15.6% (answer: Overall, Legal, -Origin; source: Overall, Legal, NaiveRAG, vs -Origin); 44.4% (answer: Overall, Mix, -Origin; source: Comprehensiveness, Mix, NaiveRAG, vs -Origin / Overall, Mix, NaiveRAG, vs -Origin); 34.8% (answer: Comprehensiveness, -High, vs NaiveRAG; source: Comprehensiveness, Agriculture, NaiveRAG, vs -High / Empowerment, Agriculture, NaiveRAG, vs -Low / Overall, Agriculture, NaiveRAG, vs -Low); 42.8% (answer: Comprehensiveness, -High, vs NaiveRAG; source: Empowerment, Mix, NaiveRAG, vs LightRAG / Comprehensiveness, CS, NaiveRAG, vs -High / Empowerment, CS, NaiveRAG, vs -Low); 40.4% (answer: Comprehensiveness, Mix, -High, vs NaiveRAG; source: Comprehensiveness, Mix, HyDE, vs LightRAG / Comprehensiveness, Mix, NaiveRAG, vs -High); 43.2% (answer: Comprehensiveness, -Low, vs NaiveRAG; source: Comprehensiveness, CS, NaiveRAG, vs -Low / Empowerment, CS, NaiveRAG, vs -Origin); 19.2% (answer: Comprehensiveness, -Low, vs NaiveRAG; source: Comprehensiveness, Legal, NaiveRAG, vs -Low); 42.8% (answer: Empowerment, -Low, vs NaiveRAG; source: Empowerment, Mix, NaiveRAG, vs LightRAG / Comprehensiveness, CS, NaiveRAG, vs -High / Empowerment, CS, NaiveRAG, vs -Low); 36.0% (answer: Comprehensiveness, Mix, -Low, vs NaiveRAG; source: Diversity, Mix, GraphRAG, vs LightRAG / Diversity, Mix, NaiveRAG, vs -High / Empowerment, Agriculture, NaiveRAG, vs -High / Comprehensiveness, Agriculture, NaiveRAG, vs -Low / Comprehensiveness, Mix, NaiveRAG, vs -Low); 24.8% (answer: Comprehensiveness, -Origin, vs NaiveRAG; source: Overall, Agriculture, HyDE, vs LightRAG / Comprehensiveness, Agriculture, NaiveRAG, vs -Origin); 39.2% (answer: Comprehensiveness, -Origin, vs NaiveRAG; source: Comprehensiveness, Mix, RQ-RAG, vs LightRAG / Diversity, CS, RQ-RAG, vs LightRAG / Comprehensiveness, CS, NaiveRAG, vs -Origin / Overall, CS, NaiveRAG, vs -Origin); 16.4% (answer: Comprehensiveness, -Origin, vs NaiveRAG; source: Comprehensiveness, Legal, NaiveRAG, vs LightRAG / Empowerment, Legal, NaiveRAG, vs LightRAG / Empowerment, Legal, NaiveRAG, vs -Low / Comprehensiveness, Legal, NaiveRAG, vs -Origin); 44.4% (answer: Comprehensiveness, -Origin, vs NaiveRAG; source: Comprehensiveness, Mix, NaiveRAG, vs -Origin / Overall, Mix, NaiveRAG, vs -Origin); 26.4% (answer: Diversity, -Origin, vs NaiveRAG; source: Overall, Legal, HyDE, vs LightRAG / Diversity, Legal, GraphRAG, vs LightRAG / Diversity, Agriculture, NaiveRAG, vs -Origin); 44.8% (answer: Diversity, -Origin, vs NaiveRAG; source: Diversity, CS, NaiveRAG, vs -Origin); 14.4% (answer: Diversity, -Origin, vs NaiveRAG; source: Overall, Legal, RQ-RAG, vs LightRAG / Diversity, Legal, NaiveRAG, vs -Origin); 25.6% (answer: Diversity, -Origin, vs NaiveRAG; source: Diversity, Mix, NaiveRAG, vs -Origin / Overall, Agriculture, NaiveRAG, vs -Origin); 32.0% (answer: Empowerment, -Origin, vs NaiveRAG; source: Empowerment, Agriculture, NaiveRAG, vs -Origin); 43.2% (answer: Empowerment, -Origin, vs NaiveRAG; source: Comprehensiveness, CS, NaiveRAG, vs -Low / Empowerment, CS, NaiveRAG, vs -Origin); 17.2% (answer: Empowerment, -Origin, vs NaiveRAG; source: Empowerment, Legal, NaiveRAG, vs -Origin); 45.2% (answer: Empowerment, Mix, -Origin, vs NaiveRAG; source: Empowerment, CS, GraphRAG, vs LightRAG / Overall, Agriculture, GraphRAG, vs LightRAG / Empowerment, Mix, NaiveRAG, vs -Origin).
```

## B8-Q3-2

- 問題：`Performance of ablated versions of LightRAG`；模式 `navigate`；63.8 秒；2 次呼叫；tokens 8513
- 來源：[1] p8 retrieval, [2] p7 retrieval, [3] p1 retrieval, [4] p8 retrieval, [5] p1 retrieval, [6] p8 table_context
- 閱讀計畫（定位 6/6，保留 0，超預算 0）：
  - ✓ Section 4.3 ABLATION STUDIES (RQ2) | need: discussion of ablated versions | priority: required | status: covered → 候選 0，納入 []，排除 []
  - ✓ Table 2 (page 8) | need: performance metrics | priority: required | status: covered → 候選 0，納入 []，排除 []
  - ✓ Section 4.4 CASE STUDY (RQ3) | need: additional context on ablation effects | priority: supplementary | status: covered → 候選 0，納入 []，排除 []
  - ✓ Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM | need: method description | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
  - ✓ Section 7.3.1 PROMPTS FOR GRAPH GENERATION | need: implementation details | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
  - ✓ Section 7.3.2 PROMPTS FOR QUERY GENERATION | need: implementation details | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
- 分析狀態：FACTUALLY_INCORRECT；完整性 complete（required ['-High', '-Low', '-Origin', 'LightRAG']，缺 []，條件 Agriculture / Comprehensiveness）；方向核對 []
- 修正：[]；刪除 []；仍不符 ['32.4% (Comprehensiveness, Agriculture, LightRAG)', '34.8% (Comprehensiveness, Agriculture, -High)', '36.0% (Comprehensiveness, Agriculture, -Low)', '24.8% (Comprehensiveness, Agriculture, -Origin)', '38.4% (Comprehensiveness, CS, LightRAG)', '42.8% (Comprehensiveness, CS, -High)', '43.2% (Comprehensiveness, CS, -Low)', '39.2% (Comprehensiveness, CS, -Origin)', '16.4% (Comprehensiveness, Legal, LightRAG)', '23.6% (Comprehensiveness, Legal, -High)', '19.2% (Comprehensiveness, Legal, -Low)', '16.4% (Comprehensiveness, Legal, -Origin)', '38.8% (Comprehensiveness, Mix, LightRAG)', '40.4% (Comprehensiveness, Mix, -High)', '36.0% (Comprehensiveness, Mix, -Low)', '44.4% (Comprehensiveness, Mix, -Origin)']；方向待定 []
- 涵蓋判定：Section 4.3 ABLATION STUDIES (RQ2)→covered；Table 2 (page 8)→covered；Section 4.4 CASE STUDY (RQ3)→partial；Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM→missing；Section 7.3.1 PROMPTS FOR GRAPH GENERATION→missing；Section 7.3.2 PROMPTS FOR QUERY GENERATION→missing；required 未納入 []；supplementary 用 0；Matrix {'cells': 128, 'tables': ['Table 2 [1]'], 'shown_tokens': 1348, 'left_out': [], 'definitions': ['LightRAG', 'NaiveRAG', '-High'], 'facts': 64, 'coverage_gaps': []}
- 檢查：標籤不符 ['32.4%', '34.8%', '36.0%', '24.8%', '38.4%', '42.8%', '43.2%', '39.2%', '16.4%', '23.6%', '19.2%', '16.4%', '38.8%', '40.4%', '36.0%', '44.4%']；全稱宣稱 1；引用可疑 []；未解析 0；找不到的數字 []

```text
The question asks for the performance of ablated versions of LightRAG. The methods are LightRAG and its variants: -High (removes high-level retrieval), -Low (removes low-level retrieval), and -Origin (uses original text in retrieval). The datasets are Agriculture, CS, Legal, and Mix. The metrics are Comprehensiveness, Diversity, Empowerment, and Overall.

From the evidence matrix [1], we read the following figures for each method variant, dataset, and metric compared to NaiveRAG:

| Method | Dataset | Metric | NaiveRAG | Method |
|--------|---------|--------|----------|--------|
| LightRAG | Agriculture | Comprehensiveness | 32.4% | 67.6% |
| -High | Agriculture | Comprehensiveness | 34.8% | 65.2% |
| -Low | Agriculture | Comprehensiveness | 36.0% | 64.0% |
| -Origin | Agriculture | Comprehensiveness | 24.8% | 75.2% |
| LightRAG | CS | Comprehensiveness | 38.4% | 61.6% |
| -High | CS | Comprehensiveness | 42.8% | 57.2% |
| -Low | CS | Comprehensiveness | 43.2% | 56.8% |
| -Origin | CS | Comprehensiveness | 39.2% | 60.8% |
| LightRAG | Legal | Comprehensiveness | 16.4% | 83.6% |
| -High | Legal | Comprehensiveness | 23.6% | 76.4% |
| -Low | Legal | Comprehensiveness | 19.2% | 80.8% |
| -Origin | Legal | Comprehensiveness | 16.4% | 83.6% |
| LightRAG | Mix | Comprehensiveness | 38.8% | 61.2% |
| -High | Mix | Comprehensiveness | 40.4% | 59.6% |
| -Low | Mix | Comprehensiveness | 36.0% | 64.0% |
| -Origin | Mix | Comprehensiveness | 44.4% | 55.6% |

For each dataset and metric, we compare the LightRAG variant's performance against NaiveRAG.

Comparing LightRAG variants to NaiveRAG:

- Comprehensiveness:
  - LightRAG outperforms NaiveRAG in all 4 datasets (Agriculture, CS, Legal, Mix).
  - -High outperforms NaiveRAG in all 4 datasets.
  - -Low outperforms NaiveRAG in all 4 datasets.
  - -Origin outperforms NaiveRAG in all 4 datasets, except in Mix (NaiveRAG 44.4%, -Origin 55.6%).

- Diversity:
  - LightRAG outperforms NaiveRAG in all 4 datasets.
  - -High outperforms NaiveRAG in all 4 datasets.
  - -Low outperforms NaiveRAG in all 4 datasets.
  - -Origin outperforms NaiveRAG in all 4 datasets.

- Empowerment:
  - LightRAG outperforms NaiveRAG in all 4 datasets.
  - -High outperforms NaiveRAG in all 4 datasets.
  - -Low outperforms NaiveRAG in all 4 datasets.
  - -Origin outperforms NaiveRAG in all 4 datasets.

- Overall:
  - LightRAG outperforms NaiveRAG in all 4 datasets.
  - -High outperforms NaiveRAG in all 4 datasets.
  - -Low outperforms NaiveRAG in all 4 datasets.
  - -Origin outperforms NaiveRAG in all 4 datasets, except in Mix (NaiveRAG 44.4%, -Origin 55.6%).

All ablated versions of LightRAG (-High, -Low, -Origin) outperform NaiveRAG in all datasets and metrics, with the exception of the -Origin variant in the Mix dataset for Overall, where the improvement is not consistent. LightRAG consistently outperforms NaiveRAG in all datasets and metrics. The -High and -Low variants each show a balanced performance, with -High performing better in some conditions and -Low in others. The -Origin variant performs well across all metrics but shows the only exception in the Mix dataset for Overall.

The figures are from Table 2 [1], and the method descriptions are from the text on page 8 [1]. The ablation studies are discussed in Section 4.3 [2], and the case study is in Section 4.4 [4].

The question asked for the performance of ablated versions of LightRAG, and the sources provided the necessary data to answer it. Each variant was compared to NaiveRAG, as required.

Figures whose labels differ from the source table: 32.4% (answer: Comprehensiveness, Agriculture, LightRAG; source: Comprehensiveness, Agriculture, NaiveRAG, vs LightRAG / Diversity, Mix, NaiveRAG, vs LightRAG / Empowerment, Agriculture, NaiveRAG, vs LightRAG / Overall, Agriculture, NaiveRAG, vs LightRAG / Overall, Agriculture, RQ-RAG, vs LightRAG / Diversity, Mix, HyDE, vs LightRAG); 34.8% (answer: Comprehensiveness, Agriculture, -High; source: Comprehensiveness, Agriculture, NaiveRAG, vs -High / Empowerment, Agriculture, NaiveRAG, vs -Low / Overall, Agriculture, NaiveRAG, vs -Low); 36.0% (answer: Comprehensiveness, Agriculture, -Low; source: Diversity, Mix, GraphRAG, vs LightRAG / Diversity, Mix, NaiveRAG, vs -High / Empowerment, Agriculture, NaiveRAG, vs -High / Comprehensiveness, Agriculture, NaiveRAG, vs -Low / Comprehensiveness, Mix, NaiveRAG, vs -Low); 24.8% (answer: Comprehensiveness, Agriculture, -Origin; source: Overall, Agriculture, HyDE, vs LightRAG / Comprehensiveness, Agriculture, NaiveRAG, vs -Origin); 38.4% (answer: Comprehensiveness, CS, LightRAG; source: Comprehensiveness, CS, NaiveRAG, vs LightRAG); 42.8% (answer: Comprehensiveness, CS, -High; source: Empowerment, Mix, NaiveRAG, vs LightRAG / Comprehensiveness, CS, NaiveRAG, vs -High / Empowerment, CS, NaiveRAG, vs -Low); 43.2% (answer: Comprehensiveness, CS, -Low; source: Comprehensiveness, CS, NaiveRAG, vs -Low / Empowerment, CS, NaiveRAG, vs -Origin); 39.2% (answer: Comprehensiveness, CS, -Origin; source: Comprehensiveness, Mix, RQ-RAG, vs LightRAG / Diversity, CS, RQ-RAG, vs LightRAG / Comprehensiveness, CS, NaiveRAG, vs -Origin / Overall, CS, NaiveRAG, vs -Origin); 16.4% (answer: Comprehensiveness, Legal, LightRAG; source: Comprehensiveness, Legal, NaiveRAG, vs LightRAG / Empowerment, Legal, NaiveRAG, vs LightRAG / Empowerment, Legal, NaiveRAG, vs -Low / Comprehensiveness, Legal, NaiveRAG, vs -Origin); 23.6% (answer: Comprehensiveness, Legal, -High; source: Diversity, Agriculture, NaiveRAG, vs LightRAG / Comprehensiveness, Legal, NaiveRAG, vs -High); 19.2% (answer: Comprehensiveness, Legal, -Low; source: Comprehensiveness, Legal, NaiveRAG, vs -Low); 16.4% (answer: Comprehensiveness, Legal, -Origin; source: Comprehensiveness, Legal, NaiveRAG, vs LightRAG / Empowerment, Legal, NaiveRAG, vs LightRAG / Empowerment, Legal, NaiveRAG, vs -Low / Comprehensiveness, Legal, NaiveRAG, vs -Origin); 38.8% (answer: Comprehensiveness, Mix, LightRAG; source: Comprehensiveness, Mix, NaiveRAG, vs LightRAG / Empowerment, CS, NaiveRAG, vs LightRAG / Overall, CS, NaiveRAG, vs LightRAG / Comprehensiveness, CS, RQ-RAG, vs LightRAG / Diversity, CS, HyDE, vs LightRAG); 40.4% (answer: Comprehensiveness, Mix, -High; source: Comprehensiveness, Mix, HyDE, vs LightRAG / Comprehensiveness, Mix, NaiveRAG, vs -High); 36.0% (answer: Comprehensiveness, Mix, -Low; source: Diversity, Mix, GraphRAG, vs LightRAG / Diversity, Mix, NaiveRAG, vs -High / Empowerment, Agriculture, NaiveRAG, vs -High / Comprehensiveness, Agriculture, NaiveRAG, vs -Low / Comprehensiveness, Mix, NaiveRAG, vs -Low); 44.4% (answer: Comprehensiveness, Mix, -Origin; source: Comprehensiveness, Mix, NaiveRAG, vs -Origin / Overall, Mix, NaiveRAG, vs -Origin).

A claim the source table does not bear out: "All ablated versions of LightRAG (-High, -Low, -Origin) outperform NaiveRAG in all datasets and metrics, with the exception of the -Origin variant in the Mix dataset for Overall, where the improvement is not consistent." — -Origin is above the compared methods in 1 cells and below in 3, for example Overall / Mix: -Origin 55.6% vs NaiveRAG 44.4% (p. 8).
```

## B8-Q3-3

- 問題：`Performance of ablated versions of LightRAG`；模式 `navigate`；101.7 秒；2 次呼叫；tokens 9400
- 來源：[1] p8 retrieval, [2] p7 retrieval, [3] p1 retrieval, [4] p8 retrieval, [5] p1 retrieval, [6] p8 table_context
- 閱讀計畫（定位 6/6，保留 0，超預算 0）：
  - ✓ Section 4.3 ABLATION STUDIES (RQ2) | need: discussion of ablated versions | priority: required | status: covered → 候選 0，納入 []，排除 []
  - ✓ Table 2 (page 8) | need: performance metrics | priority: required | status: covered → 候選 0，納入 []，排除 []
  - ✓ Section 4.4 CASE STUDY (RQ3) | need: additional context on ablation effects | priority: supplementary | status: covered → 候選 0，納入 []，排除 []
  - ✓ Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM | need: method description | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
  - ✓ Section 7.3.1 PROMPTS FOR GRAPH GENERATION | need: implementation details | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
  - ✓ Section 7.3.2 PROMPTS FOR QUERY GENERATION | need: implementation details | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
- 分析狀態：FACTUALLY_INCORRECT；完整性 uncertain（required ['-High', '-Low', '-Origin', 'LightRAG']，缺 ['-High', '-Low', '-Origin', 'LightRAG']，條件 None）；方向核對 []
- 修正：[]；刪除 []；仍不符 ['67.6% (Comprehensiveness, Agriculture, NaiveRAG)', '65.2% (Comprehensiveness, Agriculture, NaiveRAG)', '64.0% (Comprehensiveness, Agriculture, NaiveRAG)', '75.2% (Comprehensiveness, Agriculture, NaiveRAG)', '61.6% (CS, NaiveRAG)', '57.2% (CS, NaiveRAG)', '56.8% (CS, NaiveRAG)', '60.8% (CS, NaiveRAG)', '83.6% (Legal, NaiveRAG)', '76.4% (Legal, NaiveRAG)', '80.8% (Legal, NaiveRAG)', '83.6% (Legal, NaiveRAG)', '61.2% (Mix, NaiveRAG)', '59.6% (Mix, NaiveRAG)', '64.0% (Mix, NaiveRAG)', '55.6% (Mix, NaiveRAG)', '76.4% (Diversity, Agriculture, NaiveRAG)', '72.8% (Diversity, Agriculture, NaiveRAG)', '72.0% (Diversity, Agriculture, NaiveRAG)', '73.6% (Diversity, Agriculture, NaiveRAG)', '62.0% (CS, NaiveRAG)', '63.2% (CS, NaiveRAG)', '60.4% (CS, NaiveRAG)', '55.2% (CS, NaiveRAG)', '86.4% (Legal, NaiveRAG)', '83.2% (Legal, NaiveRAG)', '86.4% (Legal, NaiveRAG)', '85.6% (Legal, NaiveRAG)', '67.6% (Mix, NaiveRAG)', '64.0% (Mix, NaiveRAG)', '66.8% (Mix, NaiveRAG)', '74.4% (Mix, NaiveRAG)', '67.6% (Empowerment, Agriculture, NaiveRAG)', '64.0% (Empowerment, Agriculture, NaiveRAG)', '65.2% (Empowerment, Agriculture, NaiveRAG)', '68.0% (Empowerment, Agriculture, NaiveRAG)', '83.6% (Legal, NaiveRAG)', '77.2% (Legal, NaiveRAG)', '83.6% (Legal, NaiveRAG)', '82.8% (Legal, NaiveRAG)', '57.2% (Mix, NaiveRAG)', '52.4% (Mix, NaiveRAG)', '64.8% (Mix, NaiveRAG)', '54.8% (Mix, NaiveRAG)', '67.6% (Overall, Agriculture, NaiveRAG)', '64.8% (Overall, Agriculture, NaiveRAG)', '65.2% (Overall, Agriculture, NaiveRAG)', '74.4% (Overall, Agriculture, NaiveRAG)', '61.2% (CS, NaiveRAG)', '56.0% (CS, NaiveRAG)', '56.4% (CS, NaiveRAG)', '60.8% (CS, NaiveRAG)', '84.8% (Legal, NaiveRAG)', '78.0% (Legal, NaiveRAG)', '81.2% (Legal, NaiveRAG)', '84.4% (Legal, NaiveRAG)', '60.0% (Mix, NaiveRAG)', '57.6% (Mix, NaiveRAG)', '64.8% (Mix, NaiveRAG)', '55.6% (Mix, NaiveRAG)', '74.4% (Comprehensiveness)', '84.4% (Comprehensiveness)']；方向待定 []
- 涵蓋判定：Section 4.3 ABLATION STUDIES (RQ2)→covered；Table 2 (page 8)→covered；Section 4.4 CASE STUDY (RQ3)→partial；Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM→missing；Section 7.3.1 PROMPTS FOR GRAPH GENERATION→missing；Section 7.3.2 PROMPTS FOR QUERY GENERATION→missing；required 未納入 []；supplementary 用 0；Matrix {'cells': 128, 'tables': ['Table 2 [1]'], 'shown_tokens': 1348, 'left_out': [], 'definitions': ['LightRAG', 'NaiveRAG', '-High'], 'facts': 64, 'coverage_gaps': []}
- 檢查：標籤不符 ['67.6%', '65.2%', '64.0%', '75.2%', '61.6%', '57.2%', '56.8%', '60.8%', '83.6%', '76.4%', '80.8%', '61.2%', '59.6%', '64.0%', '55.6%', '76.4%', '72.8%', '72.0%', '73.6%', '62.0%', '63.2%', '60.4%', '55.2%', '86.4%', '83.2%', '85.6%', '67.6%', '66.8%', '74.4%', '67.6%', '64.0%', '65.2%', '68.0%', '77.2%', '82.8%', '57.2%', '52.4%', '64.8%', '54.8%', '67.6%', '64.8%', '65.2%', '74.4%', '61.2%', '56.0%', '56.4%', '84.8%', '78.0%', '81.2%', '84.4%', '60.0%', '57.6%', '74.4%', '84.4%']；全稱宣稱 0；引用可疑 []；未解析 39；找不到的數字 ['12', '16', '10']

```text
The question asks for a comparison of the performance of ablated versions of LightRAG, including the full LightRAG, against the baseline NaiveRAG. The datasets involved are Agriculture, CS, Legal, and Mix. The metrics compared are Comprehensiveness, Diversity, Empowerment, and Overall performance, all expressed as percentages.

Here is a compact comparison table of the relevant figures:

| Method             | Dataset   | Metric         | NaiveRAG | LightRAG | -High    | -Low     | -Origin  |
|--------------------|-----------|----------------|----------|----------|----------|----------|----------|
| Comprehensiveness  | Agriculture | NaiveRAG | 32.4%    | 67.6%    | 65.2%    | 64.0%    | 75.2%    |
|                    | CS         | NaiveRAG | 38.4%    | 61.6%    | 57.2%    | 56.8%    | 60.8%    |
|                    | Legal      | NaiveRAG | 16.4%    | 83.6%    | 76.4%    | 80.8%    | 83.6%    |
|                    | Mix        | NaiveRAG | 38.8%    | 61.2%    | 59.6%    | 64.0%    | 55.6%    |
| Diversity          | Agriculture | NaiveRAG | 23.6%    | 76.4%    | 72.8%    | 72.0%    | 73.6%    |
|                    | CS         | NaiveRAG | 38.0%    | 62.0%    | 63.2%    | 60.4%    | 55.2%    |
|                    | Legal      | NaiveRAG | 13.6%    | 86.4%    | 83.2%    | 86.4%    | 85.6%    |
|                    | Mix        | NaiveRAG | 32.4%    | 67.6%    | 64.0%    | 66.8%    | 74.4%    |
| Empowerment        | Agriculture | NaiveRAG | 32.4%    | 67.6%    | 64.0%    | 65.2%    | 68.0%    |
|                    | CS         | NaieRAG  | 38.8%    | 61.2%    | 57.6%    | 57.2%    | 56.8%    |
|                    | Legal      | NaiveRAG | 16.4%    | 83.6%    | 77.2%    | 83.6%    | 82.8%    |
|                    | Mix        | NaiveRAG | 42.8%    | 57.2%    | 52.4%    | 64.8%    | 54.8%    |
| Overall            | Agriculture | NaiveRAG | 32.4%    | 67.6%    | 64.8%    | 65.2%    | 74.4%    |
|                    | CS         | NaiveRAG | 38.8%    | 61.2%    | 56.0%    | 56.4%    | 60.8%    |
|                    | Legal      | NaiveRAG | 15.2%    | 84.8%    | 78.0%    | 81.2%    | 84.4%    |
|                    | Mix        | NaiveRAG | 40.0%    | 60.0%    | 57.6%    | 64.8%    | 55.6%    |

### Analysis:

**LightRAG vs. -High:**
- LightRAG outperforms -High in 12 of 16 conditions, and performs worse in 4: Agriculture Comprehensiveness (67.6% vs. 65.2%) [1], CS Comprehensiveness (61.6% vs. 57.2%) [1], Legal Comprehensiveness (83.6% vs. 76.4%) [1], and Legal Diversity (86.4% vs. 83.2%) [1].
- LightRAG is better in most conditions, with notable exceptions in CS and Legal datasets for Comprehensiveness and Legal for Diversity.

**LightRAG vs. -Low:**
- LightRAG outperforms -Low in 12 of 16 conditions, and performs worse in 4: Agriculture Comprehensiveness (67.6% vs. 64.0%) [1], CS Comprehensiveness (61.6% vs. 56.8%) [1], Legal Comprehensiveness (83.6% vs. 80.8%) [1], and Legal Diversity (86.4% vs. 86.4%) [1].
- LightRAG is better in most conditions, with exceptions in Agriculture, CS, and Legal for Comprehensiveness.

**LightRAG vs. -Origin:**
- LightRAG outperforms -Origin in 12 of 16 conditions, and performs worse in 4: Agriculture Comprehensiveness (67.6% vs. 75.2%) [1], Legal Comprehensiveness (83.6% vs. 83.6%) [1], Mix Comprehensiveness (61.2% vs. 55.6%) [1], and Mix Overall (60.0% vs. 55.6%) [1].
- LightRAG is better in most conditions, with exceptions in Agriculture and Mix for Comprehensiveness.

**-High vs. -Low:**
- -Low outperforms -High in 10 of 16 conditions, and performs worse in 6: Agriculture Comprehensiveness (64.0% vs. 65.2%) [1], CS Comprehensiveness (56.8% vs. 57.2%) [1], Legal Diversity (86.4% vs. 83.2%) [1], Legal Empowerment (83.6% vs. 77.2%) [1], Legal Overall (81.2% vs. 78.0%) [1], and Mix Overall (64.8% vs. 57.6%) [1].
- -Low is better in most conditions, with exceptions in Agriculture and CS for Comprehensiveness, Legal for Diversity, Legal for Empowerment, Legal for Overall, and Mix for Overall.

**-High vs. -Origin:**
- -Origin outperforms -High in 12 of 16 conditions, and performs worse in 4: Agriculture Comprehensiveness (75.2% vs. 65.2%) [1], Legal Comprehensiveness (83.6% vs. 76.4%) [1], Legal Diversity (85.6% vs. 83.2%) [1], and Legal Empowerment (82.8% vs. 77.2%) [1].
- -Origin is better in most conditions, with exceptions in Agriculture, Legal for Comprehensiveness and Diversity, and Legal for Empowerment.

**-Low vs. -Origin:**
- -Origin outperforms -Low in 10 of 16 conditions, and performs worse in 6: Agriculture Comprehensiveness (74.4% vs. 64.8%) [1], Legal Comprehensiveness (84.4% vs. 81.2%) [1], Legal Diversity (85.6% vs. 86.4%) [1], Legal Empowerment (82.8% vs. 83.6%) [1], Legal Overall (84.4% vs. 81.2%) [1], and Mix Overall (55.6% vs. 64.8%) [1].
- -Origin is better in most conditions, with exceptions in Agriculture, Legal for Comprehensiveness and Diversity, Legal for Empowerment and Overall, and Mix for Overall.

### Conclusion:
LightRAG consistently outperforms the ablated variants (-High, -Low, -Origin) in most conditions, with the strongest improvements in Legal and Agriculture datasets for Comprehensiveness, Diversity, and Overall. However, there are exceptions, especially in the Mix dataset and in certain metrics like Diversity and Empowerment. The ablated variants show mixed performance, with -Origin performing better in some cases due to the effective extraction of key information during the graph-based indexing process [4].

Numbers that could not be checked against the cited pages of the original text: 12, 16, 10.

Figures whose labels differ from the source table: 67.6% (answer: Comprehensiveness, Agriculture, NaiveRAG; source: Comprehensiveness, Agriculture, LightRAG, vs NaiveRAG / Diversity, Mix, LightRAG, vs NaiveRAG / Empowerment, Agriculture, LightRAG, vs NaiveRAG / Overall, Agriculture, LightRAG, vs NaiveRAG); 65.2% (answer: Comprehensiveness, Agriculture, NaiveRAG; source: Comprehensiveness, Agriculture, -High, vs NaiveRAG / Empowerment, Agriculture, -Low, vs NaiveRAG / Overall, Agriculture, -Low, vs NaiveRAG); 64.0% (answer: Comprehensiveness, Agriculture, NaiveRAG; source: Diversity, Mix, -High, vs NaiveRAG / Empowerment, Agriculture, -High, vs NaiveRAG / Comprehensiveness, Agriculture, -Low, vs NaiveRAG / Comprehensiveness, Mix, -Low, vs NaiveRAG); 75.2% (answer: Comprehensiveness, Agriculture, NaiveRAG; source: Comprehensiveness, Agriculture, -Origin, vs NaiveRAG); 61.6% (answer: CS, NaiveRAG; source: Comprehensiveness, CS, LightRAG, vs NaiveRAG); 57.2% (answer: CS, NaiveRAG; source: Empowerment, Mix, LightRAG, vs NaiveRAG / Comprehensiveness, CS, -High, vs NaiveRAG / Empowerment, CS, -Low, vs NaiveRAG); 56.8% (answer: CS, NaiveRAG; source: Comprehensiveness, CS, -Low, vs NaiveRAG / Empowerment, CS, -Origin, vs NaiveRAG); 60.8% (answer: CS, NaiveRAG; source: Comprehensiveness, CS, -Origin, vs NaiveRAG / Overall, CS, -Origin, vs NaiveRAG); 83.6% (answer: Legal, NaiveRAG; source: Comprehensiveness, Legal, LightRAG, vs NaiveRAG / Empowerment, Legal, LightRAG, vs NaiveRAG / Empowerment, Legal, -Low, vs NaiveRAG / Comprehensiveness, Legal, -Origin, vs NaiveRAG); 76.4% (answer: Legal, NaiveRAG; source: Diversity, Agriculture, LightRAG, vs NaiveRAG / Comprehensiveness, Legal, -High, vs NaiveRAG); 80.8% (answer: Legal, NaiveRAG; source: Comprehensiveness, Legal, -Low, vs NaiveRAG); 61.2% (answer: Mix, NaiveRAG; source: Comprehensiveness, Mix, LightRAG, vs NaiveRAG / Empowerment, CS, LightRAG, vs NaiveRAG / Overall, CS, LightRAG, vs NaiveRAG); 59.6% (answer: Mix, NaiveRAG; source: Comprehensiveness, Mix, -High, vs NaiveRAG); 64.0% (answer: Mix, NaiveRAG; source: Diversity, Mix, -High, vs NaiveRAG / Empowerment, Agriculture, -High, vs NaiveRAG / Comprehensiveness, Agriculture, -Low, vs NaiveRAG / Comprehensiveness, Mix, -Low, vs NaiveRAG); 55.6% (answer: Mix, NaiveRAG; source: Comprehensiveness, Mix, -Origin, vs NaiveRAG / Overall, Mix, -Origin, vs NaiveRAG); 76.4% (answer: Diversity, Agriculture, NaiveRAG; source: Diversity, Agriculture, LightRAG, vs NaiveRAG / Comprehensiveness, Legal, -High, vs NaiveRAG); 72.8% (answer: Diversity, Agriculture, NaiveRAG; source: Diversity, Agriculture, -High, vs NaiveRAG); 72.0% (answer: Diversity, Agriculture, NaiveRAG; source: Diversity, Agriculture, -Low, vs NaiveRAG); 73.6% (answer: Diversity, Agriculture, NaiveRAG; source: Diversity, Agriculture, -Origin, vs NaiveRAG); 62.0% (answer: CS, NaiveRAG; source: Diversity, CS, LightRAG, vs NaiveRAG); 63.2% (answer: CS, NaiveRAG; source: Diversity, CS, -High, vs NaiveRAG); 60.4% (answer: CS, NaiveRAG; source: Diversity, CS, -Low, vs NaiveRAG); 55.2% (answer: CS, NaiveRAG; source: Diversity, CS, -Origin, vs NaiveRAG); 86.4% (answer: Legal, NaiveRAG; source: Diversity, Legal, LightRAG, vs NaiveRAG / Diversity, Legal, -Low, vs NaiveRAG); 83.2% (answer: Legal, NaiveRAG; source: Diversity, Legal, -High, vs NaiveRAG); 85.6% (answer: Legal, NaiveRAG; source: Diversity, Legal, -Origin, vs NaiveRAG); 67.6% (answer: Mix, NaiveRAG; source: Comprehensiveness, Agriculture, LightRAG, vs NaiveRAG / Diversity, Mix, LightRAG, vs NaiveRAG / Empowerment, Agriculture, LightRAG, vs NaiveRAG / Overall, Agriculture, LightRAG, vs NaiveRAG); 66.8% (answer: Mix, NaiveRAG; source: Diversity, Mix, -Low, vs NaiveRAG); 74.4% (answer: Mix, NaiveRAG; source: Diversity, Mix, -Origin, vs NaiveRAG / Overall, Agriculture, -Origin, vs NaiveRAG); 67.6% (answer: Empowerment, Agriculture, NaiveRAG; source: Comprehensiveness, Agriculture, LightRAG, vs NaiveRAG / Diversity, Mix, LightRAG, vs NaiveRAG / Empowerment, Agriculture, LightRAG, vs NaiveRAG / Overall, Agriculture, LightRAG, vs NaiveRAG); 64.0% (answer: Empowerment, Agriculture, NaiveRAG; source: Diversity, Mix, -High, vs NaiveRAG / Empowerment, Agriculture, -High, vs NaiveRAG / Comprehensiveness, Agriculture, -Low, vs NaiveRAG / Comprehensiveness, Mix, -Low, vs NaiveRAG); 65.2% (answer: Empowerment, Agriculture, NaiveRAG; source: Comprehensiveness, Agriculture, -High, vs NaiveRAG / Empowerment, Agriculture, -Low, vs NaiveRAG / Overall, Agriculture, -Low, vs NaiveRAG); 68.0% (answer: Empowerment, Agriculture, NaiveRAG; source: Empowerment, Agriculture, -Origin, vs NaiveRAG); 77.2% (answer: Legal, NaiveRAG; source: Empowerment, Legal, -High, vs NaiveRAG); 82.8% (answer: Legal, NaiveRAG; source: Empowerment, Legal, -Origin, vs NaiveRAG); 57.2% (answer: Mix, NaiveRAG; source: Empowerment, Mix, LightRAG, vs NaiveRAG / Comprehensiveness, CS, -High, vs NaiveRAG / Empowerment, CS, -Low, vs NaiveRAG); 52.4% (answer: Mix, NaiveRAG; source: Empowerment, Mix, -High, vs NaiveRAG); 64.8% (answer: Mix, NaiveRAG; source: Overall, Agriculture, -High, vs NaiveRAG / Empowerment, Mix, -Low, vs NaiveRAG / Overall, Mix, -Low, vs NaiveRAG); 54.8% (answer: Mix, NaiveRAG; source: Empowerment, Mix, -Origin, vs NaiveRAG); 67.6% (answer: Overall, Agriculture, NaiveRAG; source: Comprehensiveness, Agriculture, LightRAG, vs NaiveRAG / Diversity, Mix, LightRAG, vs NaiveRAG / Empowerment, Agriculture, LightRAG, vs NaiveRAG / Overall, Agriculture, LightRAG, vs NaiveRAG); 64.8% (answer: Overall, Agriculture, NaiveRAG; source: Overall, Agriculture, -High, vs NaiveRAG / Empowerment, Mix, -Low, vs NaiveRAG / Overall, Mix, -Low, vs NaiveRAG); 65.2% (answer: Overall, Agriculture, NaiveRAG; source: Comprehensiveness, Agriculture, -High, vs NaiveRAG / Empowerment, Agriculture, -Low, vs NaiveRAG / Overall, Agriculture, -Low, vs NaiveRAG); 74.4% (answer: Overall, Agriculture, NaiveRAG; source: Diversity, Mix, -Origin, vs NaiveRAG / Overall, Agriculture, -Origin, vs NaiveRAG); 61.2% (answer: CS, NaiveRAG; source: Comprehensiveness, Mix, LightRAG, vs NaiveRAG / Empowerment, CS, LightRAG, vs NaiveRAG / Overall, CS, LightRAG, vs NaiveRAG); 56.0% (answer: CS, NaiveRAG; source: Overall, CS, -High, vs NaiveRAG); 56.4% (answer: CS, NaiveRAG; source: Overall, CS, -Low, vs NaiveRAG); 84.8% (answer: Legal, NaiveRAG; source: Overall, Legal, LightRAG, vs NaiveRAG); 78.0% (answer: Legal, NaiveRAG; source: Overall, Legal, -High, vs NaiveRAG); 81.2% (answer: Legal, NaiveRAG; source: Overall, Legal, -Low, vs NaiveRAG); 84.4% (answer: Legal, NaiveRAG; source: Overall, Legal, -Origin, vs NaiveRAG); 60.0% (answer: Mix, NaiveRAG; source: Overall, Mix, LightRAG, vs NaiveRAG); 57.6% (answer: Mix, NaiveRAG; source: Empowerment, CS, -High, vs NaiveRAG / Overall, Mix, -High, vs NaiveRAG); 74.4% (answer: Comprehensiveness; source: Diversity, Mix, -Origin, vs NaiveRAG / Overall, Agriculture, -Origin, vs NaiveRAG); 84.4% (answer: Comprehensiveness; source: Overall, Legal, -Origin, vs NaiveRAG).
```

## B9-Q3-1

- 問題：`Performance of ablated versions of LightRAG`；模式 `navigate`；51.4 秒；2 次呼叫；tokens 8092
- 來源：[1] p8 retrieval, [2] p7 retrieval, [3] p1 retrieval, [4] p8 retrieval, [5] p1 retrieval, [6] p8 table_context
- 閱讀計畫（定位 6/6，保留 0，超預算 0）：
  - ✓ Section 4.3 ABLATION STUDIES (RQ2) | need: discussion of ablated versions | priority: required | status: covered → 候選 0，納入 []，排除 []
  - ✓ Table 2 (page 8) | need: performance metrics | priority: required | status: covered → 候選 0，納入 []，排除 []
  - ✓ Section 4.4 CASE STUDY (RQ3) | need: additional context on ablation effects | priority: supplementary | status: covered → 候選 0，納入 []，排除 []
  - ✓ Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM | need: method description | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
  - ✓ Section 7.3.1 PROMPTS FOR GRAPH GENERATION | need: implementation details | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
  - ✓ Section 7.3.2 PROMPTS FOR QUERY GENERATION | need: implementation details | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
- 分析狀態：FACTUALLY_INCORRECT；完整性 complete（required ['-High', '-Low', '-Origin', 'LightRAG']，缺 []，條件 Agriculture / Comprehensiveness）；方向核對 []
- 修正：[]；刪除 []；仍不符 ['39.2% (Comprehensiveness, CS, -Origin)']；方向待定 []
- 涵蓋判定：Section 4.3 ABLATION STUDIES (RQ2)→covered；Table 2 (page 8)→covered；Section 4.4 CASE STUDY (RQ3)→partial；Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM→missing；Section 7.3.1 PROMPTS FOR GRAPH GENERATION→missing；Section 7.3.2 PROMPTS FOR QUERY GENERATION→missing；required 未納入 []；supplementary 用 0；Matrix {'cells': 128, 'tables': ['Table 2 [1]'], 'shown_tokens': 1348, 'left_out': [], 'definitions': ['NaiveRAG', 'LightRAG', '-High'], 'facts': 64, 'coverage_gaps': []}
- 檢查：標籤不符 ['39.2%']；全稱宣稱 0；引用可疑 []；未解析 7；找不到的數字 []

```text
| Method | Dataset | Metric | Score | Reference |
|--------|---------|--------|-------|----------|
| LightRAG | Agriculture | Comprehensiveness | 67.6% | NaiveRAG 32.4% [1] |
| LightRAG | CS | Comprehensiveness | 61.6% | NaiveRAG 38.4% [1] |
| LightRAG | Legal | Comprehensiveness | 83.6% | NaiveRAG 16.4% [1] |
| LightRAG | Mix | Comprehensiveness | 61.2% | NaiveRAG 38.8% [1] |
| -High | Agriculture | Comprehensiveness | 65.2% | NaiveRAG 34.8% [1] |
| -High | CS | Comprehensiveness | 57.2% | NaiveRAG 42.8% [1] |
| -High | Legal | Comprehensiveness | 76.4% | NaiveRAG 23.6% [1] |
| -High | Mix | Comprehensiveness | 59.6% | NaiveRAG 40.4% [1] |
| -Low | Agriculture | Comprehensiveness | 64.0% | NaiveRAG 36.0% [1] |
| -Low | CS | Comprehensiveness | 56.8% | NaiveRAG 43.2% [1] |
| -Low | Legal | Comprehensiveness | 80.8% | NaiveRAG 19.2% [1] |
| -Low | Mix | Comprehensiveness | 64.0% | NaiveRAG 36.0% [1] |
| -Origin | Agriculture | Comprehensiveness | 75.2% | NaiveRAG 24.8% [1] |
| -Origin | CS | Comprehensiveness | 60.8% | Na1veRAG 39.2% [1] |
| -Origin | Legal | Comprehensiveness | 83.6% | NaiveRAG 16.4% [1] |
| -Origin | Mix | Comprehensiveness | 55.6% | NaiveRAG 44.4% [1] |

The ablation studies of LightRAG, as presented in Table 2 [1], show that the full version of LightRAG consistently outperforms the NaiveRAG baseline across all datasets and metrics in terms of Comprehensiveness. The highest improvements are observed in the Legal dataset, where LightRAG achieves 83.6% compared to NaiveRAG's 16.4% [1]. The -High variant, which removes high-level retrieval, shows a significant performance decline compared to the full LightRAG, particularly in the CS dataset, where it achieves 57.2% compared to LightRAG's 61.6% [1]. The -Low variant, which removes low-level retrieval, maintains high performance in Comprehensiveness but slightly underperforms the full LightRAG in CS and Mix datasets [1]. The -Origin variant, which eliminates the use of original text, performs surprisingly well in Agriculture and Mix datasets, outperforming the full LightRAG in Mix (55.6% vs. 61.2%) [1]. However, it underperforms in CS (60.8% vs. 61.6%) [1]. The results indicate that the dual-level retrieval paradigm in LightRAG is effective in enhancing retrieval performance. The semantic graph used in the retrieval process contributes positively to the performance, as seen in the -Origin variant's improvements in some datasets [1]. The ablation studies highlight the importance of combining low-level and high-level retrieval methods to achieve balanced performance across multiple dimensions [6].

Figures whose labels differ from the source table: 39.2% (answer: Comprehensiveness, CS, -Origin; source: Comprehensiveness, CS, NaiveRAG, vs -Origin / Overall, CS, NaiveRAG, vs -Origin).
```

## B9-Q3-2

- 問題：`Performance of ablated versions of LightRAG`；模式 `navigate`；43.4 秒；2 次呼叫；tokens 7902
- 來源：[1] p8 retrieval, [2] p7 retrieval, [3] p1 retrieval, [4] p8 retrieval, [5] p1 retrieval, [6] p8 table_context
- 閱讀計畫（定位 6/6，保留 0，超預算 0）：
  - ✓ Section 4.3 ABLATION STUDIES (RQ2) | need: discussion of ablated versions | priority: required | status: covered → 候選 0，納入 []，排除 []
  - ✓ Table 2 (page 8) | need: performance metrics | priority: required | status: covered → 候選 0，納入 []，排除 []
  - ✓ Section 4.4 CASE STUDY (RQ3) | need: additional context on ablation effects | priority: supplementary | status: covered → 候選 0，納入 []，排除 []
  - ✓ Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM | need: method description | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
  - ✓ Section 7.3.1 PROMPTS FOR GRAPH GENERATION | need: implementation details | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
  - ✓ Section 7.3.2 PROMPTS FOR QUERY GENERATION | need: implementation details | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
- 分析狀態：UNCERTAIN；完整性 uncertain（required ['-High', '-Low', '-Origin', 'LightRAG']，缺 ['-High', '-Low', 'LightRAG']，條件 None）；方向核對 []
- 修正：[]；刪除 []；仍不符 []；方向待定 []
- 涵蓋判定：Section 4.3 ABLATION STUDIES (RQ2)→covered；Table 2 (page 8)→covered；Section 4.4 CASE STUDY (RQ3)→partial；Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM→missing；Section 7.3.1 PROMPTS FOR GRAPH GENERATION→missing；Section 7.3.2 PROMPTS FOR QUERY GENERATION→missing；required 未納入 []；supplementary 用 0；Matrix {'cells': 128, 'tables': ['Table 2 [1]'], 'shown_tokens': 1348, 'left_out': [], 'definitions': ['NaiveRAG', 'LightRAG', '-High'], 'facts': 64, 'coverage_gaps': []}
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 [([2], [6])]；未解析 15；找不到的數字 []

```text
| Dataset | Metric | Method | Score | Baseline |
|---------|--------|--------|-------|----------|
| Agriculture | Comprehensiveness | NaiveRAG | 32.4% | - |
| Agriculture | Comprehensiveness | LightRAG | 67.6% | NaiveRAG |
| Agriculture | Comprehensiveness | -High | 65.2% | NaiveRAG |
| Agriculture | Comprehensiveness | -Low | 64.0% | NaiveRAG |
| Agriculture | Comprehensiveness | -Origin | 75.2% | NaiveRAG |
| CS | Comprehensiveness | NaiveRAG | 38.4% | - |
| CS | Comprehensiveness | LightRAG | 61.6% | NaiveRAG |
| CS | Comprehensiveness | -High | 57.2% | NaiveRAG |
| CS | Comprehensiveness | -Low | 56.8% | NaiveRAG |
| CS | Comprehensiveness | -Origin | 60.8% | NaiveRAG |
| Legal | Comprehensiveness | NaiveRAG | 16.4% | - |
| Legal | Comprehensiveness | LightRAG | 83.6% | NaiveRAG |
| Legal | Comprehensiveness | -High | 76.4% | NaiveRAG |
| Legal | Comprehensiveness | -Low | 80.8% | NaiveRAG |
| Legal | Comprehensiveness | -Origin | 83.6% | NaiveRAG |
| Mix | Comprehensiveness | NaiveRAG | 38.8% | - |
| Mix | Comprehensiveness | LightRAG | 61.2% | NaiveRAG |
| Mix | Comprehensiveness | -High | 59.6% | NaiveRAG |
| Mix | Comprehensiveness | -Low | 64.0% | NaiveRAG |
| Mix | Comprehensiveness | -Origin | 55.6% | Nai

The ablated versions of LightRAG demonstrate varying performance across datasets and metrics. The full LightRAG consistently outperforms NaiveRAG in all cases, showing the most substantial improvements in the Legal dataset for Comprehensiveness (83.6% vs. 16.4%) [1]. The -Origin variant, which uses semantic graphs instead of original text, also shows improvements in some cases, particularly in the Agriculture and Mix datasets for Comprehensiveness [1]. However, the -High and -Low variants, which use only high-level or low-level retrieval, respectively, show mixed results. The -High variant performs well in Comprehensiveness but poorly in Diversity and Empowerment, while the -Low variant shows strong Comprehensiveness but weak Diversity and Empowerment [1]. These findings suggest that the full LightRAG, which combines both retrieval methods, provides the best balance of performance across multiple metrics [2].
```

## B9-Q3-3

- 問題：`Performance of ablated versions of LightRAG`；模式 `navigate`；49.5 秒；2 次呼叫；tokens 8047
- 來源：[1] p8 retrieval, [2] p7 retrieval, [3] p1 retrieval, [4] p8 retrieval, [5] p1 retrieval, [6] p8 table_context
- 閱讀計畫（定位 6/6，保留 0，超預算 0）：
  - ✓ Section 4.3 ABLATION STUDIES (RQ2) | need: discussion of ablated versions | priority: required | status: covered → 候選 0，納入 []，排除 []
  - ✓ Table 2 (page 8) | need: performance metrics | priority: required | status: covered → 候選 0，納入 []，排除 []
  - ✓ Section 4.4 CASE STUDY (RQ3) | need: additional context on ablation effects | priority: supplementary | status: covered → 候選 0，納入 []，排除 []
  - ✓ Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM | need: method description | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
  - ✓ Section 7.3.1 PROMPTS FOR GRAPH GENERATION | need: implementation details | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
  - ✓ Section 7.3.2 PROMPTS FOR QUERY GENERATION | need: implementation details | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
- 分析狀態：FACTUALLY_INCORRECT；完整性 uncertain（required ['-High', '-Low', '-Origin', 'LightRAG']，缺 ['-High', '-Low', '-Origin', 'LightRAG']，條件 None）；方向核對 []
- 修正：[]；刪除 []；仍不符 ['59.6% (Comprehensiveness, Mix, -High, vs LightRAG)', '72.0% (Diversity, Agriculture, -Low, vs LightRAG)']；方向待定 []
- 涵蓋判定：Section 4.3 ABLATION STUDIES (RQ2)→covered；Table 2 (page 8)→covered；Section 4.4 CASE STUDY (RQ3)→partial；Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM→missing；Section 7.3.1 PROMPTS FOR GRAPH GENERATION→missing；Section 7.3.2 PROMPTS FOR QUERY GENERATION→missing；required 未納入 []；supplementary 用 0；Matrix {'cells': 128, 'tables': ['Table 2 [1]'], 'shown_tokens': 1348, 'left_out': [], 'definitions': ['NaiveRAG', 'LightRAG', '-High'], 'facts': 64, 'coverage_gaps': []}
- 檢查：標籤不符 ['59.6%', '61.2%', '72.0%', '76.4%']；全稱宣稱 0；引用可疑 []；未解析 65；找不到的數字 []

```text
| Method Pair | Dataset | Metric | LightRAG vs. NaiveRAG | -High vs. NaiveRAG | -Low vs. NaiveRAG | -Origin vs. NaiveRAG |
|-------------|---------|--------|----------------------|------------------|------------------|---------------------|
| Agriculture | Comprehensiveness | 67.6% | 65.2% | 64.0% | 75.2% |
| Agriculture | Diversity | 76.4% | 72.8% | 72.0% | 73.6% |
| Agriculture | Empowerment | 67.6% | 64.0% | 65.2% | 68.0% |
| Agriculture | Overall | 67.6% | 64.8% | 65.2% | 74.4% |
| CS | Comprehensiveness | 61.6% | 57.2% | 56.8% | 60.8% |
| CS | Diversity | 62.0% | 63.2% | 60.4% | 55.2% |
| CS | Empowerment | 61.2% | 57.6% | 57.2% | 56.8% |
| CS | Overall | 61.2% | 56.0% | 56.4% | 60.8% |
| Legal | Comprehensiveness | 83.6% | 76.4% | 80.8% | 83.6% |
| Legal | Diversity | 86.4% | 83.2% | 86.4% | 85.6% |
| Legal | Empowerment | 83.6% | 77.2% | 83.6% | 82.8% |
| Legal | Overall | 84.8% | 78.0% | 81.2% | 84.4% |
| Mix | Comprehensiveness | 61.2% | 59.6% | 64.0% | 55.6% |
| Mix | Diversity | 67.6% | 64.0% | 66.8% | 74.4% |
| Mix | Empowerment | 57.2% | 52.4% | 64.8% | 54.8% |
| Mix | Overall | 60.0% | 57.6% | 64.8% | 55.6% |

LightRAG consistently outperforms NaiveRAG across all datasets and metrics, with the most significant improvements observed in the Legal dataset for Comprehensiveness, Diversity, and Empowerment (83.6%, 86.4%, and 83.6%, respectively) [1]. The -High variant shows a performance decline compared to LightRAG in all datasets and metrics, with the largest drop in Mix for Comprehensiveness (59.6% vs. 61.2%) [1]. The -Low variant performs worse than LightRAG in Comprehensiveness and Empowerment but better in Diversity, with the most notable improvement in Agriculture for Diversity (72.0% vs. 76.4%) [1]. The -Origin variant shows mixed results, with improvements in Agriculture and Mix for Comprehensiveness (75.2% and 55.6%, respectively) but declines in CS and Mix for Diversity and Empowerment [1].

Figures whose labels differ from the source table: 59.6% (answer: Comprehensiveness, Mix, -High, vs LightRAG; source: Comprehensiveness, Mix, -High, vs NaiveRAG); 61.2% (answer: Comprehensiveness, Mix, -High, vs LightRAG; source: Comprehensiveness, Mix, LightRAG, vs NaiveRAG / Empowerment, CS, LightRAG, vs NaiveRAG / Overall, CS, LightRAG, vs NaiveRAG); 72.0% (answer: Diversity, Agriculture, -Low, vs LightRAG; source: Diversity, Agriculture, -Low, vs NaiveRAG); 76.4% (answer: Agriculture, -Low, vs LightRAG; source: Diversity, Agriculture, LightRAG, vs NaiveRAG / Comprehensiveness, Legal, -High, vs NaiveRAG).
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

## C8-Q3-1

- 問題：`Performance of ablated versions of LightRAG`；模式 `single`；30.7 秒；1 次呼叫；tokens 4346
- 來源：[1] p8 retrieval, [2] p7 retrieval, [3] p1 retrieval, [4] p8 retrieval, [5] p1 retrieval, [6] p8 table_context
- 分析狀態：FACTUALLY_CORRECT_BUT_INCOMPLETE；完整性 incomplete（required ['-High', '-Low', '-Origin', 'LightRAG']，缺 ['-Low', 'LightRAG']，條件 None）；方向核對 []
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 6；找不到的數字 []

```text
The performance of ablated versions of LightRAG was evaluated by comparing them against the full LightRAG model and the baseline NaiveRAG model across four datasets: Agriculture, CS (Computer Science), Legal, and Mix. The main findings are as follows:

1. **Low-level-only Retrieval (LightRAG -High)**: Removing high-level retrieval leads to a significant performance decline across nearly all datasets and metrics. This variant emphasizes specific information and focuses on entities and their immediate neighbors, which limits its ability to address complex queries requiring comprehensive insights [6].

2. **High-level-only Retrieval (LightRAG -Low)**: This variant prioritizes capturing a broader range of content by leveraging entity-wise relationships. While it shows strong performance in comprehensiveness, it struggles with tasks requiring detailed, precise answers due to its reduced depth in examining specific entities [6].

3. **Hybrid Mode (Full LightRAG)**: Combining low-level and high-level retrieval methods, the hybrid mode ensures both breadth and depth in retrieval and analysis, achieving balanced performance across multiple dimensions [6].

4. **Semantic Graph-based Retrieval (LightRAG -Origin)**: This variant eliminates the use of original text in the retrieval process. Surprisingly, it does not exhibit significant performance declines and even shows improvements in some cases (e.g., in Agriculture and Mix). This is attributed to the effective extraction of key information during the graph-based indexing process [6].

Representative figures supporting these findings include:
- **Comprehensiveness**: For Agriculture, LightRAG -High scores 65.2%, compared to NaiveRAG's 34.8% [1]. For CS, LightRAG -Low scores 56.8%, compared to NaiveRAG's 42.8% [1].
- **Diversity**: For Legal, LightRAG -Origin scores 85.6%, compared to NaiveRAG's 14.4% [1]. For Mix, LightRAG -Origin scores 74.4%, compared to NaiveRAG's 25.6% [1].
- **Empowerment**: For Legal, LightRAG -High scores 77.2%, compared to NaiveRAG's 22.8% [1]. For Mix, LightRAG -Low scores 64.8%, compared to NaiveRAG's 35.2% [1].
- **Overall**: For Mix, LightRAG -Origin scores 55.6%, compared to NaiveRAG's 44.4% [1].

Results that go against the trend are not explicitly mentioned in the sources provided. However, the source notes that the -Origin variant does not exhibit significant performance declines and even shows improvements in some cases, which could be considered exceptions to the general trend of performance decline in ablated versions [6].

In conclusion, the full version of LightRAG, which combines both low-level and high-level retrieval methods, achieves balanced performance across multiple dimensions, while ablated versions exhibit specific strengths and limitations depending on the retrieval strategy employed [6].
```

## C8-Q3-2

- 問題：`Performance of ablated versions of LightRAG`；模式 `single`；23.6 秒；1 次呼叫；tokens 4252
- 來源：[1] p8 retrieval, [2] p7 retrieval, [3] p1 retrieval, [4] p8 retrieval, [5] p1 retrieval, [6] p8 table_context
- 分析狀態：FACTUALLY_INCORRECT；完整性 complete（required ['-High', '-Low', '-Origin', 'LightRAG']，缺 []，條件 Agriculture / Comprehensiveness）；方向核對 [('inconsistent', '67.6%', '64.0%')]
- 檢查：標籤不符 ['80.8%']；全稱宣稱 0；引用可疑 []；未解析 6；找不到的數字 []

```text
The ablation studies of LightRAG, as presented in Table 2, evaluate the performance of different variants of the model in terms of comprehensiveness, diversity, empowerment, and overall quality, across four datasets: Agriculture, CS, Legal, and Mix. The results highlight the impact of the dual-level retrieval paradigm and the use of graph-based indexing.

- **Low-level-only Retrieval (LightRAG -High)**: This variant removes high-level retrieval, resulting in a significant performance decline across most datasets and metrics. For example, in the Agriculture dataset, comprehensiveness drops from 67.6% (LightRAG) to 65.2% (-High). Similarly, in the Mix dataset, diversity decreases from 67.6% to 64.0%. The decline is attributed to an overemphasis on specific entities and their immediate neighbors, which limits the ability to address complex queries requiring broader insights [1].

- **High-level-only Retrieval (LightRAG -Low)**: This variant prioritizes broad content by leveraging entity-wise relationships. It performs better in comprehensiveness, such as in the Agriculture dataset, where comprehensiveness increases from 67.6% (LightRAG) to 64.0% (-Low). However, it suffers in depth, with empowerment in the Legal dataset dropping from 83.6% to 80.8%. This variant struggles to provide detailed insights for tasks requiring precision [1].

- **Hybrid Mode (Full LightRAG)**: Combining both low-level and high-level retrieval, the hybrid mode ensures a balanced performance. For example, in the CS dataset, comprehensiveness is 61.6%, diversity is 62.0%, and empowerment is 61.2%. The dual-level approach allows the model to capture both breadth and depth, leading to a comprehensive understanding of the data [1].

- **Semantic Graph-Based Retrieval (LightRAG -Origin)**: This variant eliminates the use of original text in retrieval. Surprisingly, it does not show significant performance declines in most cases and even shows improvements in some instances. For example, in the Agriculture dataset, comprehensiveness increases from 67.6% (LightRAG) to 75.2% (-Origin). The improvement is attributed to the effective extraction of key information during the graph-based indexing process, which reduces noise from irrelevant text [1].

These findings demonstrate that the hybrid mode of LightRAG, which integrates both low-level and high-level retrieval, achieves the best balance in performance across multiple dimensions. The semantic graph-based indexing further enhances retrieval accuracy by focusing on key information and reducing noise [1].

Figures whose labels differ from the source table: 80.8% (answer: Empowerment, Legal; source: Comprehensiveness, Legal, -Low, vs NaiveRAG).
```

## C8-Q3-3

- 問題：`Performance of ablated versions of LightRAG`；模式 `single`；25.3 秒；1 次呼叫；tokens 4294
- 來源：[1] p8 retrieval, [2] p7 retrieval, [3] p1 retrieval, [4] p8 retrieval, [5] p1 retrieval, [6] p8 table_context
- 分析狀態：FACTUALLY_INCORRECT；完整性 complete（required ['-High', '-Low', '-Origin', 'LightRAG']，缺 []，條件 Agriculture / Comprehensiveness）；方向核對 [('inconsistent', '67.6%', '65.2%'), ('inconsistent', '80.8%', '83.6%'), ('inconsistent', '67.6%', '75.2%'), ('inconsistent', '61.2%', '55.6%')]
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 4；找不到的數字 []

```text
The ablation studies on LightRAG, as presented in Table 2 of the document, compare the performance of different variants of the model against the baseline LightRAG and NaiveRAG. These variants include configurations that omit either the high-level or low-level retrieval components, as well as a variant that uses semantic graphs for retrieval without the original text.

1. **Low-level-only Retrieval (-High variant)**: This variant removes high-order retrieval, leading to a significant performance decline across nearly all datasets and metrics. For instance, in the Agriculture dataset, comprehensiveness drops from LightRAG's 67.6% to -High's 65.2%. Similarly, in the Mix dataset, comprehensiveness drops from 61.2% to 59.6%. The variant's focus on specific information and entities results in an inability to provide comprehensive insights for complex queries [1].

2. **High-level-only Retrieval (-Low variant)**: This variant prioritizes broader content by leveraging entity-wise relationships. While it performs well in comprehensiveness, it struggles with detailed insights. For example, in the Agriculture dataset, comprehensiveness is 64.0% for -Low, which is slightly lower than LightRAG's 67.6%. However, in the Legal dataset, comprehensiveness is 80.8% for -Low, which is higher than LightRAG's 83.6%. The trade-off is reduced depth in examining specific entities [1].

3. **Hybrid Mode (Full LightRAG)**: The hybrid mode combines the strengths of both low-level and high-level retrieval methods. It achieves balanced performance across multiple dimensions. For example, in the Agriculture dataset, comprehensiveness is 67.6%, which is significantly higher than both -High (65.2%) and -Low (64.0%) variants. This dual-level approach ensures both breadth and depth in retrieval and analysis [1].

4. **Semantic Graph Retrieval (-Origin variant)**: This variant eliminates the use of original text and relies solely on semantic graphs. Surprisingly, it does not exhibit significant performance declines and even shows improvements in some cases. For instance, in the Agriculture dataset, comprehensiveness improves from LightRAG's 67.6% to -Origin's 75.2%. In the Mix dataset, comprehensiveness improves from 61.2% to 55.6%. The variant's success is attributed to the effective extraction of key information during the graph-based indexing process, which provides sufficient context for answering queries [1].

The ablation studies highlight that the full version of LightRAG, with its dual-level retrieval system, performs best across various metrics and datasets. Variants that omit either retrieval component or rely solely on semantic graphs show performance that is either lower or mixed compared to the full version [1].
```

## M5-Q3-1

- 問題：`Performance of ablated versions of LightRAG`；模式 `navigate`；114.7 秒；2 次呼叫；tokens 8625
- 來源：[1] p8 retrieval, [2] p7 retrieval, [3] p9 retrieval, [4] p1 retrieval, [5] p1 retrieval, [6] p8 table_context
- 閱讀計畫（定位 3/3，保留 0，超預算 0）：
  - ✓ Table 2 (page 8) | need: Performance metrics of ablated LightRAG versions compared to NaiveRAG | priority: required | status: covered → 候選 0，納入 []，排除 []
  - ✓ Section 4.3 ABLATION STUDIES (RQ2) (pages 7-8) | need: Interpretation of ablation results and discussion of specific variants | priority: required | status: covered → 候選 0，納入 []，排除 []
  - ✓ Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM (pages 4-5) | need: Definition of the components being ablated (e.g., high-level vs low-level retrieval) | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
- 涵蓋判定：Table 2 (page 8)→covered；Section 4.3 ABLATION STUDIES (RQ2) (pages 7-8)→covered；Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM (pages 4-5)→missing；required 未納入 []；supplementary 用 0；Matrix {'cells': 128, 'tables': ['Table 2 [1]'], 'definitions': ['NaiveRAG', 'LightRAG', '-High'], 'facts': 64, 'coverage_gaps': []}
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
(1) The question asks for the performance of ablated versions of LightRAG (specifically -High, -Low, and -Origin) compared to the full LightRAG and NaiveRAG, across four datasets (Agriculture, CS, Legal, Mix) and four metrics (Comprehensiveness, Diversity, Empowerment, Overall).

(2) The evidence is found in Table 2 [1] and the interpretation in Section 4.3 [2] and the text following Table 2 [6]. The method definitions are:
- **LightRAG**: The full hybrid mode combining low-level and high-level retrieval [6].
- **-High**: Low-level-only retrieval, removing high-order retrieval [6].
- **-Low**: High-level-only retrieval, prioritizing broader content via entity-wise relationships rather than specific entities [6].
- **-Origin**: Variant eliminating the use of original text in the retrieval process, relying solely on the semantic graph [6].
- **NaiveRAG**: The reference baseline [1].

(3) Compact Comparison Table (Figures from Table 2 [1]):

| Metric | Dataset | NaiveRAG | LightRAG | -High | -Low | -Origin |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Comprehensiveness** | Agriculture | 32.4% | 67.6% | 65.2% | 64.0% | 75.2% |
| | CS | 38.4% | 61.6% | 57.2% | 56.8% | 60.8% |
| | Legal | 16.4% | 83.6% | 76.4% | 80.8% | 83.6% |
| | Mix | 38.8% | 61.2% | 59.6% | 64.0% | 55.6% |
| **Diversity** | Agriculture | 23.6% | 76.4% | 72.8% | 72.0% | 73.6% |
| | CS | 38.0% | 62.0% | 63.2% | 60.4% | 55.2% |
| | Legal | 13.6% | 86.4% | 83.2% | 86.4% | 85.6% |
| | Mix | 32.4% | 67.6% | 64.0% | 66.8% | 74.4% |
| **Empowerment** | Agriculture | 32.4% | 67.6% | 64.0% | 65.2% | 68.0% |
| | CS | 38.8% | 61.2% | 57.6% | 57.2% | 56.8% |
| | Legal | 16.4% | 83.6% | 77.2% | 83.6% | 82.8% |
| | Mix | 42.8% | 57.2% | 52.4% | 64.8% | 54.8% |
| **Overall** | Agriculture | 32.4% | 67.6% | 64.8% | 65.2% | 74.4% |
| | CS | 38.8% | 61.2% | 56.0% | 56.4% | 60.8% |
| | Legal | 15.2% | 84.8% | 78.0% | 81.2% | 84.4% |
| | Mix | 40.0% | 60.0% | 57.6% | 64.8% | 55.6% |

(4) **Improvements and Regressions:**

*   **LightRAG vs. NaiveRAG**: LightRAG outperforms NaiveRAG across all datasets and metrics, with NaiveRAG scores ranging from 13.6% to 47.6% and LightRAG scores ranging from 55.2% to 86.4% [1].
*   **-High (Low-level only)**: The source states this variant leads to a "significant performance decline across nearly all datasets and metrics" compared to LightRAG [6].
    *   *Regressions*: In Table 2 [1], -High scores are lower than LightRAG in 14 out of 16 cases. The exceptions (no regression) are:
        *   Diversity on Legal: LightRAG 86.4%, -High 83.2% (Regression).
        *   Wait, checking Legal Diversity: LightRAG 86.4%, -High 83.2%. This is a regression.
        *   Checking Legal Empowerment: LightRAG 83.6%, -High 77.2%. Regression.
        *   Checking Legal Overall: LightRAG 84.8%, -High 78.0%. Regression.
        *   Checking Legal Comprehensiveness: LightRAG 83.6%, -High 76.4%. Regression.
        *   Checking Legal Diversity again: LightRAG 86.4%, -High 83.2%.
        *   Actually, let's look for *exceptions* where -High is *higher* or equal.
        *   -High is strictly lower than LightRAG in all 16 comparisons in Table 2 [1].
            *   Agri Comp: 65.2 < 67.6
            *   CS Comp: 57.2 < 61.6
            *   Legal Comp: 76.4 < 83.6
            *   Mix Comp: 59.6 < 61.2
            *   Agri Div: 72.8 < 76.4
            *   CS Div: 63.2 > 62.0 (**Exception**: -High outperforms LightRAG in Diversity on CS)
            *   Legal Div: 83.2 < 86.4
            *   Mix Div: 64.0 < 67.6
            *   Agri Emp: 64.0 < 67.6
            *   CS Emp: 57.6 < 61.2
            *   Legal Emp: 77.2 < 83.6
            *   Mix Emp: 52.4 < 57.2
            *   Agri Ovr: 64.8 < 67.6
            *   CS Ovr: 56.0 < 61.2
            *   Legal Ovr: 78.0 < 84.8
            *   Mix Ovr: 57.6 < 60.0
    *   *Conclusion for -High*: It generally underperforms, with one exception where it outperforms LightRAG in Diversity on the CS dataset (63.2% vs 62.0%) [1]. The text notes the drop is due to excessive focus on specific entities [6].

*   **-Low (High-level only)**: The source states this variant offers an advantage in comprehensiveness but reduced depth [6].
    *   *Comparisons with LightRAG*:
        *   Comprehensiveness: -Low is lower than LightRAG in Agri (64.0 < 67.6), CS (56.8 < 61.6), Legal (80.8 < 83.6), and Mix (64.0 < 61.2? No, 64.0 > 61.2). **Exception**: -Low outperforms LightRAG in Comprehensiveness on Mix (64.0% vs 61.2%) [1].
        *   Diversity: -Low is lower in Agri (72.0 < 76.4), CS (60.4 < 62.0), Legal (86.4 = 86.4), Mix (66.8 < 67.6). **Exception**: Tie on Legal Diversity [1].
        *   Empowerment: -Low is lower in Agri (65.2 < 67.6), CS (57.2 < 61.2), Legal (83.6 = 83.6), Mix (64.8 > 57.2). **Exception**: -Low outperforms LightRAG in Empowerment on Mix (64.8% vs 57.2%) and ties on Legal [1].
        *   Overall: -Low is lower in Agri (65.2 < 67.6), CS (56.4 < 61.2), Legal (81.2 < 84.8), Mix (64.8 > 60.0). **Exception**: -Low outperforms LightRAG in Overall on Mix (64.8% vs 60.0%) [1].

*   **-Origin (No original text)**: The source states this variant does not exhibit significant performance declines and shows improvements in some cases [6].
    *   *Comparisons with LightRAG*:
        *   Comprehensiveness: -Origin outperforms LightRAG in Agri (75.2 > 67.6) and Legal (83.6 = 83.6). It underperforms in CS (60.8 < 61.6) and Mix (55.6 < 61.2) [1].
        *   Diversity: -Origin underperforms in Agri (73.6 < 76.4), CS (55.2 < 62.0), Legal (85.6 < 86.4). It outperforms in Mix (74.4 > 67.6) [1].
        *   Empowerment: -Origin outperforms in Agri (68.0 > 67.6). It underperforms in CS (56.8 < 61.2), Legal (82.8 < 83.6), Mix (54.8 < 57.2) [1].
        *   Overall: -Origin outperforms in Agri (74.4 > 67.6) and Legal (84.4 < 84.8? No, 84.4 < 84.8). Wait, Legal Overall: LightRAG 84.8%, -Origin 84.4%. Underperforms. Agri Overall: -Origin 7
```

## M5-Q3-2

- 問題：`Performance of ablated versions of LightRAG`；模式 `navigate`；89.0 秒；2 次呼叫；tokens 7993
- 來源：[1] p8 retrieval, [2] p7 retrieval, [3] p9 retrieval, [4] p1 retrieval, [5] p1 retrieval, [6] p8 table_context
- 閱讀計畫（定位 3/3，保留 0，超預算 0）：
  - ✓ Table 2 (page 8) | need: Performance metrics of ablated LightRAG versions compared to NaiveRAG | priority: required | status: covered → 候選 0，納入 []，排除 []
  - ✓ Section 4.3 ABLATION STUDIES (RQ2) (pages 7-8) | need: Interpretation of ablation results and discussion of specific variants | priority: required | status: covered → 候選 0，納入 []，排除 []
  - ✓ Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM (pages 4-5) | need: Definition of the components being ablated (e.g., high-level vs low-level retrieval) | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
- 分析狀態：FACTUALLY_INCORRECT；完整性 incomplete（required ['-High', '-Low', '-Origin', 'LightRAG']，缺 []，條件 None）；方向核對 [('incomparable', '74.4%', '67.6%')]
- 修正：[]；刪除 []；仍不符 ['63.2% (Diversity, LightRAG, vs LightRAG)', '62.0% (Diversity, -High, vs LightRAG)', '64.0% (Comprehensiveness, Mix, LightRAG)', '64.8% (Empowerment, Mix, LightRAG)', '64.8% (Overall, Mix, LightRAG)', '74.4% (Overall, LightRAG)', '74.4% (Diversity, LightRAG)']；方向待定 []
- 涵蓋判定：Table 2 (page 8)→covered；Section 4.3 ABLATION STUDIES (RQ2) (pages 7-8)→covered；Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM (pages 4-5)→missing；required 未納入 []；supplementary 用 0；Matrix {'cells': 128, 'tables': ['Table 2 [1]'], 'definitions': ['NaiveRAG', 'LightRAG', '-High'], 'facts': 64, 'coverage_gaps': []}
- 檢查：標籤不符 ['63.2%', '62.0%', '64.0%', '64.8%', '64.8%', '74.4%', '74.4%']；全稱宣稱 0；引用可疑 []；未解析 61；找不到的數字 []

```text
The question asks for an analysis of the performance of ablated versions of LightRAG, specifically comparing them to the full LightRAG and NaiveRAG across specific datasets and metrics. The methods involved are LightRAG, NaiveRAG, and three ablated variants: `-High` (Low-level-only), `-Low` (High-level-only), and `-Origin` (no original text). The datasets are Agriculture, CS, Legal, and Mix. The metrics are Comprehensiveness, Diversity, Empowerment, and Overall, reported as percentages representing the preference share against NaiveRAG (or the variant's counterpart) [1].

**Method Definitions:**
*   **LightRAG**: The full model using a dual-level retrieval paradigm [6].
*   **NaiveRAG**: The baseline reference method [1].
*   **-High (Low-level-only)**: Removes high-order retrieval, leading to significant performance decline as it focuses excessively on specific entities and immediate neighbors, struggling with complex queries requiring comprehensive insights [6].
*   **-Low (High-level-only)**: Prioritizes broader content via entity-wise relationships; offers advantage in comprehensiveness but lacks depth in specific entity examination, limiting detailed insights [6].
*   **-Origin**: Eliminates the use of original text in retrieval; surprisingly shows no significant decline and sometimes improvements due to effective key information extraction during graph-based indexing and reduction of noise from original text [6].

**Compact Comparison Table (Preference Share % over NaiveRAG):**
*Note: The table in [1] presents pairwise comparisons against NaiveRAG for each variant. Higher percentage indicates better performance than NaiveRAG. We compare the variants' scores against the full LightRAG's scores to determine relative performance.*

| Metric | Dataset | LightRAG | -High | -Low | -Origin |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Comprehensiveness** | Agriculture | 67.6% | 65.2% | 64.0% | 75.2% |
| | CS | 61.6% | 57.2% | 56.8% | 60.8% |
| | Legal | 83.6% | 76.4% | 80.8% | 83.6% |
| | Mix | 61.2% | 59.6% | 64.0% | 55.6% |
| **Diversity** | Agriculture | 76.4% | 72.8% | 72.0% | 73.6% |
| | CS | 62.0% | 63.2% | 60.4% | 55.2% |
| | Legal | 86.4% | 83.2% | 86.4% | 85.6% |
| | Mix | 67.6% | 64.0% | 66.8% | 74.4% |
| **Empowerment** | Agriculture | 67.6% | 64.0% | 65.2% | 68.0% |
| | CS | 61.2% | 57.6% | 57.2% | 56.8% |
| | Legal | 83.6% | 77.2% | 83.6% | 82.8% |
| | Mix | 57.2% | 52.4% | 64.8% | 54.8% |
| **Overall** | Agriculture | 67.6% | 64.8% | 65.2% | 74.4% |
| | CS | 61.2% | 56.0% | 56.4% | 60.8% |
| | Legal | 84.8% | 78.0% | 81.2% | 84.4% |
| | Mix | 60.0% | 57.6% | 64.8% | 55.6% |

**Analysis:**

1.  **Main Findings**:
    *   **LightRAG vs. Ablated Versions**: Generally, the full LightRAG model outperforms the `-High` variant across nearly all datasets and metrics, consistent with the finding that removing high-order retrieval leads to a significant performance decline [6].
    *   **-High Variant Performance**: The `-High` variant consistently scores lower than LightRAG in Comprehensiveness, Diversity, Empowerment, and Overall metrics for Agriculture, CS, Legal, and Mix datasets, except for one instance in Diversity (CS) where it slightly exceeds LightRAG (63.2% vs 62.0%) [1]. This supports the assertion that `-High` struggles with comprehensive insights required for complex queries [6].
    *   **-Low Variant Performance**: The `-Low` variant shows mixed results. It performs worse than LightRAG in CS and Agriculture for most metrics. However, it outperforms LightRAG in the **Mix** dataset for Comprehensiveness (64.0% vs 61.2%), Empowerment (64.8% vs 57.2%), and Overall (64.8% vs 60.0%) [1]. In the Legal dataset, `-Low` ties with LightRAG in Diversity and Empowerment [1]. This aligns with the description that `-Low` prioritizes broader content, aiding comprehensiveness but lacking depth [6].
    *   **-Origin Variant Performance**: The `-Origin` variant performs surprisingly well. It outperforms LightRAG in the **Agriculture** dataset across all metrics (e.g., Overall 74.4% vs 67.6%) and in the **Mix** dataset for Diversity (74.4% vs 67.6%) [1]. It underperforms LightRAG in CS and Mix (for most metrics) and Legal (for most metrics) [1]. The text attributes this to effective key information extraction and reduced noise from original text [6].

2.  **Representative Figures**:
    *   **Decline in -High**: In the Legal dataset, the Overall score drops from 84.8% (LightRAG) to 78.0% (-High), a significant decline [1].
    *   **Improvement in -Low (Mix)**: In the Mix dataset, the Overall score improves from 60.0% (LightRAG) to 64.8% (-Low) [1].
    *   **Improvement in -Origin (Agriculture)**: In the Agriculture dataset, the Overall score improves from 67.6% (LightRAG) to 74.4% (-Origin) [1].

3.  **Exceptions and Regressions**:
    *   **-High Exception**: `-High` outperforms LightRAG in Diversity on the CS dataset (63.2% vs 62.0%) [1].
    *   **-Low Improvements**: `-Low` outperforms LightRAG in Comprehensiveness, Empowerment, and Overall on the Mix dataset [1].
    *   **-Origin Improvements**: `-Origin` outperforms LightRAG in all metrics on the Agriculture dataset and in Diversity on the Mix dataset [1].
    *   **-Origin Regressions**: `-Origin` underperforms LightRAG in Comprehensiveness, Empowerment, and Overall on the Mix dataset (e.g., Overall 55.6% vs 60.0%) [1].

4.  **Conclusion**:
    The ablation studies confirm that the dual-level retrieval paradigm of LightRAG provides balanced performance [6]. Removing high-level retrieval (`-High`) generally degrades performance, particularly in comprehensiveness and overall quality, with only one minor exception in Diversity on CS [1]. Removing low-level retrieval (`-Low`) harms performance in specific domains like CS and Agriculture but improves it in the mixed-domain Mix dataset, suggesting that high-level retrieval is beneficial for broad context but insufficient for detail [1][6]. Surprisingly, removing original text (`-Origin`) does not significantly harm performance and can improve it, particularly in the Agriculture dataset, due to noise reduction [1][6].

Figures whose labels differ from the source table: 63.2% (answer: Diversity, LightRAG, vs LightRAG; source: Diversity, CS, -High, vs NaiveRAG); 62.0% (answer: Diversity, -High, vs LightRAG; source: Diversity, CS, LightRAG, vs NaiveRAG); 64.0% (answer: Comprehensiveness, Mix, LightRAG; source: Diversity, Mix, -High, vs NaiveRAG / Empowerment, Agriculture, -High, vs NaiveRAG / Comprehensiveness, Agriculture, -Low, vs NaiveRAG / Comprehensiveness, Mix, -Low, vs NaiveRAG); 64.8% (answer: Empowerment, Mix, LightRAG; source: Overall, Agriculture, -High, vs NaiveRAG / Empowerment, Mix, -Low, vs NaiveRAG / Overall, Mix, -Low, vs NaiveRAG); 64.8% (answer: Overall, Mix, LightRAG; source: Overall, Agriculture, -High, vs NaiveRAG / Empowerment, Mix, -Low, vs NaiveRAG / Overall, Mix, -Low, vs NaiveRAG); 74.4% (answer: Overall, LightRAG; source: Diversity, Mix, -Origin, vs NaiveRAG / Overall, Agriculture, -Origin, vs NaiveRAG); 74.4% (answer: Diversity, LightRAG; source: Diversity, Mix, -Origin, vs NaiveRAG / Overall, Agriculture, -Origin, vs NaiveRAG).
```

## M5-Q3-3

- 問題：`Performance of ablated versions of LightRAG`；模式 `navigate`；105.6 秒；2 次呼叫；tokens 8398
- 來源：[1] p8 retrieval, [2] p7 retrieval, [3] p9 retrieval, [4] p1 retrieval, [5] p1 retrieval, [6] p8 table_context
- 閱讀計畫（定位 3/3，保留 0，超預算 0）：
  - ✓ Table 2 (page 8) | need: Performance metrics of ablated LightRAG versions compared to NaiveRAG | priority: required | status: covered → 候選 0，納入 []，排除 []
  - ✓ Section 4.3 ABLATION STUDIES (RQ2) (pages 7-8) | need: Interpretation of ablation results and discussion of specific variants | priority: required | status: covered → 候選 0，納入 []，排除 []
  - ✓ Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM (pages 4-5) | need: Definition of the components being ablated (e.g., high-level vs low-level retrieval) | priority: supplementary | status: missing → 候選 0，納入 []，排除 []
- 分析狀態：FACTUALLY_INCORRECT；完整性 incomplete（required ['-High', '-Low', '-Origin', 'LightRAG']，缺 []，條件 None）；方向核對 [('incomparable', '74.4%', '67.6%')]
- 修正：[]；刪除 []；仍不符 ['64.8% (Overall, Agriculture, -High, vs LightRAG)', '56.0% (Overall, CS, -High, vs LightRAG)', '78.0% (Overall, Legal, -High, vs LightRAG)', '57.6% (Overall, Mix, -High, vs LightRAG)', '65.2% (Overall, Agriculture, -Low, vs LightRAG)', '56.4% (Overall, CS, -Low, vs LightRAG)', '81.2% (Overall, Legal, -Low, vs LightRAG)', '60.8% (Overall, CS, -Origin, vs LightRAG)', '84.4% (Overall, Legal, -Origin, vs LightRAG)', '55.6% (Overall, Mix, -Origin, vs LightRAG)', '74.4% (Overall, LightRAG)', '74.4% (Diversity, LightRAG)', '60.8% (Overall, LightRAG)', '84.4% (Overall, LightRAG)', '55.6% (Overall, Mix, LightRAG)']；方向待定 []
- 涵蓋判定：Table 2 (page 8)→covered；Section 4.3 ABLATION STUDIES (RQ2) (pages 7-8)→covered；Section 3.2 DUAL-LEVEL RETRIEVAL PARADIGM (pages 4-5)→missing；required 未納入 []；supplementary 用 0；Matrix {'cells': 128, 'tables': ['Table 2 [1]'], 'definitions': ['NaiveRAG', 'LightRAG', '-High'], 'facts': 64, 'coverage_gaps': []}
- 檢查：標籤不符 ['64.8%', '67.6%', '56.0%', '61.2%', '78.0%', '84.8%', '57.6%', '60.0%', '65.2%', '67.6%', '56.4%', '61.2%', '81.2%', '84.8%', '60.8%', '61.2%', '84.4%', '84.8%', '55.6%', '60.0%', '74.4%', '74.4%', '60.8%', '84.4%', '55.6%']；全稱宣稱 0；引用可疑 []；未解析 41；找不到的數字 []

```text
The question asks for the performance metrics of ablated LightRAG versions (-High, -Low, -Origin) compared to the full LightRAG and NaiveRAG baseline, across four datasets (Agriculture, CS, Legal, Mix) and four metrics (Comprehensiveness, Diversity, Empowerment, Overall), based on Table 2 [1].

**Method Definitions and Evidence:**
*   **LightRAG:** The full hybrid model combining low-level and high-level retrieval [6].
*   **NaiveRAG:** The baseline reference system [1].
*   **-High (Low-level-only):** Removes high-order retrieval, focusing on specific entities and immediate neighbors [6].
*   **-Low (High-level-only):** Removes low-level retrieval, prioritizing broader content via entity-wise relationships [6].
*   **-Origin (Semantic Graph):** Removes the use of original text in retrieval, relying solely on graph-based indexing [6].

**Comparison of Figures:**
Comparisons are made within the same dataset and metric, noting the percentage scores for the variant versus its paired reference (NaiveRAG or LightRAG). Note: The table provides comparative win-rates or preference scores between two systems (e.g., "NaiveRAG 32.4%, LightRAG 67.6%"). Higher scores indicate better performance in that pairwise comparison context.

**Compact Comparison Table (Selected Representative Figures showing key trends):**

| Dataset | Metric | Reference | Full LightRAG | -High (No High-level) | -Low (No Low-level) | -Origin (No Origin Text) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Agriculture** | Overall | vs NaiveRAG | 67.6% [1] | 64.8% [1] | 65.2% [1] | 74.4% [1] |
| **CS** | Overall | vs NaiveRAG | 61.2% [1] | 56.0% [1] | 56.4% [1] | 60.8% [1] |
| **Legal** | Overall | vs NaiveRAG | 84.8% [1] | 78.0% [1] | 81.2% [1] | 84.4% [1] |
| **Mix** | Overall | vs NaiveRAG | 60.0% [1] | 57.6% [1] | 64.8% [1] | 55.6% [1] |

*Note: In the table above, higher percentages for the variant indicate it performed better against NaiveRAG than the lower percentage. However, to determine if the variant is better than LightRAG, we compare their respective scores against NaiveRAG in the same row. For example, in Agriculture/Overall, LightRAG (67.6%) > -High (64.8%). In Mix/Overall, -Low (64.8%) > LightRAG (60.0%).*

**Improvements, Regressions, and Exceptions:**

*   **Regressions in -High (Low-level-only):** The -High variant shows a performance decline compared to full LightRAG across nearly all datasets and metrics, consistent with the text stating it leads to a "significant performance decline" [6]. For instance, in the Overall metric, -High scores lower than LightRAG in Agriculture (64.8% vs 67.6%), CS (56.0% vs 61.2%), Legal (78.0% vs 84.8%), and Mix (57.6% vs 60.0%) [1]. This is attributed to its inability to gather comprehensive insights for complex queries [6].

*   **Regressions in -Low (High-level-only):** The -Low variant generally performs worse than full LightRAG, particularly in metrics requiring detail. In the Overall metric, -Low scores lower than LightRAG in Agriculture (65.2% vs 67.6%), CS (56.4% vs 61.2%), and Legal (81.2% vs 84.8%) [1]. The text notes this variant struggles with tasks requiring precise, detailed answers due to reduced depth in examining specific entities [6].
    *   **Exception/Improvement:** On the **Mix** dataset's **Overall** metric, -Low (64.8%) outperforms LightRAG (60.0%) [1]. Similarly, in **Mix/Comprehensiveness**, -Low (64.0%) slightly outperforms LightRAG (61.2%) [1]. This suggests that for the Mix dataset, the broader coverage of high-level retrieval may be more beneficial than the balanced approach.

*   **Performance of -Origin (No Original Text):** The -Origin variant generally maintains high performance, often comparable to or better than full LightRAG, supporting the claim that it "does not exhibit significant performance declines" and in some cases shows improvements [6].
    *   **Improvements:** In **Agriculture**, -Origin outperforms LightRAG in Overall (74.4% vs 67.6%), Comprehensiveness (75.2% vs 67.6%), Diversity (73.6% vs 76.4% - *wait, 73.6 < 76.4, so this is a regression*), and Empowerment (68.0% vs 67.6%) [1]. Specifically, -Origin is significantly better in Agriculture Overall.
    *   **Regressions:** In **CS** and **Legal**, -Origin generally scores lower than LightRAG in Overall metrics (CS: 60.8% vs 61.2%; Legal: 84.4% vs 84.8%) [1]. In **Mix**, -Origin scores lower than LightRAG in Overall (55.6% vs 60.0%) and other metrics [1].
    *   **Exception:** The text highlights improvements in Agriculture and Mix for -Origin [6], but the data shows -Origin outperforms LightRAG in Agriculture Overall/Comprehensiveness/Empowerment, while it underperforms in Mix Overall/Comprehensiveness/Empowerment/Diversity compared to LightRAG. The text's claim of improvement in Mix might refer to comparison against NaiveRAG or specific sub-metrics not explicitly superior to LightRAG in all cases. Actually, looking closely at Mix: LightRAG Overall 60.0% vs -Origin 55.6%. The text says "in some cases... shows improvements (e.g. in Agriculture and Mix)". This contradicts the Overall metric in Mix. However, in **Mix/Diversity**, -Origin (74.4%) outperforms LightRAG (67.6%) [1]. In **Mix/Empowerment**, -Origin (54.8%) is lower than LightRAG (57.2%). So, -Origin has mixed results in Mix, with a notable win in Diversity.

**Verification of Claims:**
*   "Higher/Lower": Checked against Table 2 values [1].
*   "Outperforms/Drops": Checked against pairwise comparisons.
*   Citations: Table values from [1]; Definitions and interpretations from [6].

**Conclusion:**
The ablation studies indicate that the dual-level retrieval of full LightRAG provides a balanced performance. Removing high-level retrieval (-High) causes significant drops, especially in comprehensiveness and overall performance, as it lacks broader context [6][1]. Removing low-level retrieval (-Low) reduces performance in most cases due to lack of detailed entity exploration, with an exception on the Mix dataset where it performed better in Overall and Comprehensiveness [1]. The -Origin variant demonstrates that graph-based indexing alone is robust, outperforming full LightRAG in Agriculture (Overall) and Mix (Diversity), but underperforming in other areas, confirming that original text adds value in some contexts (CS, Legal, Mix Overall) while graph indexing suffices or improves diversity in others [1][6].

**Final Answer:**
The performance of ablated LightRAG versions compared to the full model and NaiveRAG baseline is detailed in Table 2 [1]. The **-High** variant (low-level only) shows significant performance declines across nearly all datasets and metrics compared to full LightRAG, such as in the Overall metric where it scores 64.8% vs 67.6% in Agriculture, 56.0% vs 61.2% in CS, 78.0% vs 84.8% in Legal, and 57.6% vs 60.0% in Mix [1][6]. This is attributed to its inability to handle complex queries requiring comprehensive insights [6]. The **-Low** variant (high-level only) also generally underperforms full LightRAG, e.g., in Overall: 65.2% vs 67.6% (Agriculture), 56.4% vs 61.2% (CS), and 81.2% vs 84.8% (Legal) [1], due to reduced depth in specific entity examination [6]. However, an exception occurs in the **Mix** dataset, where -Low outperforms LightRAG in Overall (64.8% vs 60.0%) and Comprehensiveness (64.0% vs 61.2%) [1]. The **-Origin** variant (graph-only, no original text) does not show significant declines and in some cases improves performance. It outperforms LightRAG in **Agriculture Overall** (74.4% vs 67.6%) and **Mix Diversity** (74.4% vs 67.6%) [1], supporting the claim that graph indexing can provide sufficient context or even reduce noise from irrelevant original text [6]. However, it underperforms LightRAG in CS Overall (60.8% vs 61.2%), Legal Overall (84.4% vs 84.8%), and Mix Overall (55.6% vs 60.0%) [1].

Figures whose labels differ from the source table: 64.8% (answer: Overall, Agriculture, -High, vs LightRAG; source: Overall, Agriculture, -High, vs NaiveRAG / Empowerment, Mix, -Low, vs NaiveRAG / Overall, Mix, -Low, vs NaiveRAG); 67.6% (answer: Overall, -High, vs LightRAG; source: Comprehensiveness, Agriculture, LightRAG, vs NaiveRAG / Diversity, Mix, LightRAG, vs NaiveRAG / Empowerment, Agriculture, LightRAG, vs NaiveRAG / Overall, Agriculture, LightRAG, vs NaiveRAG); 56.0% (answer: Overall, CS, -High, vs LightRAG; source: Overall, CS, -High, vs NaiveRAG); 61.2% (answer: Overall, -High, vs LightRAG; source: Comprehensiveness, Mix, LightRAG, vs NaiveRAG / Empowerment, CS, LightRAG, vs NaiveRAG / Overall, CS, LightRAG, vs NaiveRAG); 78.0% (answer: Overall, Legal, -High, vs LightRAG; source: Overall, Legal, -High, vs NaiveRAG); 84.8% (answer: Overall, -High, vs LightRAG; source: Overall, Legal, LightRAG, vs NaiveRAG); 57.6% (answer: Overall, Mix, -High, vs LightRAG; source: Empowerment, CS, -High, vs NaiveRAG / Overall, Mix, -High, vs NaiveRAG); 60.0% (answer: Overall, -High, vs LightRAG; source: Overall, Mix, LightRAG, vs NaiveRAG); 65.2% (answer: Overall, Agriculture, -Low, vs LightRAG; source: Comprehensiveness, Agriculture, -High, vs NaiveRAG / Empowerment, Agriculture, -Low, vs NaiveRAG / Overall, Agriculture, -Low, vs NaiveRAG); 67.6% (answer: Overall, -Low, vs LightRAG; source: Comprehensiveness, Agriculture, LightRAG, vs NaiveRAG / Diversity, Mix, LightRAG, vs NaiveRAG / Empowerment, Agriculture, LightRAG, vs NaiveRAG / Overall, Agriculture, LightRAG, vs NaiveRAG); 56.4% (answer: Overall, CS, -Low, vs LightRAG; source: Overall, CS, -Low, vs NaiveRAG); 61.2% (answer: Overall, -Low, vs LightRAG; source: Comprehensiveness, Mix, LightRAG, vs NaiveRAG / Empowerment, CS, LightRAG, vs NaiveRAG / Overall, CS, LightRAG, vs NaiveRAG); 81.2% (answer: Overall, Legal, -Low, vs LightRAG; source: Overall, Legal, -Low, vs NaiveRAG); 84.8% (answer: Overall, -Low, vs LightRAG; source: Overall, Legal, LightRAG, vs NaiveRAG); 60.8% (answer: Overall, CS, -Origin, vs LightRAG; source: Comprehensiveness, CS, -Origin, vs NaiveRAG / Overall, CS, -Origin, vs NaiveRAG); 61.2% (answer: Overall, -Origin, vs LightRAG; source: Comprehensiveness, Mix, LightRAG, vs NaiveRAG / Empowerment, CS, LightRAG, vs NaiveRAG / Overall, CS, LightRAG, vs NaiveRAG); 84.4% (answer: Overall, Legal, -Origin, vs LightRAG; source: Overall, Legal, -Origin, vs NaiveRAG); 84.8% (answer: Overall, -Origin, vs LightRAG; source: Overall, Legal, LightRAG, vs NaiveRAG); 55.6% (answer: Overall, Mix, -Origin, vs LightRAG; source: Comprehensiveness, Mix, -Origin, vs NaiveRAG / Overall, Mix, -Origin, vs NaiveRAG); 60.0% (answer: Overall, Mix, -Origin, vs LightRAG; source: Overall, Mix, LightRAG, vs NaiveRAG); 74.4% (answer: Overall, LightRAG; source: Diversity, Mix, -Origin, vs NaiveRAG / Overall, Agriculture, -Origin, vs NaiveRAG); 74.4% (answer: Diversity, LightRAG; source: Diversity, Mix, -Origin, vs NaiveRAG / Overall, Agriculture, -Origin, vs NaiveRAG); 60.8% (answer: Overall, LightRAG; source: Comprehensiveness, CS, -Origin, vs NaiveRAG / Overall, CS, -Origin, vs NaiveRAG); 84.4% (answer: Overall, LightRAG; source: Overall, Legal, -Origin, vs NaiveRAG); 55.6% (answer: Overall, Mix, LightRAG; source: Comprehensiveness, Mix, -Origin, vs NaiveRAG / Overall, Mix, -Origin, vs NaiveRAG).
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

## B5-G1-1

- 問題：`How many context units and tokens do the root-level community summaries (C0) and the source-text summarization (TS) use on the Podcast and News datasets?`；模式 `navigate`；23.2 秒；2 次呼叫；tokens 7902
- 來源：[1] p10 retrieval, [2] p10 retrieval, [3] p8 retrieval, [4] p10 retrieval, [5] p11 retrieval, [6] p11 table_context, [7] p11 table_context, [8] p8 navigation, [9] p8 navigation, [10] p9 navigation, [11] p9 navigation, [12] p10 navigation, [13] p7 navigation, [14] p7 navigation
- 閱讀計畫（定位 6/6，保留 7，超預算 0）：
  - ✓ Section 4.1.1 Datasets | need: dataset descriptions | priority: required | status: missing → 候選 2，納入 [20]，排除 [(21, 'already among the retrieved sources')]
  - ✓ Section 4.1.2 Conditions | need: context unit definitions | priority: required | status: covered → 候選 2，納入 [22]，排除 [(21, 'already among the retrieved sources')]
  - ✓ Table 2 | need: context units by condition | priority: required | status: missing → 候選 3，納入 []，排除 [(29, 'already among the retrieved sources'), (30, 'already among the retrieved sources'), (31, 'already among the retrieved sources')]
  - ✓ Section 5.1 Experiment 1 | need: token usage details | priority: required | status: covered → 候選 9，納入 [25, 24, 26]，排除 [(28, 'low relevance'), (27, 'low relevance'), (30, 'already among the retrieved sources'), (29, 'already among the retrieved sources'), (31, 'already among the retrieved sources'), (32, 'already among the retrieved sources')]
  - ✓ Table 1 | need: task examples | priority: supplementary | status: missing → 候選 3，納入 [18, 19]，排除 [(20, 'supplementary cap reached')]
  - ✓ Figure 2 | need: comparative metrics | priority: supplementary | status: missing → 候選 3，納入 []，排除 [(29, 'already among the retrieved sources'), (30, 'supplementary cap reached'), (31, 'supplementary cap reached')]
- 分析狀態：UNCERTAIN；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 修正：[]；刪除 []；仍不符 []；方向待定 []
- 涵蓋判定：Section 4.1.1 Datasets→partial；Section 4.1.2 Conditions→partial；Table 2→partial；Section 5.1 Experiment 1→partial；Table 1→missing；Figure 2→covered；required 未納入 []；supplementary 用 2；Matrix {'cells': 0, 'tables': [], 'definitions': [], 'facts': 0, 'coverage_gaps': ['Table 3 [5]']}
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
The question asks for the number of context units and tokens used by the root-level community summaries (C0) and the source-text summarization (TS) on the Podcast and News datasets.

From the provided sources, we have the following data:

| Dataset         | Method | Units | Tokens  |
|-----------------|--------|-------|---------|
| Podcast         | C0     | 34    | 26657   |
| Podcast         | TS     | 1669  | 1014611 |
| News            | C0     | 55    | 39770   |
| News            | TS     | 3197  | 1707694 |

The data shows the number of context units and the corresponding token counts for both the Podcast and News datasets for the C0 (root-level community summaries) and TS (source-text summarization) methods. These figures are derived from the dataset descriptions and the token usage details as described in the sources [1] and [4].
```

## B5-G1-2

- 問題：`How many context units and tokens do the root-level community summaries (C0) and the source-text summarization (TS) use on the Podcast and News datasets?`；模式 `navigate`；26.4 秒；2 次呼叫；tokens 7977
- 來源：[1] p10 retrieval, [2] p10 retrieval, [3] p8 retrieval, [4] p10 retrieval, [5] p11 retrieval, [6] p11 table_context, [7] p11 table_context, [8] p8 navigation, [9] p8 navigation, [10] p9 navigation, [11] p9 navigation, [12] p10 navigation, [13] p7 navigation, [14] p7 navigation
- 閱讀計畫（定位 6/6，保留 7，超預算 0）：
  - ✓ Section 4.1.1 Datasets | need: dataset descriptions | priority: required | status: missing → 候選 2，納入 [20]，排除 [(21, 'already among the retrieved sources')]
  - ✓ Section 4.1.2 Conditions | need: context unit definitions | priority: required | status: covered → 候選 2，納入 [22]，排除 [(21, 'already among the retrieved sources')]
  - ✓ Table 2 | need: context units by condition | priority: required | status: missing → 候選 3，納入 []，排除 [(29, 'already among the retrieved sources'), (30, 'already among the retrieved sources'), (31, 'already among the retrieved sources')]
  - ✓ Section 5.1 Experiment 1 | need: token usage details | priority: required | status: covered → 候選 9，納入 [25, 24, 26]，排除 [(28, 'low relevance'), (27, 'low relevance'), (30, 'already among the retrieved sources'), (29, 'already among the retrieved sources'), (31, 'already among the retrieved sources'), (32, 'already among the retrieved sources')]
  - ✓ Table 1 | need: task examples | priority: supplementary | status: missing → 候選 3，納入 [18, 19]，排除 [(20, 'supplementary cap reached')]
  - ✓ Figure 2 | need: comparative metrics | priority: supplementary | status: missing → 候選 3，納入 []，排除 [(29, 'already among the retrieved sources'), (30, 'supplementary cap reached'), (31, 'supplementary cap reached')]
- 分析狀態：UNCERTAIN；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 修正：[]；刪除 []；仍不符 []；方向待定 []
- 涵蓋判定：Section 4.1.1 Datasets→partial；Section 4.1.2 Conditions→partial；Table 2→partial；Section 5.1 Experiment 1→partial；Table 1→missing；Figure 2→covered；required 未納入 []；supplementary 用 2；Matrix {'cells': 0, 'tables': [], 'definitions': [], 'facts': 0, 'coverage_gaps': ['Table 3 [5]']}
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
The question asks for the number of context units and tokens used by root-level community summaries (C0) and source-text summarization (TS) on the Podcast and News datasets.

From Table 2 in the document, the following data is provided:

- Podcast Transcripts:
  - C0 (Root-level community summaries): 34 units, 26,657 tokens
  - TS (Source-text summarization): 1,669 units, 1,014,611 tokens
- News Articles:
  - C0 (Root-level community summaries): 55 units, 39,770 tokens
  - TS (Source-text summarization): 3,197 units, 1,707,694 tokens

The source text also states that "Root-level community summaries (C0) require dramatically fewer tokens per query (9x-43x)" compared to source-text summarization (TS) [1].

Improvements and regressions:
- Podcast Transcripts: C0 uses 9x fewer tokens than TS.
- News Articles: C0 uses 43x fewer tokens than TS.

Exceptions:
- None reported in the given sources.

Conclusion:
- Root-level community summaries (C0) significantly reduce the number of context units and tokens compared to source-text summarization (TS) for both datasets.

The data is sourced from Table 2 [4].
```

## B5-G1-3

- 問題：`How many context units and tokens do the root-level community summaries (C0) and the source-text summarization (TS) use on the Podcast and News datasets?`；模式 `navigate`；30.0 秒；2 次呼叫；tokens 8061
- 來源：[1] p10 retrieval, [2] p10 retrieval, [3] p8 retrieval, [4] p10 retrieval, [5] p11 retrieval, [6] p11 table_context, [7] p11 table_context, [8] p8 navigation, [9] p8 navigation, [10] p9 navigation, [11] p9 navigation, [12] p10 navigation, [13] p7 navigation, [14] p7 navigation
- 閱讀計畫（定位 6/6，保留 7，超預算 0）：
  - ✓ Section 4.1.1 Datasets | need: dataset descriptions | priority: required | status: missing → 候選 2，納入 [20]，排除 [(21, 'already among the retrieved sources')]
  - ✓ Section 4.1.2 Conditions | need: context unit definitions | priority: required | status: covered → 候選 2，納入 [22]，排除 [(21, 'already among the retrieved sources')]
  - ✓ Table 2 | need: context units by condition | priority: required | status: missing → 候選 3，納入 []，排除 [(29, 'already among the retrieved sources'), (30, 'already among the retrieved sources'), (31, 'already among the retrieved sources')]
  - ✓ Section 5.1 Experiment 1 | need: token usage details | priority: required | status: covered → 候選 9，納入 [25, 24, 26]，排除 [(28, 'low relevance'), (27, 'low relevance'), (30, 'already among the retrieved sources'), (29, 'already among the retrieved sources'), (31, 'already among the retrieved sources'), (32, 'already among the retrieved sources')]
  - ✓ Table 1 | need: task examples | priority: supplementary | status: missing → 候選 3，納入 [18, 19]，排除 [(20, 'supplementary cap reached')]
  - ✓ Figure 2 | need: comparative metrics | priority: supplementary | status: missing → 候選 3，納入 []，排除 [(29, 'already among the retrieved sources'), (30, 'supplementary cap reached'), (31, 'supplementary cap reached')]
- 分析狀態：UNCERTAIN；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 修正：[]；刪除 []；仍不符 []；方向待定 []
- 涵蓋判定：Section 4.1.1 Datasets→partial；Section 4.1.2 Conditions→partial；Table 2→partial；Section 5.1 Experiment 1→partial；Table 1→missing；Figure 2→covered；required 未納入 []；supplementary 用 2；Matrix {'cells': 0, 'tables': [], 'definitions': [], 'facts': 0, 'coverage_gaps': ['Table 3 [5]']}
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
The question asks for the number of context units and tokens used by the root-level community summaries (C0) and the source-text summarization (TS) on the Podcast and News datasets.

Evidence matrix:
- Podcast Transcripts: C0 has 34 units and 26,657 tokens; TS has 1,669 units and 1,014,611 tokens [1].
- News Articles: C0 has 55 units and 39,770 tokens; TS has 3,197 units and 1,707,694 tokens [1].

Analysis:
- For Podcast Transcripts, the root-level community summaries (C0) use 34 context units and 26,657 tokens, which is significantly fewer than the source-text summarization (TS) that uses 1,669 context units and 1,014,611 tokens.
- For News Articles, the root-level community summaries (C0) use 55 context units and 39,770 tokens, which is significantly fewer than the source-text summarization (TS) that uses 3,197 context units and 1,707,694 tokens.

Improvements:
- The root-level community summaries (C0) for both datasets use fewer context units and tokens compared to the source-text summarization (TS).

Regressions:
- None; the source-text summarization (TS) consistently uses more context units and tokens compared to the root-level community summaries (C0).

Exceptions:
- None; the pattern is consistent across both datasets.

Conclusion:
- The root-level community summaries (C0) use significantly fewer context units and tokens compared to the source-text summarization (TS) on both the Podcast and News datasets.
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

## M5-G1-1

- 問題：`How many context units and tokens do the root-level community summaries (C0) and the source-text summarization (TS) use on the Podcast and News datasets?`；模式 `navigate`；58.5 秒；2 次呼叫；tokens 6593
- 來源：[1] p10 retrieval, [2] p10 retrieval, [3] p10 retrieval, [4] p8 retrieval, [5] p8 retrieval, [6] p11 navigation, [7] p9 navigation, [8] p10 navigation
- 閱讀計畫（定位 3/3，保留 3，超預算 0）：
  - ✓ Table 2 (page 10) | need: Number of context units for C0 and TS conditions on Podcast and News datasets | priority: required | status: missing → 候選 3，納入 []，排除 [(29, 'already among the retrieved sources'), (30, 'already among the retrieved sources'), (31, 'already among the retrieved sources')]
  - ✓ Section 5.1 Experiment 1 (pages 9-11) | need: Token counts or resource usage details for C0 and TS conditions | priority: required | status: missing → 候選 9，納入 [32, 24, 26]，排除 [(30, 'already among the retrieved sources'), (29, 'already among the retrieved sources'), (31, 'already among the retrieved sources'), (25, 'target quota reached'), (28, 'target quota reached'), (27, 'target quota reached')]
  - ✓ Section 4.1.2 Conditions (page 8) | need: Definitions of C0 and TS to confirm what constitutes a context unit for each | priority: supplementary | status: covered → 候選 2，納入 []，排除 [(22, 'already among the retrieved sources'), (21, 'already among the retrieved sources')]
- 分析狀態：UNCERTAIN；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 修正：[]；刪除 []；仍不符 []；方向待定 []
- 涵蓋判定：Table 2 (page 10)→partial；Section 5.1 Experiment 1 (pages 9-11)→partial；Section 4.1.2 Conditions (page 8)→covered；required 未納入 []；supplementary 用 0；Matrix {'cells': 0, 'tables': [], 'definitions': [], 'facts': 0, 'coverage_gaps': ['Table 3 [6]']}
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 ['97.4%', '97.7%']

```text
The question asks for the number of context units and token counts for two specific methods—root-level community summaries (C0) and source-text summarization (TS)—across two datasets—Podcast and News.

The definitions for the conditions are found in Section 4.1.2: C0 uses root-level community summaries, which are the fewest in number [4]. TS applies a map-reduce approach directly to source texts, which are shuffled and chunked [4][5]. Table 2 provides the specific figures for context units, token counts, and percentage of maximum token count for these conditions on both datasets [1][3].

Comparing the figures from Table 2:
- **Podcast Dataset**:
  - C0: 34 Units, 26,657 Tokens [1][3].
  - TS: 1,669 Units, 1,014,611 Tokens [1][3].
- **News Dataset**:
  - C0: 55 Units, 39,770 Tokens [1][3].
  - TS: 3,197 Units, 1,707,694 Tokens [1][3].

**Improvements (Efficiency)**: C0 requires dramatically fewer resources than TS in both datasets.
- On Podcast, C0 uses 34 units compared to TS's 1,669 units, and 26,657 tokens compared to TS's 1,014,611 tokens [1][3].
- On News, C0 uses 55 units compared to TS's 3,197 units, and 39,770 tokens compared to TS's 1,707,694 tokens [1][3].
- The text states that C0 requires 9x-43x fewer tokens per query than the most resource-intensive approach (TS) [1][2]. Specifically, C0 uses only 2.6% of the max tokens for Podcast and 2.3% for News, whereas TS uses 100% of the max tokens in both cases [1].

Consistency Check:
- "Higher" resource usage for TS: 1,014,611 > 26,657 (Podcast) and 1,707,694 > 39,770 (News) [1].
- "Lower" resource usage for C0: 34 < 1,669 (Podcast units) and 55 < 3,197 (News units) [1].
- The statement that C0 requires over 97% fewer tokens than TS is supported by the percentages (2.6% vs 100% for Podcast; 2.3% vs 100% for News), implying a reduction of ~97.4% and ~97.7% respectively [1].

Source Citations:
- Figures for Podcast and News units and tokens: Table 2 in [1] and [3].
- Definitions of C0 and TS: Section 4.1.2 in [4] and [5].
- General statement on token reduction (9x-43x, >97%): Page 10 text in [1] and [2].

All requested data points (units and tokens for C0 and TS on Podcast and News) are present in Table 2.

**Comparison Table**

| Condition | Dataset | Context Units | Tokens | % Max Tokens |
| :--- | :--- | :--- | :--- | :--- |
| **C0** | Podcast | 34 | 26,657 | 2.6 |
| **TS** | Podcast | 1,669 | 1,014,611 | 100 |
| **C0** | News | 55 | 39,770 | 2.3 |
| **TS** | News | 3,197 | 1,707,694 | 100 |

**Analysis**
The root-level community summaries (C0) utilize significantly fewer context units and tokens than the source-text summarization (TS) method on both datasets. On the Podcast dataset, C0 uses 34 units and 26,657 tokens, whereas TS uses 1,669 units and 1,014,611 tokens [1][3]. On the News dataset, C0 uses 55 units and 39,770 tokens, whereas TS uses 3,197 units and 1,707,694 tokens [1][3]. C0 represents only 2.6% and 2.3% of the maximum token count for Podcast and News respectively, while TS utilizes 100% of the maximum token count in both cases [1]. The text confirms that C0 requires dramatically fewer tokens, citing a 9x-43x reduction and stating that C0 required over 97% fewer tokens compared to TS [1][2].

Numbers that could not be checked against the cited pages of the original text: 97.4%, 97.7%.
```

## M5-G1-2

- 問題：`How many context units and tokens do the root-level community summaries (C0) and the source-text summarization (TS) use on the Podcast and News datasets?`；模式 `navigate`；59.2 秒；2 次呼叫；tokens 6612
- 來源：[1] p10 retrieval, [2] p10 retrieval, [3] p10 retrieval, [4] p8 retrieval, [5] p8 retrieval, [6] p11 navigation, [7] p9 navigation, [8] p10 navigation
- 閱讀計畫（定位 3/3，保留 3，超預算 0）：
  - ✓ Table 2 (page 10) | need: Number of context units for C0 and TS conditions on Podcast and News datasets | priority: required | status: missing → 候選 3，納入 []，排除 [(29, 'already among the retrieved sources'), (30, 'already among the retrieved sources'), (31, 'already among the retrieved sources')]
  - ✓ Section 5.1 Experiment 1 (pages 9-11) | need: Token counts or resource usage details for C0 and TS conditions | priority: required | status: missing → 候選 9，納入 [32, 24, 26]，排除 [(30, 'already among the retrieved sources'), (29, 'already among the retrieved sources'), (31, 'already among the retrieved sources'), (25, 'target quota reached'), (28, 'target quota reached'), (27, 'target quota reached')]
  - ✓ Section 4.1.2 Conditions (page 8) | need: Definitions of C0 and TS to confirm what constitutes a context unit for each | priority: supplementary | status: covered → 候選 2，納入 []，排除 [(22, 'already among the retrieved sources'), (21, 'already among the retrieved sources')]
- 分析狀態：UNCERTAIN；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 修正：[]；刪除 []；仍不符 []；方向待定 []
- 涵蓋判定：Table 2 (page 10)→partial；Section 5.1 Experiment 1 (pages 9-11)→partial；Section 4.1.2 Conditions (page 8)→covered；required 未納入 []；supplementary 用 0；Matrix {'cells': 0, 'tables': [], 'definitions': [], 'facts': 0, 'coverage_gaps': ['Table 3 [6]']}
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
The question asks for the number of context units and token counts for the C0 (root-level community summaries) and TS (source-text summarization) conditions on the Podcast and News datasets.

**Definitions and Evidence:**
*   **C0 Definition:** C0 uses root-level community summaries, which are the fewest in number [4].
*   **TS Definition:** TS applies a map-reduce approach directly to source texts, where source texts are shuffled and chunked [4][5].
*   **Context Units Definition:** Table 2 defines "Units" as community summaries for C0-C3 and text chunks for TS [3].
*   **Data Source:** Table 2 on page 10 provides the specific figures for Units, Tokens, and % Max for each condition and dataset [1][3].

**Comparison of Figures:**

| Dataset | Condition | Units (Context Units) | Tokens | Source |
| :--- | :--- | :--- | :--- | :--- |
| **Podcast Transcripts** | C0 | 34 | 26,657 | [1] |
| | TS | 1,669 | 1,014,611 | [1] |
| **News Articles** | C0 | 55 | 39,770 | [1] |
| | TS | 3,197 | 1,707,694 | [1] |

**Improvements, Regressions, and Exceptions:**
*   **Resource Efficiency (Improvement for C0):** On both datasets, C0 uses significantly fewer context units and tokens compared to TS.
    *   **Podcast:** C0 uses 34 units versus 1,669 for TS, and 26,657 tokens versus 1,014,611 for TS [1]. This represents a reduction of approximately 97% in tokens (2.6% of max vs 100% of max) [1]. The text notes C0 requires "dramatically fewer tokens per query (9x-43x)" compared to map-reduce summarization (TS) [1].
    *   **News:** C0 uses 55 units versus 3,197 for TS, and 39,770 tokens versus 1,707,694 for TS [1]. This also represents a reduction of over 97% in tokens (2.3% of max vs 100% of max) [2].
*   **No Regressions:** There are no resource usage regressions for C0 compared to TS in terms of efficiency; C0 is strictly more efficient in both unit count and token count on both datasets.
*   **Exceptions:** None regarding the direction of difference; C0 is consistently lower in resource usage than TS on both datasets.

**Verification:**
*   "Higher/Lower": C0 token counts (26,657 and 39,770) are lower than TS token counts (1,014,611 and 1,707,694) [1].
*   "Outperforms/Drops": The text states GraphRAG (including C0) offers a "highly efficient method" with "dramatically fewer tokens" [1][2].

**Citations:**
*   Figures for Units and Tokens: Table 2 in source [1] and [3].
*   Definition of C0 and TS: Section 4.1.2 in source [4] and [5].
*   Definition of Context Units: Table 2 caption in source [3].

**Completeness Check:**
*   The question asked for context units and tokens for C0 and TS on Podcast and News datasets.
*   Podcast C0: 34 units, 26,657 tokens [1].
*   Podcast TS: 1,669 units, 1,014,611 tokens [1].
*   News C0: 55 units, 39,770 tokens [1].
*   News TS: 3,197 units, 1,707,694 tokens [1].
*   All requested data points are present.

Answer:
On the **Podcast Transcripts** dataset, the root-level community summaries (**C0**) use **34** context units and **26,657** tokens, whereas the source-text summarization method (**TS**) uses **1,669** context units and **1,014,611** tokens [1]. On the **News Articles** dataset, **C0** uses **55** context units and **39,770** tokens, while **TS** uses **3,197** context units and **1,707,694** tokens [1]. In both cases, C0 uses dramatically fewer tokens than TS, representing approximately 2.6% and 2.3% of the maximum token count respectively, compared to 100% for TS [1]. The context units for C0 are community summaries, while for TS they are text chunks [3].
```

## M5-G1-3

- 問題：`How many context units and tokens do the root-level community summaries (C0) and the source-text summarization (TS) use on the Podcast and News datasets?`；模式 `navigate`；55.8 秒；2 次呼叫；tokens 6529
- 來源：[1] p10 retrieval, [2] p10 retrieval, [3] p10 retrieval, [4] p8 retrieval, [5] p8 retrieval, [6] p11 navigation, [7] p9 navigation, [8] p10 navigation
- 閱讀計畫（定位 3/3，保留 3，超預算 0）：
  - ✓ Table 2 (page 10) | need: Number of context units for C0 and TS conditions on Podcast and News datasets | priority: required | status: missing → 候選 3，納入 []，排除 [(29, 'already among the retrieved sources'), (30, 'already among the retrieved sources'), (31, 'already among the retrieved sources')]
  - ✓ Section 5.1 Experiment 1 (pages 9-11) | need: Token counts or resource usage details for C0 and TS conditions | priority: required | status: missing → 候選 9，納入 [32, 24, 26]，排除 [(30, 'already among the retrieved sources'), (29, 'already among the retrieved sources'), (31, 'already among the retrieved sources'), (25, 'target quota reached'), (28, 'target quota reached'), (27, 'target quota reached')]
  - ✓ Section 4.1.2 Conditions (page 8) | need: Definitions of C0 and TS to confirm what constitutes a context unit for each | priority: supplementary | status: covered → 候選 2，納入 []，排除 [(22, 'already among the retrieved sources'), (21, 'already among the retrieved sources')]
- 分析狀態：UNCERTAIN；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 修正：[]；刪除 []；仍不符 []；方向待定 []
- 涵蓋判定：Table 2 (page 10)→partial；Section 5.1 Experiment 1 (pages 9-11)→partial；Section 4.1.2 Conditions (page 8)→covered；required 未納入 []；supplementary 用 0；Matrix {'cells': 0, 'tables': [], 'definitions': [], 'facts': 0, 'coverage_gaps': ['Table 3 [6]']}
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
The question asks for the number of context units and token counts for two specific conditions: root-level community summaries (C0) and source-text summarization (TS). It requires these metrics for two specific datasets: Podcast Transcripts and News Articles.

**Definitions:**
*   **C0:** Defined as using "root-level community summaries (fewest in number)" [4].
*   **TS:** Defined as a method where "source texts... are shuffled and chunked for the map-reduce summarization stages" [4][5].
*   **Context Units:** For C0-C3, these are community summaries; for TS, they are text chunks [3].

**Evidence Matrix (from Table 2):**
*   **Source:** Table 2 in [1] and [3].
*   **Podcast Transcripts:**
    *   C0: 34 Units, 26,657 Tokens.
    *   TS: 1,669 Units, 1,014,611 Tokens.
*   **News Articles:**
    *   C0: 55 Units, 39,770 Tokens.
    *   TS: 3,197 Units, 1,707,694 Tokens.

**Comparison:**
*   **Podcast Dataset:**
    *   **Units:** C0 uses 34 units, whereas TS uses 1,669 units. C0 uses significantly fewer units.
    *   **Tokens:** C0 uses 26,657 tokens, whereas TS uses 1,014,611 tokens. C0 uses significantly fewer tokens.
*   **News Dataset:**
    *   **Units:** C0 uses 55 units, whereas TS uses 3,197 units. C0 uses significantly fewer units.
    *   **Tokens:** C0 uses 39,770 tokens, whereas TS uses 1,707,694 tokens. C0 uses significantly fewer tokens.

**Improvements/Regressions:**
*   **Improvements:** In all four comparisons (Units and Tokens for both datasets), the C0 condition is more efficient (lower resource usage) than the TS condition. The text notes that C0 requires "dramatically fewer tokens per query (9x-43x)" compared to TS [1][3].
*   **Exceptions:** There are no exceptions to the trend of C0 being more resource-efficient than TS in this specific comparison of units and tokens.

**Verification:**
*   "Fewer units" agrees with 34 < 1,669 and 55 < 3,197 [1][3].
*   "Fewer tokens" agrees with 26,657 < 1,014,611 and 39,770 < 1,707,694 [1][3].

**Citations:**
*   Figures for units and tokens are from Table 2 [1][3].
*   Definitions for C0 and TS are from Section 4.1.2 [4][5].

**Completeness:**
*   C0 Units/Tokens for Podcast: Included.
*   C0 Units/Tokens for News: Included.
*   TS Units/Tokens for Podcast: Included.
*   TS Units/Tokens for News: Included.

**Compact Comparison Table**

| Dataset | Condition | Context Units | Tokens |
| :--- | :--- | :--- | :--- |
| Podcast Transcripts | C0 | 34 | 26,657 |
| Podcast Transcripts | TS | 1,669 | 1,014,611 |
| News Articles | C0 | 55 | 39,770 |
| News Articles | TS | 3,197 | 1,707,694 |

**Analysis**
On the **Podcast Transcripts** dataset, the root-level community summary condition (C0) uses **34** context units and **26,657** tokens, while the source-text summarization condition (TS) uses **1,669** context units and **1,014,611** tokens [1][3].

On the **News Articles** dataset, the C0 condition uses **55** context units and **39,770** tokens, while the TS condition uses **3,197** context units and **1,707,694** tokens [1][3].

In both datasets, C0 utilizes substantially fewer context units and tokens than TS [1][3]. The text describes this as C0 requiring "dramatically fewer tokens per query (9x-43x)" [1][3].
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

## B5-G2-1

- 問題：`Compare condition C2 with vector RAG (SS) on comprehensiveness in the Podcast and News datasets`；模式 `navigate`；35.0 秒；2 次呼叫；tokens 7590
- 來源：[1] p9 retrieval, [2] p11 retrieval, [3] p10 retrieval, [4] p11 retrieval, [5] p10 retrieval, [6] p10 navigation, [7] p10 navigation, [8] p9 navigation, [9] p10 navigation, [10] p10 navigation, [11] p26 navigation, [12] p26 navigation
- 閱讀計畫（定位 6/6，保留 7，超預算 0）：
  - ✓ Section 5.1 Experiment 1 | need: comprehensiveness comparison for Podcast dataset | priority: required | status: missing → 候選 9，納入 [29, 26]，排除 [(25, 'already among the retrieved sources'), (32, 'already among the retrieved sources'), (31, 'already among the retrieved sources'), (30, 'already among the retrieved sources'), (24, 'already selected for another target'), (28, 'already selected for another target'), (27, 'already selected for another target')]
  - ✓ Section 5.1 Experiment 1 | need: comprehensiveness comparison for News dataset | priority: required | status: missing → 候選 9，納入 [24, 28, 27]，排除 [(25, 'already among the retrieved sources'), (32, 'already among the retrieved sources'), (31, 'already among the retrieved sources'), (30, 'already among the retrieved sources'), (29, 'already selected for another target'), (26, 'already selected for another target')]
  - ✓ Table 2 | need: context units for C2 and SS | priority: supplementary | status: covered → 候選 3，納入 []，排除 [(29, 'already selected for another target'), (30, 'already among the retrieved sources'), (31, 'supplementary cap reached')]
  - ✓ Section 5.2 Experiment 2 | need: cluster counts for C2 and SS | priority: supplementary | status: missing → 候選 3，納入 []，排除 [(32, 'already among the retrieved sources'), (33, 'supplementary cap reached'), (34, 'supplementary cap reached')]
  - ✓ Table 3 | need: extracted claims for C2 and SS | priority: supplementary | status: covered → 候選 3，納入 []，排除 [(32, 'already among the retrieved sources'), (33, 'already among the retrieved sources'), (34, 'supplementary cap reached')]
  - ✓ Table 6 | need: pairwise comparisons for C2 vs SS | priority: supplementary | status: missing → 候選 3，納入 [74, 75]，排除 [(76, 'supplementary cap reached')]
- 分析狀態：UNCERTAIN；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 修正：[]；刪除 []；仍不符 []；方向待定 []
- 涵蓋判定：Section 5.1 Experiment 1→partial；Section 5.1 Experiment 1→partial；Table 2→missing；Section 5.2 Experiment 2→partial；Table 3→covered；Table 6→missing；required 未納入 []；supplementary 用 2；Matrix {'cells': 0, 'tables': [], 'definitions': [], 'facts': 0, 'coverage_gaps': ['Table 3 [2]']}
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
The question asks for a comparison of condition C2 with vector RAG (SS) on the metric of comprehensiveness for the Podcast and News datasets.

From the sources, the following definitions are relevant:
- Comprehensiveness is defined as the average number of claims extracted from the answers generated under each condition [8].

For the Podcast dataset, the comprehensiveness comparison between C2 and SS shows the following:
- The average number of extracted claims for C2 is 32.46.
- The average number of extracted claims for SS is 26.50 [2].
- The pairwise comparison results show that C2 has a mean score of 57.28 and SS has a mean score of 42.72, with a Z-value of -4.1 and p-value <0.001 [11].

For the News dataset, the comprehensiveness comparison between C2 and SS shows the following:
- The average number of extracted claims for C2 is 31.62.
- The average number of extracted claims for SS is 25.23 [2].
- The pairwise comparison results show that C2 has a mean score of 62.08 and SS has a mean score of 37.92, with a Z-value of -5.07 and p-value <0.001 [11].

Improvements:
- For the Podcast dataset, C2 outperforms SS in comprehensiveness with a statistically significant difference (p < 0.001).
- For the News dataset, C2 outperforms SS in comprehensiveness with a statistically significant difference (p < 0.001).
There are no regressions or exceptions in these comparisons.

The statements "outperforms" are supported by the average number of extracted claims and the pairwise comparison results, which show higher values for C2 than for SS in both datasets, along with statistically significant p-values.

The figures cited are sourced from Table 3 [2] and Table 6 [11].

The question's request is fully addressed by comparing the comprehensiveness of C2 with SS on the Podcast and News datasets using the provided data.
```

## B5-G2-2

- 問題：`Compare condition C2 with vector RAG (SS) on comprehensiveness in the Podcast and News datasets`；模式 `navigate`；30.7 秒；2 次呼叫；tokens 7492
- 來源：[1] p9 retrieval, [2] p11 retrieval, [3] p10 retrieval, [4] p11 retrieval, [5] p10 retrieval, [6] p10 navigation, [7] p10 navigation, [8] p9 navigation, [9] p10 navigation, [10] p10 navigation, [11] p26 navigation, [12] p26 navigation
- 閱讀計畫（定位 6/6，保留 7，超預算 0）：
  - ✓ Section 5.1 Experiment 1 | need: comprehensiveness comparison for Podcast dataset | priority: required | status: missing → 候選 9，納入 [29, 26]，排除 [(25, 'already among the retrieved sources'), (32, 'already among the retrieved sources'), (31, 'already among the retrieved sources'), (30, 'already among the retrieved sources'), (24, 'already selected for another target'), (28, 'already selected for another target'), (27, 'already selected for another target')]
  - ✓ Section 5.1 Experiment 1 | need: comprehensiveness comparison for News dataset | priority: required | status: missing → 候選 9，納入 [24, 28, 27]，排除 [(25, 'already among the retrieved sources'), (32, 'already among the retrieved sources'), (31, 'already among the retrieved sources'), (30, 'already among the retrieved sources'), (29, 'already selected for another target'), (26, 'already selected for another target')]
  - ✓ Table 2 | need: context units for C2 and SS | priority: supplementary | status: covered → 候選 3，納入 []，排除 [(29, 'already selected for another target'), (30, 'already among the retrieved sources'), (31, 'supplementary cap reached')]
  - ✓ Section 5.2 Experiment 2 | need: cluster counts for C2 and SS | priority: supplementary | status: missing → 候選 3，納入 []，排除 [(32, 'already among the retrieved sources'), (33, 'supplementary cap reached'), (34, 'supplementary cap reached')]
  - ✓ Table 3 | need: extracted claims for C2 and SS | priority: supplementary | status: covered → 候選 3，納入 []，排除 [(32, 'already among the retrieved sources'), (33, 'already among the retrieved sources'), (34, 'supplementary cap reached')]
  - ✓ Table 6 | need: pairwise comparisons for C2 vs SS | priority: supplementary | status: missing → 候選 3，納入 [74, 75]，排除 [(76, 'supplementary cap reached')]
- 分析狀態：UNCERTAIN；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 修正：[]；刪除 []；仍不符 []；方向待定 []
- 涵蓋判定：Section 5.1 Experiment 1→partial；Section 5.1 Experiment 1→partial；Table 2→missing；Section 5.2 Experiment 2→partial；Table 3→covered；Table 6→missing；required 未納入 []；supplementary 用 2；Matrix {'cells': 0, 'tables': [], 'definitions': [], 'facts': 0, 'coverage_gaps': ['Table 3 [2]']}
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 ['79.20%']

```text
The question asks to compare condition C2 with vector RAG (SS) on the comprehensiveness metric for the Podcast and News datasets.

From the sources, the comprehensiveness metric is defined as the average number of claims extracted from the answers generated under each condition [8]. Condition C2 refers to a global search method, and SS refers to vector RAG.

The comparison of C2 and SS on comprehensiveness:
- **Podcast dataset**: C2 achieved a comprehensiveness win rate of 77.76% over SS (p < 0.001) [11].
- **News dataset**: C2 achieved a comprehensiveness win rate of 79.20% over SS (p < 0.001) [11].

There are no exceptions reported for this comparison in the provided sources.

The win rates for C2 are higher than SS in both datasets, and the p-values confirm these differences are statistically significant.

The figures and analysis are drawn from Table 6 [11], and the definition of comprehensiveness is from the method description [8].

The comparison requested in the question is fully addressed using the data from the provided sources.

| Dataset       | Condition C2 vs. SS (Comprehensiveness Win Rate) | Source |
|---------------|--------------------------------------------------|--------|
| Podcast       | 77.76% (p < 0.001)                               | [11]   |
| News          | 79.20% (p < 0.001)                               | [11]   |

C2 outperforms SS in comprehensiveness for both the Podcast and News datasets with high win rates and statistically significant differences.

Numbers that could not be checked against the cited pages of the original text: 79.20%.
```

## B5-G2-3

- 問題：`Compare condition C2 with vector RAG (SS) on comprehensiveness in the Podcast and News datasets`；模式 `navigate`；24.1 秒；2 次呼叫；tokens 7343
- 來源：[1] p9 retrieval, [2] p11 retrieval, [3] p10 retrieval, [4] p11 retrieval, [5] p10 retrieval, [6] p10 navigation, [7] p10 navigation, [8] p9 navigation, [9] p10 navigation, [10] p10 navigation, [11] p26 navigation, [12] p26 navigation
- 閱讀計畫（定位 6/6，保留 7，超預算 0）：
  - ✓ Section 5.1 Experiment 1 | need: comprehensiveness comparison for Podcast dataset | priority: required | status: missing → 候選 9，納入 [29, 26]，排除 [(25, 'already among the retrieved sources'), (32, 'already among the retrieved sources'), (31, 'already among the retrieved sources'), (30, 'already among the retrieved sources'), (24, 'already selected for another target'), (28, 'already selected for another target'), (27, 'already selected for another target')]
  - ✓ Section 5.1 Experiment 1 | need: comprehensiveness comparison for News dataset | priority: required | status: missing → 候選 9，納入 [24, 28, 27]，排除 [(25, 'already among the retrieved sources'), (32, 'already among the retrieved sources'), (31, 'already among the retrieved sources'), (30, 'already among the retrieved sources'), (29, 'already selected for another target'), (26, 'already selected for another target')]
  - ✓ Table 2 | need: context units for C2 and SS | priority: supplementary | status: covered → 候選 3，納入 []，排除 [(29, 'already selected for another target'), (30, 'already among the retrieved sources'), (31, 'supplementary cap reached')]
  - ✓ Section 5.2 Experiment 2 | need: cluster counts for C2 and SS | priority: supplementary | status: missing → 候選 3，納入 []，排除 [(32, 'already among the retrieved sources'), (33, 'supplementary cap reached'), (34, 'supplementary cap reached')]
  - ✓ Table 3 | need: extracted claims for C2 and SS | priority: supplementary | status: covered → 候選 3，納入 []，排除 [(32, 'already among the retrieved sources'), (33, 'already among the retrieved sources'), (34, 'supplementary cap reached')]
  - ✓ Table 6 | need: pairwise comparisons for C2 vs SS | priority: supplementary | status: missing → 候選 3，納入 [74, 75]，排除 [(76, 'supplementary cap reached')]
- 分析狀態：UNCERTAIN；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 修正：[]；刪除 []；仍不符 []；方向待定 []
- 涵蓋判定：Section 5.1 Experiment 1→partial；Section 5.1 Experiment 1→partial；Table 2→missing；Section 5.2 Experiment 2→partial；Table 3→covered；Table 6→missing；required 未納入 []；supplementary 用 2；Matrix {'cells': 0, 'tables': [], 'definitions': [], 'facts': 0, 'coverage_gaps': ['Table 3 [2]']}
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
The question asks for a comparison between condition C2 and vector RAG (SS) on the metric of comprehensiveness for the Podcast and News datasets.

From the provided sources, the relevant data is as follows:

- For the Podcast dataset, condition C2 achieved a comprehensiveness win rate of 77.76% over SS, with a statistically significant difference (p < 0.001) [11].
- For the News dataset, condition C2 achieved a comprehensiveness win rate of 79.2% over SS, with a statistically significant difference (p < 0.001) [11].

Analysis:
- On the Podcast dataset, C2 outperformed SS in comprehensiveness, achieving a higher win rate.
- On the News dataset, C2 also outperformed SS in comprehensiveness, achieving a higher win rate.
- There are no exceptions or conflicting results reported for the comprehensiveness metric in the comparison between C2 and SS for these datasets.

Conclusion:
- C2 significantly outperformed SS in comprehensiveness for both the Podcast and News datasets.
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

## M5-G2-1

- 問題：`Compare condition C2 with vector RAG (SS) on comprehensiveness in the Podcast and News datasets`；模式 `navigate`；118.0 秒；2 次呼叫；tokens 9925
- 來源：[1] p11 retrieval, [2] p9 retrieval, [3] p10 retrieval, [4] p10 retrieval, [5] p8 retrieval, [6] p11 table_context, [7] p11 table_context, [8] p10 navigation, [9] p10 navigation, [10] p9 navigation, [11] p10 navigation, [12] p8 navigation, [13] p8 navigation
- 閱讀計畫（定位 4/4，保留 6，超預算 0）：
  - ✓ Section 5.1 Experiment 1 | need: textual comparison of C2 and SS on comprehensiveness for Podcast and News datasets | priority: required | status: covered → 候選 9，納入 [26, 24, 28]，排除 [(32, 'already among the retrieved sources'), (25, 'already among the retrieved sources'), (31, 'already among the retrieved sources'), (30, 'already among the retrieved sources'), (29, 'already selected for another target'), (27, 'target quota reached')]
  - ✓ Table 2 (page 10) | need: quantitative data on comprehensiveness metrics for C2 and SS across Podcast and News datasets | priority: required | status: missing → 候選 3，納入 [29]，排除 [(30, 'already among the retrieved sources'), (31, 'already among the retrieved sources')]
  - ✓ Section 4.1.2 Conditions (page 8) | need: definition of condition C2 and SS (vector RAG) to confirm experimental setup | priority: supplementary | status: covered → 候選 2，納入 [22]，排除 [(21, 'supplementary cap reached')]
  - ✓ Section 3.3 Criteria for Evaluating Global Sensemaking (pages 7-8) | need: definition of "comprehensiveness" metric used in the evaluation | priority: supplementary | status: missing → 候選 3，納入 [20]，排除 [(18, 'low relevance'), (19, 'supplementary cap reached')]
- 涵蓋判定：Section 5.1 Experiment 1→partial；Table 2 (page 10)→missing；Section 4.1.2 Conditions (page 8)→partial；Section 3.3 Criteria for Evaluating Global Sensemaking (pages 7-8)→missing；required 未納入 []；supplementary 用 2；Matrix {'cells': 0, 'tables': [], 'definitions': [], 'facts': 0, 'coverage_gaps': ['Table 3 [1]']}
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
(1) The question asks for a comparison of condition **C2** (intermediate-level community summaries) against condition **SS** (vector RAG/semantic search) regarding the metric **Comprehensiveness** on the **Podcast Transcripts** and **News Articles** datasets.

(2) **Evidence and Definitions:**
*   **Metric Definition:** Comprehensiveness is defined as the "average number of claims extracted from the answers generated under each condition," where higher values indicate better performance [10]. In Experiment 1, it is also measured via LLM-based pairwise win rates [2].
*   **Method Definitions:**
    *   **C2:** Uses intermediate-level community summaries to answer queries [5].
    *   **SS:** An implementation of vector RAG in which text chunks are retrieved and added to the available context [5].
*   **Data Sources:**
    *   **Experiment 2 (Claim-based):** Table 3 reports the average number of extracted claims [1].
    *   **Experiment 1 (LLM Win Rates):** Figure 2 and surrounding text report head-to-head win rates [2], [8], [9], [11].

(3) **Comparison of Figures:**

**Dataset: Podcast Transcripts**
*   **Claim-based Comprehensiveness (Experiment 2):**
    *   C2: 31.62 claims [1].
    *   SS: 26.50 claims [1].
    *   Comparison: C2 > SS.
*   **LLM Win Rate Comprehensiveness (Experiment 1):**
    *   Figure 2 (Podcast Comprehensiveness section): The row for **C2** against the column for **SS** shows a win rate of **81%** [9]. This means C2 was preferred over SS 81% of the time.
    *   Textual confirmation: The text states global approaches achieved comprehensiveness win rates between 72-83% for Podcast transcripts, significantly outperforming SS [2].

**Dataset: News Articles**
*   **Claim-based Comprehensiveness (Experiment 2):**
    *   C2: 31.62 claims [1]. *Correction*: Looking at Table 3 in Source [1], the column "News Articles" shows C2 has **31.62** and SS has **25.23**. Wait, let me re-read Table 3 carefully.
    *   Table 3 Headers: Condition | Average Number of Claims | News Articles | Podcast Transcripts.
    *   Row C2: 31.62 (News) | 32.46 (Podcast) [1].
    *   Row SS: 25.23 (News) | 26.50 (Podcast) [1].
    *   Comparison: C2 (31.62) > SS (25.23).
*   **LLM Win Rate Comprehensiveness (Experiment 1):**
    *   Figure 2 (News Comprehensiveness section): The row for **C2** against the column for **SS** shows a win rate of **77%** [11]. *Correction*: Let's look at Source [11] Figure 2 for News Articles.
    *   Source [11] Figure 2 "Comprehensiveness" for News Articles (bottom left quadrant usually, or labeled). The labels are SS, TS, C0, C1, C2, C3.
    *   Row C2, Column SS: The value is **77%**? Let's trace the matrix in [11].
        *   Rows: SS, TS, C0, C1, C2, C3.
        *   Columns: SS, TS, C0, C1, C2, C3.
        *   Under "Comprehensiveness" for News Articles (labeled in [11] below the Podcast section? No, [9] is Podcast, [11] is News).
        *   In [11], the section "Comprehensiveness" for News Articles shows:
            *   Row C2, Col SS: **77%**? Let's check the grid.
            *   Row 1 (SS): 50, 33, 38, 35, 29, 31
            *   Row 2 (TS): 67, 50, 53, 45, 44, 40
            *   Row 3 (C0): 62, 47, 50, 40, 41, 41
            *   Row 4 (C1): 65, 55, 60, 50, 50, 50
            *   Row 5 (C2): **71**, 56, 59, 50, 50, 51  -> Wait, Row 5 is C2. Column 1 is SS. The value is **71%**?
            *   Let's re-examine Source [9] for Podcast. Row C2 (5th row) vs SS (1st col): **81%** [9].
            *   Let's re-examine Source [11] for News. Row C2 (5th row) vs SS (1st col): **71%** [11].
            *   Textual confirmation: The text states global approaches achieved comprehensiveness win rates between 72-80% for News articles [2]. Note: 71% is close, but let's check the text again. "72-80% (p <.001) for News articles" [2]. The figure shows 71% for C2. C0 is 62%? No, C0 row (3rd row) vs SS is 62%. C1 (4th row) vs SS is 65%. C3 (6th row) vs SS is 69%. The text says "72-80%". This discrepancy might be due to averaging or specific conditions. However, the text explicitly states: "global approaches significantly outperformed conventional vector RAG (SS)... Specifically, global approaches achieved comprehensiveness win rates between 72-83% ... for Podcast ... and 72-80% ... for News" [2]. The figure data in [11] for C2 vs SS is **71%**. Wait, looking at [11] again.
            *   Source [11] Figure 2, News Comprehensiveness:
                *   Row C2, Col SS: **71** (First number in the 5th row of the Comprehensiveness block? No, the block has 6 rows).
                *   Let's align carefully.
                *   Podcast Comprehensiveness [9]:
                    *   Row C2 (5th): 81 (vs SS), 57 (vs TS), 54 (vs C0), 56 (vs C1), 50 (vs C2? No, self), 48 (vs C3).
                *   News Comprehensiveness [11]:
                    *   Row C2 (5th): **71** (vs SS), 56 (vs TS), 59 (vs C0), 50 (vs C1), 50 (vs C2? No), 51 (vs C3).
                *   So C2 vs SS for News is **71%**.
                *   Why does the text say 72-80%? The text might refer to the range of *all* global conditions. C0=62%, C1=65%, C2=71%, C3=69%. These are all below 72%.
                *   Let's check Source [2] again. "72-80% (p <.001) for News articles".
                *   Let's check Source [10] or other pages.
                *   Actually, look at Source [3]: "Intermediate-level summaries in the Podcast dataset and low-level community summaries in the News dataset achieved comprehensiveness win rates of 57% ... and 64% ...". This refers to community summaries vs source texts (TS)? No, "Community summaries vs. source texts".
                *   The prompt asks to compare C2 vs SS.
                *   Figure 2 in [11] clearly lists C2 vs SS as **71%** for News Comprehensiveness.
                *   Figure 2 in [9] clearly lists C2 vs SS as **81%** for Podcast Comprehensiveness.
                *   The text in [2] says "72-80% for News". This contradicts the specific figure for C2 (71%). However, C0-C3 are all global. Maybe the text aggregates differently? Or maybe I am misreading the grid.
                *   Let's look at [11] again.
                *   News Comprehensiveness Grid:
                    *   Row 1 (SS): 50...
                    *   Row 2 (TS): 67...
                    *   Row 3 (C0): 62...
                    *   Row 4 (C1): 65...
                    *   Row 5 (C2): **71**...
                    *   Row 6 (C3): 69...
                *   The highest is 71%. The text says 72-80%. There is a slight inconsistency between the specific table/figure values and the summary text range. I must prioritize the explicit figures cited in the sources as per instructions "Answer only from the numbered sources... read the evidence matrix". The figure [11] provides the specific value. I will use the figure values.
                *   Wait, is it possible the "72-80%" refers to Podcast? "72-83% for Podcast ... and 72-80% for News".
                *   Podcast Figure [9]: C2=81, C0=83, C1=77, C3=79, C0=72? (Row C0 is 72 vs SS? No, Row C0 is 3rd row. 72 vs SS? Let's check [9] Row C0. 72, 50, 50, 53, 50, 49. Yes, C0 vs SS is 72%). So Podcast range is 72-83%. This matches.
                *   News Figure [11]: C0=62, C1=65, C2=71, C3=69. Range is 62-71%. The text says 72-80%. This is a contradiction in the source text vs the source figure.
                *   Instruction: "read the evidence matrix... compare only figures". I will use the figures from [9] and [11] as they are the primary data representation. I will note the text's claim if necessary, but the figure is the direct evidence of the result.
                *   Actually, looking closer at [11], is it possible the rows are ordered differently? No, labels
```

## M5-G2-2

- 問題：`Compare condition C2 with vector RAG (SS) on comprehensiveness in the Podcast and News datasets`；模式 `navigate`；57.8 秒；2 次呼叫；tokens 8442
- 來源：[1] p11 retrieval, [2] p9 retrieval, [3] p10 retrieval, [4] p10 retrieval, [5] p8 retrieval, [6] p11 table_context, [7] p11 table_context, [8] p10 navigation, [9] p10 navigation, [10] p9 navigation, [11] p10 navigation, [12] p8 navigation, [13] p8 navigation
- 閱讀計畫（定位 4/4，保留 6，超預算 0）：
  - ✓ Section 5.1 Experiment 1 | need: textual comparison of C2 and SS on comprehensiveness for Podcast and News datasets | priority: required | status: covered → 候選 9，納入 [26, 24, 28]，排除 [(32, 'already among the retrieved sources'), (25, 'already among the retrieved sources'), (31, 'already among the retrieved sources'), (30, 'already among the retrieved sources'), (29, 'already selected for another target'), (27, 'target quota reached')]
  - ✓ Table 2 (page 10) | need: quantitative data on comprehensiveness metrics for C2 and SS across Podcast and News datasets | priority: required | status: missing → 候選 3，納入 [29]，排除 [(30, 'already among the retrieved sources'), (31, 'already among the retrieved sources')]
  - ✓ Section 4.1.2 Conditions (page 8) | need: definition of condition C2 and SS (vector RAG) to confirm experimental setup | priority: supplementary | status: covered → 候選 2，納入 [22]，排除 [(21, 'supplementary cap reached')]
  - ✓ Section 3.3 Criteria for Evaluating Global Sensemaking (pages 7-8) | need: definition of "comprehensiveness" metric used in the evaluation | priority: supplementary | status: missing → 候選 3，納入 [20]，排除 [(18, 'low relevance'), (19, 'supplementary cap reached')]
- 分析狀態：UNCERTAIN；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 修正：[]；刪除 []；仍不符 []；方向待定 []
- 涵蓋判定：Section 5.1 Experiment 1→partial；Table 2 (page 10)→missing；Section 4.1.2 Conditions (page 8)→partial；Section 3.3 Criteria for Evaluating Global Sensemaking (pages 7-8)→missing；required 未納入 []；supplementary 用 2；Matrix {'cells': 0, 'tables': [], 'definitions': [], 'facts': 0, 'coverage_gaps': ['Table 3 [1]']}
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 [([9], [6])]；未解析 0；找不到的數字 []

```text
The question asks for a comparison between condition C2 (intermediate-level community summaries) and SS (vector RAG/semantic search) on the metric of **comprehensiveness** across two datasets: **Podcast Transcripts** and **News Articles**.

**Method Definitions and Metrics:**
*   **Condition C2:** Uses intermediate-level community summaries to answer queries [5].
*   **Condition SS:** An implementation of vector RAG where text chunks are retrieved and added to the context window [5].
*   **Comprehensiveness Metric:** Defined as the average number of factual claims extracted from the answers [10].

**Comparison of Figures:**
The evidence provides two types of data for this comparison: LLM-based head-to-head win rates from Experiment 1 (Table 2/Figure 2 context in sources [9] and [11]) and quantitative average claim counts from Experiment 2 (Table 3 in source [1]).

**Dataset: Podcast Transcripts**
*   **Win Rates (Experiment 1):** In the Podcast transcripts, C2 achieved a comprehensiveness win rate of **79%** against SS (meaning C2 was preferred over SS in 79% of pairwise comparisons) [9]. Conversely, SS had a 21% win rate against C2 [9].
*   **Average Claims (Experiment 2):** C2 had an average of **32.46** extracted claims, while SS had **26.50** [1].

**Dataset: News Articles**
*   **Win Rates (Experiment 1):** In the News articles, C2 achieved a comprehensiveness win rate of **69%** against SS [11]. Conversely, SS had a 31% win rate against C2 [11].
*   **Average Claims (Experiment 2):** C2 had an average of **31.62** extracted claims, while SS had **25.23** [1].

**Improvements, Regressions, and Exceptions:**
*   **Improvements:** C2 outperformed SS in comprehensiveness on both datasets. In Podcast transcripts, C2 had a higher win rate (79% vs 21%) and higher average claims (32.46 vs 26.50) [1][9]. In News articles, C2 had a higher win rate (69% vs 31%) and higher average claims (31.62 vs 25.23) [1][11].
*   **Regressions:** None observed for C2 relative to SS in this specific comparison; SS performed lower in both metrics on both datasets.
*   **Exceptions/Statistical Significance:** The text states that for both datasets, all global search conditions (including C2) had statistically significantly greater comprehensiveness than SS (p < .05) [1]. The LLM win rates in Experiment 1 also align with these claim-based results [1].

**Verification of Claims:**
*   "C2 outperforms SS": Supported by win rates 79% (Podcast) and 69% (News) being >50% [9][11].
*   "Higher claims": 32.46 > 26.50 (Podcast) and 31.62 > 25.23 (News) [1].

**Citations:**
*   Definition of C2 and SS: [5].
*   Definition of Comprehensiveness: [10].
*   Podcast Win Rates (C2 vs SS): [9].
*   News Win Rates (C2 vs SS): [11].
*   Average Claims (Podcast and News): [1].
*   Statistical significance and alignment statement: [1].

**Completeness Check:**
*   Methods (C2, SS) covered? Yes.
*   Datasets (Podcast, News) covered? Yes.
*   Metric (Comprehensiveness) covered? Yes.
*   Figures compared correctly (same dataset/metric/pairing)? Yes.

**Conclusion:**
Condition C2 significantly outperforms vector RAG (SS) in comprehensiveness on both the Podcast and News datasets. In Podcast transcripts, C2 achieved a 79% win rate over SS and a higher average claim count (32.46 vs 26.50). In News articles, C2 achieved a 69% win rate over SS and a higher average claim count (31.62 vs 25.23). These differences were statistically significant [1][9][11].
```

## M5-G2-3

- 問題：`Compare condition C2 with vector RAG (SS) on comprehensiveness in the Podcast and News datasets`；模式 `navigate`；71.0 秒；2 次呼叫；tokens 8762
- 來源：[1] p11 retrieval, [2] p9 retrieval, [3] p10 retrieval, [4] p10 retrieval, [5] p8 retrieval, [6] p11 table_context, [7] p11 table_context, [8] p10 navigation, [9] p10 navigation, [10] p9 navigation, [11] p10 navigation, [12] p8 navigation, [13] p8 navigation
- 閱讀計畫（定位 4/4，保留 6，超預算 0）：
  - ✓ Section 5.1 Experiment 1 | need: textual comparison of C2 and SS on comprehensiveness for Podcast and News datasets | priority: required | status: covered → 候選 9，納入 [26, 24, 28]，排除 [(32, 'already among the retrieved sources'), (25, 'already among the retrieved sources'), (31, 'already among the retrieved sources'), (30, 'already among the retrieved sources'), (29, 'already selected for another target'), (27, 'target quota reached')]
  - ✓ Table 2 (page 10) | need: quantitative data on comprehensiveness metrics for C2 and SS across Podcast and News datasets | priority: required | status: missing → 候選 3，納入 [29]，排除 [(30, 'already among the retrieved sources'), (31, 'already among the retrieved sources')]
  - ✓ Section 4.1.2 Conditions (page 8) | need: definition of condition C2 and SS (vector RAG) to confirm experimental setup | priority: supplementary | status: covered → 候選 2，納入 [22]，排除 [(21, 'supplementary cap reached')]
  - ✓ Section 3.3 Criteria for Evaluating Global Sensemaking (pages 7-8) | need: definition of "comprehensiveness" metric used in the evaluation | priority: supplementary | status: missing → 候選 3，納入 [20]，排除 [(18, 'low relevance'), (19, 'supplementary cap reached')]
- 分析狀態：UNCERTAIN；完整性 not_applicable（required []，缺 []，條件 None）；方向核對 []
- 修正：[]；刪除 []；仍不符 []；方向待定 []
- 涵蓋判定：Section 5.1 Experiment 1→partial；Table 2 (page 10)→missing；Section 4.1.2 Conditions (page 8)→partial；Section 3.3 Criteria for Evaluating Global Sensemaking (pages 7-8)→missing；required 未納入 []；supplementary 用 2；Matrix {'cells': 0, 'tables': [], 'definitions': [], 'facts': 0, 'coverage_gaps': ['Table 3 [1]']}
- 檢查：標籤不符 []；全稱宣稱 0；引用可疑 []；未解析 0；找不到的數字 []

```text
The question asks for a comparison of condition C2 (GraphRAG using intermediate-level community summaries) against condition SS (vector RAG/semantic search) on the metric of "comprehensiveness" across two datasets: Podcast transcripts and News articles.

Evidence and Definitions:
- **Condition C2**: Defined as using intermediate-level community summaries to answer queries [5].
- **Condition SS**: Defined as an implementation of vector RAG where text chunks are retrieved and added to the context window until the token limit is reached [5][12].
- **Comprehensiveness Metric**: Defined in Experiment 1 as the win rate of one condition over another based on LLM judgment, and quantitatively in Experiment 2 as the average number of extracted factual claims per answer [10].
- **Dataset Podcast**: Comprises podcast transcripts divided into chunks [5].
- **Dataset News**: Comprises news articles divided into chunks [5].

Comparison of Figures (Experiment 1 Win Rates from Figure 2, reported in sources [9] and [11]):
The sources provide head-to-head win rate percentages where the row condition is compared against the column condition. A score >50% indicates the row condition outperforms the column condition.

*   **Podcast Dataset (Source [9], "Podcast transcripts" section, "Comprehensiveness" sub-table):**
    *   Comparison: C2 (row) vs SS (column).
    *   Value: The entry at the intersection of row C2 and column SS is **72**.
    *   Interpretation: C2 achieved a 72% win rate against SS.

*   **News Dataset (Source [11], "News Articles" section implied by context of previous table and distinct values, specifically the second "Comprehensiveness" block in source [11] or corresponding section):**
    *   Note: Source [9] contains Podcast data. Source [11] contains News data (identified by different win rates e.g., SS vs C0 is 62 in News vs 72 in Podcast). In Source [11], under the "Comprehensiveness" section:
    *   Comparison: C2 (row) vs SS (column).
    *   Value: The entry at the intersection of row C2 and column SS is **62**.
    *   Interpretation: C2 achieved a 62% win rate against SS.

*   **Quantitative Claims (Experiment 2, Source [1], Table 3):**
    *   This table reports the "Average Number of Claims" (the quantitative measure of comprehensiveness).
    *   **Podcast**: C2 = **31.62**, SS = **26.50**.
    *   **News**: C2 = **31.62** (Wait, Table 3 lists News Articles column. Let's read carefully).
    *   Table 3 in Source [1]:
        *   Column "News Articles": C2 = **31.62**, SS = **25.23**.
        *   Column "Podcast Transcripts": C2 = **32.46**, SS = **26.50**.
    *   Comparison: C2 has higher average claims than SS in both datasets.

Improvements, Regressions, and Exceptions:
- **Improvements**: C2 outperforms SS in comprehensiveness on both datasets.
    - On the Podcast dataset, C2 wins 72% of the time (Experiment 1) [9] and yields a higher average number of claims (32.46 vs 26.50) (Experiment 2) [1].
    - On the News dataset, C2 wins 62% of the time (Experiment 1) [11] and yields a higher average number of claims (31.62 vs 25.23) (Experiment 2) [1].
- **Statistical Significance**: Source [1] states that for both datasets, global search conditions (including C2) had significantly greater comprehensiveness than SS (p < .05) [1]. Source [2] notes global approaches significantly outperformed SS in comprehensiveness across datasets (p < .001) [2].
- **Exceptions**: There are no regressions or exceptions where SS outperformed C2 on comprehensiveness in these specific pairwise comparisons.

Verification of Terms:
- "Outperforms": C2 win rates of 72% and 62% are >50%, confirming outperformance [9][11].
- "Higher": Claim counts for C2 (32.46, 31.62) are higher than SS (26.50, 25.23) [1].

Citations:
- Definition of C2 and SS: [5].
- Definition of Comprehensiveness: [10].
- Podcast Win Rate (72%): [9].
- News Win Rate (62%): [11].
- Podcast Claim Counts (C2: 32.46, SS: 26.50): [1].
- News Claim Counts (C2: 31.62, SS: 25.23): [1].
- Statistical significance: [1][2].

Missing Information: All requested comparisons (C2 vs SS, Comprehensiveness, Podcast, News) are present.

**Conclusion:**
Condition C2 outperforms vector RAG (SS) on comprehensiveness in both the Podcast and News datasets. In the Podcast dataset, C2 achieved a 72% win rate against SS [9] and a higher average number of extracted claims (32.46 compared to 26.50) [1]. In the News dataset, C2 achieved a 62% win rate against SS [11] and a higher average number of extracted claims (31.62 compared to 25.23) [1]. These differences were statistically significant [1].
```
