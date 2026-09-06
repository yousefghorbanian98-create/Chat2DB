/**
 * API contract types for the MP core.
 *
 * Split out of `client.ts` so the runtime client stays small; these shapes are
 * derived from `mp-app/openapi.yaml` and verified against live responses.
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

export interface LoginResponse {
  token: string;
  role: string;
  gym_id: number;
  expires_in: number;
}

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

/** The athlete's own plan: the internal `payload` blob is stripped server-side. */
export type ClientNutrition = Omit<NutritionRow, 'payload'>;

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

/** A masked payment row as the athlete may see it (no `staff_id`, C11). */
export interface ClientPayment {
  id: number;
  member_id: number;
  package_id: number | null;
  amount_rial: number;
  method: string;
  receipt_no: string;
  voided: boolean;
  created_at: string;
}

/** Signed, short-lived check-in QR handed to the athlete to show the kiosk. */
export interface CheckinQr {
  payload: Record<string, unknown>;
  expires_in: number;
}

/** One performed set; `weight_kg` stays absent for bodyweight work. */
export interface WorkoutSetInput {
  weight_kg?: number;
  reps?: number;
}

export interface WorkoutExerciseInput {
  name: string;
  sets?: WorkoutSetInput[];
}

/** A session the athlete logged themselves, as read back from the server. */
export interface WorkoutLog {
  id: number;
  member_id: number;
  program_id: number | null;
  session_date: string;
  athlete_note: string | null;
  exercises: WorkoutExerciseInput[];
  created_at: string;
}

/** Body for `POST /client/me/workouts`. */
export interface WorkoutLogCreate {
  session_date: string;
  program_id?: number | null;
  exercises: WorkoutExerciseInput[];
  athlete_note?: string | null;
}
