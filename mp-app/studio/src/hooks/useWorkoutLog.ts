import { useCallback, useState } from 'react';

import { ApiError, api, type WorkoutLog } from '../api/client';
import {
  emptyWorkoutDraft,
  toWorkoutBody,
  validateWorkout,
  type WorkoutDraft,
} from '../client/workoutDraft';
import type { ButtonState } from '../components/MotionButton';

/** One numeric field of a set, as typed into the form. */
export type WorkoutSetPatch = Partial<WorkoutDraft['exercises'][number]['sets'][number]>;

/** Editors for the draft. Split out so each stays inside the line budget. */
export interface WorkoutDraftEditors {
  setNote: (note: string) => void;
  setSessionDate: (sessionDate: string) => void;
  setExerciseName: (index: number, name: string) => void;
  addExercise: () => void;
  addSet: (index: number) => void;
  /** Merge one field into a single set (weight and/or reps). */
  setSet: (exercise: number, set: number, patch: WorkoutSetPatch) => void;
}

export interface WorkoutLogState extends WorkoutDraftEditors {
  draft: WorkoutDraft;
  state: ButtonState;
  error: string | null;
  saved: WorkoutLog | null;
  submit: () => void;
  reset: () => void;
}

const blankSet = { weight: '', reps: '' };

/** Immutable patch helper shared by every editor below. */
function useDraft() {
  const [draft, setDraft] = useState<WorkoutDraft>(() => emptyWorkoutDraft());
  const patch = useCallback((fn: (d: WorkoutDraft) => WorkoutDraft) => setDraft(fn), []);
  return { draft, setDraft, patch };
}

/** One editor per gesture the form offers. */
function useDraftEditors(
  patch: (fn: (d: WorkoutDraft) => WorkoutDraft) => void,
): WorkoutDraftEditors {
  const setNote = useCallback((note: string) => patch((d) => ({ ...d, note })), [patch]);
  const setSessionDate = useCallback(
    (sessionDate: string) => patch((d) => ({ ...d, sessionDate })),
    [patch],
  );
  const setExerciseName = useCallback(
    (index: number, name: string) =>
      patch((d) => ({
        ...d,
        exercises: d.exercises.map((e, i) => (i === index ? { ...e, name } : e)),
      })),
    [patch],
  );
  const addExercise = useCallback(
    () =>
      patch((d) => ({ ...d, exercises: [...d.exercises, { name: '', sets: [{ ...blankSet }] }] })),
    [patch],
  );
  const addSet = useCallback(
    (index: number) =>
      patch((d) => ({
        ...d,
        exercises: d.exercises.map((e, i) =>
          i === index ? { ...e, sets: [...e.sets, { ...blankSet }] } : e,
        ),
      })),
    [patch],
  );
  const setSet = useCallback(
    (exercise: number, set: number, next: Partial<typeof blankSet>) =>
      patch((d) => ({
        ...d,
        exercises: d.exercises.map((e, ei) =>
          ei !== exercise
            ? e
            : { ...e, sets: e.sets.map((s, si) => (si === set ? { ...s, ...next } : s)) },
        ),
      })),
    [patch],
  );

  return { setNote, setSessionDate, setExerciseName, addExercise, addSet, setSet };
}

/**
 * The athlete logging their own session.
 *
 * On success the form clears and the history is re-read; on failure the draft is
 * kept and the server's message is shown, so a flaky gym network never costs the
 * athlete what they just typed.
 */
export function useWorkoutLog(onSaved: () => Promise<WorkoutLog[]>): WorkoutLogState {
  const { draft, setDraft, patch } = useDraft();
  const [state, setState] = useState<ButtonState>('idle');
  const [error, setError] = useState<string | null>(null);
  const [saved, setSaved] = useState<WorkoutLog | null>(null);

  const reset = useCallback(() => {
    setDraft(emptyWorkoutDraft());
    setSaved(null);
    setState('idle');
    setError(null);
  }, [setDraft]);

  const submit = useCallback(() => {
    const problems = validateWorkout(draft);
    if (problems.length > 0) {
      setState('error');
      setError(problems[0]?.message ?? 'فرم ناقص است');
      return;
    }
    setState('loading');
    setError(null);
    void api
      .logWorkout(toWorkoutBody(draft))
      .then((row) => {
        setSaved(row);
        setState('success');
        setDraft(emptyWorkoutDraft());
        void onSaved();
      })
      .catch((err: unknown) => {
        setState('error');
        setError(err instanceof ApiError ? err.detail : 'ثبت جلسه ناموفق بود');
      });
  }, [draft, onSaved, setDraft]);

  const editors = useDraftEditors(patch);

  return { draft, state, error, saved, submit, reset, ...editors };
}
