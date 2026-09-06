import { useCallback, useEffect, useState } from 'react';

import {
  ApiError,
  api,
  type Assessment,
  type ClientNutrition,
  type ClientPayment,
  type Injury,
  type Member,
  type ProgramRow,
  type WorkoutLog,
} from '../api/client';

export interface ClientData {
  me: Member | null;
  assessments: Assessment[];
  programs: ProgramRow[];
  nutrition: ClientNutrition | null;
  injuries: Injury[];
  payments: ClientPayment[];
  workouts: WorkoutLog[];
  loading: boolean;
  error: string | null;
  reload: () => void;
  /** Re-read only the session log, after the athlete saves one. */
  refreshWorkouts: () => Promise<WorkoutLog[]>;
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

/** Everything the athlete shell renders, fetched in one parallel round trip. */
interface ClientBundle {
  me: Member;
  assessments: Assessment[];
  programs: ProgramRow[];
  nutrition: ClientNutrition | null;
  injuries: Injury[];
  payments: ClientPayment[];
  workouts: WorkoutLog[];
}

/** Fetch all seven athlete endpoints at once; any failure rejects the bundle. */
async function loadBundle(): Promise<ClientBundle> {
  const [me, assessments, programs, nutrition, injuries, payments, workouts] = await Promise.all([
    api.clientMe(),
    api.clientAssessments(),
    api.clientPrograms(),
    loadNutrition(),
    api.clientInjuries(),
    api.clientPayments(),
    api.clientWorkouts(),
  ]);
  return { me, assessments, programs, nutrition, injuries, payments, workouts };
}

/**
 * The athlete's own (server-masked) profile, history, programs, macros,
 * restrictions, payments and session log.
 *
 * Everything comes from `/client/*`, which the core force-scopes to the MEMBER
 * token and strips clinician notes and staff attribution (C9, C11) — the shell
 * never sees a raw row.
 */
export function useClientData(): ClientData {
  const [bundle, setBundle] = useState<ClientBundle | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [reloadKey, setReloadKey] = useState(0);

  const refreshWorkouts = useCallback(async () => {
    const rows = await api.clientWorkouts();
    setBundle((b) => (b === null ? b : { ...b, workouts: rows }));
    return rows;
  }, []);

  useEffect(() => {
    let alive = true;
    void loadBundle()
      .then((loaded) => {
        if (!alive) return;
        setBundle(loaded);
        setError(null);
      })
      .catch(() => {
        if (alive) setError('بارگذاری اطلاعات میسر نشد — دوباره تلاش کنید.');
      })
      .finally(() => {
        if (alive) setLoading(false);
      });
    return () => {
      alive = false;
    };
  }, [reloadKey]);

  const reload = useCallback(() => setReloadKey((k) => k + 1), []);

  return {
    me: bundle?.me ?? null,
    assessments: bundle?.assessments ?? [],
    programs: bundle?.programs ?? [],
    nutrition: bundle?.nutrition ?? null,
    injuries: bundle?.injuries ?? [],
    payments: bundle?.payments ?? [],
    workouts: bundle?.workouts ?? [],
    loading,
    error,
    reload,
    refreshWorkouts,
  };
}
