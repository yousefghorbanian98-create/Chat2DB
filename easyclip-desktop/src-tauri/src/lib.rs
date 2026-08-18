use serde::{Deserialize, Serialize};
use std::{
    path::{Path, PathBuf},
    process::{Command, Stdio},
};
use tauri::{AppHandle, Manager};

#[derive(Serialize)]
struct SystemProfile {
    os: String,
    arch: String,
    nvidia_available: bool,
    gpu_name: Option<String>,
    ffmpeg_available: bool,
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

#[derive(Deserialize)]
#[serde(rename_all = "camelCase")]
struct AnalyzeRequest {
    input_path: String,
    output_dir: String,
    model: String,
    language: String,
    target_duration: u32,
    clip_count: u32,
}

#[derive(Deserialize)]
#[serde(rename_all = "camelCase")]
struct DownloadRequest {
    url: String,
    output_dir: String,
    height: String,
}

fn bundled_tool(app: &AppHandle, name: &str) -> PathBuf {
    let executable = if cfg!(target_os = "windows") {
        format!("{name}.exe")
    } else {
        name.to_owned()
    };

    app.path()
        .resource_dir()
        .ok()
        .map(|directory| directory.join("bin").join(&executable))
        .filter(|path| path.exists())
        .unwrap_or_else(|| PathBuf::from(executable))
}

fn engine_command(app: &AppHandle) -> Result<Command, String> {
    let bundled = bundled_tool(app, "easyclip-engine");
    if bundled.exists() {
        return Ok(Command::new(bundled));
    }

    // Development fallback. Production bundles the PyInstaller executable.
    let script = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join("..")
        .join("engine")
        .join("easyclip_engine.py");
    if script.is_file() {
        let mut command = Command::new("python");
        command.arg(script);
        return Ok(command);
    }
    Err("EasyClip local engine is not installed".to_owned())
}

fn parse_engine_output(output: std::process::Output) -> Result<serde_json::Value, String> {
    let stdout = String::from_utf8_lossy(&output.stdout);
    let value: serde_json::Value = stdout
        .lines()
        .rev()
        .find(|line| !line.trim().is_empty())
        .ok_or_else(|| format!("The local engine returned no result: {}", String::from_utf8_lossy(&output.stderr)))?
        .parse()
        .map_err(|error| format!("Invalid local engine response ({error}): {stdout}"))?;
    if !output.status.success() || value.get("ok").and_then(|item| item.as_bool()) != Some(true) {
        return Err(value.get("error").and_then(|item| item.as_str()).unwrap_or("Local engine failed").to_owned());
    }
    Ok(value)
}

fn command_available(executable: &Path) -> bool {
    Command::new(executable)
        .arg("-version")
        .stdout(Stdio::null())
        .stderr(Stdio::null())
        .status()
        .is_ok_and(|status| status.success())
}

fn nvidia_gpu() -> Option<String> {
    Command::new("nvidia-smi")
        .args(["--query-gpu=name", "--format=csv,noheader"])
        .output()
        .ok()
        .filter(|result| result.status.success())
        .and_then(|result| String::from_utf8(result.stdout).ok())
        .and_then(|output| output.lines().next().map(str::trim).map(str::to_owned))
        .filter(|name| !name.is_empty())
}

#[tauri::command]
fn system_profile(app: AppHandle) -> SystemProfile {
    let gpu_name = nvidia_gpu();
    SystemProfile {
        os: std::env::consts::OS.to_owned(),
        arch: std::env::consts::ARCH.to_owned(),
        nvidia_available: gpu_name.is_some(),
        gpu_name,
        ffmpeg_available: command_available(&bundled_tool(&app, "ffmpeg")),
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

    let metadata = file_path
        .metadata()
        .map_err(|error| format!("Unable to read video: {error}"))?;
    if !metadata.is_file() {
        return Err("Selected path is not a file".to_owned());
    }

    let output = Command::new(bundled_tool(&app, "ffprobe"))
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
        return Err(String::from_utf8_lossy(&output.stderr).trim().to_owned());
    }

    let probe: serde_json::Value = serde_json::from_slice(&output.stdout)
        .map_err(|error| format!("Invalid FFprobe response: {error}"))?;
    let stream = probe["streams"]
        .as_array()
        .and_then(|items| items.first())
        .ok_or_else(|| "No video stream was found".to_owned())?;
    let duration_seconds = probe["format"]["duration"]
        .as_str()
        .and_then(|value| value.parse().ok())
        .unwrap_or_default();

    Ok(VideoFile {
        name: file_path
            .file_name()
            .and_then(|value| value.to_str())
            .unwrap_or("video")
            .to_owned(),
        path,
        size_bytes: metadata.len(),
        extension,
        duration_seconds,
        width: stream["width"].as_u64().unwrap_or_default() as u32,
        height: stream["height"].as_u64().unwrap_or_default() as u32,
        codec: stream["codec_name"].as_str().unwrap_or("unknown").to_owned(),
    })
}

fn escaped_subtitle_path(path: &str) -> String {
    path.replace('\\', "/")
        .replace(':', "\\:")
        .replace('\'', "\\'")
}

#[tauri::command]
async fn render_vertical_clip(app: AppHandle, request: RenderRequest) -> Result<RenderResult, String> {
    if request.start_seconds < 0.0 || request.end_seconds <= request.start_seconds {
        return Err("Invalid clip time range".to_owned());
    }
    if request.end_seconds - request.start_seconds > 180.0 {
        return Err("A clip cannot be longer than 180 seconds".to_owned());
    }
    if !Path::new(&request.input_path).is_file() {
        return Err("Input video does not exist".to_owned());
    }
    if let Some(parent) = Path::new(&request.output_path).parent() {
        std::fs::create_dir_all(parent).map_err(|error| format!("Cannot create output folder: {error}"))?;
    }

    let nvidia_encoder_available = request.use_nvidia && nvidia_gpu().is_some();
    let mut filter = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920".to_owned();
    if let Some(caption) = request.caption_path.as_deref().filter(|path| Path::new(path).is_file()) {
        filter.push_str(&format!(",subtitles='{}':force_style='FontName=Segoe UI,FontSize=18,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=3,Shadow=0,Alignment=2,MarginV=120'", escaped_subtitle_path(caption)));
    }

    let executable = bundled_tool(&app, "ffmpeg");
    let input = request.input_path.clone();
    let output_path = request.output_path.clone();
    let start = format!("{:.3}", request.start_seconds);
    let duration = format!("{:.3}", request.end_seconds - request.start_seconds);
    let output_for_command = output_path.clone();

    let result = tauri::async_runtime::spawn_blocking(move || {
        let mut command = Command::new(executable);
        command.args(["-hide_banner", "-y", "-ss", &start, "-i", &input, "-t", &duration, "-vf", &filter]);
        if nvidia_encoder_available {
            command.args(["-c:v", "h264_nvenc", "-preset", "p5", "-cq", "21"]);
        } else {
            command.args(["-c:v", "libx264", "-preset", "medium", "-crf", "21"]);
        }
        command.args(["-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", &output_for_command]);
        command.output()
    })
    .await
    .map_err(|error| format!("Render task failed: {error}"))?
    .map_err(|error| format!("Cannot start FFmpeg: {error}"))?;

    if !result.status.success() {
        return Err(format!("FFmpeg failed: {}", String::from_utf8_lossy(&result.stderr).trim()));
    }

    Ok(RenderResult {
        output_path,
        used_nvidia: nvidia_encoder_available,
        duration_seconds: request.end_seconds - request.start_seconds,
    })
}

#[tauri::command]
async fn download_video(app: AppHandle, request: DownloadRequest) -> Result<serde_json::Value, String> {
    if !request.url.starts_with("https://") && !request.url.starts_with("http://") {
        return Err("Enter a valid http/https video URL".to_owned());
    }
    std::fs::create_dir_all(&request.output_dir)
        .map_err(|error| format!("Cannot create download folder: {error}"))?;
    let mut command = engine_command(&app)?;
    command.args([
        "download", "--url", &request.url, "--output-dir", &request.output_dir,
        "--height", &request.height,
    ]);
    let result = tauri::async_runtime::spawn_blocking(move || command.output())
        .await
        .map_err(|error| format!("Download task failed: {error}"))?
        .map_err(|error| format!("Cannot start local engine: {error}"))?;
    parse_engine_output(result)
}

#[tauri::command]
async fn analyze_video(app: AppHandle, request: AnalyzeRequest) -> Result<serde_json::Value, String> {
    if !Path::new(&request.input_path).is_file() {
        return Err("Input video does not exist".to_owned());
    }
    if !(15..=180).contains(&request.target_duration) || !(1..=30).contains(&request.clip_count) {
        return Err("Invalid highlight settings".to_owned());
    }
    std::fs::create_dir_all(&request.output_dir)
        .map_err(|error| format!("Cannot create analysis folder: {error}"))?;
    let mut command = engine_command(&app)?;
    command.args([
        "analyze", "--input", &request.input_path, "--output-dir", &request.output_dir,
        "--model", &request.model, "--language", &request.language,
        "--target-duration", &request.target_duration.to_string(),
        "--clip-count", &request.clip_count.to_string(),
    ]);
    let result = tauri::async_runtime::spawn_blocking(move || command.output())
        .await
        .map_err(|error| format!("Analysis task failed: {error}"))?
        .map_err(|error| format!("Cannot start local engine: {error}"))?;
    parse_engine_output(result)
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_dialog::init())
        .invoke_handler(tauri::generate_handler![
            system_profile,
            inspect_video,
            render_vertical_clip,
            download_video,
            analyze_video
        ])
        .run(tauri::generate_context!())
        .expect("error while running EasyClip Desktop");
}
