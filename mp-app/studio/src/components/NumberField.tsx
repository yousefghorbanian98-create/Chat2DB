import { useState, type CSSProperties } from 'react';

interface NumberFieldProps {
  label: string;
  subLabel?: string;
  value: string;
  onChange: (next: string) => void;
  onBlur?: () => void;
  error?: string | null;
  /** Optional leading badge (e.g. the numbered caliper-site marker). */
  badge?: number;
  unit?: string;
}

const STACK: CSSProperties = { display: 'flex', flexDirection: 'column', gap: 6 };
const LABEL: CSSProperties = {
  display: 'flex',
  alignItems: 'center',
  gap: 8,
  fontSize: 13,
  color: 'var(--color-muted-foreground)',
};
const BADGE: CSSProperties = {
  width: 18,
  height: 18,
  borderRadius: '50%',
  background: 'var(--color-primary)',
  color: 'var(--color-on-primary)',
  display: 'inline-flex',
  alignItems: 'center',
  justifyContent: 'center',
  fontSize: 11,
  fontWeight: 700,
};
const INPUT: CSSProperties = {
  flex: 1,
  background: 'transparent',
  border: 'none',
  color: 'var(--color-foreground)',
  padding: '12px 14px',
  fontSize: 16,
  fontVariantNumeric: 'tabular-nums',
  outline: 'none',
  minWidth: 0,
};
const UNIT: CSSProperties = {
  paddingInlineEnd: 12,
  color: 'var(--color-muted-foreground)',
  fontSize: 13,
  fontFamily: 'var(--font-mono)',
};
const ERR_TEXT: CSSProperties = { color: 'var(--color-destructive)', fontSize: 12 };

/** Focus ring + error border, hoisted so the JSX stays inside the budget. */
function boxStyle(hasError: boolean, focused: boolean): CSSProperties {
  return {
    display: 'flex',
    alignItems: 'center',
    border: `1px solid ${hasError ? 'var(--color-destructive)' : 'var(--color-border-subtle)'}`,
    borderRadius: 8,
    background: '#0A1218',
    transition: 'border-color 150ms, box-shadow 150ms',
    boxShadow: focused ? '0 0 0 3px rgba(0,184,106,0.25)' : 'none',
  };
}

const SUB_LABEL: CSSProperties = { opacity: 0.6, marginInlineStart: 6 };

/** Numbered caliper-site marker + bilingual label. */
function FieldLabel({
  label,
  subLabel,
  badge,
}: {
  label: string;
  subLabel?: string | undefined;
  badge?: number | undefined;
}) {
  return (
    <label htmlFor={`jp7-${label}`} style={LABEL}>
      {badge !== undefined ? (
        <span aria-hidden style={BADGE}>
          {badge}
        </span>
      ) : null}
      <span>
        {label}
        {subLabel ? <span style={SUB_LABEL}>{subLabel}</span> : null}
      </span>
    </label>
  );
}

/**
 * Decimal number field per `pages/assessment-jp7.md`:
 * `inputMode="decimal"`, `dir="ltr"`, tabular nums, 16px, validate on blur.
 * Errors use the FINN-LOOP shake and an error summary elsewhere links to them.
 */
export function NumberField({
  label,
  subLabel,
  value,
  onChange,
  onBlur,
  error,
  badge,
  unit = 'mm',
}: NumberFieldProps) {
  const [focused, setFocused] = useState(false);

  return (
    <div style={STACK}>
      <FieldLabel label={label} subLabel={subLabel} badge={badge} />

      <div style={boxStyle(Boolean(error), focused)}>
        <input
          id={`jp7-${label}`}
          className="numeric"
          inputMode="decimal"
          dir="ltr"
          type="text"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onFocus={() => setFocused(true)}
          onBlur={() => {
            setFocused(false);
            onBlur?.();
          }}
          aria-invalid={Boolean(error)}
          aria-describedby={error ? `err-${label}` : undefined}
          style={INPUT}
        />
        <span style={UNIT}>{unit}</span>
      </div>

      {error ? (
        <span id={`err-${label}`} role="alert" style={ERR_TEXT}>
          {error}
        </span>
      ) : null}
    </div>
  );
}
