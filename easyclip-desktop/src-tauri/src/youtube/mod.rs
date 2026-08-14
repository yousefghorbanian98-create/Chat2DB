//! YouTube Autopilot: connect a Google account, read a source channel, and
//! re-publish selected videos to the signed-in user's own channel.

pub mod api;
pub mod auth;
pub mod download;
pub mod parse;
pub mod queue;
pub mod store;
pub mod upload;

use serde::{Deserialize, Serialize};
use std::{
    io::{BufRead, BufReader, Read, Seek, SeekFrom},
    path::PathBuf,
    sync::Mutex,
    time::Duration,
};
use tauri::{AppHandle, Emitter, Manager, State};

use api::{ChannelInfo, SourceVideo};
use queue::{Job, JobState};
use upload::{Privacy, UploadMetadata, DEFAULT_DAILY_QUOTA, UPLOAD_QUOTA_COST};

const SETTING_CLIENT_ID: &str = "google_client_id";
const SETTING_CLIENT_SECRET: &str = "google_client_secret";

/// Shared, lazily-initialised state for the feature.
#[derive(Default)]
pub struct YoutubeState {
    inner: Mutex<Option<Runtime>>,
}

struct Runtime {
    connection: rusqlite::Connection,
    access_token: Option<String>,
    my_channel: Option<ChannelInfo>,
    paused: bool,
}

impl YoutubeState {
    fn with<T>(
        &self,
        app: &AppHandle,
        action: impl FnOnce(&mut Runtime) -> Result<T, String>,
    ) -> Result<T, String> {
        let mut guard = self
            .inner
            .lock()
            .map_err(|_| "Internal state was poisoned".to_owned())?;
        if guard.is_none() {
            let path = database_path(app)?;
            let connection = store::open(&path)?;
            let _ = store::recover_in_flight(&connection, &now_iso());
            *guard = Some(Runtime {
                connection,
                access_token: None,
                my_channel: None,
                paused: false,
            });
        }
        action(guard.as_mut().expect("runtime initialised above"))
    }
}

fn database_path(app: &AppHandle) -> Result<PathBuf, String> {
    let directory = app
        .path()
        .app_data_dir()
        .map_err(|error| format!("Cannot locate the app data directory: {error}"))?;
    Ok(directory.join("easyclip.db"))
}

fn work_directory(app: &AppHandle) -> Result<PathBuf, String> {
    let directory = app
        .path()
        .app_data_dir()
        .map_err(|error| format!("Cannot locate the app data directory: {error}"))?
        .join("autopilot");
    std::fs::create_dir_all(&directory)
        .map_err(|error| format!("Cannot create the work directory: {error}"))?;
    Ok(directory)
}

fn now_iso() -> String {
    chrono::Utc::now().to_rfc3339()
}

/// Quota resets at midnight US Pacific, so bucket usage by that day.
fn quota_day() -> String {
    let pacific = chrono::Utc::now() - chrono::Duration::hours(8);
    pacific.format("%Y-%m-%d").to_string()
}

fn new_id() -> String {
    format!(
        "job-{}-{}",
        chrono::Utc::now().timestamp_millis(),
        &auth::generate_state()[..8]
    )
}

// ------------------------------------------------------------------ events --

#[derive(Clone, Serialize)]
#[serde(rename_all = "camelCase")]
struct JobProgress {
    job_id: String,
    state: String,
    progress: u8,
    message: Option<String>,
}

fn emit_job(app: &AppHandle, job_id: &str, state: JobState, progress: u8, message: Option<String>) {
    let _ = app.emit(
        "autopilot-progress",
        JobProgress {
            job_id: job_id.to_owned(),
            state: state.as_str().to_owned(),
            progress,
            message,
        },
    );
}

// ---------------------------------------------------------------- commands --

#[derive(Serialize)]
#[serde(rename_all = "camelCase")]
pub struct AutopilotStatus {
    pub configured: bool,
    pub connected: bool,
    pub channel: Option<ChannelInfo>,
    pub uploads_remaining: u32,
    pub quota_spent: u32,
    pub daily_quota: u32,
    pub paused: bool,
    pub jobs: Vec<Job>,
    pub yt_dlp_available: bool,
}

