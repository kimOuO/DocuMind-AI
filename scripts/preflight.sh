#!/usr/bin/env bash
# 啟動前檢查：一次檢查完所有項目，最後一次列出要處理的事，不逐項停下。
# `make up`、`make deploy` 會先執行它；單獨執行：`make preflight`。
# 有「未通過」的項目時結束碼為 1；「提醒」不擋啟動。
set -uo pipefail
cd "$(dirname "$0")/.."

# 需要的版本（實測版本：Docker 29.5、Compose 5.1、Ollama 0.24.0）
MIN_DOCKER="20.10"      # host.docker.internal 需要 host-gateway
MIN_COMPOSE="2.2"       # `docker compose up --wait`
MIN_OLLAMA="0.24.0"     # 超量輸入的拒絕行為（truncate=false、shift=false）在這個版本實測
REQUIRED_MODELS=("qwen3:32b|生成模型，約 20 GB" "bge-m3|嵌入模型，約 1.2 GB")
OPTIONAL_MODELS=("qwen3.6:27b-q4_K_M|前端可切換的第二個生成模型，約 17 GB")
# 建議資源
MIN_VRAM_MIB=24000      # qwen3:32b（Q4_K_M）約需 20 GB 顯示記憶體
MIN_RAM_GB=16
MIN_DISK_GB=10          # 映像與資料；模型另需約 21 GB

setting() {  # 讀 .env（沒有就讀 .env.sample）的值，去掉行內註解
  local file=".env"; [[ -f "$file" ]] || file=".env.sample"
  local value; value="$(grep -E "^$1=" "$file" 2>/dev/null | tail -1 | cut -d= -f2- | sed 's/[[:space:]]*#.*$//' | xargs)"
  echo "${value:-$2}"
}
WEB_PORT="$(setting WEB_PORT 3000)"; DB_PORT="$(setting DB_PORT 5433)"
OLLAMA_PORT="$(setting HTTP_OLLAMA_PORT 11434)"
# Ollama 在另一台機器時（.env 的 COMPOSE_OLLAMA_HOST 填了 IP），直接檢查那一台。
OLLAMA_HOST_SETTING="$(setting COMPOSE_OLLAMA_HOST host.docker.internal)"
REMOTE_OLLAMA=""
if [[ "$OLLAMA_HOST_SETTING" != "host.docker.internal" && "$OLLAMA_HOST_SETTING" != "ollama" ]]; then REMOTE_OLLAMA="$OLLAMA_HOST_SETTING"; fi
OLLAMA_URL="${PREFLIGHT_OLLAMA_URL:-http://${REMOTE_OLLAMA:-127.0.0.1}:${OLLAMA_PORT}}"

failures=(); warnings=()
ok()   { printf '  [通過]   %s\n' "$1"; }
fail() { printf '  [未通過] %s\n' "$1"; failures+=("$1｜$2"); }
warn() { printf '  [提醒]   %s\n' "$1"; warnings+=("$1｜$2"); }
at_least() { [[ "$(printf '%s\n%s\n' "$2" "$1" | sort -V | head -1)" == "$2" ]]; }

echo "啟動前檢查"
echo "一、容器環境"
if command -v docker >/dev/null 2>&1; then
  docker_version="$(docker version --format '{{.Client.Version}}' 2>/dev/null || true)"
  if [[ -n "$docker_version" ]] && at_least "$docker_version" "$MIN_DOCKER"; then ok "Docker $docker_version（需要 ≥ $MIN_DOCKER）"
  else fail "Docker 版本 ${docker_version:-未知}，需要 ≥ $MIN_DOCKER" "升級 Docker：https://docs.docker.com/engine/install/"; fi
  if docker info >/dev/null 2>&1; then ok "Docker 服務執行中"
  else fail "Docker 服務沒有回應" "啟動 Docker（例如 sudo systemctl start docker），並確認目前的使用者可以執行 docker"; fi
  compose_version="$(docker compose version --short 2>/dev/null | sed 's/^v//' || true)"
  if [[ -n "$compose_version" ]] && at_least "$compose_version" "$MIN_COMPOSE"; then ok "Docker Compose $compose_version（需要 ≥ $MIN_COMPOSE）"
  else fail "找不到 Docker Compose v2，或版本低於 $MIN_COMPOSE" "安裝 Compose 外掛：https://docs.docker.com/compose/install/"; fi
else
  fail "沒有安裝 Docker" "安裝 Docker Engine ≥ $MIN_DOCKER 與 Compose 外掛 ≥ $MIN_COMPOSE：https://docs.docker.com/engine/install/"
fi

echo "二、模型服務（Ollama）"
if ! command -v curl >/dev/null 2>&1; then
  fail "沒有 curl，無法檢查 Ollama" "安裝 curl 後重跑"
