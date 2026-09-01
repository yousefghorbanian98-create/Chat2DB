import { useEffect, useState } from 'react'
import { motion } from 'motion/react'
import Icon, { type IconName } from './Icon.tsx'
import { api } from '../lib/api.ts'
import type { Command, McpServer, Usage } from '../lib/types.ts'

type Tab = 'route' | 'commands' | 'mcp' | 'usage'

const TABS: Array<{ id: Tab; label: string; icon: IconName }> = [
  { id: 'route', label: 'مهارت‌ها', icon: 'search' },
  { id: 'commands', label: 'دستورها', icon: 'sparkles' },
  { id: 'mcp', label: 'MCP', icon: 'plug' },
  { id: 'usage', label: 'مصرف', icon: 'clock' },
]

interface Props {
  query: string
  commands: Command[]
  onPickCommand: (slug: string) => void
}

function Empty({ icon, text }: { icon: IconName; text: string }) {
  return (
    <div className="flex flex-col items-center gap-2 py-10 text-center">
      <span className="text-muted">
        <Icon name={icon} size={20} />
      </span>
      <p className="text-body-sm text-muted-soft">{text}</p>
    </div>
  )
}

export default function SidePanel({ query, commands, onPickCommand }: Props) {
  const [tab, setTab] = useState<Tab>('route')
  const [route, setRoute] = useState<Array<{ name: string; score: number }>>([])
  const [mcp, setMcp] = useState<Array<McpServer & { enabled: boolean }>>([])
  const [usage, setUsage] = useState<Usage | null>(null)

  useEffect(() => {
    if (tab === 'mcp') api.mcp().then(setMcp).catch(() => setMcp([]))
    if (tab === 'usage') api.usage().then(setUsage).catch(() => setUsage(null))
  }, [tab])

  useEffect(() => {
    if (tab !== 'route') return
    if (!query.trim()) {
      setRoute([])
      return
    }
    const id = setTimeout(() => {
      api.route(query).then(setRoute).catch(() => setRoute([]))
    }, 180)
    return () => clearTimeout(id)
  }, [query, tab])

  return (
    <aside className="flex h-full w-[360px] shrink-0 flex-col border-r border-hairline bg-canvas-soft">
      <div className="flex border-b border-hairline">
        {TABS.map((t) => {
          const active = tab === t.id
          return (
            <button
              key={t.id}
              onClick={() => setTab(t.id)}
              className={`relative flex flex-1 flex-col items-center gap-1 px-2 py-2.5 text-nav transition-colors ${
                active ? 'text-ink' : 'text-muted hover:text-body'
              }`}
            >
              <Icon name={t.icon} size={16} />
              {t.label}
              {active && (
                <motion.span
                  layoutId="side-tab"
                  className="absolute inset-x-3 -bottom-px h-0.5 rounded-full"
                  style={{ backgroundColor: 'var(--color-brand)' }}
                  transition={{ duration: 0.24, ease: [0.16, 1, 0.3, 1] }}
                />
              )}
            </button>
          )
        })}
      </div>

      <div className="flex-1 overflow-y-auto p-3">
        {tab === 'route' && (
          <div className="space-y-2">
            <p className="text-body-sm leading-relaxed text-muted">
              لایه‌ی مهارت برای این عبارت کدام گزینه را انتخاب می‌کند — هرچه امتیاز
              بالاتر، ارتباط بیشتر.
            </p>
            {route.length === 0 ? (
              <Empty icon="search" text="متنی بنویسید تا مسیریابی نمایش داده شود" />
            ) : (
              route.map((r, i) => (
                <motion.div
                  key={r.name}
                  initial={{ opacity: 0, x: 6 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.2, delay: 0.02 * i, ease: [0.16, 1, 0.3, 1] }}
                  className="rounded-md border border-hairline bg-surface px-3 py-2"
                >
                  <div className="flex items-center justify-between gap-2">
                    <span className="text-code text-ink">{r.name}</span>
                    <span className="text-code text-muted">{r.score}</span>
                  </div>
                  {/* نوارِ امتیاز — بدون سایه، فقط تضادِ سطح */}
                  <div className="mt-2 h-1 overflow-hidden rounded-full bg-canvas">
                    <motion.div
                      initial={{ width: 0 }}
                      animate={{ width: `${Math.min(100, (r.score / 8) * 100)}%` }}
                      transition={{ duration: 0.4, ease: [0.16, 1, 0.3, 1] }}
                      className="h-full rounded-full"
                      style={{ backgroundColor: 'var(--color-brand)' }}
                    />
                  </div>
                </motion.div>
              ))
            )}
          </div>
        )}

        {tab === 'commands' && (
          <ul className="space-y-0.5">
            {commands.length === 0 && <Empty icon="sparkles" text="فرمانی بار نشده است" />}
            {commands.map((c) => (
              <li key={c.slug}>
                <button
                  onClick={() => onPickCommand(c.slug)}
                  className="w-full rounded-md border border-transparent px-3 py-2 text-right transition-colors hover:border-hairline hover:bg-surface"
                >
                  <span className="block text-code text-ink">/{c.slug}</span>
                  <span className="mt-0.5 block text-body-sm leading-relaxed text-muted">
                    {c.description}
                  </span>
                </button>
              </li>
            ))}
          </ul>
        )}

        {tab === 'mcp' && (
          <ul className="space-y-1">
            {mcp.length === 0 && <Empty icon="plug" text="سروری تعریف نشده است" />}
            {mcp.map((s) => (
              <li key={s.id} className="rounded-md border border-hairline bg-surface px-3 py-2">
                <div className="flex items-center justify-between gap-2">
                  <span className="text-body-sm text-ink">{s.name}</span>
                  <span className="rounded-full border border-hairline-strong px-2 py-0.5 text-caption text-muted">
                    {s.category}
                  </span>
                </div>
                <p className="mt-1 text-body-sm leading-relaxed text-muted">{s.what}</p>
              </li>
            ))}
          </ul>
        )}

        {tab === 'usage' && (
          <div className="space-y-2">
            <Row label="اجراها" value={String(usage?.runs ?? 0)} />
            <Row label="توکنِ ورودی" value={String(usage?.promptTokens ?? 0)} />
            <Row label="توکنِ خروجی" value={String(usage?.completionTokens ?? 0)} />
            <p className="pt-2 text-body-sm leading-relaxed text-muted">
              هزینه‌ی مالی نمایش داده نمی‌شود چون Forge خودش با provider تماس نمی‌گیرد؛
              این اعداد پس از اتصالِ هسته‌ی اجرا معنا پیدا می‌کنند.
            </p>
          </div>
        )}
      </div>
    </aside>
  )
}

function Row({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex items-center justify-between rounded-md border border-hairline bg-surface px-3 py-2">
      <span className="text-body-sm text-body">{label}</span>
      <span className="text-code text-ink">{value}</span>
    </div>
  )
}
