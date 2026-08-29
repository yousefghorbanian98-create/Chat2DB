import { motion, useReducedMotion } from 'framer-motion';

import { springs } from '../motion/presets';

interface StatCardProps {
  labelFa: string;
  labelEn: string;
  value: string;
  unit?: string;
  tone?: 'primary' | 'gold' | 'default';
}

const COLOR = {
  primary: 'var(--color-accent)',
  gold: 'var(--color-secondary)',
  default: 'var(--color-foreground)',
} as const;

/**
 * Animated count-in stat (FINN-LOOP: "every number change must animate").
 * Value slides/scales in on mount; reduced motion renders it statically.
 */
export function StatCard({ labelFa, labelEn, value, unit, tone = 'default' }: StatCardProps) {
  const reduced = useReducedMotion() ?? false;

  return (
    <motion.div
      initial={reduced ? false : { opacity: 0, y: 14, scale: 0.96 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      transition={springs.smooth}
      style={{
        padding: 'var(--space-lg)',
        borderRadius: 'var(--radius-md)',
        background: 'rgba(10,18,24,0.5)',
        border: '1px solid var(--color-border-subtle)',
        minWidth: 110,
      }}
    >
      <div style={{ fontSize: 12, color: 'var(--color-muted-foreground)' }}>
        {labelFa} <span dir="ltr" style={{ opacity: 0.6 }}>{labelEn}</span>
      </div>
      <div
        className="numeric"
        dir="ltr"
        style={{
          fontSize: 26,
          fontWeight: 700,
          fontFamily: 'var(--font-display)',
          color: COLOR[tone],
          fontVariantNumeric: 'tabular-nums',
        }}
      >
        {value}
        {unit ? <span style={{ fontSize: 14, marginInlineStart: 4 }}>{unit}</span> : null}
      </div>
    </motion.div>
  );
}
