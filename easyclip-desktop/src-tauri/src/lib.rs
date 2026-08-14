mod media;
mod youtube;

use media::{captions_for_clip, ensure_output_extension, escaped_filter_path, parse_srt, paths_are_equal, CaptionSegment, TemporaryDirectory};
use serde::{Deserialize, Serialize};
use std::{
    fs,
    path::{Path, PathBuf},
    process::{Command, Output, Stdio},
};
use tauri::{AppHandle, Emitter, Manager};

#[cfg(target_os = "windows")]
use std::os::windows::process::CommandExt;

fn media_command(executable: impl AsRef<std::ffi::OsStr>) -> Command {
    let mut command = Command::new(executable);
    #[cfg(target_os = "windows")]
    command.creation_flags(0x0800_0000); // CREATE_NO_WINDOW
    command
}

#[derive(Serialize)]
struct SystemProfile {
    os: String,
    arch: String,
    nvidia_available: bool,
    gpu_name: Option<String>,
    ffmpeg_available: bool,
    whisper_available: bool,
    model_available: bool,
}

#[derive(Serialize)]
struct VideoFile {
    name: String,
    path: String,
    size_bytes: u64,
    extension: String,
    duration_seconds: f64,
    width: u32,
    height: u32,
    codec: String,
}

#[derive(Deserialize)]
#[serde(rename_all = "camelCase")]
struct TranscriptionRequest {
    input_path: String,
    output_path: String,
    language: String,
    job_id: String,
}

#[derive(Serialize)]
#[serde(rename_all = "camelCase")]
struct TranscriptionResult {
    subtitle_path: String,
    language: String,
    duration_seconds: f64,
    segments: Vec<CaptionSegment>,
}

#[derive(Clone, Serialize)]
#[serde(rename_all = "camelCase")]
struct TranscriptionProgress {
    job_id: String,
    stage: String,
    progress: u8,
}

#[derive(Deserialize)]
#[serde(rename_all = "camelCase")]
struct RenderRequest {
    input_path: String,
    output_path: String,
    start_seconds: f64,
    end_seconds: f64,
    caption_path: Option<String>,
    use_nvidia: bool,
}

#[derive(Serialize)]
#[serde(rename_all = "camelCase")]
struct RenderResult {
    output_path: String,
    used_nvidia: bool,
    duration_seconds: f64,
}

fn bundled_resource(app: &AppHandle, relative_path: impl AsRef<Path>) -> PathBuf {
    let relative_path = relative_path.as_ref();
    app.path()
        .resource_dir()
        .ok()
        .map(|directory| directory.join(relative_path))
        .filter(|path| path.exists())
        .unwrap_or_else(|| PathBuf::from(relative_path))
}

/// Public wrapper so the youtube module can spawn bundled tools.
pub fn media_command_public(executable: impl AsRef<std::ffi::OsStr>) -> Command {
    media_command(executable)
}

/// Public wrapper so the youtube module can locate bundled tools.
pub fn bundled_tool_path(app: &AppHandle, name: &str) -> PathBuf {
    bundled_tool(app, name)
}

fn bundled_tool(app: &AppHandle, name: &str) -> PathBuf {
    let executable = if cfg!(target_os = "windows") {
        format!("{name}.exe")
    } else {
        name.to_owned()
    };
    let bundled = bundled_resource(app, Path::new("bin").join(&executable));
    if bundled.exists() {
        bundled
    } else {
        PathBuf::from(executable)
    }
}

fn command_available(executable: &Path, version_argument: &str) -> bool {
    media_command(executable)
        .arg(version_argument)
        .stdout(Stdio::null())
        .stderr(Stdio::null())
        .status()
        .is_ok_and(|status| status.success())
}

fn ffmpeg_has_encoder(executable: &Path, encoder: &str) -> bool {
    media_command(executable)
        .args(["-hide_banner", "-encoders"])
        .output()
        .ok()
        .filter(|result| result.status.success())
        .map(|result| String::from_utf8_lossy(&result.stdout).contains(encoder))
        .unwrap_or(false)
}

fn nvidia_gpu() -> Option<String> {
    media_command("nvidia-smi")
        .args(["--query-gpu=name", "--format=csv,noheader"])
        .output()
        .ok()
        .filter(|result| result.status.success())
        .and_then(|result| String::from_utf8(result.stdout).ok())
        .and_then(|output| output.lines().next().map(str::trim).map(str::to_owned))
        .filter(|name| !name.is_empty())
}

