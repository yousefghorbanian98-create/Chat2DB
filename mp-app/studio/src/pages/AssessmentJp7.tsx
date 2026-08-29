import { AnimatePresence, motion } from 'framer-motion';
import { useCallback, useEffect, useMemo, useState } from 'react';

import { api, type Assessment, type Injury, type Member } from '../api/client';
import { BodyFatChart } from '../components/BodyFatChart';
import { MotionButton } from '../components/MotionButton';
import { NumberField } from '../components/NumberField';
import { Skeleton } from '../components/Skeleton';
import { StatCard } from '../components/StatCard';
import { computeJp7, type Sex } from '../core/jp7';
import {
  SITE_META,
  SITE_ORDER,
  canCalculate,
  draftToPayload,
  emptyDraft,
  validateDraft,
  type FieldError,
  type Jp7Draft,
} from './jp7Validation';

const CLASSIFICATION_FA: Record<string, string> = {
  essential: 'ضروری',
  athletic: 'ورزشکاری',
  fit: 'آماده',
  average: 'متوسط',
  overfat: 'بیش‌چربی',
  obese: 'چاق',
};

type LoadPhase = 'loading' | 'ready' | 'error';

/**
 * Jackson–Pollock 7 assessment page, built to `pages/assessment-jp7.md` and
 * mockup 07: three columns on wide screens, silhouette markers, results panel,
 * BF% trend at the bottom, injury safety banner, and an error summary.
 */
