import { motion, useReducedMotion } from 'framer-motion';
import type { CSSProperties } from 'react';
import type { MotionStyle } from 'framer-motion';

import type { Member, MembershipPackage, Payment } from '../api/client';
import { formatRial, type PaymentDraft } from '../ops/opsValidation';
import { usePayment } from '../hooks/usePayment';
import { MotionButton } from './MotionButton';
import { MotionCard } from './MotionCard';
import { fieldLabel, muted, stackLg } from '../styles/blocks';

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

const CHIPS: CSSProperties = { display: 'flex', flexWrap: 'wrap', gap: 8 };
const FIELDSET: CSSProperties = { border: 'none', padding: 0, margin: 0 };
const ALERT: MotionStyle = { margin: 0, color: 'var(--color-destructive)' };

/** Quick-pick package chips, or a note that none are defined yet. */
function PackageChips({
  packages,
  onPick,
}: {
  packages: MembershipPackage[];
  onPick: (p: MembershipPackage) => void;
}) {
  if (packages.length === 0) {
    return (
      <p style={{ ...muted, margin: 0, fontSize: 13 }}>
        بسته‌ای تعریف نشده — مبلغ را دستی وارد کنید.
      </p>
    );
  }
  return (
    <div style={CHIPS}>
      {packages.map((p) => (
        <button
          key={p.id}
          type="button"
          className="mp-btn mp-btn-ghost mp-chip"
          data-testid={`package-${p.id}`}
          onClick={() => onPick(p)}
        >
          {p.name} ·{' '}
          <span className="numeric" dir="ltr">
            {formatRial(p.price_rial)}
          </span>
        </button>
      ))}
    </div>
  );
}

/** Method radio group rendered as chips. */
function MethodPicker({
  method,
  onSelect,
}: {
  method: PaymentDraft['method'];
  onSelect: (m: PaymentDraft['method']) => void;
}) {
  return (
    <fieldset style={FIELDSET}>
      <legend style={{ fontSize: 13, color: 'var(--color-muted-foreground)' }}>روش</legend>
      <div style={CHIPS}>
        {METHODS.map((m) => {
          const active = method === m.id;
          return (
            <button
              key={m.id}
              type="button"
              className="mp-btn mp-chip"
              data-testid={`method-${m.id}`}
              aria-pressed={active}
              onClick={() => onSelect(m.id)}
              style={{
                background: active ? 'var(--color-accent)' : 'transparent',
                color: active ? 'var(--color-on-accent)' : 'var(--color-foreground)',
                border: '1px solid var(--color-border-subtle)',
              }}
            >
              {m.fa}
            </button>
          );
        })}
      </div>
    </fieldset>
  );
}

/** Receipt line with the PDF link — the proof the cashier hands over. */
function PaymentReceipt({ paid, reduced }: { paid: Payment; reduced: boolean }) {
  return (
    <motion.div
      role="status"
      data-testid="payment-success"
      initial={reduced ? false : { opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      style={{ fontSize: 14 }}
    >
      پرداخت{' '}
      <span className="numeric" dir="ltr">
        {formatRial(paid.amount_rial)}
      </span>{' '}
      ریال ثبت شد
      {paid.receipt_no ? (
        <>
          {' '}
          · رسید{' '}
          <span className="numeric" dir="ltr">
            {paid.receipt_no}
          </span>{' '}
          <a href={`/api/v1/payments/${paid.id}/receipt`} target="_blank" rel="noreferrer">
            دریافت PDF
          </a>
        </>
      ) : null}
    </motion.div>
  );
}

interface PaymentFieldsProps {
  draft: PaymentDraft;
  members: Member[];
  onChange: (updater: (d: PaymentDraft) => PaymentDraft) => void;
}

/** Payer + amount, kept as one unit because they validate together. */
function PaymentFields({ draft, members, onChange }: PaymentFieldsProps) {
  return (
    <>
      <label style={fieldLabel}>
        <span>عضو</span>
        <select
          data-testid="payment-member"
          className="mp-input"
          value={draft.memberId ?? ''}
          onChange={(e) =>
            onChange((d) => ({ ...d, memberId: e.target.value ? Number(e.target.value) : null }))
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

      <label style={fieldLabel}>
        <span>مبلغ (ریال)</span>
        <input
          data-testid="payment-amount"
          className="mp-input numeric"
          inputMode="numeric"
          dir="ltr"
          value={draft.amountRial}
          onChange={(e) => onChange((d) => ({ ...d, amountRial: e.target.value }))}
          placeholder="500,000"
        />
      </label>
    </>
  );
}

/** Front-desk cash entry: package quick-pick, Rial amount, receipt link. */
export function PaymentPanel({ members, onPaid }: PaymentPanelProps) {
  const reduced = useReducedMotion() ?? false;
  const { packages, draft, state, paid, error, setDraft, pickPackage, submit } = usePayment(onPaid);

  return (
    <MotionCard title="پرداخت و تمدید" testId="payment-panel">
      <div style={stackLg}>
        <PackageChips packages={packages} onPick={pickPackage} />

        <PaymentFields draft={draft} members={members} onChange={setDraft} />

        <MethodPicker
          method={draft.method}
          onSelect={(m) => setDraft((d) => ({ ...d, method: m }))}
        />

        <MotionButton onClick={submit} state={state}>
          ثبت پرداخت
        </MotionButton>

        {error ? (
          <motion.p
            role="alert"
            data-testid="payment-error"
            initial={reduced ? false : { opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            style={ALERT}
          >
            {error}
          </motion.p>
        ) : null}

        {paid ? <PaymentReceipt paid={paid} reduced={reduced} /> : null}
      </div>
    </MotionCard>
  );
}

export default PaymentPanel;
