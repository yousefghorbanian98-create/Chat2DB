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
            className="flex size-12 items-center justify-center rounded-lg border border-hairline-strong bg-surface"
            style={{ color: 'var(--color-brand)' }}
          >
            <Icon name="sparkles" size={22} />
          </span>
          <h2 className="mt-5 text-display-md text-ink">Forge</h2>
          <p className="mt-2 max-w-md text-body-md text-muted">
            سه ابزارِ کدنویسی در یک پنجره. بنویسید چه می‌خواهید — یا یکی از
            شروع‌کننده‌های زیر را انتخاب کنید.
          </p>
        </div>

        {/* شروع‌کننده‌ها */}
        <div className="mt-8 grid gap-2 sm:grid-cols-2">
          {SUGGESTIONS.map((s, i) => (
            <motion.button
              key={s.title}
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.28, delay: 0.04 * i, ease: [0.16, 1, 0.3, 1] }}
              onClick={() => onPick(s.prompt)}
              className="group flex items-start gap-3 rounded-lg border border-hairline bg-canvas-soft px-4 py-3 text-right transition-colors hover:border-hairline-strong hover:bg-surface"
            >
              <span className="mt-0.5 shrink-0 text-muted transition-colors group-hover:text-ink">
                <Icon name={s.icon} size={17} />
              </span>
              <span className="min-w-0">
                <span className="block text-body-sm text-ink">{s.title}</span>
                <span className="mt-0.5 block text-body-sm text-muted">{s.hint}</span>
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
            className="mt-4 flex w-full items-center gap-3 rounded-lg border border-hairline bg-canvas-soft px-4 py-3 text-right transition-colors hover:border-hairline-strong hover:bg-surface"
          >
            <span className="shrink-0 text-muted">
              <Icon name="wrench" size={17} />
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
