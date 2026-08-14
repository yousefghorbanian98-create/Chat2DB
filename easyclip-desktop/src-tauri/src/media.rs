use serde::Serialize;
use std::{
    fs,
    path::{Path, PathBuf},
    time::{SystemTime, UNIX_EPOCH},
};

#[derive(Clone, Debug, Serialize, PartialEq)]
#[serde(rename_all = "camelCase")]
pub struct CaptionSegment {
    pub index: usize,
    pub start_ms: u64,
    pub end_ms: u64,
    pub text: String,
}

pub struct TemporaryDirectory {
    path: PathBuf,
}

impl TemporaryDirectory {
    pub fn new(label: &str) -> Result<Self, String> {
        let timestamp = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .map_err(|error| format!("System clock error: {error}"))?
            .as_nanos();
        let safe_label: String = label
            .chars()
            .filter(|character| character.is_ascii_alphanumeric() || matches!(character, '-' | '_'))
            .take(48)
            .collect();
        let path = std::env::temp_dir()
            .join("easyclip-desktop")
            .join(format!("{}-{}-{timestamp}", if safe_label.is_empty() { "job" } else { &safe_label }, std::process::id()));
        fs::create_dir_all(&path).map_err(|error| format!("Cannot create temporary workspace: {error}"))?;
        Ok(Self { path })
    }

    pub fn path(&self) -> &Path {
        &self.path
    }
}

impl Drop for TemporaryDirectory {
    fn drop(&mut self) {
        let _ = fs::remove_dir_all(&self.path);
    }
}

pub fn parse_srt(contents: &str) -> Result<Vec<CaptionSegment>, String> {
    let normalized = contents.trim_start_matches('\u{feff}').replace("\r\n", "\n").replace('\r', "\n");
    let mut segments = Vec::new();

    for block in normalized.split("\n\n").filter(|block| !block.trim().is_empty()) {
        let lines: Vec<&str> = block.lines().collect();
        if lines.len() < 2 {
            continue;
        }

        let (timing_index, source_index) = if lines[0].contains("-->") { (0, segments.len() + 1) } else { (1, lines[0].trim().parse().unwrap_or(segments.len() + 1)) };
        let timing = lines
            .get(timing_index)
            .ok_or_else(|| "Caption block is missing a timestamp".to_owned())?;
        let (start, end) = timing
            .split_once("-->")
            .ok_or_else(|| format!("Invalid SRT timestamp: {timing}"))?;
        let start_ms = parse_srt_timestamp(start.trim())?;
        let end_token = end.split_whitespace().next().unwrap_or_default();
        let end_ms = parse_srt_timestamp(end_token)?;
        if end_ms <= start_ms {
            return Err(format!("Caption {source_index} has an invalid time range"));
        }

        let text = lines[(timing_index + 1)..].join("\n").trim().to_owned();
        if !text.is_empty() {
            segments.push(CaptionSegment {
                index: source_index,
                start_ms,
                end_ms,
                text,
            });
        }
    }

    if segments.is_empty() {
        return Err("The SRT file contains no readable caption segments".to_owned());
    }
    Ok(segments)
}

pub fn captions_for_clip(contents: &str, start_seconds: f64, end_seconds: f64) -> Result<Option<String>, String> {
    let start_ms = (start_seconds * 1000.0).round() as u64;
    let end_ms = (end_seconds * 1000.0).round() as u64;
    let clipped: Vec<CaptionSegment> = parse_srt(contents)?
        .into_iter()
        .filter_map(|segment| {
            let overlap_start = segment.start_ms.max(start_ms);
            let overlap_end = segment.end_ms.min(end_ms);
            (overlap_end > overlap_start).then(|| CaptionSegment {
                index: 0,
                start_ms: overlap_start - start_ms,
                end_ms: overlap_end - start_ms,
                text: segment.text,
            })
        })
        .collect();

    if clipped.is_empty() {
        return Ok(None);
    }

    let mut output = String::new();
    for (index, segment) in clipped.iter().enumerate() {
        output.push_str(&format!(
            "{}\n{} --> {}\n{}\n\n",
            index + 1,
            format_srt_timestamp(segment.start_ms),
            format_srt_timestamp(segment.end_ms),
            segment.text
        ));
    }
    Ok(Some(output))
}

