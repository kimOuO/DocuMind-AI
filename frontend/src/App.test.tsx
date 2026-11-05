import { render, screen } from '@testing-library/react'
import { afterEach, expect, test, vi } from 'vitest'
import App from './App'
import type { Health } from './lib/api'

const healthy: Health = {
  status: 'ok',
  database: { ok: true, detail: 'pgvector 0.8.0' },
  ollama: { ok: true, detail: 'models available' },
  llm_model: 'qwen3:32b',
  embed_model: 'bge-m3',
  llm_context_limit: 10000,
}

function mockHealth(body: Health) {
  vi.stubGlobal(
    'fetch',
    vi.fn(async () => new Response(JSON.stringify(body), { status: 200 })),
  )
}

afterEach(() => {
  vi.unstubAllGlobals()
})

test('shows that everything is healthy', async () => {
  mockHealth(healthy)
  render(<App />)

  expect(await screen.findByText('全部正常')).toBeInTheDocument()
  expect(screen.getByText(/Context 上限/)).toHaveTextContent('10,000')
})

test('flags a dependency that is down', async () => {
  mockHealth({ ...healthy, status: 'degraded', ollama: { ok: false, detail: 'ConnectError' } })
  render(<App />)

  expect(await screen.findByText('部分異常')).toBeInTheDocument()
  expect(screen.getByText('ConnectError')).toBeInTheDocument()
})

test('reports when the backend cannot be reached', async () => {
  vi.stubGlobal(
    'fetch',
    vi.fn(async () => new Response('', { status: 502 })),
  )
  render(<App />)

  expect(await screen.findByRole('alert')).toHaveTextContent('HTTP 502')
})
