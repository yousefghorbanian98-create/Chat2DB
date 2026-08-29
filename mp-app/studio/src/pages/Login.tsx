import { motion, useReducedMotion, type MotionStyle } from 'framer-motion';
import type { CSSProperties } from 'react';
import { useState, type FormEvent } from 'react';

import { ApiError } from '../api/client';
import { MotionButton } from '../components/MotionButton';
import { springs } from '../motion/presets';
import { useAuth } from '../auth/useAuth';
import { fieldLabel } from '../styles/blocks';

const PAGE: MotionStyle = {
  minHeight: '100%',
  display: 'grid',
  placeItems: 'center',
  padding: 'var(--space-2xl)',
};
const CARD: CSSProperties = {
  width: 'min(400px, 100%)',
  padding: 'var(--space-3xl)',
  display: 'flex',
  flexDirection: 'column',
  gap: 'var(--space-lg)',
};
const HEAD: CSSProperties = { textAlign: 'center', marginBottom: 'var(--space-md)' };
const SUBHEAD: CSSProperties = { color: 'var(--color-muted-foreground)', margin: '4px 0 0' };
const ERR: MotionStyle = { color: 'var(--color-destructive)', fontSize: 13, margin: 0 };

interface CredentialsProps {
  username: string;
  pin: string;
  onUsername: (v: string) => void;
  onPin: (v: string) => void;
}

/** Username + PIN pair. Kept together because they submit as one unit. */
function Credentials({ username, pin, onUsername, onPin }: CredentialsProps) {
  return (
    <>
      <label style={fieldLabel}>
        نام کاربری
        <input
          className="mp-input"
          value={username}
          onChange={(e) => onUsername(e.target.value)}
          autoComplete="username"
        />
      </label>

      <label style={fieldLabel}>
        پین
        <input
          className="mp-input numeric"
          type="password"
          inputMode="numeric"
          value={pin}
          onChange={(e) => onPin(e.target.value)}
          autoComplete="current-password"
        />
      </label>
    </>
  );
}

/** Studio wordmark above the form. */
function BrandHeader() {
  return (
    <div style={HEAD}>
      <h1 style={{ fontSize: 30 }}>
        Muscle Paradise <span style={{ color: 'var(--color-primary)' }}>Studio</span>
      </h1>
      <p style={SUBHEAD}>ورود کارکنان — پین</p>
    </div>
  );
}

/** Shaken alert — a login failure must never be silent. */
function LoginError({ message, reduced }: { message: string; reduced: boolean }) {
  return (
    <motion.p
      role="alert"
      animate={reduced ? { x: 0 } : { x: [0, -8, 8, -6, 6, -3, 3, 0] }}
      transition={{ duration: reduced ? 0 : 0.5 }}
      style={ERR}
    >
      {message}
    </motion.p>
  );
}

/** Staff PIN sign-in. Errors are specific: a 401 is not a network failure. */
export function Login() {
  const { login } = useAuth();
  const reduced = useReducedMotion() ?? false;
  const [username, setUsername] = useState('');
  const [pin, setPin] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function submit(e: FormEvent) {
    e.preventDefault();
    if (!username.trim() || !pin) {
      setError('نام کاربری و پین را وارد کنید');
      return;
    }
    setLoading(true);
    setError(null);
    try {
      await login(username.trim(), pin);
    } catch (err) {
      setError(
        err instanceof ApiError && err.status === 401
          ? 'نام کاربری یا پین نادرست است'
          : 'ارتباط با هستهٔ محلی برقرار نشد — دوباره تلاش کنید',
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <motion.main
      initial={reduced ? false : { opacity: 0, scale: 0.96 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={springs.smooth}
      style={PAGE}
    >
      <form onSubmit={submit} className="glass" style={CARD}>
        <BrandHeader />

        <Credentials username={username} pin={pin} onUsername={setUsername} onPin={setPin} />

        {error ? <LoginError message={error} reduced={reduced} /> : null}

        <MotionButton type="submit" state={loading ? 'loading' : 'idle'}>
          ورود
        </MotionButton>
      </form>
    </motion.main>
  );
}

export default Login;
