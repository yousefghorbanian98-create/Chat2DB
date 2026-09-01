import { useState } from 'react'
import { AnimatePresence, motion } from 'motion/react'
import Icon from './Icon.tsx'
import { api, type UpdateCheck } from '../lib/api.ts'

interface Props {
  check: UpdateCheck | null
}

/**
 * نشانگرِ به‌روزرسانیِ تفاضلی.
 *
 * نکته‌ی طراحی: اندازه‌ی بسته کنارِ دکمه نوشته می‌شود تا معلوم باشد این
 * به‌روزرسانی «چند کیلوبایت» است نه «یک نصب‌کننده‌ی ۲۱ مگابایتیِ دوباره».
 */
export default function UpdateChip({ check }: Props) {
  const [state, setState] = useState<'idle' | 'applying' | 'done' | 'error'>('idle')
  const [message, setMessage] = useState('')

  if (!check || check.upToDate) return null

  const kb = (check.deltaBytes / 1024).toFixed(1)
  const mb = (check.fullBytes / 1048576).toFixed(1)

  const apply = async () => {
    setState('applying')
    try {
      const res = await api.updateApply()
      if (!res.ok) {
        setState('error')
        setMessage(res.error ?? 'ناموفق')
        return
      }
      setState('done')
      setMessage(
        res.restartRequired
          ? `${res.applied} فایل به‌روزرسانی شد — برنامه را دوباره باز کنید`
          : `${res.applied} فایل به‌روزرسانی شد — در حال بارگذاریِ دوباره`,
      )
      // اگر فقط دارایی‌های رابط عوض شده باشند، یک بارگذاریِ دوباره کافی است
      if (res.reloadSufficient) {
        setTimeout(() => window.location.reload(), 900)
      }
    } catch (err) {
      setState('error')
      setMessage(err instanceof Error ? err.message : 'خطای ناشناخته')
    }
  }

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0, y: -4 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0 }}
        transition={{ duration: 0.22, ease: [0.16, 1, 0.3, 1] }}
        className="flex items-center gap-2 rounded-md border border-hairline bg-surface px-2 py-1"
      >
        <span style={{ color: 'var(--color-done)' }}>
          <Icon name="download" size={13} />
        </span>

        {state === 'idle' && (
          <>
            <span className="text-body-sm text-body">
              به‌روزرسانیِ {kb} کیلوبایت
              <span className="text-muted"> (به‌جای {mb} مگابایت)</span>
            </span>
            <button
              onClick={apply}
              className="rounded-md border border-hairline px-2 py-0.5 text-button text-ink transition-colors hover:bg-surface-strong"
            >
              اعمال
            </button>
          </>
        )}

        {state === 'applying' && (
          <span className="flex items-center gap-1.5 text-body-sm text-muted">
            <span className="flex items-center gap-0.5">
              {[0, 1, 2].map((i) => (
                <span
                  key={i}
                  className="size-1.5 animate-forge-pulse rounded-full"
                  style={{ backgroundColor: 'var(--color-brand)', animationDelay: `${i * 0.16}s` }}
                />
              ))}
            </span>
            در حال دریافت و تأیید…
          </span>
        )}

        {(state === 'done' || state === 'error') && (
          <span
            className="text-body-sm"
            style={{ color: state === 'error' ? 'var(--color-error)' : 'var(--color-success)' }}
          >
            {message}
          </span>
        )}
      </motion.div>
    </AnimatePresence>
  )
}
