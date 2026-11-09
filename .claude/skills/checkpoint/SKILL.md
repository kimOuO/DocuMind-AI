---
name: checkpoint
description: >
  完成開發階段或 session 收尾時使用。
  當使用者說「checkpoint」「收尾」「打 cp」「階段完成」時，
  執行驗證、更新開發紀錄、保存 AI 協作證據，並建立 Git checkpoint。
---

# Checkpoint Skill

## 目標

為 DocuMind-AI 建立可追溯、可驗證、可恢復的開發階段紀錄。

優先順序：

1. 確保程式品質與驗收正確
2. 保存真實的人機協作過程
3. 記錄技術決策及其驗證證據
4. 建立可回溯的 Git 版本

禁止虛構使用者發言、測試結果、決策理由。

細節規則在 `references/`：

- `references/validation.md`：驗證與驗收怎麼記錄
- `references/decision-log.md`：決策日誌的欄位與寫法
- `references/git-workflow.md`：提交、標記、推送的規則

自動檢查腳本：`scripts/check_checkpoint.py`（第 2 步與第 8 步使用）。

## 1. 確認 Checkpoint 類型

### Session Checkpoint

適用於一般開發工作結束。執行：`make check`、Session 摘要、必要的決策日誌更新、Transcript 匯出。
預設不建立 Phase Tag。

### Phase Checkpoint

適用於 P0–P7 階段驗收完成。執行完整流程：驗證及階段驗收、決策日誌、Session 摘要、階段回顧、協作心得、Transcript、Git Commit／Tag、最終報告。

使用者未指定類型時依上下文判斷。無法判斷時採 Session 模式，避免意外建立正式階段標記。

## 2. 執行前檢查

執行：

    python3 .claude/skills/checkpoint/scripts/check_checkpoint.py --mode <session|phase> [--tag cp-{number}-{outcome}]

腳本只用標準庫，可用系統 `python3`。它會確認：位於 Git repository、目前 branch 與 HEAD、`git status`、`make` 目標存在、`docs/02-specs/` 與 `docs/04-dev-journal/` 存在、Tag 是否已存在、決策日誌是否有缺漏欄位。

- 不可覆蓋既有 Tag。
- 不可擅自丟棄工作區中的修改。
- 不可使用 `git reset --hard` 或強制推送。
- 名稱不明確的正式 Phase Tag，必須先取得使用者確認。

腳本回報 BLOCKING 時停止，回報使用者。

## 3. 執行測試與驗收

執行 `make check`，P4 及之後另執行 `make eval`；這個階段改過前端或後端模組的，`make up` 重建後再跑 `make smoke-api`（CLAUDE.md 互動規則第 2 條）。記錄方式見 `references/validation.md`。

- 對照 `docs/02-specs/` 的驗收條件，逐項記錄 PASS、FAIL 或 NOT TESTED。
- 不可將未執行的驗收標示為 PASS。
- 核心驗收失敗時：可修正與本階段直接相關的問題，修正後必須重新檢查；無法修復時停止正式 Phase Checkpoint，不建立成功的階段 Tag，保留目前結果並回報。

## 4. 更新 Decision Log

檔案：`docs/05-ai-collaboration/decision-log.md`。欄位與寫法見 `references/decision-log.md`。

- 只記錄具有影響力的決策：架構選擇、模型與工具選型、RAG 檢索策略、Token Budget、AI 建議被拒絕或修改、人工介入修正重大問題。
- 「使用者原始回覆」必須逐字保留。使用者沒有說明理由時填「未說明」。
- 禁止推測使用者的心理、動機或想法。
- 不可為了增加 AI 協作案例數量而虛構決策。

## 5. 建立 Session 摘要

位置：`docs/05-ai-collaboration/sessions/YYYY-MM-DD-NN.md`

固定五個小節：本次目標｜AI 完成的工作｜使用者介入修改的部分｜遇到的問題｜下一步。

- 以事實為主、精簡，不逐輪重述對話，只記錄可查證的操作與結果。
- 沒有人工介入時明確記錄「無」。
- 使用當地日期；同日已有紀錄則遞增 NN。
- 重新執行同一 Checkpoint 時更新原檔，不建立重複紀錄。

