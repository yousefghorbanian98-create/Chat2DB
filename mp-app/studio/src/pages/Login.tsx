import { motion, useReducedMotion } from 'framer-motion';
import { useState, type FormEvent } from 'react';

import { ApiError } from '../api/client';
import { MotionButton } from '../components/MotionButton';
import { springs } from '../motion/presets';
import { useAuth } from '../auth/AuthContext';

/**
 * Staff PIN login (map §2.3 Kiosk-style minimalism + §15 security).
 * Never tells the user *which* of username/PIN was wrong.
 */
export function Login() {
  const { login } = useAuth();
  const reduced = useReducedMotion() ?? false;

  const [username, setUsername] = useState('');
  const [pin, setPin] = useState('');
  const [phase, setPhase] = useState<'idle' | 'loading' | 'error'>('idle');
  const [error, setError] = useState<string | null>(null);

  async function submit(e: FormEvent) {
    e.preventDefault();
    if (!username.trim() || !pin) {
      setError('نام کاربری و پین را وارد کنید');
      setPhase('error');
      return;
    }
    setPhase('loading');
    try {
      await login(username.trim(), pin);
    } catch (err) {
      setPhase('error');
      setError(err instanceof ApiError && err.status === 401
        ? 'نام کاربری یا پین نادرست است'
        : 'ارتباط با هستهٔ محلی برقرار نشد — دوباره تلاش کنید');
    }
  }

  const inputStyle = {
    width: '100%',
    background: '#0A1218',
    border: '1px solid var(--color-border-subtle)',
    color: 'var(--color-foreground)',
    padding: '12px 14px',
    borderRadius: 8,
    fontSize: 16,
    outline: 'none',
  } as const;

  return (
    <motion.main
      initial={reduced ? false : { opacity: 0, scale: 0.96 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={springs.smooth}
      style={{
        minHeight: '100%',
        display: 'grid',
        placeItems: 'center',
        padding: 'var(--space-2xl)',
      }}
    >
      <form
        onSubmit={submit}
        className="glass"
        style={{
          width: 'min(400px, 100%)',
          padding: 'var(--space-3xl)',
          display: 'flex',
          flexDirection: 'column',
          gap: 'var(--space-lg)',
        }}
      >
        <div style={{ textAlign: 'center', marginBottom: 'var(--space-md)' }}>
          <h1 style={{ fontSize: 30 }}>
            Muscle Paradise <span style={{ color: 'var(--color-primary)' }}>Studio</span>
          </h1>
          <p style={{ color: 'var(--color-muted-foreground)', margin: '4px 0 0' }}>
            ورود کارکنان — پین
          </p>
        </div>

        <label style={{ display: 'flex', flexDirection: 'column', gap: 6, fontSize: 13, color: 'var(--color-muted-foreground)' }}>
          نام کاربری
          <input
            style={inputStyle}
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            autoComplete="username"
          />
        </label>

        <label style={{ display: 'flex', flexDirection: 'column', gap: 6, fontSize: 13, color: 'var(--color-muted-foreground)' }}>
          پین
          <input
            className="numeric"
            style={inputStyle}
            type="password"
            inputMode="numeric"
            value={pin}
            onChange={(e) => setPin(e.target.value)}
            autoComplete="current-password"
          />
        </label>

        {error ? (
          <motion.p
            role="alert"
            animate={reduced ? { x: 0 } : { x: [0, -8, 8, -6, 6, -3, 3, 0] }}
            transition={{ duration: reduced ? 0 : 0.5 }}
            style={{ color: 'var(--color-destructive)', fontSize: 13, margin: 0 }}
          >
            {error}
          </motion.p>
        ) : null}

        <MotionButton type="submit" state={phase === 'loading' ? 'loading' : 'idle'}>
          ورود
        </MotionButton>
      </form>
    </motion.main>
  );
}
