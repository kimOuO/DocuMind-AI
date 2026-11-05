import { useEffect, useState } from 'react'
import { fetchHealth, type DependencyStatus, type Health } from './lib/api'

type State =
  | { kind: 'loading' }
  | { kind: 'ready'; health: Health }
  | { kind: 'error'; message: string }

function StatusRow({ label, status }: { label: string; status: DependencyStatus }) {
  return (
    <li className="flex items-baseline justify-between gap-4 border-t border-border py-2">
      <span>{label}</span>
      <span className={status.ok ? 'text-success' : 'text-danger'}>
        {status.ok ? '正常' : '異常'}
        <span className="ml-2 font-mono text-sm text-muted">{status.detail}</span>
      </span>
    </li>
  )
}

/** P0 placeholder: proves the frontend, backend, database and LLM server are wired up. */
export default function App() {
  const [state, setState] = useState<State>({ kind: 'loading' })

  useEffect(() => {
    fetchHealth()
      .then((health) => setState({ kind: 'ready', health }))
      .catch((error: unknown) =>
        setState({ kind: 'error', message: error instanceof Error ? error.message : String(error) }),
      )
  }, [])

  return (
    <main className="mx-auto max-w-xl px-4 py-16">
      <h1 className="text-2xl font-semibold">DocuMind-AI</h1>
      <p className="mt-1 text-muted">讓 AI 跟文件對話 · 系統狀態</p>

      <section className="mt-6 rounded-lg border border-border bg-surface p-4">
        {state.kind === 'loading' && <p>檢查中…</p>}
        {state.kind === 'error' && (
          <p role="alert" className="text-danger">
            無法連線到後端：{state.message}
          </p>
        )}
        {state.kind === 'ready' && (
          <>
            <p>
              整體狀態：
              <strong className={state.health.status === 'ok' ? 'text-success' : 'text-danger'}>
                {state.health.status === 'ok' ? '全部正常' : '部分異常'}
              </strong>
            </p>
            <ul className="mt-3 list-none p-0">
              <StatusRow label="資料庫（PostgreSQL + pgvector）" status={state.health.database} />
              <StatusRow label="LLM 服務（Ollama）" status={state.health.ollama} />
            </ul>
            <p className="mt-3 text-sm text-muted">
              模型 {state.health.llm_model} · Embedding {state.health.embed_model} · Context 上限{' '}
              {state.health.llm_context_limit.toLocaleString()} tokens
            </p>
          </>
        )}
      </section>
    </main>
  )
}
