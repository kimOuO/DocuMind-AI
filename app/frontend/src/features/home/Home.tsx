import { useState } from 'react'
import { type DocumentItem } from '../../lib/api'
import { ChatPanel } from '../chat/ChatPanel'
import { DocumentPanel } from '../documents/DocumentPanel'

/** The signed-in workspace (D91): conversations and sources in the left rail, the
 * conversation in the middle, a source viewer on the right when a citation is opened. */
export function Home() {
  const [documents, setDocuments] = useState<DocumentItem[]>([])
  return (
    <div className="min-h-0 flex-1 p-4">
      <ChatPanel documents={documents} sidebar={<DocumentPanel onChange={setDocuments} />} />
    </div>
  )
}
