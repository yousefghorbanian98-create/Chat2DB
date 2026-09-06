import { CheckinPanel } from '../components/CheckinPanel';
import { MotionButton } from '../components/MotionButton';
import { OpsKpis } from '../components/OpsKpis';
import { PaymentPanel } from '../components/PaymentPanel';
import { Skeleton } from '../components/Skeleton';
import { useAuth } from '../auth/useAuth';
import { useMembers } from '../hooks/useMembers';
import { useOpsKpis } from '../hooks/useOpsKpis';
import { stackLg, stackXl } from '../styles/blocks';

/** Finance roles see money KPIs; everyone else gets door KPIs only (§2.4). */
const FINANCE_ROLES = new Set(['OWNER', 'ADMIN']);

const PANEL_GRID = {
  display: 'grid',
  gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))',
  gap: 'var(--space-xl)',
  alignItems: 'start',
};

/**
 * Operations console (Phase 2): door control + cash desk + live KPIs.
 * KPI numbers come from the server, never from the client (no invented maths).
 */
export function Operations() {
  const { role } = useAuth();
  const { members, loading: membersLoading } = useMembers();
  const canSeeFinance = role !== null && FINANCE_ROLES.has(role);
  const { dash, today, phase, refresh } = useOpsKpis(canSeeFinance);

  if (membersLoading || phase === 'loading') {
    return (
      <div style={stackLg}>
        <Skeleton label="بارگذاری شاخص‌های عملیاتی" height={92} />
        <Skeleton label="بارگذاری کنترل ورود" height={300} />
      </div>
    );
  }

  if (phase === 'error') {
    return (
      <div role="alert" data-testid="ops-error" style={stackLg}>
        <p style={{ color: 'var(--color-destructive)', margin: 0 }}>
          دریافت دادهٔ عملیات ناموفق بود. هسته را بررسی کنید.
        </p>
        <MotionButton onClick={refresh}>تلاش دوباره</MotionButton>
      </div>
    );
  }

  return (
    <div style={stackXl}>
      <OpsKpis
        today={today}
        memberCount={members.length}
        dash={dash}
        canSeeFinance={canSeeFinance}
      />
      <section style={PANEL_GRID}>
        <CheckinPanel members={members} onCheckedIn={refresh} />
        <PaymentPanel members={members} onPaid={refresh} />
      </section>
    </div>
  );
}

export default Operations;
