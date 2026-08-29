/**
 * Thin typed API client for the MP core (port 8751).
 *
 * Uses **relative URLs** — the Vite dev server proxies `/api` and `/health` to
 * the Python core, so the browser never hardcodes localhost. Auth is carried in
 * a Bearer header read from `sessionStorage`.
 */

export interface CoreHealth {
  status: 'ok' | 'degraded';
  service: string;
  version: string;
  db: { ok: boolean; schema_version?: string | null; table_count?: number };
}

export interface Member {
  id: number;
  membership_code: string;
  first_name: string;
  last_name: string;
  sex: 'male' | 'female';
  birth_date: string | null;
  phone: string | null;
  membership_exp: string | null;
  guardian_consent: boolean;
  active_injuries: number;
}

export interface Assessment {
  id: number;
  member_id: number;
  protocol: string;
  equation: string;
  age_years: number;
  weight_kg: number;
  sum_mm: number;
  body_density: number;
  body_fat_pct: number;
  fat_mass_kg: number | null;
  lean_mass_kg: number | null;
  classification: string | null;
  created_at: string;
}

export interface Injury {
  id: number;
  member_id: number;
  body_region: string;
  label: string;
  status: string;
  pain_0_10: number | null;
  contraindicated_patterns: string[];
  member_visible_note: string | null;
}

export interface CalcResult {
  protocol: string;
  equation: string;
  sum_mm: number;
  body_density: number;
  body_fat_pct: number;
  fat_mass_kg: number | null;
  lean_mass_kg: number | null;
  classification: string | null;
  disclaimer: string;
}

export type Sites = {
  chest: number;
  midaxillary: number;
  triceps: number;
  subscapular: number;
  abdominal: number;
  suprailiac: number;
  thigh: number;
};

export class ApiError extends Error {
  constructor(
    public readonly status: number,
    public readonly detail: string,
  ) {
    super(`API ${status}: ${detail}`);
    this.name = 'ApiError';
  }
}

const TOKEN_KEY = 'mp.token';

export const tokenStore = {
  get(): string | null {
    try {
      return sessionStorage.getItem(TOKEN_KEY);
    } catch {
      return null;
    }
  },
  set(token: string): void {
    try {
      sessionStorage.setItem(TOKEN_KEY, token);
    } catch {
      /* private mode: session lives in memory */
    }
  },
  clear(): void {
    try {
      sessionStorage.removeItem(TOKEN_KEY);
    } catch {
      /* noop */
    }
  },
} as const;

async function request<T>(path: string, init: RequestInit = {}): Promise<T> {
  const token = tokenStore.get();
  const res = await fetch(path, {
    ...init,
    headers: {
      'content-type': 'application/json',
      ...(token ? { authorization: `Bearer ${token}` } : {}),
      ...(init.headers ?? {}),
    },
  });

  if (!res.ok) {
    let detail = res.statusText;
    try {
      const body = (await res.json()) as { detail?: string };
      detail = body.detail ?? detail;
    } catch {
      /* non-JSON error body */
    }
    throw new ApiError(res.status, detail);
  }
  if (res.status === 204) return undefined as T;
  return (await res.json()) as T;
}

export interface LoginResponse {
  token: string;
  role: string;
  gym_id: number;
  expires_in: number;
}