#[tauri::command]
pub fn autopilot_status(
    app: AppHandle,
    state: State<'_, YoutubeState>,
) -> Result<AutopilotStatus, String> {
    let yt_dlp_available = crate::bundled_tool_path(&app, "yt-dlp").exists();
    state.with(&app, |runtime| {
        let spent = store::quota_spent(&runtime.connection, &quota_day());
        Ok(AutopilotStatus {
            configured: store::get_setting(&runtime.connection, SETTING_CLIENT_ID).is_some()
                && store::get_setting(&runtime.connection, SETTING_CLIENT_SECRET).is_some(),
            connected: runtime.my_channel.is_some() || store::load_refresh_token().is_some(),
            channel: runtime.my_channel.clone(),
            uploads_remaining: upload::uploads_remaining(spent, DEFAULT_DAILY_QUOTA),
            quota_spent: spent,
            daily_quota: DEFAULT_DAILY_QUOTA,
            paused: runtime.paused,
            jobs: store::list_jobs(&runtime.connection)?,
            yt_dlp_available,
        })
    })
}

#[tauri::command]
pub fn autopilot_save_credentials(
    app: AppHandle,
    state: State<'_, YoutubeState>,
    client_id: String,
    client_secret: String,
) -> Result<(), String> {
    let client_id = client_id.trim().to_owned();
    let client_secret = client_secret.trim().to_owned();
    if client_id.is_empty() || client_secret.is_empty() {
        return Err("Enter both the Client ID and the Client secret".to_owned());
    }
    if !client_id.ends_with(".apps.googleusercontent.com") {
        return Err(
            "That does not look like a Google OAuth Client ID (it should end with \
             .apps.googleusercontent.com)"
                .to_owned(),
        );
    }
    state.with(&app, |runtime| {
        store::set_setting(&runtime.connection, SETTING_CLIENT_ID, &client_id)?;
        store::set_setting(&runtime.connection, SETTING_CLIENT_SECRET, &client_secret)
    })
}

fn credentials(runtime: &Runtime) -> Result<(String, String), String> {
    let id = store::get_setting(&runtime.connection, SETTING_CLIENT_ID)
        .ok_or_else(|| "Add your Google OAuth credentials first".to_owned())?;
    let secret = store::get_setting(&runtime.connection, SETTING_CLIENT_SECRET)
        .ok_or_else(|| "Add your Google OAuth credentials first".to_owned())?;
    Ok((id, secret))
}

#[tauri::command]
pub async fn autopilot_connect(
    app: AppHandle,
    state: State<'_, YoutubeState>,
) -> Result<ChannelInfo, String> {
    let (client_id, client_secret) = state.with(&app, credentials)?;

    let server = auth::LoopbackServer::bind()?;
    let redirect_uri = server.redirect_uri();
    let pkce = auth::Pkce::generate();
    let csrf = auth::generate_state();
    let url = auth::build_auth_url(&client_id, &redirect_uri, &pkce.challenge, &csrf);

    tauri_plugin_opener::open_url(&url, None::<&str>)
        .map_err(|error| format!("Cannot open the browser for sign-in: {error}"))?;

    // Blocking listener, moved off the async runtime.
    let code = tauri::async_runtime::spawn_blocking(move || {
        server.wait_for_code(&csrf, Duration::from_secs(300))
    })
    .await
    .map_err(|error| format!("Sign-in task failed: {error}"))??;

    let client = api::http_client()?;
    let tokens = api::exchange_code(
        &client,
        &client_id,
        &client_secret,
        &code,
        &pkce.verifier,
        &redirect_uri,
    )
    .await?;

    if let Some(refresh) = tokens.refresh_token.as_deref() {
        store::save_refresh_token(refresh)?;
    }
    let channel = api::my_channel(&client, &tokens.access_token).await?;

    state.with(&app, |runtime| {
        runtime.access_token = Some(tokens.access_token.clone());
        runtime.my_channel = Some(channel.clone());
        Ok(())
    })?;
    Ok(channel)
}

