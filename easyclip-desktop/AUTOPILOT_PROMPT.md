# Master Prompt — EasyClip Autopilot (YouTube channel → your channel)

> Paste everything below the line into a fresh agent session. It is written to be
> executed in ONE run: build → debug → verify → push to GitHub → produce Setup.exe.

---

## ROLE

You are a senior Rust + TypeScript engineer with deep Tauri 2, OAuth 2.0, and
YouTube Data API v3 experience. You will implement a complete, working feature in an
existing repository, debug it until it actually compiles and passes tests, and push it
to GitHub. Do not stop to ask questions unless you hit a credential you cannot obtain.
Make reasonable decisions and document them. Work autonomously to completion.

## REPOSITORY

- Repo: `https://github.com/yousefghorbanian98-create/Chat2DB`
- Branch to use: `arena/019ffe1e-chat2db` (create your commits here; do NOT touch `main`)
- App lives in the subdirectory: `easyclip-desktop/`
- GitHub CLI (`gh`) and `git` are pre-authenticated.

### Existing stack (do not rewrite it — extend it)

| Layer | Detail |
|---|---|
| Shell | Tauri 2 (Rust), NSIS installer, Windows x64 |
| Frontend | React 19 + TypeScript 5.9 + Vite 7, `lucide-react` icons |
| Rust crate | `easyclip-desktop` at `easyclip-desktop/src-tauri`, lib name `easyclip_desktop_lib` |
| Existing Rust deps | `tauri`, `tauri-plugin-dialog`, `serde`, `serde_json` |
| Existing source | `src-tauri/src/lib.rs` (commands), `src-tauri/src/media.rs` (ffmpeg/whisper), `src/App.tsx` (entire UI, single file) |
| Bundled binaries | `src-tauri/resources/bin/{ffmpeg,ffprobe,whisper-cli}.exe`, model at `src-tauri/resources/models/ggml-base.bin`, font at `src-tauri/resources/fonts/` |
| Prep script | `easyclip-desktop/scripts/prepare-windows-resources.ps1` (downloads + SHA-256 verifies pinned binaries) |
| CI | `.github/workflows/easyclip-windows.yml` — builds the NSIS `Setup.exe` |

The app already does, locally and offline: audio extraction (FFmpeg) → transcription
(whisper.cpp, Persian/English/auto) → SRT generation → burn-in with libass using Noto
Sans Arabic (correct Persian RTL shaping) → 1080x1920 H.264/AAC export with NVENC and
automatic libx264 CPU fallback. The UI is bilingual (Persian/English) with full RTL.

**Reuse all of that.** Your job is the missing automation layer.

## WHAT TO BUILD

Replace the `ComingSoon` placeholder for the `"youtube"` page in `src/App.tsx` with a
real feature. The user's goal, verbatim:

> Log in with my own Google account, select my own YouTube channel. Then I paste a link
> to a video from *some other* channel, and the app pulls that channel's videos — all of
> them, or the ones I tick — and uploads them to MY channel automatically, with no manual
> work from me.

Build exactly this as an **Autopilot pipeline**:

```
source channel URL/video URL
  → resolve channel → list videos → user selects (or "select all" / "auto-watch new")
  → download source video
  → [optional] auto-clip into vertical Shorts using the EXISTING caption+render pipeline
  → upload to the signed-in user's channel via YouTube Data API v3 (resumable)
  → record state so nothing is ever uploaded twice
  → repeat on a schedule, unattended
```

---

## PART 1 — Google OAuth (Rust side, new file `src-tauri/src/youtube/auth.rs`)

Use the **OAuth 2.0 Loopback flow for native apps** — NOT the deprecated OOB flow, and
NOT an embedded webview (Google blocks embedded webviews for sign-in).

1. Start a `tiny_http` listener on `127.0.0.1:0` (random free port); read the actual port.
2. Build the auth URL with **PKCE** (S256 — generate a 43–128 char `code_verifier`, send
   `code_challenge`), plus a random `state` you verify on return.
   - `scope`: `https://www.googleapis.com/auth/youtube.upload https://www.googleapis.com/auth/youtube.readonly https://www.googleapis.com/auth/userinfo.profile`
   - `access_type=offline`, `prompt=consent` (required to reliably receive a refresh token)
   - `redirect_uri=http://127.0.0.1:{port}`
