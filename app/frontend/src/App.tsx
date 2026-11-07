import { useEffect, useState } from 'react'
import { GraphBackdrop } from './components/GraphBackdrop'
import { AuthForm } from './features/auth/AuthForm'
import { Home } from './features/home/Home'
import { ApiError, fetchMe, logout, type User } from './lib/api'

type Session =
  | { kind: 'checking' }
  | { kind: 'anonymous' }
  | { kind: 'authenticated'; user: User }
  | { kind: 'unreachable'; message: string }

export default function App() {
  const [session, setSession] = useState<Session>({ kind: 'checking' })

  // On load, ask the backend who we are. The session cookie is HttpOnly, so
  // this request is the only way for the page to know whether it is logged in.
  useEffect(() => {
    fetchMe()
      .then((user) => setSession({ kind: 'authenticated', user }))
      .catch((error: unknown) => {
        if (error instanceof ApiError && error.status === 401) {
          setSession({ kind: 'anonymous' })
        } else {
          setSession({
            kind: 'unreachable',
            message: error instanceof Error ? error.message : String(error),
          })
        }
      })
  }, [])

  async function handleLogout() {
    try {
      await logout()
    } finally {
      setSession({ kind: 'anonymous' })
    }
  }

  const signedIn = session.kind === 'authenticated'
  if (!signedIn) {
    return (
      <main className="relative flex min-h-full items-center justify-center overflow-hidden bg-bg px-4 py-10">
        <GraphBackdrop />
        <div className="relative z-10 w-full max-w-sm">
          <div className="mb-6 text-center">
            <span
              aria-hidden="true"
              className="mx-auto flex h-12 w-12 items-center justify-center rounded-2xl bg-accent text-xl font-bold text-on-accent shadow-md"
            >
              D
            </span>
            <h1 className="mt-4 text-2xl font-semibold tracking-tight">DocuMind-AI</h1>
            <p className="mt-1 text-sm text-muted">與你的文件對話。有來源才說，找不到就明說。</p>
          </div>
          {session.kind === 'checking' && <p className="text-center text-muted">載入中…</p>}
          {session.kind === 'unreachable' && (
            <p role="alert" className="panel p-4 text-center text-danger">
              無法連線到後端：{session.message}
            </p>
          )}
          {session.kind === 'anonymous' && (
            <AuthForm onLoggedIn={(user) => setSession({ kind: 'authenticated', user })} />
          )}
          <p className="mt-6 text-center text-xs text-muted">
            PDF · TXT · Markdown · 本地模型 · 每個回答引用檔名與頁碼
          </p>
        </div>
      </main>
    )
  }
  return (
    <main className="flex h-full flex-col">
      <header className="flex items-center gap-3 border-b border-border bg-surface px-5 py-2.5">
        <span
          aria-hidden="true"
          className="flex h-8 w-8 items-center justify-center rounded-lg bg-accent text-sm font-bold text-on-accent"
        >
          D
        </span>
        <div className="flex flex-wrap items-baseline gap-x-3">
          <h1 className="text-base font-semibold">DocuMind-AI</h1>
          <p className="hidden text-sm text-muted sm:block">與你的文件對話</p>
        </div>
        <div className="ml-auto flex items-center gap-3 text-sm">
          <span className="text-muted">
            已登入：<strong className="text-text">{session.user.display_name}</strong>
          </span>
          <button
            type="button"
            className="rounded-full border border-border px-3 py-1 text-sm hover:bg-surface-2"
            onClick={handleLogout}
          >
            登出
          </button>
        </div>
      </header>
      <Home />
    </main>
  )
}