#[tauri::command]
pub fn autopilot_disconnect(app: AppHandle, state: State<'_, YoutubeState>) -> Result<(), String> {
    store::delete_refresh_token()?;
    state.with(&app, |runtime| {
        runtime.access_token = None;
        runtime.my_channel = None;
        Ok(())
    })
}

/// Return a usable access token, refreshing via the keychain when needed.
async fn access_token(app: &AppHandle, state: &State<'_, YoutubeState>) -> Result<String, String> {
    if let Some(token) = state.with(app, |runtime| Ok(runtime.access_token.clone()))? {
        return Ok(token);
    }
    let (client_id, client_secret) = state.with(app, credentials)?;
    let refresh = store::load_refresh_token()
        .ok_or_else(|| "Connect your Google account first".to_owned())?;
    let client = api::http_client()?;
    let tokens = api::refresh_access_token(&client, &client_id, &client_secret, &refresh).await?;
    let channel = api::my_channel(&client, &tokens.access_token).await?;
    state.with(app, |runtime| {
        runtime.access_token = Some(tokens.access_token.clone());
        runtime.my_channel = Some(channel);
        Ok(())
    })?;
    Ok(tokens.access_token)
}

#[derive(Serialize)]
#[serde(rename_all = "camelCase")]
pub struct SourceListing {
    pub channel: ChannelInfo,
    pub videos: Vec<SourceVideo>,
    /// True when the source is the signed-in user's own channel (no warning).
    pub is_own_channel: bool,
    pub acknowledged: bool,
}

#[tauri::command]
pub async fn autopilot_load_source(
    app: AppHandle,
    state: State<'_, YoutubeState>,
    link: String,
    max_videos: usize,
) -> Result<SourceListing, String> {
    let source = parse::parse_source(&link)?;
    let token = access_token(&app, &state).await?;
    let client = api::http_client()?;
    let channel = api::resolve_channel(&client, &token, &source).await?;
    let videos = api::channel_videos(&client, &token, &channel, max_videos.clamp(1, 500)).await?;

    let (mine, acknowledged) = state.with(&app, |runtime| {
        Ok((
            runtime
                .my_channel
                .as_ref()
                .map(|c| c.id == channel.id)
                .unwrap_or(false),
            store::is_acknowledged(&runtime.connection, &channel.id),
        ))
    })?;

    Ok(SourceListing {
        channel,
        videos,
        is_own_channel: mine,
        acknowledged,
    })
}

#[tauri::command]
pub fn autopilot_acknowledge(
    app: AppHandle,
    state: State<'_, YoutubeState>,
    channel_id: String,
) -> Result<(), String> {
    state.with(&app, |runtime| {
        store::acknowledge_channel(&runtime.connection, &channel_id, &now_iso())
    })
}

#[derive(Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct EnqueueRequest {
    pub channel_id: String,
    pub videos: Vec<SourceVideo>,
}

#[tauri::command]
pub fn autopilot_enqueue(
    app: AppHandle,
    state: State<'_, YoutubeState>,
    request: EnqueueRequest,
) -> Result<usize, String> {
    state.with(&app, |runtime| {
        if !store::is_acknowledged(&runtime.connection, &request.channel_id) {
            let own = runtime
                .my_channel
                .as_ref()
                .map(|c| c.id == request.channel_id)
                .unwrap_or(false);
            if !own {
                return Err(
                    "Confirm you own this content or have permission before queueing".to_owned(),
                );
            }
        }
        let now = now_iso();
        let mut added = 0usize;
        for video in &request.videos {
            if store::insert_job(
                &runtime.connection,
                &new_id(),
                &video.id,
                &request.channel_id,
                &video.title,
                &now,
            )? {
                added += 1;
            }
        }
        Ok(added)
    })
}

