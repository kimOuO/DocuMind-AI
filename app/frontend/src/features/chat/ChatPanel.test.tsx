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
  origin: 'retrieval',
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

const NO_NUMBERS = {
  unverified_numbers: [],
  verified_numbers: [],
  mislabelled_numbers: [],
  unresolved_numbers: [],
  overstated_claims: [],
  doubtful_citations: [],
}

function answerStream(
  overrides: { done?: object; scope?: object; pieces?: string[]; sources?: object[]; route?: object } = {},
) {
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
    ['route', overrides.route ?? { type: 'retrieval', standalone_question: QUESTION }],
    ['sources', overrides.sources ?? [SOURCE]],
    ...pieces.map((text): [string, unknown] => ['delta', { text }]),
    ['usage', { prompt_tokens: 2099, completion_tokens: 298, limit: 10000 }],
    [
      'done',
      {
        status: 'completed',
        answered: true,
        cited: [1],
        finish_reason: 'stop',
        ...NO_NUMBERS,
        ...overrides.done,
      },
    ],
  ])
}

function stored(status = 'completed', answered: boolean | null = true, sources: object[] = [SOURCE]) {
  return {
    ...CONVERSATION,
    title: QUESTION.slice(0, 40),
    messages: [
      { id: 'u1', role: 'user', content: QUESTION, status: 'completed', answered: null, sources: [], created_at: '2026-11-05T09:00:01Z' },
      { id: 'a1', role: 'assistant', content: 'The ablated versions perform worse [1].', status, answered, sources, created_at: '2026-11-05T09:00:02Z' },
    ],
  }
}

