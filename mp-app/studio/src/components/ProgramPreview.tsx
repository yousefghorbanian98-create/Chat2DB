import { motion, useReducedMotion } from 'framer-motion';

import type { GeneratedProgram } from '../api/client';

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

/**
 * Read-only preview of a generated program: the days the coach will approve,
 * every exercise the filters dropped (and why), and the injury filters that
 * were in force. Transparency here is the point of the dry-run rule (C6/C8).
 */
export function ProgramPreview({ program }: ProgramPreviewProps) {
  const reduced = useReducedMotion() ?? false;
  const dropped = program.meta.dropped;

  return (
    <div
      data-testid="program-preview"
      style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-lg)' }}
    >
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8, alignItems: 'center' }}>
        <strong style={{ fontFamily: 'var(--font-display)' }}>
          {TEMPLATE_FA[program.template] ?? program.template}
        </strong>
        <span className="mp-chip" style={{ minHeight: 28, padding: '2px 12px', fontSize: 12 }}>
          #{program.id}
        </span>
        <span className="mp-chip" style={{ minHeight: 28, padding: '2px 12px', fontSize: 12 }}>
          {program.status}
        </span>
        {program.meta.corrective_block_added ? (
          <span
            className="mp-chip"
            style={{ minHeight: 28, padding: '2px 12px', fontSize: 12 }}
          >
            بلوک اصلاحی اضافه شد
          </span>
        ) : null}
      </div>

      {program.meta.blocked_patterns.length > 0 ? (
        <motion.p
          data-testid="blocked-patterns"
          initial={reduced ? false : { opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          style={{
            margin: 0,
            padding: '10px 14px',
            borderRadius: 'var(--radius-sm)',
            background: 'rgba(255, 176, 32, 0.12)',
            border: '1px solid rgba(255, 176, 32, 0.35)',
            fontSize: 13,
          }}
        >
          فیلترهای آسیب فعال:{' '}
          <span dir="ltr" className="numeric">
            {program.meta.blocked_patterns.join(', ')}
          </span>
        </motion.p>
      ) : null}

      <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-md)' }}>
        {program.days.map((day) => (
          <div
            key={day.name}
            style={{
              padding: 'var(--space-md)',
              borderRadius: 'var(--radius-sm)',
              border: '1px solid var(--color-border-subtle)',
            }}
          >
            <div style={{ fontSize: 13, color: 'var(--color-muted-foreground)' }}>
              روز <span dir="ltr">{day.name}</span> · {day.exercises.length} حرکت
            </div>
            {day.exercises.length === 0 ? (
              <p style={{ margin: '6px 0 0', fontSize: 13 }}>حرکتی باقی نماند.</p>
            ) : (
              <ul
                dir="ltr"
                className="numeric"
                style={{
                  margin: '6px 0 0',
                  paddingInlineStart: 18,
                  fontSize: 13,
                  lineHeight: 1.7,
                }}
              >
                {day.exercises.map((key) => (
                  <li key={key}>{key}</li>
                ))}
              </ul>
            )}
          </div>
        ))}
      </div>

      {dropped.length === 0 ? (
        <p
          data-testid="no-drops"
          style={{ margin: 0, fontSize: 13, color: 'var(--color-accent)' }}
        >
          هیچ حرکتی حذف نشد.
        </p>
      ) : (
        <div data-testid="dropped-list" style={{ fontSize: 13 }}>
          <div style={{ color: 'var(--color-muted-foreground)', marginBottom: 6 }}>
            حذف‌شده‌ها ({dropped.length}):
          </div>
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
      )}
    </div>
  );
}

export default ProgramPreview;
