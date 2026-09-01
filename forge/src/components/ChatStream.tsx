import { useState } from 'react'
import { AnimatePresence, motion } from 'motion/react'
import Icon from './Icon.tsx'
import StagePill from './StagePill.tsx'
import type { Message } from '../lib/types.ts'

export interface TraceEntry {
  stage: Message['stage'] & string
  text?: string
}

interface Props {
  messages: Message[]
  trace: TraceEntry[]
  busy: boolean
  skills: string[]
}

/** نمایشِ متن با پشتیبانی از بلوک کد (JetBrains Mono طبق DESIGN.md) */
function Formatted({ text }: { text: string }) {
  const parts = text.split(/(```[\s\S]*?```)/g)
  return (
    <>
      {parts.map((part, i) => {
        if (part.startsWith('```')) {
          const lang = part.match(/^```([a-z]*)/)?.[1] ?? ''
          const body = part.replace(/^```[a-z]*\n?/, '').replace(/```$/, '')
          return (
            <CodeBlock key={i} code={body} lang={lang} />
          )
        }
        return (
          <span key={i} className="whitespace-pre-wrap">
            {part}
          </span>
        )
      })}
    </>
  )
}

function CodeBlock({ code, lang }: { code: string; lang: string }) {
  const [copied, setCopied] = useState(false)
  return (
    <div className="my-3 overflow-hidden rounded-lg border border-hairline bg-canvas">
      <div className="flex items-center justify-between border-b border-hairline px-3 py-1.5">
        <span className="text-caption text-muted">{lang || 'کد'}</span>
        <button
          onClick={() => {
            navigator.clipboard?.writeText(code).then(() => {
              setCopied(true)
              setTimeout(() => setCopied(false), 1400)
            })
          }}
          className="flex items-center gap-1 text-caption text-muted transition-colors hover:text-ink"
        >
          <Icon name={copied ? 'check' : 'copy'} size={13} />
          {copied ? 'کپی شد' : 'کپی'}
        </button>
      </div>
      <pre dir="ltr" className="overflow-x-auto p-3 text-left text-code text-body">
        <code>{code}</code>
      </pre>
    </div>
  )
}

function Avatar({ role }: { role: Message['role'] }) {
  const map = {
    user: { icon: 'message' as const, token: 'brand' },
    agent: { icon: 'terminal' as const, token: 'muted' },
    system: { icon: 'alert' as const, token: 'muted-soft' },
  }
  const m = map[role]
  return (
    <span
      className="flex size-7 shrink-0 items-center justify-center rounded-chip border border-hairline bg-surface-strong"
      style={{ color: `var(--color-${m.token})` }}
    >
      <Icon name={m.icon} size={15} />
    </span>
  )
}

export default function ChatStream({ messages, trace, busy, skills }: Props) {
  return (
    <div className="flex-1 overflow-y-auto px-6 py-6">
      <div className="mx-auto max-w-3xl">
        {messages.map((m) => (
          <motion.div
            key={m.id}
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.32, ease: [0.16, 1, 0.3, 1] }}
            className="py-2"
          >
            <div
              className={
                m.role === 'user'
                  ? 'rounded-card border border-hairline bg-surface-strong p-5'
                  : 'rounded-card border border-hairline bg-surface p-5'
              }
            >
              <div className="mb-3 flex items-center gap-2">
                <Avatar role={m.role} />
                <span className="text-caption text-muted">
                  {m.role === 'user' ? 'شما' : m.role === 'agent' ? 'عامل' : 'سیستم'}
                </span>
                <span className="text-caption text-muted-soft">
                  {new Date(m.at).toLocaleTimeString('fa-IR', {
                    hour: '2-digit',
                    minute: '2-digit',
                  })}
                </span>
              </div>
              <div
                className={
                  m.role === 'user'
                    ? 'text-body-md text-ink'
                    : 'text-body-md leading-relaxed text-body'
                }
              >
                <Formatted text={m.text} />
              </div>
            </div>
          </motion.div>
        ))}

        {/* ردیفِ مراحل: خطِ زمانیِ عمودی با پاستیل‌های DESIGN.md */}
        <AnimatePresence>
          {(busy || trace.length > 0) && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="py-2"
            >
              <div className="rounded-card border border-hairline bg-surface p-5">
                <div className="mb-3 flex items-center gap-2">
                  <span className="flex size-7 shrink-0 items-center justify-center rounded-chip border border-hairline bg-surface-strong">
                    <span className="flex items-center gap-0.5">
                      {[0, 1, 2].map((i) => (
                        <span
                          key={i}
                          className="size-1.5 animate-forge-pulse rounded-full"
                          style={{
                            backgroundColor: 'var(--color-brand)',
                            animationDelay: `${i * 0.16}s`,
                          }}
                        />
                      ))}
                    </span>
                  </span>
                  <span className="text-caption text-muted">مراحلِ اجرا</span>
                </div>
                <div className="flex flex-wrap items-center gap-2">
                  {trace.map((t, i) => (
                    <StagePill key={`${t.stage}-${i}`} stage={t.stage} text={t.text} />
                  ))}
                  {busy && trace.length === 0 && (
                    <span className="text-body-sm text-muted">در حال آماده‌سازی…</span>
                  )}
                </div>

                {skills.length > 0 && (
                  <div className="mt-3 flex flex-wrap items-center gap-2 border-t border-hairline pt-3">
                    <span className="text-caption text-muted">مهارت‌ها</span>
                    {skills.map((s) => (
                      <span
                        key={s}
                        className="rounded-full border border-hairline-strong px-2.5 py-1 text-code text-body"
                      >
                        {s}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  )
}
