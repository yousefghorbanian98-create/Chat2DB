//! Source video download via the bundled `yt-dlp`.
//!
//! The YouTube Data API cannot return video bytes, so `yt-dlp` is the only
//! practical route. Progress parsing is a pure function so it can be tested
//! without spawning anything.

/// Extract the percentage from a `yt-dlp` progress line.
///
/// Lines look like `[download]  42.3% of 10.00MiB at 1.00MiB/s ETA 00:05`.
pub fn parse_progress_line(line: &str) -> Option<f32> {
    let trimmed = line.trim();
    if !trimmed.starts_with("[download]") {
        return None;
    }
    let percent_token = trimmed
        .split_whitespace()
        .find(|token| token.ends_with('%'))?;
    percent_token.trim_end_matches('%').parse::<f32>().ok()
}

/// Detect the "already downloaded" line so it is not treated as an error.
pub fn is_already_downloaded(line: &str) -> bool {
    line.contains("has already been downloaded")
}

/// Build the `yt-dlp` argument list for a single video.
pub fn download_args(video_id: &str, output_template: &str, rate_limit: Option<&str>) -> Vec<String> {
    let mut args = vec![
        "--no-playlist".to_owned(),
        "--no-warnings".to_owned(),
        "--newline".to_owned(),
        "--no-color".to_owned(),
        "--retries".to_owned(),
        "3".to_owned(),
        "--fragment-retries".to_owned(),
        "3".to_owned(),
        "-f".to_owned(),
        "bv*[height<=1080][ext=mp4]+ba[ext=m4a]/bv*[height<=1080]+ba/b[height<=1080]/b".to_owned(),
        "--merge-output-format".to_owned(),
        "mp4".to_owned(),
        "-o".to_owned(),
        output_template.to_owned(),
    ];
    if let Some(rate) = rate_limit {
        if !rate.is_empty() {
            args.push("--limit-rate".to_owned());
            args.push(rate.to_owned());
        }
    }
    args.push(format!("https://www.youtube.com/watch?v={video_id}"));
    args
}

/// Turn a `yt-dlp` failure into something actionable.
pub fn describe_download_error(stderr: &str) -> String {
    let lowered = stderr.to_lowercase();
    if lowered.contains("private video") {
        "That video is private and cannot be downloaded".to_owned()
    } else if lowered.contains("members-only") || lowered.contains("join this channel") {
        "That video is members-only".to_owned()
    } else if lowered.contains("age") && lowered.contains("confirm") {
        "That video is age-restricted and cannot be downloaded without sign-in".to_owned()
    } else if lowered.contains("video unavailable") || lowered.contains("removed") {
        "That video is unavailable or has been removed".to_owned()
    } else if lowered.contains("sign in to confirm") || lowered.contains("not a bot") {
        "YouTube asked for bot verification. Slow the queue down and try again later.".to_owned()
    } else {
        let detail = stderr
            .lines()
            .rev()
            .find(|line| !line.trim().is_empty())
            .unwrap_or("unknown error")
            .trim();
        format!("Download failed: {detail}")
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parses_progress_percentages() {
        assert_eq!(
            parse_progress_line("[download]  42.3% of 10.00MiB at 1.00MiB/s ETA 00:05"),
            Some(42.3)
        );
        assert_eq!(parse_progress_line("[download] 100% of 10.00MiB"), Some(100.0));
        assert_eq!(parse_progress_line("[download]   0.0% of ~1.00MiB"), Some(0.0));
    }

    #[test]
    fn ignores_non_progress_lines() {
        assert_eq!(parse_progress_line("[info] Writing metadata"), None);
        assert_eq!(parse_progress_line(""), None);
        assert_eq!(parse_progress_line("[download] Destination: out.mp4"), None);
    }

    #[test]
    fn detects_cached_downloads() {
        assert!(is_already_downloaded(
            "[download] out.mp4 has already been downloaded"
        ));
        assert!(!is_already_downloaded("[download] 10%"));
    }

    #[test]
    fn builds_arguments_with_capped_resolution() {
        let args = download_args("abc123", "/tmp/%(id)s.%(ext)s", None);
        assert!(args.contains(&"--no-playlist".to_owned()));
        assert!(args.iter().any(|a| a.contains("height<=1080")));
        assert!(args.contains(&"https://www.youtube.com/watch?v=abc123".to_owned()));
        assert!(!args.contains(&"--limit-rate".to_owned()));
    }

    #[test]
    fn adds_rate_limit_when_requested() {
        let args = download_args("abc", "out", Some("2M"));
        let index = args.iter().position(|a| a == "--limit-rate").unwrap();
        assert_eq!(args[index + 1], "2M");
        // An empty rate is ignored rather than passed through.
        assert!(!download_args("abc", "out", Some("")).contains(&"--limit-rate".to_owned()));
    }

    #[test]
    fn explains_common_download_failures() {
        assert!(describe_download_error("ERROR: Private video").contains("private"));
        assert!(describe_download_error("ERROR: Video unavailable").contains("unavailable"));
        assert!(describe_download_error("ERROR: Sign in to confirm you're not a bot")
            .contains("bot verification"));
        assert!(describe_download_error("ERROR: something odd").contains("something odd"));
    }
}
