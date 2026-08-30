import { motion, useReducedMotion, type MotionStyle } from 'framer-motion';
import { useEffect, type CSSProperties } from 'react';

import { durations, springs } from '../motion/presets';

// Framer wants bezier control points as a tuple, not a CSS string.
const EXPO: [number, number, number, number] = [0.16, 1, 0.3, 1];
const QUART: [number, number, number, number] = [0.76, 0, 0.24, 1];
const DECEL: [number, number, number, number] = [0, 0.7, 0.1, 1];

const WRAP: MotionStyle = {
  position: 'fixed',
  inset: 0,
  background: 'var(--color-background)',
  overflow: 'hidden',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  cursor: 'pointer',
};
const GLOW: MotionStyle = { position: 'absolute', borderRadius: '50%', filter: 'blur(90px)' };
const STACK: CSSProperties = {
  position: 'relative',
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  gap: 'var(--space-lg)',
  padding: 'var(--space-3xl)',
};
const TITLE: CSSProperties = {
  display: 'flex',
  margin: 0,
  fontSize: 'clamp(40px, 8vw, 84px)',
  fontWeight: 800,
  letterSpacing: '0.02em',
  color: 'var(--color-foreground)',
};
const BAR: CSSProperties = {
  width: 220,
  height: 3,
  borderRadius: 2,
  background: 'var(--color-muted)',
  overflow: 'hidden',
};

const NAME = 'MUSCLE PARADISE';

/** Two slow-breathing brand glows (transform/opacity only — perf watchdog). */
function Glows() {
  return (
    <>
      <motion.div
        style={{
          ...GLOW,
          width: 480,
          height: 480,
          top: '-12%',
          right: '-8%',
          background: 'var(--color-primary)',
        }}
        initial={{ opacity: 0.1, scale: 0.9 }}
        animate={{ opacity: [0.14, 0.24, 0.14], scale: [0.9, 1.08, 0.9] }}
        transition={{ duration: 6, repeat: Infinity, ease: 'easeInOut' }}
      />
      <motion.div
        style={{
          ...GLOW,
          width: 380,
          height: 380,
          bottom: '-14%',
          left: '-6%',
          background: 'var(--color-secondary)',
        }}
        initial={{ opacity: 0.06, scale: 1 }}
        animate={{ opacity: [0.08, 0.16, 0.08], scale: [1, 1.12, 1] }}
        transition={{ duration: 7, repeat: Infinity, ease: 'easeInOut', delay: 0.6 }}
      />
    </>
  );
}

/** The MP monogram draws itself in with a spring. */
function Mark() {
  return (
    <motion.svg
      width="120"
      height="120"
      viewBox="0 0 120 120"
      initial={{ scale: 0.6, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      transition={springs.bouncy}
      data-testid="landing-mark"
    >
      <motion.circle
        cx="60"
        cy="60"
        r="54"
        fill="none"
        stroke="var(--color-primary)"
        strokeWidth="3"
        initial={{ pathLength: 0 }}
        animate={{ pathLength: 1 }}
        transition={{ duration: durations.dramatic, ease: EXPO }}
      />
      <motion.path
        d="M34 78 V44 L48 66 L62 44 V78"
        fill="none"
        stroke="var(--color-foreground)"
        strokeWidth="6"
        strokeLinecap="round"
        strokeLinejoin="round"
        initial={{ pathLength: 0 }}
        animate={{ pathLength: 1 }}
        transition={{ duration: durations.cinematic, ease: QUART, delay: 0.25 }}
      />
      <motion.path
        d="M74 44 h14 M81 44 v34"
        fill="none"
        stroke="var(--color-secondary)"
        strokeWidth="6"
        strokeLinecap="round"
        initial={{ pathLength: 0 }}
        animate={{ pathLength: 1 }}
        transition={{ duration: durations.slow, ease: EXPO, delay: 0.6 }}
      />
    </motion.svg>
  );
}

/** Staggered letter reveal for the wordmark. */
function Wordmark() {
  return (
    <h1 style={TITLE} aria-label={NAME} data-testid="landing-title">
      {NAME.split('').map((ch, i) => (
        <motion.span
          key={i}
          style={{ display: 'inline-block', whiteSpace: 'pre' }}
          initial={{ opacity: 0, y: 28, filter: 'blur(6px)' }}
          animate={{ opacity: 1, y: 0, filter: 'blur(0px)' }}
          transition={{ ...springs.smooth, delay: 0.5 + i * 0.045 }}
        >
          {ch}
        </motion.span>
      ))}
    </h1>
  );
}

/**
 * Cinematic entrance — the one place FINN-LOOP's full motion bar is allowed.
 *
 * Data surfaces stay on MASTER.md's calm dial; this splash is the celebration.
 * Reduced-motion users get a static mark + title and a quick hand-off.
 */
export function Landing({ onDone }: { onDone: () => void }) {
  const reduced = useReducedMotion();

  useEffect(() => {
    const t = window.setTimeout(onDone, reduced ? 600 : 3200);
    return () => window.clearTimeout(t);
  }, [onDone, reduced]);

  return (
    <motion.div
      style={WRAP}
      onClick={onDone}
      data-testid="landing"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
    >
      {reduced ? null : <Glows />}
      <div style={STACK}>
        <Mark />
        <Wordmark />
        <motion.p
          style={{ color: 'var(--color-muted-foreground)', margin: 0, fontSize: 18 }}
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1.2, ease: EXPO, duration: durations.medium }}
        >
          سیستم‌عامل باشگاه — قدرتمند، دقیق، شخصی
        </motion.p>
        <div style={BAR}>
          <motion.div
            style={
              {
                height: '100%',
                background: 'var(--color-accent)',
                transformOrigin: 'left',
              } as MotionStyle
            }
            initial={{ scaleX: 0 }}
            animate={{ scaleX: 1 }}
            transition={{ duration: reduced ? 0.2 : 2.6, ease: DECEL }}
          />
        </div>
      </div>
    </motion.div>
  );
}

export default Landing;
