# Build Report — 1.0.0

Date: 2026-08-15 (UTC)
Host: Linux x64 sandbox, Node 22.22.3 (development host); Windows Server 2022 x64 (release build host, GitHub Actions)
Target: Windows 10/11 x64
Branch: `arena/01a0044a-chat2db`

## Executive result

The Electron/React application source, strict preload boundary, SQLite migrations, OAuth flow, two-pool upload/download queue, resumable chunked uploads, channel monitoring with fingerprint + backoff + custom cron, Whisper transcription fallback, Ollama integration, FFmpeg render pipeline, tray, routed pages, and Windows packaging configuration are implemented under `youtube-auto-uploader/`.

On this Linux host every static and dynamic check that can run does pass:

```text
npm ci --ignore-scripts   -> exit 0
npm rebuild better-sqlite3 (native binding built against local Node headers) -> exit 0
npm run typecheck         -> exit 0
npm run lint              -> exit 0 (0 errors, 0 warnings)
npm run smoke             -> 16/16 tests pass (includes native SQLite migration test)
npm run build             -> main/preload/renderer bundles emitted
npm audit --omit=dev      -> 0 vulnerabilities
```

The Windows installer itself must be produced by the GitHub Actions workflow `.github/workflows/build-youtube-uploader.yml` (windows-2022 runner). **Dispatching that workflow from this environment is currently blocked**: the Arena GitHub App token returns `HTTP 403: Resource not accessible by integration` for `workflow_dispatch`, run re-runs, and any push that modifies a workflow file (missing `actions: write` / `workflows` permissions). The workflow file is present on this branch and supports manual dispatch — a repository maintainer needs to run it once from the Actions tab with branch `arena/01a0044a-chat2db` selected (or grant the app the `actions`/`workflows` permissions). Once the run succeeds, the sizes and SHA-256 hashes below must be filled in from the run's `SHA256SUMS.txt`.

## Phase A — static correctness

| Check | Result | Evidence |
|---|---|---|
| Dependency resolution | Pass | `npm ci --ignore-scripts` exit 0; lockfile regenerated after dependency cleanup. |
| TypeScript strict | Pass | `npm run typecheck` exit 0. |
| ESLint | Pass | `npm run lint` exit 0, zero warnings. |
| Production build | Pass | `npm run build` exit 0; main, preload, renderer bundles emitted. |
| IPC matching | Pass | Every invoke channel in `electron/preload.ts` has a handler in `electron/ipc/index.ts`; renderer event subscription uses a fixed allow-list. |
| SQL migration | Pass at runtime | `better-sqlite3` was compiled from source against local Node headers; migration test creates all tables including migration 003 (resumable-upload checkpoints, monitor backoff counters). |
| Path handling | Pass | Runtime paths use `path.join`; yt-dlp output uses platform-aware paths. |

## Phase B — smoke tests

`npm run smoke` runs 16 tests, all passing on this host with the compiled native binding:

- database migration creates all tables and settings round-trip (real SQLite, no mocks);
- retry succeeds after two transient failures / stops after configured attempts;
- Ollama unavailable and mock-server model listing;
- upload queue persists and uploads a local file;
- **queue restores interrupted jobs after a restart** (job re-queued from persisted payload and uploaded);
- **download and upload stages run in separate pools with configured concurrency** (peak parallel downloads observed = 2 with `download: 2`);
- **cancel aborts an active job through its AbortSignal** and the row is marked `cancelled`;
- quota tracking blocks when the daily estimate is exhausted;
- cron validation, instant matching, and due-window evaluation;
- whisper.cpp SRT output parsing;
- channel monitor persisted exponential backoff after consecutive failures;
- channel monitor response fingerprint (etag) stored and unchanged listings skipped.

FFmpeg/yt-dlp binary smoke tests (`npm run smoke:binaries`) require the Windows binaries, which cannot be downloaded from this sandbox (the TLS-intercepting proxy resets connections to `www.gyan.dev` and `release-assets.githubusercontent.com`). They run in the Windows workflow after `npm run prebuild:win`.

## Phase C/D — application boot and feature integration

Electron boot, OAuth browser flow, tray behavior, and end-to-end downloads/uploads remain Windows-target checks executed after installing the packaged artifact. Implemented and unit-verified code paths:

- yt-dlp metadata/playlist/captions/download with **AbortSignal-based process termination**;
- two-stage queue (download pool + upload pool) with **settings-driven concurrency** (`downloadConcurrency`, `uploadConcurrency`);
- **application-managed resumable uploads in 10 MB chunks** with the session URI and committed offset checkpointed to SQLite, so an interrupted upload resumes from the last committed chunk after restart;
- channel monitor with per-channel hour interval **or five-field custom cron**, stored response fingerprint to skip unchanged listings, and **persisted per-channel exponential backoff** (2^n minutes, capped at 6 h);
- **local Whisper transcription fallback** for videos without captions: user points Settings → Whisper at a whisper.cpp executable and GGML/GGUF model; nothing is bundled, no network needed;
- clipper pipeline cancellation (kills running yt-dlp/ffmpeg/whisper children);
- graceful shutdown: monitor stopped, queue and clipper aborted, tray destroyed, database closed inside a guarded handler; stale temp directories swept at boot.

