import { useEffect, useRef } from 'react'
import { motion } from 'motion/react'

interface Props {
  value: string
  onChange: (v: string) => void
  onSubmit: () => void
  busy: boolean
  onOpenPalette: () => void
}

export default function Composer({ value, onChange, onSubmit, busy, onOpenPalette }: Props) {
  const ref = useRef<HTMLTextAreaElement>(null)

  useEffect(() => {
    const el = ref.current
    if (!el) return
    el.style.height = 'auto'
    el.style.height = `${Math.min(el.scrollHeight, 180)}px`
  }, [value])

  return (
    <div className="border-t border-hairline bg-canvas-soft px-6 py-4">
      <div className="flex items-end gap-3">
        <textarea
          ref={ref}
          rows={1}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault()
              onSubmit()
            }
            if (e.key === 'k' && (e.metaKey || e.ctrlKey)) {
              e.preventDefault()
              onOpenPalette()
            }
          }}
          placeholder="چه کاری انجام شود؟ برای دستورها Ctrl+K را بزنید…"
          className="min-h-[40px] flex-1 resize-none rounded-md border border-hairline bg-surface px-3 py-2 text-[14px] text-ink outline-none transition-colors placeholder:text-muted-soft focus:border-hairline-strong"
        />

        <motion.button
          whileTap={{ scale: 0.97 }}
          onClick={onSubmit}
          disabled={busy || !value.trim()}
          className="h-10 shrink-0 rounded-md px-5 text-[14px] font-medium text-white transition-colors disabled:opacity-40"
          style={{ backgroundColor: 'var(--color-brand)' }}
        >
          {busy ? 'در حال اجرا…' : 'اجرا'}
        </motion.button>
      </div>

      <p className="mt-2 text-[11px] text-muted">
        Enter برای ارسال · Shift+Enter برای خط جدید · Ctrl+K برای فهرستِ دستورها
      </p>
    </div>
  )
}