else
  ollama_version="$(curl -s --max-time 5 "$OLLAMA_URL/api/version" 2>/dev/null | sed -n 's/.*"version":"\([^"]*\)".*/\1/p')"
  if [[ -z "$ollama_version" ]]; then
    fail "連不到 Ollama（$OLLAMA_URL）" "安裝並啟動 Ollama ≥ $MIN_OLLAMA：https://ollama.com/download"
    for item in "${REQUIRED_MODELS[@]}"; do fail "無法確認模型 ${item%%|*}（${item##*|}）" "Ollama 啟動後執行：ollama pull ${item%%|*}"; done
  else
    if at_least "$ollama_version" "$MIN_OLLAMA"; then ok "Ollama $ollama_version（需要 ≥ $MIN_OLLAMA）"
    else fail "Ollama 版本 $ollama_version，需要 ≥ $MIN_OLLAMA" "升級 Ollama：https://ollama.com/download（10K 上限的第二層保護在 $MIN_OLLAMA 實測）"; fi
    tags="$(curl -s --max-time 10 "$OLLAMA_URL/api/tags" 2>/dev/null)"
    has_model() { grep -q "\"name\":\"$1\"" <<<"$tags" || grep -q "\"name\":\"$1:latest\"" <<<"$tags"; }
    for item in "${REQUIRED_MODELS[@]}"; do
      name="${item%%|*}"; note="${item##*|}"
      if has_model "$name"; then ok "模型 $name（$note）"; else fail "缺少模型 $name（$note）" "執行：ollama pull $name"; fi
    done
    for item in "${OPTIONAL_MODELS[@]}"; do
      name="${item%%|*}"; note="${item##*|}"
      if has_model "$name"; then ok "選用模型 $name（$note）"
      else warn "沒有選用模型 $name（$note）" "要用前端的模型切換才需要：ollama pull $name；不用的話把 .env 的 ALT_LLM_MODEL 留空"; fi
    done
    # 後端在容器裡，經 Docker 橋接網路連主機的 Ollama：Ollama 只聽 127.0.0.1 時連不到。
    gateway="$(docker network inspect bridge -f '{{(index .IPAM.Config 0).Gateway}}' 2>/dev/null || true)"
    if [[ -n "$REMOTE_OLLAMA" ]]; then ok "Ollama 在另一台機器（$REMOTE_OLLAMA:$OLLAMA_PORT），已連線確認"
    elif [[ -n "$gateway" ]]; then
      if curl -s --max-time 5 "http://$gateway:$OLLAMA_PORT/api/version" >/dev/null 2>&1; then ok "容器連得到主機的 Ollama（$gateway:$OLLAMA_PORT）"
      else fail "Ollama 只接受本機連線，容器連不到" "讓 Ollama 監聽所有介面：設定環境變數 OLLAMA_HOST=0.0.0.0 後重啟 Ollama（systemd：sudo systemctl edit ollama 加 Environment=\"OLLAMA_HOST=0.0.0.0\"）"; fi
    fi
  fi
fi

echo "三、連接埠"
stack_running="$(docker compose ps -q 2>/dev/null | head -1 || true)"
port_busy() { (command -v ss >/dev/null 2>&1 && ss -ltn 2>/dev/null | grep -qE "[:.]$1\s") || (command -v lsof >/dev/null 2>&1 && lsof -iTCP:"$1" -sTCP:LISTEN >/dev/null 2>&1); }
for pair in "$WEB_PORT|網頁（WEB_PORT）" "$DB_PORT|資料庫（DB_PORT）"; do
  port="${pair%%|*}"; label="${pair##*|}"
  if [[ -n "$stack_running" ]]; then ok "連接埠 $port：$label，本專案的容器已在執行"
  elif port_busy "$port"; then fail "連接埠 $port 已被其他程式占用（$label）" "停掉占用的程式，或在 .env 改 ${label#*（} 的值"
  else ok "連接埠 $port 可用（$label）"; fi
done

echo "四、資源建議"
if command -v nvidia-smi >/dev/null 2>&1; then
  vram="$(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits 2>/dev/null | sort -nr | head -1 | tr -d ' ')"
  if [[ -n "$vram" && "$vram" -ge "$MIN_VRAM_MIB" ]]; then ok "顯示記憶體 $((vram / 1024)) GB（建議 ≥ $((MIN_VRAM_MIB / 1000)) GB）"
  else warn "顯示記憶體 ${vram:-未知} MiB，低於建議的 $((MIN_VRAM_MIB / 1000)) GB" "qwen3:32b 約需 20 GB 顯示記憶體；不足時會退回 CPU 或混合運算，回答會慢很多"; fi
else
  warn "找不到 NVIDIA 顯示卡（nvidia-smi）" "沒有 GPU 也能執行，但一題可能要數分鐘；建議 ≥ $((MIN_VRAM_MIB / 1000)) GB 顯示記憶體"
fi
if [[ -r /proc/meminfo ]]; then
  ram_gb="$(awk '/MemTotal/ {printf "%d", $2 / 1024 / 1024}' /proc/meminfo)"
  if [[ "$ram_gb" -ge "$MIN_RAM_GB" ]]; then ok "記憶體 ${ram_gb} GB（建議 ≥ $MIN_RAM_GB GB）"
  else warn "記憶體 ${ram_gb} GB，低於建議的 $MIN_RAM_GB GB" "容器與模型載入可能不足"; fi
fi
disk_gb="$(df -Pk . | awk 'NR==2 {printf "%d", $4 / 1024 / 1024}')"
if [[ "$disk_gb" -ge "$MIN_DISK_GB" ]]; then ok "可用磁碟 ${disk_gb} GB（映像與資料建議 ≥ $MIN_DISK_GB GB；模型另需約 21 GB）"
else warn "可用磁碟 ${disk_gb} GB，低於建議的 $MIN_DISK_GB GB" "清出空間；模型另需約 21 GB"; fi

echo
if (( ${#warnings[@]} )); then
  echo "提醒（不影響啟動）："
  for w in "${warnings[@]}"; do printf '  - %s\n      → %s\n' "${w%%｜*}" "${w#*｜}"; done
fi
if (( ${#failures[@]} )); then
  echo "未通過 ${#failures[@]} 項，請全部處理後再執行："
  i=1; for f in "${failures[@]}"; do printf '  %d. %s\n      → %s\n' "$i" "${f%%｜*}" "${f#*｜}"; i=$((i + 1)); done
  exit 1
fi
echo "全部通過，可以啟動。"
