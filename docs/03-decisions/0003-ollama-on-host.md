# ADR 0003：容器連主機上的 Ollama

- 狀態：已採用
- 日期：2026-11-05
- 對應決策日誌：D12

## 背景

部署用 Docker Compose，但 LLM（`qwen3:32b`，約 20GB）與 embedding 模型（`bge-m3`）已下載在主機的 Ollama 裡，由主機的 GPU 提供服務。

## 考慮過的選項

| 選項 | 優點 | 缺點 |
|---|---|---|
| 後端容器連主機 Ollama | 不必重新下載模型；啟動快 | 依賴主機已安裝 Ollama，且要監聽容器連得到的位址 |
| Ollama 也放進 compose | 一個指令全部起來，完全自包含 | 首次啟動要下載約 21GB；需要 NVIDIA container runtime |

## 決定

預設連主機 Ollama：後端容器設定 `extra_hosts: host.docker.internal:host-gateway`，`OLLAMA_BASE_URL=http://host.docker.internal:11434`。
另外提供 compose profile `ollama`，給沒有預裝 Ollama 的機器使用。

## 驗證（2026-11-05）

- 主機 Ollama 的 systemd 設定為 `OLLAMA_HOST=0.0.0.0:11434`，容器可連線。
- `make up` 後，經前端 Nginx 呼叫 `/api/health` 回傳 `ollama.ok = true`、`models available`。

## 後果

- 若主機 Ollama 只監聽 `127.0.0.1`，容器會連不到；`/api/health` 會顯示 `ollama.ok = false`。解法是把 `OLLAMA_HOST` 設為 `0.0.0.0`，或改用 `ollama` profile。README 需寫明。
- `ollama` profile 尚未在這台機器上實測。
