import { motion, useReducedMotion } from 'framer-motion';
import { useState } from 'react';

import { api, ApiError, type Member } from '../api/client';
import { qrLooksComplete } from '../ops/opsValidation';
import { MotionButton, type ButtonState } from './MotionButton';
import { MotionCard } from './MotionCard';

interface CheckinPanelProps {
  members: Member[];
  /** Called after a successful check-in so the KPI strip can refresh. */
  onCheckedIn: () => void;
}

type Outcome = { kind: 'ok'; text: string } | { kind: 'fail'; text: string } | null;

/** Translate the door-facing HTTP codes into Persian the reception can act on. */
function describeError(err: unknown): string {
  if (err instanceof ApiError) {
    if (err.status === 402) return 'اشتراک منقضی شده — تمدید در پذیرش';
    if (err.status === 409) return 'این عضو همین حالا داخل باشگاه است';
    if (err.status === 401) return 'QR نامعتبر یا دستکاری‌شده';
    if (err.status === 404) return 'عضو پیدا نشد';
    return err.detail;
  }
  return 'خطای ناشناخته';
}

/**
 * Door control: manual check-in for the desk plus a signed-QR path for the
 * kiosk scanner. Both surface loading/error/empty/success (FINN-LOOP).
 */
export function CheckinPanel({ members, onCheckedIn }: CheckinPanelProps) {
  const reduced = useReducedMotion() ?? false;
  const [memberId, setMemberId] = useState<number | null>(null);
  const [qrText, setQrText] = useState('');
  const [state, setState] = useState<ButtonState>('idle');
  const [outcome, setOutcome] = useState<Outcome>(null);

  async function run(task: () => Promise<unknown>, okText: string) {
    setState('loading');
    setOutcome(null);
    try {
      await task();
      setState('success');
      setOutcome({ kind: 'ok', text: okText });
      onCheckedIn();
    } catch (err) {
      setState('error');
      setOutcome({ kind: 'fail', text: describeError(err) });
    }
  }

  function submitQr() {
    let payload: Record<string, unknown>;
    try {
      payload = JSON.parse(qrText) as Record<string, unknown>;
    } catch {
      setState('error');
      setOutcome({ kind: 'fail', text: 'JSON نامعتبر — خروجی اسکنر را بچسبانید' });
      return;
    }
    if (!qrLooksComplete(payload)) {
      setState('error');
      setOutcome({ kind: 'fail', text: 'QR فاقد فیلدهای امضاشده (mid/gym/exp/sig)' });
      return;
    }
    void run(() => api.checkInQr(payload), 'چک‌این با QR انجام شد');
  }

  return (
    <MotionCard title="کنترل ورود" testId="checkin-panel">
      {members.length === 0 ? (
        <p data-testid="checkin-empty" style={{ color: 'var(--color-muted-foreground)' }}>
          هنوز عضوی ثبت نشده است.
        </p>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-lg)' }}>
          <label style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
            <span style={{ fontSize: 13, color: 'var(--color-muted-foreground)' }}>عضو</span>
            <select
              data-testid="checkin-member"
              value={memberId ?? ''}
              onChange={(e) => setMemberId(e.target.value ? Number(e.target.value) : null)}
              className="mp-input"
            >
              <option value="">— انتخاب کنید —</option>
              {members.map((m) => (
                <option key={m.id} value={m.id}>
                  {m.first_name} {m.last_name} · {m.membership_code}
                </option>
              ))}
            </select>
          </label>

          <MotionButton
            onClick={() =>
              memberId !== null &&
              void run(() => api.checkInManual(memberId), 'ورود ثبت شد')
            }
            disabled={memberId === null}
            state={state}
          >
            ثبت ورود
          </MotionButton>

          <label style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
            <span style={{ fontSize: 13, color: 'var(--color-muted-foreground)' }}>
              یا چسباندن QR امضاشده
            </span>
            <textarea
              data-testid="checkin-qr"
              className="mp-input"
              dir="ltr"
              rows={3}
              value={qrText}
              onChange={(e) => setQrText(e.target.value)}
              placeholder='{"typ":"member","gym":1,"mid":7,"exp":0,"sig":"…"}'
            />
          </label>
          <MotionButton variant="ghost" onClick={submitQr} disabled={qrText.trim() === ''}>
            چک‌این با QR
          </MotionButton>

          {outcome && (
            <motion.p
              role={outcome.kind === 'fail' ? 'alert' : 'status'}
              data-testid="checkin-outcome"
              initial={reduced ? false : { opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              style={{
                margin: 0,
                color:
                  outcome.kind === 'ok'
                    ? 'var(--color-accent)'
                    : 'var(--color-destructive)',
              }}
            >
              {outcome.text}
            </motion.p>
          )}
        </div>
      )}
    </MotionCard>
  );
}

export default CheckinPanel;
