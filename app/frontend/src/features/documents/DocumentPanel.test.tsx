import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { afterEach, expect, test, vi } from 'vitest'
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
    'GET /api/v1/documents': { status: 200, body: [PAPER, { ...NOTES, status: 'ready' }] },
  })
  render(<DocumentPanel />)

  const paper = (await screen.findByText('2410.05779v3.pdf')).closest('li')!
  expect(within(paper).getByText(/1\.1 MB/)).toBeInTheDocument()
  expect(within(paper).getByText('已上傳，等待處理')).toBeInTheDocument()
  const notes = screen.getByText('notes.txt').closest('li')!
  expect(within(notes).getByText('可以提問')).toBeInTheDocument()
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

test('formats file sizes', () => {
  expect(formatSize(61)).toBe('61 B')
  expect(formatSize(2048)).toBe('2.0 KB')
  expect(formatSize(1123301)).toBe('1.1 MB')
})
