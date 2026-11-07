import { useEffect, useRef, useState, type ChangeEvent } from 'react'
import {
  ApiError,
  deleteDocument,
  listDocuments,
  retryDocument,
  uploadDocument,
  watchDocument,
  type DocumentItem,
  type DocumentProgress,
  type DocumentStatus,
  type SummaryStatus,
} from '../../lib/api'
import { ConfirmDialog } from '../../components/ConfirmDialog'
import { formatSize } from '../../lib/format'

const STATUS_LABEL: Record<DocumentStatus, string> = {
  uploaded: '已上傳，等待處理',
  processing: '處理中',
  ready: '可以提問',
  failed: '處理失敗',
}

const STATUS_CLASS: Record<DocumentStatus, string> = {
  uploaded: 'bg-surface-2 text-muted',
  processing: 'bg-accent-soft text-accent',
  ready: 'bg-success-soft text-success',
  failed: 'bg-danger-soft text-danger',
}

const STAGE_LABEL: Record<string, string> = {
  parsing: '解析文件',
  chunking: '切分段落',
  embedding: '建立索引',
  summarizing: '產生摘要',
}

const SUMMARY_LABEL: Record<SummaryStatus, string> = {
  none: '尚無摘要',
  processing: '摘要產生中',
  ready: '摘要已完成',
  failed: '摘要失敗',
  skipped: '未建摘要（摘要類問題以檢索回答）',
}

/** Still being worked on: indexing, or the summary that follows it (AC-11). */
function isUnfinished(document: DocumentItem): boolean {
  return (
    document.status === 'uploaded' ||
    document.status === 'processing' ||
    document.summary_status === 'processing'
  )
}

/** What a document is doing right now, or what became of it. */
function describeState(document: DocumentItem, progress: DocumentProgress | undefined): string {
  if (document.status === 'processing' && progress?.stage) {
    const counted = progress.total ? ` ${progress.current ?? 0}/${progress.total}` : ''
    return `${STATUS_LABEL.processing}：${STAGE_LABEL[progress.stage] ?? progress.stage}${counted}`
  }
  if (document.status === 'ready') {
    const pages = document.page_count === null ? '' : ` · ${document.page_count} 頁`
    const chunks = document.chunk_count ? ` · ${document.chunk_count} 個片段` : ''
    // The summary is made after indexing; its sections are counted as they are done.
    const counted =
      document.summary_status === 'processing' && progress?.kind === 'summary' && progress.total
        ? ` ${progress.current ?? 0}/${progress.total}`
        : ''
    return `${STATUS_LABEL.ready}${pages}${chunks} · ${SUMMARY_LABEL[document.summary_status]}${counted}`
  }
  return STATUS_LABEL[document.status]
}

const MESSAGES: Record<string, string> = {
  UNSUPPORTED_MEDIA_TYPE: '不支援這個檔案格式。可上傳 PDF、TXT、Markdown。',
  FILE_TOO_LARGE: '檔案超過大小上限。',
  EMPTY_FILE: '這個檔案是空的。',
  DOCUMENT_NOT_FOUND: '找不到這份文件，可能已經被刪除。',
  RETRY_NOT_ALLOWED: '這份文件目前不能重試。',
  ORIGIN_NOT_ALLOWED: '這個網址不在允許的來源清單內，請從設定的網址開啟。',
}

function describe(error: unknown): string {
  if (error instanceof ApiError) return MESSAGES[error.code] ?? error.message
  return '無法連線到伺服器，請稍後再試。'
}

