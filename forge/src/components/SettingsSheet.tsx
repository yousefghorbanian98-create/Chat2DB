import { useEffect, useState } from 'react'
import { AnimatePresence, motion } from 'motion/react'
import Icon from './Icon.tsx'
import { api, type SettingsView } from '../lib/api.ts'

interface Props {
  open: boolean
  onClose: () => void
  onSaved: () => void
}

/**
 * تنظیمات — «مغز» اینجا وصل می‌شود.
 *
 * تا پیش از این برنامه نه می‌دانست روی کدام پوشه کار کند و نه می‌شد به مدلی
 * وصلش کرد؛ برای همین عملاً هیچ خروجی‌ای تولید نمی‌کرد. این دو چیز همین‌جا
 * تنظیم می‌شوند و روی دیسکِ خودِ کاربر می‌مانند.
 */
type ProviderType = 'openai-compatible' | 'anthropic'

const PRESETS: Array<{ label: string; type: ProviderType; baseUrl: string; model: string }> = [
  { label: 'OpenAI', type: 'openai-compatible', baseUrl: 'https://api.openai.com/v1', model: 'gpt-4o-mini' },
  { label: 'Anthropic', type: 'anthropic', baseUrl: 'https://api.anthropic.com', model: 'claude-sonnet-4-5' },
  { label: 'Groq', type: 'openai-compatible', baseUrl: 'https://api.groq.com/openai/v1', model: 'llama-3.3-70b-versatile' },
  { label: 'OpenRouter', type: 'openai-compatible', baseUrl: 'https://openrouter.ai/api/v1', model: 'anthropic/claude-sonnet-4.5' },
  { label: 'Ollama (محلی)', type: 'openai-compatible', baseUrl: 'http://localhost:11434/v1', model: 'llama3.2' },
]

