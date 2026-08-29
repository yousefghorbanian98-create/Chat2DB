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
} as const;
