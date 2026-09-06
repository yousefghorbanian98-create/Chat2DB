import { useCallback, useEffect, useState } from 'react';

import { api, type Dashboard } from '../api/client';

export type OpsPhase = 'loading' | 'ready' | 'error';

export interface OpsKpiState {
  dash: Dashboard | null;
  today: number | null;
  phase: OpsPhase;
  /** Bumps the reload key so the error state has a real retry affordance. */
  refresh: () => void;
}

/**
 * Door + finance KPIs.
 *
 * State updates stay inside the async body (never synchronously in the effect)
 * so React does not cascade a second render, and a finance-role failure cannot
 * take the door controls down with it.
 */
export function useOpsKpis(canSeeFinance: boolean): OpsKpiState {
  const [dash, setDash] = useState<Dashboard | null>(null);
  const [today, setToday] = useState<number | null>(null);
  const [phase, setPhase] = useState<OpsPhase>('loading');
  const [reloadKey, setReloadKey] = useState(0);

  useEffect(() => {
    let alive = true;
    void (async () => {
      try {
        const todayRes = await api.attendanceToday();
        if (!alive) return;
        setToday(todayRes.check_ins);
        if (canSeeFinance) {
          try {
            const d = await api.dashboard();
            if (alive) setDash(d);
          } catch {
            if (alive) setDash(null); // finance block must not break door controls
          }
        }
        if (alive) setPhase('ready');
      } catch {
        if (alive) setPhase('error');
      }
    })();
    return () => {
      alive = false;
    };
  }, [canSeeFinance, reloadKey]);

  const refresh = useCallback(() => setReloadKey((k) => k + 1), []);

  return { dash, today, phase, refresh };
}
