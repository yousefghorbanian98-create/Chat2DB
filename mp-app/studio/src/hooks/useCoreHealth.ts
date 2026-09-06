import { useEffect, useState } from 'react';

import type { CoreHealth } from '../api/client';

const HEALTH_URL = '/health';
const POLL_MS = 5000;

export type HealthPhase = 'loading' | 'online' | 'offline';

export interface CoreHealthState {
  phase: HealthPhase;
  /** One-line human description of what the core reported (or the failure). */
  detail: string;
}

function describe(body: CoreHealth): string {
  const schema = body.db.schema_version ?? '—';
  const tables = body.db.table_count ?? 0;
  return `${body.service} ${body.version} · schema ${schema} · ${tables} tables`;
}

/**
 * Poll `/health` every 5s so the shell always shows whether the local core is
 * reachable. Local-first means this indicator is load-bearing, not decoration.
 */
export function useCoreHealth(): CoreHealthState {
  const [phase, setPhase] = useState<HealthPhase>('loading');
  const [detail, setDetail] = useState('');

  useEffect(() => {
    let alive = true;

    async function probe(): Promise<void> {
      try {
        const res = await fetch(HEALTH_URL, { cache: 'no-store' });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const body = (await res.json()) as CoreHealth;
        if (!alive) return;
        setDetail(describe(body));
        setPhase(body.status === 'ok' && body.db.ok ? 'online' : 'offline');
      } catch (error) {
        if (!alive) return;
        setDetail(error instanceof Error ? error.message : String(error));
        setPhase('offline');
      }
    }

    void probe();
    const timer = setInterval(probe, POLL_MS);
    return () => {
      alive = false;
      clearInterval(timer);
    };
  }, []);

  return { phase, detail };
}
