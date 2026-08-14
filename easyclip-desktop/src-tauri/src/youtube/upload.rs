//! Resumable upload helpers for `videos.insert`.
//!
//! Large video files cannot use a simple upload, so this implements Google's
//! resumable protocol. The byte-range arithmetic lives here as pure functions so
//! it can be unit tested without touching the network — getting a `Content-Range`
//! off by one byte is the classic way to corrupt an upload.

use serde::{Deserialize, Serialize};

/// 8 MiB. Google requires chunks to be a multiple of 256 KiB.
pub const CHUNK_SIZE: u64 = 8 * 1024 * 1024;
pub const RESUMABLE_ENDPOINT: &str =
    "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status";

/// Quota cost of a single `videos.insert` call.
pub const UPLOAD_QUOTA_COST: u32 = 1600;
/// Default daily quota for a fresh Google Cloud project.
pub const DEFAULT_DAILY_QUOTA: u32 = 10_000;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize, Default)]
#[serde(rename_all = "lowercase")]
pub enum Privacy {
    /// Safe by default: nothing goes public by accident.
    #[default]
    Private,
    Unlisted,
    Public,
}

impl Privacy {
    pub fn as_str(self) -> &'static str {
        match self {
            Privacy::Private => "private",
            Privacy::Unlisted => "unlisted",
            Privacy::Public => "public",
        }
    }
}

/// Metadata for a single upload.
#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct UploadMetadata {
    pub title: String,
    pub description: String,
    pub tags: Vec<String>,
    pub category_id: String,
    pub privacy: Privacy,
    /// RFC 3339 timestamp for scheduled publication.
    pub publish_at: Option<String>,
}

impl UploadMetadata {
    /// Build the JSON body for the resumable session request.
    pub fn to_body(&self) -> serde_json::Value {
        let mut status = serde_json::json!({
            "privacyStatus": self.privacy.as_str(),
            "selfDeclaredMadeForKids": false,
        });
        // A scheduled publish time is only meaningful while the video is private.
        if let Some(publish_at) = self.publish_at.as_deref() {
            if self.privacy == Privacy::Private {
                status["publishAt"] = serde_json::Value::String(publish_at.to_owned());
            }
        }
        serde_json::json!({
            "snippet": {
                "title": super::parse::safe_title(&self.title),
                "description": super::parse::safe_description(&self.description),
                "tags": self.tags,
                "categoryId": self.category_id,
            },
            "status": status,
        })
    }
}

/// How many uploads remain within a daily quota.
pub fn uploads_remaining(spent_units: u32, daily_quota: u32) -> u32 {
    daily_quota.saturating_sub(spent_units) / UPLOAD_QUOTA_COST
}

/// The `Content-Range` value for a chunk starting at `offset`.
///
/// Ranges are inclusive on both ends, so a 10-byte file sent whole is
/// `bytes 0-9/10`.
pub fn content_range(offset: u64, chunk_length: u64, total: u64) -> String {
    if chunk_length == 0 {
        return format!("bytes */{total}");
    }
    let last = offset + chunk_length - 1;
    format!("bytes {offset}-{last}/{total}")
}

/// The `Content-Range` used to *query* how much of an interrupted upload landed.
pub fn probe_range(total: u64) -> String {
    format!("bytes */{total}")
}

/// Size of the next chunk to send.
pub fn next_chunk_length(offset: u64, total: u64) -> u64 {
    total.saturating_sub(offset).min(CHUNK_SIZE)
}

/// Parse the `Range` header Google returns for a partially received upload.
///
/// The header looks like `bytes=0-1048575`, meaning bytes 0 through 1048575 are
/// stored, so the next byte to send is 1048576. An absent header means nothing
/// was stored and the upload restarts at 0.
pub fn resume_offset(range_header: Option<&str>) -> u64 {
    let Some(header) = range_header else {
        return 0;
    };
    let Some((_, ranges)) = header.split_once('=') else {
        return 0;
    };
    // If multiple ranges are present, the last end wins.
    ranges
        .split(',')
        .filter_map(|part| part.rsplit('-').next())
        .filter_map(|end| end.trim().parse::<u64>().ok())
        .max()
        .map(|end| end + 1)
        .unwrap_or(0)
}

/// Whether an HTTP status should be retried.
pub fn is_retryable(status: u16) -> bool {
    status == 408 || status == 429 || (500..=599).contains(&status)
}

/// Whether an HTTP status means "chunk accepted, keep going".
pub fn is_incomplete(status: u16) -> bool {
    status == 308
}

/// Exponential backoff with a cap, in milliseconds.
pub fn backoff_millis(attempt: u32) -> u64 {
    let base = 1_000u64.saturating_mul(1u64 << attempt.min(6));
    base.min(64_000)
}

