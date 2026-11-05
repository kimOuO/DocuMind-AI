import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { afterEach, expect, test, vi } from 'vitest'
import App from './App'

const USER = {
  id: '11111111-1111-1111-1111-111111111111',
  username: 'kim',
  display_name: 'kim',
  answer_language: 'auto',
  answer_detail: 'normal',
  created_at: '2026-11-05T00:00:00Z',
  last_login_at: '2026-11-05T00:00:00Z',
}
const HEALTH = {
  status: 'ok',
  database: { ok: true, detail: 'pgvector 0.8.7' },
  ollama: { ok: true, detail: 'models available' },
  llm_model: 'qwen3:32b',
  embed_model: 'bge-m3',
  llm_context_limit: 10000,
}

type Reply = { status: number; body?: unknown }

/** Stub `fetch` with a table of "METHOD path" -> reply; replies may be queued in an array. */
function mockApi(routes: Record<string, Reply | Reply[]>) {
  const calls: string[] = []
  vi.stubGlobal(
    'fetch',
    vi.fn(async (url: string, init?: RequestInit) => {
      const key = `${init?.method ?? 'GET'} ${url}`
      calls.push(key)
      const entry = routes[key]
      const reply = Array.isArray(entry) ? (entry.length > 1 ? entry.shift()! : entry[0]) : entry
      if (!reply) throw new Error(`unexpected request: ${key}`)
      const body = reply.body === undefined ? null : JSON.stringify(reply.body)
      return new Response(reply.status === 204 ? null : body, { status: reply.status })
    }),
  )
  return calls
}

const UNAUTHENTICATED = { status: 401, body: { code: 'NOT_AUTHENTICATED', detail: 'Please log in.' } }

afterEach(() => {
  vi.unstubAllGlobals()
})

test('shows the login form when nobody is logged in', async () => {
  mockApi({ 'GET /api/v1/users/me': UNAUTHENTICATED })
  render(<App />)

  expect(await screen.findByRole('heading', { name: '登入' })).toBeInTheDocument()
  expect(screen.queryByText(/已登入/)).not.toBeInTheDocument()
})

test('logging in shows who is logged in and the system status', async () => {
  const calls = mockApi({
    'GET /api/v1/users/me': UNAUTHENTICATED,
    'POST /api/v1/auth/login': { status: 200, body: USER },
    'GET /api/v1/health': { status: 200, body: HEALTH },
    'GET /api/v1/documents': { status: 200, body: [] },
    'GET /api/v1/conversations': { status: 200, body: [] },
  })
  render(<App />)

  await userEvent.type(await screen.findByLabelText('使用者名稱'), 'kim')
  await userEvent.type(screen.getByLabelText('密碼'), 's3cret-password')
  await userEvent.click(screen.getByRole('button', { name: '登入' }))

  expect(await screen.findByText('kim')).toBeInTheDocument()
  expect(await screen.findByText('全部正常')).toBeInTheDocument()
  expect(calls).toContain('POST /api/v1/auth/login')
})

test('a wrong password shows a message and stays on the form', async () => {
  mockApi({
    'GET /api/v1/users/me': UNAUTHENTICATED,
    'POST /api/v1/auth/login': {
      status: 401,
      body: { code: 'INVALID_CREDENTIALS', detail: 'Incorrect username or password.' },
    },
  })
  render(<App />)

  await userEvent.type(await screen.findByLabelText('使用者名稱'), 'kim')
  await userEvent.type(screen.getByLabelText('密碼'), 'wrong-password')
  await userEvent.click(screen.getByRole('button', { name: '登入' }))

  expect(await screen.findByRole('alert')).toHaveTextContent('帳號或密碼不正確')
  expect(screen.getByRole('heading', { name: '登入' })).toBeInTheDocument()
})

test('registering asks the user to log in afterwards', async () => {
  const calls = mockApi({
    'GET /api/v1/users/me': UNAUTHENTICATED,
    'POST /api/v1/auth/register': { status: 201, body: USER },
  })
  render(<App />)

  await userEvent.click(await screen.findByRole('button', { name: /還沒有帳號/ }))
  await userEvent.type(screen.getByLabelText('使用者名稱'), 'kim')
  await userEvent.type(screen.getByLabelText('密碼'), 's3cret-password')
  await userEvent.click(screen.getByRole('button', { name: '建立帳號' }))

  expect(await screen.findByRole('status')).toHaveTextContent('註冊成功')
  expect(screen.getByRole('heading', { name: '登入' })).toBeInTheDocument()
  expect(calls).not.toContain('POST /api/v1/auth/login')
})

test('an existing session goes straight to the signed-in page, and logout returns to login', async () => {
  const calls = mockApi({
    'GET /api/v1/users/me': { status: 200, body: USER },
    'GET /api/v1/health': { status: 200, body: HEALTH },
    'GET /api/v1/documents': { status: 200, body: [] },
    'GET /api/v1/conversations': { status: 200, body: [] },
    'POST /api/v1/auth/logout': { status: 204 },
  })
  render(<App />)

  expect(await screen.findByText(/已登入/)).toBeInTheDocument()
  await userEvent.click(screen.getByRole('button', { name: '登出' }))

  expect(await screen.findByRole('heading', { name: '登入' })).toBeInTheDocument()
  expect(calls).toContain('POST /api/v1/auth/logout')
})

test('reports when the backend cannot be reached', async () => {
  mockApi({ 'GET /api/v1/users/me': { status: 502 } })
  render(<App />)

  expect(await screen.findByRole('alert')).toHaveTextContent('HTTP 502')
})
