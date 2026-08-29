import { motion, useReducedMotion } from 'framer-motion';

interface SkeletonProps {
  /** Accessible description of what is loading (never a blank block). */
  label: string;
  width?: number | string;
  height?: number | string;
  radius?: number;
}

/**
 * Premium shimmer skeleton — FINN-LOOP forbids blank loading states.
 * Reduced motion freezes the shimmer instead of removing the affordance.
 */
export function Skeleton({ label, width = '100%', height = 16, radius = 8 }: SkeletonProps) {
  const reduced = useReducedMotion() ?? false;

  return (
    <motion.div
      role="status"
      aria-label={label}
      data-testid="mp-skeleton"
      animate={
        reduced
          ? { backgroundPosition: '0% 0' }
          : { backgroundPosition: ['200% 0', '-200% 0'] }
      }
      transition={
        reduced
          ? { duration: 0 }
          : { duration: 1.8, repeat: Infinity, ease: 'linear' }
      }
      style={{
        width,
        height,
        borderRadius: radius,
        backgroundColor: 'var(--color-skeleton)',
        backgroundImage:
          'linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.08) 50%, transparent 100%)',
        backgroundSize: '200% 100%',
      }}
    />
  );
}
