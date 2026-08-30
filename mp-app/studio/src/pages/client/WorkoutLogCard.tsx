import { useState, type CSSProperties } from 'react';

import { MotionButton } from '../../components/MotionButton';
import { faDate } from '../../core/jalali';
import type { WorkoutLog } from '../../api/client';
import type { WorkoutDraftExercise } from '../../client/workoutDraft';
import type { WorkoutLogState } from '../../hooks/useWorkoutLog';
import { cardSection, cardTitle, fieldLabel, muted, noteSmall } from '../../styles/blocks';

const STACK: CSSProperties = { display: 'flex', flexDirection: 'column', gap: 'var(--space-md)' };
const BOX: CSSProperties = {
  background: '#0A1218',
  border: '1px solid var(--color-border-subtle)',
  borderRadius: 8,
  padding: '10px 12px',
  color: 'var(--color-foreground)',
  fontSize: 16,
  outline: 'none',
  width: '100%',
  minWidth: 0,
};
const SET_ROW: CSSProperties = { display: 'flex', gap: 8, alignItems: 'center' };
const HISTORY: CSSProperties = { margin: 0, paddingInlineStart: 0, listStyle: 'none' };

/** One numeric box inside a set row. */
function SetBox({
  label,
  value,
  unit,
  onChange,
}: {
  label: string;
  value: string;
  unit: string;
  onChange: (v: string) => void;
}) {
  const [focused, setFocused] = useState(false);
  return (
    <label style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: 4 }}>
      <span style={noteSmall}>{label}</span>
      <input
        className="numeric"
        inputMode="decimal"
        dir="ltr"
        type="text"
        value={value}
        placeholder={unit}
        onChange={(e) => onChange(e.target.value)}
        onFocus={() => setFocused(true)}
        onBlur={() => setFocused(false)}
        aria-label={label}
        style={{
          ...BOX,
          fontVariantNumeric: 'tabular-nums',
          boxShadow: focused ? '0 0 0 3px rgba(0,184,106,0.25)' : 'none',
        }}
      />
    </label>
  );
}

/** One movement: its name, its performed sets, and a way to add another set. */
function ExerciseEditor({
  exercise,
  index,
  onRename,
  onAddSet,
  onEditSet,
}: {
  exercise: WorkoutDraftExercise;
  index: number;
  onRename: (name: string) => void;
  onAddSet: () => void;
  onEditSet: (set: number, patch: { weight?: string; reps?: string }) => void;
}) {
  return (
    <div style={{ ...STACK, gap: 8 }} data-testid={`exercise-${index}`}>
      <input
        type="text"
        value={exercise.name}
        placeholder="نام حرکت"
        onChange={(e) => onRename(e.target.value)}
        aria-label={`نام حرکت ${index + 1}`}
        style={BOX}
      />
      {exercise.sets.map((s, si) => (
        <div key={si} style={SET_ROW}>
          <SetBox
            label="وزن (kg)"
            unit="kg"
            value={s.weight}
            onChange={(v) => onEditSet(si, { weight: v })}
          />
          <SetBox
            label="تکرار"
            unit="reps"
            value={s.reps}
            onChange={(v) => onEditSet(si, { reps: v })}
          />
        </div>
      ))}
      <MotionButton variant="ghost" onClick={onAddSet}>
        افزودن ست
      </MotionButton>
    </div>
  );
}

/** The athlete's own previous sessions, newest first. */
function WorkoutHistory({ history }: { history: WorkoutLog[] }) {
  return (
    <>
      <h4 style={cardTitle}>جلسات پیشین</h4>
      {history.length === 0 ? (
        <p style={muted}>هنوز جلسه‌ای ثبت نکرده‌اید.</p>
      ) : (
        <ul style={HISTORY} data-testid="workout-history">
          {history.slice(0, 8).map((w) => (
            <li key={w.id} style={{ paddingBlock: 'var(--space-sm)' }}>
              <strong className="numeric">{faDate(w.created_at)}</strong>
              <div style={muted}>{w.exercises.map((e) => e.name).join('، ')}</div>
              {w.athlete_note ? <div style={noteSmall}>{w.athlete_note}</div> : null}
            </li>
          ))}
        </ul>
      )}
    </>
  );
}

/** Success/failure line under the form. */
function WorkoutStatus({ error, saved }: { error: string | null; saved: WorkoutLog | null }) {
  if (error !== null) {
    return (
      <p role="alert" style={{ color: 'var(--color-destructive)' }}>
        {error}
      </p>
    );
  }
  if (saved !== null) {
    return (
      <p style={{ color: 'var(--color-success)' }} data-testid="workout-saved">
        جلسهٔ <span className="numeric">{faDate(saved.created_at)}</span> ثبت شد.
      </p>
    );
  }
  return null;
}

/** The entry form: one date, any number of movements, an optional note. */
function WorkoutForm({ state }: { state: WorkoutLogState }) {
  const { draft, state: buttonState } = state;
  return (
    <div style={STACK}>
      <label style={fieldLabel}>
        تاریخ جلسه
        <input
          className="numeric"
          dir="ltr"
          type="date"
          value={draft.sessionDate}
          onChange={(e) => state.setSessionDate(e.target.value)}
          style={BOX}
          aria-label="تاریخ جلسه"
        />
      </label>

      {draft.exercises.map((ex, ei) => (
        <ExerciseEditor
          key={ei}
          exercise={ex}
          index={ei}
          onRename={(name) => state.setExerciseName(ei, name)}
          onAddSet={() => state.addSet(ei)}
          onEditSet={(si, patch) => state.setSet(ei, si, patch)}
        />
      ))}

      <MotionButton variant="ghost" onClick={state.addExercise}>
        افزودن حرکت
      </MotionButton>

      <label style={fieldLabel}>
        یادداشت من
        <textarea
          value={draft.note}
          onChange={(e) => state.setNote(e.target.value)}
          rows={2}
          style={{ ...BOX, resize: 'vertical' }}
          aria-label="یادداشت جلسه"
        />
      </label>

      <WorkoutStatus error={state.error} saved={state.saved} />

      <MotionButton state={buttonState} onClick={state.submit} disabled={buttonState === 'loading'}>
        ثبت جلسه
      </MotionButton>
    </div>
  );
}

/**
 * The athlete logs their own session and sees the ones before it.
 *
 * Weight and reps are both optional on purpose: a bodyweight or timed set is
 * real training, and forcing a number would mean inventing a measurement.
 */
export function WorkoutLogCard({
  state,
  history,
}: {
  state: WorkoutLogState;
  history: WorkoutLog[];
}) {
  return (
    <section className="glass" style={cardSection} data-testid="client-workouts">
      <h3 style={cardTitle}>ثبت جلسهٔ تمرین</h3>
      <WorkoutForm state={state} />
      <WorkoutHistory history={history} />
    </section>
  );
}

export default WorkoutLogCard;
