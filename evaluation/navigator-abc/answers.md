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
