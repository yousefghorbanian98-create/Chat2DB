import { motion, useReducedMotion, type MotionStyle } from 'framer-motion';

import { stackLg } from '../styles/blocks';

import type { CSSProperties } from 'react';

import type { DroppedExercise, GeneratedProgram, ProgramDayPreview } from '../api/client';

interface ProgramPreviewProps {
  program: GeneratedProgram;
}

const TEMPLATE_FA: Record<string, string> = {
  ppl: 'فشار / کشش / پا',
  ul: 'بالاتنه / پایین‌تنه',
  fb: 'فول بادی',
  corrective: 'حرکتی اصلاحی',
};

const REASON_FA: Record<string, string> = {
  hard_block: 'الگوی حرکتی به‌دلیل آسیب مسدود است',
  injury_block: 'به‌دلیل آسیب حذف شد',
  equipment: 'تجهیز موجود نیست',
  no_candidate: 'جایگزین مناسبی در کتابخانه نبود',
  duplicate: 'حرکت تکراری',
};

/** Persian label for a drop reason, falling back to the raw token. */
function reasonFa(reason: string | undefined): string {
  if (!reason) return 'حذف شد';
  return REASON_FA[reason] ?? reason;
}

const CHIP: CSSProperties = { minHeight: 28, padding: '2px 12px', fontSize: 12 };
const HEAD_ROW: CSSProperties = {
  display: 'flex',
  flexWrap: 'wrap',
  gap: 8,
  alignItems: 'center',
};
const BANNER: MotionStyle = {
  margin: 0,
  padding: '10px 14px',
  borderRadius: 'var(--radius-sm)',
  background: 'rgba(255, 176, 32, 0.12)',
  border: '1px solid rgba(255, 176, 32, 0.35)',
  fontSize: 13,
};

/** Template name + id/status chips + the corrective-block marker. */
function PreviewHeader({ program }: { program: GeneratedProgram }) {
  return (
    <div style={HEAD_ROW}>
      <strong style={{ fontFamily: 'var(--font-display)' }}>
        {TEMPLATE_FA[program.template] ?? program.template}
      </strong>
      <span className="mp-chip" style={CHIP}>
        #{program.id}
      </span>
      <span className="mp-chip" style={CHIP}>
        {program.status}
      </span>
      {program.meta.corrective_block_added ? (
        <span className="mp-chip" style={CHIP}>
          بلوک اصلاحی اضافه شد
        </span>
      ) : null}
    </div>
  );
}

/** The injury filters that were in force when this program was built. */
function BlockedBanner({ patterns, reduced }: { patterns: string[]; reduced: boolean }) {
  if (patterns.length === 0) return null;
  return (
    <motion.p
      data-testid="blocked-patterns"
      initial={reduced ? false : { opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      style={BANNER}
    >
      فیلترهای آسیب فعال:{' '}
      <span dir="ltr" className="numeric">
        {patterns.join(', ')}
      </span>
    </motion.p>
  );
}

const DAY_STACK: CSSProperties = {
  display: 'flex',
  flexDirection: 'column',
  gap: 'var(--space-md)',
};
const DAY_CARD: CSSProperties = {
  padding: 'var(--space-md)',
  borderRadius: 'var(--radius-sm)',
  border: '1px solid var(--color-border-subtle)',
};
const DAY_HEAD: CSSProperties = { fontSize: 13, color: 'var(--color-muted-foreground)' };
const EX_LIST: CSSProperties = {
  margin: '6px 0 0',
  paddingInlineStart: 18,
  fontSize: 13,
  lineHeight: 1.7,
};

/** One training day: its name, how many slots survived, and the exercises. */
function DayCard({ day }: { day: ProgramDayPreview }) {
  return (
    <div style={DAY_CARD}>
      <div style={DAY_HEAD}>
        روز <span dir="ltr">{day.name}</span> · {day.exercises.length} حرکت
      </div>
      {day.exercises.length === 0 ? (
        <p style={{ margin: '6px 0 0', fontSize: 13 }}>حرکتی باقی نماند.</p>
      ) : (
        <ul dir="ltr" className="numeric" style={EX_LIST}>
          {day.exercises.map((key) => (
            <li key={key}>{key}</li>
          ))}
        </ul>
      )}
    </div>
  );
}

/** Every exercise the filters removed, with the reason — the trust surface. */
function DroppedList({ dropped }: { dropped: Array<DroppedExercise & { day: string }> }) {
  return (
    <div data-testid="dropped-list" style={{ fontSize: 13 }}>
      <div style={{ ...DAY_HEAD, marginBottom: 6 }}>حذف‌شده‌ها ({dropped.length}):</div>
      <ul style={{ margin: 0, paddingInlineStart: 18, lineHeight: 1.7 }}>
        {dropped.map((d, i) => (
          <li key={`${d.day ?? ''}-${d.exercise ?? i}`}>
            <span dir="ltr" className="numeric">
              {d.day ?? ''} / {d.exercise ?? '—'}
            </span>{' '}
            — {reasonFa(d.reason)}
          </li>
        ))}
      </ul>
    </div>
  );
}

/**
 * Read-only preview of a generated program: the days the coach will approve,
 * every exercise the filters dropped (and why), and the injury filters that
 * were in force. Transparency here is the point of the dry-run rule (C6/C8).
 */
export function ProgramPreview({ program }: ProgramPreviewProps) {
  const reduced = useReducedMotion() ?? false;
  const dropped = program.meta.dropped;

  return (
    <div data-testid="program-preview" style={stackLg}>
      <PreviewHeader program={program} />

      <BlockedBanner patterns={program.meta.blocked_patterns} reduced={reduced} />

      <div style={DAY_STACK}>
        {program.days.map((day) => (
          <DayCard key={day.name} day={day} />
        ))}
      </div>

      {dropped.length === 0 ? (
        <p data-testid="no-drops" style={{ margin: 0, fontSize: 13, color: 'var(--color-accent)' }}>
          هیچ حرکتی حذف نشد.
        </p>
      ) : (
        <DroppedList dropped={dropped} />
      )}
    </div>
  );
}

export default ProgramPreview;
