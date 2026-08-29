import { motion, useReducedMotion } from 'framer-motion';
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
}: MotionButtonProps) {
  const reduced = useReducedMotion() ?? false;
  const busy = state === 'loading';
  const isDisabled = disabled || busy;

  return (
    <motion.button
      type="button"
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
      style={{
        background: BACKGROUND[variant],
        color: FOREGROUND[variant],
        border:
          variant === 'ghost' ? '1px solid var(--color-border-subtle)' : 'none',
        borderRadius: 'var(--radius-sm)',
        minHeight: 44, // MASTER.md: touch target >= 44px
        padding: '12px 22px',
        fontFamily: 'var(--font-body)',
        fontSize: 15,
        fontWeight: 600,
        cursor: isDisabled ? 'not-allowed' : 'pointer',
        opacity: isDisabled ? 0.7 : 1,
      }}
    >
      {busy ? (
        <span className="mp-btn-spinner" aria-hidden>
          <motion.span
            animate={{ opacity: [0.3, 1, 0.3] }}
            transition={{ duration: 1, repeat: Infinity }}
          >
            ●●●
          </motion.span>
        </span>
      ) : (
        children
      )}
      {state === 'error' && (
        <motion.span
          role="alert"
          animate={reduced ? { x: 0 } : { x: [0, -6, 6, -4, 4, 0] }}
          transition={{ duration: reduced ? 0 : durations.slow }}
          style={{ marginInlineStart: 8 }}
        >
          {STATE_LABEL.error}
        </motion.span>
      )}
    </motion.button>
  );
}
