import { useEffect, useMemo, useState } from 'react'
import { AnimatePresence, motion } from 'motion/react'
import type { Agent, Command } from '../lib/types.ts'

interface Props {
  open: boolean
  onClose: () => void
  commands: Command[]
  agents: Agent[]
  onPick: (slug: string) => void
}

export default function CommandPalette({ open, onClose, commands, agents, onPick }: Props) {
  const [q, setQ] = useState('')

  useEffect(() => {
    if (open) setQ('')
  }, [open])

  const filtered = useMemo(() => {
    const needle = q.trim().toLowerCase()
    const all = [
      ...commands.map((c) => ({ slug: c.slug, description: c.description, kind: 'دستور' as const })),
      ...agents.map((a) => ({ slug: a.slug, description: a.description, kind: 'ساب‌ایجنت' as const })),
    ]
    if (!needle) return all
    return all.filter(
      (i) => i.slug.includes(needle) || i.description.toLowerCase().includes(needle),
    )
  }, [q, commands, agents])

  useEffect(() => {
    if (!open) return
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose()
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [open, onClose])

  return (
    <AnimatePresence>
      {open && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.18 }}
          className="fixed inset-0 z-50 flex items-start justify-center bg-black/50 pt-24"
          onClick={onClose}
        >
          <motion.div
            initial={{ opacity: 0, y: -12, scale: 0.98 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -8, scale: 0.98 }}
            transition={{ duration: 0.24, ease: [0.16, 1, 0.3, 1] }}
            onClick={(e) => e.stopPropagation()}
            className="w-[min(560px,92vw)] overflow-hidden rounded-card border border-hairline-strong bg-surface"
          >
            <input
              autoFocus
              value={q}
              onChange={(e) => setQ(e.target.value)}
              placeholder="جستجو در دستورها و ساب‌ایجنت‌ها…"
              className="w-full border-b border-hairline bg-transparent px-4 py-3 text-[14px] text-ink outline-none placeholder:text-muted-soft"
            />

            <ul className="max-h-80 overflow-y-auto p-2">
              {filtered.length === 0 ? (
                <li className="px-3 py-6 text-center text-[13px] text-muted">چیزی یافت نشد</li>
              ) : (
                filtered.map((item) => (
                  <li key={`${item.kind}-${item.slug}`}>
                    <button
                      onClick={() => {
                        onPick(item.slug)
                        onClose()
                      }}
                      className="flex w-full items-center justify-between gap-3 rounded-control px-3 py-2 text-right transition-colors hover:bg-canvas-soft"
                    >
                      <span className="font-mono text-[13px] text-ink">/{item.slug}</span>
                      <span className="flex-1 truncate text-[12px] text-muted">
                        {item.description}
                      </span>
                      <span className="shrink-0 rounded-full border border-hairline px-2 py-0.5 text-[10px] text-muted">
                        {item.kind}
                      </span>
                    </button>
                  </li>
                ))
              )}
            </ul>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  )
}
