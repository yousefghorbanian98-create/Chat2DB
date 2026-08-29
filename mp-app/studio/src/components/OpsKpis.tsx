import type { Dashboard } from '../api/client';
import { formatRial } from '../ops/opsValidation';
import { StatCard } from './StatCard';

interface OpsKpisProps {
  today: number | null;
  memberCount: number;
  dash: Dashboard | null;
  /** Money KPIs are finance-only (map §2.4). */
  canSeeFinance: boolean;
}

/** The KPI strip. Every number is the server's, never recomputed here. */
export function OpsKpis({ today, memberCount, dash, canSeeFinance }: OpsKpisProps) {
  return (
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
      <StatCard labelFa="اعضا" labelEn="members" value={String(memberCount)} />
      {canSeeFinance && dash ? (
        <>
          <StatCard labelFa="اعضای فعال" labelEn="active" value={String(dash.members_active)} />
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
  );
}

export default OpsKpis;
