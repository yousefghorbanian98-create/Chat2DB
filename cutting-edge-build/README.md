# 🎬 Cutting Edge (CE)

> **Clip smarter, not harder.**

Cutting Edge is an **open-source Windows desktop application** that transforms long-form videos into professional short-form clips for social media — with AI-powered highlight selection, face tracking, cinematic hooks, karaoke captions, B-Roll, voiceover, and auto-upload.

**Current version: 0.2.0**

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🤖 **AI Clip Selection** | Gemini, Claude, OpenAI, or local Ollama pick the best moments |
| 🎯 **Face Tracking** | MediaPipe-powered smart reframing with smooth pan |
| 💬 **Karaoke Captions** | Word-by-word animated ASS subtitles (4+ styles) |
| 🎬 **Cinematic Hooks** | 3-second attention-grabbing intros with glitch effects |
| 🖼️ **B-Roll** | Auto-fetched contextual stock footage (Pexels) |
| 🎙️ **VoiceOver** | AI script + TTS commentary with audio ducking |
| 📱 **Multi-Aspect** | 9:16, 1:1, 4:5, 3:4 outputs |
| 🔄 **Auto-Update** | Update installed app without reinstall (electron-updater) |
| 🔒 **Local-First** | Full offline mode with Ollama + local Whisper |

---

## 🚀 Quick Start (Development)

```bash
# Backend
cd backend
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8742

# Frontend (another terminal)
cd frontend
npm install
npm run dev
# Open http://localhost:5173
```

---

## 🪟 Windows Installer (2 ways)

### Way 1: GitHub Actions (automatic)
Push the code to GitHub → the `Build Windows Installer` workflow builds `Cutting Edge Setup.exe` automatically. Download from Actions → Artifacts (or Releases on `v*` tags).

### Way 2: Local PowerShell script
```powershell
powershell -ExecutionPolicy Bypass -File scripts\build-installer-local.ps1
```
Result: `frontend\release\Cutting Edge Setup.exe`

---

## 🔄 Auto-Update System

1. Tag a new version: `git tag v0.3.0 && git push origin v0.3.0`
2. GitHub Actions builds + publishes the new installer + `latest.yml`
3. Installed app checks for updates on startup (5s) and via Settings → "بررسی آپدیت"
4. Only delta changes are downloaded (2-10 MB), no reinstall needed

---

## 🏗 Architecture

```
Electron Shell (Windows UI)  ←→  FastAPI Backend (:8742)  ←→  Processing Pipeline
                                                                 Ingest → Transcribe → AI Select → Export
```

---

## 📄 License

MIT