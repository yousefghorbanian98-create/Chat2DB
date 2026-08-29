import { motion, useReducedMotion, type MotionStyle } from 'framer-motion';
import type { CSSProperties } from 'react';

import type {
  DryRunResult,
  GeneratedProgram,
  Member,
  ProgramRow,
  ProgramTemplate,
} from '../api/client';
import { MotionButton, type ButtonState } from '../components/MotionButton';
import { ProgramPreview } from '../components/ProgramPreview';
import { Skeleton } from '../components/Skeleton';
import { useMembers } from '../hooks/useMembers';
import { useProgramPlanner } from '../hooks/useProgramPlanner';
import { fieldLabel, muted, stackLg } from '../styles/blocks';

const TEMPLATES: ReadonlyArray<{ code: ProgramTemplate; fa: string }> = [
  { code: 'ppl', fa: 'فشار / کشش / پا' },
  { code: 'ul', fa: 'بالاتنه / پایین‌تنه' },
  { code: 'fb', fa: 'فول بادی' },
  { code: 'corrective', fa: 'حرکتی اصلاحی' },
];

const PAGE: CSSProperties = { display: 'flex', flexDirection: 'column', gap: 'var(--space-xl)' };
const CONTROL_ROW: CSSProperties = {
  display: 'flex',
  flexWrap: 'wrap',
  gap: 'var(--space-lg)',
  alignItems: 'end',
};
const MEMBER_FIELD: CSSProperties = { ...fieldLabel, minWidth: 240 };
const CHIP_ROW: CSSProperties = { display: 'flex', flexWrap: 'wrap', gap: 8 };
const FIELDSET: CSSProperties = { border: 'none', padding: 0, margin: 0 };
const BUTTON_ROW: CSSProperties = { display: 'flex', flexWrap: 'wrap', gap: 'var(--space-md)' };
const NOTICE: MotionStyle = { margin: 0, fontSize: 14 };
const HISTORY_LIST: CSSProperties = { margin: 0, paddingInlineStart: 18, lineHeight: 1.8 };

