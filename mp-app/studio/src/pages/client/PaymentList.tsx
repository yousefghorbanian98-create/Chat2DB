import type { ClientPayment } from '../../api/client';
import { faDate } from '../../core/jalali';
import { formatRial } from '../../ops/opsValidation';
import { cardSection, cardTitle, muted } from '../../styles/blocks';

const LIST: React.CSSProperties = { margin: 0, paddingInlineStart: 0, listStyle: 'none' };
const ROW: React.CSSProperties = {
  display: 'flex',
  justifyContent: 'space-between',
  alignItems: 'baseline',
  gap: 'var(--space-md)',
  paddingBlock: 'var(--space-sm)',
  borderBottom: '1px solid var(--color-border)',
};

const METHOD_FA: Record<string, string> = {
  cash: 'نقدی',
  card: 'کارت',
  transfer: 'کارت‌به‌کارت',
  pos: 'دستگاه کارت‌خوان',
};

/**
 * The athlete's payment history.
 *
 * `staff_id` is masked server-side (C11) — who typed the receipt at the desk is
 * internal bookkeeping, not the member's business.
 */
export function PaymentList({ rows }: { rows: ClientPayment[] }) {
  return (
    <section className="glass" style={cardSection} data-testid="client-payments">
      <h3 style={cardTitle}>سوابق پرداخت من</h3>
      {rows.length === 0 ? (
        <p style={muted}>هنوز پرداختی ثبت نشده است.</p>
      ) : (
        <ul style={LIST}>
          {rows.map((p) => (
            <li key={p.id} style={ROW}>
              <div>
                <span className="numeric" style={{ color: 'var(--color-accent)' }}>
                  {formatRial(p.amount_rial)}
                </span>{' '}
                <span style={muted}>ریال · {METHOD_FA[p.method] ?? p.method}</span>
                <div style={muted}>
                  <span className="numeric">{faDate(p.created_at)}</span> — رسید{' '}
                  <span className="numeric">{p.receipt_no}</span>
                </div>
              </div>
              {p.voided ? (
                <span style={{ color: 'var(--color-destructive)' }}>باطل‌شده</span>
              ) : null}
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}

export default PaymentList;
