import { useEffect, useState, type FormEvent, type ReactNode } from 'react'
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

const ROUTE_LABEL: Record<string, string> = {
  retrieval: '檢索',
  summary: '摘要',
}
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
        {usage.calls !== undefined && usage.calls > 1
          ? `這 ${usage.calls} 次呼叫合計的 token`
          : '這次呼叫的 token'}
        ：輸入 {prompt.toLocaleString()} + 回答 {completion.toLocaleString()} = {total.toLocaleString()}
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
        Navigator 計畫：{navigation.items.length} 項，定位 {navigation.located} 項，補充 {navigation.kept}{' '}
        個片段
        {navigation.excluded_budget > 0 && `（${navigation.excluded_budget} 個因預算未納入）`}
        {navigation.unmet_required &&
          navigation.unmet_required.length > 0 &&
          `；必要證據未納入：${navigation.unmet_required.join('、')}`}
      </summary>
      <ul className="mt-1 list-none p-0">
        {navigation.items.map((item) => (
          <li key={item.text} className={item.located ? '' : 'text-muted'}>
            {item.location ? `${item.location}：${item.need ?? ''}` : item.text}
            {item.located
              ? `（第 ${item.pages[0]}${item.pages.length > 1 ? `–${item.pages[item.pages.length - 1]}` : ''} 頁）`
              : '（文件中找不到）'}
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
      {skipped}。初稿核對發現 {revision.draft_triggers?.length ?? 0} 項，修正稿{' '}
      {revision.revision_triggers?.length ?? 0} 項。
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

function SourceList({ sources, onView }: { sources: Source[]; onView: (source: Source) => void }) {
  if (sources.length === 0) return null
  return (
    <div className="mt-3">
      <p className="text-xs font-semibold text-muted">來源</p>
      <ul className="mt-1 list-none space-y-1 p-0 text-sm">
        {sources.map((source) => {
          const origin = describeOrigin(source)
          return (
            <li key={source.index} className="rounded-lg border border-border bg-surface-2 px-3 py-1.5">
              <details>
                <summary className="cursor-pointer font-medium text-accent">
                  [{source.index}] {source.filename} · {pageRange(source.page_start, source.page_end)}
                  {origin && <span className="text-muted"> · {origin}</span>}
                </summary>
                <p className="mt-1 whitespace-pre-wrap break-words text-muted">{source.snippet}</p>
                <button
                  type="button"
                  className="mt-1 text-xs text-accent underline"
                  onClick={() => onView(source)}
                  aria-label={`在右側檢視來源 ${source.index}`}
                >
                  在右側檢視原文第 {source.page_start} 頁
                </button>
              </details>
            </li>
          )
        })}
      </ul>
    </div>
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
    verified.length +
    unverified.length +
    mislabelled.length +
    unresolved.length +
    overstated.length +
    doubtful.length
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
          未能判定：{item.number}（答案：{item.answer_labels.join('、')}
          ；原文可能是：
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
            {claim.compared.length > 0 ? claim.compared.join('、') : '其他方法'}
            的共同格子
          </p>
        ),
      )}
      {doubtful.map((item) => (
        // A doubt, not an error: the cited source hardly states the sentence, another source does.
        <p key={item.sentence} className="text-muted">
          引用可疑：「{item.sentence}」引用 [{item.cited.join('][')}
          ]，但較接近的來源是 [{item.closer.join('][')}]
        </p>
      ))}
    </details>
  )
}

/** The model's answer as formatted text. Raw HTML in it is never rendered. */
/** The notes the backend appends after an answer (figure, label and claim checks). */
const NOTE_PREFIXES = [
  'Numbers that could not be checked',
  'Figures whose labels differ',
  'A claim the source table does not bear out',
  'The summary of "',
  '以下數字未能',
  '以下數字的標籤',
  '以下結論與原文表格不符',
]

/** The answer proper and the program's notes, which are shown apart from it (D89). */
function splitNotes(content: string): { answer: string; notes: string[] } {
  const paragraphs = content.split(/\n\n+/)
  const notes = paragraphs.filter((p) => NOTE_PREFIXES.some((prefix) => p.trim().startsWith(prefix)))
  const answer = paragraphs.filter((p) => !notes.includes(p)).join('\n\n')
  return { answer, notes: notes.map((n) => n.trim()) }
}

