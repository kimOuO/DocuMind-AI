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
  uploaded: 'text-muted',
  processing: 'text-accent',
  ready: 'text-success',
  failed: 'text-danger',
}

const STAGE_LABEL: Record<string, string> = {
  parsing: '解析文件',
  chunking: '切分段落',
  embedding: '建立索引',
  summarizing: '產生摘要',
}

/** What a document is doing right now, or what became of it. */
function describeState(document: DocumentItem, progress: DocumentProgress | undefined): string {
  if (document.status === 'processing' && progress?.stage) {
    const counted = progress.total ? ` ${progress.current ?? 0}/${progress.total}` : ''
    return `${STATUS_LABEL.processing}：${STAGE_LABEL[progress.stage] ?? progress.stage}${counted}`
  }
  if (document.status === 'ready') {
    const pages = document.page_count === null ? '' : ` · ${document.page_count} 頁`
    return `${STATUS_LABEL.ready}${pages} · ${document.chunk_count} 個片段`
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

  // Follow every document that is waiting or being processed, and stop
  // following those that are finished or gone.
  useEffect(() => {
    const open = watchers.current
    const unfinished = new Set(
      (documents ?? [])
        .filter((d) => d.status === 'uploaded' || d.status === 'processing')
        .map((d) => d.id),
    )
    for (const [id, stop] of open) {
      if (!unfinished.has(id)) {
        stop()
        open.delete(id)
      }
    }
    for (const id of unfinished) {
      if (open.has(id)) continue
      const stop = watchDocument(id, {
        onStatus: (status) =>
          setDocuments((current) =>
            current === null ? current : current.map((d) => (d.id === id ? { ...d, status } : d)),
          ),
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

  async function handleFile(event: ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0]
    if (!file) return
    setBusy(true)
    setError(null)
    setNotice(null)
    try {
      const known = new Set((documents ?? []).map((d) => d.id))
      const uploaded = await uploadDocument(file)
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
    <section className="mt-4 rounded-lg border border-border bg-surface p-4">
      <div className="flex items-center justify-between gap-4">
        <h2 className="font-semibold">我的文件</h2>
        <label className="cursor-pointer rounded-md bg-accent px-3 py-1 text-sm font-medium text-surface">
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
      <p className="mt-1 text-sm text-muted">支援 PDF、TXT、Markdown。</p>

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
        <p className="mt-3 text-muted">還沒有文件。上傳第一份文件開始使用。</p>
      )}
      {documents !== null && documents.length > 0 && (
        <ul className="mt-3 list-none p-0">
          {documents.map((document) => (
            <li
              key={document.id}
              className="flex items-center justify-between gap-4 border-t border-border py-2"
            >
              <div className="min-w-0">
                <p className="truncate font-medium">{document.filename}</p>
                <p className="text-sm">
                  <span className="text-muted">{formatSize(document.file_size)} · </span>
                  <span className={STATUS_CLASS[document.status]}>
                    {describeState(document, progress[document.id])}
                  </span>
                </p>
                {document.status === 'failed' && document.error && (
                  <p className="break-words text-sm text-muted">原因：{document.error}</p>
                )}
              </div>
              {document.status === 'failed' && (
                <button
                  type="button"
                  className="shrink-0 rounded-md border border-border px-2 py-1 text-sm"
                  onClick={() => handleRetry(document)}
                  aria-label={`重試 ${document.filename}`}
                >
                  重試
                </button>
              )}
              <button
                type="button"
                className="shrink-0 rounded-md border border-border px-2 py-1 text-sm text-danger"
                onClick={() => setPendingDelete(document)}
                aria-label={`刪除 ${document.filename}`}
              >
                刪除
              </button>
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