/** Athlete picker for the planner. */
function MemberField({
  members,
  memberId,
  onChange,
}: {
  members: Member[];
  memberId: number | null;
  onChange: (id: number | null) => void;
}) {
  return (
    <label style={MEMBER_FIELD}>
      <span>عضو</span>
      <select
        data-testid="programs-member"
        className="mp-input"
        value={memberId ?? ''}
        onChange={(e) => onChange(e.target.value ? Number(e.target.value) : null)}
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

/** Split-template chips. */
function TemplatePicker({
  template,
  onSelect,
}: {
  template: ProgramTemplate;
  onSelect: (t: ProgramTemplate) => void;
}) {
  return (
    <fieldset style={FIELDSET}>
      <legend style={{ fontSize: 13, color: 'var(--color-muted-foreground)' }}>قالب</legend>
      <div style={CHIP_ROW}>
        {TEMPLATES.map((t) => {
          const active = template === t.code;
          return (
            <button
              key={t.code}
              type="button"
              className="mp-chip"
              data-testid={`template-${t.code}`}
              aria-pressed={active}
              onClick={() => onSelect(t.code)}
              style={{
                background: active ? 'var(--color-accent)' : 'transparent',
                color: active ? 'var(--color-on-accent)' : 'var(--color-foreground)',
              }}
            >
              {t.fa}
            </button>
          );
        })}
      </div>
    </fieldset>
  );
}

/** The generate bar: athlete, template, go. */
function PlannerControls(props: {
  members: Member[];
  memberId: number | null;
  template: ProgramTemplate;
  genState: ButtonState;
  onMember: (id: number | null) => void;
  onTemplate: (t: ProgramTemplate) => void;
  onGenerate: () => void;
}) {
  return (
    <div style={CONTROL_ROW}>
      <MemberField members={props.members} memberId={props.memberId} onChange={props.onMember} />
      <TemplatePicker template={props.template} onSelect={props.onTemplate} />
      <MotionButton
        onClick={props.onGenerate}
        state={props.genState}
        disabled={props.memberId === null}
      >
        ساخت برنامه
      </MotionButton>
    </div>
  );
}

/** Dry-run verdict — the gate that decides whether apply is reachable. */
function DryRunVerdict({
  check,
  safeToApply,
}: {
  check: DryRunResult | null;
  safeToApply: boolean;
}) {
  if (!check) {
    return (
      <p style={{ ...muted, margin: 0, fontSize: 13 }}>اعمال فقط بعد از بررسی ایمنی فعال می‌شود.</p>
    );
  }
  return (
    <p
      data-testid="dryrun-result"
      role="status"
      style={{
        margin: 0,
        fontSize: 14,
        color: safeToApply ? 'var(--color-accent)' : 'var(--color-destructive)',
      }}
    >
      {safeToApply
        ? 'ایمن برای اعمال — هیچ حرکتی با فیلترهای فعلی تضاد ندارد.'
        : `ناایمن — تازه مسدودشده: ${check.newly_blocked.join(', ')}`}
    </p>
  );
}

/** Draft + the dry-run/apply pair. Apply is disabled until the gate opens. */
function DraftSection(props: {
  draft: GeneratedProgram;
  check: DryRunResult | null;
  safeToApply: boolean;
  applyState: ButtonState;
  onDryRun: () => void;
  onApply: () => void;
}) {
  return (
    <div style={stackLg}>
      <ProgramPreview program={props.draft} />
      <div style={BUTTON_ROW}>
        <MotionButton variant="ghost" onClick={props.onDryRun}>
          بررسی ایمنی (dry-run)
        </MotionButton>
        <MotionButton
          onClick={props.onApply}
          state={props.applyState}
          disabled={!props.safeToApply}
        >
          تأیید و اعمال
        </MotionButton>
      </div>
      <DryRunVerdict check={props.check} safeToApply={props.safeToApply} />
    </div>
  );
}

/** Previously generated programs for this athlete. */
function ProgramHistory({ history }: { history: ProgramRow[] }) {
  return (
    <section data-testid="program-history" style={{ fontSize: 13 }}>
      <h3 style={{ fontSize: 16, marginBottom: 8 }}>تاریخچه</h3>
      {history.length === 0 ? (
        <p style={{ ...muted, margin: 0 }}>هنوز برنامه‌ای نیست.</p>
      ) : (
        <ul style={HISTORY_LIST}>
          {history.map((p) => (
            <li key={p.id}>
              #{p.id} · {p.title} · <strong>{p.status}</strong> · <span dir="ltr">{p.source}</span>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}

/** Apply is only offered after a dry-run said it is safe (rules C6 + C8). */
export function Programs() {
  const reduced = useReducedMotion() ?? false;
  const { members, loading } = useMembers();
  const p = useProgramPlanner();

  if (loading) return <Skeleton label="بارگذاری برنامه‌ها" height={320} />;

  return (
    <div style={PAGE}>
      <PlannerControls
        members={members}
        memberId={p.memberId}
        template={p.template}
        genState={p.genState}
        onMember={p.setMemberId}
        onTemplate={p.setTemplate}
        onGenerate={p.generate}
      />

      {p.notice ? (
        <motion.p
          role="status"
          data-testid="programs-notice"
          initial={reduced ? false : { opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          style={NOTICE}
        >
          {p.notice}
        </motion.p>
      ) : null}

      {p.draft ? (
        <DraftSection
          draft={p.draft}
          check={p.check}
          safeToApply={p.safeToApply}
          applyState={p.applyState}
          onDryRun={p.dryRun}
          onApply={p.apply}
        />
      ) : (
        <p style={{ ...muted, margin: 0 }}>
          یک عضو و قالب انتخاب کنید تا برنامهٔ قانون‌محور ساخته شود.
        </p>
      )}

      <ProgramHistory history={p.history} />
    </div>
  );
}

export default Programs;
