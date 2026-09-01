import { motion } from 'motion/react'
import Icon from './Icon.tsx'
import type { HealthResponse } from '../lib/api.ts'
import type { HealthState } from '../lib/types.ts'

const STATE_STYLE: Record<
  HealthState,
  { label: string; token: string; icon: 'check' | 'alert' | 'close' }
> = {
  ready: { label: 'آماده', token: 'success', icon: 'check' },
  degraded: { label: 'ناقص', token: 'done', icon: 'alert' },
  missing: { label: 'غایب', token: 'muted', icon: 'close' },
}

interface Props {
  health: HealthResponse | null
  onOpenSetup?: () => void
}

export default function StatusPills({ health, onOpenSetup }: Props) {
  if (!health) return null

  return (
    <div className="flex flex-wrap items-center gap-1.5">
      {health.adapters.map((a, i) => {
        const style = STATE_STYLE[a.state]
        return (
          <motion.button
            key={a.name}
            type="button"
            onClick={onOpenSetup}
            title={`${a.detail} — برای راهنما کلیک کنید`}
            initial={{ opacity: 0, y: -4 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.22, delay: 0.03 * i, ease: [0.16, 1, 0.3, 1] }}
            className="flex items-center gap-1.5 rounded-md border border-hairline bg-surface px-2 py-1 transition-colors hover:border-hairline-strong hover:bg-surface-strong"
          >
            <span style={{ color: `var(--color-${style.token})` }}>
              <Icon name={style.icon} size={13} />
            </span>
            <span className="text-code text-body">{a.name}</span>
            <span className="text-caption text-muted">{style.label}</span>
          </motion.button>
        )
      })}
    </div>
  )
}
