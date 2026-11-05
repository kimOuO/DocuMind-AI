import { useState, type FormEvent } from 'react'
import { ApiError, login, register, type User } from '../../lib/api'

type Mode = 'login' | 'register'

const MESSAGES: Record<string, string> = {
  INVALID_CREDENTIALS: '帳號或密碼不正確。',
  USERNAME_TAKEN: '這個使用者名稱已經有人使用。',
  VALIDATION_ERROR: '使用者名稱需 3–32 個英數字元，密碼至少 8 個字元。',
  ORIGIN_NOT_ALLOWED: '這個網址不在允許的來源清單內，請從設定的網址開啟。',
}

function describe(error: unknown): string {
  if (error instanceof ApiError) return MESSAGES[error.code] ?? error.message
  return '無法連線到伺服器，請稍後再試。'
}

export function AuthForm({ onLoggedIn }: { onLoggedIn: (user: User) => void }) {
  const [mode, setMode] = useState<Mode>('login')
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [notice, setNotice] = useState<string | null>(null)

  function switchTo(next: Mode) {
    setMode(next)
    setError(null)
  }

  async function submit(event: FormEvent) {
    event.preventDefault()
    setBusy(true)
    setError(null)
    setNotice(null)
    try {
      if (mode === 'register') {
        await register(username, password)
        setPassword('')
        setMode('login')
        setNotice('註冊成功，請登入。')
      } else {
        onLoggedIn(await login(username, password))
      }
    } catch (caught) {
      setError(describe(caught))
    } finally {
      setBusy(false)
    }
  }

  const isLogin = mode === 'login'
  return (
    <section className="mx-auto mt-10 max-w-sm rounded-lg border border-border bg-surface p-6">
      <h2 className="text-lg font-semibold">{isLogin ? '登入' : '註冊'}</h2>
      {notice && (
        <p role="status" className="mt-2 text-sm text-success">
          {notice}
        </p>
      )}
      <form onSubmit={submit} className="mt-4 flex flex-col gap-3">
        <label className="flex flex-col gap-1 text-sm">
          使用者名稱
          <input
            className="rounded-md border border-border bg-bg px-3 py-2 text-base"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            autoComplete="username"
            required
          />
        </label>
        <label className="flex flex-col gap-1 text-sm">
          密碼
          <input
            className="rounded-md border border-border bg-bg px-3 py-2 text-base"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            autoComplete={isLogin ? 'current-password' : 'new-password'}
            required
          />
        </label>
        {error && (
          <p role="alert" className="text-sm text-danger">
            {error}
          </p>
        )}
        <button
          type="submit"
          disabled={busy}
          className="rounded-md bg-accent px-3 py-2 font-medium text-surface disabled:opacity-60"
        >
          {busy ? '處理中…' : isLogin ? '登入' : '建立帳號'}
        </button>
      </form>
      <button
        type="button"
        className="mt-4 text-sm text-accent underline"
        onClick={() => switchTo(isLogin ? 'register' : 'login')}
      >
        {isLogin ? '還沒有帳號？註冊' : '已經有帳號？登入'}
      </button>
    </section>
  )
}
