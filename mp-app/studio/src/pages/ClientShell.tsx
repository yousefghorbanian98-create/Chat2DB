import type { CSSProperties } from 'react';

import type { Assessment, ClientNutrition, Member, ProgramRow } from '../api/client';
import { MotionButton } from '../components/MotionButton';
import { MotionCard } from '../components/MotionCard';
import { Skeleton } from '../components/Skeleton';
import { StatCard } from '../components/StatCard';
import { useAuth } from '../auth/useAuth';
import { useClientData } from '../hooks/useClientData';
import { faDate } from '../core/jalali';
import { cardSection, cardTitle, muted, stackLg } from '../styles/blocks';

const PAGE: CSSProperties = {
  padding: 'var(--space-2xl)',
  display: 'flex',
  flexDirection: 'column',
  gap: 'var(--space-xl)',
};
const STAT_ROW: CSSProperties = { display: 'flex', flexWrap: 'wrap', gap: 'var(--space-lg)' };
const LIST: CSSProperties = { margin: 0, paddingInlineStart: 18, lineHeight: 1.9 };

/** The athlete's masked identity card. */
function ProfileCard({ me }: { me: Member }) {
  return (
    <MotionCard title="پروفایل من" testId="client-profile">
      <div style={STAT_ROW}>
        <StatCard labelFa="نام" labelEn="name" value={`${me.first_name} ${me.last_name}`} />
        <StatCard labelFa="کد عضویت" labelEn="code" value={me.membership_code} />
        <StatCard
          labelFa="اعتبار تا"
          labelEn="exp"
          value={me.membership_exp ? faDate(me.membership_exp) : '—'}
        />
      </div>
    </MotionCard>
  );
}

/** Daily energy + macro targets (the internal payload blob is server-stripped). */
function NutritionCard({ plan }: { plan: ClientNutrition }) {
  return (
    <MotionCard title="تغذیهٔ من" testId="client-nutrition">
      <div style={STAT_ROW}>
        <StatCard labelFa="کالری روزانه" labelEn="kcal" value={plan.tdee_kcal.toFixed(0)} unit="kcal" tone="primary" />
        <StatCard labelFa="پروتئین" labelEn="protein" value={plan.protein_g.toFixed(0)} unit="g" />
        <StatCard labelFa="کربوهیدرات" labelEn="carbs" value={plan.carbs_g.toFixed(0)} unit="g" />
        <StatCard labelFa="چربی" labelEn="fat" value={plan.fat_g.toFixed(0)} unit="g" />
      </div>
    </MotionCard>
  );
}

/** Body-fat trend, newest first (masked assessment rows). */
function AssessmentList({ rows }: { rows: Assessment[] }) {
  return (
    <section className="glass" style={cardSection} data-testid="client-assessments">
      <h3 style={cardTitle}>روند ارزیابی من</h3>
      {rows.length === 0 ? (
        <p style={muted}>هنوز ارزیابی‌ای ثبت نشده است.</p>
      ) : (
        <ul style={LIST}>
          {rows.slice(0, 6).map((a) => (
            <li key={a.id}>
              <span className="numeric">{faDate(a.created_at)}</span> — چربی{' '}
              {a.body_fat_pct.toFixed(1)}٪ · وزن {a.weight_kg.toFixed(1)} kg
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}

/** The athlete's programs with their lifecycle status. */
function ProgramList({ rows }: { rows: ProgramRow[] }) {
  return (
    <section className="glass" style={cardSection} data-testid="client-programs">
      <h3 style={cardTitle}>برنامه‌های من</h3>
      {rows.length === 0 ? (
        <p style={muted}>هنوز برنامه‌ای برای شما ساخته نشده است.</p>
      ) : (
        <ul style={LIST}>
          {rows.map((p) => (
            <li key={p.id}>
              {p.title} — <strong>{p.status}</strong>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}

/**
 * Athlete (client) shell. Rendered only for a MEMBER token; every row is the
 * server-masked version, so no clinician note can leak here (C9).
 */
export function ClientShell() {
  const { logout } = useAuth();
  const { me, assessments, programs, nutrition, loading, error, reload } = useClientData();

  return (
    <div style={PAGE}>
      <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h1 style={{ fontSize: 26 }}>
          ماسل پارادایز <span style={{ color: 'var(--color-primary)' }}>ورزشکار</span>
        </h1>
        <MotionButton variant="ghost" onClick={logout}>
          خروج
        </MotionButton>
      </header>

      {loading ? (
        <div style={stackLg}>
          <Skeleton label="بارگذاری پروفایل" height={80} />
          <Skeleton label="بارگذاری روند" height={160} />
        </div>
      ) : error ? (
        <div role="alert" style={{ ...stackLg, color: 'var(--color-destructive)' }}>
          <p>{error}</p>
          <MotionButton onClick={reload}>تلاش دوباره</MotionButton>
        </div>
      ) : me ? (
        <>
          <ProfileCard me={me} />
          {nutrition ? <NutritionCard plan={nutrition} /> : null}
          <AssessmentList rows={assessments} />
          <ProgramList rows={programs} />
        </>
      ) : null}
    </div>
  );
}

export default ClientShell;
