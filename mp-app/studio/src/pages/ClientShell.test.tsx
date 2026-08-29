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
  loading?: boolean;
  error?: string | null;
}) {
  useClientData.mockReturnValue({
    me: d.me,
    assessments: d.assessments,
    programs: d.programs,
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
      assessments: [{ id: 1, created_at: '2026-08-30T00:00:00Z', body_fat_pct: 13.6453, weight_kg: 58 }],
      programs: [{ id: 9, title: 'قدرت', status: 'active' }],
    });
    render(<ClientShell />);
    expect(screen.getByTestId('client-profile').textContent).toContain('نسیم');
    expect(screen.getByTestId('client-assessments').textContent).toContain('13.6');
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

  it('surfaces a transport error instead of an empty shell', () => {
    setData({ me: null, assessments: [], programs: [], error: 'بارگذاری اطلاعات میسر نشد — دوباره تلاش کنید.' });
    render(<ClientShell />);
    expect(screen.getByRole('alert')).toBeTruthy();
  });
});