3. Open the system browser with `tauri_plugin_opener` (add it). Never an in-app webview.
4. Capture `?code=`, verify `state`, respond with a small styled bilingual HTML "you may
   close this window" page, then shut the listener down.
5. Exchange the code at `https://oauth2.googleapis.com/token` for access + refresh tokens.
6. **Store the refresh token in the OS keychain** via the `keyring` crate (Windows
   Credential Manager), service `ai.easyclip.desktop`. Never write tokens to disk in
   plaintext, never log them, never put a client secret in the frontend.
7. Implement automatic refresh: if a call returns 401, refresh once and retry.
8. Command `youtube_disconnect` must delete the keychain entry and clear cached state.

Google Cloud client credentials are supplied by the end user at runtime (see Part 6) —
"Desktop app" OAuth client type. Do **not** hardcode any credential in the repo.

## PART 2 — Source channel ingestion (`src-tauri/src/youtube/source.rs`)

Accept any of: a video URL (`watch?v=`, `youtu.be/`, `/shorts/`), a channel URL
(`/channel/UC…`, `/@handle`, `/c/name`, `/user/name`), or a playlist URL.

- Resolve to a channel ID using the API: `videos.list` → `snippet.channelId`, or
  `search.list`/`channels.list?forHandle=` for handles.
- Enumerate the full catalogue the quota-cheap way: `channels.list?part=contentDetails`
  → `relatedPlaylists.uploads` → page `playlistItems.list` (50/page, follow
  `nextPageToken`). Do **not** use `search.list` for enumeration — it costs 100 units
  per call and truncates results.
- For each video collect: id, title, description, duration, publishedAt, thumbnail,
  view count, and `status.license` (`youtube` vs `creativeCommon`).
- Cache results in SQLite so re-opening is instant.

## PART 3 — Download (`src-tauri/src/youtube/download.rs`)

The YouTube Data API cannot download video bytes. Use **`yt-dlp`**:

- Extend `scripts/prepare-windows-resources.ps1` to also fetch a pinned `yt-dlp.exe`
  release into `src-tauri/resources/bin/`, verified by SHA-256, exactly matching the
  existing style of that script (pinned URL + size + hash constants).
- Add `yt-dlp.exe` to the Tauri `bundle.resources` so it ships in the installer.
- Invoke it with `-f "bv*[height<=1080]+ba/b" --merge-output-format mp4`, writing into a
  work directory under `app_data_dir()`.
- Stream stdout, parse the `[download] xx.x%` lines, and emit Tauri events for progress.
- Respect a user-set concurrency limit (default 2) and a rate limit (`--limit-rate`).
- Handle failures with exponential backoff, max 3 attempts, and surface a clear error.

## PART 4 — Upload (`src-tauri/src/youtube/upload.rs`)

Use the **resumable** upload protocol (files are large; simple upload will fail):

1. `POST https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status`
   with the metadata JSON body → read the `Location` header (the session URI).
2. `PUT` the bytes to that URI in ~8 MB chunks with a correct
   `Content-Range: bytes a-b/total` header.
3. On network failure, query the session with `Content-Range: bytes */total`, read the
   `Range` response header, and resume from that byte — never restart from zero.
4. Treat HTTP 308 as "keep going", 200/201 as done, 5xx/429 as retryable with
   exponential backoff + jitter.
5. Metadata to send: title (≤100 chars, truncate safely on a char boundary — beware
   Persian/UTF-8, never split a grapheme), description, tags, `categoryId`,
   `privacyStatus` (user-selectable: `private` / `unlisted` / `public`, **default
   `private`**), `selfDeclaredMadeForKids: false`, and optional `publishAt` (RFC 3339)
   for scheduled release.
6. Emit upload progress events; persist the session URI so an interrupted upload resumes
   after an app restart.

**Quota reality — put this in the UI:** a single `videos.insert` costs **1600 units** of
the default **10,000 units/day** quota. That is **~6 uploads per day** per Google Cloud
project. The app must track spent quota, show "X of ~6 uploads left today", and pause
the queue with a clear message instead of hammering the API into errors.

