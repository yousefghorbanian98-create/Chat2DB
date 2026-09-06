import type { Member } from '../../api/client';

interface MemberSelectProps {
  members: Member[];
  memberId: number | null;
  onSelect: (memberId: number | null) => void;
}

/** The athlete picker at the top of the JP7 page (mockup 07). */
export function MemberSelect({ members, memberId, onSelect }: MemberSelectProps) {
  return (
    <label
      style={{
        display: 'flex',
        flexDirection: 'column',
        gap: 6,
        fontSize: 13,
        color: 'var(--color-muted-foreground)',
      }}
    >
      ورزشکار
      <select
        data-testid="assessment-member"
        value={memberId ?? ''}
        onChange={(e) => onSelect(e.target.value ? Number(e.target.value) : null)}
        className="mp-input"
        style={{ minWidth: 200 }}
      >
        <option value="">— انتخاب —</option>
        {members.map((m) => (
          <option key={m.id} value={m.id}>
            {m.first_name} {m.last_name}
          </option>
        ))}
      </select>
    </label>
  );
}

export default MemberSelect;
