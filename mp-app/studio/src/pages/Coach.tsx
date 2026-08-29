import { motion, useReducedMotion } from 'framer-motion';
import { useCallback, useEffect, useState } from 'react';

import {
  api,
  ApiError,
  type ActivityLevel,
  type AiRuntime,
  type Member,
  type NutritionPlan,
} from '../api/client';
import { MotionButton, type ButtonState } from '../components/MotionButton';
import { MotionCard } from '../components/MotionCard';
import { Skeleton } from '../components/Skeleton';
import { StatCard } from '../components/StatCard';

type Goal = 'cut' | 'maintain' | 'bulk';

const GOALS: ReadonlyArray<{ code: Goal; fa: string }> = [
  { code: 'cut', fa: 'کاهش چربی' },
  { code: 'maintain', fa: 'حفظ وزن' },
  { code: 'bulk', fa: 'عضله‌سازی' },
];

const ACTIVITIES: ReadonlyArray<{ code: ActivityLevel; fa: string }> = [
  { code: 'sedentary', fa: 'کم‌تحرک' },
  { code: 'light', fa: 'سبک' },
  { code: 'moderate', fa: 'متوسط' },
  { code: 'active', fa: 'پرتحرک' },
  { code: 'athlete', fa: 'ورزشکار' },
];

/** Deterministic nutrition + honest AI status. No number here is invented by
 *  the client: every kcal/gram comes from the server (rules JP7/C4). */
