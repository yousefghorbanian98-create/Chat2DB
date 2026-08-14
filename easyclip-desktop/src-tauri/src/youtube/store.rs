//! Local persistence: SQLite for jobs/settings, OS keychain for the refresh token.

use rusqlite::{params, Connection};
use std::path::Path;

use super::queue::{Job, JobState};

const KEYRING_SERVICE: &str = "ai.easyclip.desktop";
const KEYRING_USER: &str = "google-refresh-token";

pub fn open(path: &Path) -> Result<Connection, String> {
    if let Some(parent) = path.parent() {
        std::fs::create_dir_all(parent)
            .map_err(|error| format!("Cannot create the data directory: {error}"))?;
    }
    let connection = Connection::open(path)
        .map_err(|error| format!("Cannot open the local database: {error}"))?;
    migrate(&connection)?;
    Ok(connection)
}

pub fn migrate(connection: &Connection) -> Result<(), String> {
    connection
        .execute_batch(
            "PRAGMA journal_mode=WAL;
             CREATE TABLE IF NOT EXISTS jobs (
                 id TEXT PRIMARY KEY,
                 source_video_id TEXT NOT NULL UNIQUE,
                 source_channel_id TEXT NOT NULL,
                 title TEXT NOT NULL,
                 state TEXT NOT NULL,
                 attempts INTEGER NOT NULL DEFAULT 0,
                 error TEXT,
                 target_video_id TEXT,
                 upload_session TEXT,
                 created_at TEXT NOT NULL,
                 updated_at TEXT NOT NULL
             );
             CREATE INDEX IF NOT EXISTS jobs_state_idx ON jobs(state);
             CREATE TABLE IF NOT EXISTS settings (
                 key TEXT PRIMARY KEY,
                 value TEXT NOT NULL
             );
             CREATE TABLE IF NOT EXISTS quota (
                 day TEXT PRIMARY KEY,
                 units INTEGER NOT NULL DEFAULT 0
             );
             CREATE TABLE IF NOT EXISTS acknowledgements (
                 channel_id TEXT PRIMARY KEY,
                 acknowledged_at TEXT NOT NULL
             );",
        )
        .map_err(|error| format!("Cannot prepare the local database: {error}"))
}

pub fn set_setting(connection: &Connection, key: &str, value: &str) -> Result<(), String> {
    connection
        .execute(
            "INSERT INTO settings(key, value) VALUES(?1, ?2)
             ON CONFLICT(key) DO UPDATE SET value = excluded.value",
            params![key, value],
        )
        .map(|_| ())
        .map_err(|error| format!("Cannot save setting: {error}"))
}

pub fn get_setting(connection: &Connection, key: &str) -> Option<String> {
    connection
        .query_row(
            "SELECT value FROM settings WHERE key = ?1",
            params![key],
            |row| row.get::<_, String>(0),
        )
        .ok()
}

/// Insert a job, ignoring anything already queued for the same source video.
///
/// Returns `true` when a new row was created. The `UNIQUE` constraint on
/// `source_video_id` is what makes double-uploading impossible.
pub fn insert_job(
    connection: &Connection,
    id: &str,
    source_video_id: &str,
    source_channel_id: &str,
    title: &str,
    now: &str,
) -> Result<bool, String> {
    let changed = connection
        .execute(
            "INSERT OR IGNORE INTO jobs
               (id, source_video_id, source_channel_id, title, state, attempts, created_at, updated_at)
             VALUES(?1, ?2, ?3, ?4, 'pending', 0, ?5, ?5)",
            params![id, source_video_id, source_channel_id, title, now],
        )
        .map_err(|error| format!("Cannot queue video: {error}"))?;
    Ok(changed > 0)
}

pub fn update_job_state(
    connection: &Connection,
    id: &str,
    state: JobState,
    error: Option<&str>,
    now: &str,
) -> Result<(), String> {
    connection
        .execute(
            "UPDATE jobs SET state = ?2, error = ?3, updated_at = ?4 WHERE id = ?1",
            params![id, state.as_str(), error, now],
        )
        .map(|_| ())
        .map_err(|error| format!("Cannot update job: {error}"))
}

pub fn set_job_target(
    connection: &Connection,
    id: &str,
    target_video_id: &str,
    now: &str,
) -> Result<(), String> {
    connection
        .execute(
            "UPDATE jobs SET target_video_id = ?2, state = 'done', error = NULL, updated_at = ?3 WHERE id = ?1",
            params![id, target_video_id, now],
        )
        .map(|_| ())
        .map_err(|error| format!("Cannot record upload: {error}"))
}

pub fn increment_attempts(connection: &Connection, id: &str) -> Result<u32, String> {
    connection
        .execute(
            "UPDATE jobs SET attempts = attempts + 1 WHERE id = ?1",
            params![id],
        )
        .map_err(|error| format!("Cannot update attempts: {error}"))?;
    connection
        .query_row(
            "SELECT attempts FROM jobs WHERE id = ?1",
            params![id],
            |row| row.get::<_, i64>(0),
        )
        .map(|value| value as u32)
        .map_err(|error| format!("Cannot read attempts: {error}"))
}

