const API = '/api/v1'

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

export type DocumentStatus = 'uploaded' | 'processing' | 'ready' | 'failed'

export interface DocumentItem {
  id: string
  filename: string
  media_type: string
  file_size: number
  status: DocumentStatus
  summary_status: 'none' | 'processing' | 'ready' | 'failed'
  error: string | null
  page_count: number | null
  chunk_count: number
  created_at: string
  updated_at: string
}

export interface User {
  id: string
  username: string
  display_name: string
  answer_language: string
  answer_detail: string
  created_at: string
  last_login_at: string | null
}

/** An error response from the API: `{ detail, code }` plus the HTTP status. */
export class ApiError extends Error {
  readonly status: number
  readonly code: string

  constructor(status: number, code: string, detail: string) {
    super(detail)
    this.status = status
    this.code = code
  }
}

async function request<T>(method: string, path: string, body?: unknown): Promise<T> {
  // A FormData body (file upload) sets its own multipart Content-Type.
  const isForm = body instanceof FormData
  const response = await fetch(`${API}${path}`, {
    method,
    // The session lives in an HttpOnly cookie; the browser sends it for us.
    credentials: 'same-origin',
    headers: body === undefined || isForm ? undefined : { 'Content-Type': 'application/json' },
    body: body === undefined ? undefined : isForm ? body : JSON.stringify(body),
  })
  if (!response.ok) {
    let code = 'HTTP_ERROR'
    let detail = `Backend responded with HTTP ${response.status}`
    try {
      const payload = (await response.json()) as { code?: string; detail?: string }
      code = payload.code ?? code
      detail = payload.detail ?? detail
    } catch {
      // Not a JSON error body (for example a proxy error page); keep the defaults.
    }
    throw new ApiError(response.status, code, detail)
  }
  return response.status === 204 ? (undefined as T) : ((await response.json()) as T)
}

export const fetchHealth = () => request<Health>('GET', '/health')
export const fetchMe = () => request<User>('GET', '/users/me')
export const register = (username: string, password: string) =>
  request<User>('POST', '/auth/register', { username, password })
export const login = (username: string, password: string) =>
  request<User>('POST', '/auth/login', { username, password })
export const logout = () => request<void>('POST', '/auth/logout')

export const listDocuments = () => request<DocumentItem[]>('GET', '/documents')
export const deleteDocument = (id: string) => request<void>('DELETE', `/documents/${id}`)
export const retryDocument = (id: string) =>
  request<DocumentItem>('POST', `/documents/${id}/retry`)
export function uploadDocument(file: File) {
  const form = new FormData()
  form.append('file', file)
  return request<DocumentItem>('POST', '/documents', form)
}

export interface DocumentProgress {
  kind: string
  stage: 'parsing' | 'chunking' | 'embedding' | 'summarizing' | null
  current: number | null
  total: number | null
}

export interface DocumentWatcher {
  onStatus: (status: DocumentStatus) => void
  onProgress: (progress: DocumentProgress) => void
  /** Processing ended, or the stream could not continue. Time to reload the list. */
  onDone: () => void
}

/**
 * Follow the processing of one document through server-sent events.
 * Returns a function that stops watching.
 */
export function watchDocument(id: string, watcher: DocumentWatcher): () => void {
  if (typeof EventSource === 'undefined') return () => {}
  const source = new EventSource(`${API}/documents/${id}/events`)
  const finish = () => {
    // Close first: an EventSource reconnects by itself when the server ends the stream.
    source.close()
    watcher.onDone()
  }
  source.addEventListener('status', (event) => {
    watcher.onStatus((JSON.parse((event as MessageEvent<string>).data) as { status: DocumentStatus }).status)
  })
  source.addEventListener('progress', (event) => {
    watcher.onProgress(JSON.parse((event as MessageEvent<string>).data) as DocumentProgress)
  })
  source.addEventListener('done', finish)
  source.addEventListener('error', (event) => {
    // The server also sends an event named "error" (with data) when processing
    // failed; `done` follows it. Without data it is a connection problem: the
    // browser retries by itself unless it has given up.
    const fromServer = typeof (event as MessageEvent<string>).data === 'string'
    if (!fromServer && source.readyState === EventSource.CLOSED) finish()
  })
  return () => source.close()
}
