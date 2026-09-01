# 🪐 Jcode Desktop — COSMIC ODYSSEY

A pro-max **Windows desktop shell** for the [jcode](https://github.com/1jehuang/jcode) AI coding
agent — the real jcode TUI runs inside a beautiful cosmic cockpit: a WebGL star field, black hole,
pulsar beams and nebula behind glass panels, with a multi-session sidebar, command palette and
provider logins.

> The UI theme is ported from a "COSMIC ODYSSEY" design reference (purple/cyan neon, glassmorphism,
> magnetic buttons, custom cursor, preloader, noise + vignette).

## What it does

- Runs the **real jcode engine** in a terminal (PTY) inside a frameless, themed window.
- **Multi-session** management (sidebar + titlebar tabs), persisted across restarts.
- **Provider login flows** — Claude, OpenAI, Gemini, Copilot, Azure, OpenRouter, DeepSeek, Kimi,
  Ollama, LM Studio, Fireworks and any OpenAI-compatible endpoint.
- **Command palette** (`Ctrl+K`), keyboard shortcuts, cosmic toggles (black hole / pulsar / nebula /
  star density / intensity), multiple themes, custom cursor, magnetic buttons.
- **Self-downloads & verifies** (SHA256) the jcode engine on first run, or uses a bundled copy.

## Live preview (browser)

```
npm install          # compiles node-pty for Node
npm run preview      # serves http://localhost:4173
```

The preview runs the same UI with a real shell in the terminal pane.

## Run the desktop app (needs the Electron runtime — full internet)

```
npm install
ELECTRON_SKIP_BINARY_DOWNLOAD=0 npx electron-rebuild -f -w node-pty   # rebuild pty for Electron
npm run fetch:jcode                                                    # download jcode binaries
npm start                                                              # launch Electron
```

## Build the Windows installer

On Windows (or CI — see `.github/workflows/build-windows.yml`):

```
npm ci
npm run fetch:jcode
npm run dist:win
```

Produces `dist/Jcode Desktop-Setup-1.0.0.exe` (NSIS, desktop + start-menu shortcuts).

## Structure

```
src/main/      Electron main process (window, pty sessions, jcode engine, IPC)
src/preload/   contextBridge API
src/renderer/  UI (cosmos WebGL, xterm.js, app logic)
scripts/       preview server, jcode fetcher, icon builder
resources/     icons + (downloaded) jcode binaries
```

## Notes

- jcode requires your own provider credentials (API key or subscription OAuth). Use
  *Settings → Providers* to run `jcode login --provider <id>`.
- jcode is MIT licensed (© 1jehuang). This shell is an independent community UI.
