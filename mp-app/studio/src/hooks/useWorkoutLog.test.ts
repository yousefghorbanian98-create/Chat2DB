import { act, renderHook, waitFor } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';

import { api, ApiError } from '../api/client';
import type * as apiClient from '../api/client';
import { useWorkoutLog, type WorkoutLogState } from './useWorkoutLog';

vi.mock('../api/client', async () => {
  const actual = await vi.importActual<typeof apiClient>('../api/client');
  return { ...actual, api: { ...actual.api, logWorkout: vi.fn() } };
});

const logWorkout = vi.mocked(api.logWorkout);
const onSaved = vi.fn().mockResolvedValue([]);

/** Type one real exercise into the draft so submit has something to send. */
function fill(result: { current: WorkoutLogState }) {
  act(() => result.current.setExerciseName(0, 'اسکات'));
  act(() => result.current.setSet(0, 0, { weight: '60' }));
  act(() => result.current.setSet(0, 0, { reps: '8' }));
}

describe('useWorkoutLog', () => {
  beforeEach(() => {
    logWorkout.mockReset();
    onSaved.mockClear();
  });

  it('refuses to submit with no named exercise, and says why in Persian', () => {
    const { result } = renderHook(() => useWorkoutLog(onSaved));
    act(() => result.current.submit());
    expect(logWorkout).not.toHaveBeenCalled();
    expect(result.current.state).toBe('error');
    expect(result.current.error).toBe('حداقل یک حرکت را نام ببرید');
    expect(onSaved).not.toHaveBeenCalled();
  });

  it('posts the session and clears the form on success', async () => {
    logWorkout.mockResolvedValue({
      id: 1,
      member_id: 2,
      program_id: null,
      session_date: '2026-08-30',
      athlete_note: null,
      exercises: [{ name: 'اسکات', sets: [{ weight_kg: 60, reps: 8 }] }],
      created_at: '2026-08-30T10:00:00Z',
    });

    const { result } = renderHook(() => useWorkoutLog(onSaved));
    fill(result);
    act(() => result.current.submit());

    await waitFor(() => expect(result.current.state).toBe('success'));
    expect(logWorkout).toHaveBeenCalledWith(
      expect.objectContaining({
        session_date: '2026-08-30',
        exercises: [{ name: 'اسکات', sets: [{ weight_kg: 60, reps: 8 }] }],
      }),
    );
    // The form is emptied for the next session, and the history is re-read.
    expect(result.current.draft.exercises[0]?.name).toBe('');
    expect(onSaved).toHaveBeenCalledTimes(1);
  });

  it('keeps the draft and surfaces the server message when the write fails', async () => {
    logWorkout.mockRejectedValue(new ApiError(422, 'فرمت تاریخ نامعتبر است'));

    const { result } = renderHook(() => useWorkoutLog(onSaved));
    fill(result);
    act(() => result.current.submit());

    await waitFor(() => expect(result.current.state).toBe('error'));
    expect(result.current.error).toBe('فرمت تاریخ نامعتبر است');
    // A flaky gym network must not cost the athlete what they typed.
    expect(result.current.draft.exercises[0]?.name).toBe('اسکات');
    expect(onSaved).not.toHaveBeenCalled();
  });

  it('falls back to a generic message when the failure is not an ApiError', async () => {
    logWorkout.mockRejectedValue(new TypeError('network'));
    const { result } = renderHook(() => useWorkoutLog(onSaved));
    fill(result);
    act(() => result.current.submit());
    await waitFor(() => expect(result.current.error).toBe('ثبت جلسه ناموفق بود'));
  });

  it('adds exercises and sets without touching the others', () => {
    const { result } = renderHook(() => useWorkoutLog(onSaved));
    act(() => result.current.setExerciseName(0, 'اسکات'));
    act(() => result.current.addExercise());
    act(() => result.current.setExerciseName(1, 'پرس سینه'));
    act(() => result.current.addSet(0));
    act(() => result.current.setSet(0, 1, { reps: '12' }));

    const [first, second] = result.current.draft.exercises;
    expect(first?.name).toBe('اسکات');
    expect(first?.sets).toHaveLength(2);
    expect(first?.sets[1]?.reps).toBe('12');
    expect(second?.name).toBe('پرس سینه');
    expect(second?.sets).toHaveLength(1);
  });

  it('records the note and the session date', () => {
    const { result } = renderHook(() => useWorkoutLog(onSaved));
    act(() => result.current.setNote('ست آخر سنگین بود'));
    act(() => result.current.setSessionDate('2026-09-01'));
    expect(result.current.draft.note).toBe('ست آخر سنگین بود');
    expect(result.current.draft.sessionDate).toBe('2026-09-01');
  });

  it('reset clears the form, the saved row and any error', async () => {
    logWorkout.mockRejectedValue(new ApiError(500, 'boom'));
    const { result } = renderHook(() => useWorkoutLog(onSaved));
    fill(result);
    act(() => result.current.submit());
    await waitFor(() => expect(result.current.error).not.toBeNull());

    act(() => result.current.reset());
    expect(result.current.error).toBeNull();
    expect(result.current.state).toBe('idle');
    expect(result.current.saved).toBeNull();
    expect(result.current.draft.exercises[0]?.name).toBe('');
  });
});
