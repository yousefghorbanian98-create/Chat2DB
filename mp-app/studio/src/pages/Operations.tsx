import { useCallback, useEffect, useState } from 'react';

import { api, type Dashboard, type Member } from '../api/client';
import { CheckinPanel } from '../components/CheckinPanel';
import { MotionButton } from '../components/MotionButton';
import { PaymentPanel } from '../components/PaymentPanel';
import { Skeleton } from '../components/Skeleton';
import { StatCard } from '../components/StatCard';
import { useAuth } from '../auth/AuthContext';
import { formatRial } from '../ops/opsValidation';

type Phase = 'loading' | 'ready' | 'error';

/** Finance roles see money KPIs; everyone else gets door KPIs only (§2.4). */
const FINANCE_ROLES = new Set(['OWNER', 'ADMIN']);

/**
 * Operations console (Phase 2): door control + cash desk + live KPIs.
 * KPI numbers come from the server, never from the client (no invented maths).
 */
export function Operations() {
  const { role } = useAuth();
  const [members, setMembers] = useState<Member[]>([]);
  const [dash, setDash] = useState<Dashboard | null>(null);
  const [today, setToday] = useState<number | null>(null);
  const [phase, setPhase] = useState<Phase>('loading');

  const canSeeFinance = role !== null && FINANCE_ROLES.has(role);

  const refresh = useCallback(async () => {
    try {
      const [list, todayRes] = await Promise.all([api.listMembers(), api.attendanceToday()]);
      setMembers(list);
      setToday(todayRes.check_ins);
      if (canSeeFinance) {
        try {
          setDash(await api.dashboard());
        } catch {
          setDash(null); // finance block must not break the door controls
        }
      }
      setPhase('ready');
    } catch {
      setPhase('error');
    }
  }, [canSeeFinance]);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  if (phase === 'loading') {
    return (
      <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-lg)' }}>
        <Skeleton label="بارگذاری شاخص‌های عملیاتی" height={92} />
        <Skeleton label="بارگذاری کنترل ورود" height={300} />
      </div>
    );
  }

  if (phase === 'error') {
    return (
      <div
        role="alert"
        data-testid="ops-error"
        style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-lg)' }}
      >
        <p style={{ color: 'var(--color-destructive)', margin: 0 }}>
          دریافت دادهٔ عملیات ناموفق بود. هسته را بررسی کنید.
        </p>
        <MotionButton onClick={() => void refresh()}>تلاش دوباره</MotionButton>
      </div>
    );
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-xl)' }}>
      <section
        data-testid="ops-kpis"
        style={{ display: 'flex', flexWrap: 'wrap', gap: 'var(--space-lg)' }}
      >
        <StatCard
          labelFa="ورودی امروز"
          labelEn="check-ins today"
          value={String(today ?? 0)}
          tone="primary"
        />
        <StatCard labelFa="اعضا" labelEn="members" value={String(members.length)} />
        {canSeeFinance && dash ? (
          <>
            <StatCard
              labelFa="اعضای فعال"
              labelEn="active"
              value={String(dash.members_active)}
            />
            <StatCard
              labelFa="درآمد این ماه"
              labelEn="revenue"
              value={formatRial(dash.revenue_rial_this_month)}
              unit="ریال"
              tone="gold"
            />
            <StatCard
              labelFa="آسیب فعال"
              labelEn="injuries"
              value={String(dash.members_with_active_injury)}
            />
          </>
        ) : null}
      </section>

      <section
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))',
          gap: 'var(--space-xl)',
          alignItems: 'start',
        }}
      >
        <CheckinPanel members={members} onCheckedIn={() => void refresh()} />
        <PaymentPanel members={members} onPaid={() => void refresh()} />
      </section>
    </div>
  );
}

export default Operations;
