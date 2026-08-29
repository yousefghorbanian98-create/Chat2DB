import { motion, useReducedMotion } from 'framer-motion';
import { useState } from 'react';

import type { Member } from '../api/client';
import type { ButtonState } from './MotionButton';
import { MotionButton } from './MotionButton';
import { MotionCard } from './MotionCard';
import { useCheckin, type Outcome } from '../hooks/useCheckin';
import { fieldLabel, muted, stackLg } from '../styles/blocks';

interface CheckinPanelProps {
  members: Member[];
  /** Called after a successful check-in so the KPI strip can refresh. */
  onCheckedIn: () => void;
}

const QR_PLACEHOLDER = '{"typ":"member","gym":1,"mid":7,"exp":0,"sig":"…"}';

/** The athlete dropdown at the door. */
function MemberPicker({
  members,
  memberId,
  onSelect,
}: {
  members: Member[];
  memberId: number | null;
  onSelect: (id: number | null) => void;
}) {
  return (
    <label style={fieldLabel}>
      <span>عضو</span>
      <select
        data-testid="checkin-member"
        value={memberId ?? ''}
        onChange={(e) => onSelect(e.target.value ? Number(e.target.value) : null)}
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
  );
}

/** Kiosk path: paste the scanner's signed payload instead of scanning. */
function QrPaste({
  value,
  onChange,
  onSubmit,
}: {
  value: string;
  onChange: (v: string) => void;
  onSubmit: () => void;
}) {
  return (
    <>
      <label style={fieldLabel}>
        <span>یا چسباندن QR امضاشده</span>
        <textarea
          data-testid="checkin-qr"
          className="mp-input"
          dir="ltr"
          rows={3}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          placeholder={QR_PLACEHOLDER}
        />
      </label>
      <MotionButton variant="ghost" onClick={onSubmit} disabled={value.trim() === ''}>
        چک‌این با QR
      </MotionButton>
    </>
  );
}

/** Door result line: green on success, red with an actionable reason on failure. */
function OutcomeLine({ outcome, reduced }: { outcome: Outcome; reduced: boolean }) {
  if (!outcome) return null;
  const ok = outcome.kind === 'ok';
  return (
    <motion.p
      role={ok ? 'status' : 'alert'}
      data-testid="checkin-outcome"
      initial={reduced ? false : { opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      style={{ margin: 0, color: ok ? 'var(--color-accent)' : 'var(--color-destructive)' }}
    >
      {outcome.text}
    </motion.p>
  );
}

interface PanelBodyProps {
  members: Member[];
  memberId: number | null;
  onSelect: (id: number | null) => void;
  state: ButtonState;
  outcome: Outcome;
  qrText: string;
  setQrText: (v: string) => void;
  onManual: () => void;
  onSubmitQr: () => void;
  reduced: boolean;
}

/** The two check-in paths plus their shared result line. */
function PanelBody(props: PanelBodyProps) {
  return (
    <div style={stackLg}>
      <MemberPicker members={props.members} memberId={props.memberId} onSelect={props.onSelect} />
      <MotionButton onClick={props.onManual} disabled={props.memberId === null} state={props.state}>
        ثبت ورود
      </MotionButton>
      <QrPaste value={props.qrText} onChange={props.setQrText} onSubmit={props.onSubmitQr} />
      <OutcomeLine outcome={props.outcome} reduced={props.reduced} />
    </div>
  );
}

/**
 * Door control: manual check-in for the desk plus a signed-QR path for the
 * kiosk scanner. Both surface loading/error/empty/success (FINN-LOOP).
 */
export function CheckinPanel({ members, onCheckedIn }: CheckinPanelProps) {
  const reduced = useReducedMotion() ?? false;
  const [memberId, setMemberId] = useState<number | null>(null);
  const { state, outcome, qrText, setQrText, checkInManual, submitQr } = useCheckin(onCheckedIn);

  return (
    <MotionCard title="کنترل ورود" testId="checkin-panel">
      {members.length === 0 ? (
        <p data-testid="checkin-empty" style={muted}>
          هنوز عضوی ثبت نشده است.
        </p>
      ) : (
        <PanelBody
          members={members}
          memberId={memberId}
          onSelect={setMemberId}
          state={state}
          outcome={outcome}
          qrText={qrText}
          setQrText={setQrText}
          onManual={() => memberId !== null && checkInManual(memberId)}
          onSubmitQr={submitQr}
          reduced={reduced}
        />
      )}
    </MotionCard>
  );
}

export default CheckinPanel;
