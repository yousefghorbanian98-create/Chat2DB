import { motion, useReducedMotion, type MotionStyle } from 'framer-motion';
import type { CSSProperties } from 'react';

import type { ActivityLevel, AiRuntime, Member, NutritionPlan } from '../api/client';
import { MotionButton, type ButtonState } from '../components/MotionButton';
import { MotionCard } from '../components/MotionCard';
import { Skeleton } from '../components/Skeleton';
import { StatCard } from '../components/StatCard';
import { useNutrition, type Goal } from '../hooks/useNutrition';
import { fieldLabel, muted, stackLg } from '../styles/blocks';

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

const PAGE: CSSProperties = { display: 'flex', flexDirection: 'column', gap: 'var(--space-xl)' };
const CHIP_ROW: CSSProperties = { display: 'flex', flexWrap: 'wrap', gap: 8 };
const FIELDSET: CSSProperties = { border: 'none', padding: 0, margin: 0 };
const ALERT: MotionStyle = { margin: 0, color: 'var(--color-destructive)', fontSize: 14 };
const STAT_ROW: CSSProperties = { display: 'flex', flexWrap: 'wrap', gap: 'var(--space-lg)' };
const AI_BOX: CSSProperties = {
  display: 'flex',
  flexDirection: 'column',
  gap: 8,
  fontSize: 14,
};
const AI_META: CSSProperties = { margin: 0, fontSize: 12, opacity: 0.7 };

/** Chip picker for the goal, shared shape with the payment method picker. */
function ChipPicker({
  selected,
  onSelect,
  prefix,
}: {
  selected: string;
  onSelect: (code: Goal) => void;
  prefix: string;
}) {
  return (
    <fieldset style={FIELDSET}>
      <legend style={{ fontSize: 13, color: 'var(--color-muted-foreground)' }}>هدف</legend>
      <div style={CHIP_ROW}>
        {GOALS.map((g) => {
          const active = selected === g.code;
          return (
            <button
              key={g.code}
              type="button"
              className="mp-chip"
              data-testid={`${prefix}-${g.code}`}
              aria-pressed={active}
              onClick={() => onSelect(g.code)}
              style={{
                background: active ? 'var(--color-accent)' : 'transparent',
                color: active ? 'var(--color-on-accent)' : 'var(--color-foreground)',
              }}
            >
              {g.fa}
            </button>
          );
        })}
      </div>
    </fieldset>
  );
}

/** Athlete picker — changing it clears the previous plan. */
function MemberField({
  members,
  memberId,
  onChange,
}: {
  members: Member[];
  memberId: number | null;
  onChange: (id: number | null) => void;
}) {
  return (
    <label style={fieldLabel}>
      <span>عضو</span>
      <select
        data-testid="nutrition-member"
        className="mp-input"
        value={memberId ?? ''}
        onChange={(e) => onChange(e.target.value ? Number(e.target.value) : null)}
      >
        <option value="">— انتخاب کنید —</option>
        {members.map((m) => (
          <option key={m.id} value={m.id}>
            {m.first_name} {m.last_name} · {m.membership_code}
          </option>
        ))}
      </select>
    </label>
  );
}

/** Activity multiplier picker (feeds the TDEE factor server-side). */
function ActivityField({
  activity,
  onChange,
}: {
  activity: ActivityLevel;
  onChange: (a: ActivityLevel) => void;
}) {
  return (
    <label style={fieldLabel}>
      <span>سطح فعالیت</span>
      <select
        data-testid="nutrition-activity"
        className="mp-input"
        value={activity}
        onChange={(e) => onChange(e.target.value as ActivityLevel)}
      >
        {ACTIVITIES.map((a) => (
          <option key={a.code} value={a.code}>
            {a.fa}
          </option>
        ))}
      </select>
    </label>
  );
}

/** Athlete + goal + activity: the three inputs that drive the calculation. */
function NutritionForm(props: {
  members: Member[];
  memberId: number | null;
  goal: Goal;
  activity: ActivityLevel;
  state: ButtonState;
  error: string | null;
  reduced: boolean;
  onMember: (id: number | null) => void;
  onGoal: (g: Goal) => void;
  onActivity: (a: ActivityLevel) => void;
  onCompute: () => void;
}) {
  return (
    <MotionCard title="تغذیه — کچ-مک‌آردل از تودهٔ بدون چربی" testId="nutrition-card">
      <div style={stackLg}>
        <MemberField members={props.members} memberId={props.memberId} onChange={props.onMember} />

        <ChipPicker selected={props.goal} onSelect={props.onGoal} prefix="goal" />

        <ActivityField activity={props.activity} onChange={props.onActivity} />

        <MotionButton
          onClick={props.onCompute}
          state={props.state}
          disabled={props.memberId === null}
        >
          محاسبهٔ انرژی و ماکرو
        </MotionButton>

        {props.error ? (
          <motion.p
            role="alert"
            data-testid="nutrition-error"
            initial={props.reduced ? false : { opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            style={ALERT}
          >
            {props.error}
          </motion.p>
        ) : null}
      </div>
    </MotionCard>
  );
}

/** Energy + macro readout, straight from the server's numbers. */
function NutritionResult({ plan }: { plan: NutritionPlan }) {
  return (
    <section data-testid="nutrition-result" style={stackLg}>
      <div style={STAT_ROW}>
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
      <div style={STAT_ROW}>
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
      <p style={{ ...muted, margin: 0, fontSize: 12 }}>
        این اعداد صرفاً راهنمای محاسباتی‌اند و جای توصیهٔ پزشک یا متخصص تغذیه را نمی‌گیرند.
      </p>
    </section>
  );
}

/**
 * Honest AI status. When no local model is reachable we say so plainly rather
 * than pretending the rule engine is something it is not (C6/C7).
 */
function AiStatusCard({ runtime }: { runtime: AiRuntime | null }) {
  return (
    <MotionCard title="وضعیت هوش مصنوعی" testId="ai-card">
      {runtime === null ? (
        <p style={{ ...muted, margin: 0, fontSize: 13 }}>وضعیت هستهٔ AI در دسترس نیست.</p>
      ) : (
        <div style={AI_BOX}>
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
          <p dir="ltr" className="numeric" style={AI_META}>
            {runtime.base_url}
          </p>
          {runtime.error ? (
            <p dir="ltr" className="numeric" style={AI_META}>
              {runtime.error}
            </p>
          ) : null}
          <p data-testid="ai-note" style={{ ...muted, margin: 0, fontSize: 12 }}>
            {runtime.note}
          </p>
        </div>
      )}
    </MotionCard>
  );
}

/** Deterministic nutrition + honest AI status. No number here is invented by
 *  the client: every kcal/gram comes from the server (rules JP7/C4). */
export function Coach() {
  const reduced = useReducedMotion() ?? false;
  const n = useNutrition();

  if (n.loading) return <Skeleton label="بارگذاری صفحهٔ مربی" height={320} />;

  return (
    <div style={PAGE}>
      <NutritionForm
        members={n.members}
        memberId={n.memberId}
        goal={n.goal}
        activity={n.activity}
        state={n.state}
        error={n.error}
        reduced={reduced}
        onMember={(id) => {
          n.setMemberId(id);
        }}
        onGoal={n.setGoal}
        onActivity={n.setActivity}
        onCompute={n.compute}
      />

      {n.plan ? <NutritionResult plan={n.plan} /> : null}

      <AiStatusCard runtime={n.runtime} />
    </div>
  );
}

export default Coach;
