import { motion } from 'motion/react'
import Icon, { type IconName } from './Icon.tsx'
import type { HealthResponse } from '../lib/api.ts'

interface Props {
  onPick: (prompt: string) => void
  health: HealthResponse | null
  onOpenSetup: () => void
}

/**
 * چرا چنین چیزی لازم بود؟ رابط برای نخستین‌بار یک پاراگرافِ تنها نشان می‌داد
 * و هیچ راهنمایی نمی‌کرد که کاربر دقیقاً چه می‌تواند بگوید — یا چرا بعضی
 * ابزارها کار نمی‌کنند. اینجا هر دو پرسش را همان لحظه‌ی اول جواب می‌دهیم.
 */
const SUGGESTIONS: Array<{ icon: IconName; title: string; hint: string; prompt: string }> = [
  {
    icon: 'search',
    title: 'این کدبیس را توضیح بده',
    hint: 'مسیرِ اجرا را بخوان و معماری را توضیح بده',
    prompt: '/revelation این کدبیس را توضیح بده — از کجا شروع می‌شود و هر بخش چه می‌کند؟',
  },
  {
    icon: 'sparkles',
    title: 'یک قابلیتِ جدید بساز',
    hint: 'از ایده تا پیاده‌سازی با برنامه‌ی مرحله‌به‌مرحله',
    prompt: '/genesis می‌خواهم یک قابلیتِ جدید اضافه کنم. از کجا شروع کنیم؟',
  },
  {
    icon: 'alert',
    title: 'چرا این تست شکست می‌خورد؟',
    hint: 'ردیابیِ خطا تا رسیدن به علتِ ریشه‌ای',
    prompt: '/exorcise این تست fail می‌شود؛ علتِ ریشه‌ای را پیدا کن.',
  },
  {
    icon: 'check',
    title: 'این Pull Request را بازبینی کن',
    hint: 'بررسیِ کیفیت، ریسک و قراردادهای پروژه',
    prompt: '/judgment این Pull Request را بازبینی کن و ریسک‌ها را بگو.',
  },
]

export default function Welcome({ onPick, health, onOpenSetup }: Props) {
  const pending = (health?.adapters ?? []).filter((a) => a.state !== 'ready')

  return (
    <div className="flex h-full items-center justify-center overflow-y-auto px-6 py-10">
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.32, ease: [0.16, 1, 0.3, 1] }}
        className="mx-auto w-full max-w-2xl"
      >
        {/* نشان و معرفی */}
        <div className="flex flex-col items-center text-center">
          <span
            className="flex size-14 items-center justify-center rounded-card border border-hairline bg-surface-strong"
            style={{ color: 'var(--color-brand)' }}
          >
            <Icon name="sparkles" size={26} />
          </span>
          <h2 className="mt-6 text-display-lg text-ink">Forge</h2>
          <p className="mt-3 max-w-md text-body-md text-muted">
            سه ابزارِ کدنویسی در یک پنجره. بنویسید چه می‌خواهید — یا یکی از
            شروع‌کننده‌های زیر را انتخاب کنید.
          </p>
        </div>

        {/* شروع‌کننده‌ها */}
        <div className="mt-10 grid gap-3 sm:grid-cols-2">
          {SUGGESTIONS.map((s, i) => (
            <motion.button
              key={s.title}
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.32, delay: 0.06 * i, ease: [0.16, 1, 0.3, 1] }}
              onClick={() => onPick(s.prompt)}
              className="group lift flex items-start gap-3 rounded-card border border-hairline bg-surface px-4 py-4 text-right hover:lift-hover"
            >
              <span
                className="flex size-9 shrink-0 items-center justify-center rounded-control bg-surface-strong text-muted transition-colors group-hover:text-ink"
              >
                <Icon name={s.icon} size={18} />
              </span>
              <span className="min-w-0 pt-0.5">
                <span className="block text-body-md text-ink">{s.title}</span>
                <span className="mt-1 block text-body-sm text-muted">{s.hint}</span>
              </span>
            </motion.button>
          ))}
        </div>

        {/* اگر ابزاری ناقص یا غایب است، همان‌جا راهنمایی کن — پنهان نماند */}
        {pending.length > 0 && (
          <motion.button
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.3, delay: 0.2, ease: [0.16, 1, 0.3, 1] }}
            onClick={onOpenSetup}
            className="lift mt-3 flex w-full items-center gap-3 rounded-card border border-hairline bg-surface px-4 py-3 text-right hover:lift-hover"
          >
            <span className="flex size-9 shrink-0 items-center justify-center rounded-control bg-surface-strong text-muted">
              <Icon name="wrench" size={18} />
            </span>
            <span className="min-w-0 flex-1">
              <span className="block text-body-sm text-ink">
                {pending.length} ابزار هنوز کامل وصل نیست
              </span>
              <span className="mt-0.5 block truncate text-body-sm text-muted">
                {pending.map((a) => a.name).join(' · ')} — برای راهنمای نصب اینجا را باز کنید
              </span>
            </span>
            <span className="shrink-0 text-muted">
              <Icon name="chevron" size={16} />
            </span>
          </motion.button>
        )}
      </motion.div>
    </div>
  )
}