pub fn list_jobs(connection: &Connection) -> Result<Vec<Job>, String> {
    let mut statement = connection
        .prepare(
            "SELECT id, source_video_id, source_channel_id, title, state, attempts, error, target_video_id
             FROM jobs ORDER BY created_at ASC",
        )
        .map_err(|error| format!("Cannot read the queue: {error}"))?;
    let rows = statement
        .query_map([], |row| {
            Ok(Job {
                id: row.get(0)?,
                source_video_id: row.get(1)?,
                source_channel_id: row.get(2)?,
                title: row.get(3)?,
                state: JobState::from_str(&row.get::<_, String>(4)?)
                    .unwrap_or(JobState::Pending),
                attempts: row.get::<_, i64>(5)? as u32,
                error: row.get(6)?,
                target_video_id: row.get(7)?,
                progress: 0,
            })
        })
        .map_err(|error| format!("Cannot read the queue: {error}"))?;
    rows.collect::<Result<Vec<_>, _>>()
        .map_err(|error| format!("Cannot read the queue: {error}"))
}

pub fn known_video_ids(connection: &Connection, channel_id: &str) -> Result<Vec<String>, String> {
    let mut statement = connection
        .prepare("SELECT source_video_id FROM jobs WHERE source_channel_id = ?1")
        .map_err(|error| format!("Cannot read the queue: {error}"))?;
    let rows = statement
        .query_map(params![channel_id], |row| row.get::<_, String>(0))
        .map_err(|error| format!("Cannot read the queue: {error}"))?;
    rows.collect::<Result<Vec<_>, _>>()
        .map_err(|error| format!("Cannot read the queue: {error}"))
}

/// Rewind jobs that were mid-flight when the app was last closed.
pub fn recover_in_flight(connection: &Connection, now: &str) -> Result<usize, String> {
    connection
        .execute(
            "UPDATE jobs SET state = 'pending', updated_at = ?1
             WHERE state IN ('downloading','clipping','uploading')",
            params![now],
        )
        .map_err(|error| format!("Cannot recover the queue: {error}"))
}

pub fn remove_job(connection: &Connection, id: &str) -> Result<(), String> {
    connection
        .execute("DELETE FROM jobs WHERE id = ?1", params![id])
        .map(|_| ())
        .map_err(|error| format!("Cannot remove job: {error}"))
}

pub fn add_quota(connection: &Connection, day: &str, units: u32) -> Result<(), String> {
    connection
        .execute(
            "INSERT INTO quota(day, units) VALUES(?1, ?2)
             ON CONFLICT(day) DO UPDATE SET units = units + excluded.units",
            params![day, units],
        )
        .map(|_| ())
        .map_err(|error| format!("Cannot record quota: {error}"))
}

pub fn quota_spent(connection: &Connection, day: &str) -> u32 {
    connection
        .query_row(
            "SELECT units FROM quota WHERE day = ?1",
            params![day],
            |row| row.get::<_, i64>(0),
        )
        .map(|value| value as u32)
        .unwrap_or(0)
}

pub fn acknowledge_channel(
    connection: &Connection,
    channel_id: &str,
    now: &str,
) -> Result<(), String> {
    connection
        .execute(
            "INSERT OR REPLACE INTO acknowledgements(channel_id, acknowledged_at) VALUES(?1, ?2)",
            params![channel_id, now],
        )
        .map(|_| ())
        .map_err(|error| format!("Cannot record acknowledgement: {error}"))
}

pub fn is_acknowledged(connection: &Connection, channel_id: &str) -> bool {
    connection
        .query_row(
            "SELECT 1 FROM acknowledgements WHERE channel_id = ?1",
            params![channel_id],
            |row| row.get::<_, i64>(0),
        )
        .is_ok()
}

// ---------------------------------------------------------------- keychain --

pub fn save_refresh_token(token: &str) -> Result<(), String> {
    keyring::Entry::new(KEYRING_SERVICE, KEYRING_USER)
        .and_then(|entry| entry.set_password(token))
        .map_err(|error| format!("Cannot save the sign-in securely: {error}"))
}

pub fn load_refresh_token() -> Option<String> {
    keyring::Entry::new(KEYRING_SERVICE, KEYRING_USER)
        .and_then(|entry| entry.get_password())
        .ok()
}

