# ADR 0001：Python 環境用標準 venv + pip

- 狀態：已採用
- 日期：2026-11-05
- 對應決策日誌：D08

## 背景

專案需要隔離的 Python 環境。最終要把程式碼交給面試官在本地執行，開發時間只有一週。

## 考慮過的選項

| 選項 | 優點 | 缺點 |
|---|---|---|
| uv + `.venv`（AI 建議） | 快、有 lock 檔、免 sudo | 多一個要安裝與解釋的工具 |
| conda | 可管理非 Python 相依 | 要另裝 miniconda；與 Dockerfile 的安裝方式不一致 |
| 標準 venv + pip | Python 內建、人人會用、重現流程直觀 | 沒有完整 lock 檔；速度較慢 |

## 決定

採用標準 venv + pip，環境在 `.venv`，相依寫在 `requirements.txt` 與 `requirements-dev.txt` 並釘死版本。
理由（使用者）：降低額外的工具依賴，讓環境建立與專案重現流程更直觀。

Dockerfile 也在映像內建立 venv 並用同一份 `requirements.txt` 安裝，開發與部署的安裝方式一致。

## 補充（2026-11-05）：Node 也放進 venv

使用者要求「使用 venv 內開發，不再本機開發」。P0 一開始用 nvm 把 Node 裝在使用者家目錄，已改用 nodeenv 把 Node 裝進同一個 venv（`.venv/bin/node`），`nodeenv` 釘在 `requirements-dev.txt`，Node 版本記在 `app/frontend/.node-version`。對應決策日誌 D20。

## 後果

- 面試官只需要 `python3 -m venv` 與 `pip install -r`，或直接用 Docker。
- `requirements.txt` 只釘直接相依，間接相依的版本可能隨時間漂移。若出現重現問題，再改用 pip-tools 產生完整鎖定檔。
- 部分 Debian/Ubuntu 預設沒裝 `python3-venv`（本開發機即是）。`make setup` 內建後備流程：`python3 -m venv --without-pip` 再用 `get-pip.py` 補 pip，不需 sudo。
