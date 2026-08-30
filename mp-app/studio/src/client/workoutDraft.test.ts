import { describe, expect, it } from 'vitest';

import {
  emptyWorkoutDraft,
  todayIso,
  toWorkoutBody,
  validateWorkout,
  type WorkoutDraft,
} from './workoutDraft';

/** A draft with one real exercise, used by several cases. */
function draft(over: Partial<WorkoutDraft> = {}): WorkoutDraft {
  return { ...emptyWorkoutDraft(new Date('2026-08-30T10:00:00Z')), ...over };
}

describe('todayIso', () => {
  it('formats the browser-local day as ISO', () => {
    expect(todayIso(new Date(2026, 7, 30))).toBe('2026-08-30');
    expect(todayIso(new Date(2026, 0, 5))).toBe('2026-01-05');
  });
});

describe('validateWorkout', () => {
  it('rejects a session with no named exercise', () => {
    const problems = validateWorkout(draft({ exercises: [{ name: '  ', sets: [] }] }));
    expect(problems.map((p) => p.message)).toContain('حداقل یک حرکت را نام ببرید');
  });

  it('rejects a malformed date', () => {
    expect(validateWorkout(draft({ sessionDate: '1405/06/08' }))[0]?.field).toBe('sessionDate');
  });

  it('rejects a non-numeric weight or rep count', () => {
    const problems = validateWorkout(
      draft({ exercises: [{ name: 'اسکات', sets: [{ weight: 'abc', reps: '' }] }] }),
    );
    expect(problems.map((p) => p.message)).toContain('وزن و تکرار باید عدد باشند');
  });

  it('accepts a blank set — it is simply not recorded', () => {
    const problems = validateWorkout(
      draft({ exercises: [{ name: 'اسکات', sets: [{ weight: '', reps: '' }] }] }),
    );
    expect(problems).toEqual([]);
  });

  it('accepts a bodyweight set with reps only', () => {
    const problems = validateWorkout(
      draft({ exercises: [{ name: 'بارفیکس', sets: [{ weight: '', reps: '12' }] }] }),
    );
    expect(problems).toEqual([]);
  });
});

describe('toWorkoutBody', () => {
  it('omits a weight that was never entered rather than inventing zero', () => {
    const body = toWorkoutBody(
      draft({ exercises: [{ name: 'بارفیکس', sets: [{ weight: '', reps: '12' }] }] }),
    );
    const sets = body.exercises[0]?.sets ?? [];
    expect(sets[0]).toEqual({ reps: 12 });
    expect(sets[0]).not.toHaveProperty('weight_kg');
  });

  it('drops unnamed exercises and fully blank sets', () => {
    const body = toWorkoutBody(
      draft({
        exercises: [
          {
            name: 'اسکات',
            sets: [
              { weight: '60', reps: '8' },
              { weight: '', reps: '' },
            ],
          },
          { name: '   ', sets: [{ weight: '10', reps: '5' }] },
        ],
      }),
    );
    expect(body.exercises).toHaveLength(1);
    expect(body.exercises[0]?.sets).toEqual([{ weight_kg: 60, reps: 8 }]);
  });

  it('omits the note when it is blank, and trims it when it is not', () => {
    expect(toWorkoutBody(draft({ note: '   ' }))).not.toHaveProperty('athlete_note');
    expect(toWorkoutBody(draft({ note: ' سنگین ' })).athlete_note).toBe('سنگین');
  });

  it('keeps the ISO session date untouched for faDate to render', () => {
    expect(toWorkoutBody(draft({ sessionDate: '2026-08-30' })).session_date).toBe('2026-08-30');
  });
});