fn emit_transcription_progress(app: &AppHandle, job_id: &str, stage: &str, progress: u8) {
    let _ = app.emit(
        "transcription-progress",
        TranscriptionProgress {
            job_id: job_id.to_owned(),
            stage: stage.to_owned(),
            progress,
        },
    );
}

#[tauri::command]
fn system_profile(app: AppHandle) -> SystemProfile {
    let gpu_name = nvidia_gpu();
    let ffmpeg = bundled_tool(&app, "ffmpeg");
    let whisper = bundled_tool(&app, "whisper-cli");
    SystemProfile {
        os: std::env::consts::OS.to_owned(),
        arch: std::env::consts::ARCH.to_owned(),
        nvidia_available: gpu_name.is_some() && ffmpeg_has_encoder(&ffmpeg, "h264_nvenc"),
        gpu_name,
        ffmpeg_available: command_available(&ffmpeg, "-version"),
        whisper_available: command_available(&whisper, "--version"),
        model_available: bundled_resource(&app, "models/ggml-base.bin").is_file(),
    }
}

#[tauri::command]
fn inspect_video(app: AppHandle, path: String) -> Result<VideoFile, String> {
    let file_path = Path::new(&path);
    let allowed = ["mp4", "mov", "mkv", "webm", "avi", "m4v"];
    let extension = file_path
        .extension()
        .and_then(|value| value.to_str())
        .unwrap_or_default()
        .to_lowercase();

    if !allowed.contains(&extension.as_str()) {
        return Err("Unsupported video format".to_owned());
    }

    let metadata = file_path.metadata().map_err(|error| format!("Unable to read video: {error}"))?;
    if !metadata.is_file() {
        return Err("Selected path is not a file".to_owned());
    }

    let output = media_command(bundled_tool(&app, "ffprobe"))
        .args([
            "-v",
            "error",
            "-select_streams",
            "v:0",
            "-show_entries",
            "stream=width,height,codec_name:format=duration",
            "-of",
            "json",
            &path,
        ])
        .output()
        .map_err(|error| format!("FFprobe is not available: {error}"))?;

    if !output.status.success() {
        return Err(format!("FFprobe failed: {}", String::from_utf8_lossy(&output.stderr).trim()));
    }

    let probe: serde_json::Value = serde_json::from_slice(&output.stdout).map_err(|error| format!("Invalid FFprobe response: {error}"))?;
    let stream = probe["streams"]
        .as_array()
        .and_then(|items| items.first())
        .ok_or_else(|| "No video stream was found".to_owned())?;
    let duration_seconds = probe["format"]["duration"]
        .as_str()
        .and_then(|value| value.parse().ok())
        .unwrap_or_default();

    Ok(VideoFile {
        name: file_path.file_name().and_then(|value| value.to_str()).unwrap_or("video").to_owned(),
        path,
        size_bytes: metadata.len(),
        extension,
        duration_seconds,
        width: stream["width"].as_u64().unwrap_or_default() as u32,
        height: stream["height"].as_u64().unwrap_or_default() as u32,
        codec: stream["codec_name"].as_str().unwrap_or("unknown").to_owned(),
    })
}

