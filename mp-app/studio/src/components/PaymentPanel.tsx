import { motion, useReducedMotion } from 'framer-motion';
import { useEffect, useState } from 'react';

import { api, ApiError, type Member, type MembershipPackage, type Payment } from '../api/client';
import { formatRial, parseRial, validatePayment, emptyPaymentDraft, type PaymentDraft } from '../ops/opsValidation';
import { MotionButton, type ButtonState } from './MotionButton';
import { MotionCard } from './MotionCard';

interface PaymentPanelProps {
  members: Member[];
  onPaid: () => void;
}

const METHODS: ReadonlyArray<{ id: PaymentDraft['method']; fa: string }> = [
  { id: 'cash', fa: 'نقد' },
  { id: 'card', fa: 'کارت' },
  { id: 'transfer', fa: 'کارت‌به‌کارت' },
  { id: 'pos', fa: 'POS' },
];

/** Front-desk cash entry: package quick-pick, Rial amount, receipt link. */
export function PaymentPanel({ members, onPaid }: PaymentPanelProps) {
  const reduced = useReducedMotion() ?? false;
  const [packages, setPackages] = useState<MembershipPackage[]>([]);
  const [draft, setDraft] = useState<PaymentDraft>(emptyPaymentDraft);
  const [state, setState] = useState<ButtonState>('idle');
  const [paid, setPaid] = useState<Payment | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let alive = true;
    (async () => {
      try {
        const list = await api.listPackages();
        if (alive) setPackages(list);
      } catch {
        /* packages are optional; a cashier can still enter a free amount */
      }
    })();
    return () => {
      alive = false;
    };
  }, []);

  function pickPackage(pkg: MembershipPackage) {
    setDraft((d) => ({
      ...d,
      packageId: pkg.id,
      amountRial: String(pkg.price_rial),
    }));
  }

  async function submit() {
    const problems = validatePayment(draft);
    if (problems.length > 0) {
      setState('error');
      setError(problems[0]?.message ?? 'فرم ناقص است');
      return;
    }
    setState('loading');
    setError(null);
    try {
      // exactOptionalPropertyTypes: omit package_id entirely rather than
      // passing `undefined`.
      const body = {
        member_id: draft.memberId as number,
        amount_rial: parseRial(draft.amountRial) as number,
        method: draft.method,
        ...(draft.packageId === null ? {} : { package_id: draft.packageId }),
      };
      const res = await api.recordPayment(body);
      setPaid(res);
      setState('success');
      setDraft(emptyPaymentDraft);
      onPaid();
    } catch (err) {
      setState('error');
      setError(err instanceof ApiError ? err.detail : 'ثبت پرداخت ناموفق بود');
    }
  }

  return (
    <MotionCard title="پرداخت و تمدید" testId="payment-panel">
      <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-lg)' }}>
        {packages.length === 0 ? (
          <p style={{ margin: 0, color: 'var(--color-muted-foreground)', fontSize: 13 }}>
            بسته‌ای تعریف نشده — مبلغ را دستی وارد کنید.
          </p>
        ) : (
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
            {packages.map((p) => (
              <button
                key={p.id}
                type="button"
                className="mp-btn mp-btn-ghost mp-chip"
                data-testid={`package-${p.id}`}
                onClick={() => pickPackage(p)}
              >
                {p.name} · <span className="numeric" dir="ltr">{formatRial(p.price_rial)}</span>
              </button>
            ))}
          </div>
        )}

        <label style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
          <span style={{ fontSize: 13, color: 'var(--color-muted-foreground)' }}>عضو</span>
          <select
            data-testid="payment-member"
            className="mp-input"
            value={draft.memberId ?? ''}
            onChange={(e) =>
              setDraft((d) => ({
                ...d,
                memberId: e.target.value ? Number(e.target.value) : null,
              }))
            }
          >
            <option value="">— انتخاب کنید —</option>
            {members.map((m) => (
              <option key={m.id} value={m.id}>
                {m.first_name} {m.last_name} · {m.membership_code}
              </option>
            ))}
          </select>
        </label>

        <label style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
          <span style={{ fontSize: 13, color: 'var(--color-muted-foreground)' }}>
            مبلغ (ریال)
          </span>
          <input
            data-testid="payment-amount"
            className="mp-input numeric"
            inputMode="numeric"
            dir="ltr"
            value={draft.amountRial}
            onChange={(e) => setDraft((d) => ({ ...d, amountRial: e.target.value }))}
            placeholder="500,000"
          />
        </label>

        <fieldset style={{ border: 'none', padding: 0, margin: 0 }}>
          <legend style={{ fontSize: 13, color: 'var(--color-muted-foreground)' }}>روش</legend>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
            {METHODS.map((m) => (
              <button
                key={m.id}
                type="button"
                className="mp-btn mp-chip"
                data-testid={`method-${m.id}`}
                aria-pressed={draft.method === m.id}
                onClick={() => setDraft((d) => ({ ...d, method: m.id }))}
                style={{
                  background:
                    draft.method === m.id ? 'var(--color-accent)' : 'transparent',
                  color:
                    draft.method === m.id
                      ? 'var(--color-on-accent)'
                      : 'var(--color-foreground)',
                  border: '1px solid var(--color-border-subtle)',
                }}
              >
                {m.fa}
              </button>
            ))}
          </div>
        </fieldset>

        <MotionButton onClick={() => void submit()} state={state}>
          ثبت پرداخت
        </MotionButton>

        {error && (
          <motion.p
            role="alert"
            data-testid="payment-error"
            initial={reduced ? false : { opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            style={{ margin: 0, color: 'var(--color-destructive)' }}
          >
            {error}
          </motion.p>
        )}

        {paid && (
          <motion.div
            role="status"
            data-testid="payment-success"
            initial={reduced ? false : { opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            style={{ fontSize: 14 }}
          >
            پرداخت{' '}
            <span className="numeric" dir="ltr">{formatRial(paid.amount_rial)}</span> ریال ثبت شد
            {paid.receipt_no ? (
              <>
                {' '}· رسید <span className="numeric" dir="ltr">{paid.receipt_no}</span>{' '}
                <a href={`/api/v1/payments/${paid.id}/receipt`} target="_blank" rel="noreferrer">
                  دریافت PDF
                </a>
              </>
            ) : null}
          </motion.div>
        )}
      </div>
    </MotionCard>
  );
}

export default PaymentPanel;
