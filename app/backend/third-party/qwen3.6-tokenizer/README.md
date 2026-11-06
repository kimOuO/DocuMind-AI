# Qwen3.6 tokenizer（第三方資產）

後端以 `TOKENIZER_PATH`／`TOKENIZER_SHA256` 指到這份檔案時，預算守門會用它計算 token 數。它是 `qwen3.6:27b` 的 tokenizer，與 `qwen3-tokenizer/` 的 Qwen3 檔案**不同**（詞表 248,044 筆對 151,669 筆），兩者不可混用：以 Qwen3 的檔案計 qwen3.6 的 prompt，表格文字會少算最多約 3%（D77／M5 的第一次執行：估 6,501、實際 6,690）。

> 內附的只有 tokenizer。模型本身（`qwen3.6:27b-q4_K_M`）仍須事先用 Ollama 安裝。預設模型 `qwen3:32b` 仍用 `qwen3-tokenizer/`。

## 來源

| 項目 | 內容 |
|---|---|
| 檔案 | `tokenizer.json` |
| 來源模型 | [`Qwen/Qwen3.6-27B`](https://huggingface.co/Qwen/Qwen3.6-27B)（Hugging Face） |
| Revision | `6a9e13bd6fc8f0983b9b99948120bc37f49c13e9` |
| 下載網址 | `https://huggingface.co/Qwen/Qwen3.6-27B/resolve/main/tokenizer.json`（取得時 `main` 即上列 revision） |
| 取得日期 | 2026-11-07 |
| 大小 | 12,807,982 bytes |
| SHA-256 | `5f9e4d4901a92b997e463c1f46055088b6cca5ca61a6522d1b9f64c4bb81cb42` |
| 詞表 | 248,044 筆（含 26 個特殊 token）；BPE 合併規則 247,587 條 |
| 授權 | Apache License 2.0，全文見同目錄的 `LICENSE`（取自同一 repo） |
| 修改 | 無。檔案內容與來源逐位元組相同 |

檔案不可被格式化工具改動，否則 SHA-256 會不符。

## 與 Ollama 模型的對應

對應的 Ollama 模型：`qwen3.6:27b-q4_K_M`（architecture `qwen35`，27.8B，Q4_K_M，Ollama 0.24.0）。Ollama 對這個家族用內建的渲染器而非 Go 模板（`ollama show --template` 只回 `{{ .Prompt }}`），所以本專案的 `chat_template.py`（Qwen3 的模板）渲染後的計數與 Ollama 回報的 `prompt_eval_count` 不完全相等。2026-11-07 以四段文字實測（`think=false`、`num_predict=1`）：

| 文字 | Ollama 實際 | 本檔計數（含模板） | 差 |
|---|---|---|---|
| 一般句子 ×20 | 1,392 | 1,397 | +5 |
| Table 2 切塊（表格文字） | 1,513 | 1,517 | +4 |
| Table 6 切塊 | 413 | 417 | +4 |
| 地圖與計畫格式 | 1,221 | 1,226 | +5 |

本檔計數一律多 4–5 個 token（Qwen3 模板的包裝比 qwen3.6 的多幾個 token），守門偏保守，不會少算。同樣四段以 Qwen3 的檔案計數：+5、−12、+2、+15，表格文字會少算。

## 使用方式

在 `.env` 設：

```
LLM_MODEL=qwen3.6:27b-q4_K_M
TOKENIZER_PATH=third-party/qwen3.6-tokenizer/tokenizer.json
TOKENIZER_SHA256=5f9e4d4901a92b997e463c1f46055088b6cca5ca61a6522d1b9f64c4bb81cb42
```

更換模型時依 `qwen3-tokenizer/README.md` 的步驟：下載對應 repo 的 `tokenizer.json` 與 `LICENSE`、記 revision、更新 SHA-256，並重新比對計數。
