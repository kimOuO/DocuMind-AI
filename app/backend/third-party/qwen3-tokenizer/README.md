# Qwen3 tokenizer（第三方資產）

後端用這份檔案在本地計算 token 數，讓每次 LLM 呼叫在送出前就能確認不超過 10,000 tokens。
檔案直接放在專案內：建置與執行時不需要連到 Hugging Face。

> 內附的只有 tokenizer。模型本身（`qwen3:32b`、`bge-m3`）仍須事先用 Ollama 安裝。

## 來源

| 項目 | 內容 |
|---|---|
| 檔案 | `tokenizer.json` |
| 來源模型 | [`Qwen/Qwen3-32B`](https://huggingface.co/Qwen/Qwen3-32B)（Hugging Face） |
| Revision | `9216db5781bf21249d130ec9da846c4624c16137` |
| 下載網址 | `https://huggingface.co/Qwen/Qwen3-32B/resolve/9216db5781bf21249d130ec9da846c4624c16137/tokenizer.json` |
| 取得日期 | 2026-11-05 |
| 大小 | 11,422,654 bytes |
| SHA-256 | `aeb13307a71acd8fe81861d94ad54ab689df773318809eed3cbe794b4492dae4` |
| 授權 | Apache License 2.0，全文見同目錄的 `LICENSE`（取自同一個 revision，Copyright 2024 Alibaba Cloud） |
| 修改 | 無。檔案內容與來源逐位元組相同 |

檔案不可被格式化工具改動（例如補上結尾換行），否則 SHA-256 會不符。`.pre-commit-config.yaml` 已將本目錄排除在會修改檔案的檢查之外；單元測試會核對 SHA-256。

## 與 Ollama 模型的對應

對應的 Ollama 模型：`qwen3:32b`（digest `030ee887880f…`，Q4_K_M，Ollama 0.24.0）。

2026-11-05 以 Ollama 的 `/api/show`（`verbose: true`）取出模型檔內嵌的 tokenizer，逐筆比對：

| 比對項目 | 結果 |
|---|---|
| 詞表 | 本檔的 151,669 筆（含 26 個特殊 token），在 Ollama 模型內的 id 與內容逐筆相同 |
| Ollama 多出的項目 | 267 筆，全部是 `[PAD151669]`–`[PAD151935]` 的填充佔位 |
| BPE 合併規則 | 兩邊各 151,387 條，內容與順序完全相同 |
| 起始 token | Ollama 模型的 `add_bos_token` 為 `false`，本地計數也不加 |

詞表與規則相同不代表計數必然相同：實際送出的 prompt 還會套用 chat template。計數的一致性由標記為 `llm` 的測試以 Ollama 回報的 `prompt_eval_count` 驗證（驗收條件 AC-25）。

## 更換模型或更新檔案時

1. 從對應模型的 Hugging Face repo 下載 `tokenizer.json` 與 `LICENSE`，記下 revision。
2. 更新本檔的來源表與程式中記錄的 SHA-256。
3. 重新比對詞表，並重跑 AC-25 的測試。
