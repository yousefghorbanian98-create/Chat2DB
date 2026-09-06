import type { Member } from '../../api/client';

interface AthleteProfileProps {
  member: Member | null;
}

/** Column 1: who is being assessed. Read-only identity, never editable here. */
export function AthleteProfile({ member }: AthleteProfileProps) {
  return (
    <section className="glass" style={{ padding: 'var(--space-2xl)' }}>
      <h3 style={{ marginBottom: 'var(--space-lg)' }}>ورزشکار</h3>
      {member ? (
        <div style={{ display: 'grid', gap: 'var(--space-md)', fontSize: 14 }}>
          <div style={{ fontSize: 20, fontFamily: 'var(--font-display)' }}>
            {member.first_name} {member.last_name}
          </div>
          <div style={{ color: 'var(--color-muted-foreground)' }}>
            جنسیت: {member.sex === 'male' ? 'مرد' : 'زن'}
          </div>
          <div style={{ color: 'var(--color-muted-foreground)' }} className="numeric" dir="ltr">
            {member.membership_code}
          </div>
          {member.birth_date ? (
            <div style={{ color: 'var(--color-muted-foreground)' }} className="numeric" dir="ltr">
              {member.birth_date}
            </div>
          ) : null}
        </div>
      ) : (
        <p style={{ color: 'var(--color-muted-foreground)' }}>ابتدا یک ورزشکار انتخاب کنید.</p>
      )}
    </section>
  );
}

export default AthleteProfile;
