# 提交、標記、推送的規則

## 提交前

1. `git status` 與 `git diff --stat`：確認只包含這次該提交的檔案。
2. `make check` 通過。
3. 跑檢查腳本，確認沒有敏感資訊（金鑰、密碼、電子郵件、電話）。
4. 不提交：`.env`、`.venv/`、`node_modules/`、`.data/`、打包產生的 zip。

## Git 命名規範（2026-11-05 定案，已凍結）

不再為了格式重寫歷史。已推送的提交與標記不修改，不使用 force push。

### Commit 訊息

採用 Conventional Commits：

```
<type>(<scope>): <description>

階段：這次工作屬於哪個階段與工作項目
完成：
- 這個提交交付的東西
驗證：
- 實際執行過且通過的驗收條件與檢查
- 未驗證：還沒驗證的項目（沒有就省略這一行）

Co-Authored-By: …
```

- **標題用英文**，簡短描述實際的變更，72 個字元以內。
- `type`：`feat` 新功能、`fix` 修正、`refactor` 重整、`test` 測試、`docs` 文件、`chore` 工具與設定。
- `scope` 是**功能模組**，不放 P0、P1、P2 等階段編號。目前使用的 scope：
  `auth`、`documents`、`ingestion`、`retrieval`、`conversations`、`chat`、`summarization`、`llm`、`core`、`frontend`、`evaluation`、`specs`、`decisions`、`readme`、`config`、`deploy`、`package`、`agent-rules`、`tests`、`project`。
- **內文用繁體中文**，固定三段：階段、完成、驗證。「驗證」只寫實際執行過的結果。
- 一個工作項目拆成數個範圍清楚的提交（例如後端、前端、文件各一個）。每個提交都要能通過測試。

範例：

```
feat(documents): add upload, listing and deletion

階段：P2-B 文件管理
完成：
- 上傳後存檔並建立文件與排隊中的處理工作
- 依擁有者列出、讀取、刪除文件；相同內容不重複建立
驗證：
- AC-02、AC-35 通過；make check 通過
```

### Checkpoint Tag

- 格式：`cp-{number}-{outcome}`。`number` 對應規格的工作編號，`outcome` 用英文說明這個階段的成果。
- 只在整個階段驗收通過時建立；階段內的工作項目不打 Tag。
- 一律用 annotated tag，說明文字用英文，寫明這個階段交付了什麼。

| Tag | 階段成果 |
|---|---|
| `cp-0-foundation` | 專案骨架、隔離的開發環境、容器部署（已推送，不修改） |
| `cp-1-architecture-specs` | 平台規格與架構設計確認，主要架構凍結 |
| `cp-2-platform-rag-mvp` | 帳號、文件管理、入庫、附來源的問答 |
| `cp-3-document-qa` | 摘要、對話記憶、拒答；三個指定問題通過 |
| `cp-4-rag-evaluation` | 檢索評測與參數決策 |
| `cp-5-platform-ui` | 完整介面與個人偏好 |
| `cp-6-stabilization` | 整合、權限與一致性檢查 |
| `cp-7-final-delivery` | 說明文件、Demo、簡報、打包 |

名稱以此表為準；實際成果與預期不同時，先向使用者確認再調整尚未建立的名稱。

### Release Tag

- 與 Checkpoint Tag 分開管理，採用 Semantic Versioning：`v{major}.{minor}.{patch}`。
- 首次可交付的版本先考慮 `v0.1.0`，是否使用 `v1.0.0` 依最終版本的成熟度由使用者決定。
- 建立 Release Tag 時附上 Release Notes，說明這個版本包含的功能與已知限制。

### Tag 的共通規則

- Tag 已存在就停下來問使用者，不覆蓋。
- 尚未推送的 Tag 只有在使用者明確同意時才能重建；已推送的 Tag 不移動、不刪除。

## 決策日誌的 commit 欄位

提交之前無法知道自己的 hash。做法：

- 預設填 **Tag 名稱**（例如 `cp-2-platform-rag-mvp`），不需要回填。
- 真的需要 hash 時，在正式 commit 之後另建一個只改日誌的 metadata commit。
- 不使用「提交 → 回填 → amend → hash 又變了」的循環。

## 推送

- 使用者明確授權才推送。沒有授權就只做本地 commit 與 tag，並在回報中寫 Local Only。
- 指令：`git push` 與 `git push origin <tag>`（或 `git push --follow-tags`）。
- 在這個環境，Claude 的 `git push` 可能被權限機制擋下。被擋下時不要繞過，請使用者自己執行：
  `! git push --follow-tags`
- 推送失敗或沒有執行，回報中不可寫成已同步。

## 禁止

- `git reset --hard`、`git push --force`、`git clean -fd`、刪除或移動既有 Tag。
- 丟棄工作區中不是自己這次產生的修改。
- 推送到非 `origin` 的遠端，或把 repo 改成公開。
