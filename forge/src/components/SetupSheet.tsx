import { useEffect } from 'react'
import { AnimatePresence, motion } from 'motion/react'
import Icon from './Icon.tsx'
import type { HealthResponse } from '../lib/api.ts'
import type { HealthState } from '../lib/types.ts'

interface Props {
  open: boolean
  onClose: () => void
  health: HealthResponse | null
}

/**
 * راهنمایِ وصل‌کردنِ ابزارها.
 *
 * چرا ساخته شد؟ وضعیتِ «غایب/ناقص» فقط در قالبِ چند قرصِ کوچک در بالای صفحه
 * نشان داده می‌شد و هیچ توضیحی نداشت که یعنی چه و چه باید کرد. اینجا هر
 * ابزار با نیازمندی و نشانیِ منبع آمده است.
 *
 * نشانی‌ها از بررسیِ مستقیمِ هر پروژه در همین دوره گرفته شده‌اند.
 */
const GUIDE: Record<
  string,
  { title: string; needs: string; role: string; url: string; fallback: string }
> = {
  jcode: {
    title: 'Jcode',
    needs: 'Rust (برای ساخت) — باینریِ jcode در PATH',
    role: 'هسته‌ی اجرا: فرمان‌ها را واقعاً روی کد اجرا می‌کند',
    url: 'https://github.com/1jehuang/jcode',
    fallback: 'بدونِ آن، فرمان‌ها ارسال می‌شوند اما چیزی اجرا نمی‌شود.',
  },
  soup: {
    title: 'Soup',
    needs: 'Python ۳٫۱۲ یا newer',
    role: 'انتخابِ مهارت: کدام مهارت به این درخواست می‌خورد',
    url: 'https://github.com/southwind-ai/soup',
    fallback: 'بدونِ آن، Forge از مسیریابِ داخلیِ خودش (BM25 روی همان مهارت‌ها) استفاده می‌کند.',
  },
  godmode: {
    title: 'Godmode',
    needs: 'همراهِ برنامه است — چیزی لازم ندارد',
    role: 'محتوا: ۹ فرمان و ۵ عامل',
    url: 'https://github.com/patrickking67/godmode',
    fallback: 'محتوایش از پیش داخلِ برنامه است (Apache-2.0).',
  },
  mcp: {
    title: 'MCP',
    needs: 'Node ۲۲ و پیکربندیِ کلاینتِ MCP',
    role: 'دسترسی به ابزارهای بیرونی از طریقِ پروتکلِ MCP',
    url: 'https://modelcontextprotocol.io',
    fallback: 'بدونِ آن، فقط ابزارهای داخلی در دسترس‌اند.',
  },
}

const STATE: Record<HealthState, { label: string; token: string; icon: 'check' | 'alert' | 'close' }> =
  {
    ready: { label: 'آماده', token: 'success', icon: 'check' },
    degraded: { label: 'ناقص', token: 'done', icon: 'alert' },
    missing: { label: 'غایب', token: 'muted', icon: 'close' },
  }

export default function SetupSheet({ open, onClose, health }: Props) {
  useEffect(() => {
    if (!open) return
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose()
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [open, onClose])

  const adapters = health?.adapters ?? []

  return (
    <AnimatePresence>
      {open && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.18, ease: [0.16, 1, 0.3, 1] }}
          className="fixed inset-0 z-50 flex items-center justify-center p-6"
          style={{ backgroundColor: 'color-mix(in oklab, var(--color-canvas) 78%, transparent)' }}
          onClick={onClose}
          role="dialog"
          aria-modal="true"
          aria-label="راهنمای وصل‌کردنِ ابزارها"
        >
          <motion.div
            initial={{ opacity: 0, y: 12, scale: 0.985 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 8, scale: 0.99 }}
            transition={{ duration: 0.24, ease: [0.16, 1, 0.3, 1] }}
            onClick={(e) => e.stopPropagation()}
            className="max-h-[80vh] w-full max-w-xl overflow-y-auto rounded-card border border-hairline bg-canvas-soft"
          >
            <div className="flex items-start justify-between border-b border-hairline px-6 py-5">
              <div>
                <h2 className="text-title-md text-ink">وصل‌کردنِ ابزارها</h2>
                <p className="mt-1 text-body-sm text-muted">
                  Forge خودش مدل ندارد؛ این ابزارها هستند که کار را انجام می‌دهند.
                </p>
              </div>
              <button
                onClick={onClose}
                aria-label="بستن"
                className="rounded-control border border-hairline p-2 text-muted transition-colors hover:bg-surface hover:text-ink"
              >
                <Icon name="close" size={16} />
              </button>
            </div>

            <ul className="divide-y divide-hairline">
              {adapters.length === 0 && (
                <li className="px-5 py-6 text-body-sm text-muted">
                  وضعیتی از سرور نرسید — سرور در حال بالا آمدن است.
                </li>
              )}
              {adapters.map((a) => {
                const g = GUIDE[a.name]
                const st = STATE[a.state]
                return (
                  <li key={a.name} className="px-5 py-4">
                    <div className="flex items-start gap-3">
                      <span
                        className="mt-1 shrink-0"
                        style={{ color: `var(--color-${st.token})` }}
                      >
                        <Icon name={st.icon} size={16} />
                      </span>
                      <div className="min-w-0 flex-1">
                        <div className="flex items-center gap-2">
                          <span className="text-body-sm text-ink">{g?.title ?? a.name}</span>
                          <span
                            className="text-caption"
                            style={{ color: `var(--color-${st.token})` }}
                          >
                            {st.label}
                          </span>
                        </div>
                        {g && <p className="mt-1 text-body-sm text-muted">{g.role}</p>}
                        <p className="mt-1 text-code text-muted-soft">{a.detail || g?.needs}</p>
                        <p className="mt-1 text-body-sm text-muted">{g?.fallback}</p>
                        {g && a.state !== 'ready' && (
                          <a
                            href={g.url}
                            target="_blank"
                            rel="noreferrer"
                            className="mt-2 inline-flex items-center gap-1.5 text-body-sm text-ink underline decoration-hairline-strong underline-offset-4 transition-colors hover:decoration-brand"
                          >
                            <Icon name="download" size={14} />
                            صفحه‌ی پروژه
                          </a>
                        )}
                      </div>
                    </div>
                  </li>
                )
              })}
            </ul>

            <div className="border-t border-hairline px-5 py-3">
              <p className="text-body-sm text-muted">
                پس از نصب، برنامه را دوباره اجرا کنید تا وضعیت به‌روزرسانی شود.
              </p>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  )
}
