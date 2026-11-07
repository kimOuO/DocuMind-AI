import { useEffect, useState, type FormEvent } from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { ConfirmDialog } from '../../components/ConfirmDialog'
import {
  ApiError,
  askQuestion,
  createConversation,
  deleteConversation,
  getConversation,
  listConversations,
  type ChatMessage,
  type Conversation,
  type DocumentItem,
  type MessageStatus,
  type NumberCheck,
  type SearchScope,
  type Source,
  type Navigation,
  type Revision,
  type Stage,
  type Usage,
} from '../../lib/api'

const MESSAGES: Record<string, string> = {
  QUESTION_TOO_LONG: '問題太長，請縮短後再送出。',
  EMPTY_QUESTION: '請輸入問題。',
  NO_READY_DOCUMENT: '還沒有可以提問的文件。請先上傳文件並等待處理完成。',
  DOCUMENT_NOT_READY: '選取的文件還沒有處理完成。',
  DOCUMENT_NOT_FOUND: '找不到選取的文件，可能已經被刪除。',
  CONVERSATION_NOT_FOUND: '找不到這個對話，可能已經被刪除。',
  ORIGIN_NOT_ALLOWED: '這個網址不在允許的來源清單內，請從設定的網址開啟。',
  INPUT_EXCEEDS_CONTEXT: '這次提問的內容超過模型的長度上限，沒有產生回答。',
  LLM_UNAVAILABLE: '語言模型目前無法使用，請稍後再試。',
  EMBEDDING_UNAVAILABLE: '嵌入模型目前無法使用，請稍後再試。',
  EMBEDDING_INPUT_FAILED: '嵌入模型算不出這段文字的向量（服務正常），請換個說法再問。',
}

/** An answer that is not `completed` must never look like a finished one. */
const UNFINISHED_LABEL: Partial<Record<MessageStatus, string>> = {
  pending: '回答產生中…',
  streaming: '回答產生中…',
  interrupted: '回答未完成',
  failed: '回答失敗',
}

function describe(error: unknown): string {
  if (error instanceof ApiError) return MESSAGES[error.code] ?? error.message
  return '無法連線到伺服器，請稍後再試。'
}

const ROUTE_LABEL: Record<string, string> = { retrieval: '檢索', summary: '摘要' }
const STAGE_LABEL: Record<Stage, string> = {
  navigating: 'Navigator 規劃要看的章節與表格中',
  generating: '產生初稿中（兩次呼叫模式，初稿不會直接顯示）',
  verifying: '核對中',
  correcting: '依表格修正數字與比較用語',
  revising: '依核對結果修正中',
  finalizing: '整理最終回答',
}
const REVISION_LABEL = {
  verified: '已通過核對',
  unverified: '核對仍有疑點',
}

const COVERAGE_LABEL: Record<string, string> = {
  covered: '原始來源已涵蓋',
  partial: '原始來源部分涵蓋',
  missing: '原始來源未涵蓋',
  unknown: '涵蓋與否無法判定',
  not_located: '',
}

/** Generic prompts for a first question — not tied to any particular document. */
const QUICK_QUESTIONS = ['summary this document.', '這份文件的主要結論是什麼？', '文件裡有哪些表格與數據？']

const STAGE_ORDER: Stage[] = ['navigating', 'generating', 'verifying', 'correcting', 'revising', 'finalizing']
const STAGE_SHORT: Record<Stage, string> = {
  navigating: '規劃閱讀',
  generating: '產生初稿',
  verifying: '核對',
  correcting: '修正',
  revising: '修正',
  finalizing: '整理',
}

/** The pipeline's steps so far; the current one carries its full description. */
function StageSteps({ stage }: { stage: Stage | null }) {
  // The single-call default reports no stages: only the waiting line shows.
  if (stage === null) return <p className="mt-2 text-muted">檢索並產生回答中…</p>
  const reached = STAGE_ORDER.indexOf(stage)
  const shown = STAGE_ORDER.filter((_, index) => index <= reached)
  return (
    <div className="mt-2">
      <ol className="flex flex-wrap items-center gap-1 text-xs" aria-label="處理步驟">
        {shown.map((step, index) => (
          <li
            key={step}
            className={`rounded-full border px-2 py-0.5 ${
              index === shown.length - 1 ? 'border-accent text-accent' : 'border-border text-muted'
            }`}
            aria-current={index === shown.length - 1 ? 'step' : undefined}
          >
            {STAGE_SHORT[step]}
          </li>
        ))}
      </ol>
      <p className="mt-1 text-muted">{STAGE_LABEL[stage]}</p>
    </div>
  )
}

