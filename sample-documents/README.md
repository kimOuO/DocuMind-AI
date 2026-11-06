# sample-documents

Fixed documents used by the tests, the retrieval experiments and the demo, so
that results can be reproduced without network access.

| File | Source | License |
|---|---|---|
| `2404.16130v2.pdf` | Darren Edge, Ha Trinh, Newman Cheng, Joshua Bradley, Alex Chao, Apurva Mody, Steven Truitt, Dasha Metropolitansky, Robert Osazuwa Ness, Jonathan Larson. *From Local to Global: A Graph RAG Approach to Query-Focused Summarization.* arXiv:2404.16130, version 2. <https://arxiv.org/abs/2404.16130> | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |
| `2410.05779v3.pdf` | Zirui Guo, Lianghao Xia, Yanhua Yu, Tu Ao, Chao Huang. *LightRAG: Simple and Fast Retrieval-Augmented Generation.* arXiv:2410.05779, version 3 (28 Apr 2025). <https://arxiv.org/abs/2410.05779> | [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) |

Both PDFs are the unmodified files published on arXiv. The LightRAG paper is included under the
terms of its licence: attribution as given above, non-commercial use only, and
any adaptation must be shared under the same licence. It is not covered by this
project's own licence. If you intend to use this repository commercially, remove
the file and download the paper from the URL above instead.

The Graph RAG paper (CC BY 4.0, 6.9 MB) is **not committed**: it exceeds the repository's 4 MB file limit. The D69 revision experiment (evaluation/revision-ab) and its ground truth use it as a second document; download it first:

```bash
curl -sL -o sample-documents/2404.16130v2.pdf https://arxiv.org/pdf/2404.16130v2
``` Licences as shown on the arXiv abstract pages on 2026-11-05 and 2026-11-06.
