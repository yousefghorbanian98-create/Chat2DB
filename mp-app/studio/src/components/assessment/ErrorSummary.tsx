import type { FieldError } from '../../pages/jp7Validation';

interface ErrorSummaryProps {
  errors: FieldError[];
}

/**
 * A11y summary at the top of the form: screen-reader users hear the first few
 * problems instead of hunting through seven fields.
 */
export function ErrorSummary({ errors }: ErrorSummaryProps) {
  if (errors.length === 0) return null;

  return (
    <div
      role="alert"
      data-testid="error-summary"
      style={{
        padding: '10px 14px',
        borderRadius: 8,
        background: 'rgba(239,68,68,0.12)',
        border: '1px solid var(--color-injury-active)',
        color: '#FCA5A5',
        fontSize: 13,
      }}
    >
      {errors.length} خطا:{' '}
      {errors
        .slice(0, 3)
        .map((e) => e.messageFa)
        .join('، ')}
      {errors.length > 3 ? '، …' : ''}
    </div>
  );
}

export default ErrorSummary;