## Phase E — packaging

Performed by `.github/workflows/build-youtube-uploader.yml` on windows-2022:

1. `npm ci --ignore-scripts`
2. `npm rebuild better-sqlite3`
3. `npm run typecheck && npm run lint`
4. `npm run smoke`
5. `npm run prebuild:win` (downloads and checksum-verifies ffmpeg.exe/ffprobe.exe/yt-dlp.exe, generates the ambient music loop)
6. `npm run smoke:binaries`
7. `npx electron-builder install-app-deps`
8. `npm run pack:win` (NSIS x64 + Portable)
9. Verifies both executables exist, installer ≤ 250 MB, writes `SHA256SUMS.txt`, uploads artifact `YouTube-Auto-Uploader-1.0.0-Windows-x64`.

### Release run record (to be filled from the successful Actions run)

| Item | Value |
|---|---|
| Workflow run URL | _pending — dispatch requires maintainer (see Executive result)_ |
| `YouTube Auto-Uploader 1.0.0 x64.exe` size / SHA-256 | _pending_ |
| `YouTube Auto-Uploader 1.0.0 Portable.exe` size / SHA-256 | _pending_ |

## Code signing

**The Windows artifacts are NOT code-signed.** No Authenticode certificate is available; the workflow sets `CSC_IDENTITY_AUTO_DISCOVERY: 'false'` to guarantee electron-builder does not attempt discovery. Windows SmartScreen will warn on first run, which is expected for unsigned community builds. Do not describe the output as signed unless a certificate is configured and `Get-AuthenticodeSignature` returns `Valid`.

## Security review

- Renderer: `nodeIntegration:false`, `contextIsolation:true`, sandbox enabled; fixed preload method/event allow-list.
- **No Google client ID, secret, or API key is embedded anywhere in the source.** All OAuth credentials are entered by the user at runtime and stored via keytar (Windows Credential Manager) with OS-encrypted `safeStorage` fallback.
- OAuth callback binds to `127.0.0.1` on an ephemeral port only.
- Ollama defaults to loopback; whisper.cpp runs as a local child process.
- No `eval` or renderer-provided command execution.
- Explicit copyright/responsibility gate before sign-in.

## Dependency audit

Unused runtime dependencies (`node-cron`, `fluent-ffmpeg`, `yt-dlp-exec` and their type packages) were removed. `react-router-dom` was upgraded to 7.18.2 (fixes the open-redirect/SSR advisories) and `uuid` is forced to ≥ 11.1.1 via an override for the googleapis/gaxios chain. Result: **`npm audit --omit=dev` reports 0 vulnerabilities.** The full tree (dev/build tooling: electron-builder-era transitive packages) still carries advisories that do not ship in the packaged app.

## Fonts

The previously bundled DejaVu compatibility files were replaced with the genuine typefaces, both under the SIL Open Font License 1.1 (license texts bundled alongside):

- `Inter-Regular.ttf`, `Inter-Bold.ttf` — Inter v3.19 (name table verified: "Inter Regular"/"Inter Bold"), `OFL-Inter.txt`;
- `Vazirmatn-Regular.ttf` — Vazirmatn v33.003 (name table verified: "Vazirmatn Regular"), `OFL-Vazirmatn.txt`.

## Localization

The i18n dictionary was extended (status labels, common actions, privacy levels) with complete English and Persian coverage; the top bar page titles now translate, and RTL layout rules (`[dir=rtl]` sidebar/topbar mirroring, Vazirmatn font family) apply when Persian is selected. Full-page Persian coverage of every long-form descriptive paragraph remains partial.

## Known remaining limitations

1. Whisper fallback requires the user to supply a whisper.cpp executable and model (deliberately not bundled to keep the installer small and offline-safe); there is no in-app model downloader yet.
2. Batch list inline per-item metadata overrides, failure CSV export, and auto-updater remain unimplemented.
3. Live Google-account OAuth and real YouTube upload E2E cannot run in CI; they remain manual Windows checks.
4. Persian translation covers navigation/status/common actions but not every descriptive sentence.
5. Windows-only runtime checks (tray minimize on close, portable launch, clean install/uninstall on Windows 10/11 VMs, memory soak, real-Ollama E2E) must be performed on the packaged artifact.
6. Artifacts are unsigned (see Code signing).

## Required maintainer step

Open GitHub → Actions → “Build YouTube Auto-Uploader” → Run workflow → select branch `arena/01a0044a-chat2db` → Run. Alternatively grant the Arena GitHub App `actions: write` (and `workflows`) permission so the agent can dispatch and monitor the run itself. After a green run, download artifact `YouTube-Auto-Uploader-1.0.0-Windows-x64` and record the sizes/hashes in the table above.
