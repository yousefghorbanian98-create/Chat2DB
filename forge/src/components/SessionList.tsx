import { motion } from 'motion/react'
import Icon from './Icon.tsx'
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
        <span className="text-caption text-muted">نشست‌ها</span>
        <button
          onClick={onNew}
          aria-label="نشستِ جدید"
          className="flex items-center gap-1.5 rounded-md border border-hairline px-2.5 py-1.5 text-button text-body transition-colors hover:bg-surface hover:text-ink"
        >
          <Icon name="plus" size={14} />
          جدید
        </button>
      </div>

      <div className="flex-1 overflow-y-auto p-2">
        {sessions.length === 0 ? (
          <div className="flex flex-col items-center gap-2 px-2 py-8 text-center">
            <span className="text-muted">
              <Icon name="stack" size={20} />
            </span>
            <p className="text-body-sm text-muted">هنوز نشستی نیست</p>
          </div>
        ) : (
          <ul className="space-y-0.5">
            {sessions.map((s, i) => {
              const active = s.id === activeId
              return (
                <motion.li
                  key={s.id}
                  initial={{ opacity: 0, x: -6 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.22, delay: 0.02 * i, ease: [0.16, 1, 0.3, 1] }}
                >
                  <button
                    onClick={() => onSelect(s.id)}
                    className={`relative w-full overflow-hidden rounded-md px-3 py-2 text-right transition-colors ${
                      active ? 'bg-surface' : 'hover:bg-surface/60'
                    }`}
                  >
                    {/* نشانگرِ نشستِ فعال — عمق با خطِ مویی، نه سایه */}
                    {active && (
                      <span
                        className="absolute inset-y-1 right-0 w-0.5 rounded-full"
                        style={{ backgroundColor: 'var(--color-brand)' }}
                      />
                    )}
                    <span
                      className={`block truncate text-body-sm ${active ? 'text-ink' : 'text-body'}`}
                    >
                      {s.title}
                    </span>
                    <span className="mt-0.5 flex items-center gap-1.5 text-caption text-muted">
                      <Icon name="message" size={11} />
                      {s.messages.length}
                      <span className="text-muted-soft">·</span>
                      <Icon name="clock" size={11} />
                      {new Date(s.createdAt).toLocaleDateString('fa-IR')}
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
