# EasyClip Desktop

A Windows-first desktop application that turns long local or online videos into
captioned vertical highlights. The interface is React + Tauri; the local media
engine is Python, Faster-Whisper, yt-dlp, and FFmpeg.

## Current features

- Persian/English RTL/LTR interface
- Import MP4, MOV, MKV, WebM, AVI, and M4V files
- Download a public YouTube, TikTok, or Instagram URL through yt-dlp
- Fully local Faster-Whisper transcription with word timestamps
- Local sliding-window highlight ranking (no cloud AI/API key)
- Suggested clips with score, title, time range, and generated SRT captions
- Review or manually adjust clip times and captions
- Export 1080×1920 H.264/AAC MP4 with FFmpeg
- NVIDIA NVENC rendering when an NVIDIA GPU is available, with CPU fallback
- Windows NSIS installer and portable ZIP builds

The first analysis downloads the selected `small` Whisper model into the user's
model cache. After that model and the source video are present, analysis and
rendering work offline. URL import naturally requires internet access.

## Open-source foundation

This application combines adapted parts of two MIT-licensed projects:

- [opensource-clipping](https://github.com/NaufalRizqullah/opensource-clipping):
  source download/format selection and Faster-Whisper transcription flow.
- [ai-highlight-clip](https://github.com/toki-plus/ai-highlight-clip): overlapping
  candidate windows and timestamp-aware subtitle grouping.

See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for copyright and license
notices. EasyClip's combined engine is in `engine/easyclip_engine.py`.

## Development

```bash
npm install
npm run build
python -m unittest discover -s engine -p "test_*.py"
```

Native development additionally requires Rust, Tauri prerequisites, Python
3.11 with `engine/requirements.txt`, and FFmpeg/FFprobe on `PATH`:

```bash
npm run tauri dev
```

## Windows builds

The `EasyClip Windows` GitHub Actions workflow:

1. packages the Python engine with PyInstaller;
2. downloads an FFmpeg essentials build;
3. builds an unsigned NSIS `Setup.exe`;
4. creates `EasyClip-Windows-x64-Portable.zip`; and
5. uploads both as a workflow artifact.

Development builds are unsigned, so Windows SmartScreen may warn until a
code-signing certificate is configured. API keys, models, downloaded videos,
and generated installers must not be committed.