pub fn ensure_output_extension(path: &Path, expected: &str) -> Result<(), String> {
    let extension = path.extension().and_then(|value| value.to_str()).unwrap_or_default();
    if !extension.eq_ignore_ascii_case(expected) {
        return Err(format!("Output file must use the .{expected} extension"));
    }
    if let Some(parent) = path.parent().filter(|parent| !parent.as_os_str().is_empty()) {
        fs::create_dir_all(parent).map_err(|error| format!("Cannot create output folder: {error}"))?;
    }
    Ok(())
}

pub fn paths_are_equal(first: &Path, second: &Path) -> bool {
    if cfg!(target_os = "windows") {
        first.to_string_lossy().eq_ignore_ascii_case(&second.to_string_lossy())
    } else {
        first == second
    }
}

pub fn escaped_filter_path(path: &Path) -> String {
    path.to_string_lossy()
        .replace('\\', "/")
        .replace(':', "\\:")
        .replace('\'', "\\'")
        .replace('[', "\\[")
        .replace(']', "\\]")
        .replace(',', "\\,")
        .replace(';', "\\;")
}

fn parse_srt_timestamp(value: &str) -> Result<u64, String> {
    let value = value.replace('.', ",");
    let (clock, milliseconds) = value
        .split_once(',')
        .ok_or_else(|| format!("Invalid SRT timestamp: {value}"))?;
    let parts: Vec<&str> = clock.split(':').collect();
    if parts.len() != 3 {
        return Err(format!("Invalid SRT timestamp: {value}"));
    }
    let hours: u64 = parts[0].parse().map_err(|_| format!("Invalid SRT timestamp: {value}"))?;
    let minutes: u64 = parts[1].parse().map_err(|_| format!("Invalid SRT timestamp: {value}"))?;
    let seconds: u64 = parts[2].parse().map_err(|_| format!("Invalid SRT timestamp: {value}"))?;
    let millis: u64 = milliseconds
        .chars()
        .take(3)
        .collect::<String>()
        .parse()
        .map_err(|_| format!("Invalid SRT timestamp: {value}"))?;
    Ok((((hours * 60) + minutes) * 60 + seconds) * 1000 + millis)
}

fn format_srt_timestamp(milliseconds: u64) -> String {
    let hours = milliseconds / 3_600_000;
    let minutes = (milliseconds % 3_600_000) / 60_000;
    let seconds = (milliseconds % 60_000) / 1000;
    let millis = milliseconds % 1000;
    format!("{hours:02}:{minutes:02}:{seconds:02},{millis:03}")
}

#[cfg(test)]
mod tests {
    use super::*;

    const SAMPLE: &str = "\u{feff}1\r\n00:00:01,250 --> 00:00:03,500\r\nسلام دنیا\r\n\r\n2\r\n00:00:04.000 --> 00:00:06.250\r\nHello\r\nworld\r\n";

    #[test]
    fn parses_multilingual_srt_and_multiline_text() {
        let segments = parse_srt(SAMPLE).expect("SRT should parse");
        assert_eq!(segments.len(), 2);
        assert_eq!(segments[0].text, "سلام دنیا");
        assert_eq!(segments[1].text, "Hello\nworld");
        assert_eq!(segments[1].end_ms, 6250);
    }

    #[test]
    fn clips_and_rebases_source_timeline_captions() {
        let output = captions_for_clip(SAMPLE, 2.0, 5.0)
            .expect("captions should clip")
            .expect("captions should overlap");
        assert!(output.contains("00:00:00,000 --> 00:00:01,500"));
        assert!(output.contains("00:00:02,000 --> 00:00:03,000"));
        assert!(output.contains("سلام دنیا"));
    }

    #[test]
    fn returns_none_when_clip_has_no_captions() {
        assert_eq!(captions_for_clip(SAMPLE, 10.0, 12.0).unwrap(), None);
    }

    #[test]
    fn escapes_windows_filter_paths() {
        let escaped = escaped_filter_path(Path::new("C:\\Creator's Clips\\captions[1].srt"));
        assert_eq!(escaped, "C\\:/Creator\\'s Clips/captions\\[1\\].srt");
    }
}
