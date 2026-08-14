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
