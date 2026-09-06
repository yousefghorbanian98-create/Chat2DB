import { useMemo, useState, type CSSProperties } from 'react';

import type { Assessment } from '../api/client';

import { AthleteProfile } from '../components/assessment/AthleteProfile';
import { ErrorSummary } from '../components/assessment/ErrorSummary';
import { InjuryBanner } from '../components/assessment/InjuryBanner';
import { MemberSelect } from '../components/assessment/MemberSelect';
import { ResultPanel } from '../components/assessment/ResultPanel';
import { SiteForm } from '../components/assessment/SiteForm';
import { BodyFatChart } from '../components/BodyFatChart';
import { MotionButton } from '../components/MotionButton';
import { Skeleton } from '../components/Skeleton';
import { useMembers } from '../hooks/useMembers';
import { canCalculate, emptyDraft, type Jp7Draft } from './jp7Validation';
import { useAssessmentData } from './assessment/useAssessmentData';
import { useJp7Actions } from './assessment/useJp7Actions';

const PAGE: CSSProperties = {
  padding: 'var(--space-2xl)',
  display: 'grid',
  gap: 'var(--space-xl)',
};
const GRID: CSSProperties = {
  display: 'grid',
  gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
  gap: 'var(--space-xl)',
  alignItems: 'start',
};
const TOP_ROW: CSSProperties = {
  display: 'flex',
  gap: 'var(--space-lg)',
  flexWrap: 'wrap',
  alignItems: 'center',
};

/** Body-fat trend over the athlete's saved assessments. */
function TrendSection({ history }: { history: Assessment[] }) {
  return (
    <section className="glass" style={{ padding: 'var(--space-2xl)' }}>
      <h3 style={{ marginBottom: 'var(--space-lg)' }}>روند درصد چربی بدن</h3>
      <BodyFatChart history={history} />
    </section>
  );
}

/** Skeleton shell — never a blank block while the roster loads. */
function LoadingState() {
  return (
    <div style={PAGE}>
      <Skeleton label="بارگذاری اعضا" height={44} />
      <Skeleton label="فرم ارزیابی" height={300} />
    </div>
  );
}

/** The core is unreachable; say so and offer the only real action. */
function OfflineState({ onRetry }: { onRetry: () => void }) {
  return (
    <div role="alert" style={{ ...PAGE, textAlign: 'center', color: 'var(--color-destructive)' }}>
      <p>ارتباط با هستهٔ محلی برقرار نشد.</p>
      <MotionButton onClick={onRetry}>تلاش دوباره</MotionButton>
    </div>
  );
}

/**
 * Jackson–Pollock 7 assessment page (mockup 07).
 *
 * The page owns only state wiring and layout; visuals live in
 * `components/assessment/*` and behaviour in `assessment/use*` hooks.
 */
export function AssessmentJp7() {
  const { members, loading, error: membersError } = useMembers();
  const [memberId, setMemberId] = useState<number | null>(null);
  const [draft, setDraft] = useState<Jp7Draft>(emptyDraft);
  const { assessments, injuries, addAssessment } = useAssessmentData(memberId);
  const member = useMemo(() => members.find((m) => m.id === memberId) ?? null, [members, memberId]);
  const jp7 = useJp7Actions(draft, member, addAssessment);

  const activeInjuries = useMemo(
    () => injuries.filter((i) => i.status === 'active' || i.status === 'chronic'),
    [injuries],
  );

  // Reset the form when the athlete changes (render-phase, not in an effect).
  const [prevId, setPrevId] = useState<number | null>(null);
  if (memberId !== prevId) {
    setPrevId(memberId);
    setDraft(emptyDraft());
    jp7.reset();
  }

  if (loading) return <LoadingState />;
  if (membersError) return <OfflineState onRetry={() => window.location.reload()} />;

  return (
    <div style={PAGE}>
      <div style={TOP_ROW}>
        <MemberSelect members={members} memberId={memberId} onSelect={setMemberId} />
        <InjuryBanner injuries={activeInjuries} />
      </div>

      <ErrorSummary errors={jp7.errors} />

      <div style={GRID}>
        <AthleteProfile member={member} />
        <SiteForm
          draft={draft}
          errors={jp7.errors}
          canCalculate={canCalculate(draft) && member !== null}
          canSave={jp7.preview !== null}
          saving={jp7.saving}
          onSiteChange={(key, value) =>
            setDraft((d) => ({ ...d, sites: { ...d.sites, [key]: value } }))
          }
          onWeightChange={(v) => setDraft((d) => ({ ...d, weightKg: v }))}
          onAgeChange={(v) => setDraft((d) => ({ ...d, ageYears: v }))}
          onBlurValidate={() => jp7.validateNow(draft)}
          onCalculate={jp7.calculate}
          onSave={jp7.save}
        />
        <ResultPanel preview={jp7.preview} saved={jp7.saved} />
      </div>

      <TrendSection history={assessments} />
    </div>
  );
}

export default AssessmentJp7;
