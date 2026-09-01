import { useEffect, useState } from 'react'
import { motion } from 'motion/react'
import { api } from '../lib/api.ts'
import type { Command, McpServer, Usage } from '../lib/types.ts'

type Tab = 'route' | 'commands' | 'mcp' | 'usage'

const TABS: Array<{ id: Tab; label: string }> = [
  { id: 'route', label: 'مهارت‌ها' },
  { id: 'commands', label: 'دستورها' },
  { id: 'mcp', label: 'MCP' },
  { id: 'usage', label: 'مصرف' },
]

interface Props {
  query: string
  commands: Command[]
  onPickCommand: (slug: string) => void
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
        {TABS.map((t) => (
          <button
            key={t.id}
            onClick={() => setTab(t.id)}
            className={`flex-1 border-b-2 px-2 py-3 text-[12px] transition-colors ${
              tab === t.id
                ? 'border-brand text-ink'
                : 'border-transparent text-muted hover:text-body'
            }`}
          >
            {t.label}
          </button>
        ))}
      </div>

      <div className="flex-1 overflow-y-auto p-3">
        {tab === 'route' && (
          <div className="space-y-2">
            <p className="text-[11px] leading-relaxed text-muted">
              لایهٔ Soup برای این عبارت کدام مهارت‌ها را انتخاب می‌کند.
            </p>
            {route.length === 0 ? (
              <p className="py-6 text-center text-[12px] text-muted-soft">
                متنی بنویسید تا مسیریابی نمایش داده شود
              </p>
            ) : (
              route.map((r) => (
                <motion.div
                  key={r.name}
                  initial={{ opacity: 0, x: 6 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.2, ease: [0.16, 1, 0.3, 1] }}
                  className="flex items-center justify-between rounded-md border border-hairline bg-surface px-3 py-2"
                >
                  <span className="font-mono text-[13px] text-ink">{r.name}</span>
                  <span className="font-mono text-[11px] text-muted">{r.score}</span>
                </motion.div>
              ))
            )}
          </div>
        )}

        {tab === 'commands' && (
          <ul className="space-y-1">
            {commands.map((c) => (
              <li key={c.slug}>
                <button
                  onClick={() => onPickCommand(c.slug)}
                  className="w-full rounded-md border border-transparent px-3 py-2 text-right transition-colors hover:border-hairline hover:bg-surface"
                >
                  <span className="block font-mono text-[13px] text-ink">/{c.slug}</span>
                  <span className="mt-0.5 block text-[12px] leading-relaxed text-muted">
                    {c.description}
                  </span>
                </button>
              </li>
            ))}
          </ul>
        )}

        {tab === 'mcp' && (
          <ul className="space-y-1">
            {mcp.map((s) => (
              <li
                key={s.id}
                className="rounded-md border border-hairline bg-surface px-3 py-2"
              >
                <div className="flex items-center justify-between">
                  <span className="text-[13px] text-ink">{s.name}</span>
                  <span className="rounded-full border border-hairline-strong px-2 py-0.5 text-[10px] text-muted">
                    {s.category}
                  </span>
                </div>
                <p className="mt-1 text-[11px] leading-relaxed text-muted">{s.what}</p>
              </li>
            ))}
          </ul>
        )}

        {tab === 'usage' && (
          <div className="space-y-3">
            <Row label="اجراها" value={String(usage?.runs ?? 0)} />
            <Row label="توکنِ ورودی" value={String(usage?.promptTokens ?? 0)} />
            <Row label="توکنِ خروجی" value={String(usage?.completionTokens ?? 0)} />
            <p className="pt-2 text-[11px] leading-relaxed text-muted">
              هزینهٔ مالی نمایش داده نمی‌شود چون Forge خودش با provider تماس نمی‌گیرد؛
              اعداد مربوط به مصرفِ واقعی پس از اتصالِ هستهٔ اجرا معنا پیدا می‌کنند.
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
      <span className="text-[13px] text-body">{label}</span>
      <span className="font-mono text-[13px] text-ink">{value}</span>
    </div>
  )
}
