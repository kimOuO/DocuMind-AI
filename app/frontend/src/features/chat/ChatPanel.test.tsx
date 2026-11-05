import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { afterEach, expect, test, vi } from 'vitest'
import type { DocumentItem } from '../../lib/api'
import { ChatPanel } from './ChatPanel'

const PAPER: DocumentItem = {
  id: 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
  filename: 'paper.pdf',
  media_type: 'pdf',
  file_size: 1123301,
  status: 'ready',
  summary_status: 'none',
  error: null,
  page_count: 16,
  chunk_count: 48,
  created_at: '2026-11-05T08:00:00Z',
  updated_at: '2026-11-05T08:00:00Z',
}
const NOTES: DocumentItem = { ...PAPER, id: 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', filename: 'notes.txt' }
const WAITING: DocumentItem = { ...PAPER, id: 'cccccccc-cccc-cccc-cccc-cccccccccccc', filename: 'waiting.md', status: 'processing' }

const CONVERSATION = {
  id: '11111111-1111-1111-1111-111111111111',
  title: '',
  created_at: '2026-11-05T09:00:00Z',
  updated_at: '2026-11-05T09:00:00Z',
}
const SOURCE = {
  index: 1,
  kind: 'chunk',
  document_id: PAPER.id,
  filename: 'paper.pdf',
  page_start: 8,
  page_end: 8,
  section_title: null,
  snippet: 'Table 2: Performance of ablated versions of LightRAG',
  score: 0.7111,
}
const QUESTION = 'Performance of ablated versions of LightRAG'
const ASK = `POST /api/v1/conversations/${CONVERSATION.id}/messages`

type Reply = { status: number; body?: unknown; text?: string }

/** Stub `fetch` with "METHOD path" -> reply; an array is consumed one reply per call. */
function mockApi(routes: Record<string, Reply | Reply[]>) {
  const calls: { key: string; body: unknown }[] = []
  vi.stubGlobal(
    'fetch',
    vi.fn(async (url: string, init?: RequestInit) => {
      const key = `${init?.method ?? 'GET'} ${url}`
      calls.push({ key, body: typeof init?.body === 'string' ? JSON.parse(init.body) : init?.body })
      const entry = routes[key]
      const reply = Array.isArray(entry) ? (entry.length > 1 ? entry.shift()! : entry[0]) : entry
      if (!reply) throw new Error(`unexpected request: ${key}`)
      if (reply.text !== undefined) return new Response(reply.text, { status: reply.status })
      const body = reply.body === undefined ? null : JSON.stringify(reply.body)
      return new Response(reply.status === 204 ? null : body, { status: reply.status })
    }),
  )
  return calls
}

/** An answer stream as the server sends it. */
function sse(events: [string, unknown][]): Reply {
  return {
    status: 200,
    text: events.map(([name, data]) => `event: ${name}\ndata: ${JSON.stringify(data)}\n\n`).join(''),
  }
}

function answerStream(overrides: { done?: object; scope?: object; pieces?: string[] } = {}) {
  const pieces = overrides.pieces ?? ['The ablated versions', ' perform worse [1].']
  return sse([
    [
      'start',
      {
        user_message_id: 'u1',
        assistant_message_id: 'a1',
        scope: overrides.scope ?? { mode: 'all', document_ids: [PAPER.id, NOTES.id] },
      },
    ],
    ['route', { type: 'retrieval', standalone_question: QUESTION }],
    ['sources', [SOURCE]],
    ...pieces.map((text): [string, unknown] => ['delta', { text }]),
    ['usage', { prompt_tokens: 2099, completion_tokens: 298, limit: 10000 }],
    [
      'done',
      { status: 'completed', answered: true, cited: [1], finish_reason: 'stop', ...overrides.done },
    ],
  ])
}

function stored(status = 'completed', answered: boolean | null = true) {
  return {
    ...CONVERSATION,
    title: QUESTION.slice(0, 40),
    messages: [
      { id: 'u1', role: 'user', content: QUESTION, status: 'completed', answered: null, sources: [], created_at: '2026-11-05T09:00:01Z' },
      { id: 'a1', role: 'assistant', content: 'The ablated versions perform worse [1].', status, answered, sources: [SOURCE], created_at: '2026-11-05T09:00:02Z' },
    ],
  }
}

async function ask(text = QUESTION) {
  await userEvent.type(screen.getByLabelText('問題'), text)
  await userEvent.click(screen.getByRole('button', { name: '送出' }))
}

afterEach(() => {
  vi.unstubAllGlobals()
})

test('asking creates a conversation and shows the answer with its sources, scope and usage', async () => {
  const calls = mockApi({
    'GET /api/v1/conversations': [
      { status: 200, body: [] },
      { status: 200, body: [{ ...CONVERSATION, title: QUESTION.slice(0, 40) }] },
    ],
    'POST /api/v1/conversations': { status: 201, body: CONVERSATION },
    [ASK]: answerStream(),
    [`GET /api/v1/conversations/${CONVERSATION.id}`]: { status: 200, body: stored() },
  })
  render(<ChatPanel documents={[PAPER, NOTES]} />)

  await ask()

  const conversation = await screen.findByRole('list', { name: '對話內容' })
  expect(within(conversation).getByText(QUESTION)).toBeInTheDocument()
  expect(within(conversation).getByText('The ablated versions perform worse [1].')).toBeInTheDocument()
  expect(within(conversation).getByText(/\[1\] paper\.pdf · 第 8 頁/)).toBeInTheDocument()
  expect(within(conversation).getByText(SOURCE.snippet)).toBeInTheDocument()
  // No document was ticked: the whole library is searched, and the page says so.
  expect(screen.getByText('這次搜尋的範圍：所有可用文件（2 份）')).toBeInTheDocument()
  expect(screen.getByText(/輸入 2,099 \+ 回答 298 = 2,397 \/ 10,000/)).toBeInTheDocument()
  expect(calls.find((c) => c.key === ASK)!.body).toEqual({ question: QUESTION, document_ids: [] })
  // A finished answer carries no warning label, and the question box is cleared.
  expect(screen.queryByText('回答未完成')).not.toBeInTheDocument()
  expect(screen.getByLabelText('問題')).toHaveValue('')
  // The new conversation is selected, under the title the server gave it.
  expect(await screen.findByRole('option', { name: QUESTION.slice(0, 40) })).toBeInTheDocument()
})

test('ticked documents limit the search and are named as the scope', async () => {
  const calls = mockApi({
    'GET /api/v1/conversations': { status: 200, body: [] },
    'POST /api/v1/conversations': { status: 201, body: CONVERSATION },
    [ASK]: answerStream({ scope: { mode: 'selected', document_ids: [NOTES.id] } }),
    [`GET /api/v1/conversations/${CONVERSATION.id}`]: { status: 200, body: stored() },
  })
  render(<ChatPanel documents={[PAPER, NOTES, WAITING]} />)

  // Only documents that are ready can be chosen.
  expect(screen.queryByLabelText('waiting.md')).not.toBeInTheDocument()
  expect(screen.getByText('搜尋範圍：所有可用文件')).toBeInTheDocument()
  await userEvent.click(screen.getByLabelText('notes.txt'))
  expect(screen.getByText('搜尋範圍：已選 1 份')).toBeInTheDocument()
  await ask()

  expect(await screen.findByText('這次搜尋的範圍：notes.txt')).toBeInTheDocument()
  expect(calls.find((c) => c.key === ASK)!.body).toEqual({
    question: QUESTION,
    document_ids: [NOTES.id],
  })
})

test('an answer that was cut short is labelled as unfinished', async () => {
  mockApi({
    'GET /api/v1/conversations': { status: 200, body: [] },
    'POST /api/v1/conversations': { status: 201, body: CONVERSATION },
    [ASK]: answerStream({ done: { status: 'interrupted', answered: null, finish_reason: 'output_limit' } }),
    [`GET /api/v1/conversations/${CONVERSATION.id}`]: { status: 200, body: stored('interrupted', null) },
  })
  render(<ChatPanel documents={[PAPER]} />)

  await ask()

  expect(await screen.findByText('回答未完成')).toBeInTheDocument()
  // What was produced is still shown.
  expect(screen.getByText('The ablated versions perform worse [1].')).toBeInTheDocument()
})

test('an answer without any cited source is labelled as not found', async () => {
  mockApi({
    'GET /api/v1/conversations': { status: 200, body: [] },
    'POST /api/v1/conversations': { status: 201, body: CONVERSATION },
    [ASK]: answerStream({ done: { answered: false, cited: [] } }),
    [`GET /api/v1/conversations/${CONVERSATION.id}`]: { status: 200, body: stored('completed', false) },
  })
  render(<ChatPanel documents={[PAPER]} />)

  await ask()

  expect(await screen.findByText('文件中找不到答案')).toBeInTheDocument()
})

test('a failure reported during the answer marks it failed and explains', async () => {
  mockApi({
    'GET /api/v1/conversations': { status: 200, body: [] },
    'POST /api/v1/conversations': { status: 201, body: CONVERSATION },
    [ASK]: sse([
      ['start', { user_message_id: 'u1', assistant_message_id: 'a1', scope: { mode: 'all', document_ids: [PAPER.id] } }],
      ['route', { type: 'retrieval', standalone_question: QUESTION }],
      ['sources', [SOURCE]],
      ['error', { code: 'LLM_UNAVAILABLE', detail: 'Ollama answered 500' }],
    ]),
    [`GET /api/v1/conversations/${CONVERSATION.id}`]: { status: 200, body: stored('failed', null) },
  })
  render(<ChatPanel documents={[PAPER]} />)

  await ask()

  expect(await screen.findByText('回答失敗')).toBeInTheDocument()
  expect(screen.getByRole('alert')).toHaveTextContent('語言模型目前無法使用')
})

test('a question that is too long is refused and stays in the box', async () => {
  mockApi({
    'GET /api/v1/conversations': { status: 200, body: [] },
    'POST /api/v1/conversations': { status: 201, body: CONVERSATION },
    [ASK]: { status: 422, body: { code: 'QUESTION_TOO_LONG', detail: 'The question is 360 tokens long.' } },
  })
  render(<ChatPanel documents={[PAPER]} />)

  await ask('a very long question')

  expect(await screen.findByRole('alert')).toHaveTextContent('問題太長，請縮短後再送出。')
  expect(screen.getByLabelText('問題')).toHaveValue('a very long question')
  expect(screen.queryByRole('list', { name: '對話內容' })).not.toBeInTheDocument()
})

test('without a ready document nothing can be asked', async () => {
  mockApi({ 'GET /api/v1/conversations': { status: 200, body: [] } })
  render(<ChatPanel documents={[WAITING]} />)

  expect(await screen.findByText(/還沒有可以提問的文件/)).toBeInTheDocument()
  expect(screen.getByLabelText('問題')).toBeDisabled()
  expect(screen.getByRole('button', { name: '送出' })).toBeDisabled()
})

test('an earlier conversation can be opened, with unfinished answers still labelled, and deleted', async () => {
  const earlier = { ...CONVERSATION, title: 'ablation' }
  const calls = mockApi({
    'GET /api/v1/conversations': { status: 200, body: [earlier] },
    [`GET /api/v1/conversations/${CONVERSATION.id}`]: {
      status: 200,
      body: { ...stored('interrupted', null), title: 'ablation' },
    },
    [`DELETE /api/v1/conversations/${CONVERSATION.id}`]: { status: 204 },
  })
  render(<ChatPanel documents={[PAPER]} />)

  await userEvent.selectOptions(await screen.findByLabelText('對話'), await screen.findByRole('option', { name: 'ablation' }))

  expect(await screen.findByText(QUESTION)).toBeInTheDocument()
  expect(screen.getByText('回答未完成')).toBeInTheDocument()

  await userEvent.click(screen.getByRole('button', { name: '刪除對話' }))
  const dialog = screen.getByRole('dialog', { name: '刪除對話' })
  expect(dialog).toHaveTextContent('ablation')
  await userEvent.click(within(dialog).getByRole('button', { name: '確定刪除' }))

  expect(await screen.findByRole('option', { name: '新對話' })).toBeInTheDocument()
  expect(screen.queryByRole('option', { name: 'ablation' })).not.toBeInTheDocument()
  expect(screen.queryByText(QUESTION)).not.toBeInTheDocument()
  expect(calls.map((c) => c.key)).toContain(`DELETE /api/v1/conversations/${CONVERSATION.id}`)
})