/** Tokens of this answer's calls against the 10K limit (AC-21). */
function UsageMeter({ usage }: { usage: Usage }) {
  const prompt = usage.prompt_tokens ?? 0
  const completion = usage.completion_tokens ?? 0
  const total = prompt + completion
  const share = usage.limit ? Math.min(100, Math.round((total / usage.limit) * 100)) : null
  return (
    <div className="mt-2">
      <p className="text-muted">
        {usage.calls !== undefined && usage.calls > 1 ? `這 ${usage.calls} 次呼叫合計的 token` : '這次呼叫的 token'}
        ：輸入 {prompt.toLocaleString()} + 回答 {completion.toLocaleString()} ={' '}
        {total.toLocaleString()}
        {usage.limit !== null && ` / ${usage.limit.toLocaleString()}`}
      </p>
      {share !== null && (
        <div
          role="progressbar"
          aria-label="token 用量"
          aria-valuemin={0}
          aria-valuemax={100}
          aria-valuenow={share}
          className="mt-1 h-1.5 w-full overflow-hidden rounded-full bg-border"
        >
          <div className="h-full rounded-full bg-accent" style={{ width: `${share}%` }} />
        </div>
      )}
    </div>
  )
}

/** The Navigator's reading plan (D71 navigate mode): candidates checked against the document map. */
function NavigationNote({ navigation }: { navigation: Navigation }) {
  if (navigation.skipped) {
    return <p className="text-sm text-muted">Navigator 未執行（{navigation.skipped}），回答依原始檢索。</p>
  }
  return (
    <details className="mt-2 text-sm">
      <summary className="cursor-pointer text-muted">
        Navigator 計畫：{navigation.items.length} 項，定位 {navigation.located} 項，補充 {navigation.kept} 個片段
        {navigation.excluded_budget > 0 && `（${navigation.excluded_budget} 個因預算未納入）`}
        {navigation.unmet_required && navigation.unmet_required.length > 0 && `；必要證據未納入：${navigation.unmet_required.join('、')}`}
      </summary>
      <ul className="mt-1 list-none p-0">
        {navigation.items.map((item) => (
          <li key={item.text} className={item.located ? '' : 'text-muted'}>
            {item.location ? `${item.location}：${item.need ?? ''}` : item.text}
            {item.located ? `（第 ${item.pages[0]}${item.pages.length > 1 ? `–${item.pages[item.pages.length - 1]}` : ''} 頁）` : '（文件中找不到）'}
            {item.coverage && item.coverage !== 'not_located' && `，${COVERAGE_LABEL[item.coverage]}`}
            {item.selected && item.selected.length > 0 && `，補充 ${item.selected.length} 個片段`}
          </li>
        ))}
      </ul>
    </details>
  )
}

/** What the experimental two-call mode did (D69), for the reader: which text was kept and why. */
function RevisionNote({ revision }: { revision: Revision }) {
  if (revision.chosen === undefined || revision.status === undefined) return null
  const kept = revision.chosen === 'revision' ? '顯示的是修正後的回答' : '顯示的是初稿'
  const skipped = revision.skipped ? `（未修正：${revision.skipped}）` : ''
  return (
    <p className="text-sm text-muted">
      兩次呼叫模式：{kept}，{REVISION_LABEL[revision.status]}
      {skipped}。初稿核對發現 {revision.draft_triggers?.length ?? 0} 項，修正稿 {revision.revision_triggers?.length ?? 0} 項。
    </p>
  )
}

function pageRange(first: number, last: number): string {
  return first === last ? `第 ${first} 頁` : `第 ${first}–${last} 頁`
}