export const api = {
  health: () => request<CoreHealth>('/health'),
  login: (username: string, pin: string) =>
    request<LoginResponse>('/api/v1/auth/pin', {
      method: 'POST',
      body: JSON.stringify({ username, pin }),
    }),
  listMembers: () => request<Member[]>('/api/v1/members'),
  listAssessments: (memberId: number) =>
    request<Assessment[]>(`/api/v1/members/${memberId}/assessments`),
  saveAssessment: (
    memberId: number,
    body: { weight_kg: number; height_cm?: number; age_years: number; sites_mm: Sites; equation?: string },
  ) =>
    request<Assessment>(`/api/v1/members/${memberId}/assessments`, {
      method: 'POST',
      body: JSON.stringify(body),
    }),
  calculate: (body: { weight_kg: number; age_years: number; sites_mm: Sites; equation?: string }) =>
    request<CalcResult>('/api/v1/assessments/calculate', {
      method: 'POST',
      body: JSON.stringify(body),
    }),
  listInjuries: (memberId: number) => request<Injury[]>(`/api/v1/members/${memberId}/injuries`),

  // Phase 2 — operations. Paths verified against mp-app/openapi.yaml: the
  // payments router has no prefix, so packages live at /api/v1/packages.
  attendanceToday: () => request<AttendanceToday>('/api/v1/attendance/today'),
  checkInManual: (memberId: number) =>
    request<CheckinResult>('/api/v1/attendance/check-in', {
      method: 'POST',
      body: JSON.stringify({ member_id: memberId, method: 'manual' }),
    }),
  checkInQr: (payload: Record<string, unknown>) =>
    request<CheckinResult>('/api/v1/attendance/check-in', {
      method: 'POST',
      body: JSON.stringify({ payload, method: 'qr' }),
    }),
  listPackages: () => request<MembershipPackage[]>('/api/v1/packages'),
  recordPayment: (body: {
    member_id: number;
    amount_rial: number;
    method?: 'cash' | 'card' | 'transfer' | 'pos';
    package_id?: number;
  }) => request<Payment>('/api/v1/payments', { method: 'POST', body: JSON.stringify(body) }),
  voidPayment: (paymentId: number) =>
    request<Payment>(`/api/v1/payments/${paymentId}/void`, { method: 'POST' }),
  dashboard: () => request<Dashboard>('/api/v1/reports/dashboard'),

  // Phase 3 — rule planner (generate → dry-run → apply → archive)
  generateProgram: (memberId: number, template: ProgramTemplate) =>
    request<GeneratedProgram>(`/api/v1/members/${memberId}/programs/generate`, {
      method: 'POST',
      body: JSON.stringify({ template }),
    }),
  listPrograms: (memberId: number) =>
    request<ProgramRow[]>(`/api/v1/members/${memberId}/programs`),
  dryRunProgram: (programId: number) =>
    request<DryRunResult>(`/api/v1/programs/${programId}/dry-run`, { method: 'POST' }),
  applyProgram: (programId: number) =>
    request<ApplyResult>(`/api/v1/programs/${programId}/apply`, { method: 'POST' }),
  archiveProgram: (programId: number) =>
    request<ApplyResult>(`/api/v1/programs/${programId}/archive`, { method: 'POST' }),

  // Phase 4 — deterministic nutrition from the latest assessment LBM
  planNutrition: (
    memberId: number,
    body: { goal?: 'cut' | 'maintain' | 'bulk'; activity?: ActivityLevel; protein_g_per_kg?: number },
  ) =>
    request<NutritionPlan>(`/api/v1/nutrition/members/${memberId}/plan`, {
      method: 'POST',
      body: JSON.stringify(body),
    }),
  getNutrition: (memberId: number) =>
    request<NutritionRow>(`/api/v1/nutrition/members/${memberId}/plan`),

  // Phase 4/6 — AI runtime, delta sync, backup
  aiRuntime: () => request<AiRuntime>('/api/v1/ai/runtime'),
  syncDelta: (since?: string) =>
    request<SyncDelta>(
      `/api/v1/sync/delta${since ? `?since=${encodeURIComponent(since)}` : ''}`,
    ),
  createBackup: (password: string) =>
    request<BackupBlob>('/api/v1/admin/backup', {
      method: 'POST',
      body: JSON.stringify({ password }),
    }),
  restoreBackup: (password: string, blobB64: string) =>
    request<RestoreResult>('/api/v1/admin/backup/restore', {
      method: 'POST',
      body: JSON.stringify({ password, blob_b64: blobB64 }),
    }),
} as const;

export interface BackupBlob {
  blob_b64: string;
  bytes: number;
}

export interface RestoreResult {
  restored: Record<string, number>;
  rows: number;
}

export interface AttendanceToday {
  date: string;
  check_ins: number;
}

export interface CheckinResult {
  id: number;
  member_id: number;
  method: string;
}

export interface MembershipPackage {
  id: number;
  name: string;
  duration_days: number;
  price_rial: number;
  /** SQLite stores booleans as 0/1. */
  active: number;
  created_at: string;
}

export interface Payment {
  id: number;
  member_id: number;
  package_id: number | null;
  amount_rial: number;
  method: string;
  receipt_no: string | null;
  /** SQLite stores booleans as 0/1. */
  voided: number;
  staff_id: number | null;
  created_at: string;
}

export interface Dashboard {
  date: string;
  members_total: number;
  members_active: number;
  members_with_active_injury: number;
  check_ins_today: number;
  revenue_rial_this_month: number;
}

export type ProgramTemplate = 'ppl' | 'ul' | 'fb' | 'corrective';

export interface DroppedExercise {
  exercise?: string;
  reason?: string;
  [k: string]: unknown;
}

export interface ProgramDayPreview {
  name: string;
  exercises: string[];
  dropped: DroppedExercise[];
}

export interface GeneratedProgram {
  id: number;
  status: string;
  template: string;
  days: ProgramDayPreview[];
  meta: {
    blocked_patterns: string[];
    equipment_available: string[];
    dropped: Array<DroppedExercise & { day: string }>;
    corrective_block_added: boolean;
  };
}

export interface ProgramRow {
  id: number;
  member_id: number;
  title: string;
  status: string;
  source: string;
  payload: string;
  judge_score: number | null;
  generated_by: number | null;
  approved_by: number | null;
  applied_at: string | null;
  created_at: string;
}

export interface DryRunResult {
  program_id: number;
  status: string;
  safe_to_apply: boolean;
  newly_blocked: string[];
}

export interface ApplyResult {
  id: number;
  status: string;
  applied_at?: string | null;
}

export type ActivityLevel = 'sedentary' | 'light' | 'moderate' | 'active' | 'athlete';

/** Response of POST /nutrition/members/{id}/plan (verified live). */
export interface NutritionPlan {
  member_id: number;
  lean_mass_kg: number;
  bmr_kcal: number;
  tdee_kcal: number;
  target_kcal: number;
  protein_g: number;
  carbs_g: number;
  fat_g: number;
}

/** Response of GET /nutrition/members/{id}/plan — the stored row. */
export interface NutritionRow {
  id: number;
  member_id: number;
  bmr_kcal: number;
  tdee_kcal: number;
  protein_g: number;
  carbs_g: number;
  fat_g: number;
  payload: string;
  created_at: string;
}

export interface AiRuntime {
  available: boolean;
  base_url: string;
  model: string | null;
  models: string[];
  error: string | null;
  note: string;
}

export interface SyncDelta {
  cursor: string;
  total: number;
  changes: Record<string, Array<Record<string, unknown>>>;
}
