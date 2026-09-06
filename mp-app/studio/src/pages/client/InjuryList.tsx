import type { Injury } from '../../api/client';
import { cardSection, cardTitle, muted } from '../../styles/blocks';

const LIST: React.CSSProperties = { margin: 0, paddingInlineStart: 0, listStyle: 'none' };
const ROW: React.CSSProperties = {
  display: 'flex',
  flexDirection: 'column',
  gap: 4,
  paddingBlock: 'var(--space-sm)',
  borderBottom: '1px solid var(--color-border)',
};
const CHIPS: React.CSSProperties = { display: 'flex', flexWrap: 'wrap', gap: 6 };

const REGION_FA: Record<string, string> = {
  lumbar: 'کمر',
  cervical: 'گردن',
  shoulder: 'شانه',
  knee: 'زانو',
  hip: 'لگن',
  ankle: 'مچ پا',
  wrist: 'مچ دست',
  elbow: 'آرنج',
};

const STATUS_FA: Record<string, string> = {
  active: 'فعال',
  healing: 'در حال بهبود',
  cleared: 'رفع شده',
};

/** A restriction chip — these drive the planner's hard filters (C6). */
function Chip({ text, tone }: { text: string; tone: 'danger' | 'ok' }) {
  return (
    <span
      className="chip"
      style={{
        color: tone === 'danger' ? 'var(--color-destructive)' : 'var(--color-success)',
        borderColor: tone === 'danger' ? 'var(--color-destructive)' : 'var(--color-success)',
      }}
    >
      {text}
    </span>
  );
}

/**
 * The athlete's own injuries and limitations.
 *
 * The clinician note is stripped server-side for a MEMBER role, so this list can
 * never show it — there is nothing here to hide by accident.
 */
export function InjuryList({ rows }: { rows: Injury[] }) {
  return (
    <section className="glass" style={cardSection} data-testid="client-injuries">
      <h3 style={cardTitle}>محدودیت‌های من</h3>
      {rows.length === 0 ? (
        <p style={muted}>هیچ محدودیتی برای شما ثبت نشده است.</p>
      ) : (
        <ul style={LIST}>
          {rows.map((i) => (
            <li key={i.id} style={ROW}>
              <strong>
                {i.label} — {REGION_FA[i.body_region] ?? i.body_region}
              </strong>
              <span style={muted}>وضعیت: {STATUS_FA[i.status] ?? i.status}</span>
              <div style={CHIPS}>
                {i.contraindicated_patterns.map((p) => (
                  <Chip key={p} text={`ممنوع: ${p}`} tone="danger" />
                ))}
              </div>
              {i.member_visible_note ? <span style={muted}>{i.member_visible_note}</span> : null}
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}

export default InjuryList;