const CITATION = /\[(\d{1,3}(?:\s*,\s*\d{1,3})*)\]/g

/** "[1][2,3]" becomes links the renderer turns into buttons; the sentence around a citation
 * is what the viewer highlights in the source. */
function linkCitations(markdown: string): string {
  return markdown.replace(CITATION, (_, list: string) =>
    list
      .split(',')
      .map((n) => n.trim())
      .map((n) => `[${n}](#cite-${n})`)
      .join(''),
  )
}

function sentenceAround(text: string, citation: number): string {
  const marker = new RegExp(`\\[(?:\\d{1,3}\\s*,\\s*)*${citation}(?:\\s*,\\s*\\d{1,3})*\\]`)
  const at = text.search(marker)
  if (at < 0) return ''
  const before = text.slice(0, at)
  const start = Math.max(before.lastIndexOf('. '), before.lastIndexOf('。'), before.lastIndexOf('\n')) + 1
  return text.slice(start, at).replace(/\*\*/g, '').trim()
}

function AnswerText({ content, onCite }: { content: string; onCite?: (index: number) => void }) {
  return (
    <div className="answer break-words">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        skipHtml
        components={{
          a: ({ href, children }) => {
            const match = href?.match(/^#cite-(\d+)$/)
            if (match && onCite) {
              const index = Number(match[1])
              return (
                <button
                  type="button"
                  className="cite"
                  aria-label={`來源 ${index}`}
                  onClick={() => onCite(index)}
                >
                  {index}
                </button>
              )
            }
            return (
              <a href={href} target="_blank" rel="noreferrer">
                {children}
              </a>
            )
          },
        }}
      >
        {onCite ? linkCitations(content) : content}
      </ReactMarkdown>
    </div>
  )
}

/** Words and figures of the citing sentence that the source holds too: what to highlight. */
function highlights(snippet: string, sentence: string): string[] {
  const numbers = sentence.match(/\d[\d,.]*%?/g) ?? []
  const words = (sentence.match(/[A-Za-z][A-Za-z-]{3,}/g) ?? []).filter(
    (w) =>
      !['that', 'this', 'with', 'from', 'than', 'which', 'their', 'while', 'these', 'those'].includes(
        w.toLowerCase(),
      ),
  )
  return [...new Set([...numbers, ...words])].filter((term) => snippet.includes(term))
}

function Highlighted({ text, terms }: { text: string; terms: string[] }) {
  if (terms.length === 0) return <>{text}</>
  const escaped = terms
    .map((t) => t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'))
    .sort((a, b) => b.length - a.length)
  const parts = text.split(new RegExp(`(${escaped.join('|')})`, 'g'))
  return (
    <>
      {parts.map((part, i) =>
        terms.includes(part) ? (
          <mark key={i} className="rounded bg-warning-soft px-0.5 text-text">
            {part}
          </mark>
        ) : (
          <span key={i}>{part}</span>
        ),
      )}
    </>
  )
}

export function SourceViewer({
  source,
  sentence,
  onClose,
}: {
  source: Source
  sentence: string
  onClose: () => void
}) {
  const isPdf = source.filename.toLowerCase().endsWith('.pdf')
  const fileUrl = `/api/v1/documents/${source.document_id}/file#page=${source.page_start}`
  const terms = highlights(source.snippet, sentence)
  return (
    <section
      aria-label="來源檢視"
      className="flex h-full flex-col rounded-xl border border-border bg-surface"
    >
      <header className="flex items-start gap-2 border-b border-border px-3 py-2">
        <div className="min-w-0 flex-1">
          <p className="truncate text-sm font-semibold">
            [{source.index}] {source.filename}
          </p>
          <p className="text-xs text-muted">
            {pageRange(source.page_start, source.page_end)}
            {source.section_title ? ` · ${source.section_title}` : ''}
            {describeOrigin(source) ? ` · ${describeOrigin(source)}` : ''}
          </p>
        </div>
        <a className="text-xs text-accent underline" href={fileUrl} target="_blank" rel="noreferrer">
          開新分頁
        </a>
        <button
          type="button"
          className="rounded-full border border-border px-2 text-xs hover:bg-surface-2"
          onClick={onClose}
          aria-label="關閉來源檢視"
        >
          ✕
        </button>
      </header>
      {sentence && (
        <p className="border-b border-border px-3 py-2 text-xs text-muted">引用這段的句子：「{sentence}」</p>
      )}
      <p className="max-h-48 overflow-y-auto whitespace-pre-wrap break-words px-3 py-2 text-sm">
        <Highlighted text={source.snippet} terms={terms} />
      </p>
      {isPdf && (
        <iframe
          title={`${source.filename} 第 ${source.page_start} 頁`}
          src={fileUrl}
          className="min-h-[55vh] flex-1 border-t border-border"
        />
      )}
    </section>
  )
}

function MessageView({
  message,
  onCite,
}: {
  message: ChatMessage
  onCite: (source: Source, sentence: string) => void
}) {
  if (message.role === 'user') {
    return (
      <li className="flex justify-end py-2">
        <div className="max-w-[80%] rounded-2xl rounded-br-md bg-accent px-4 py-2 text-on-accent">
          <p className="whitespace-pre-wrap break-words">{message.content}</p>
        </div>
      </li>
    )
  }
  const unfinished = UNFINISHED_LABEL[message.status]
  const { answer, notes } = splitNotes(message.content)
  const cite = (index: number) => {
    const source = message.sources.find((s) => s.index === index)
    if (source) onCite(source, sentenceAround(answer, index))
  }
  return (
    <li className="py-2">
      <div className="flex items-start gap-3">
        <span
          aria-hidden="true"
          className="mt-1 flex h-7 w-7 shrink-0 items-center justify-center rounded-lg bg-accent text-xs font-bold text-on-accent"
        >
          D
        </span>
        <div className="min-w-0 flex-1">
          {(unfinished || (message.status === 'completed' && message.answered === false)) && (
            <p className="mb-1 text-xs text-muted">
              {unfinished && (
                <span
                  className={`font-medium ${message.status === 'failed' ? 'text-danger' : 'text-accent'}`}
                >
                  {unfinished}
                </span>
              )}
              {message.status === 'completed' && message.answered === false && (
                <span className="pill bg-warning-soft font-medium text-warning">文件中找不到答案</span>
              )}
            </p>
          )}
          <AnswerText content={answer} onCite={message.sources.length > 0 ? cite : undefined} />
          {notes.length > 0 && (
            <details className="mt-2 rounded-lg border border-warning-soft bg-warning-soft/40 px-3 py-1.5 text-xs">
              <summary className="cursor-pointer font-medium text-warning">
                核對結果（{notes.length} 則註記）
              </summary>
              <ul className="mt-1 list-disc space-y-1 pl-4 text-muted">
                {notes.map((note, i) => (
                  <li key={i} className="whitespace-pre-wrap break-words">
                    {note}
                  </li>
                ))}
              </ul>
            </details>
          )}
          <SourceList sources={message.sources} onView={(source) => onCite(source, '')} />
        </div>
      </div>
    </li>
  )
}

/** Ask questions about the user's ready documents, in a conversation. */
export function ChatPanel({ documents, sidebar }: { documents: DocumentItem[]; sidebar?: ReactNode }) {
  const ready = documents.filter((document) => document.status === 'ready')
  const [conversations, setConversations] = useState<Conversation[]>([])
  const [activeId, setActiveId] = useState<string | null>(null)
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [selected, setSelected] = useState<string[]>([])
  const [question, setQuestion] = useState('')
  const [asking, setAsking] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [scope, setScope] = useState<SearchScope | null>(null)
  const [route, setRoute] = useState<{
    type: string
    standalone_question: string
    asked: string
  } | null>(null)
  const [usage, setUsage] = useState<Usage | null>(null)
  const [stage, setStage] = useState<Stage | null>(null)
  const [revision, setRevision] = useState<Revision | null>(null)
  const [navigation, setNavigation] = useState<Navigation | null>(null)
  const [check, setCheck] = useState<NumberCheck | null>(null)
  const [pendingDelete, setPendingDelete] = useState<Conversation | null>(null)
  const [panelOpen, setPanelOpen] = useState(false)
  const [viewer, setViewer] = useState<{
    source: Source
    sentence: string
  } | null>(null)

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
    setViewer(null)
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
            updateAnswer((answer) => ({
              ...answer,
              content: answer.content + askEvent.data.text,
            }))
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
    <details
      aria-label="本次回答的檢索與用量"
      className="rounded-xl border border-border bg-surface-2 px-3 py-2 text-sm"
      open={viewer === null && !inspectorEmpty}
    >
      <summary className="cursor-pointer text-xs font-semibold uppercase tracking-wide text-muted">
        本次回答的檢索與用量
      </summary>
      {inspectorEmpty && (
        <p className="mt-2 text-muted">送出問題後，這裡會顯示搜尋範圍、處理步驟、token 用量與數字核對。</p>
      )}
      {scopeText !== null && <p className="mt-2 text-muted">這次搜尋的範圍：{scopeText}</p>}
      {route !== null && <p className="text-muted">問題類型：{ROUTE_LABEL[route.type] ?? route.type}</p>}
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
    </details>
  )

  const rail = (
    <aside className="flex min-h-0 flex-col gap-4 overflow-y-auto" aria-label="文件與對話">
      {sidebar}
      <section className="panel p-3">
        <div className="flex items-center justify-between">
          <h2 className="text-sm font-semibold">對話</h2>
          <button
            type="button"
            className="rounded-full border border-border px-3 py-1 text-xs hover:bg-surface-2 disabled:opacity-50"
            disabled={asking || activeId === null}
            onClick={() => open(null)}
          >
            ＋ 新對話
          </button>
        </div>
        <ul className="mt-2 list-none space-y-1 p-0 text-sm" aria-label="對話清單">
          {conversations.length === 0 && <li className="px-2 py-1 text-xs text-muted">還沒有對話。</li>}
          {conversations.map((conversation) => {
            const isActive = conversation.id === activeId
            return (
              <li key={conversation.id} className="flex items-center gap-1">
                <button
                  type="button"
                  className={`min-w-0 flex-1 truncate rounded-lg px-2 py-1.5 text-left hover:bg-surface-2 ${
                    isActive ? 'bg-accent-soft font-medium text-accent' : ''
                  }`}
                  disabled={asking}
                  aria-current={isActive ? 'true' : undefined}
                  onClick={() => open(conversation.id)}
                >
                  {conversation.title || '（未命名的對話）'}
                </button>
                {isActive && (
                  <button
                    type="button"
                    className="rounded-full px-2 py-1 text-xs text-muted hover:bg-danger-soft hover:text-danger"
                    disabled={asking}
                    aria-label="刪除對話"
                    title="刪除對話"
                    onClick={() => setPendingDelete(conversation)}
                  >
                    ✕
                  </button>
                )}
              </li>
            )
          })}
        </ul>
      </section>
    </aside>
  )

  return (
    <div
      className={`grid h-full min-h-0 gap-4 lg:grid-cols-[minmax(260px,300px)_minmax(0,1fr)${
        panelOpen ? '_minmax(360px,440px)' : ''
      }]`}
    >
      {rail}
      <section className="panel flex h-full min-h-0 flex-col p-4">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <h2 className="truncate font-semibold">{active ? active.title || '（未命名的對話）' : '新對話'}</h2>
          <button
            type="button"
            className={`rounded-full border px-3 py-1 text-xs ${
              panelOpen ? 'border-accent bg-accent-soft text-accent' : 'border-border hover:bg-surface-2'
            }`}
            aria-pressed={panelOpen}
            onClick={() => setPanelOpen((open) => !open)}
          >
            {panelOpen ? '收起來源檢視 ▸' : '◂ 來源檢視'}
          </button>
        </div>

        {ready.length === 0 ? (
          <p className="mt-2 text-muted">還沒有可以提問的文件。上傳文件並等待處理完成後就能提問。</p>
        ) : (
          <fieldset className="mt-3 rounded-lg bg-surface-2 px-3 py-2 text-sm">
            <legend className="px-1 text-xs text-muted">
              搜尋範圍：
              {scopeIds.length === 0 ? '所有可用文件' : `已選 ${scopeIds.length} 份`}
            </legend>
            <div className="flex flex-wrap gap-x-3 gap-y-1">
              {ready.map((document) => (
                <label
                  key={document.id}
                  className={`flex cursor-pointer items-center gap-1 rounded-full border px-2 py-0.5 text-xs ${
                    scopeIds.includes(document.id)
                      ? 'border-accent bg-accent-soft text-accent'
                      : 'border-border'
                  }`}
                >
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

        <div className="mt-3 grid min-h-0 flex-1 gap-4">
          <div className="flex min-h-0 min-w-0 flex-col">
            {messages.length > 0 ? (
              <ul
                className="min-h-0 flex-1 list-none space-y-1 overflow-y-auto p-0 pr-1"
                aria-label="對話內容"
              >
                {messages.map((message) => (
                  <MessageView
                    key={message.id}
                    message={message}
                    onCite={(source, sentence) => {
                      setViewer({ source, sentence })
                      setPanelOpen(true)
                    }}
                  />
                ))}
              </ul>
            ) : (
              ready.length > 0 && (
                <div className="rounded-xl border border-dashed border-border bg-surface-2 p-6 text-center text-sm text-muted">
                  還沒有對話。輸入問題，或用下面的快捷鈕。回答會附來源，文件裡沒有的內容會明說找不到。
                </div>
              )
            )}
            {error && (
              <p role="alert" className="mt-2 text-sm text-danger">
                {error}
              </p>
            )}

            <form
              className="mt-3 flex items-end gap-2 rounded-2xl border border-border bg-surface-2 p-2 focus-within:border-accent"
              onSubmit={handleAsk}
            >
              <label className="flex-1">
                <span className="sr-only">問題</span>
                <textarea
                  className="w-full resize-none bg-transparent px-2 py-1 outline-none"
                  rows={2}
                  placeholder="針對文件提問，例如：summary this document."
                  value={question}
                  disabled={asking || ready.length === 0}
                  onChange={(event) => setQuestion(event.target.value)}
                />
              </label>
              <span className="hidden pb-1 text-xs text-muted sm:block">
                {ready.length > 0 &&
                  (scopeIds.length === 0 ? `${ready.length} 份來源` : `${scopeIds.length} 份來源`)}
              </span>
              <button
                type="submit"
                className="rounded-full bg-accent px-4 py-1.5 text-sm font-medium text-on-accent disabled:opacity-50"
                disabled={asking || ready.length === 0 || question.trim() === ''}
              >
                {asking ? '回答中…' : '送出'}
              </button>
            </form>
            {ready.length > 0 && messages.length === 0 && (
              <div className="mt-2 flex flex-wrap gap-2" aria-label="快捷問題">
                {QUICK_QUESTIONS.map((text) => (
                  <button
                    key={text}
                    type="button"
                    className="rounded-full border border-border bg-surface px-3 py-0.5 text-xs text-muted hover:border-accent hover:text-accent"
                    disabled={asking}
                    onClick={() => setQuestion(text)}
                  >
                    {text}
                  </button>
                ))}
              </div>
            )}
            <div className="mt-2">{inspector}</div>
          </div>
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
      {panelOpen && (
        <div className="min-h-0">
          {viewer ? (
            <SourceViewer
              source={viewer.source}
              sentence={viewer.sentence}
              onClose={() => setPanelOpen(false)}
            />
          ) : (
            <section
              aria-label="來源檢視"
              className="flex h-full flex-col items-center justify-center rounded-xl border border-dashed border-border bg-surface-2 p-6 text-center text-sm text-muted"
            >
              點回答裡的數字標籤，或來源卡上的「在右側檢視」，這裡會顯示該段原文、引用它的句子，以及 PDF
              的那一頁。
            </section>
          )}
        </div>
      )}
    </div>
  )
}
