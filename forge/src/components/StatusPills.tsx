import { motion } from 'motion/react'
import type { HealthResponse } from '../lib/api.ts'
import type { HealthState } from '../lib/types.ts'

const STATE_STYLE: Record<HealthState, { label: string; token: string }> = {
  ready: { label: 'آماده', token: 'success' },
  degraded: { label: 'ناقص', token: 'done' },
  missing: { label: 'غایب', token: 'muted' },
}

export default function StatusPills({ health }: { health: HealthResponse | null }) {
  if (!health) return null

  return (
    <div className="flex flex-wrap items-center gap-2">
      {health.adapters.map((a) => {
        const style = STATE_STYLE[a.state]
        return (
          <motion.div
            key={a.name}
            initial={{ opacity: 0, y: -4 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.22, ease: [0.16, 1, 0.3, 1] }}
            title={a.detail}
            className="flex items-center gap-2 rounded-md border border-hairline bg-surface px-2 py-1"
          >
            <span
              className="size-2 rounded-full"
              style={{ backgroundColor: `var(--color-${style.token})` }}
            />
            <span className="font-mono text-[11px] text-body">{a.name}</span>
            <span className="text-[11px] text-muted">{style.label}</span>
          </motion.div>
        )
      })}
    </div>
  )
}
