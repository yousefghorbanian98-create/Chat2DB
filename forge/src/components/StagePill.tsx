import { motion } from 'motion/react'
import type { Stage } from '../lib/types.ts'
import { STAGE_TOKEN } from '../lib/types.ts'

/**
 * قرصِ مرحله — امضای بصریِ DESIGN.md.
 * این پنج رنگ فقط برای مراحلِ اجرای عامل استفاده می‌شوند
 * و هرگز به‌عنوان رنگِ عملیاتیِ سیستم به کار نمی‌روند.
 */
export default function StagePill({ stage, text }: { stage: Stage; text?: string }) {
  const token = STAGE_TOKEN[stage]

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.96, y: 2 }}
      animate={{ opacity: 1, scale: 1, y: 0 }}
      transition={{ duration: 0.2, ease: [0.16, 1, 0.3, 1] }}
      className="inline-flex items-center gap-2 rounded-full border px-3 py-1 text-[11px] leading-none"
      style={{
        borderColor: `color-mix(in oklab, var(--color-${token}) 35%, transparent)`,
        backgroundColor: `color-mix(in oklab, var(--color-${token}) 12%, transparent)`,
        color: `var(--color-${token})`,
      }}
    >
      <span
        className="size-1.5 rounded-full"
        style={{ backgroundColor: `var(--color-${token})` }}
      />
      <span className="font-medium">{stage}</span>
      {text ? <span className="opacity-80">{text}</span> : null}
    </motion.div>
  )
}
