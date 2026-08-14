//! Pure, dependency-light helpers for the YouTube Autopilot feature.
//!
//! Everything in this module is deterministic and unit tested. No network, no
//! filesystem, no clock. Keeping the fiddly string logic here means the parts of
//! the feature that are easiest to get wrong are also the parts that are easiest
//! to verify.

/// A reference to something on YouTube, resolved from arbitrary user input.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum SourceRef {
    /// A single video id (11 characters).
    Video(String),
    /// A canonical channel id (starts with `UC`).
    Channel(String),
    /// An `@handle` (without the `@`).
    Handle(String),
    /// A legacy `/c/name` or `/user/name` vanity name.
    LegacyName(String),
    /// A playlist id.
    Playlist(String),
}

fn strip_scheme_and_host(input: &str) -> Option<&str> {
    let without_scheme = input
        .strip_prefix("https://")
        .or_else(|| input.strip_prefix("http://"))
        .unwrap_or(input);
    let without_www = without_scheme.strip_prefix("www.").unwrap_or(without_scheme);

    for host in [
        "m.youtube.com/",
        "music.youtube.com/",
        "youtube.com/",
        "youtu.be/",
    ] {
        if let Some(rest) = without_www.strip_prefix(host) {
            return Some(rest);
        }
    }
    None
}

fn query_value<'a>(path: &'a str, key: &str) -> Option<&'a str> {
    let (_, query) = path.split_once('?')?;
    for pair in query.split('&') {
        let (name, value) = pair.split_once('=')?;
        if name == key && !value.is_empty() {
            return Some(value);
        }
    }
    None
}

fn trim_path(segment: &str) -> &str {
    segment
        .split('?')
        .next()
        .unwrap_or("")
        .split('#')
        .next()
        .unwrap_or("")
        .trim_end_matches('/')
}

fn looks_like_video_id(value: &str) -> bool {
    value.len() == 11
        && value
            .chars()
            .all(|c| c.is_ascii_alphanumeric() || c == '-' || c == '_')
}

/// Resolve any YouTube URL (or a bare id/handle) into a [`SourceRef`].
///
/// Accepts `watch?v=`, `youtu.be/`, `/shorts/`, `/live/`, `/embed/`,
/// `/channel/UC…`, `/@handle`, `/c/name`, `/user/name`, `playlist?list=` and
/// bare ids, with or without a scheme, `www.`, `m.` or `music.` prefix.
pub fn parse_source(input: &str) -> Result<SourceRef, String> {
    let input = input.trim();
    if input.is_empty() {
        return Err("Enter a YouTube video or channel link".to_owned());
    }

    if let Some(rest) = strip_scheme_and_host(input) {
        // youtu.be/<id> has the id as the first path segment.
        if input.contains("youtu.be/") {
            let id = trim_path(rest);
            if looks_like_video_id(id) {
                return Ok(SourceRef::Video(id.to_owned()));
            }
            return Err("That youtu.be link does not contain a valid video id".to_owned());
        }

        if let Some(id) = query_value(rest, "v") {
            let id = trim_path(id);
            if looks_like_video_id(id) {
                return Ok(SourceRef::Video(id.to_owned()));
            }
            return Err("That link does not contain a valid video id".to_owned());
        }

        if let Some(list) = query_value(rest, "list") {
            return Ok(SourceRef::Playlist(trim_path(list).to_owned()));
        }

        for prefix in ["shorts/", "live/", "embed/", "v/"] {
            if let Some(tail) = rest.strip_prefix(prefix) {
                let id = trim_path(tail).split('/').next().unwrap_or("");
                if looks_like_video_id(id) {
                    return Ok(SourceRef::Video(id.to_owned()));
                }
                return Err("That link does not contain a valid video id".to_owned());
            }
        }

        if let Some(tail) = rest.strip_prefix("channel/") {
            let id = trim_path(tail).split('/').next().unwrap_or("");
            if id.starts_with("UC") && id.len() > 10 {
                return Ok(SourceRef::Channel(id.to_owned()));
            }
            return Err("That link does not contain a valid channel id".to_owned());
        }

        if let Some(tail) = rest.strip_prefix('@') {
            let handle = trim_path(tail).split('/').next().unwrap_or("");
            if !handle.is_empty() {
                return Ok(SourceRef::Handle(handle.to_owned()));
            }
        }

        for prefix in ["c/", "user/"] {
            if let Some(tail) = rest.strip_prefix(prefix) {
                let name = trim_path(tail).split('/').next().unwrap_or("");
                if !name.is_empty() {
                    return Ok(SourceRef::LegacyName(name.to_owned()));
                }
            }
        }

        return Err("Unrecognised YouTube link".to_owned());
    }

    // Bare values, no URL.
    if let Some(handle) = input.strip_prefix('@') {
        if !handle.is_empty() {
            return Ok(SourceRef::Handle(handle.to_owned()));
        }
    }
    if input.starts_with("UC") && input.len() > 10 {
        return Ok(SourceRef::Channel(input.to_owned()));
    }
    if input.starts_with("PL") || input.starts_with("UU") || input.starts_with("OL") {
        return Ok(SourceRef::Playlist(input.to_owned()));
    }
    if looks_like_video_id(input) {
        return Ok(SourceRef::Video(input.to_owned()));
    }

    Err("Unrecognised YouTube link".to_owned())
}

