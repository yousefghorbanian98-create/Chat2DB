import { useEffect, useRef } from 'react'
import { motion } from 'motion/react'
import Icon from './Icon.tsx'

interface Props {
  value: string
  onChange: (v: string) => void
  onSubmit: () => void
  busy: boolean
  onOpenPalette: () => void
  /** با هر تغییر، نشانگر به داخلِ کادر می‌رود (برای پیشنهادهای صفحه‌ی آغاز) */
  focusSignal?: number
}

export default function Composer({
  value,
  onChange,
  onSubmit,
  busy,
  onOpenPalette,
  focusSignal = 0,
}: Props) {
  const ref = useRef<HTMLTextAreaElement>(null)

  useEffect(() => {
    if (focusSignal === 0) return
    ref.current?.focus()
  }, [focusSignal])

  useEffect(() => {
    const el = ref.current
    if (!el) return
    el.style.height = 'auto'
    el.style.height = `${Math.min(el.scrollHeight, 180)}px`
  }, [value])

  return (
    <div className="border-t border-hairline bg-canvas-soft px-6 py-4">
      <div className="mx-auto max-w-3xl">
        {/* ظرفِ ورودی — DESIGN.md: فیلد روی سطحِ کارت با خطِ مویی */}
        <div className="flex items-end gap-2 rounded-lg border border-hairline bg-surface px-3 py-2 transition-colors focus-within:border-hairline-strong">
          <button
            onClick={onOpenPalette}
            aria-label="فهرستِ دستورها"
            title="فهرستِ دستورها (Ctrl+K)"
            className="mb-1 shrink-0 rounded-md p-2 text-muted transition-colors hover:bg-canvas hover:text-ink"
          >
            <Icon name="sparkles" size={17} />
          </button>

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
            placeholder="چه کاری انجام شود؟"
            aria-label="پیام"
            className="min-h-[36px] flex-1 resize-none bg-transparent py-2 text-body-md text-ink outline-none placeholder:text-muted-soft"
          />

          <motion.button
            whileTap={{ scale: 0.97 }}
            onClick={onSubmit}
            disabled={busy || !value.trim()}
            aria-label="اجرا"
            className="mb-0.5 flex h-10 shrink-0 items-center gap-2 rounded-lg px-4 text-button text-ink transition-colors disabled:opacity-40"
            style={{ backgroundColor: 'var(--color-brand)' }}
          >
            {busy ? (
              <>
                <span className="flex items-center gap-0.5">
                  {[0, 1, 2].map((i) => (
                    <span
                      key={i}
                      className="size-1.5 animate-forge-pulse rounded-full"
                      style={{ backgroundColor: 'var(--color-ink)', animationDelay: `${i * 0.16}s` }}
                    />
                  ))}
                </span>
                <span>در حال اجرا</span>
              </>
            ) : (
              <>
                <Icon name="send" size={16} />
                <span>اجرا</span>
              </>
            )}
          </motion.button>
        </div>

        <div className="mt-2 flex items-center justify-between px-1">
          <p className="text-body-sm text-muted">
            <span className="kbd-chip">Enter</span> ارسال ·{' '}
            <span className="kbd-chip">Shift</span> + <span className="kbd-chip">Enter</span> خطِ جدید
          </p>
          <button
            onClick={onOpenPalette}
            className="flex items-center gap-1.5 text-body-sm text-muted transition-colors hover:text-ink"
          >
            <span className="kbd-chip">Ctrl</span> + <span className="kbd-chip">K</span>
            <span>دستورها</span>
          </button>
        </div>
      </div>
    </div>
  )
}
