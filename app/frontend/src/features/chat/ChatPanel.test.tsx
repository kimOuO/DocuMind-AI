import { fireEvent, render, screen, within } from '@testing-library/react'
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
  build_summary: true,
  error: null,
  page_count: 16,
  chunk_count: 48,
  created_at: '2026-11-05T08:00:00Z',
  updated_at: '2026-11-05T08:00:00Z',
}
const NOTES: DocumentItem = { ...PAPER, id: 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', filename: 'notes.txt' }
const WAITING: DocumentItem = {
  ...PAPER,
  id: 'cccccccc-cccc-cccc-cccc-cccccccccccc',
  filename: 'waiting.md',
  status: 'processing',
}

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
  overrides: {
    done?: object
    scope?: object
    pieces?: string[]
    sources?: object[]
    route?: object
    temperature?: number | null
  } = {},
) {
  const pieces = overrides.pieces ?? ['The ablated versions', ' perform worse [1].']
  return sse([
    [
      'start',
      {
        user_message_id: 'u1',
        assistant_message_id: 'a1',
        scope: overrides.scope ?? { mode: 'all', document_ids: [PAPER.id, NOTES.id] },
        temperature: overrides.temperature ?? null,
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

/** An answer line as rendered: citations are chips showing the bare number, so "[1]" reads "1". */
function answerLine(expected: string) {
  const rendered = expected.replace(/\[(\d+)\]/g, '$1')
  return (_: string, element: Element | null) => element?.tagName === 'P' && element.textContent === rendered
}

function stored(status = 'completed', answered: boolean | null = true, sources: object[] = [SOURCE]) {
  return {
    ...CONVERSATION,
    title: QUESTION.slice(0, 40),
    messages: [
      {
        id: 'u1',
        role: 'user',
        content: QUESTION,
        status: 'completed',
        answered: null,
        sources: [],
        created_at: '2026-11-05T09:00:01Z',
      },
      {
        id: 'a1',
        role: 'assistant',
        content: 'The ablated versions perform worse [1].',
        status,
        answered,
        sources,
        created_at: '2026-11-05T09:00:02Z',
      },
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
  localStorage.clear()
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
  expect(
    within(conversation).getByText(answerLine('The ablated versions perform worse [1].')),
  ).toBeInTheDocument()
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
  expect(await screen.findByRole('button', { name: QUESTION.slice(0, 40) })).toHaveAttribute(
    'aria-current',
    'true',
  )
})

test('summary sources show their section and page range, and added context is labelled', async () => {
  const whole = {
    ...SOURCE,
    kind: 'summary',
    page_start: 1,
    page_end: 16,
    snippet: 'LightRAG combines…',
    score: null,
    origin: 'summary',
  }
  const section = {
    ...whole,
    index: 2,
    page_start: 7,
    page_end: 9,
    section_title: '4 Evaluation',
    snippet: 'LightRAG wins 83.6%…',
  }
  const context = {
    ...SOURCE,
    index: 3,
    origin: 'table_context',
    score: null,
    snippet: 'The -High variant removes…',
  }
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
          verified_numbers: [
            { number: '83.6%', document_id: PAPER.id, page: 7, snippet: '…LightRAG 83.6%…' },
          ],
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
    screen.getByText(
      '標籤不符：59.6%（答案：Overall、Mix；原文：Comprehensiveness、Mix、-High、vs NaiveRAG）',
    ),
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

test('the two-call mode reports which text was kept and the summed token usage', async () => {
  mockApi(
    routesFor(
      sse([
        [
          'start',
          {
            user_message_id: 'u1',
            assistant_message_id: 'a1',
            scope: { mode: 'all', document_ids: [PAPER.id] },
          },
        ],
        ['route', { type: 'retrieval', standalone_question: QUESTION }],
        ['sources', [SOURCE]],
        ['stage', { stage: 'generating' }],
        ['stage', { stage: 'verifying' }],
        ['stage', { stage: 'revising' }],
        ['stage', { stage: 'verifying' }],
        ['stage', { stage: 'finalizing' }],
        ['delta', { text: 'The ablated versions perform worse [1].' }],
        ['usage', { prompt_tokens: 7000, completion_tokens: 900, limit: null, calls: 2 }],
        [
          'done',
          {
            status: 'completed',
            answered: true,
            cited: [1],
            finish_reason: 'stop',
            ...NO_NUMBERS,
            revision: {
              mode: 'conditional',
              triggered: true,
              draft_triggers: [{ kind: 'mislabelled_number', severity: 'hard', feedback: '…' }],
              revision_triggers: [],
              skipped: null,
              chosen: 'revision',
              status: 'verified',
              reason: 'the revision removed hard faults',
            },
          },
        ],
      ]),
    ),
  )
  render(<ChatPanel documents={[PAPER]} />)

  await ask()

  expect(await screen.findByText(answerLine('The ablated versions perform worse [1].'))).toBeInTheDocument()
  expect(
    screen.getByText('兩次呼叫模式：顯示的是修正後的回答，已通過核對。初稿核對發現 1 項，修正稿 0 項。'),
  ).toBeInTheDocument()
  expect(screen.getByText(/這 2 次呼叫合計的 token：輸入 7,000 \+ 回答 900 = 7,900$/)).toBeInTheDocument()
})

test('the navigate mode shows the plan, what was located and the added sources', async () => {
  mockApi(
    routesFor(
      sse([
        [
          'start',
          {
            user_message_id: 'u1',
            assistant_message_id: 'a1',
            scope: { mode: 'all', document_ids: [PAPER.id] },
          },
        ],
        ['route', { type: 'retrieval', standalone_question: QUESTION }],
        ['stage', { stage: 'navigating' }],
        ['sources', [SOURCE, { ...SOURCE, index: 2, page_start: 8, page_end: 8, origin: 'navigation' }]],
        ['delta', { text: 'The ablated versions perform worse [1].' }],
        ['usage', { prompt_tokens: 5000, completion_tokens: 600, limit: null, calls: 2 }],
        [
          'done',
          {
            status: 'completed',
            answered: true,
            cited: [1],
            finish_reason: 'stop',
            ...NO_NUMBERS,
            revision: null,
            navigation: {
              map_entries: 9,
              plan: '- Table 2 (page 8)\n- Table 9',
              items: [
                { text: 'Table 2 (page 8)', located: true, pages: [8] },
                { text: 'Table 9', located: false, pages: [] },
              ],
              located: 1,
              fetched: 2,
              kept: 1,
              excluded_budget: 1,
              skipped: null,
            },
          },
        ],
      ]),
    ),
  )
  render(<ChatPanel documents={[PAPER]} />)

  await ask()

  expect(await screen.findByText(answerLine('The ablated versions perform worse [1].'))).toBeInTheDocument()
  expect(
    screen.getByText('Navigator 計畫：2 項，定位 1 項，補充 1 個片段（1 個因預算未納入）'),
  ).toBeInTheDocument()
  expect(screen.getByText('Table 2 (page 8)（第 8 頁）')).toBeInTheDocument()
  expect(screen.getByText('Table 9（文件中找不到）')).toBeInTheDocument()
  // The stored conversation (reloaded after the stream) decides which sources show; the
  // origin label of plan-fetched sources is a one-line mapping in describeOrigin.
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

test('the answer is rendered as formatted text, with citations as clickable chips', async () => {
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
  expect(
    within(conversation).getByText((_, el) => el?.tagName === 'LI' && el.textContent === 'second 23'),
  ).toBeInTheDocument()
  expect(within(conversation).getAllByRole('button', { name: /^來源 \d$/ })).toHaveLength(3)
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
  expect(screen.getByText(answerLine('The ablated versions perform worse [1].'))).toBeInTheDocument()
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
      [
        'start',
        {
          user_message_id: 'u1',
          assistant_message_id: 'a1',
          scope: { mode: 'all', document_ids: [PAPER.id] },
        },
      ],
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

  await userEvent.click(await screen.findByRole('button', { name: 'ablation' }))

  expect(await screen.findByText(QUESTION)).toBeInTheDocument()
  expect(screen.getByText('回答未完成')).toBeInTheDocument()

  await userEvent.click(screen.getByRole('button', { name: '刪除對話' }))
  const dialog = screen.getByRole('dialog', { name: '刪除對話' })
  expect(dialog).toHaveTextContent('ablation')
  await userEvent.click(within(dialog).getByRole('button', { name: '確定刪除' }))

  expect(await screen.findByText('還沒有對話。')).toBeInTheDocument()
  expect(screen.queryByRole('button', { name: 'ablation' })).not.toBeInTheDocument()
  expect(screen.queryByText(QUESTION)).not.toBeInTheDocument()
  expect(calls.map((c) => c.key)).toContain(`DELETE /api/v1/conversations/${CONVERSATION.id}`)
})

test('a source card opens the source in the right-hand panel, which the user can close and reopen', async () => {
  mockApi(routesFor(answerStream(), stored()))
  render(<ChatPanel documents={[PAPER]} />)

  await ask()
  expect(screen.queryByRole('region', { name: '來源檢視' })).not.toBeInTheDocument()
  await userEvent.click(await screen.findByRole('button', { name: '在右側檢視來源 1' }))

  const viewer = screen.getByRole('region', { name: '來源檢視' })
  expect(within(viewer).getByText(/\[1\] paper\.pdf/)).toBeInTheDocument()
  expect(within(viewer).getByRole('link', { name: '開新分頁' })).toHaveAttribute(
    'href',
    `/api/v1/documents/${SOURCE.document_id}/file?p=8#page=8`,
  )
  // The panel is the user's to open and close; closed, it keeps nothing on screen.
  await userEvent.click(screen.getByRole('button', { name: /收起來源檢視/ }))
  expect(screen.queryByRole('region', { name: '來源檢視' })).not.toBeInTheDocument()
  await userEvent.click(screen.getByRole('button', { name: /來源檢視/ }))
  expect(
    within(screen.getByRole('region', { name: '來源檢視' })).getByText(/\[1\] paper\.pdf/),
  ).toBeInTheDocument()
})

test('clicking a citation opens the source beside the answer with the cited page', async () => {
  mockApi(routesFor(answerStream(), stored()))
  render(<ChatPanel documents={[PAPER]} />)

  await ask()
  const conversation = await screen.findByRole('list', { name: '對話內容' })
  await userEvent.click(within(conversation).getByRole('button', { name: '來源 1' }))

  const viewer = screen.getByRole('region', { name: '來源檢視' })
  expect(within(viewer).getByText(/\[1\] paper\.pdf/)).toBeInTheDocument()
  expect(within(viewer).getByText(/第 8 頁/)).toBeInTheDocument()
  expect(
    within(viewer).getByText(/引用這段的句子：「The ablated versions perform worse」/),
  ).toBeInTheDocument()
  expect(within(viewer).getByTitle('paper.pdf 第 8 頁')).toHaveAttribute(
    'src',
    `/api/v1/documents/${SOURCE.document_id}/file?p=8#page=8`,
  )
  await userEvent.click(within(viewer).getByRole('button', { name: '關閉來源檢視' }))
  expect(screen.queryByRole('region', { name: '來源檢視' })).not.toBeInTheDocument()
})

test("the program's notes after an answer are folded away from the answer text", async () => {
  const content =
    'LightRAG wins [1].\n\nNumbers that could not be checked against the cited pages of the original text: 99%.'
  mockApi(
    routesFor(answerStream({ pieces: [content] }), {
      ...stored(),
      messages: [stored().messages[0], { ...stored().messages[1], content }],
    }),
  )
  render(<ChatPanel documents={[PAPER]} />)

  await ask()

  const conversation = await screen.findByRole('list', { name: '對話內容' })
  expect(within(conversation).getByText(answerLine('LightRAG wins [1].'))).toBeInTheDocument()
  expect(within(conversation).getByText('核對結果（1 則註記）')).toBeInTheDocument()
  expect(within(conversation).getByText(/Numbers that could not be checked/)).toBeInTheDocument()
})

test('Enter sends the question and Shift+Enter only adds a line', async () => {
  const calls = mockApi(routesFor(answerStream(), stored()))
  render(<ChatPanel documents={[PAPER]} />)
  const box = await screen.findByLabelText('問題')

  await userEvent.type(box, 'first line{Shift>}{Enter}{/Shift}second')
  expect(calls.some((c) => c.key === ASK)).toBe(false)
  expect(box).toHaveValue('first line\nsecond')

  await userEvent.type(box, '{Enter}')

  expect(calls.find((c) => c.key === ASK)!.body).toEqual({ question: 'first line\nsecond', document_ids: [] })
})

test('opening another citation moves the embedded page, and Esc closes the panel', async () => {
  const second = { ...SOURCE, index: 2, page_start: 3, page_end: 3, snippet: 'Dual-level retrieval…' }
  const content = 'One [1]. Two [2].'
  const detail = {
    ...stored(),
    messages: [stored().messages[0], { ...stored().messages[1], content, sources: [SOURCE, second] }],
  }
  mockApi(routesFor(answerStream({ pieces: [content], sources: [SOURCE, second] }), detail))
  render(<ChatPanel documents={[PAPER]} />)

  await ask()
  const conversation = await screen.findByRole('list', { name: '對話內容' })
  await userEvent.click(within(conversation).getByRole('button', { name: '來源 1' }))
  expect(screen.getByTitle('paper.pdf 第 8 頁')).toHaveAttribute(
    'src',
    expect.stringContaining('?p=8#page=8'),
  )

  await userEvent.click(within(conversation).getByRole('button', { name: '來源 2' }))
  expect(screen.queryByTitle('paper.pdf 第 8 頁')).not.toBeInTheDocument()
  expect(screen.getByTitle('paper.pdf 第 3 頁')).toHaveAttribute(
    'src',
    expect.stringContaining('?p=3#page=3'),
  )

  await userEvent.keyboard('{Escape}')
  expect(screen.queryByRole('region', { name: '來源檢視' })).not.toBeInTheDocument()
})

test('the temperature slider sets the sampling temperature of the next answer and can go back to the default', async () => {
  // After each answer the stored conversation is reloaded; the second one carries its temperature.
  const warm = {
    ...stored(),
    messages: stored().messages.map((m, i) => (i === 1 ? { ...m, temperature: 0.4 } : m)),
  }
  const calls = mockApi({
    ...routesFor(answerStream()),
    [ASK]: [answerStream(), answerStream({ temperature: 0.4 })],
    [`GET /api/v1/conversations/${CONVERSATION.id}`]: [
      { status: 200, body: stored() },
      { status: 200, body: warm },
    ],
    'GET /api/v1/health': {
      status: 200,
      body: {
        status: 'ok',
        database: { ok: true, detail: 'pgvector' },
        ollama: { ok: true, detail: 'models available' },
        llm_model: 'qwen3:32b',
        embed_model: 'bge-m3',
        llm_context_limit: 10000,
        answer_temperature: 0,
      },
    },
  })
  render(<ChatPanel documents={[PAPER]} />)

  // Untouched, the slider shows the server's default and the request carries no temperature.
  expect(await screen.findByText('0.0（預設）')).toBeInTheDocument()
  await ask()
  expect(calls.find((c) => c.key === ASK)!.body).toEqual({ question: QUESTION, document_ids: [] })

  // Moved to 0.4: the next request says so, the answer is labelled, the choice is remembered.
  fireEvent.change(screen.getByRole('slider', { name: '回答溫度' }), { target: { value: '0.4' } })
  expect(screen.getByText('0.4')).toBeInTheDocument()
  await ask('Another question')
  expect(calls.filter((c) => c.key === ASK)[1].body).toEqual({
    question: 'Another question',
    document_ids: [],
    temperature: 0.4,
  })
  expect(await screen.findByText('溫度 0.4')).toBeInTheDocument()
  expect(localStorage.getItem('documind.temperature')).toBe('0.4')

  // Back to the default: the figure returns and the stored choice is gone.
  await userEvent.click(screen.getByRole('button', { name: '回預設' }))
  expect(screen.getByText('0.0（預設）')).toBeInTheDocument()
  expect(localStorage.getItem('documind.temperature')).toBeNull()
})