/// Convert a channel id into its "uploads" playlist id.
///
/// Every channel `UC…` has a matching uploads playlist `UU…`. Using this avoids
/// an API round trip, and avoids `search.list` which costs 100 quota units and
/// silently truncates long catalogues.
pub fn uploads_playlist_for_channel(channel_id: &str) -> Option<String> {
    let rest = channel_id.strip_prefix("UC")?;
    if rest.is_empty() {
        return None;
    }
    Some(format!("UU{rest}"))
}

/// Percent-encode a string for use in a query component.
pub fn percent_encode(value: &str) -> String {
    let mut out = String::with_capacity(value.len());
    for byte in value.as_bytes() {
        match byte {
            b'A'..=b'Z' | b'a'..=b'z' | b'0'..=b'9' | b'-' | b'_' | b'.' | b'~' => {
                out.push(*byte as char)
            }
            _ => out.push_str(&format!("%{byte:02X}")),
        }
    }
    out
}

/// Decode a percent-encoded query component (also turns `+` into a space).
pub fn percent_decode(value: &str) -> String {
    let bytes = value.as_bytes();
    let mut out: Vec<u8> = Vec::with_capacity(bytes.len());
    let mut index = 0;
    while index < bytes.len() {
        match bytes[index] {
            b'%' if index + 2 < bytes.len() => {
                let hex = std::str::from_utf8(&bytes[index + 1..index + 3]).unwrap_or("");
                match u8::from_str_radix(hex, 16) {
                    Ok(decoded) => {
                        out.push(decoded);
                        index += 3;
                    }
                    Err(_) => {
                        out.push(bytes[index]);
                        index += 1;
                    }
                }
            }
            b'+' => {
                out.push(b' ');
                index += 1;
            }
            other => {
                out.push(other);
                index += 1;
            }
        }
    }
    String::from_utf8_lossy(&out).into_owned()
}

/// YouTube rejects `<` and `>` in titles and descriptions.
pub fn strip_angle_brackets(value: &str) -> String {
    value.replace(['<', '>'], "")
}

/// Truncate to at most `limit` *characters* (not bytes).
///
/// YouTube counts characters, and Persian text is multi-byte, so naive byte
/// slicing both over-truncates and can panic on a char boundary.
pub fn truncate_chars(value: &str, limit: usize) -> String {
    if value.chars().count() <= limit {
        return value.to_owned();
    }
    value.chars().take(limit).collect()
}

/// Build a YouTube-safe video title (≤ 100 characters, no angle brackets).
pub fn safe_title(value: &str) -> String {
    let cleaned = strip_angle_brackets(value.trim());
    let cleaned = if cleaned.trim().is_empty() {
        "Untitled".to_owned()
    } else {
        cleaned
    };
    truncate_chars(&cleaned, 100)
}

/// Build a YouTube-safe description (≤ 5000 characters, no angle brackets).
pub fn safe_description(value: &str) -> String {
    truncate_chars(&strip_angle_brackets(value), 5000)
}

/// Context for [`apply_template`].
pub struct TemplateContext<'a> {
    pub title: &'a str,
    pub channel: &'a str,
    pub video_id: &'a str,
    pub index: usize,
    pub date: &'a str,
}

/// Substitute `{title}`, `{channel}`, `{id}`, `{index}` and `{date}` tokens.
pub fn apply_template(template: &str, context: &TemplateContext) -> String {
    template
        .replace("{title}", context.title)
        .replace("{channel}", context.channel)
        .replace("{id}", context.video_id)
        .replace("{index}", &context.index.to_string())
        .replace("{date}", context.date)
}

/// Format seconds as `H:MM:SS` or `M:SS`.
pub fn format_duration(total_seconds: u64) -> String {
    let hours = total_seconds / 3600;
    let minutes = (total_seconds % 3600) / 60;
    let seconds = total_seconds % 60;
    if hours > 0 {
        format!("{hours}:{minutes:02}:{seconds:02}")
    } else {
        format!("{minutes}:{seconds:02}")
    }
}