## 6. 更新 Phase Journal

僅 Phase Checkpoint 執行。位置：`docs/04-dev-journal/P{n}.md`，依 `TEMPLATE.md`。

AI 可以整理：階段目標、實作內容、架構變化、測試結果、遭遇問題、下一步規劃。

「我的想法」必須由使用者提供。詢問 2–3 個具體的開放式問題，例如：

- 這個階段你最不認同 AI 的哪個建議？
- 哪個問題是你介入後才解決的？
- 這次合作讓你改變了什麼做法？

使用者未回答時標示「待補」，不可自行生成心得；不影響已完成的技術紀錄，正式驗收可標示為「通過，心得待補」。

## 7. 更新協作心得

檔案：`docs/05-ai-collaboration/insights.md`。只有出現值得在簡報展示的案例才新增。

優先記錄：AI 有效加速工作、AI 提出錯誤方案、人工修正 AI 的問題、AI 與人工方案的實驗比較、使用者從協作中得到的方法改進。

每筆必須能連結到 Decision ID、Session 或測試證據。不得把 AI 的推測當成使用者心得。

## 8. 匯出 Transcript

執行 `make transcript`，然後再跑一次檢查腳本（會掃描逐字稿與已追蹤檔案中的敏感資訊）。

確認：指令實際成功、產生的檔案存在、內容對應本次 Session、沒有重複匯出。

Transcript 不得包含 API Keys、Access Tokens、Passwords、私有憑證、不應公開的個人資料。
匯出功能不可用時，記錄原因及待補事項，不得假裝已成功匯出。

## 9. Git Commit 與 Tag

僅正式 Phase Checkpoint 預設執行。規則見 `references/git-workflow.md`。

- 提交前：檢查 `git diff`、確認 staged files、避免包含無關檔案、確認測試與驗收通過、檢查敏感資訊。
- 提交採 Conventional Commits：標題 `type(scope): description` 用英文，scope 是功能模組、不放階段編號；內文用繁體中文三段：階段、完成、驗證。完整規範見 `references/git-workflow.md`。
- 決策日誌的 Commit 欄位可填 Tag 名稱，避免自我引用。需要填實際 Hash 時允許另建 metadata commit，不可使用無限 amend 流程。
- 建立 Annotated Tag，格式 `cp-{number}-{outcome}`，例如 `git tag -a cp-2-platform-rag-mvp -m "Checkpoint 2: accounts, document management, ingestion and question answering with citations"`。不可覆蓋既有名稱。Release Tag（`v0.1.0` 等）另依 `references/git-workflow.md`。
- 使用者已授權 Push 才推送；未授權則只建立本地 Commit 與 Tag。Push 失敗時不可宣稱遠端同步成功。

## 10. 錯誤處理與恢復

Checkpoint 必須可以重複執行。重新執行時檢查既有 Session、Decision ID、Transcript、Commit 與 Tag，避免重複寫入。

**BLOCKING**（停止正式完成流程）：`make check` 失敗、必要驗收失敗、Git repository 狀態異常、敏感資訊外洩風險、Tag 名稱衝突。

**NON-BLOCKING**（記為 Pending，不可宣稱全部完成）：使用者心得未補、截圖未提供、無可記錄的協作心得。

## 11. 截圖證據

遇到下列五種時刻時提醒使用者：重要技術決策、AI 提出錯誤方案、使用者介入修正、測試前後比較、最終 Demo。

儲存位置：`docs/05-ai-collaboration/screenshots/`，檔名 `YYYYMMDD-NN-description.png`。

截圖必須真實來自開發過程。不得生成虛假的開發截圖。

## 12. 最終回報格式

以繁體中文回報：

- Checkpoint：名稱與階段
- Validation：PASS／FAIL／PARTIAL
- Acceptance：通過數與未完成數
- Evidence：日誌與報告路徑
- Git：Commit Hash 與 Tag
- Remote：Pushed／Local Only／Failed
- Pending：未完成事項
- Screenshot：建議保存的畫面

不可宣稱沒有實際驗證過的項目成功。
