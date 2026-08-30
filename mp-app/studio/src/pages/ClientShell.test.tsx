import { render, screen } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';

import ClientShell from './ClientShell';

vi.mock('../auth/useAuth', () => ({ useAuth: () => ({ logout: vi.fn(), role: 'MEMBER' }) }));

const useClientData = vi.fn();
vi.mock('../hooks/useClientData', () => ({ useClientData: () => useClientData() }));

function setData(d: {
  me: { id: number; first_name: string; last_name: string; membership_code: string } | null;
  assessments: { id: number; created_at: string; body_fat_pct: number; weight_kg: number }[];
  programs: { id: number; title: string; status: string }[];
  nutrition?: { tdee_kcal: number; protein_g: number; carbs_g: number; fat_g: number } | null;
  loading?: boolean;
  error?: string | null;
}) {
  useClientData.mockReturnValue({
    me: d.me,
    assessments: d.assessments,
    programs: d.programs,
    nutrition: d.nutrition ?? null,
    loading: d.loading ?? false,
    error: d.error ?? null,
    reload: vi.fn(),
  });
}

describe('ClientShell (athlete web shell)', () => {
  beforeEach(() => setData({ me: null, assessments: [], programs: [] }));

  it('renders the masked profile and a body-fat figure', () => {
    setData({
      me: { id: 2, first_name: 'نسیم', last_name: 'رحیمی', membership_code: 'MP-DEMO-1' },
      assessments: [
        { id: 1, created_at: '2026-08-30T00:00:00Z', body_fat_pct: 13.6453, weight_kg: 58 },
      ],
      programs: [{ id: 9, title: 'قدرت', status: 'active' }],
    });
    render(<ClientShell />);
    expect(screen.getByTestId('client-profile').textContent).toContain('نسیم');
    expect(screen.getByTestId('client-assessments').textContent).toContain('13.6');
    // Persian-first contract (C): the date is Jalali, never a raw ISO slice.
    expect(screen.getByTestId('client-assessments').textContent).toContain('۱۴۰۵/۰۶/۰۸');
    expect(screen.getByTestId('client-assessments').textContent).not.toContain('2026-08-30');
    expect(screen.getByTestId('client-programs').textContent).toContain('قدرت');
  });

  it('shows an empty state when there is no program yet', () => {
    setData({
      me: { id: 2, first_name: 'نسیم', last_name: 'رحیمی', membership_code: 'MP-DEMO-1' },
      assessments: [],
      programs: [],
    });
    render(<ClientShell />);
    expect(screen.getByTestId('client-programs').textContent).toContain('هنوز برنامه‌ای');
    expect(screen.getByTestId('client-assessments').textContent).toContain('هنوز ارزیابی‌ای');
  });

  it('shows macro targets when a plan exists, and hides the card when not', () => {
    const me = { id: 2, first_name: 'نسیم', last_name: 'رحیمی', membership_code: 'MP-DEMO-1' };
    setData({
      me,
      assessments: [],
      programs: [],
      nutrition: { tdee_kcal: 2431, protein_g: 147, carbs_g: 273, fat_g: 81 },
    });
    const { rerender } = render(<ClientShell />);
    const card = screen.getByTestId('client-nutrition');
    expect(card.textContent).toContain('2431');
    expect(card.textContent).toContain('147');
    expect(card.textContent).not.toContain('payload');

    setData({ me, assessments: [], programs: [], nutrition: null });
    rerender(<ClientShell />);
    expect(screen.queryByTestId('client-nutrition')).toBeNull();
  });

  it('surfaces a transport error instead of an empty shell', () => {
    setData({
      me: null,
      assessments: [],
      programs: [],
      error: 'بارگذاری اطلاعات میسر نشد — دوباره تلاش کنید.',
    });
    render(<ClientShell />);
    expect(screen.getByRole('alert')).toBeTruthy();
  });
});