/** The routes every answer test needs: a new conversation, the stream, the stored result. */
function routesFor(stream: Reply, storedDetail: object = stored()) {
  return {
    'GET /api/v1/conversations': [
      { status: 200, body: [] },
      { status: 200, body: [{ ...CONVERSATION, title: QUESTION.slice(0, 40) }] },
    ],
    'POST /api/v1/conversations': { status: 201, body: CONVERSATION },
    [ASK]: stream,
    [`GET /api/v1/conversations/${CONVERSATION.id}`]: { status: 200, body: storedDetail },
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

test('summary sources show their section and page range, and added context is labelled', async () => {
  const whole = { ...SOURCE, kind: 'summary', page_start: 1, page_end: 16, snippet: 'LightRAG combines…', score: null, origin: 'summary' }
  const section = { ...whole, index: 2, page_start: 7, page_end: 9, section_title: '4 Evaluation', snippet: 'LightRAG wins 83.6%…' }
  const context = { ...SOURCE, index: 3, origin: 'table_context', score: null, snippet: 'The -High variant removes…' }
  const sources = [whole, section, context]
  mockApi(
    routesFor(
      answerStream({ sources, route: { type: 'summary', standalone_question: 'summary this document.' } }),
      stored('completed', true, sources),
    ),
  )
  render(<ChatPanel documents={[PAPER]} />)

  await ask('summary this document.')

  const conversation = await screen.findByRole('list', { name: '對話內容' })
  const headings = within(conversation)
    .getAllByText((_, element) => element?.tagName === 'SUMMARY')
    .map((element) => element.textContent)
  expect(headings).toEqual([
    '[1] paper.pdf · 第 1–16 頁 · 全文摘要',
    '[2] paper.pdf · 第 7–9 頁 · 章節摘要：4 Evaluation',
    '[3] paper.pdf · 第 8 頁 · 表格之後的討論',
  ])
  expect(screen.getByText('問題類型：摘要')).toBeInTheDocument()
})

test('the number check lists the figures found on the cited pages and flags the rest', async () => {
  mockApi(
    routesFor(
      answerStream({
        done: {
          unverified_numbers: ['12,345'],
          verified_numbers: [{ number: '83.6%', document_id: PAPER.id, page: 7, snippet: '…LightRAG 83.6%…' }],
          mislabelled_numbers: [
            {
              number: '59.6%',
              answer_labels: ['Overall', 'Mix'],
              source_labels: [['Comprehensiveness', 'Mix', '-High', 'vs NaiveRAG']],
              sentence: 'In Mix, the Overall score is 59.6%.',
            },
          ],
          unresolved_numbers: [
            {
              number: '57.6%',
              answer_labels: ['Overall', 'Mix'],
              source_labels: [['Overall', 'Mix', '-High', 'vs NaiveRAG']],
              sentence: 'In Mix, its Overall score is 57.6%.',
              reason: 'missing',
            },
          ],
          overstated_claims: [
            {
              sentence: 'LightRAG consistently outperforms -High across all datasets and metrics.',
              method: 'LightRAG',
              compared: ['-High'],
              higher: 4,
              lower: 2,
              examples: ['Diversity / Agriculture: LightRAG 60.0% vs -High 62.0% (p. 1)'],
              status: 'contradicted',
              reason: null,
            },
          ],
          doubtful_citations: [
            {
              sentence: 'GraphRAG dismantles its community structure when new documents arrive.',
              cited: [3],
              closer: [5],
              coverage_cited: 0.1,
              coverage_closer: 0.7,
            },
          ],
        },
      }),
    ),
  )
  render(<ChatPanel documents={[PAPER]} />)

  await ask()

  expect(
    await screen.findByText(
      '數字核對：1 個在引用的頁面找到、1 個找不到、1 個標籤不符、1 個未能判定、1 個結論與表格不符、1 個引用可疑',
    ),
  ).toBeInTheDocument()
  expect(screen.getByText(/83\.6% · 第 7 頁/)).toBeInTheDocument()
  expect(screen.getByText('…LightRAG 83.6%…')).toBeInTheDocument()
  expect(screen.getByText('找不到：12,345')).toBeInTheDocument()
  expect(
    screen.getByText('標籤不符：59.6%（答案：Overall、Mix；原文：Comprehensiveness、Mix、-High、vs NaiveRAG）'),
  ).toBeInTheDocument()
  // An unresolved figure is explained, not shown as an error.
  const unresolved = screen.getByText(
    '未能判定：57.6%（答案：Overall、Mix；原文可能是：Overall、Mix、-High、vs NaiveRAG；答案沒寫出全部標籤）',
  )
  expect(unresolved).toHaveClass('text-muted')
  expect(unresolved).not.toHaveClass('text-danger')
  // A universal claim the table contradicts is an error; a doubtful citation is only a doubt.
  const claim = screen.getByText(/結論與表格不符：「LightRAG consistently outperforms -High/)
  expect(claim).toHaveClass('text-danger')
  expect(claim).toHaveTextContent('LightRAG 在 4 格高於比較對象、2 格低於，例如 Diversity / Agriculture')
  const doubt = screen.getByText(/引用可疑：「GraphRAG dismantles its community structure/)
  expect(doubt).toHaveClass('text-muted')
  expect(doubt).toHaveTextContent('引用 [3]，但較接近的來源是 [5]')
})

test('an answer without numbers shows no number check', async () => {
  mockApi(routesFor(answerStream()))
  render(<ChatPanel documents={[PAPER]} />)

  await ask()

  await screen.findByRole('list', { name: '對話內容' })
  expect(screen.queryByText(/數字核對/)).not.toBeInTheDocument()
})

test('a follow-up question that was rewritten shows the standalone question', async () => {
  const rewritten = 'LightRAG 的雙層檢索的缺點是什麼？'
  mockApi(routesFor(answerStream({ route: { type: 'retrieval', standalone_question: rewritten } })))
  render(<ChatPanel documents={[PAPER]} />)

  await ask('那它的缺點呢？')

  expect(await screen.findByText(`改寫後的問題：${rewritten}`)).toBeInTheDocument()
  expect(screen.getByText('問題類型：檢索')).toBeInTheDocument()
})

test('the answer is rendered as formatted text, with citations kept literally', async () => {
  mockApi({
    'GET /api/v1/conversations': { status: 200, body: [] },
    'POST /api/v1/conversations': { status: 201, body: CONVERSATION },
    [ASK]: answerStream({ pieces: ['**Low-level**', ' retrieval [1]\n\n- first\n- second [2][3]'] }),
    [`GET /api/v1/conversations/${CONVERSATION.id}`]: {
      status: 200,
      body: {
        ...stored(),
        messages: [
          stored().messages[0],
          { ...stored().messages[1], content: '**Low-level** retrieval [1]\n\n- first\n- second [2][3]' },
        ],
      },
    },
  })
  render(<ChatPanel documents={[PAPER]} />)

  await ask()

  const conversation = await screen.findByRole('list', { name: '對話內容' })
  const bold = within(conversation).getByText('Low-level')
  expect(bold.tagName).toBe('STRONG')
  expect(within(conversation).queryByText(/\*\*/)).not.toBeInTheDocument()
  expect(within(conversation).getByText('first').tagName).toBe('LI')
  expect(within(conversation).getByText('second [2][3]')).toBeInTheDocument()
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
