import { motion } from 'motion/react'
import type { Session } from '../lib/types.ts'

interface Props {
  sessions: Session[]
  activeId: string | null
  onSelect: (id: string) => void
  onNew: () => void
}

export default function SessionList({ sessions, activeId, onSelect, onNew }: Props) {
  return (
    <aside className="flex h-full w-[280px] shrink-0 flex-col border-l border-hairline bg-canvas-soft">
      <div className="flex items-center justify-between border-b border-hairline px-4 py-3">
        <span className="text-[11px] font-semibold uppercase tracking-[0.88px] text-muted">
          نشست‌ها
        </span>
        <button
          onClick={onNew}
          className="rounded-md border border-hairline px-2 py-1 text-[12px] text-body transition-colors hover:bg-surface hover:text-ink"
        >
          + جدید
        </button>
      </div>

      <div className="flex-1 overflow-y-auto p-2">
        {sessions.length === 0 ? (
          <p className="px-2 py-6 text-center text-[13px] text-muted">
            هنوز نشستی نیست
          </p>
        ) : (
          <ul className="space-y-1">
            {sessions.map((s) => {
              const active = s.id === activeId
              return (
                <motion.li
                  key={s.id}
                  initial={{ opacity: 0, x: -6 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.22, ease: [0.16, 1, 0.3, 1] }}
                >
                  <button
                    onClick={() => onSelect(s.id)}
                    className={`w-full rounded-md border px-3 py-2 text-right transition-colors ${
                      active
                        ? 'border-hairline-strong bg-surface text-ink'
                        : 'border-transparent text-body hover:bg-surface/60'
                    }`}
                  >
                    <span className="block truncate text-[13px]">{s.title}</span>
                    <span className="mt-0.5 block font-mono text-[11px] text-muted">
                      {s.messages.length} پیام · {new Date(s.createdAt).toLocaleDateString('fa-IR')}
                    </span>
                  </button>
                </motion.li>
              )
            })}
          </ul>
        )}
      </div>
    </aside>
  )
}
