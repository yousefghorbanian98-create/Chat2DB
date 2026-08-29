import { motion, useReducedMotion, type MotionStyle } from 'framer-motion';
import type { ReactNode } from 'react';

import { buttonVariants, durations, springs } from '../motion/presets';

export type ButtonVariant = 'primary' | 'ghost' | 'danger';
export type ButtonState = 'idle' | 'loading' | 'success' | 'error';

interface MotionButtonProps {
  children: ReactNode;
  onClick?: () => void;
  variant?: ButtonVariant;
  state?: ButtonState;
  disabled?: boolean;
  /** Defaults to "button" so an unhandled click never submits a form. */
  type?: 'button' | 'submit';
}

const BACKGROUND: Record<ButtonVariant, string> = {
  primary: 'var(--color-accent)',
  ghost: 'transparent',
  danger: 'var(--color-destructive)',
};

const FOREGROUND: Record<ButtonVariant, string> = {
  primary: 'var(--color-on-accent)',
  ghost: 'var(--color-foreground)',
  danger: '#ffffff',
};

const STATE_LABEL: Record<ButtonState, string> = {
  idle: '',
  loading: 'در حال پردازش…',
  success: 'انجام شد',
  error: 'خطا — تلاش دوباره',
};

/** Hoisted so the JSX stays inside the function budget (no per-render object). */
function buttonStyle(variant: ButtonVariant, isDisabled: boolean): MotionStyle {
  return {
    background: BACKGROUND[variant],
    color: FOREGROUND[variant],
    border: variant === 'ghost' ? '1px solid var(--color-border-subtle)' : 'none',
    borderRadius: 'var(--radius-sm)',
    minHeight: 44, // MASTER.md: touch target >= 44px
    padding: '12px 22px',
    fontFamily: 'var(--font-body)',
    fontSize: 15,
    fontWeight: 600,
    cursor: isDisabled ? 'not-allowed' : 'pointer',
    opacity: isDisabled ? 0.7 : 1,
  };
}

/** Pulsing dots — a blank button while loading is forbidden by the loop. */
function Spinner() {
  return (
    <span className="mp-btn-spinner" aria-hidden>
      <motion.span
        animate={{ opacity: [0.3, 1, 0.3] }}
        transition={{ duration: 1, repeat: Infinity }}
      >
        ●●●
      </motion.span>
    </span>
  );
}

/** Recovery hint with the FINN-LOOP error shake (neutralised for reduced motion). */
function ErrorBadge({ reduced }: { reduced: boolean }) {
  return (
    <motion.span
      role="alert"
      animate={reduced ? { x: 0 } : { x: [0, -6, 6, -4, 4, 0] }}
      transition={{ duration: reduced ? 0 : durations.slow }}
      style={{ marginInlineStart: 8 }}
    >
      {STATE_LABEL.error}
    </motion.span>
  );
}

/**
 * Pressable button with spring feedback and all four MP states.
 *
 * FINN-LOOP: every button needs tap feedback (scale 0.95) and never a blank
 * loading state. Reduced motion is honoured via `useReducedMotion`.
 */
export function MotionButton({
  children,
  onClick,
  variant = 'primary',
  state = 'idle',
  disabled = false,
  type = 'button',
}: MotionButtonProps) {
  const reduced = useReducedMotion() ?? false;
  const busy = state === 'loading';
  const isDisabled = disabled || busy;

  return (
    <motion.button
      type={type}
      className={`mp-btn mp-btn-${variant}`}
      onClick={onClick}
      disabled={isDisabled}
      aria-busy={busy}
      aria-label={state === 'loading' ? STATE_LABEL.loading : undefined}
      initial="rest"
      animate={state === 'success' ? 'success' : 'rest'}
      {...(isDisabled || reduced ? {} : { whileHover: 'hover', whileTap: 'tap' })}
      variants={buttonVariants}
      transition={reduced ? { duration: 0 } : springs.snappy}
      style={buttonStyle(variant, isDisabled)}
    >
      {busy ? <Spinner /> : children}
      {state === 'error' && <ErrorBadge reduced={reduced} />}
    </motion.button>
  );
}
