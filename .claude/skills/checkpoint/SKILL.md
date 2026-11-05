---
name: checkpoint
description: 在一個開發階段（P0–P7）或一次 session 結束時執行：跑檢查、更新決策日誌、寫 session 摘要與階段回顧、匯出逐字稿、提交並打 tag。使用者說「checkpoint」「收尾」「打 cp」或某階段完成時使用。
---

# Checkpoint

把一個階段收乾淨，並自動留下互動紀錄。依序執行，任何一步失敗就停下來回報，不要跳過。

輸入：階段代號（例如 `P2`）與 checkpoint 名稱（例如 `cp-2-mvp`）。沒給就從 `docs/devlog/` 推斷下一個，並向使用者確認。

## 1. 驗證

- 執行 `make check`。失敗就修到綠燈，或停下來回報。
- 這個階段有對應驗收條件（見 `docs/specs/`）就逐條實測，記下證據（指令與輸出、數字）。
- P4 之後另跑 `make eval`，把報告路徑記下來。

## 2. 決策日誌 `docs/ai-collab/decision-log.md`

- 檢查這個階段做過的每個技術決策是否都有一筆。缺的補上。
- 每筆的「我的原始回覆」只能貼使用者實際說過的話。沒說理由就寫「未說明」，不可代寫。
- 補上「驗證結果」與「對應 commit」（commit 之後回填 hash）。
- AI 建議被否決或修改的，在「案例候選」標 ✓。

## 3. Session 摘要 `docs/ai-collab/sessions/YYYY-MM-DD-NN.md`

精簡，五個小節，不逐輪整理：本次目標｜AI 完成的工作｜使用者介入修改的部分｜遇到的問題｜下一步。

## 4. 階段回顧 `docs/devlog/P{n}.md`

依 `docs/devlog/TEMPLATE.md`。事實部分由你寫；「我的想法」一節向使用者問 2–3 個具體問題（用開放題），把回答原文貼入。使用者沒回答就留「待補」，不可代寫。

## 5. 心得 `docs/ai-collab/insights.md`

這個階段有值得放進 PPT 的協作心得就加一行（AI 做對什麼、做錯什麼、人怎麼介入）。沒有就不加。

## 6. 逐字稿

執行 `make transcript`。

## 7. 提交與標記

- `git add` 相關檔案，Conventional Commit 訊息，英文。
- 回填決策日誌的 commit hash 後再提交一次（或 amend 尚未推送的那個 commit）。
- `git tag cp-N-名稱`。
- 有設定遠端就 `git push --follow-tags`；沒有就告訴使用者。

## 8. 回報

用繁體中文簡短回報：通過的檢查、驗收證據、tag 名稱、未完成事項。
若這個階段出現了五種截圖時刻之一（重要決策、AI 出錯、人工介入修正、測試前後比較、最終 Demo），提醒使用者補截圖並存到 `docs/ai-collab/screenshots/`，檔名 `YYYYMMDD-NN-說明.png`。