#[tauri::command]
pub fn autopilot_set_paused(
    app: AppHandle,
    state: State<'_, YoutubeState>,
    paused: bool,
) -> Result<(), String> {
    state.with(&app, |runtime| {
        runtime.paused = paused;
        Ok(())
    })
}

#[tauri::command]
pub fn autopilot_remove_job(
    app: AppHandle,
    state: State<'_, YoutubeState>,
    job_id: String,
) -> Result<(), String> {
    state.with(&app, |runtime| {
        store::remove_job(&runtime.connection, &job_id)
    })
}

#[derive(Serialize)]
#[serde(rename_all = "camelCase")]
pub struct SelfTest {
    pub yt_dlp: bool,
    pub ffmpeg: bool,
    pub keychain: bool,
    pub database: bool,
    pub details: Vec<String>,
}

#[tauri::command]
pub fn autopilot_self_test(app: AppHandle, state: State<'_, YoutubeState>) -> SelfTest {
    let mut details = Vec::new();

    let yt_dlp_path = crate::bundled_tool_path(&app, "yt-dlp");
    let yt_dlp = yt_dlp_path.exists();
    details.push(if yt_dlp {
        format!("yt-dlp found at {}", yt_dlp_path.display())
    } else {
        "yt-dlp is missing — reinstall EasyClip Desktop".to_owned()
    });

    let ffmpeg_path = crate::bundled_tool_path(&app, "ffmpeg");
    let ffmpeg = ffmpeg_path.exists();
    details.push(if ffmpeg {
        "FFmpeg found".to_owned()
    } else {
        "FFmpeg is missing".to_owned()
    });

    let keychain = match store::save_refresh_token("__easyclip_probe__") {
        Ok(()) => {
            let readable = store::load_refresh_token().is_some();
            let _ = store::delete_refresh_token();
            details.push("Windows Credential Manager is writable".to_owned());
            readable
        }
        Err(error) => {
            details.push(format!("Credential store unavailable: {error}"));
            false
        }
    };

    let database = state
        .with(&app, |runtime| store::list_jobs(&runtime.connection))
        .is_ok();
    details.push(if database {
        "Local database is readable".to_owned()
    } else {
        "Local database could not be opened".to_owned()
    });

    SelfTest {
        yt_dlp,
        ffmpeg,
        keychain,
        database,
        details,
    }
}

// ------------------------------------------------------------- the pipeline --

#[derive(Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct RunOptions {
    pub privacy: Privacy,
    pub title_template: String,
    pub description_template: String,
    pub tags: Vec<String>,
    pub category_id: String,
    pub dry_run: bool,
    pub rate_limit: Option<String>,
}

/// Process a single queued job end to end.
#[tauri::command]
pub async fn autopilot_run_job(
    app: AppHandle,
    state: State<'_, YoutubeState>,
    job_id: String,
    options: RunOptions,
) -> Result<String, String> {
    let jobs = state.with(&app, |runtime| store::list_jobs(&runtime.connection))?;
    let job = jobs
        .into_iter()
        .find(|candidate| candidate.id == job_id)
        .ok_or_else(|| "That job is no longer in the queue".to_owned())?;

    let spent = state.with(&app, |runtime| {
        Ok(store::quota_spent(&runtime.connection, &quota_day()))
    })?;
    if upload::uploads_remaining(spent, DEFAULT_DAILY_QUOTA) == 0 && !options.dry_run {
        return Err(
            "Daily upload quota is exhausted (about 6 uploads per day). The queue will \
             resume tomorrow."
                .to_owned(),
        );
    }

    let outcome = run_job_inner(&app, &state, &job, &options).await;
    let now = now_iso();
    match &outcome {
        Ok(video_id) => {
            state.with(&app, |runtime| {
                if options.dry_run {
                    store::update_job_state(&runtime.connection, &job.id, JobState::Skipped, None, &now)
                } else {
                    store::add_quota(&runtime.connection, &quota_day(), UPLOAD_QUOTA_COST)?;
                    store::set_job_target(&runtime.connection, &job.id, video_id, &now)
                }
            })?;
            emit_job(&app, &job.id, JobState::Done, 100, None);
        }
        Err(error) => {
            state.with(&app, |runtime| {
                store::increment_attempts(&runtime.connection, &job.id)?;
                store::update_job_state(
                    &runtime.connection,
                    &job.id,
                    JobState::Failed,
                    Some(error),
                    &now,
                )
            })?;
            emit_job(&app, &job.id, JobState::Failed, 0, Some(error.clone()));
        }
    }
    outcome
}

