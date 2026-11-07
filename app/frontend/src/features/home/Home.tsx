import { useEffect, useState } from 'react'
import {
  fetchHealth,
  type DependencyStatus,
  type DocumentItem,
  type Health,
} from '../../lib/api'
import { ChatPanel } from '../chat/ChatPanel'
import { DocumentPanel } from '../documents/DocumentPanel'

type HealthState =
  | { kind: 'loading' }
  | { kind: 'ready'; health: Health }
  | { kind: 'error'; message: string }

function StatusRow({ label, status }: { label: string; status: DependencyStatus }) {
  return (
    <li className="flex items-baseline justify-between gap-4 border-t border-border py-2 text-sm">
      <span>{label}</span>
      <span className={`pill ${status.ok ? 'bg-success-soft text-success' : 'bg-danger-soft text-danger'}`}>
        {status.ok ? '正常' : '異常'}
        <span className="ml-1 font-mono text-xs opacity-80">{status.detail}</span>
      </span>
    </li>
  )
}

/** The signed-in workspace: sources on the left, the conversation and its inspector on the right. */
export function Home() {
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
    <div className="grid min-h-0 flex-1 gap-4 p-4 lg:grid-cols-[minmax(280px,320px)_minmax(0,1fr)]">
      <div className="min-h-0 min-w-0 space-y-4 overflow-y-auto">
        <DocumentPanel onChange={setDocuments} />
        <SystemStatus state={state} />
      </div>
      <div className="min-h-0 min-w-0">
        <ChatPanel documents={documents} />
      </div>
    </div>
  )
}

function SystemStatus({ state }: { state: HealthState }) {
  return (
    <>
      <section className="panel p-4">
        <h2 className="text-sm font-semibold text-muted">系統狀態</h2>
        {state.kind === 'loading' && <p className="mt-2">檢查中…</p>}
        {state.kind === 'error' && (
          <p role="alert" className="mt-2 text-danger">
            無法取得系統狀態：{state.message}
          </p>
        )}
        {state.kind === 'ready' && (
          <>
            <p className="mt-2 text-sm">
              整體狀態：
              <strong className={state.health.status === 'ok' ? 'text-success' : 'text-danger'}>
                {state.health.status === 'ok' ? '全部正常' : '部分異常'}
              </strong>
            </p>
            <ul className="mt-3 list-none p-0">
              <StatusRow label="資料庫（PostgreSQL + pgvector）" status={state.health.database} />
              <StatusRow label="LLM 服務（Ollama）" status={state.health.ollama} />
            </ul>
            <p className="mt-3 text-xs text-muted">
              模型 {state.health.llm_model} · Embedding {state.health.embed_model} · Context 上限{' '}
              {state.health.llm_context_limit.toLocaleString()} tokens
            </p>
          </>
        )}
      </section>
    </>
  )
}