/// Parse an ISO 8601 duration as returned by `videos.list` (e.g. `PT1H2M3S`).
pub fn parse_iso8601_duration(value: &str) -> u64 {
    let Some(rest) = value.strip_prefix("PT") else {
        return 0;
    };
    let mut total = 0u64;
    let mut number = String::new();
    for character in rest.chars() {
        if character.is_ascii_digit() {
            number.push(character);
            continue;
        }
        let parsed: u64 = number.parse().unwrap_or(0);
        number.clear();
        match character {
            'H' => total += parsed * 3600,
            'M' => total += parsed * 60,
            'S' => total += parsed,
            _ => {}
        }
    }
    total
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parses_every_video_url_shape() {
        let expected = SourceRef::Video("dQw4w9WgXcQ".to_owned());
        for input in [
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "http://youtube.com/watch?v=dQw4w9WgXcQ",
            "https://m.youtube.com/watch?v=dQw4w9WgXcQ&t=42s",
            "https://youtu.be/dQw4w9WgXcQ",
            "https://youtu.be/dQw4w9WgXcQ?si=abcdef",
            "https://www.youtube.com/shorts/dQw4w9WgXcQ",
            "https://www.youtube.com/live/dQw4w9WgXcQ",
            "https://www.youtube.com/embed/dQw4w9WgXcQ",
            "www.youtube.com/watch?v=dQw4w9WgXcQ",
            "dQw4w9WgXcQ",
        ] {
            assert_eq!(parse_source(input).unwrap(), expected, "input: {input}");
        }
    }

    #[test]
    fn parses_channel_handle_and_legacy_urls() {
        assert_eq!(
            parse_source("https://www.youtube.com/channel/UCabcdefghijklmnop").unwrap(),
            SourceRef::Channel("UCabcdefghijklmnop".to_owned())
        );
        assert_eq!(
            parse_source("https://www.youtube.com/@SomeCreator").unwrap(),
            SourceRef::Handle("SomeCreator".to_owned())
        );
        assert_eq!(
            parse_source("@SomeCreator").unwrap(),
            SourceRef::Handle("SomeCreator".to_owned())
        );
        assert_eq!(
            parse_source("https://www.youtube.com/c/LegacyName/videos").unwrap(),
            SourceRef::LegacyName("LegacyName".to_owned())
        );
        assert_eq!(
            parse_source("https://www.youtube.com/user/OldName").unwrap(),
            SourceRef::LegacyName("OldName".to_owned())
        );
    }

    #[test]
    fn parses_playlists() {
        assert_eq!(
            parse_source("https://www.youtube.com/playlist?list=PLabcdef").unwrap(),
            SourceRef::Playlist("PLabcdef".to_owned())
        );
    }

    #[test]
    fn rejects_malformed_input() {
        for input in ["", "   ", "https://vimeo.com/12345", "not a link"] {
            assert!(parse_source(input).is_err(), "should reject: {input}");
        }
    }

    #[test]
    fn derives_uploads_playlist() {
        assert_eq!(
            uploads_playlist_for_channel("UCabcdef").as_deref(),
            Some("UUabcdef")
        );
        assert_eq!(uploads_playlist_for_channel("PLnope"), None);
    }

    #[test]
    fn percent_round_trips_persian() {
        let original = "سلام EasyClip";
        assert_eq!(percent_decode(&percent_encode(original)), original);
    }

    #[test]
    fn percent_decode_handles_plus_and_literals() {
        assert_eq!(percent_decode("a+b"), "a b");
        assert_eq!(percent_decode("100%"), "100%");
    }

    #[test]
    fn truncates_persian_titles_without_splitting_characters() {
        // 150 Persian characters: every char is multi-byte in UTF-8.
        let long = "ب".repeat(150);
        let title = safe_title(&long);
        assert_eq!(title.chars().count(), 100);
        // The real assertion: the result is still valid UTF-8 Persian text.
        assert!(title.chars().all(|c| c == 'ب'));
    }

    #[test]
    fn safe_title_strips_brackets_and_handles_empty() {
        assert_eq!(safe_title("  <script>hi  "), "scripthi");
        assert_eq!(safe_title("   "), "Untitled");
    }

    #[test]
    fn applies_template_tokens() {
        let context = TemplateContext {
            title: "My Video",
            channel: "Creator",
            video_id: "abc123",
            index: 7,
            date: "2026-08-14",
        };
        assert_eq!(
            apply_template("{index}. {title} — {channel} ({date}) {id}", &context),
            "7. My Video — Creator (2026-08-14) abc123"
        );
    }

    #[test]
    fn formats_durations() {
        assert_eq!(format_duration(59), "0:59");
        assert_eq!(format_duration(605), "10:05");
        assert_eq!(format_duration(3725), "1:02:05");
    }

    #[test]
    fn parses_iso8601_durations() {
        assert_eq!(parse_iso8601_duration("PT1H2M3S"), 3723);
        assert_eq!(parse_iso8601_duration("PT45S"), 45);
        assert_eq!(parse_iso8601_duration("PT10M"), 600);
        assert_eq!(parse_iso8601_duration("garbage"), 0);
    }
}
