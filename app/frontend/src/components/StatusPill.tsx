import { useEffect, useState } from 'react'
import { fetchHealth, type Health } from '../lib/api'

type HealthState =
  { kind: 'loading' } | { kind: 'ready'; health: Health } | { kind: 'error'; message: string }

/** System status as one dot in the header (D91): green when the database and the model
 * service answer, red otherwise; the details are in the tooltip. */
export function StatusPill() {
  const [state, setState] = useState<HealthState>({ kind: 'loading' })

  useEffect(() => {
    fetchHealth()
      .then((health) => setState({ kind: 'ready', health }))
      .catch((error: unknown) =>
        setState({
          kind: 'error',
          message: error instanceof Error ? error.message : String(error),
        }),
      )
  }, [])

  if (state.kind === 'loading') {
    return <span className="pill bg-surface-2 text-muted">檢查中…</span>
  }
  if (state.kind === 'error') {
    return (
      <span role="alert" className="pill bg-danger-soft text-danger" title={state.message}>
        ● 無法取得系統狀態
      </span>
    )
  }
  const { health } = state
  const ok = health.status === 'ok'
  const details = [
    `資料庫：${health.database.ok ? '正常' : '異常'}（${health.database.detail}）`,
    `LLM 服務：${health.ollama.ok ? '正常' : '異常'}（${health.ollama.detail}）`,
    `模型 ${health.llm_model} · Embedding ${health.embed_model} · Context 上限 ${health.llm_context_limit.toLocaleString()} tokens`,
  ].join('\n')
  return (
    <span
      className={`pill ${ok ? 'bg-success-soft text-success' : 'bg-danger-soft text-danger'}`}
      title={details}
      aria-label={`系統狀態：${ok ? '全部正常' : '部分異常'}`}
    >
      <span aria-hidden="true">●</span>
      <span>{ok ? '全部正常' : '部分異常'}</span>
      <span className="ml-1 hidden font-mono text-xs opacity-80 md:inline">{health.llm_model}</span>
    </span>
  )
}