pub fn delete_refresh_token() -> Result<(), String> {
    match keyring::Entry::new(KEYRING_SERVICE, KEYRING_USER) {
        Ok(entry) => match entry.delete_credential() {
            Ok(()) => Ok(()),
            // Already gone is success as far as the caller is concerned.
            Err(keyring::Error::NoEntry) => Ok(()),
            Err(error) => Err(format!("Cannot clear the saved sign-in: {error}")),
        },
        Err(error) => Err(format!("Cannot access the credential store: {error}")),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn memory_db() -> Connection {
        let connection = Connection::open_in_memory().unwrap();
        migrate(&connection).unwrap();
        connection
    }

    #[test]
    fn migration_is_idempotent() {
        let connection = memory_db();
        migrate(&connection).unwrap();
        migrate(&connection).unwrap();
    }

    #[test]
    fn unique_constraint_prevents_double_queueing() {
        let connection = memory_db();
        let first = insert_job(&connection, "j1", "vid1", "UCabc", "One", "now").unwrap();
        let second = insert_job(&connection, "j2", "vid1", "UCabc", "One again", "now").unwrap();
        assert!(first, "first insert should create a row");
        assert!(!second, "duplicate source video must be ignored");
        assert_eq!(list_jobs(&connection).unwrap().len(), 1);
    }

    #[test]
    fn tracks_job_lifecycle() {
        let connection = memory_db();
        insert_job(&connection, "j1", "vid1", "UCabc", "One", "now").unwrap();

        update_job_state(&connection, "j1", JobState::Uploading, None, "now").unwrap();
        assert_eq!(list_jobs(&connection).unwrap()[0].state, JobState::Uploading);

        set_job_target(&connection, "j1", "newVid", "now").unwrap();
        let job = &list_jobs(&connection).unwrap()[0];
        assert_eq!(job.state, JobState::Done);
        assert_eq!(job.target_video_id.as_deref(), Some("newVid"));
    }

    #[test]
    fn records_failures_and_attempts() {
        let connection = memory_db();
        insert_job(&connection, "j1", "vid1", "UCabc", "One", "now").unwrap();
        update_job_state(&connection, "j1", JobState::Failed, Some("boom"), "now").unwrap();
        assert_eq!(increment_attempts(&connection, "j1").unwrap(), 1);
        assert_eq!(increment_attempts(&connection, "j1").unwrap(), 2);
        let job = &list_jobs(&connection).unwrap()[0];
        assert_eq!(job.error.as_deref(), Some("boom"));
        assert_eq!(job.attempts, 2);
    }

    #[test]
    fn recovers_in_flight_jobs_after_restart() {
        let connection = memory_db();
        insert_job(&connection, "j1", "v1", "UCabc", "a", "now").unwrap();
        insert_job(&connection, "j2", "v2", "UCabc", "b", "now").unwrap();
        insert_job(&connection, "j3", "v3", "UCabc", "c", "now").unwrap();
        update_job_state(&connection, "j1", JobState::Uploading, None, "now").unwrap();
        update_job_state(&connection, "j2", JobState::Downloading, None, "now").unwrap();
        set_job_target(&connection, "j3", "done", "now").unwrap();

        assert_eq!(recover_in_flight(&connection, "later").unwrap(), 2);
        let jobs = list_jobs(&connection).unwrap();
        assert_eq!(jobs[0].state, JobState::Pending);
        assert_eq!(jobs[1].state, JobState::Pending);
        // A finished job must not be rewound.
        assert_eq!(jobs[2].state, JobState::Done);
    }

    #[test]
    fn known_ids_are_scoped_to_a_channel() {
        let connection = memory_db();
        insert_job(&connection, "j1", "v1", "UCone", "a", "now").unwrap();
        insert_job(&connection, "j2", "v2", "UCtwo", "b", "now").unwrap();
        assert_eq!(known_video_ids(&connection, "UCone").unwrap(), vec!["v1"]);
    }

    #[test]
    fn quota_accumulates_per_day() {
        let connection = memory_db();
        assert_eq!(quota_spent(&connection, "2026-08-14"), 0);
        add_quota(&connection, "2026-08-14", 1600).unwrap();
        add_quota(&connection, "2026-08-14", 1600).unwrap();
        assert_eq!(quota_spent(&connection, "2026-08-14"), 3200);
        // A new day starts clean.
        assert_eq!(quota_spent(&connection, "2026-08-15"), 0);
    }

    #[test]
    fn settings_round_trip_and_overwrite() {
        let connection = memory_db();
        assert!(get_setting(&connection, "missing").is_none());
        set_setting(&connection, "privacy", "private").unwrap();
        set_setting(&connection, "privacy", "unlisted").unwrap();
        assert_eq!(get_setting(&connection, "privacy").as_deref(), Some("unlisted"));
    }

    #[test]
    fn acknowledgements_are_remembered() {
        let connection = memory_db();
        assert!(!is_acknowledged(&connection, "UCabc"));
        acknowledge_channel(&connection, "UCabc", "now").unwrap();
        assert!(is_acknowledged(&connection, "UCabc"));
    }

    #[test]
    fn jobs_can_be_removed() {
        let connection = memory_db();
        insert_job(&connection, "j1", "v1", "UCabc", "a", "now").unwrap();
        remove_job(&connection, "j1").unwrap();
        assert!(list_jobs(&connection).unwrap().is_empty());
        // Removing frees the video id to be queued again.
        assert!(insert_job(&connection, "j2", "v1", "UCabc", "a", "now").unwrap());
    }
}
