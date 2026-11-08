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
  /** The server's default answer temperature (AC-60); null = the model's default. */
  answer_temperature: number | null
  /** Debug mode (D98): the check notes are appended to answers and the check panel shown. */
  check_notes: boolean
}

export type DocumentStatus = 'uploaded' | 'processing' | 'ready' | 'failed'
export type SummaryStatus = 'none' | 'processing' | 'ready' | 'failed' | 'skipped'

export interface DocumentItem {
  id: string
  filename: string
  media_type: string
  file_size: number
  status: DocumentStatus
  summary_status: SummaryStatus
  /** Whether a summary tree is built after indexing (chosen at upload, D91). */
  build_summary: boolean
  error: string | null
  page_count: number | null
  chunk_count: number
  created_at: string
  updated_at: string
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
  // A FormData body (file upload) sets its own multipart Content-Type.
  const isForm = body instanceof FormData
  const response = await fetch(`${API}${path}`, {
    method,
    // The session lives in an HttpOnly cookie; the browser sends it for us.
    credentials: 'same-origin',
    headers: body === undefined || isForm ? undefined : { 'Content-Type': 'application/json' },
    body: body === undefined ? undefined : isForm ? body : JSON.stringify(body),
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

export const listDocuments = () => request<DocumentItem[]>('GET', '/documents')
export const deleteDocument = (id: string) => request<void>('DELETE', `/documents/${id}`)
export const retryDocument = (id: string) => request<DocumentItem>('POST', `/documents/${id}/retry`)
export function uploadDocument(file: File, buildSummary = true) {
  const form = new FormData()
  form.append('file', file)
  form.append('build_summary', buildSummary ? 'true' : 'false')
  return request<DocumentItem>('POST', '/documents', form)
}

export interface DocumentProgress {
  kind: string
  stage: 'parsing' | 'chunking' | 'embedding' | 'summarizing' | null
  current: number | null
  total: number | null
}

export interface DocumentWatcher {
  onStatus: (status: { status: DocumentStatus; summary_status: SummaryStatus }) => void
  onProgress: (progress: DocumentProgress) => void
  /** Processing ended, or the stream could not continue. Time to reload the list. */
  onDone: () => void
}

/**
 * Follow the processing of one document through server-sent events.
 * Returns a function that stops watching.
 */
export function watchDocument(id: string, watcher: DocumentWatcher): () => void {
  if (typeof EventSource === 'undefined') return () => {}
  const source = new EventSource(`${API}/documents/${id}/events`)
  const finish = () => {
    // Close first: an EventSource reconnects by itself when the server ends the stream.
    source.close()
    watcher.onDone()
  }
  source.addEventListener('status', (event) => {
    watcher.onStatus(
      JSON.parse((event as MessageEvent<string>).data) as {
        status: DocumentStatus
        summary_status: SummaryStatus
      },
    )
  })
  source.addEventListener('progress', (event) => {
    watcher.onProgress(JSON.parse((event as MessageEvent<string>).data) as DocumentProgress)
  })
  source.addEventListener('done', finish)
  source.addEventListener('error', (event) => {
    // The server also sends an event named "error" (with data) when processing
    // failed; `done` follows it. Without data it is a connection problem: the
    // browser retries by itself unless it has given up.
    const fromServer = typeof (event as MessageEvent<string>).data === 'string'
    if (!fromServer && source.readyState === EventSource.CLOSED) finish()
  })
  return () => source.close()
}

export interface Conversation {
  id: string
  title: string
  created_at: string
  updated_at: string
}

export interface Source {
  index: number
  kind: 'chunk' | 'summary'
  document_id: string
  filename: string
  page_start: number
  page_end: number
  section_title: string | null
  snippet: string
  score: number | null
  /** How the source got here: found by search, added as a table's discussion, or a stored summary. */
  origin: 'retrieval' | 'table_context' | 'navigation' | 'summary' | 'previous_turn'
}

export type MessageStatus = 'pending' | 'streaming' | 'completed' | 'failed' | 'interrupted'

export interface ChatMessage {
  id: string
  role: 'user' | 'assistant'
  content: string
  status: MessageStatus
  answered: boolean | null
  sources: Source[]
  /** The answer's sampling temperature (AC-60); null for questions and the model default. */
  temperature?: number | null
  created_at: string
}

export interface ConversationDetail extends Conversation {
  messages: ChatMessage[]
}

export interface SearchScope {
  mode: 'all' | 'selected'
  document_ids: string[]
}

export interface Usage {
  prompt_tokens: number | null
  completion_tokens: number | null
  /** The per-call limit; null when the figures are the sum of several calls (D69). */
  limit: number | null
  calls?: number
}

/** A finding that faulted a draft in the two-call mode (D69). */
export interface RevisionTrigger {
  kind: string
  severity: 'hard' | 'soft'
  feedback: string
}

/** What the experimental two-call mode did for this answer (D69); null in the default mode. */
export interface Revision {
  mode: 'conditional' | 'always'
  triggered?: boolean
  draft_triggers?: RevisionTrigger[]
  revision_triggers?: RevisionTrigger[]
  skipped?: string | null
  chosen?: 'draft' | 'revision'
  status?: 'verified' | 'unverified'
  reason?: string
}

export type Stage = 'navigating' | 'generating' | 'verifying' | 'correcting' | 'revising' | 'finalizing'

/** What the experimental navigate mode did (D71); null in the other modes. */
export interface DirectionIssue {
  sentence: string
  left: string
  right: string
  status: 'inconsistent' | 'uncertain' | 'incomparable'
  detail: string
}

export interface Completeness {
  status: 'complete' | 'incomplete' | 'not_applicable'
  required: string[]
  missing: string[]
  condition: string | null
}

export type AnalysisStatus =
  'SUPPORTED_AND_COMPLETE' | 'FACTUALLY_CORRECT_BUT_INCOMPLETE' | 'FACTUALLY_INCORRECT' | 'UNCERTAIN'

export interface NavigationTarget {
  text: string
  located: boolean
  pages: number[]
  /** D73: the Navigator's place, what it needs there, and how the selection went. */
  location?: string
  need?: string
  priority?: 'required' | 'supplementary'
  status?: 'covered' | 'missing' | null
  /** D74: how far the retrieved sources already held the target, judged by structure. */
  coverage?: 'covered' | 'partial' | 'missing' | 'unknown' | 'not_located'
  label?: string | null
  candidates?: number
  selected?: number[]
  excluded?: { ordinal: number; reason: string }[]
}

export interface Navigation {
  map_entries: number
  plan: string | null
  items: NavigationTarget[]
  located: number
  fetched: number
  kept: number
  excluded_budget: number
  skipped: string | null
  budget?: number
  evidence_tokens?: number
  embedding?: { texts: number; failed: string | null }
  coverage?: { location: string; status: string; reason: string }[]
  unmet_required?: string[]
  supplementary_used?: number
  matrix?: { cells: number; tables: string[]; definitions: string[] }
  log?: {
    ordinal: number
    page: number
    kept: boolean
    reason: string
    target?: number | null
    score?: number | null
  }[]
}

/** A figure of the answer found on a cited page, with the original text around it (AC-26). */
export interface VerifiedNumber {
  number: string
  document_id: string
  page: number
  snippet: string
}

/** A table figure whose labels in the answer differ from the source table (D64). */
export interface MislabelledNumber {
  number: string
  answer_labels: string[]
  source_labels: string[][]
  sentence: string
}

/** A table figure the check could neither confirm nor contradict (D67): the labels the
 *  answer gives it fit some cells, but a label is missing or two candidates are given. */
export interface UnresolvedNumber extends MislabelledNumber {
  reason: 'missing' | 'ambiguous'
}

/** A sentence claiming one method wins everywhere, checked cell by cell against the table (D68). */
export interface OverstatedClaim {
  sentence: string
  method: string
  compared: string[]
  higher: number
  lower: number
  examples: string[]
  status: 'contradicted' | 'unresolved'
  reason: string | null
}

/** A statement whose citation points at a source that hardly states it, while another does (D68). */
export interface DoubtfulCitation {
  sentence: string
  cited: number[]
  closer: number[]
  coverage_cited: number
  coverage_closer: number
}

export interface NumberCheck {
  verified_numbers: VerifiedNumber[]
  unverified_numbers: string[]
  mislabelled_numbers: MislabelledNumber[]
  unresolved_numbers: UnresolvedNumber[]
  overstated_claims: OverstatedClaim[]
  doubtful_citations: DoubtfulCitation[]
}

/** The events of an answer stream, in the order they arrive. */
export type AskEvent =
  | {
      name: 'start'
      data: {
        user_message_id: string
        assistant_message_id: string
        scope: SearchScope
        /** The temperature the answer call uses: the request's, else the server's default. */
        temperature: number | null
      }
    }
  | { name: 'route'; data: { type: string; standalone_question: string } }
  | { name: 'sources'; data: Source[] }
  | { name: 'stage'; data: { stage: Stage } }
  | { name: 'delta'; data: { text: string } }
  | { name: 'usage'; data: Usage }
  | {
      name: 'done'
      data: NumberCheck & {
        status: MessageStatus
        answered: boolean | null
        cited: number[]
        finish_reason: string | null
        revision: Revision | null
        navigation?: Navigation | null
        /** D74: two-figure comparisons checked against the tables, and completeness. */
        direction_issues?: DirectionIssue[]
        completeness?: Completeness
        analysis_status?: AnalysisStatus | null
        /** D75: what the deterministic correction changed before the answer was sent. */
        correction?: {
          changed: boolean
          edits: { kind: string; before: string; after: string }[]
          removed: string[]
          remaining: string[]
        } | null
      }
    }
  | { name: 'error'; data: { code: string; detail: string } }

export const listConversations = () => request<Conversation[]>('GET', '/conversations')
export const createConversation = (title?: string) =>
  request<Conversation>('POST', '/conversations', { title: title ?? null })
export const getConversation = (id: string) => request<ConversationDetail>('GET', `/conversations/${id}`)
export const deleteConversation = (id: string) => request<void>('DELETE', `/conversations/${id}`)

/**
 * Ask a question. A question that is refused throws an ApiError before any
 * event; otherwise `onEvent` is called for each event until the answer ends.
 */
export async function askQuestion(
  conversationId: string,
  question: string,
  documentIds: string[],
  onEvent: (event: AskEvent) => void,
  temperature: number | null = null,
): Promise<void> {
  // `temperature` is sent only when the user chose one; omitted, the server's default
  // applies (AC-60).
  const body: Record<string, unknown> = { question, document_ids: documentIds }
  if (temperature !== null) body.temperature = temperature
  const response = await fetch(`${API}/conversations/${conversationId}/messages`, {
    method: 'POST',
    credentials: 'same-origin',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  if (!response.ok || response.body === null) {
    let code = 'HTTP_ERROR'
    let detail = `Backend responded with HTTP ${response.status}`
    try {
      const payload = (await response.json()) as { code?: string; detail?: unknown }
      code = payload.code ?? code
      if (typeof payload.detail === 'string') detail = payload.detail
    } catch {
      // Not a JSON error body; keep the defaults.
    }
    throw new ApiError(response.status, code, detail)
  }

  const reader = response.body.getReader()
  const decoder = new TextDecoder()
  let buffer = ''
  const flush = () => {
    // Events are separated by a blank line: "event: <name>\ndata: <json>".
    let end = buffer.indexOf('\n\n')
    while (end !== -1) {
      const block = buffer.slice(0, end)
      buffer = buffer.slice(end + 2)
      const name = /^event: (.*)$/m.exec(block)?.[1]
      const data = /^data: (.*)$/m.exec(block)?.[1]
      if (name && data) onEvent({ name, data: JSON.parse(data) } as AskEvent)
      end = buffer.indexOf('\n\n')
    }
  }
  for (;;) {
    const { done, value } = await reader.read()
    if (done) break
    buffer += decoder.decode(value, { stream: true })
    flush()
  }
  buffer += decoder.decode()
  flush()
}
