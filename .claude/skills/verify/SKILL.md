---
name: verify
description: 改完程式後的驗證流程：秒級檢查 → 相關測試檔 → 找寫死的斷言 → 背景跑 make check 同時寫紀錄 → 直接印失敗名稱 → 綠了才提交部署。當使用者說「驗證」「跑測試」「檢查」或改完任何後端／前端程式時使用。
---

# verify — 改完程式的驗證流程

目標：一次 `make check` 就綠，不讓使用者等第二次。每一步都有固定指令，不自己發明。

## 0. 原則

- `make check` 要 2.5 分鐘，只在**提交前跑一次**當門；迭代階段只跑秒級檢查與相關檔案。
- 找失敗一律印出 `FAILED` 名稱與 `E   ` 行，不要只看「2 failed」那一行。
- 跑整套時丟背景，同時做規格、決策日誌、README；不乾等。
- 背景指令**不要接 `| grep | head`**，輸出會緩衝到結束；改成寫到檔案，用 `until grep -q ...; do sleep 3; done` 等。
- `tests/integration/*_real.py` 是標 `llm` 的真模型測試，**永遠帶 `-m "not llm"`**，否則單題就在等 Ollama、卡十幾分鐘。

## 1. 秒級檢查（每次改完都跑，約 15 秒）

後端：

    cd app/backend && ../../.venv/bin/ruff format app tests >/dev/null && ../../.venv/bin/ruff check app tests && ../../.venv/bin/mypy app | tail -1 && ../../.venv/bin/pytest -q -p no:cacheprovider -o addopts="" tests/unit | tail -1

前端（這就是 `make check-frontend`；`npx tsc --noEmit` 不等價，曾漏抓 TS2322）：

    source .venv/bin/activate && cd app/frontend && npm run check 2>&1 | grep -E "Tests |Test Files|error"

前端格式化只用專案風格：`npx prettier --single-quote --no-semi --print-width 110 --trailing-comma all --write <files>`。

## 2. 相關的整合測試檔（約 40 秒）

改到 chat／retrieval／summary 就跑對應檔：

    cd app/backend && ../../.venv/bin/pytest -q -m "not llm" tests/integration/test_chat.py tests/integration/test_chat_memory.py tests/integration/test_chat_summary.py 2>&1 | grep -E "^FAILED|^E   | passed| failed"

## 3. 改了共用的事件或物件欄位，先找寫死的斷言

`route`、`sources`、`done`、`start`、health、message 的欄位一變，別的測試檔會紅。先 grep 一起改，不要等整套才發現：

    grep -rn '"route"\] == {\|\["route"\] == {\|received\[1\]\[1\] == {' app/backend/tests/
    grep -rn 'set(answer) == {\|payload == {\|"sources"\]\[0\] == {' app/backend/tests/
    grep -rn 'answer_temperature\|check_notes' app/frontend/src/**/*.test.tsx

前端的 `mockApi` 會對未預期的請求丟錯：新增 `fetchHealth` 這類呼叫時，所有測試的路由表都要補。

## 4. 整套檢查（提交前一次，背景跑）

    cd /home/mitlab/DocuMind-AI && make check > /tmp/claude-1000/-home-mitlab-DocuMind-AI/<session>/scratchpad/check.log 2>&1 &

同時去寫規格與決策日誌。等待用：

    until grep -qE " passed| failed|error TS|Error" check.log; do sleep 3; done; grep -E "^FAILED|^E   | passed| failed|error TS|Tests |Test Files" check.log

紅了：只重跑那一檔（第 2 步的指令）修到綠，再跑一次整套。

## 5. 提交與部署（指令用 `&&` 串，失敗就停）

- commit 訊息寫到 scratchpad 的檔案再 `git commit -F`，**不要在 heredoc 裡再包 heredoc**（曾把 python 腳本當成 commit 訊息）。
- 提交後 `make up`，`sleep 20`，`curl -s http://127.0.0.1:3000/api/v1/health` 確認 `status: ok` 與設定值。
- 示範環境的 API 要帶 `Origin: http://127.0.0.1:3000`，否則 403。

## 6. 實測與紀錄

- 用 scratchpad 的重放腳本對示範部署跑使用者指定的情境（同一對話、temperature 0、建不建摘要），記錄存 `evaluation/stability/conversation-runs/`。
- 逐句對原文判定後，才寫「通過」；決策日誌的驗證結果與 commit hash 補上，再提交記錄。