/** Where a source came from: a search hit with its similarity, a table's discussion, or a summary. */
function describeOrigin(source: Source): string {
  if (source.kind === 'summary') {
    return source.section_title === null ? '全文摘要' : `章節摘要：${source.section_title}`
  }
  if (source.origin === 'table_context') return '表格之後的討論'
  if (source.origin === 'navigation') return '依閱讀計畫補充'
  return source.score === null ? '' : `相似度 ${source.score.toFixed(2)}`
}

function SourceList({ sources }: { sources: Source[] }) {
  if (sources.length === 0) return null
  return (
    <ul className="mt-2 list-none p-0 text-sm">
      {sources.map((source) => {
        const origin = describeOrigin(source)
        return (
          <li key={source.index} className="border-t border-border py-1">
            <details>
              <summary className="cursor-pointer">
                [{source.index}] {source.filename} · {pageRange(source.page_start, source.page_end)}
                {origin && <span className="text-muted"> · {origin}</span>}
              </summary>
              <p className="mt-1 whitespace-pre-wrap break-words text-muted">{source.snippet}</p>
            </details>
          </li>
        )
      })}
    </ul>
  )
}

/** How the answer's figures compare with the original text of the cited pages (AC-26). */
function NumberCheckView({ check }: { check: NumberCheck }) {
  const {
    verified_numbers: verified,
    unverified_numbers: unverified,
    mislabelled_numbers: mislabelled,
    unresolved_numbers: unresolved,
    overstated_claims: overstated,
    doubtful_citations: doubtful,
  } = check
  const contradicted = overstated.filter((claim) => claim.status === 'contradicted')
  const total =
    verified.length + unverified.length + mislabelled.length + unresolved.length + overstated.length + doubtful.length
  if (total === 0) return null
  const parts = [`${verified.length} 個在引用的頁面找到`]
  if (unverified.length > 0) parts.push(`${unverified.length} 個找不到`)
  if (mislabelled.length > 0) parts.push(`${mislabelled.length} 個標籤不符`)
  if (unresolved.length > 0) parts.push(`${unresolved.length} 個未能判定`)
  if (contradicted.length > 0) parts.push(`${contradicted.length} 個結論與表格不符`)
  if (doubtful.length > 0) parts.push(`${doubtful.length} 個引用可疑`)
  return (
    <details className="mt-2 text-sm">
      <summary className="cursor-pointer text-muted">數字核對：{parts.join('、')}</summary>
      {verified.length > 0 && (
        <ul className="mt-1 list-none p-0">
          {verified.map((item) => (
            <li key={`${item.number}-${item.page}`} className="py-1">
              <span>
                {item.number} · 第 {item.page} 頁
              </span>
              <p className="whitespace-pre-wrap break-words text-muted">{item.snippet}</p>
            </li>
          ))}
        </ul>
      )}
      {unverified.length > 0 && <p className="text-danger">找不到：{unverified.join('、')}</p>}
      {mislabelled.map((item) => (
        <p key={item.number} className="text-danger">
          標籤不符：{item.number}（答案：{item.answer_labels.join('、')}；原文：
          {item.source_labels.map((labels) => labels.join('、')).join(' / ')}）
        </p>
      ))}
      {unresolved.map((item) => (
        // Not an error: the answer did not say enough for the check to decide (D67).
        <p key={`${item.number}-${item.answer_labels.join()}`} className="text-muted">
          未能判定：{item.number}（答案：{item.answer_labels.join('、')}；原文可能是：
          {item.source_labels.map((labels) => labels.join('、')).join(' / ')}；
          {item.reason === 'missing' ? '答案沒寫出全部標籤' : '答案裡有兩個候選標籤'}）
        </p>
      ))}
      {overstated.map((claim) =>
        claim.status === 'contradicted' ? (
          <p key={claim.sentence} className="text-danger">
            結論與表格不符：「{claim.sentence}」{claim.method} 在 {claim.higher} 格高於比較對象、{claim.lower}{' '}
            格低於，例如 {claim.examples.slice(0, 3).join('；')}
          </p>
        ) : (
          <p key={claim.sentence} className="text-muted">
            結論未能核對：「{claim.sentence}」引用的表格裡沒有 {claim.method} 與
            {claim.compared.length > 0 ? claim.compared.join('、') : '其他方法'}的共同格子
          </p>
        ),
      )}
      {doubtful.map((item) => (
        // A doubt, not an error: the cited source hardly states the sentence, another source does.
        <p key={item.sentence} className="text-muted">
          引用可疑：「{item.sentence}」引用 [{item.cited.join('][')}]，但較接近的來源是 [{item.closer.join('][')}]
        </p>
      ))}
    </details>
  )
}

