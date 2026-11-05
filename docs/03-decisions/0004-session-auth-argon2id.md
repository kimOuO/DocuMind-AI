# ADR 0004：登入採用伺服器端 Session，密碼以 Argon2id 雜湊

- 狀態：已採用
- 日期：2026-11-05
- 對應決策日誌：D44、D45、D47

## 背景

平台需要註冊、登入、登出，並以登入的使用者作為每個操作的操作者。密碼不得明文儲存，不自行設計雜湊或加密。會改變資料的請求要能抵擋跨站請求偽造，並避免 Session Fixation。

## 考慮過的選項

**登入狀態**

| 選項 | 優點 | 缺點 |
|---|---|---|
| 伺服器端 Session＋HttpOnly Cookie | 登出立即失效；JavaScript 讀不到；`EventSource` 自動帶上；測試容易 | 多一張 `sessions` 表 |
| JWT 放在 Authorization 標頭 | 不需要資料表 | 登出無法真正失效；要存在 localStorage；`EventSource` 不能設定標頭 |

**密碼雜湊的套件**

| 選項 | 說明 |
|---|---|
| `argon2-cffi` | Argon2 參考實作的 Python 綁定，維護活躍，MIT 授權，直接提供 Argon2id |
| `pwdlib[argon2]` | 包了一層的工具，底層同樣是 `argon2-cffi` |
| `passlib` | 多年未更新 |

## 決定

- 伺服器端 Session＋HttpOnly Cookie（使用者決定，D44）。
- Argon2id，使用 `argon2-cffi==25.1.0`（使用者指定優先評估，D47）。
  - 2026-11-05 查得的最新穩定版為 25.1.0；在專案的 Python 3.12.3 上安裝與執行正常。
  - 採用函式庫的預設參數（Argon2id、記憶體 64 MiB、3 次迭代、4 個執行緒），在開發機上雜湊一次約 59 ms。
  - 直接使用它，不再包一層，少一個相依。
- Session token 以 `secrets.token_urlsafe(32)` 產生；資料庫只存 SHA-256。
- 每次登入都發新的 token，請求帶來的舊 Session 先刪除（避免 Session Fixation）。
- 會改變資料的請求檢查來源：有 `Origin` 看 `Origin`，沒有則看 `Referer`，兩者皆無或不在允許清單內回 `403`。在驗證登入之前執行。

## 驗證（2026-11-05）

- AC-28、AC-29、AC-31、AC-44、AC-45 的整合測試通過（對真實的 PostgreSQL）。
- 對 Docker 部署版以 curl 實測：缺來源與外部來源回 `403`；只帶合法 `Referer` 可登入；登出後舊 Cookie 回 `401`；資料庫中為 `$argon2id$` 開頭的雜湊。

## 後果

- 非瀏覽器的用戶端（測試、curl）必須自行帶上允許的 `Origin` 或 `Referer`。
- 用不在清單內的位址開啟網站（例如區網 IP）時，寫入請求會被擋下；需把該位址加入 `ALLOWED_ORIGINS`。前端對這個錯誤有專門的提示。
- 沒有登入次數限制；本地以 HTTP 執行時 `Secure` Cookie 關閉。兩者列為已知限制。
- 帳號不存在與密碼錯誤回傳相同的錯誤；帳號不存在時仍對一組假的雜湊做驗證，讓兩種情況花費的時間相近。
