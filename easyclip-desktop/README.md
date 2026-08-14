# EasyClip Desktop

EasyClip Desktop is a Windows-first, local AI video clipping studio built with Tauri, React, and Rust. Version 0.2 generates Persian and English subtitles without uploading media, then burns them into vertical MP4 clips.

## Local caption and render pipeline

1. The bundled FFmpeg 9.0.1 extracts 16 kHz mono PCM audio.
2. The bundled whisper.cpp 1.9.2 CLI transcribes with the multilingual `ggml-base` model.
3. The app writes a UTF-8 SRT file and previews its timed segments.
4. Before export, full-source SRT timestamps are clipped and rebased to the selected clip range.
5. FFmpeg/libass burns captions with the bundled Noto Sans Arabic font, including Persian RTL shaping.
6. FFmpeg exports a 1080×1920 H.264/AAC MP4. NVIDIA NVENC is selected when both a supported GPU and `h264_nvenc` are available; a failed NVENC render automatically retries with libx264 on the CPU.

All processing is local. The Windows Setup includes FFmpeg, FFprobe, whisper.cpp, the multilingual model, the caption font, and their license notices.

## Supported captions

- Explicit Persian (`fa`)
- Explicit English (`en`)
- Whisper automatic language detection
- Generated or manually selected UTF-8 SubRip (`.srt`) files

Selected SRT files are interpreted on the original video's timeline. This lets a single generated subtitle file be reused for any clip range.

## Development

Node.js 18+ is required for the web interface:

```bash
npm install
npm run dev
npm run build
```

A native desktop build additionally requires stable Rust and the Tauri 2 Windows prerequisites:

```bash
npm run tauri -- dev
```

On non-Windows development hosts, the app can use `ffmpeg`, `ffprobe`, and `whisper-cli` from `PATH`; a model must still be available as `models/ggml-base.bin` in the Tauri resource directory.

## Build `Setup.exe` on Windows

The preparation script downloads pinned x64 artifacts, validates each file's size and SHA-256, and stages only generated resources ignored by Git:

```powershell
npm ci
npm run prepare:windows
npm run tauri -- build --bundles nsis --target x86_64-pc-windows-msvc
```

Or run both preparation and packaging:

```powershell
npm run build:windows
```

The unsigned installer is created under:

```text
src-tauri/target/release/bundle/nsis/*-setup.exe
```

When an explicit target is passed (as in CI), it is under:

```text
src-tauri/target/x86_64-pc-windows-msvc/release/bundle/nsis/*-setup.exe
```

`.github/workflows/easyclip-windows.yml` performs the verified download, frontend build, Rust tests, NSIS build, and uploads `EasyClip-Desktop-0.2.0-Setup.exe` plus `SHA256SUMS.txt` as a GitHub Actions artifact. It does not publish a GitHub Release. The development installer is unsigned, so Windows SmartScreen may warn until code signing is configured.

## Dependency provenance

Pinned versions, artifact hashes, source links, and license terms are documented in `src-tauri/resources/licenses/THIRD_PARTY_NOTICES.md`. Runtime binaries, model weights, generated manifests, videos, and installers must not be committed.

## YouTube Autopilot

Connect your own Google account, point EasyClip at a source channel, pick videos, and
let it download, prepare and publish them to **your** channel unattended.

### Google Cloud setup (you must do this once)

The app ships no credentials, so you supply your own OAuth client:

1. Open <https://console.cloud.google.com> and create a project.
2. **APIs & Services → Library** → enable **YouTube Data API v3**.
3. **OAuth consent screen** → *External* → set an app name and support email → add the
   scopes `youtube.upload`, `youtube.readonly`, `userinfo.profile` → add your own Google
   account under **Test users**.
4. **Credentials → Create credentials → OAuth client ID → Desktop app** → copy the
   **Client ID** and **Client secret**.
5. In EasyClip open **YouTube → Autopilot** and paste both values, then **Sign in with
   Google**. The system browser opens; approve access and return to the app.

> **While the OAuth app stays in "Testing", Google expires the refresh token after
> 7 days.** When that happens the app asks you to sign in again. Publish the consent
> screen to remove the limit.

### Daily quota — the real ceiling

A `videos.insert` call costs **1600** of the default **10,000 units/day**, so a fresh
project uploads **about 6 videos per day**. The queue tracks spend, shows how many
uploads remain, and pauses instead of failing when the budget is gone. The quota resets
at midnight US Pacific. Request more via the quota form in Google Cloud if you need it.

### How it works

1. Paste a video, channel, `@handle` or playlist link.
2. The uploads playlist is paged with `playlistItems.list` (1 unit per 50 videos) rather
   than `search.list` (100 units and truncated results).
3. Tick the videos you want, or **Select all**.
4. Each job downloads with the bundled `yt-dlp`, then uploads with Google's **resumable**
   protocol in 8 MiB chunks. An interrupted upload resumes from the exact byte Google
   stored rather than restarting.
5. A `UNIQUE(source_video_id)` constraint in the local SQLite database means a video can
   never be queued or uploaded twice, even across restarts.

Sign-in is the OAuth **loopback + PKCE** flow for native apps, opened in your real
browser. The refresh token is stored in **Windows Credential Manager**, never on disk in
plaintext and never in the repository.

### Copyright — read this before using a channel that is not yours

Re-uploading someone else's videos without permission causes **copyright strikes**.
**Three strikes in 90 days permanently deletes your channel** and every video on it.
Bulk re-uploading is also caught by YouTube's *reused content* and *spam* policies, and
downloading other people's videos breaks YouTube's Terms of Service.

The app therefore:

- blocks queueing from a channel that is not yours until you tick an explicit
  *"I own this content or have written permission"* confirmation (stored with a timestamp);
- badges **Creative Commons** videos green and standard-licence videos amber;
- defaults every upload to **Private**;
- adds `Original: https://youtu.be/<id>` attribution to the description;
- hides the warning entirely when the source is your own channel.

Use **Dry run** to exercise the whole pipeline without uploading anything.

### Commands and events

| Command | Purpose |
|---|---|
| `autopilot_status` | Connection, quota, queue and `yt-dlp` availability |
| `autopilot_save_credentials` | Store the Google Client ID/secret |
| `autopilot_connect` / `autopilot_disconnect` | Sign in / clear the keychain entry |
| `autopilot_load_source` | Resolve a link and list the channel's videos |
| `autopilot_acknowledge` | Record the copyright confirmation |
| `autopilot_enqueue` | Add selected videos to the queue |
| `autopilot_run_job` | Download + upload one job |
| `autopilot_set_paused` / `autopilot_remove_job` | Queue control |
| `autopilot_self_test` | Verify `yt-dlp`, FFmpeg, keychain and database |

The `autopilot-progress` event carries `{ jobId, state, progress, message }`.
