import { motion, useReducedMotion } from 'framer-motion';
import type { ReactNode } from 'react';

import { cardVariants, springs, type MotionMode } from '../motion/presets';

interface MotionCardProps {
  children: ReactNode;
  title?: string;
  mode?: MotionMode;
  /** Launcher tiles animate in; table cells must not (MASTER.md). */
  animateOnMount?: boolean;
  testId?: string;
}

/**
 * Glass card / launcher tile.
 *
 * MASTER.md forbids scaling dense table rows, so `dashboard` mode translates
 * by 2px only; `cinematic` mode (launcher, celebrations) lifts + scales.
 */
export function MotionCard({
  children,
  title,
  mode = 'dashboard',
  animateOnMount = false,
  testId,
}: MotionCardProps) {
  const reduced = useReducedMotion() ?? false;
  const variants = cardVariants(mode);

  return (
    <motion.article
      data-testid={testId}
      className="glass mp-card"
      variants={variants}
      initial={animateOnMount && !reduced ? { opacity: 0, y: 12 } : false}
      animate="rest"
      {...(reduced ? {} : { whileHover: 'hover', whileTap: 'tap' })}
      transition={reduced ? { duration: 0 } : springs.smooth}
      style={{
        padding: 'var(--space-2xl)',
        minHeight: 120,
        cursor: 'pointer',
      }}
    >
      {title ? <h3 style={{ marginBottom: 'var(--space-md)' }}>{title}</h3> : null}
      {children}
    </motion.article>
  );
}
