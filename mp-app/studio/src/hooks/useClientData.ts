import { useCallback, useEffect, useState } from 'react';

import { api, type Assessment, type Member, type ProgramRow } from '../api/client';

export interface ClientData {
  me: Member | null;
  assessments: Assessment[];
  programs: ProgramRow[];
  loading: boolean;
  error: string | null;
  reload: () => void;
}

/**
 * The athlete's own (server-masked) profile, history and programs.
 *
 * Everything comes from `/client/*`, which the core force-scopes to the MEMBER
 * token and strips clinician notes (C9) — the shell never sees raw rows.
 */
export function useClientData(): ClientData {
  const [me, setMe] = useState<Member | null>(null);
  const [assessments, setAssessments] = useState<Assessment[]>([]);
  const [programs, setPrograms] = useState<ProgramRow[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [reloadKey, setReloadKey] = useState(0);

  useEffect(() => {
    let alive = true;
    (async () => {
      try {
        const [profile, hist, progs] = await Promise.all([
          api.clientMe(),
          api.clientAssessments(),
          api.clientPrograms(),
        ]);
        if (!alive) return;
        setMe(profile);
        setAssessments(hist);
        setPrograms(progs);
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

  return { me, assessments, programs, loading, error, reload };
}
