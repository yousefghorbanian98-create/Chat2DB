import type { WorkoutExerciseInput, WorkoutLogCreate } from '../api/client';

/**
 * Pure draft state + validation for the athlete's own session log.
 *
 * Kept framework-free so it is unit-testable without React. Dates are stored as
 * ISO `YYYY-MM-DD` — the single canonical form in this app — and rendered
 * through `faDate`, which is the only Jalali formatter the UI uses.
 */

export interface WorkoutDraftSet {
  weight: string;
  reps: string;
}

export interface WorkoutDraftExercise {
  name: string;
  sets: WorkoutDraftSet[];
}

export interface WorkoutDraft {
  sessionDate: string;
  exercises: WorkoutDraftExercise[];
  note: string;
}

export interface WorkoutFieldError {
  field: 'sessionDate' | 'exercises' | string;
  message: string;
}

/** Today as ISO `YYYY-MM-DD` in the browser's own calendar day. */
export function todayIso(now: Date = new Date()): string {
  const y = now.getFullYear();
  const m = String(now.getMonth() + 1).padStart(2, '0');
  const d = String(now.getDate()).padStart(2, '0');
  return `${y}-${m}-${d}`;
}

/** One blank exercise with one blank set — the smallest honest starting form. */
export function emptyWorkoutDraft(now: Date = new Date()): WorkoutDraft {
  return {
    sessionDate: todayIso(now),
    exercises: [{ name: '', sets: [{ weight: '', reps: '' }] }],
    note: '',
  };
}

/** A set with neither load nor reps carries no information, so it is dropped. */
function keepSet(s: WorkoutDraftSet): boolean {
  return s.weight.trim() !== '' || s.reps.trim() !== '';
}

/** Parse a numeric field; an empty string means "not recorded", not zero. */
function num(value: string): number | null {
  const trimmed = value.trim();
  if (trimmed === '') return null;
  const n = Number(trimmed);
  return Number.isFinite(n) && n >= 0 ? n : null;
}

/**
 * True only when the athlete typed something that is not a usable number.
 *
 * An empty box is *not* an error: a bodyweight set has no load and a timed set
 * may have no rep count. Only a value that was entered and cannot be parsed is
 * wrong — conflating the two would force athletes to invent a measurement.
 */
function isBadNumber(value: string): boolean {
  return value.trim() !== '' && num(value) === null;
}

/** Field-level checks mirroring the pydantic model on the server. */
export function validateWorkout(draft: WorkoutDraft): WorkoutFieldError[] {
  const errors: WorkoutFieldError[] = [];
  if (!/^\d{4}-\d{2}-\d{2}$/.test(draft.sessionDate)) {
    errors.push({ field: 'sessionDate', message: 'تاریخ جلسه را وارد کنید' });
  }
  const named = draft.exercises.filter((e) => e.name.trim() !== '');
  if (named.length === 0) {
    errors.push({ field: 'exercises', message: 'حداقل یک حرکت را نام ببرید' });
  }
  for (const ex of draft.exercises) {
    for (const s of ex.sets) {
      if (!keepSet(s)) continue;
      if (isBadNumber(s.weight) || isBadNumber(s.reps)) {
        errors.push({ field: 'exercises', message: 'وزن و تکرار باید عدد باشند' });
        return errors;
      }
    }
  }
  return errors;
}

/** Build the request body, omitting anything the athlete did not record. */
export function toWorkoutBody(draft: WorkoutDraft): WorkoutLogCreate {
  const exercises: WorkoutExerciseInput[] = draft.exercises
    .filter((e) => e.name.trim() !== '')
    .map((e) => ({
      name: e.name.trim(),
      sets: e.sets.filter(keepSet).map((s) => ({
        ...(num(s.weight) === null ? {} : { weight_kg: num(s.weight) as number }),
        ...(num(s.reps) === null ? {} : { reps: num(s.reps) as number }),
      })),
    }));
  return {
    session_date: draft.sessionDate,
    exercises,
    ...(draft.note.trim() === '' ? {} : { athlete_note: draft.note.trim() }),
  };
}