/** The model's answer as formatted text. Raw HTML in it is never rendered. */
function AnswerText({ content }: { content: string }) {
  return (
    <div className="answer break-words">
      <ReactMarkdown remarkPlugins={[remarkGfm]} skipHtml>
        {content}
      </ReactMarkdown>
    </div>
  )
}

function MessageView({ message }: { message: ChatMessage }) {
  if (message.role === 'user') {
    return (
      <li className="border-t border-border py-2">
        <p className="text-sm text-muted">你</p>
        <p className="whitespace-pre-wrap break-words">{message.content}</p>
      </li>
    )
  }
  const unfinished = UNFINISHED_LABEL[message.status]
  return (
    <li className="border-t border-border py-2">
      <p className="text-sm text-muted">
        回答
        {unfinished && (
          <span
            className={`ml-2 font-medium ${message.status === 'failed' ? 'text-danger' : 'text-accent'}`}
          >
            {unfinished}
          </span>
        )}
        {message.status === 'completed' && message.answered === false && (
          <span className="ml-2 font-medium text-accent">文件中找不到答案</span>
        )}
      </p>
      <AnswerText content={message.content} />
      <SourceList sources={message.sources} />
    </li>
  )
}

/** Ask questions about the user's ready documents, in a conversation. */
export function ChatPanel({ documents }: { documents: DocumentItem[] }) {
  const ready = documents.filter((document) => document.status === 'ready')
  const [conversations, setConversations] = useState<Conversation[]>([])
  const [activeId, setActiveId] = useState<string | null>(null)
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [selected, setSelected] = useState<string[]>([])
  const [question, setQuestion] = useState('')
  const [asking, setAsking] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [scope, setScope] = useState<SearchScope | null>(null)
  const [route, setRoute] = useState<{ type: string; standalone_question: string; asked: string } | null>(null)
  const [usage, setUsage] = useState<Usage | null>(null)
  const [stage, setStage] = useState<Stage | null>(null)
  const [revision, setRevision] = useState<Revision | null>(null)
  const [navigation, setNavigation] = useState<Navigation | null>(null)
  const [check, setCheck] = useState<NumberCheck | null>(null)
  const [pendingDelete, setPendingDelete] = useState<Conversation | null>(null)

  useEffect(() => {
    let active = true
    listConversations()
      .then((items) => {
        if (active) setConversations(items)
      })
      .catch((caught: unknown) => {
        if (active) setError(describe(caught))
      })
    return () => {
      active = false
    }
  }, [])

  // A document that is no longer ready (deleted, for example) cannot stay selected.
  const readyIds = ready.map((document) => document.id)
  const scopeIds = selected.filter((id) => readyIds.includes(id))

  async function open(id: string | null) {
    setActiveId(id)
    setScope(null)
    setRoute(null)
    setUsage(null)
    setStage(null)
    setRevision(null)
    setNavigation(null)
    setCheck(null)
    setError(null)
    if (id === null) {
      setMessages([])
      return
    }
    try {
      setMessages((await getConversation(id)).messages)
    } catch (caught) {
      setError(describe(caught))
      setMessages([])
    }
  }

  async function reload(id: string) {
    try {
      const [detail, list] = await Promise.all([getConversation(id), listConversations()])
      setMessages(detail.messages)
      setConversations(list)
    } catch (caught) {
      setError(describe(caught))
    }
  }

  async function handleAsk(event: FormEvent) {
    event.preventDefault()
    const text = question.trim()
    if (!text || asking) return
    setAsking(true)
    setError(null)
    setScope(null)
    setRoute(null)
    setUsage(null)
    setStage(null)
    setRevision(null)
    setNavigation(null)
    setCheck(null)
    let conversationId = activeId
    try {
      if (conversationId === null) {
        const created = await createConversation()
        conversationId = created.id
        setActiveId(created.id)
        setConversations((current) => [created, ...current])
      }
      const updateAnswer = (change: (answer: ChatMessage) => ChatMessage) =>
        setMessages((current) =>
          current.map((message, index) => (index === current.length - 1 ? change(message) : message)),
        )
      let started = false
      await askQuestion(conversationId, text, scopeIds, (askEvent) => {
        switch (askEvent.name) {
          case 'start': {
            started = true
            const now = new Date().toISOString()
            setQuestion('')
            setScope(askEvent.data.scope)
            setMessages((current) => [
              ...current,
              {
                id: askEvent.data.user_message_id,
                role: 'user',
                content: text,
                status: 'completed',
                answered: null,
                sources: [],
                created_at: now,
              },
              {
                id: askEvent.data.assistant_message_id,
                role: 'assistant',
                content: '',
                status: 'streaming',
                answered: null,
                sources: [],
                created_at: now,
              },
            ])
            break
          }
          case 'route':
            setRoute({ ...askEvent.data, asked: text })
            break
          case 'sources':
            updateAnswer((answer) => ({ ...answer, sources: askEvent.data }))
            break
          case 'stage':
            setStage(askEvent.data.stage)
            break
          case 'delta':
            updateAnswer((answer) => ({ ...answer, content: answer.content + askEvent.data.text }))
            break
          case 'usage':
            setUsage(askEvent.data)
            break
          case 'done':
            updateAnswer((answer) => ({
              ...answer,
              status: askEvent.data.status,
              answered: askEvent.data.answered,
            }))
            setCheck(askEvent.data)
            setRevision(askEvent.data.revision ?? null)
            setNavigation(askEvent.data.navigation ?? null)
            setStage(null)
            break
          case 'error':
            updateAnswer((answer) => ({ ...answer, status: 'failed' }))
            setError(MESSAGES[askEvent.data.code] ?? askEvent.data.detail)
            break
        }
      })
      // The stored conversation is the authority: reload it, and its title.
      if (started) await reload(conversationId)
    } catch (caught) {
      setError(describe(caught))
      // The stream broke before it ended: show what the server kept.
      if (conversationId !== null && !(caught instanceof ApiError)) await reload(conversationId)
    } finally {
      setAsking(false)
    }
  }

  async function handleDelete(conversation: Conversation) {
    setPendingDelete(null)
    try {
      await deleteConversation(conversation.id)
      setConversations((current) => current.filter((item) => item.id !== conversation.id))
      if (activeId === conversation.id) await open(null)
    } catch (caught) {
      setError(describe(caught))
    }
  }

  const active = conversations.find((conversation) => conversation.id === activeId) ?? null
  const scopeText =
    scope === null
      ? null
      : scope.mode === 'all'
        ? `所有可用文件（${scope.document_ids.length} 份）`
        : scope.document_ids
            .map((id) => documents.find((document) => document.id === id)?.filename ?? id)
            .join('、')

  const inspectorEmpty =
    scope === null && route === null && stage === null && usage === null && check === null
  const inspector = (
    <aside
      aria-label="本次回答的檢索與用量"
      className="rounded-lg border border-border bg-bg p-3 text-sm lg:sticky lg:top-4"
    >
      <h3 className="font-semibold">本次回答</h3>
      {inspectorEmpty && (
        <p className="mt-2 text-muted">送出問題後，這裡會顯示搜尋範圍、處理步驟、token 用量與數字核對。</p>
      )}
      {scopeText !== null && <p className="mt-2 text-muted">這次搜尋的範圍：{scopeText}</p>}
      {route !== null && (
        <p className="text-muted">問題類型：{ROUTE_LABEL[route.type] ?? route.type}</p>
      )}
      {route !== null && route.standalone_question !== route.asked && (
        <p className="text-muted">改寫後的問題：{route.standalone_question}</p>
      )}
      {(stage !== null || asking) && <StageSteps stage={stage} />}
      {navigation !== null && <NavigationNote navigation={navigation} />}
      {revision !== null && <RevisionNote revision={revision} />}
      {usage && usage.prompt_tokens !== null && usage.completion_tokens !== null && (
        <UsageMeter usage={usage} />
      )}
      {check !== null && <NumberCheckView check={check} />}
    </aside>
  )

  return (
    <section className="mt-4 rounded-lg border border-border bg-surface p-4">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <h2 className="font-semibold">提問</h2>
        <div className="flex items-center gap-2">
          <label className="text-sm">
            <span className="sr-only">對話</span>
            <select
              className="rounded-md border border-border bg-surface px-2 py-1 text-sm"
              value={activeId ?? ''}
              disabled={asking}
              onChange={(event) => open(event.target.value || null)}
            >
              <option value="">新對話</option>
              {conversations.map((conversation) => (
                <option key={conversation.id} value={conversation.id}>
                  {conversation.title || '（未命名的對話）'}
                </option>
              ))}
            </select>
          </label>
          {active && (
            <button
              type="button"
              className="rounded-md border border-border px-2 py-1 text-sm text-danger"
              disabled={asking}
              onClick={() => setPendingDelete(active)}
            >
              刪除對話
            </button>
          )}
        </div>
      </div>

      {ready.length === 0 ? (
        <p className="mt-2 text-muted">還沒有可以提問的文件。上傳文件並等待處理完成後就能提問。</p>
      ) : (
        <fieldset className="mt-2 text-sm">
          <legend className="text-muted">
            搜尋範圍：{scopeIds.length === 0 ? '所有可用文件' : `已選 ${scopeIds.length} 份`}
          </legend>
          <div className="mt-1 flex flex-wrap gap-x-4 gap-y-1">
            {ready.map((document) => (
              <label key={document.id} className="flex items-center gap-1">
                <input
                  type="checkbox"
                  checked={scopeIds.includes(document.id)}
                  disabled={asking}
                  onChange={(event) =>
                    setSelected(
                      event.target.checked
                        ? [...scopeIds, document.id]
                        : scopeIds.filter((id) => id !== document.id),
                    )
                  }
                />
                {document.filename}
              </label>
            ))}
          </div>
        </fieldset>
      )}

      <div className="mt-3 grid gap-4 lg:grid-cols-[minmax(0,1fr)_minmax(280px,340px)] lg:items-start">
        <div className="min-w-0">
          {messages.length > 0 ? (
            <ul className="list-none p-0" aria-label="對話內容">
              {messages.map((message) => (
                <MessageView key={message.id} message={message} />
              ))}
            </ul>
          ) : (
            ready.length > 0 && (
              <p className="text-sm text-muted">
                還沒有對話。輸入問題，或用下面的快捷鈕。回答會附來源，文件裡沒有的內容會明說找不到。
              </p>
            )
          )}
          {error && (
            <p role="alert" className="mt-2 text-sm text-danger">
              {error}
            </p>
          )}

          <form className="mt-3 flex gap-2" onSubmit={handleAsk}>
            <label className="flex-1">
              <span className="sr-only">問題</span>
              <textarea
                className="w-full rounded-md border border-border bg-surface px-2 py-1"
                rows={2}
                placeholder="針對文件提問，例如：summary this document."
                value={question}
                disabled={asking || ready.length === 0}
                onChange={(event) => setQuestion(event.target.value)}
              />
            </label>
            <button
              type="submit"
              className="self-end rounded-md bg-accent px-3 py-1 text-sm font-medium text-surface disabled:opacity-50"
              disabled={asking || ready.length === 0 || question.trim() === ''}
            >
              {asking ? '回答中…' : '送出'}
            </button>
          </form>
          {ready.length > 0 && (
            <div className="mt-2 flex flex-wrap gap-2" aria-label="快捷問題">
              {QUICK_QUESTIONS.map((text) => (
                <button
                  key={text}
                  type="button"
                  className="rounded-full border border-border px-3 py-0.5 text-xs text-muted hover:text-text"
                  disabled={asking}
                  onClick={() => setQuestion(text)}
                >
                  {text}
                </button>
              ))}
            </div>
          )}
        </div>
        {inspector}
      </div>

      {pendingDelete && (
        <ConfirmDialog
          title="刪除對話"
          message={`確定要刪除「${pendingDelete.title || '未命名的對話'}」嗎？對話中的問題與回答會一併刪除，無法復原。`}
          confirmLabel="確定刪除"
          danger
          onConfirm={() => handleDelete(pendingDelete)}
          onCancel={() => setPendingDelete(null)}
        />
      )}
    </section>
  )
}