## PART 5 — Queue, scheduler, dedupe (`src-tauri/src/youtube/queue.rs`)

- SQLite via `rusqlite` (bundled feature) at `app_data_dir()/easyclip.db`.
- Table `jobs`: id, source_video_id, source_channel_id, title, state
  (`pending|downloading|clipping|uploading|done|failed|skipped`), attempts, error,
  target_video_id, created_at, updated_at, plus a **`UNIQUE(source_video_id)`** constraint
  — this is what guarantees nothing is ever uploaded twice.
- A background worker (`tokio` task) drains the queue respecting concurrency + quota, and
  survives app restarts by resuming any non-terminal job.
- "Auto-watch" mode: poll the source channel's uploads playlist every N minutes
  (default 30) and enqueue anything new automatically. This is the "zero manual work" part.
- A "dry run" toggle that runs the whole pipeline but stops before `videos.insert`.

## PART 6 — Frontend (`src/App.tsx` + `src/youtube.css`)

Match the existing dark visual language exactly (`#111116` panels, `#24242c` borders,
`#7954ec` purple accent, Inter, small 8–13px type, pill badges). Keep the file's terse
formatting style. Every string must exist in **both** the `fa` and `en` translation
objects that already exist in `App.tsx`; the Persian UI must stay fully RTL.

Screens to build:

1. **Setup** — inputs for Google Client ID + Client Secret, with an inline collapsible
   guide (see below). Validate before enabling Connect.
2. **Connect** — "Sign in with Google" button; after auth show avatar, channel title,
   subscriber count, and a Disconnect button.
3. **Source** — paste box for the URL, then a virtualised table of the channel's videos
   with thumbnail, title, duration, date, a checkbox per row, "select all", a search
   filter, and a date-range filter.
4. **Options** — privacy (default Private), title template with tokens
   (`{title}`, `{index}`, `{date}`, `{channel}`), description template, tags,
   "auto-clip into Shorts" toggle (reusing the existing caption/render pipeline),
   caption language (fa/en/auto), schedule spacing (e.g. one upload every 4 h), and
   the auto-watch interval.
5. **Queue** — live per-job rows with state, a progress bar, error text, a link to the
   uploaded video, plus Pause / Resume / Retry / Remove, and the daily quota meter.

Add a `youtube:` permission set to `src-tauri/capabilities/default.json` as needed, and
whatever `opener` permission the sign-in flow requires.

## PART 7 — LEGAL GATE (mandatory, non-negotiable — implement it, do not skip it)

Re-uploading another creator's videos without permission triggers copyright strikes;
three strikes in 90 days permanently deletes the channel, and mass re-uploading is also
caught by YouTube's "reused content" and spam policies. Downloading other people's videos
also violates YouTube's Terms of Service. The user has been told this and still wants the
tool, so build it — but build it responsibly:

- On first use of a source channel, show a blocking modal (bilingual) stating the strike /
  termination / ToS risk. Require an explicit checkbox: *"I own this content or have
  written permission from the rights holder."* Store the acknowledgement with a timestamp.
- Detect `status.license == "creativeCommon"` and badge those videos green as
  "safe to reuse (CC-BY)"; badge standard-licence videos amber.
- Default `privacyStatus` to **private** so nothing goes public by accident.
- If the signed-in channel ID equals the source channel ID, hide the warning entirely —
  that is the safe, intended path.
- Auto-fill the description template with `Original: https://youtu.be/{id}` attribution.

## PART 8 — BUILD, DEBUG, AND VERIFY (do not skip — the task is not done until this passes)

Iterate until **all** of these are green. Actually run them; read the errors; fix; re-run.

```bash
cd easyclip-desktop
npm ci
npm run build                                   # tsc + vite, must be zero errors
cargo fmt --manifest-path src-tauri/Cargo.toml
cargo clippy --manifest-path src-tauri/Cargo.toml --all-targets -- -D warnings
cargo test  --manifest-path src-tauri/Cargo.toml
```

Write real unit tests for the pure logic (no network):

