import { motion, useReducedMotion, type MotionStyle } from 'framer-motion';
import type { CSSProperties } from 'react';
import { useState, type FormEvent } from 'react';

import { ApiError } from '../api/client';
import { MotionButton } from '../components/MotionButton';
import { springs } from '../motion/presets';
import { useAuth } from '../auth/useAuth';
import { fieldLabel } from '../styles/blocks';

type Mode = 'staff' | 'member';

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
const MODE_ROW: CSSProperties = { display: 'flex', gap: 8, justifyContent: 'center' };

interface PairProps {
  first: string;
  pin: string;
  firstLabel: string;
  onFirst: (v: string) => void;
  onPin: (v: string) => void;
}

/** A labelled text + PIN pair, shared by both modes. */
function Pair({ first, pin, firstLabel, onFirst, onPin }: PairProps) {
  return (
    <>
      <label style={fieldLabel}>
        {firstLabel}
        <input className="mp-input" value={first} onChange={(e) => onFirst(e.target.value)} />
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

/** Studio wordmark; the subtitle follows the active mode. */
function BrandHeader({ mode }: { mode: Mode }) {
  return (
    <div style={HEAD}>
      <h1 style={{ fontSize: 30 }}>
        Muscle Paradise <span style={{ color: 'var(--color-primary)' }}>Studio</span>
      </h1>
      <p style={SUBHEAD}>
        {mode === 'staff' ? 'ورود کارکنان — پین' : 'ورود ورزشکار — کد عضویت و پین'}
      </p>
    </div>
  );
}

/** Staff / athlete toggle. */
function ModeSwitch({ mode, onMode }: { mode: Mode; onMode: (m: Mode) => void }) {
  return (
    <div style={MODE_ROW}>
      {(['staff', 'member'] as const).map((m) => (
        <button
          key={m}
          type="button"
          className="mp-chip"
          data-testid={`mode-${m}`}
          aria-pressed={mode === m}
          onClick={() => onMode(m)}
          style={{
            background: mode === m ? 'var(--color-accent)' : 'transparent',
            color: mode === m ? 'var(--color-on-accent)' : 'var(--color-foreground)',
          }}
        >
          {m === 'staff' ? 'کارکنان' : 'ورزشکار'}
        </button>
      ))}
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

/** A 401 is wrong credentials; anything else is a transport failure. */
function describeLoginError(err: unknown): string {
  return err instanceof ApiError && err.status === 401
    ? 'اعتبارها نادرست است'
    : 'ارتباط با هستهٔ محلی برقرار نشد — دوباره تلاش کنید';
}

/** Dual-mode sign-in: staff PIN, or athlete membership-code + PIN (C9). */
export function Login({ initialMode = 'staff' }: { initialMode?: Mode }) {
  const { login, memberLogin } = useAuth();
  const reduced = useReducedMotion() ?? false;
  const [mode, setMode] = useState<Mode>(initialMode);
  const [first, setFirst] = useState('');
  const [pin, setPin] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function submit(e: FormEvent) {
    e.preventDefault();
    if (!first.trim() || !pin) {
      setError('هر دو فیلد را وارد کنید');
      return;
    }
    setLoading(true);
    setError(null);
    try {
      if (mode === 'staff') await login(first.trim(), pin);
      else await memberLogin(first.trim(), pin);
    } catch (err) {
      setError(describeLoginError(err));
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
        <BrandHeader mode={mode} />
        <ModeSwitch mode={mode} onMode={setMode} />
        <Pair
          first={first}
          pin={pin}
          firstLabel={mode === 'staff' ? 'نام کاربری' : 'کد عضویت'}
          onFirst={setFirst}
          onPin={setPin}
        />
        {error ? <LoginError message={error} reduced={reduced} /> : null}
        <MotionButton type="submit" state={loading ? 'loading' : 'idle'}>
          ورود
        </MotionButton>
      </form>
    </motion.main>
  );
}

export default Login;
