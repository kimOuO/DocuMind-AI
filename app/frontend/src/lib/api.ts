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
  const response = await fetch(`${API}${path}`, {
    method,
    // The session lives in an HttpOnly cookie; the browser sends it for us.
    credentials: 'same-origin',
    headers: body === undefined ? undefined : { 'Content-Type': 'application/json' },
    body: body === undefined ? undefined : JSON.stringify(body),
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
