import { useEffect, useState } from 'react'
import {
  fetchHealth,
  type DependencyStatus,
  type DocumentItem,
  type Health,
  type User,
} from '../../lib/api'
import { ChatPanel } from '../chat/ChatPanel'
import { DocumentPanel } from '../documents/DocumentPanel'

type HealthState =
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

/** The signed-in area: who is logged in, their documents, questions, and whether the system is up. */
export function Home({ user, onLogout }: { user: User; onLogout: () => void }) {
  const [state, setState] = useState<HealthState>({ kind: 'loading' })
  const [documents, setDocuments] = useState<DocumentItem[]>([])

  useEffect(() => {
    fetchHealth()
      .then((health) => setState({ kind: 'ready', health }))
      .catch((error: unknown) =>
        setState({ kind: 'error', message: error instanceof Error ? error.message : String(error) }),
      )
  }, [])

  return (
    <>
      <div className="mt-6 flex items-center justify-between">
        <p>
          已登入：<strong>{user.display_name}</strong>
        </p>
        <button
          type="button"
          className="rounded-md border border-border px-3 py-1 text-sm"
          onClick={onLogout}
        >
          登出
        </button>
      </div>

      <DocumentPanel onChange={setDocuments} />
      <ChatPanel documents={documents} />

      <section className="mt-4 rounded-lg border border-border bg-surface p-4">
        <h2 className="font-semibold">系統狀態</h2>
        {state.kind === 'loading' && <p className="mt-2">檢查中…</p>}
        {state.kind === 'error' && (
          <p role="alert" className="mt-2 text-danger">
            無法取得系統狀態：{state.message}
          </p>
        )}
        {state.kind === 'ready' && (
          <>
            <p className="mt-2">
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
    </>
  )
}