/// Overall progress as a percentage.
pub fn progress_percent(sent: u64, total: u64) -> u8 {
    if total == 0 {
        return 0;
    }
    ((sent.min(total) as f64 / total as f64) * 100.0).round() as u8
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn builds_inclusive_content_ranges() {
        assert_eq!(content_range(0, 10, 10), "bytes 0-9/10");
        assert_eq!(content_range(0, CHUNK_SIZE, 20_000_000), "bytes 0-8388607/20000000");
        assert_eq!(
            content_range(CHUNK_SIZE, CHUNK_SIZE, 20_000_000),
            "bytes 8388608-16777215/20000000"
        );
    }

    #[test]
    fn builds_final_short_chunk_range() {
        let total = 20_000_000u64;
        let offset = 2 * CHUNK_SIZE; // 16777216
        let length = next_chunk_length(offset, total);
        assert_eq!(length, total - offset);
        assert_eq!(content_range(offset, length, total), "bytes 16777216-19999999/20000000");
    }

    #[test]
    fn zero_length_chunk_becomes_a_probe() {
        assert_eq!(content_range(0, 0, 500), "bytes */500");
        assert_eq!(probe_range(500), "bytes */500");
    }

    #[test]
    fn chunk_length_never_exceeds_remaining() {
        assert_eq!(next_chunk_length(0, 100), 100);
        assert_eq!(next_chunk_length(0, CHUNK_SIZE * 3), CHUNK_SIZE);
        assert_eq!(next_chunk_length(CHUNK_SIZE * 3, CHUNK_SIZE * 3), 0);
    }

    #[test]
    fn computes_resume_offset_from_range_header() {
        assert_eq!(resume_offset(Some("bytes=0-1048575")), 1_048_576);
        assert_eq!(resume_offset(Some("bytes=0-0")), 1);
        assert_eq!(resume_offset(None), 0);
        assert_eq!(resume_offset(Some("garbage")), 0);
    }

    #[test]
    fn resuming_then_ranging_is_consistent() {
        // Simulate: 20 MB file, first chunk stored, connection dropped.
        let total = 20_000_000u64;
        let offset = resume_offset(Some("bytes=0-8388607"));
        assert_eq!(offset, CHUNK_SIZE);
        let length = next_chunk_length(offset, total);
        assert_eq!(content_range(offset, length, total), "bytes 8388608-16777215/20000000");
    }

    #[test]
    fn classifies_http_statuses() {
        assert!(is_retryable(500));
        assert!(is_retryable(503));
        assert!(is_retryable(429));
        assert!(!is_retryable(400));
        assert!(!is_retryable(401));
        assert!(is_incomplete(308));
        assert!(!is_incomplete(200));
    }

    #[test]
    fn backoff_grows_then_caps() {
        assert_eq!(backoff_millis(0), 1_000);
        assert_eq!(backoff_millis(1), 2_000);
        assert_eq!(backoff_millis(3), 8_000);
        assert_eq!(backoff_millis(50), 64_000);
    }

    #[test]
    fn quota_maths_matches_googles_limits() {
        // The headline constraint: ~6 uploads per day on a default project.
        assert_eq!(uploads_remaining(0, DEFAULT_DAILY_QUOTA), 6);
        assert_eq!(uploads_remaining(UPLOAD_QUOTA_COST, DEFAULT_DAILY_QUOTA), 5);
        assert_eq!(uploads_remaining(9_600, DEFAULT_DAILY_QUOTA), 0);
        assert_eq!(uploads_remaining(99_999, DEFAULT_DAILY_QUOTA), 0);
    }

    #[test]
    fn reports_progress() {
        assert_eq!(progress_percent(0, 100), 0);
        assert_eq!(progress_percent(50, 100), 50);
        assert_eq!(progress_percent(100, 100), 100);
        assert_eq!(progress_percent(150, 100), 100);
        assert_eq!(progress_percent(1, 0), 0);
    }

    #[test]
    fn metadata_defaults_to_private_and_blocks_kids_flag() {
        let metadata = UploadMetadata {
            title: "t".into(),
            description: "d".into(),
            tags: vec!["a".into()],
            category_id: "22".into(),
            privacy: Privacy::default(),
            publish_at: None,
        };
        let body = metadata.to_body();
        assert_eq!(body["status"]["privacyStatus"], "private");
        assert_eq!(body["status"]["selfDeclaredMadeForKids"], false);
        assert!(body["status"].get("publishAt").is_none());
    }

    #[test]
    fn scheduled_publish_only_applies_to_private_videos() {
        let mut metadata = UploadMetadata {
            title: "t".into(),
            description: "d".into(),
            tags: vec![],
            category_id: "22".into(),
            privacy: Privacy::Private,
            publish_at: Some("2026-09-01T10:00:00Z".into()),
        };
        assert_eq!(metadata.to_body()["status"]["publishAt"], "2026-09-01T10:00:00Z");

        metadata.privacy = Privacy::Public;
        assert!(metadata.to_body()["status"].get("publishAt").is_none());
    }

    #[test]
    fn metadata_sanitises_persian_titles() {
        let metadata = UploadMetadata {
            title: "ب".repeat(150),
            description: "<b>hi</b>".into(),
            tags: vec![],
            category_id: "22".into(),
            privacy: Privacy::Private,
            publish_at: None,
        };
        let body = metadata.to_body();
        let title = body["snippet"]["title"].as_str().unwrap();
        assert_eq!(title.chars().count(), 100);
        assert_eq!(body["snippet"]["description"], "bhi/b");
    }
}