export default function SettingsSheet({ open, onClose, onSaved }: Props) {
  const [settings, setSettings] = useState<SettingsView | null>(null)
  const [workspace, setWorkspace] = useState('')
  const [workspaceState, setWorkspaceState] = useState<'unknown' | 'ok' | 'bad'>('unknown')
  const [type, setType] = useState<ProviderType>('openai-compatible')
  const [baseUrl, setBaseUrl] = useState('')
  const [model, setModel] = useState('')
  const [apiKey, setApiKey] = useState('')
  const [saving, setSaving] = useState(false)
  const [test, setTest] = useState<{ ok: boolean; message: string } | null>(null)

  useEffect(() => {
    if (!open) return
    api
      .settings()
      .then((s) => {
        setSettings(s)
        setWorkspace(s.workspaceDir ?? '')
        setWorkspaceState(s.workspaceDir ? 'ok' : 'unknown')
        if (s.provider) {
          setType(s.provider.type)
          setBaseUrl(s.provider.baseUrl)
          setModel(s.provider.model)
        }
      })
      .catch(() => setSettings(null))
  }, [open])

  const checkWorkspace = async () => {
    if (!workspace.trim()) return
    const r = await api.validateWorkspace(workspace.trim()).catch(() => null)
    setWorkspaceState(r?.isDirectory ? 'ok' : 'bad')
  }

  const save = async () => {
    setSaving(true)
    setTest(null)
    try {
      await api.saveSettings({
        workspaceDir: workspace.trim() || null,
        provider: model.trim()
          ? {
              type,
              baseUrl: baseUrl.trim() || (type === 'anthropic' ? 'https://api.anthropic.com' : 'https://api.openai.com/v1'),
              model: model.trim(),
              // خالی گذاشتن یعنی «کلیدِ قبلی را نگه دار» — سرور آن را نادیده می‌گیرد
              apiKey: apiKey.trim() || (settings?.provider ? '__KEEP__' : ''),
            }
          : null,
      })
      onSaved()
      onClose()
    } finally {
      setSaving(false)
    }
  }

  const runTest = async () => {
    setTest(null)
    const r = await api.testProvider().catch((e: Error) => ({ ok: false, message: e.message }))
    setTest(r)
  }

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
          aria-label="تنظیمات"
        >
          <motion.div
            initial={{ opacity: 0, y: 12, scale: 0.985 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 8, scale: 0.99 }}
            transition={{ duration: 0.24, ease: [0.16, 1, 0.3, 1] }}
            onClick={(e) => e.stopPropagation()}
            className="max-h-[85vh] w-full max-w-2xl overflow-y-auto rounded-card border border-hairline bg-canvas-soft"
          >
            <div className="flex items-start justify-between border-b border-hairline px-6 py-5">
              <div>
                <h2 className="text-title-md text-ink">تنظیمات</h2>
                <p className="mt-1 text-body-sm text-muted">
                  برای اینکه برنامه واقعاً کاری انجام دهد، پوشه‌ی پروژه و یک مدل لازم است.
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

            <div className="space-y-6 px-6 py-5">
              {/* ۱) پوشه‌ی پروژه */}
              <section>
                <h3 className="text-caption text-muted">پوشه‌ی پروژه</h3>
                <p className="mt-1 text-body-sm text-muted">
                  عامل روی همین پوشه کار می‌کند. بدون آن، اجرا عملاً بی‌معناست.
                </p>
                <div className="mt-3 flex gap-2">
                  <input
                    dir="ltr"
                    value={workspace}
                    onChange={(e) => {
                      setWorkspace(e.target.value)
                      setWorkspaceState('unknown')
                    }}
                    placeholder="C:\Users\...\my-project"
                    className="min-w-0 flex-1 rounded-control border border-hairline bg-surface px-3 py-2 text-left text-code text-ink outline-none placeholder:text-muted-soft"
                  />
                  <button
                    onClick={checkWorkspace}
                    className="shrink-0 rounded-control border border-hairline px-3 py-2 text-button text-body transition-colors hover:bg-surface hover:text-ink"
                  >
                    بررسی
                  </button>
                </div>
                {workspaceState !== 'unknown' && (
                  <p
                    className="mt-2 flex items-center gap-1.5 text-body-sm"
                    style={{
                      color: workspaceState === 'ok' ? 'var(--color-success)' : 'var(--color-error)',
                    }}
                  >
                    <Icon name={workspaceState === 'ok' ? 'check' : 'alert'} size={14} />
                    {workspaceState === 'ok' ? 'پوشه وجود دارد' : 'این مسیر پوشه نیست یا وجود ندارد'}
                  </p>
                )}
              </section>

              {/* ۲) مدل */}
              <section>
                <h3 className="text-caption text-muted">مدل (مغزِ برنامه)</h3>
                <p className="mt-1 text-body-sm text-muted">
                  کلید فقط در فایلِ تنظیمات روی همین دستگاه می‌ماند و تنها به پایگاهی
                  فرستاده می‌شود که خودتان اینجا می‌دهید.
                </p>

                <div className="mt-3 flex flex-wrap gap-2">
                  {PRESETS.map((p) => (
                    <button
                      key={p.label}
                      onClick={() => {
                        setType(p.type)
                        setBaseUrl(p.baseUrl)
                        setModel(p.model)
                      }}
                      className="rounded-chip border border-hairline px-3 py-1.5 text-button text-body transition-colors hover:bg-surface hover:text-ink"
                    >
                      {p.label}
                    </button>
                  ))}
                </div>

                <div className="mt-3 grid gap-2 sm:grid-cols-2">
                  <input
                    dir="ltr"
                    value={baseUrl}
                    onChange={(e) => setBaseUrl(e.target.value)}
                    placeholder="https://api.openai.com/v1"
                    className="rounded-control border border-hairline bg-surface px-3 py-2 text-left text-code text-ink outline-none placeholder:text-muted-soft"
                  />
                  <input
                    dir="ltr"
                    value={model}
                    onChange={(e) => setModel(e.target.value)}
                    placeholder="gpt-4o-mini"
                    className="rounded-control border border-hairline bg-surface px-3 py-2 text-left text-code text-ink outline-none placeholder:text-muted-soft"
                  />
                </div>
                <input
                  dir="ltr"
                  type="password"
                  value={apiKey}
                  onChange={(e) => setApiKey(e.target.value)}
                  placeholder={settings?.provider ? 'کلیدِ فعلی ذخیره است — برای تغییر بنویسید' : 'API key'}
                  className="mt-2 w-full rounded-control border border-hairline bg-surface px-3 py-2 text-left text-code text-ink outline-none placeholder:text-muted-soft"
                />

                <button
                  onClick={runTest}
                  className="mt-3 rounded-control border border-hairline px-3 py-2 text-button text-body transition-colors hover:bg-surface hover:text-ink"
                >
                  تستِ اتصال
                </button>
                {test && (
                  <p
                    className="mt-2 text-body-sm"
                    style={{ color: test.ok ? 'var(--color-success)' : 'var(--color-error)' }}
                  >
                    {test.message}
                  </p>
                )}
              </section>
            </div>

            <div className="flex items-center justify-between border-t border-hairline px-6 py-4">
              <p className="text-body-sm text-muted">
                {settings?.provider ? 'مدل ذخیره شده است' : 'هنوز مدلی ذخیره نشده'}
              </p>
              <div className="flex gap-2">
                <button
                  onClick={onClose}
                  className="rounded-control border border-hairline px-4 py-2 text-button text-body transition-colors hover:bg-surface hover:text-ink"
                >
                  انصراف
                </button>
                <button
                  onClick={save}
                  disabled={saving}
                  className="rounded-control px-4 py-2 text-button text-ink transition-opacity hover:opacity-90 disabled:opacity-50"
                  style={{ backgroundColor: 'var(--color-brand)' }}
                >
                  {saving ? 'در حال ذخیره…' : 'ذخیره'}
                </button>
              </div>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  )
}
