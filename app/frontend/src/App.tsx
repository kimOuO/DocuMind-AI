import { useEffect, useState } from 'react'
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

  return (
    <main className="mx-auto max-w-xl px-4 py-12">
      <h1 className="text-2xl font-semibold">DocuMind-AI</h1>
      <p className="mt-1 text-muted">AI 文件管理與問答平台</p>

      {session.kind === 'checking' && <p className="mt-6">載入中…</p>}
      {session.kind === 'unreachable' && (
        <p role="alert" className="mt-6 text-danger">
          無法連線到後端：{session.message}
        </p>
      )}
      {session.kind === 'anonymous' && (
        <AuthForm onLoggedIn={(user) => setSession({ kind: 'authenticated', user })} />
      )}
      {session.kind === 'authenticated' && <Home user={session.user} onLogout={handleLogout} />}
    </main>
  )
}
