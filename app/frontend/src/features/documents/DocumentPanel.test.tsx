import { act, render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { afterEach, beforeEach, expect, test, vi } from 'vitest'
import { formatSize } from '../../lib/format'
import { DocumentPanel } from './DocumentPanel'

const PAPER = {
  id: 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
  filename: '2410.05779v3.pdf',
  media_type: 'pdf',
  file_size: 1123301,
  status: 'uploaded',
  summary_status: 'none',
  error: null,
  page_count: null,
  chunk_count: 0,
  created_at: '2026-11-05T08:00:00Z',
  updated_at: '2026-11-05T08:00:00Z',
}
const NOTES = { ...PAPER, id: 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', filename: 'notes.txt', file_size: 61 }

type Reply = { status: number; body?: unknown }

/** Stub `fetch` with "METHOD path" -> reply; an array is consumed one reply per call. */
function mockApi(routes: Record<string, Reply | Reply[]>) {
  const calls: { key: string; body: unknown }[] = []
  vi.stubGlobal(
    'fetch',
    vi.fn(async (url: string, init?: RequestInit) => {
      const key = `${init?.method ?? 'GET'} ${url}`
      calls.push({ key, body: init?.body })
      const entry = routes[key]
      const reply = Array.isArray(entry) ? (entry.length > 1 ? entry.shift()! : entry[0]) : entry
      if (!reply) throw new Error(`unexpected request: ${key}`)
      const body = reply.body === undefined ? null : JSON.stringify(reply.body)
      return new Response(reply.status === 204 ? null : body, { status: reply.status })
    }),
  )
  return calls
}

/** Stands in for the browser's EventSource; tests push events through it. */
class FakeEventSource {
  static readonly CLOSED = 2
  static instances: FakeEventSource[] = []
  readonly url: string
  readyState = 1
  private listeners = new Map<string, ((event: unknown) => void)[]>()

  constructor(url: string) {
    this.url = url
    FakeEventSource.instances.push(this)
  }

  addEventListener(name: string, listener: (event: unknown) => void) {
    this.listeners.set(name, [...(this.listeners.get(name) ?? []), listener])
  }

  close() {
    this.readyState = FakeEventSource.CLOSED
  }

  /** Deliver a server-sent event; without data it is a plain connection error. */
  emit(name: string, data?: unknown) {
    const event = data === undefined ? {} : { data: JSON.stringify(data) }
    for (const listener of this.listeners.get(name) ?? []) listener(event)
  }
}

const streamFor = (id: string) =>
  FakeEventSource.instances.find((source) => source.url === `/api/v1/documents/${id}/events`)

beforeEach(() => {
  FakeEventSource.instances = []
  vi.stubGlobal('EventSource', FakeEventSource)
})

afterEach(() => {
  vi.unstubAllGlobals()
})

test('shows an empty state when there are no documents', async () => {
  mockApi({ 'GET /api/v1/documents': { status: 200, body: [] } })
  render(<DocumentPanel />)

  expect(await screen.findByText(/還沒有文件/)).toBeInTheDocument()
})

test('lists my documents with their size and status', async () => {
  mockApi({
    'GET /api/v1/documents': {
      status: 200,
      body: [PAPER, { ...NOTES, status: 'ready', page_count: 1, chunk_count: 1 }],
    },
  })
  render(<DocumentPanel />)

  const paper = (await screen.findByText('2410.05779v3.pdf')).closest('li')!
  expect(within(paper).getByText(/1\.1 MB/)).toBeInTheDocument()
  expect(within(paper).getByText('已上傳，等待處理')).toBeInTheDocument()
  const notes = screen.getByText('notes.txt').closest('li')!
  expect(within(notes).getByText('可以提問 · 1 頁 · 1 個片段')).toBeInTheDocument()
})

test('uploading a file sends it and refreshes the list', async () => {
  const calls = mockApi({
    'GET /api/v1/documents': [
      { status: 200, body: [] },
      { status: 200, body: [NOTES] },
    ],
    'POST /api/v1/documents': { status: 202, body: NOTES },
  })
  render(<DocumentPanel />)
  await screen.findByText(/還沒有文件/)

  const file = new File(['hello'], 'notes.txt', { type: 'text/plain' })
  await userEvent.upload(screen.getByLabelText(/上傳文件/), file)

  expect(await screen.findByRole('status')).toHaveTextContent('已上傳 notes.txt')
  expect(await screen.findByText('notes.txt')).toBeInTheDocument()
  const post = calls.find((c) => c.key === 'POST /api/v1/documents')!
  expect(post.body).toBeInstanceOf(FormData)
  expect((post.body as FormData).get('file')).toBeInstanceOf(File)
})

test('uploading content that already exists says so', async () => {
  mockApi({
    'GET /api/v1/documents': { status: 200, body: [NOTES] },
    'POST /api/v1/documents': { status: 200, body: NOTES },
  })
  render(<DocumentPanel />)
  await screen.findByText('notes.txt')

  await userEvent.upload(screen.getByLabelText(/上傳文件/), new File(['hello'], 'copy.txt'))

  expect(await screen.findByRole('status')).toHaveTextContent('先前已經上傳過')
})

test('an unsupported format shows an explanation', async () => {
  mockApi({
    'GET /api/v1/documents': { status: 200, body: [] },
    'POST /api/v1/documents': {
      status: 415,
      body: { code: 'UNSUPPORTED_MEDIA_TYPE', detail: 'Unsupported file type.' },
    },
  })
  render(<DocumentPanel />)
  await screen.findByText(/還沒有文件/)

  // Bypass the input's accept filter, as a drag-and-drop or a renamed file would.
  await userEvent.upload(screen.getByLabelText(/上傳文件/), new File(['x'], 'report.docx'), {
    applyAccept: false,
  })

  expect(await screen.findByRole('alert')).toHaveTextContent('不支援這個檔案格式')
})

test('deleting asks for confirmation in the platform dialog, then removes the document', async () => {
  const calls = mockApi({
    'GET /api/v1/documents': [
      { status: 200, body: [NOTES] },
      { status: 200, body: [] },
    ],
    [`DELETE /api/v1/documents/${NOTES.id}`]: { status: 204 },
  })
  render(<DocumentPanel />)

  await userEvent.click(await screen.findByRole('button', { name: '刪除 notes.txt' }))

  const dialog = screen.getByRole('dialog', { name: '刪除文件' })
  expect(dialog).toHaveTextContent('notes.txt')
  expect(calls.every((c) => !c.key.startsWith('DELETE'))).toBe(true)

  await userEvent.click(within(dialog).getByRole('button', { name: '確定刪除' }))

  expect(await screen.findByText(/還沒有文件/)).toBeInTheDocument()
  expect(screen.queryByRole('dialog')).not.toBeInTheDocument()
  expect(calls.map((c) => c.key)).toContain(`DELETE /api/v1/documents/${NOTES.id}`)
})

test('cancelling the dialog deletes nothing', async () => {
  const calls = mockApi({ 'GET /api/v1/documents': { status: 200, body: [NOTES] } })
  render(<DocumentPanel />)

  await userEvent.click(await screen.findByRole('button', { name: '刪除 notes.txt' }))
  await userEvent.click(within(screen.getByRole('dialog')).getByRole('button', { name: '取消' }))

  expect(screen.queryByRole('dialog')).not.toBeInTheDocument()
  expect(screen.getByText('notes.txt')).toBeInTheDocument()
  expect(calls.every((c) => !c.key.startsWith('DELETE'))).toBe(true)
})

test('pressing Escape closes the dialog without deleting', async () => {
  const calls = mockApi({ 'GET /api/v1/documents': { status: 200, body: [NOTES] } })
  render(<DocumentPanel />)

  await userEvent.click(await screen.findByRole('button', { name: '刪除 notes.txt' }))
  await userEvent.keyboard('{Escape}')

  expect(screen.queryByRole('dialog')).not.toBeInTheDocument()
  expect(calls.every((c) => !c.key.startsWith('DELETE'))).toBe(true)
})

test('follows a document that is being processed and shows its progress', async () => {
  mockApi({
    'GET /api/v1/documents': [
      { status: 200, body: [PAPER] },
      { status: 200, body: [{ ...PAPER, status: 'ready', page_count: 16, chunk_count: 48 }] },
    ],
  })
  render(<DocumentPanel />)
  await screen.findByText('已上傳，等待處理')
  const stream = streamFor(PAPER.id)!

  act(() => stream.emit('status', { status: 'processing', summary_status: 'none' }))
  act(() => stream.emit('progress', { kind: 'index', stage: 'embedding', current: 16, total: 48 }))
  expect(screen.getByText('處理中：建立索引 16/48')).toBeInTheDocument()

  act(() => stream.emit('done', { status: 'ready', summary_status: 'none' }))

  expect(await screen.findByText('可以提問 · 16 頁 · 48 個片段')).toBeInTheDocument()
  expect(stream.readyState).toBe(FakeEventSource.CLOSED)
})

test('does not follow documents that are already finished', async () => {
  mockApi({ 'GET /api/v1/documents': { status: 200, body: [{ ...NOTES, status: 'ready' }] } })
  render(<DocumentPanel />)

  await screen.findByText('notes.txt')

  expect(FakeEventSource.instances).toHaveLength(0)
})

test('a failed document shows why and can be retried', async () => {
  const failed = { ...NOTES, status: 'failed', error: 'The embedding service answered 500.' }
  const calls = mockApi({
    'GET /api/v1/documents': [
      { status: 200, body: [failed] },
      { status: 200, body: [{ ...NOTES, status: 'processing' }] },
    ],
    [`POST /api/v1/documents/${NOTES.id}/retry`]: { status: 202, body: { ...NOTES, status: 'processing' } },
  })
  render(<DocumentPanel />)

  expect(await screen.findByText('處理失敗')).toBeInTheDocument()
  expect(screen.getByText('原因：The embedding service answered 500.')).toBeInTheDocument()
  await userEvent.click(screen.getByRole('button', { name: '重試 notes.txt' }))

  expect(await screen.findByRole('status')).toHaveTextContent('已重新排入處理')
  expect(calls.map((c) => c.key)).toContain(`POST /api/v1/documents/${NOTES.id}/retry`)
  expect(screen.queryByRole('button', { name: '重試 notes.txt' })).not.toBeInTheDocument()
  // The retried document is followed again.
  expect(streamFor(NOTES.id)).toBeDefined()
})

test('a processing failure reported by the stream shows the reason after reloading', async () => {
  mockApi({
    'GET /api/v1/documents': [
      { status: 200, body: [PAPER] },
      { status: 200, body: [{ ...PAPER, status: 'failed', error: 'No text could be extracted.' }] },
    ],
  })
  render(<DocumentPanel />)
  await screen.findByText('已上傳，等待處理')
  const stream = streamFor(PAPER.id)!

  // The server's own "error" event carries data and is followed by "done".
  act(() => stream.emit('error', { kind: 'index', detail: 'No text could be extracted.' }))
  expect(stream.readyState).not.toBe(FakeEventSource.CLOSED)
  act(() => stream.emit('done', { status: 'failed', summary_status: 'none' }))

  expect(await screen.findByText('原因：No text could be extracted.')).toBeInTheDocument()
})

test('stops following when the panel goes away', async () => {
  mockApi({ 'GET /api/v1/documents': { status: 200, body: [PAPER] } })
  const { unmount } = render(<DocumentPanel />)
  await screen.findByText('已上傳，等待處理')

  unmount()

  expect(streamFor(PAPER.id)!.readyState).toBe(FakeEventSource.CLOSED)
})

test('formats file sizes', () => {
  expect(formatSize(61)).toBe('61 B')
  expect(formatSize(2048)).toBe('2.0 KB')
  expect(formatSize(1123301)).toBe('1.1 MB')
})