export function DocumentPanel({
  onChange,
}: {
  /** Told whenever the list of documents changes, so other panels can use it. */
  onChange?: (documents: DocumentItem[]) => void
} = {}) {
  const [documents, setDocuments] = useState<DocumentItem[] | null>(null)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [notice, setNotice] = useState<string | null>(null)
  const [pendingDelete, setPendingDelete] = useState<DocumentItem | null>(null)
  const [progress, setProgress] = useState<Record<string, DocumentProgress>>({})
  const fileInput = useRef<HTMLInputElement>(null)
  // One open progress stream per document that is still being processed.
  const watchers = useRef(new Map<string, () => void>())

  // Initial load. State is only set from the promise callbacks, and not at all
  // if the component has been unmounted in the meantime.
  useEffect(() => {
    let active = true
    listDocuments()
      .then((items) => {
        if (active) setDocuments(items)
      })
      .catch((caught: unknown) => {
        if (!active) return
        setError(describe(caught))
        setDocuments([])
      })
    return () => {
      active = false
    }
  }, [])

  async function refresh() {
    try {
      setDocuments(await listDocuments())
    } catch (caught) {
      setError(describe(caught))
    }
  }

  useEffect(() => {
    if (documents !== null) onChange?.(documents)
  }, [documents, onChange])

  // Follow every document that is waiting, being indexed or being summarised,
  // and stop following those that are finished or gone.
  useEffect(() => {
    const open = watchers.current
    const unfinished = new Set((documents ?? []).filter(isUnfinished).map((d) => d.id))
    for (const [id, stop] of open) {
      if (!unfinished.has(id)) {
        stop()
        open.delete(id)
      }
    }
    for (const id of unfinished) {
      if (open.has(id)) continue
      const stop = watchDocument(id, {
        onStatus: ({ status, summary_status }) => {
          setDocuments((current) =>
            current === null
              ? current
              : current.map((d) => (d.id === id ? { ...d, status, summary_status } : d)),
          )
          // Indexed: the list now has the page and chunk counts, and the document can
          // be asked about while its summary is still being made.
          if (status === 'ready') {
            listDocuments()
              .then(setDocuments)
              .catch((caught: unknown) => setError(describe(caught)))
          }
        },
        onProgress: (update) => setProgress((current) => ({ ...current, [id]: update })),
        onDone: () => {
          open.delete(id)
          setProgress((current) => {
            const rest = { ...current }
            delete rest[id]
            return rest
          })
          // The list has the final page and chunk counts, or the reason it failed.
          listDocuments()
            .then(setDocuments)
            .catch((caught: unknown) => setError(describe(caught)))
        },
      })
      open.set(id, stop)
    }
  }, [documents])

  useEffect(() => {
    const open = watchers.current
    return () => {
      for (const stop of open.values()) stop()
      open.clear()
    }
  }, [])

  const [buildSummary, setBuildSummary] = useState(true)

  async function handleFile(event: ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0]
    if (!file) return
    setBusy(true)
    setError(null)
    setNotice(null)
    try {
      const known = new Set((documents ?? []).map((d) => d.id))
      const uploaded = await uploadDocument(file, buildSummary)
      setNotice(
        known.has(uploaded.id)
          ? `這份文件先前已經上傳過（${uploaded.filename}）。`
          : `已上傳 ${uploaded.filename}。`,
      )
      await refresh()
    } catch (caught) {
      setError(describe(caught))
    } finally {
      setBusy(false)
      // Allow choosing the same file again.
      if (fileInput.current) fileInput.current.value = ''
    }
  }

  async function handleDelete(document: DocumentItem) {
    setPendingDelete(null)
    setError(null)
    setNotice(null)
    try {
      await deleteDocument(document.id)
      setNotice(`已刪除 ${document.filename}。`)
    } catch (caught) {
      setError(describe(caught))
    }
    await refresh()
  }

  async function handleRetry(document: DocumentItem) {
    setError(null)
    setNotice(null)
    try {
      await retryDocument(document.id)
      setNotice(`已重新排入處理：${document.filename}。`)
    } catch (caught) {
      setError(describe(caught))
    }
    await refresh()
  }

  return (
    <section className="panel p-4">
      <div className="flex items-center justify-between gap-4">
        <h2 className="font-semibold">我的文件</h2>
        <label className="cursor-pointer rounded-full bg-accent px-3 py-1 text-sm font-medium text-on-accent hover:opacity-90">
          {busy ? '上傳中…' : '上傳文件'}
          <input
            ref={fileInput}
            type="file"
            accept=".pdf,.txt,.md"
            className="sr-only"
            disabled={busy}
            onChange={handleFile}
          />
        </label>
      </div>
      <p className="mt-1 text-xs text-muted">支援 PDF、TXT、Markdown。上傳後在背景解析並建立索引。</p>
      <label className="mt-2 flex cursor-pointer items-start gap-2 text-xs text-muted">
        <input
          type="checkbox"
          className="mt-0.5"
          checked={buildSummary}
          disabled={busy}
          onChange={(event) => setBuildSummary(event.target.checked)}
        />
        <span>
          上傳後建立摘要樹（建議）。逐章讀完整份文件再濃縮，約 3 分鐘；關掉則 summary
          類問題只依據檢索到的片段回答。
        </span>
      </label>

      {notice && (
        <p role="status" className="mt-2 text-sm text-success">
          {notice}
        </p>
      )}
      {error && (
        <p role="alert" className="mt-2 text-sm text-danger">
          {error}
        </p>
      )}

      {documents === null && <p className="mt-3">載入中…</p>}
      {documents !== null && documents.length === 0 && (
        <div className="mt-3 rounded-lg border border-dashed border-border bg-surface-2 p-4 text-center text-sm text-muted">
          還沒有文件。上傳第一份文件開始使用。
        </div>
      )}
      {documents !== null && documents.length > 0 && (
        <ul className="mt-3 list-none space-y-2 p-0">
          {documents.map((document) => (
            <li
              key={document.id}
              className="flex items-start gap-3 rounded-xl border border-border bg-surface-2 p-3 shadow-sm"
            >
              <span
                aria-hidden="true"
                className="mt-0.5 flex h-10 w-8 shrink-0 items-center justify-center rounded-md border border-border bg-surface text-[10px] font-semibold uppercase text-accent"
              >
                {document.media_type}
              </span>
              <div className="min-w-0 flex-1">
                <p className="truncate text-sm font-medium" title={document.filename}>
                  {document.filename}
                </p>
                <p className="mt-1 text-xs">
                  <span className="text-muted">{formatSize(document.file_size)} · </span>
                  <span className={`pill ${STATUS_CLASS[document.status]}`}>
                    {describeState(document, progress[document.id])}
                  </span>
                </p>
                {document.status === 'failed' && document.error && (
                  <p className="mt-1 break-words text-xs text-muted">原因：{document.error}</p>
                )}
                {(() => {
                  const p = progress[document.id]
                  const active =
                    p?.total &&
                    ((document.status === 'processing' && p.kind === 'index') ||
                      (document.summary_status === 'processing' && p.kind === 'summary'))
                  if (!active) return null
                  const label =
                    p.kind === 'summary'
                      ? `摘要：第 ${p.current ?? 0}／${p.total} 章`
                      : `索引：${p.current ?? 0}／${p.total}`
                  return (
                    <div className="mt-1 flex items-center gap-2 text-xs text-muted">
                      <progress
                        className="h-1.5 w-full accent-accent"
                        value={p.current ?? 0}
                        max={p.total}
                        aria-label={label}
                      />
                      <span className="shrink-0">{label}</span>
                    </div>
                  )
                })()}
                <div className="mt-1 flex gap-2">
                  {document.status === 'failed' && (
                    <button
                      type="button"
                      className="rounded-full border border-border px-2 py-0.5 text-xs hover:bg-surface"
                      onClick={() => handleRetry(document)}
                      aria-label={`重試 ${document.filename}`}
                    >
                      重試
                    </button>
                  )}
                  {document.status === 'ready' &&
                    (document.summary_status === 'none' ||
                      document.summary_status === 'failed' ||
                      document.summary_status === 'skipped') && (
                      <button
                        type="button"
                        className="rounded-full border border-border px-2 py-0.5 text-xs hover:bg-surface"
                        onClick={() => handleRetry(document)}
                        aria-label={`建立摘要 ${document.filename}`}
                      >
                        建立摘要
                      </button>
                    )}
                  <button
                    type="button"
                    className="rounded-full border border-border px-2 py-0.5 text-xs text-danger hover:bg-surface"
                    onClick={() => setPendingDelete(document)}
                    aria-label={`刪除 ${document.filename}`}
                  >
                    刪除
                  </button>
                </div>
              </div>
            </li>
          ))}
        </ul>
      )}

      {pendingDelete && (
        <ConfirmDialog
          title="刪除文件"
          message={`確定要刪除「${pendingDelete.filename}」嗎？刪除後無法復原。`}
          confirmLabel="確定刪除"
          danger
          onConfirm={() => handleDelete(pendingDelete)}
          onCancel={() => setPendingDelete(null)}
        />
      )}
    </section>
  )
}