async fn run_job_inner(
    app: &AppHandle,
    state: &State<'_, YoutubeState>,
    job: &Job,
    options: &RunOptions,
) -> Result<String, String> {
    let now = now_iso();
    state.with(app, |runtime| {
        store::update_job_state(&runtime.connection, &job.id, JobState::Downloading, None, &now)
    })?;
    emit_job(app, &job.id, JobState::Downloading, 0, None);

    let workspace = work_directory(app)?;
    let target = workspace.join(format!("{}.mp4", job.source_video_id));
    let template = workspace
        .join(format!("{}.%(ext)s", job.source_video_id))
        .to_string_lossy()
        .into_owned();

    let yt_dlp = crate::bundled_tool_path(app, "yt-dlp");
    if !yt_dlp.exists() {
        return Err("yt-dlp is missing. Reinstall EasyClip Desktop.".to_owned());
    }

    let args = download::download_args(
        &job.source_video_id,
        &template,
        options.rate_limit.as_deref(),
    );
    let app_for_download = app.clone();
    let job_id = job.id.clone();
    let downloaded = tauri::async_runtime::spawn_blocking(move || -> Result<(), String> {
        let mut child = crate::media_command_public(&yt_dlp)
            .args(&args)
            .stdout(std::process::Stdio::piped())
            .stderr(std::process::Stdio::piped())
            .spawn()
            .map_err(|error| format!("Cannot start yt-dlp: {error}"))?;

        if let Some(stdout) = child.stdout.take() {
            for line in BufReader::new(stdout).lines().map_while(Result::ok) {
                if let Some(percent) = download::parse_progress_line(&line) {
                    emit_job(
                        &app_for_download,
                        &job_id,
                        JobState::Downloading,
                        percent.round() as u8,
                        None,
                    );
                }
            }
        }
        let output = child
            .wait_with_output()
            .map_err(|error| format!("yt-dlp did not finish: {error}"))?;
        if !output.status.success() {
            return Err(download::describe_download_error(
                &String::from_utf8_lossy(&output.stderr),
            ));
        }
        Ok(())
    })
    .await
    .map_err(|error| format!("Download task failed: {error}"))?;
    downloaded?;

    if !target.is_file() {
        return Err("yt-dlp finished but produced no MP4 file".to_owned());
    }

    let context = parse::TemplateContext {
        title: &job.title,
        channel: &job.source_channel_id,
        video_id: &job.source_video_id,
        index: 1,
        date: &now[..10.min(now.len())],
    };
    let metadata = UploadMetadata {
        title: parse::apply_template(&options.title_template, &context),
        description: parse::apply_template(&options.description_template, &context),
        tags: options.tags.clone(),
        category_id: options.category_id.clone(),
        privacy: options.privacy,
        publish_at: None,
    };

    if options.dry_run {
        emit_job(app, &job.id, JobState::Skipped, 100, Some("Dry run".into()));
        return Ok(String::new());
    }

    let now = now_iso();
    state.with(app, |runtime| {
        store::update_job_state(&runtime.connection, &job.id, JobState::Uploading, None, &now)
    })?;
    emit_job(app, &job.id, JobState::Uploading, 0, None);

    let token = access_token(app, state).await?;
    upload_file(app, &job.id, &token, &target, &metadata).await
}

