# 驗證與驗收的記錄方式

## 自動檢查

| 指令 | 內容 | 何時執行 |
|---|---|---|
| `make check` | 後端 ruff、ruff format、mypy、pytest；前端 eslint、tsc、vitest | 每次 checkpoint |
| `make test` | 含需要資料庫的測試（需先 `make db`） | 有資料庫相關變更時 |
| `make eval` | 檢索與回答品質評測，產出 `evaluation/` 下的報告 | P4 及之後 |
| `make up` | Docker 部署版；再呼叫 `/api/health` | Phase checkpoint |

每個指令記錄四項：執行的指令、exit code、通過與失敗的數量、日誌或報告的路徑。
只寫實際看到的輸出。沒有執行的指令不要列出數字。

## 驗收條件

驗收條件在 `docs/02-specs/01-requirements.md`，每條有編號（AC-01…）。
Phase checkpoint 時在階段回顧中列一張表：

| 編號 | 驗收條件 | 狀態 | 證據 |
|---|---|---|---|
| AC-01 | … | PASS／FAIL／NOT TESTED | 指令與輸出摘要、測試名稱、或截圖檔名 |

狀態的定義：

- **PASS**：這次 checkpoint 中實際執行過，結果符合。
- **FAIL**：實際執行過，結果不符合。寫出差異。
- **NOT TESTED**：沒有執行。寫出原因（尚未實作、缺環境、時間不足）。

沿用上一次 checkpoint 的結果不算 PASS，要重新執行。

## 題目的硬性限制

每個 Phase checkpoint（P2 之後）都要重新確認：

- 所有 LLM 呼叫的 prompt + completion ≤ 10,000 tokens：查 `GET /api/v1/llm-calls`。分開回報兩個數字：`measured.max_total_tokens`（實測合規的依據）與 `unmeasured` 的筆數及其預算上界（只代表送出前通過檢查，不可稱為實測合規）。
- 程式沒有呼叫任何雲端 LLM 或文件解析 API。
- 回答附來源；無答案的問題會拒答。

## 失敗時

- 與本階段直接相關的問題可以當場修正，修正後整套檢查重跑。
- 修不好：停止 Phase checkpoint，不打成功的 Tag，把目前結果與失敗原因回報使用者。