export function AssessmentJp7() {
  const [members, setMembers] = useState<Member[]>([]);
  const [memberId, setMemberId] = useState<number | null>(null);
  const [assessments, setAssessments] = useState<Assessment[]>([]);
  const [injuries, setInjuries] = useState<Injury[]>([]);
  const [phase, setPhase] = useState<LoadPhase>('loading');

  const [draft, setDraft] = useState<Jp7Draft>(emptyDraft);
  const [errors, setErrors] = useState<FieldError[]>([]);
  const [preview, setPreview] = useState<ReturnType<typeof computeJp7> | null>(null);
  const [saved, setSaved] = useState<Assessment | null>(null);
  const [action, setAction] = useState<'idle' | 'saving'>('idle');

  useEffect(() => {
    let alive = true;
    (async () => {
      try {
        const list = await api.listMembers();
        if (!alive) return;
        setMembers(list);
        setPhase('ready');
      } catch {
        if (alive) setPhase('error');
      }
    })();
    return () => {
      alive = false;
    };
  }, []);

  const member = useMemo(
    () => members.find((m) => m.id === memberId) ?? null,
    [members, memberId],
  );

  // Load history + injuries whenever a member is chosen.
  useEffect(() => {
    if (memberId === null) return;
    let alive = true;
    (async () => {
      try {
        const [assess, inj] = await Promise.all([
          api.listAssessments(memberId),
          api.listInjuries(memberId),
        ]);
        if (!alive) return;
        setAssessments(assess);
        setInjuries(inj);
      } catch {
        /* history is non-fatal for the form */
      }
    })();
    return () => {
      alive = false;
    };
  }, [memberId]);

  const activeInjuries = useMemo(
    () => injuries.filter((i) => i.status === 'active' || i.status === 'chronic'),
    [injuries],
  );

  const handleCalculate = useCallback(() => {
    const errs = validateDraft(draft);
    setErrors(errs);
    setPreview(null);
    if (errs.length > 0 || !member) return;

    const payload = draftToPayload(draft);
    setPreview(
      computeJp7({
        sex: member.sex as Sex,
        age: payload.age_years,
        sites: payload.sites_mm,
        weightKg: payload.weight_kg,
      }),
    );
  }, [draft, member]);

  const handleSave = useCallback(async () => {
    if (!member || !preview) return;
    setAction('saving');
    try {
      const payload = draftToPayload(draft);
      const stored = await api.saveAssessment(member.id, payload);
      setSaved(stored);
      setAssessments((prev) => [stored, ...prev]);
    } finally {
      setAction('idle');
    }
  }, [member, preview, draft]);

  const siteError = (key: (typeof SITE_ORDER)[number]) =>
    errors.find((e) => e.field === key)?.messageFa ?? null;

  const gridStyle: React.CSSProperties = {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
    gap: 'var(--space-xl)',
    alignItems: 'start',
  };

  if (phase === 'loading') {
    return (
      <div style={{ padding: 'var(--space-2xl)', display: 'grid', gap: 'var(--space-xl)' }}>
        <Skeleton label="بارگذاری اعضا" height={44} />
        <Skeleton label="فرم ارزیابی" height={300} />
      </div>
    );
  }

  if (phase === 'error') {
    return (
      <div role="alert" style={{ padding: 'var(--space-3xl)', textAlign: 'center', color: 'var(--color-destructive)' }}>
        ارتباط با هستهٔ محلی برقرار نشد — صفحه را تازه‌سازی کنید.
      </div>
    );
  }

  return (
    <div style={{ padding: 'var(--space-2xl)', display: 'grid', gap: 'var(--space-xl)' }}>
      {/* Member picker + injury safety banner */}
      <div style={{ display: 'flex', gap: 'var(--space-lg)', flexWrap: 'wrap', alignItems: 'center' }}>
        <label style={{ display: 'flex', flexDirection: 'column', gap: 6, fontSize: 13, color: 'var(--color-muted-foreground)' }}>
          ورزشکار
          <select
            value={memberId ?? ''}
            onChange={(e) => {
              setMemberId(e.target.value ? Number(e.target.value) : null);
              setPreview(null);
              setSaved(null);
              setDraft(emptyDraft());
              setErrors([]);
            }}
            style={{
              background: '#0A1218',
              border: '1px solid var(--color-border-subtle)',
              color: 'var(--color-foreground)',
              padding: '10px 12px',
              borderRadius: 8,
              fontSize: 15,
              minWidth: 200,
            }}
          >
            <option value="">— انتخاب —</option>
            {members.map((m) => (
              <option key={m.id} value={m.id}>
                {m.first_name} {m.last_name}
              </option>
            ))}
          </select>
        </label>

        <AnimatePresence>
          {activeInjuries.length > 0 && (
            <motion.div
              initial={{ opacity: 0, y: -8 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              role="alert"
              style={{
                padding: '8px 14px',
                borderRadius: 8,
                background: 'rgba(239,68,68,0.15)',
                border: '1px solid var(--color-injury-active)',
                color: '#FCA5A5',
                fontSize: 13,
              }}
            >
              ⚠ {activeInjuries.length} آسیب فعال — قبل از اعمال برنامه بررسی شود
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Error summary (A11y: top of form on failed calculate) */}
      {errors.length > 0 && (
        <div role="alert" style={{
          padding: '10px 14px',
          borderRadius: 8,
          background: 'rgba(239,68,68,0.12)',
          border: '1px solid var(--color-injury-active)',
          color: '#FCA5A5',
          fontSize: 13,
        }}>
          {errors.length} خطا: {errors.slice(0, 3).map((e) => e.messageFa).join('، ')}
          {errors.length > 3 ? '، …' : ''}
        </div>
      )}

      <div style={gridStyle}>
        {/* Column 1: athlete profile */}
        <section className="glass" style={{ padding: 'var(--space-2xl)' }}>
          <h3 style={{ marginBottom: 'var(--space-lg)' }}>ورزشکار</h3>
          {member ? (
            <div style={{ display: 'grid', gap: 'var(--space-md)', fontSize: 14 }}>
              <div style={{ fontSize: 20, fontFamily: 'var(--font-display)' }}>
                {member.first_name} {member.last_name}
              </div>
              <div style={{ color: 'var(--color-muted-foreground)' }}>
                جنسیت: {member.sex === 'male' ? 'مرد' : 'زن'}
              </div>
              <div style={{ color: 'var(--color-muted-foreground)' }} className="numeric" dir="ltr">
                {member.membership_code}
              </div>
              {member.birth_date ? (
                <div style={{ color: 'var(--color-muted-foreground)' }} className="numeric" dir="ltr">
                  {member.birth_date}
                </div>
              ) : null}
            </div>
          ) : (
            <p style={{ color: 'var(--color-muted-foreground)' }}>ابتدا یک ورزشکار انتخاب کنید.</p>
          )}
        </section>

        {/* Column 2: 7-site form */}
        <section className="glass" style={{ padding: 'var(--space-2xl)' }}>
          <h3 style={{ marginBottom: 'var(--space-lg)' }}>ضخامت چین پوستی (mm)</h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(150px, 1fr))', gap: 'var(--space-lg)' }}>
            {SITE_ORDER.map((key, i) => (
              <NumberField
                key={key}
                badge={i + 1}
                label={SITE_META[key].en}
                subLabel={SITE_META[key].fa}
                value={draft.sites[key]}
                onChange={(v) => {
                  setDraft((d) => ({ ...d, sites: { ...d.sites, [key]: v } }));
                }}
                onBlur={() => setErrors(validateDraft(draft))}
                error={siteError(key)}
              />
            ))}
            <NumberField
              label="Weight"
              subLabel="وزن"
              unit="kg"
              value={draft.weightKg}
              onChange={(v) => setDraft((d) => ({ ...d, weightKg: v }))}
              onBlur={() => setErrors(validateDraft(draft))}
              error={errors.find((e) => e.field === 'weightKg')?.messageFa ?? null}
            />
            <NumberField
              label="Age"
              subLabel="سن"
              unit="y"
              value={draft.ageYears}
              onChange={(v) => setDraft((d) => ({ ...d, ageYears: v }))}
              onBlur={() => setErrors(validateDraft(draft))}
              error={errors.find((e) => e.field === 'ageYears')?.messageFa ?? null}
            />
          </div>

          <div style={{ display: 'flex', gap: 'var(--space-lg)', marginTop: 'var(--space-xl)' }}>
            <MotionButton onClick={handleCalculate} disabled={!canCalculate(draft) || !member}>
              محاسبه
            </MotionButton>
            <MotionButton variant="ghost" onClick={handleSave} disabled={!preview} state={action === 'saving' ? 'loading' : 'idle'}>
              ذخیره ارزیابی
            </MotionButton>
          </div>
        </section>

        {/* Column 3: results */}
        <section className="glass" style={{ padding: 'var(--space-2xl)' }}>
          <h3 style={{ marginBottom: 'var(--space-lg)' }}>نتایج</h3>
          {preview ? (
            <div style={{ display: 'grid', gap: 'var(--space-lg)' }}>
              <div style={{ fontSize: 44, fontWeight: 700, fontFamily: 'var(--font-display)', color: 'var(--color-accent)' }} className="numeric" dir="ltr">
                {preview.bodyFatPct.toFixed(1)}%
              </div>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 'var(--space-lg)' }}>
                <StatCard labelFa="جرم چربی" labelEn="FM" value={preview.fatMassKg?.toFixed(1) ?? '—'} unit="kg" tone="gold" />
                <StatCard labelFa="جرم بدون چربی" labelEn="LBM" value={preview.leanMassKg?.toFixed(1) ?? '—'} unit="kg" tone="primary" />
                <StatCard labelFa="چگالی بدن" labelEn="BD" value={preview.bodyDensity.toFixed(4)} />
                <StatCard labelFa="رده" labelEn="Class" value={CLASSIFICATION_FA[preview.classification] ?? preview.classification} />
              </div>
              <p style={{ fontSize: 12, color: 'var(--color-muted-foreground)', margin: 0 }}>
                پیش‌نمایش — عدد نهایی پس از ذخیره توسط هستهٔ محلی تأیید می‌شود.
              </p>
            </div>
          ) : saved ? (
            <div style={{ color: 'var(--color-success)', fontSize: 14 }}>
              ✔ ذخیره شد: BF {saved.body_fat_pct.toFixed(1)}%
            </div>
          ) : (
            <p style={{ color: 'var(--color-muted-foreground)' }}>ابتدا «محاسبه» را بزنید.</p>
          )}
        </section>
      </div>

      {/* Bottom: BF% trend */}
      <section className="glass" style={{ padding: 'var(--space-2xl)' }}>
        <h3 style={{ marginBottom: 'var(--space-lg)' }}>روند درصد چربی بدن</h3>
        <BodyFatChart history={assessments} />
      </section>
    </div>
  );
}

export default AssessmentJp7;
