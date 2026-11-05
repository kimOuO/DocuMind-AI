export interface DependencyStatus {
  ok: boolean
  detail: string
}

export interface Health {
  status: 'ok' | 'degraded'
  database: DependencyStatus
  ollama: DependencyStatus
  llm_model: string
  embed_model: string
  llm_context_limit: number
}

export async function fetchHealth(): Promise<Health> {
  const response = await fetch('/api/v1/health')
  if (!response.ok) {
    throw new Error(`Backend responded with HTTP ${response.status}`)
  }
  return (await response.json()) as Health
}