/// Resumable upload of a local file. Returns the new video id.
async fn upload_file(
    app: &AppHandle,
    job_id: &str,
    access_token: &str,
    path: &std::path::Path,
    metadata: &UploadMetadata,
) -> Result<String, String> {
    let client = api::http_client()?;
    let total = path
        .metadata()
        .map_err(|error| format!("Cannot read the downloaded file: {error}"))?
        .len();

    let session = client
        .post(upload::RESUMABLE_ENDPOINT)
        .bearer_auth(access_token)
        .header("X-Upload-Content-Length", total.to_string())
        .header("X-Upload-Content-Type", "video/*")
        .json(&metadata.to_body())
        .send()
        .await
        .map_err(|error| format!("Cannot start the upload: {error}"))?;

    if !session.status().is_success() {
        let status = session.status().as_u16();
        let body = session.text().await.unwrap_or_default();
        return Err(api::describe_google_error(&body, status));
    }
    let session_uri = session
        .headers()
        .get("location")
        .and_then(|value| value.to_str().ok())
        .ok_or_else(|| "Google did not return an upload session".to_owned())?
        .to_owned();

    let mut file =
        std::fs::File::open(path).map_err(|error| format!("Cannot open the video: {error}"))?;
    let mut offset = 0u64;
    let mut attempt = 0u32;

    while offset < total {
        let length = upload::next_chunk_length(offset, total);
        let mut buffer = vec![0u8; length as usize];
        file.seek(SeekFrom::Start(offset))
            .map_err(|error| format!("Cannot seek the video: {error}"))?;
        file.read_exact(&mut buffer)
            .map_err(|error| format!("Cannot read the video: {error}"))?;

        let response = client
            .put(&session_uri)
            .header("Content-Length", length.to_string())
            .header("Content-Range", upload::content_range(offset, length, total))
            .body(buffer)
            .send()
            .await;

        let response = match response {
            Ok(response) => response,
            Err(_) if attempt < 5 => {
                // Network dropped: ask Google how much it actually stored.
                tokio::time::sleep(Duration::from_millis(upload::backoff_millis(attempt))).await;
                attempt += 1;
                offset = probe_offset(&client, &session_uri, total).await.unwrap_or(offset);
                continue;
            }
            Err(error) => return Err(format!("Upload failed: {error}")),
        };

        let status = response.status().as_u16();
        if upload::is_incomplete(status) {
            let stored = response
                .headers()
                .get("range")
                .and_then(|value| value.to_str().ok());
            offset = upload::resume_offset(stored).max(offset + length);
            attempt = 0;
            emit_job(
                app,
                job_id,
                JobState::Uploading,
                upload::progress_percent(offset, total),
                None,
            );
            continue;
        }

        if status == 200 || status == 201 {
            let body = response.text().await.unwrap_or_default();
            let value: serde_json::Value = serde_json::from_str(&body).unwrap_or_default();
            return value["id"]
                .as_str()
                .map(str::to_owned)
                .ok_or_else(|| "Upload finished but Google did not return a video id".to_owned());
        }

        if upload::is_retryable(status) && attempt < 5 {
            tokio::time::sleep(Duration::from_millis(upload::backoff_millis(attempt))).await;
            attempt += 1;
            offset = probe_offset(&client, &session_uri, total).await.unwrap_or(offset);
            continue;
        }

        let body = response.text().await.unwrap_or_default();
        return Err(api::describe_google_error(&body, status));
    }

    Err("The upload ended without a confirmation from Google".to_owned())
}

async fn probe_offset(client: &reqwest::Client, session_uri: &str, total: u64) -> Option<u64> {
    let response = client
        .put(session_uri)
        .header("Content-Length", "0")
        .header("Content-Range", upload::probe_range(total))
        .send()
        .await
        .ok()?;
    let stored = response
        .headers()
        .get("range")
        .and_then(|value| value.to_str().ok());
    Some(upload::resume_offset(stored))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn quota_day_is_iso_dated() {
        let day = quota_day();
        assert_eq!(day.len(), 10);
        assert_eq!(day.matches('-').count(), 2);
    }

    #[test]
    fn generated_job_ids_are_unique() {
        assert_ne!(new_id(), new_id());
    }
}
