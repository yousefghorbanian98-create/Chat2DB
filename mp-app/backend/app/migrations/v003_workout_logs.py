"""v003: athlete workout session log (client app, map §5).

The athlete records what they actually did — sets, reps, load — against a
program, so the client app is a training log and not just a viewer.

`payload` holds the session as JSON (``mp.workout/v1``). `athlete_note` is the
athlete's own wording about their own session; unlike a clinician ``note`` it is
never stripped by the member field mask, because it belongs to the member.
"""

from __future__ import annotations

from app.migrations.base import Migration

_STATEMENTS = (
    """
    CREATE TABLE IF NOT EXISTS workout_logs (
        id           INTEGER PRIMARY KEY,
        gym_id       INTEGER NOT NULL REFERENCES gyms(id),
        created_at   TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
        updated_at   TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
        deleted_at   TEXT,
        rev          INTEGER NOT NULL DEFAULT 1,
        member_id    INTEGER NOT NULL REFERENCES members(id),
        program_id   INTEGER REFERENCES training_programs(id),
        session_date TEXT NOT NULL,
        payload      TEXT NOT NULL,
        athlete_note TEXT
    )
    """,
    """
    CREATE INDEX IF NOT EXISTS ix_workout_logs_member
        ON workout_logs (gym_id, member_id, deleted_at)
    """,
)

MIGRATION = Migration(
    version="0003_workout_logs",
    label="athlete workout session log",
    statements=_STATEMENTS,
)
