import { render, screen } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';

import ClientShell from './ClientShell';

vi.mock('../auth/useAuth', () => ({ useAuth: () => ({ logout: vi.fn(), role: 'MEMBER' }) }));

const useClientData = vi.fn();
vi.mock('../hooks/useClientData', () => ({ useClientData: () => useClientData() }));

const useWorkoutLog = vi.fn();
vi.mock('../hooks/useWorkoutLog', () => ({ useWorkoutLog: () => useWorkoutLog() }));

// The kiosk QR mints on mount; stub it so these tests never touch the network.
vi.mock('../hooks/useCheckinQr', () => ({
  useCheckinQr: () => ({ payload: null, secondsLeft: 60, error: null, refresh: vi.fn() }),
}));

/** A minimal, valid workout-log form state for the shell to render. */
function workoutState() {
  return {
    draft: { sessionDate: '2026-08-30', exercises: [{ name: '', sets: [] }], note: '' },
    state: 'idle',
    error: null,
    saved: null,
    setNote: vi.fn(),
    setSessionDate: vi.fn(),
    setExerciseName: vi.fn(),
    addExercise: vi.fn(),
    addSet: vi.fn(),
    setSet: vi.fn(),
    submit: vi.fn(),
    reset: vi.fn(),
  };
}

function setData(d: {
  me: { id: number; first_name: string; last_name: string; membership_code: string } | null;
  assessments: { id: number; created_at: string; body_fat_pct: number; weight_kg: number }[];
  programs: { id: number; title: string; status: string }[];
  nutrition?: { tdee_kcal: number; protein_g: number; carbs_g: number; fat_g: number } | null;
  injuries?: {
    id: number;
    body_region: string;
    label: string;
    status: string;
    contraindicated_patterns: string[];
    member_visible_note: string | null;
  }[];
  payments?: {
    id: number;
    amount_rial: number;
    method: string;
    receipt_no: string;
    created_at: string;
    voided: boolean;
  }[];
  workouts?: { id: number; created_at: string; exercises: { name: string }[] }[];
  loading?: boolean;
  error?: string | null;
}) {
  useClientData.mockReturnValue({
    me: d.me,
    assessments: d.assessments,
    programs: d.programs,
    nutrition: d.nutrition ?? null,
    injuries: d.injuries ?? [],
    payments: d.payments ?? [],
    workouts: d.workouts ?? [],
    loading: d.loading ?? false,
    error: d.error ?? null,
    reload: vi.fn(),
    refreshWorkouts: vi.fn().mockResolvedValue([]),
  });
}

describe('ClientShell (athlete web shell)', () => {
  beforeEach(() => {
    setData({ me: null, assessments: [], programs: [] });
    useWorkoutLog.mockReturnValue(workoutState());
  });

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

it("lists the athlete's restrictions and their payment history", () => {
  setData({
    me: { id: 2, first_name: 'نسیم', last_name: 'رحیمی', membership_code: 'MP-DEMO-1' },
    assessments: [],
    programs: [],
    injuries: [
      {
        id: 5,
        body_region: 'lumbar',
        label: 'کمردرد مزمن',
        status: 'active',
        contraindicated_patterns: ['deadlift'],
        member_visible_note: 'از ددلیفت سنگین پرهیز کنید',
      },
    ],
    payments: [
      {
        id: 7,
        amount_rial: 2500000,
        method: 'card',
        receipt_no: 'R-1042',
        created_at: '2026-08-30T00:00:00Z',
        voided: false,
      },
    ],
  });
  render(<ClientShell />);

  const injuries = screen.getByTestId('client-injuries');
  expect(injuries.textContent).toContain('کمردرد مزمن');
  expect(injuries.textContent).toContain('کمر');
  // C6: the forbidden pattern is what the planner must hard-filter on.
  expect(injuries.textContent).toContain('ممنوع: deadlift');
  expect(injuries.textContent).toContain('از ددلیفت سنگین پرهیز کنید');
  // C9: the clinician note is stripped server-side, so nothing here can show it.
  expect(injuries.textContent).not.toContain('clinician');

  const payments = screen.getByTestId('client-payments');
  // formatRial is deliberately Latin-digit, grouped like the receipt PDF
  // (pinned in opsValidation.test.ts) — do not "Persian-ify" it here.
  expect(payments.textContent).toContain('2,500,000');
  expect(payments.textContent).toContain('R-1042');
  // C11: who took the money at the desk is internal, never rendered.
  expect(payments.textContent).not.toContain('staff');
});

it('shows empty states for restrictions and payments', () => {
  setData({
    me: { id: 2, first_name: 'نسیم', last_name: 'رحیمی', membership_code: 'MP-DEMO-1' },
    assessments: [],
    programs: [],
  });
  render(<ClientShell />);
  expect(screen.getByTestId('client-injuries').textContent).toContain('هیچ محدودیتی');
  expect(screen.getByTestId('client-payments').textContent).toContain('هنوز پرداختی');
  expect(screen.getByTestId('client-workouts').textContent).toContain('ثبت جلسهٔ تمرین');
});

it('renders logged sessions newest-first with their Persian date', () => {
  setData({
    me: { id: 2, first_name: 'نسیم', last_name: 'رحیمی', membership_code: 'MP-DEMO-1' },
    assessments: [],
    programs: [],
    workouts: [{ id: 11, created_at: '2026-08-30T00:00:00Z', exercises: [{ name: 'اسکات' }] }],
  });
  render(<ClientShell />);
  const history = screen.getByTestId('workout-history');
  expect(history.textContent).toContain('اسکات');
  expect(history.textContent).toContain('۱۴۰۵/۰۶/۰۸');
});