export function Coach() {
  const reduced = useReducedMotion() ?? false;
  const [members, setMembers] = useState<Member[]>([]);
  const [memberId, setMemberId] = useState<number | null>(null);
  const [goal, setGoal] = useState<Goal>('maintain');
  const [activity, setActivity] = useState<ActivityLevel>('moderate');
  const [plan, setPlan] = useState<NutritionPlan | null>(null);
  const [runtime, setRuntime] = useState<AiRuntime | null>(null);
  const [state, setState] = useState<ButtonState>('idle');
  const [error, setError] = useState<string | null>(null);
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

  const compute = useCallback(async () => {
    if (memberId === null) return;
    setState('loading');
    setError(null);
    try {
      setPlan(await api.planNutrition(memberId, { goal, activity }));
      setState('success');
    } catch (err) {
      setState('error');
      setPlan(null);
      setError(
        err instanceof ApiError && err.status === 422
          ? 'ابتدا یک ارزیابی JP7 ثبت کنید — بدون تودهٔ بدون چربی، عددی ساخته نمی‌شود.'
          : err instanceof ApiError
            ? err.detail
            : 'محاسبه ناموفق بود',
      );
    }
  }, [memberId, goal, activity]);

  if (loading) return <Skeleton label="بارگذاری صفحهٔ مربی" height={320} />;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-xl)' }}>
      <MotionCard title="تغذیه — کچ-مک‌آردل از تودهٔ بدون چربی" testId="nutrition-card">
        <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-lg)' }}>
          <label style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
            <span style={{ fontSize: 13, color: 'var(--color-muted-foreground)' }}>عضو</span>
            <select
              data-testid="nutrition-member"
              className="mp-input"
              value={memberId ?? ''}
              onChange={(e) => {
                setMemberId(e.target.value ? Number(e.target.value) : null);
                setPlan(null);
              }}
            >
              <option value="">— انتخاب کنید —</option>
              {members.map((m) => (
                <option key={m.id} value={m.id}>
                  {m.first_name} {m.last_name} · {m.membership_code}
                </option>
              ))}
            </select>
          </label>

          <fieldset style={{ border: 'none', padding: 0, margin: 0 }}>
            <legend style={{ fontSize: 13, color: 'var(--color-muted-foreground)' }}>هدف</legend>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
              {GOALS.map((g) => (
                <button
                  key={g.code}
                  type="button"
                  className="mp-chip"
                  data-testid={`goal-${g.code}`}
                  aria-pressed={goal === g.code}
                  onClick={() => setGoal(g.code)}
                  style={{
                    background: goal === g.code ? 'var(--color-accent)' : 'transparent',
                    color: goal === g.code ? 'var(--color-on-accent)' : 'var(--color-foreground)',
                  }}
                >
                  {g.fa}
                </button>
              ))}
            </div>
          </fieldset>

          <label style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
            <span style={{ fontSize: 13, color: 'var(--color-muted-foreground)' }}>
              سطح فعالیت
            </span>
            <select
              data-testid="nutrition-activity"
              className="mp-input"
              value={activity}
              onChange={(e) => setActivity(e.target.value as ActivityLevel)}
            >
              {ACTIVITIES.map((a) => (
                <option key={a.code} value={a.code}>
                  {a.fa}
                </option>
              ))}
            </select>
          </label>

          <MotionButton onClick={() => void compute()} state={state} disabled={memberId === null}>
            محاسبهٔ انرژی و ماکرو
          </MotionButton>

          {error ? (
            <motion.p
              role="alert"
              data-testid="nutrition-error"
              initial={reduced ? false : { opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              style={{ margin: 0, color: 'var(--color-destructive)', fontSize: 14 }}
            >
              {error}
            </motion.p>
          ) : null}
        </div>
      </MotionCard>

      {plan ? (
        <section
          data-testid="nutrition-result"
          style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-lg)' }}
        >
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 'var(--space-lg)' }}>
            <StatCard
              labelFa="تودهٔ بدون چربی"
              labelEn="LBM"
              value={plan.lean_mass_kg.toFixed(2)}
              unit="kg"
            />
            <StatCard labelFa="BMR" labelEn="kcal" value={plan.bmr_kcal.toFixed(0)} unit="kcal" />
            <StatCard labelFa="TDEE" labelEn="kcal" value={plan.tdee_kcal.toFixed(0)} unit="kcal" />
            <StatCard
              labelFa="هدف روزانه"
              labelEn="target"
              value={plan.target_kcal.toFixed(0)}
              unit="kcal"
              tone="primary"
            />
          </div>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 'var(--space-lg)' }}>
            <StatCard
              labelFa="پروتئین"
              labelEn="protein"
              value={plan.protein_g.toFixed(0)}
              unit="g"
              tone="gold"
            />
            <StatCard labelFa="کربوهیدرات" labelEn="carbs" value={plan.carbs_g.toFixed(0)} unit="g" />
            <StatCard labelFa="چربی" labelEn="fat" value={plan.fat_g.toFixed(0)} unit="g" />
          </div>
          <p style={{ margin: 0, fontSize: 12, color: 'var(--color-muted-foreground)' }}>
            این اعداد صرفاً راهنمای محاسباتی‌اند و جای توصیهٔ پزشک یا متخصص تغذیه را نمی‌گیرند.
          </p>
        </section>
      ) : null}

      <MotionCard title="وضعیت هوش مصنوعی" testId="ai-card">
        {runtime === null ? (
          <p style={{ margin: 0, color: 'var(--color-muted-foreground)', fontSize: 13 }}>
            وضعیت هستهٔ AI در دسترس نیست.
          </p>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 8, fontSize: 14 }}>
            <p data-testid="ai-available" style={{ margin: 0 }}>
              {runtime.available ? (
                <>
                  مدل محلی فعال:{' '}
                  <span dir="ltr" className="numeric">
                    {runtime.model ?? '—'}
                  </span>
                </>
              ) : (
                'مدل محلی در دسترس نیست — برنامه‌ها کاملاً قانون‌محور ساخته می‌شوند.'
              )}
            </p>
            <p dir="ltr" className="numeric" style={{ margin: 0, fontSize: 12, opacity: 0.7 }}>
              {runtime.base_url}
            </p>
            {runtime.error ? (
              <p dir="ltr" className="numeric" style={{ margin: 0, fontSize: 12, opacity: 0.7 }}>
                {runtime.error}
              </p>
            ) : null}
            <p
              data-testid="ai-note"
              style={{ margin: 0, fontSize: 12, color: 'var(--color-muted-foreground)' }}
            >
              {runtime.note}
            </p>
          </div>
        )}
      </MotionCard>
    </div>
  );
}

export default Coach;