#[tauri::command]
async fn generate_subtitles(app: AppHandle, request: TranscriptionRequest) -> Result<TranscriptionResult, String> {
    if !matches!(request.language.as_str(), "fa" | "en" | "auto") {
        return Err("Caption language must be fa, en, or auto".to_owned());
    }
    let input_path = PathBuf::from(&request.input_path);
    let output_path = PathBuf::from(&request.output_path);
    if !input_path.is_file() {
        return Err("Input video does not exist".to_owned());
    }
    ensure_output_extension(&output_path, "srt")?;
    if paths_are_equal(&input_path, &output_path) {
        return Err("Subtitle output cannot overwrite the input video".to_owned());
    }

    let ffmpeg = bundled_tool(&app, "ffmpeg");
    let whisper = bundled_tool(&app, "whisper-cli");
    let model = bundled_resource(&app, "models/ggml-base.bin");
    if !command_available(&ffmpeg, "-version") {
        return Err("Bundled FFmpeg is unavailable. Reinstall EasyClip Desktop.".to_owned());
    }
    if !command_available(&whisper, "--version") {
        return Err("Bundled whisper.cpp is unavailable. Reinstall EasyClip Desktop.".to_owned());
    }
    if !model.is_file() {
        return Err("Bundled multilingual Whisper model is unavailable. Reinstall EasyClip Desktop.".to_owned());
    }

    let job_id = request.job_id.clone();
    let language = request.language.clone();
    let app_for_task = app.clone();
    let result = tauri::async_runtime::spawn_blocking(move || -> Result<TranscriptionResult, String> {
        let workspace = TemporaryDirectory::new(&job_id)?;
        let audio_path = workspace.path().join("audio-16khz.wav");
        let transcript_prefix = workspace.path().join("captions");

        emit_transcription_progress(&app_for_task, &job_id, "extracting", 8);
        let extraction = media_command(&ffmpeg)
            .args(["-hide_banner", "-loglevel", "error", "-y", "-i"])
            .arg(&input_path)
            .args(["-vn", "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le"])
            .arg(&audio_path)
            .output()
            .map_err(|error| format!("Cannot start FFmpeg audio extraction: {error}"))?;
        if !extraction.status.success() {
            return Err(format!("Audio extraction failed: {}", String::from_utf8_lossy(&extraction.stderr).trim()));
        }

        emit_transcription_progress(&app_for_task, &job_id, "transcribing", 28);
        let threads = std::thread::available_parallelism().map(usize::from).unwrap_or(4).clamp(2, 8).to_string();
        let transcription = media_command(&whisper)
            .arg("-m")
            .arg(&model)
            .arg("-f")
            .arg(&audio_path)
            .args(["-l", &language, "-t", &threads, "-ml", "42", "-sow", "-osrt", "-np", "-of"])
            .arg(&transcript_prefix)
            .output()
            .map_err(|error| format!("Cannot start whisper.cpp: {error}"))?;
        if !transcription.status.success() {
            let details = String::from_utf8_lossy(&transcription.stderr);
            return Err(format!("Whisper transcription failed: {}", details.trim()));
        }

        emit_transcription_progress(&app_for_task, &job_id, "writing", 92);
        let generated_path = transcript_prefix.with_extension("srt");
        let generated = fs::read_to_string(&generated_path).map_err(|error| format!("Whisper did not create a valid UTF-8 SRT file: {error}"))?;
        let segments = parse_srt(&generated)?;
        fs::copy(&generated_path, &output_path).map_err(|error| format!("Cannot save subtitle file: {error}"))?;
        let duration_seconds = segments.last().map(|segment| segment.end_ms as f64 / 1000.0).unwrap_or_default();
        emit_transcription_progress(&app_for_task, &job_id, "complete", 100);

        Ok(TranscriptionResult {
            subtitle_path: output_path.to_string_lossy().into_owned(),
            language,
            duration_seconds,
            segments,
        })
    })
    .await
    .map_err(|error| format!("Transcription task failed: {error}"))?;

    result
}

fn run_ffmpeg_render(
    executable: &Path,
    input: &Path,
    output: &Path,
    start: &str,
    duration: &str,
    filter: &str,
    use_nvidia: bool,
) -> std::io::Result<Output> {
    let mut command = media_command(executable);
    command
        .args(["-hide_banner", "-y", "-ss", start, "-i"])
        .arg(input)
        .args(["-t", duration, "-map", "0:v:0", "-map", "0:a:0?", "-sn", "-vf", filter]);
    if use_nvidia {
        command.args(["-c:v", "h264_nvenc", "-preset", "p5", "-cq", "21"]);
    } else {
        command.args(["-c:v", "libx264", "-preset", "medium", "-crf", "21"]);
    }
    command
        .args(["-c:a", "aac", "-b:a", "192k", "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-avoid_negative_ts", "make_zero"])
        .arg(output)
        .output()
}