- URL parsing: all channel/video/playlist/handle/Shorts forms, plus malformed input.
- PKCE `code_challenge` derivation against a known RFC 7636 vector.
- `Content-Range` header construction, including the final short chunk.
- Resume-offset maths from a `Range: bytes=0-N` response header.
- Title truncation at 100 chars with multi-byte Persian text (must not split a char).
- Template token substitution.
- Quota accounting arithmetic.

Also add a `--self-test` CLI path or a hidden UI button that verifies `yt-dlp.exe`,
`ffmpeg.exe`, and the keychain are all reachable, and reports each one's status.

**Cross-compilation note:** if you are on Linux you cannot produce a Windows `.exe`
locally. That is expected — validate with `cargo check --target x86_64-pc-windows-msvc`
if available, otherwise rely on `cargo test` on the host plus CI for the real build.

## PART 9 — SHIP IT

1. Commit in logical chunks with clear messages (not one giant commit).
2. Push to `arena/019ffe1e-chat2db`.

   **CRITICAL GOTCHA:** if you are authenticated as a GitHub App / bot without the
   `workflows` permission, any push that creates or modifies a file under
   `.github/workflows/` is rejected with
   *"refusing to allow a GitHub App to create or update workflow … without `workflows`
   permission."* This also blocks the Contents API, the git-refs API, and
   `workflow_dispatch`. If you hit it: push every other file, place the workflow change
   at `easyclip-desktop/ci/` instead, and tell the user to move it into
   `.github/workflows/` themselves through the GitHub web UI (**Commit changes...**
   button at the top-right, then choose *Commit directly to the branch* in the modal).
3. Open a PR to `main` summarising the feature, the new permissions, and the risks.
4. Trigger `easyclip-windows.yml` and watch it to completion.

   **KNOWN CI GOTCHA (already fixed once — do not regress it):** in
   `src-tauri/tauri.conf.json`, the NSIS language must be spelled **`"Farsi"`**, not
   `"Persian"`. NSIS ships `Farsi.nlf` and has no `Persian.nlf`, so `makensis` exits 1
   and the "Build NSIS installer" step fails. Tauri accepts `"persian"` for its *own*
   translation strings, which makes this misleading.
5. Report the artifact link: `EasyClip-Desktop-<version>-Windows-x64`, containing
   `Setup.exe` + `SHA256SUMS.txt` (14-day retention).

## PART 10 — DOCUMENT

Append to `easyclip-desktop/README.md` a bilingual **"YouTube Autopilot"** section with
the exact Google Cloud setup steps, because the user must do this part themselves:

1. Open <https://console.cloud.google.com> → create a project.
2. **APIs & Services → Library → enable "YouTube Data API v3"**.
3. **OAuth consent screen** → External → fill app name + support email → add the three
   scopes listed in Part 1 → add your own Google account under **Test users**.
   (While the app is in "Testing", refresh tokens expire after 7 days — say this
   explicitly in the README, it is the #1 confusing failure.)
4. **Credentials → Create credentials → OAuth client ID → Desktop app** → copy the
   Client ID and Client secret.
5. Paste both into EasyClip → Settings → YouTube.
6. Note the ~6 uploads/day quota ceiling and link to the quota-increase request form.

Document every new Tauri command with its parameters and emitted events.

## CONSTRAINTS

- No secrets, tokens, or client IDs committed to the repo. Ever.
- Do not break the existing offline caption/render pipeline or its tests.
- Do not add a cloud backend — everything stays local to the user's machine.
- Keep the app fully functional offline when the YouTube feature is unused.
- Handle every network call with explicit timeouts and typed, user-readable errors —
  never `unwrap()` on I/O.
- All new user-facing strings must be added to both `fa` and `en` translations.
- Prefer `reqwest` (rustls) + `tokio`; add `keyring`, `rusqlite` (bundled), `sha2`,
  `base64`, `url`, `rand`, `chrono`, `tauri-plugin-opener`.

## DELIVERABLE

A pushed branch, a green CI run, a downloadable `Setup.exe`, and a short report listing:
what you built, what you tested, what failed and how you fixed it, and any limitation
that remains (quota ceiling, 7-day test-mode token expiry, unsigned installer /
SmartScreen warning).
