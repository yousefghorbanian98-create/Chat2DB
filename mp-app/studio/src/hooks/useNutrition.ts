import { useCallback, useEffect, useState } from 'react';

import {
  api,
  ApiError,
  type ActivityLevel,
  type AiRuntime,
  type Member,
  type NutritionPlan,
} from '../api/client';
import type { ButtonState } from '../components/MotionButton';

export type Goal = 'cut' | 'maintain' | 'bulk';

export interface NutritionState {
  members: Member[];
  runtime: AiRuntime | null;
  loading: boolean;
  memberId: number | null;
  setMemberId: (id: number | null) => void;
  goal: Goal;
  setGoal: (g: Goal) => void;
  activity: ActivityLevel;
  setActivity: (a: ActivityLevel) => void;
  plan: NutritionPlan | null;
  state: ButtonState;
  error: string | null;
  compute: () => void;
}

/** Translate a nutrition failure into the reason a coach can act on. */
function describeNutritionError(err: unknown): string {
  if (!(err instanceof ApiError)) return 'محاسبه ناموفق بود';
  if (err.status === 422) {
    return 'ابتدا یک ارزیابی JP7 ثبت کنید — بدون تودهٔ بدون چربی، عددی ساخته نمی‌شود.';
  }
  return err.detail || 'محاسبه ناموفق بود';
}

/**
 * Coach page data: roster, AI runtime status, and the nutrition plan.
 *
 * Every kcal/gram comes from the local core (C4 — the client never invents a
 * number), and a missing LBM surfaces as an actionable 422, not a blank field.
 */
interface Bootstrap {
  members: Member[];
  runtime: AiRuntime | null;
  loading: boolean;
}

/** Roster + AI runtime status, loaded once. Both are optional. */
function useCoachBootstrap(): Bootstrap {
  const [members, setMembers] = useState<Member[]>([]);
  const [runtime, setRuntime] = useState<AiRuntime | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let alive = true;
    (async () => {
      const [list, rt] = await Promise.allSettled([api.listMembers(), api.aiRuntime()]);
      if (!alive) return;
      if (list.status === 'fulfilled') setMembers(list.value);
      if (rt.status === 'fulfilled') setRuntime(rt.value);
      setLoading(false);
    })();
    return () => {
      alive = false;
    };
  }, []);

  return { members, runtime, loading };
}

export function useNutrition(): NutritionState {
  const { members, runtime, loading } = useCoachBootstrap();
  const [memberId, setMemberId] = useState<number | null>(null);
  const [goal, setGoal] = useState<Goal>('maintain');
  const [activity, setActivity] = useState<ActivityLevel>('moderate');
  const [plan, setPlan] = useState<NutritionPlan | null>(null);
  const [state, setState] = useState<ButtonState>('idle');
  const [error, setError] = useState<string | null>(null);

  /** Switching athlete invalidates the previous plan — never show stale macros. */
  const selectMember = useCallback((id: number | null) => {
    setMemberId(id);
    setPlan(null);
    setError(null);
    setState('idle');
  }, []);

  const compute = useCallback(() => {
    if (memberId === null) return;
    setState('loading');
    setError(null);
    void api
      .planNutrition(memberId, { goal, activity })
      .then((p) => {
        setPlan(p);
        setState('success');
      })
      .catch((err: unknown) => {
        setState('error');
        setPlan(null);
        setError(describeNutritionError(err));
      });
  }, [memberId, goal, activity]);

  return {
    members,
    runtime,
    loading,
    memberId,
    setMemberId: selectMember,
    goal,
    setGoal,
    activity,
    setActivity,
    plan,
    state,
    error,
    compute,
  };
}
