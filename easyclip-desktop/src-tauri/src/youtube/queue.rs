//! Job queue state machine and dedupe rules.
//!
//! The persistence layer is SQLite, but the *decisions* live here as pure
//! functions so the rules that stop a video being uploaded twice can be tested
//! directly.

use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum JobState {
    Pending,
    Downloading,
    Clipping,
    Uploading,
    Done,
    Failed,
    Skipped,
}

impl JobState {
    pub fn as_str(self) -> &'static str {
        match self {
            JobState::Pending => "pending",
            JobState::Downloading => "downloading",
            JobState::Clipping => "clipping",
            JobState::Uploading => "uploading",
            JobState::Done => "done",
            JobState::Failed => "failed",
            JobState::Skipped => "skipped",
        }
    }

    #[allow(clippy::should_implement_trait)]
    pub fn from_str(value: &str) -> Option<Self> {
        Some(match value {
            "pending" => JobState::Pending,
            "downloading" => JobState::Downloading,
            "clipping" => JobState::Clipping,
            "uploading" => JobState::Uploading,
            "done" => JobState::Done,
            "failed" => JobState::Failed,
            "skipped" => JobState::Skipped,
            _ => return None,
        })
    }

    /// Terminal states are never picked up by the worker again.
    pub fn is_terminal(self) -> bool {
        matches!(self, JobState::Done | JobState::Skipped)
    }

    /// States that were mid-flight when the app closed and must be rewound.
    pub fn is_in_flight(self) -> bool {
        matches!(
            self,
            JobState::Downloading | JobState::Clipping | JobState::Uploading
        )
    }
}

pub const MAX_ATTEMPTS: u32 = 3;

/// A job may be retried while it has attempts left.
pub fn can_retry(state: JobState, attempts: u32) -> bool {
    state == JobState::Failed && attempts < MAX_ATTEMPTS
}

/// After a crash or restart, in-flight jobs return to `Pending`.
pub fn state_after_restart(state: JobState) -> JobState {
    if state.is_in_flight() {
        JobState::Pending
    } else {
        state
    }
}

/// Decide whether the worker may start another job right now.
pub fn should_start_job(
    running: usize,
    concurrency: usize,
    uploads_left: u32,
    paused: bool,
) -> bool {
    !paused && running < concurrency.max(1) && uploads_left > 0
}

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct Job {
    pub id: String,
    pub source_video_id: String,
    pub source_channel_id: String,
    pub title: String,
    pub state: JobState,
    pub attempts: u32,
    pub error: Option<String>,
    pub target_video_id: Option<String>,
    pub progress: u8,
}

/// Filter a freshly fetched catalogue down to videos that are not already known.
///
/// This is the in-memory mirror of the `UNIQUE(source_video_id)` constraint.
pub fn new_video_ids<'a>(fetched: &[&'a str], known: &[String]) -> Vec<&'a str> {
    fetched
        .iter()
        .copied()
        .filter(|id| !known.iter().any(|seen| seen == id))
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn state_strings_round_trip() {
        for state in [
            JobState::Pending,
            JobState::Downloading,
            JobState::Clipping,
            JobState::Uploading,
            JobState::Done,
            JobState::Failed,
            JobState::Skipped,
        ] {
            assert_eq!(JobState::from_str(state.as_str()), Some(state));
        }
        assert_eq!(JobState::from_str("nonsense"), None);
    }

    #[test]
    fn identifies_terminal_and_in_flight_states() {
        assert!(JobState::Done.is_terminal());
        assert!(JobState::Skipped.is_terminal());
        assert!(!JobState::Failed.is_terminal());
        assert!(JobState::Uploading.is_in_flight());
        assert!(!JobState::Pending.is_in_flight());
    }

    #[test]
    fn retries_are_bounded() {
        assert!(can_retry(JobState::Failed, 0));
        assert!(can_retry(JobState::Failed, 2));
        assert!(!can_retry(JobState::Failed, 3));
        assert!(!can_retry(JobState::Done, 0));
    }

    #[test]
    fn restart_rewinds_in_flight_jobs_only() {
        assert_eq!(state_after_restart(JobState::Uploading), JobState::Pending);
        assert_eq!(state_after_restart(JobState::Downloading), JobState::Pending);
        assert_eq!(state_after_restart(JobState::Done), JobState::Done);
        assert_eq!(state_after_restart(JobState::Failed), JobState::Failed);
    }

    #[test]
    fn worker_respects_concurrency_quota_and_pause() {
        assert!(should_start_job(0, 2, 6, false));
        assert!(should_start_job(1, 2, 1, false));
        // At the concurrency limit.
        assert!(!should_start_job(2, 2, 6, false));
        // Out of daily quota.
        assert!(!should_start_job(0, 2, 0, false));
        // Explicitly paused.
        assert!(!should_start_job(0, 2, 6, true));
        // A zero concurrency setting still allows one worker.
        assert!(should_start_job(0, 0, 6, false));
    }

    #[test]
    fn dedupe_filters_already_known_videos() {
        let fetched = vec!["a", "b", "c"];
        let known = vec!["b".to_owned()];
        assert_eq!(new_video_ids(&fetched, &known), vec!["a", "c"]);
    }

    #[test]
    fn dedupe_is_stable_when_everything_is_known() {
        let fetched = vec!["a", "b"];
        let known = vec!["a".to_owned(), "b".to_owned()];
        assert!(new_video_ids(&fetched, &known).is_empty());
    }
}
