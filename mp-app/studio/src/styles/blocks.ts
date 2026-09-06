import type { CSSProperties } from 'react';

/**
 * Hoisted layout/style blocks.
 *
 * Inline `style={{...}}` literals recreate an object on every render and bury
 * the JSX they decorate. Hoisting them keeps components inside the 50-line
 * budget for the *markup that matters* and gives one place to change a look.
 */

export const cardSection: CSSProperties = {
  padding: 'var(--space-2xl)',
};

export const cardTitle: CSSProperties = {
  marginBottom: 'var(--space-lg)',
};

export const muted: CSSProperties = {
  color: 'var(--color-muted-foreground)',
};

export const fieldLabel: CSSProperties = {
  display: 'flex',
  flexDirection: 'column',
  gap: 6,
  fontSize: 13,
  ...muted,
};

export const chipRow: CSSProperties = {
  display: 'flex',
  flexWrap: 'wrap',
  gap: 8,
};

export const stackLg: CSSProperties = {
  display: 'flex',
  flexDirection: 'column',
  gap: 'var(--space-lg)',
};

export const stackXl: CSSProperties = {
  display: 'flex',
  flexDirection: 'column',
  gap: 'var(--space-xl)',
};

export const alertDanger: CSSProperties = {
  padding: '10px 14px',
  borderRadius: 8,
  background: 'rgba(239,68,68,0.12)',
  border: '1px solid var(--color-injury-active)',
  color: '#FCA5A5',
  fontSize: 13,
};

export const noteSmall: CSSProperties = {
  fontSize: 12,
  margin: 0,
  ...muted,
};

export const siteGrid: CSSProperties = {
  display: 'grid',
  gridTemplateColumns: 'repeat(auto-fill, minmax(150px, 1fr))',
  gap: 'var(--space-lg)',
};

export const twoColGrid: CSSProperties = {
  display: 'grid',
  gridTemplateColumns: 'repeat(2, 1fr)',
  gap: 'var(--space-lg)',
};

export const bigNumber: CSSProperties = {
  fontSize: 44,
  fontWeight: 700,
  fontFamily: 'var(--font-display)',
  color: 'var(--color-accent)',
};

export const athleteName: CSSProperties = {
  fontSize: 20,
  fontFamily: 'var(--font-display)',
};

export const ltrNumeric: CSSProperties = {
  color: 'var(--color-muted-foreground)',
};
