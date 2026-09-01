import { AnimatePresence, motion } from 'motion/react'
import type { Message, Stage } from '../lib/types.ts'
import StagePill from './StagePill.tsx'

export interface TraceEntry {
  stage: Stage
  text?: string
}

interface Props {
  messages: Message[]
  trace: TraceEntry[]
  busy: boolean
  skills: string[]
}

/** نمایشِ متن با پشتیبانیِ ابتدایی از بلوک کد (JetBrains Mono طبق DESIGN.md) */
function Formatted({ text }: { text: string }) {
  const parts = text.split(/(```[\s\S]*?```)/g)
  return (
    <>
      {parts.map((part, i) => {
        if (part.startsWith('```')) {
          const body = part.replace(/^```[a-z]*\n?/, '').replace(/```$/, '')
          return (
            <pre
              key={i}
              dir="ltr"
              className="my-3 overflow-x-auto rounded-md border border-hairline bg-canvas p-3 text-left font-mono text-[13px] leading-relaxed text-body"
            >
              <code>{body}</code>
            </pre>
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

export default function ChatStream({ messages, trace, busy, skills }: Props) {
  return (
    <div className="flex-1 overflow-y-auto px-6 py-5">
      {messages.length === 0 && !busy ? (
        <div className="flex h-full flex-col items-center justify-center text-center">
          <h2 className="text-[26px] leading-tight text-ink">Forge</h2>
          <p className="mt-2 max-w-md text-[14px] text-muted">
            سه ابزار در یک پنجره: Jcode برای اجرا، Godmode برای گردش‌کار، Soup برای
            انتخابِ مهارت. وضعیتِ هر کدام در بالای صفحه است.
          </p>
        </div>
      ) : null}

      <div className="mx-auto max-w-3xl space-y-4">
        {messages.map((m) => (
          <motion.div
            key={m.id}
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.26, ease: [0.16, 1, 0.3, 1] }}
            className={
              m.role === 'user'
                ? 'rounded-md border border-hairline bg-surface px-4 py-3 text-[15px] text-ink'
                : 'rounded-md border border-hairline-strong bg-canvas-soft px-4 py-3 text-[14px] leading-relaxed text-body'
            }
          >
            {m.role !== 'user' && (
              <span className="mb-1 block text-[11px] font-semibold uppercase tracking-[0.88px] text-muted">
                {m.role === 'agent' ? 'عامل' : 'سیستم'}
              </span>
            )}
            <Formatted text={m.text} />
          </motion.div>
        ))}

        <AnimatePresence>
          {trace.length > 0 && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="flex flex-wrap gap-2 pt-1"
            >
              {trace.map((t, i) => (
                <StagePill key={`${t.stage}-${i}`} stage={t.stage} text={t.text} />
              ))}
            </motion.div>
          )}
        </AnimatePresence>

        {skills.length > 0 && !busy && (
          <div className="flex flex-wrap items-center gap-2 pt-1">
            <span className="text-[11px] uppercase tracking-[0.88px] text-muted">مهارت‌ها</span>
            {skills.map((s) => (
              <span
                key={s}
                className="rounded-full border border-hairline-strong px-2.5 py-1 font-mono text-[11px] text-body"
              >
                {s}
              </span>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