#[tauri::command]
async fn render_vertical_clip(app: AppHandle, request: RenderRequest) -> Result<RenderResult, String> {
    if !request.start_seconds.is_finite()
        || !request.end_seconds.is_finite()
        || request.start_seconds < 0.0
        || request.end_seconds <= request.start_seconds
    {
        return Err("Invalid clip time range".to_owned());
    }
    if request.end_seconds - request.start_seconds > 180.0 {
        return Err("A clip cannot be longer than 180 seconds".to_owned());
    }

    let input_path = PathBuf::from(&request.input_path);
    let output_path = PathBuf::from(&request.output_path);
    if !input_path.is_file() {
        return Err("Input video does not exist".to_owned());
    }
    ensure_output_extension(&output_path, "mp4")?;
    if paths_are_equal(&input_path, &output_path) {
        return Err("Output clip cannot overwrite the input video".to_owned());
    }

    let ffmpeg = bundled_tool(&app, "ffmpeg");
    if !command_available(&ffmpeg, "-version") {
        return Err("Bundled FFmpeg is unavailable. Reinstall EasyClip Desktop.".to_owned());
    }

    let workspace = TemporaryDirectory::new("render")?;
    let mut filter = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920".to_owned();
    if let Some(caption_path) = request.caption_path.as_deref() {
        let caption_path = PathBuf::from(caption_path);
        if !caption_path.is_file() {
            return Err("The selected SRT caption file no longer exists".to_owned());
        }
        let contents = fs::read_to_string(&caption_path).map_err(|error| format!("Caption file must be UTF-8 SRT: {error}"))?;
        if let Some(clipped_captions) = captions_for_clip(&contents, request.start_seconds, request.end_seconds)? {
            let clipped_path = workspace.path().join("clip-captions.srt");
            fs::write(&clipped_path, clipped_captions).map_err(|error| format!("Cannot prepare captions for rendering: {error}"))?;
            let font_directory = bundled_resource(&app, "fonts");
            let fonts_option = font_directory
                .is_dir()
                .then(|| format!(":fontsdir='{}'", escaped_filter_path(&font_directory)))
                .unwrap_or_default();
            filter.push_str(&format!(
                ",subtitles=filename='{}'{}:charenc=UTF-8:force_style='FontName=Noto Sans Arabic,FontSize=18,PrimaryColour=&H00FFFFFF,OutlineColour=&H00101010,BackColour=&H80000000,BorderStyle=1,Outline=3,Shadow=1,Alignment=2,MarginV=120'",
                escaped_filter_path(&clipped_path), fonts_option
            ));
        }
    }

    let nvidia_encoder_available = request.use_nvidia && nvidia_gpu().is_some() && ffmpeg_has_encoder(&ffmpeg, "h264_nvenc");
    let input_for_task = input_path.clone();
    let output_for_task = output_path.clone();
    let start = format!("{:.3}", request.start_seconds);
    let duration_value = request.end_seconds - request.start_seconds;
    let duration = format!("{duration_value:.3}");

    let result = tauri::async_runtime::spawn_blocking(move || -> Result<bool, String> {
        let first = run_ffmpeg_render(&ffmpeg, &input_for_task, &output_for_task, &start, &duration, &filter, nvidia_encoder_available)
            .map_err(|error| format!("Cannot start FFmpeg: {error}"))?;
        if first.status.success() {
            return Ok(nvidia_encoder_available);
        }

        let first_error = String::from_utf8_lossy(&first.stderr).trim().to_owned();
        if !nvidia_encoder_available {
            let _ = fs::remove_file(&output_for_task);
            return Err(format!("FFmpeg failed: {first_error}"));
        }

        let _ = fs::remove_file(&output_for_task);
        let fallback = run_ffmpeg_render(&ffmpeg, &input_for_task, &output_for_task, &start, &duration, &filter, false)
            .map_err(|error| format!("Cannot start FFmpeg CPU fallback: {error}"))?;
        if !fallback.status.success() {
            let _ = fs::remove_file(&output_for_task);
            return Err(format!(
                "NVIDIA render failed ({first_error}); CPU fallback failed: {}",
                String::from_utf8_lossy(&fallback.stderr).trim()
            ));
        }
        Ok(false)
    })
    .await
    .map_err(|error| format!("Render task failed: {error}"))??;

    Ok(RenderResult {
        output_path: output_path.to_string_lossy().into_owned(),
        used_nvidia: result,
        duration_seconds: duration_value,
    })
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_dialog::init())
        .plugin(tauri_plugin_opener::init())
        .manage(youtube::YoutubeState::default())
        .invoke_handler(tauri::generate_handler![
            system_profile,
            inspect_video,
            generate_subtitles,
            render_vertical_clip,
            youtube::autopilot_status,
            youtube::autopilot_save_credentials,
            youtube::autopilot_connect,
            youtube::autopilot_disconnect,
            youtube::autopilot_load_source,
            youtube::autopilot_acknowledge,
            youtube::autopilot_enqueue,
            youtube::autopilot_set_paused,
            youtube::autopilot_remove_job,
            youtube::autopilot_self_test,
            youtube::autopilot_run_job
        ])
        .run(tauri::generate_context!())
        .expect("error while running EasyClip Desktop");
}
