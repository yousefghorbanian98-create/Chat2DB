import { useEffect, useState } from 'react';
import { AnimatePresence, motion } from 'framer-motion';

import { durations, springs } from '../motion/presets';
import { Skeleton } from './Skeleton';

/** Shape of the Phase 0 /health response from mp-app/backend. */
export interface CoreHealth {
  status: 'ok' | 'degraded';
  service: string;
  version: string;
  db: { ok: boolean; schema_version?: string | null; table_count?: number };
}

type Phase = 'loading' | 'online' | 'offline';

const HEALTH_URL = '/health';

/**
 * Local-core status pill: loading -> online/offline, with an animated swap.
 *
 * The Studio shell must never render a blank header while it discovers whether
 * the Python core on :8751 is up (map: Studio polls /health before rendering).
 */
export function CoreStatus() {
  const [phase, setPhase] = useState<Phase>('loading');
  const [detail, setDetail] = useState<string>('');

  useEffect(() => {
    let alive = true;

    async function probe(): Promise<void> {
      try {
        const res = await fetch(HEALTH_URL, { cache: 'no-store' });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const body = (await res.json()) as CoreHealth;
        if (!alive) return;
        setDetail(
          `${body.service} ${body.version} · schema ${body.db.schema_version ?? '—'} · ${
            body.db.table_count ?? 0
          } tables`,
        );
        setPhase(body.status === 'ok' && body.db.ok ? 'online' : 'offline');
      } catch (error) {
        if (!alive) return;
        setDetail(error instanceof Error ? error.message : String(error));
        setPhase('offline');
      }
    }

    void probe();
    const timer = setInterval(probe, 5000);
    return () => {
      alive = false;
      clearInterval(timer);
    };
  }, []);

  if (phase === 'loading') {
    return <Skeleton label="بررسی وضعیت هستهٔ محلی" height={22} width={260} />;
  }

  const online = phase === 'online';

  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={phase}
        data-testid="mp-core-status"
        data-phase={phase}
        role="status"
        initial={{ opacity: 0, y: 6 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -6 }}
        transition={springs.snappy}
        style={{
          display: 'inline-flex',
          alignItems: 'center',
          gap: 'var(--space-md)',
          padding: '6px 12px',
          borderRadius: 999,
          border: '1px solid var(--color-border-subtle)',
          fontSize: 13,
          transition: `color ${durations.normal}s`,
        }}
      >
        <motion.span
          aria-hidden
          animate={online ? { scale: [1, 1.25, 1] } : { scale: 1 }}
          transition={{ duration: 1.6, repeat: online ? Infinity : 0 }}
          style={{
            width: 8,
            height: 8,
            borderRadius: '50%',
            background: online ? 'var(--color-success)' : 'var(--color-destructive)',
          }}
        />
        <span className="numeric" dir="ltr">
          {online ? detail : `هستهٔ محلی در دسترس نیست — ${detail}`}
        </span>
      </motion.div>
    </AnimatePresence>
  );
}
