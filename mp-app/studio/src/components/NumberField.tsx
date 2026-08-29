import { useState } from 'react';

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
    <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
      <label
        htmlFor={`jp7-${label}`}
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: 8,
          fontSize: 13,
          color: 'var(--color-muted-foreground)',
        }}
      >
        {badge !== undefined ? (
          <span
            aria-hidden
            style={{
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
            }}
          >
            {badge}
          </span>
        ) : null}
        <span>
          {label}
          {subLabel ? <span style={{ opacity: 0.6, marginInlineStart: 6 }}>{subLabel}</span> : null}
        </span>
      </label>

      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          border: `1px solid ${error ? 'var(--color-destructive)' : 'var(--color-border-subtle)'}`,
          borderRadius: 8,
          background: '#0A1218',
          transition: 'border-color 150ms, box-shadow 150ms',
          boxShadow: focused ? '0 0 0 3px rgba(0,184,106,0.25)' : 'none',
        }}
      >
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
          style={{
            flex: 1,
            background: 'transparent',
            border: 'none',
            color: 'var(--color-foreground)',
            padding: '12px 14px',
            fontSize: 16,
            fontVariantNumeric: 'tabular-nums',
            outline: 'none',
            minWidth: 0,
          }}
        />
        <span
          style={{
            paddingInlineEnd: 12,
            color: 'var(--color-muted-foreground)',
            fontSize: 13,
            fontFamily: 'var(--font-mono)',
          }}
        >
          {unit}
        </span>
      </div>

      {error ? (
        <span id={`err-${label}`} role="alert" style={{ color: 'var(--color-destructive)', fontSize: 12 }}>
          {error}
        </span>
      ) : null}
    </div>
  );
}
