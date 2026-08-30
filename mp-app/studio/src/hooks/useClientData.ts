import { useCallback, useEffect, useState } from 'react';

import {
  ApiError,
  api,
  type Assessment,
  type ClientNutrition,
  type Member,
  type ProgramRow,
} from '../api/client';

export interface ClientData {
  me: Member | null;
  assessments: Assessment[];
  programs: ProgramRow[];
  nutrition: ClientNutrition | null;
  loading: boolean;
  error: string | null;
  reload: () => void;
}

/**
 * The athlete's own (server-masked) profile, history, programs and macros.
 *
 * Everything comes from `/client/*`, which the core force-scopes to the MEMBER
 * token and strips clinician notes (C9) — the shell never sees raw rows.
 */
export function useClientData(): ClientData {
  const [me, setMe] = useState<Member | null>(null);
  const [assessments, setAssessments] = useState<Assessment[]>([]);
  const [programs, setPrograms] = useState<ProgramRow[]>([]);
  const [nutrition, setNutrition] = useState<ClientNutrition | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [reloadKey, setReloadKey] = useState(0);

  useEffect(() => {
    let alive = true;
    (async () => {
      try {
        const [profile, hist, progs, plan] = await Promise.all([
          api.clientMe(),
          api.clientAssessments(),
          api.clientPrograms(),
          loadNutrition(),
        ]);
        if (!alive) return;
        setMe(profile);
        setAssessments(hist);
        setPrograms(progs);
        setNutrition(plan);
        setError(null);
      } catch {
        if (alive) setError('بارگذاری اطلاعات میسر نشد — دوباره تلاش کنید.');
      } finally {
        if (alive) setLoading(false);
      }
    })();
    return () => {
      alive = false;
    };
  }, [reloadKey]);

  const reload = useCallback(() => setReloadKey((k) => k + 1), []);

  return { me, assessments, programs, nutrition, loading, error, reload };
}

/** The plan is optional until the coach writes one; anything else is an error. */
async function loadNutrition(): Promise<ClientNutrition | null> {
  try {
    return await api.clientNutrition();
  } catch (err) {
    if (err instanceof ApiError && err.status === 404) return null;
    throw err;
  }
}
