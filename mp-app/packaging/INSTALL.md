# Muscle Paradise 0.19.0 — installer

Local-first gym OS. **Everything runs on your own machine** against a SQLite
file; there is no cloud account and no telemetry.

## What this package contains

| Component | State |
|---|---|
| Core API (FastAPI + SQLite, migrations, PDF receipts, encrypted backups) | complete — 249 tests, 90.8% coverage |
| **Admin app** (owner + coach) — installable PWA at `/` | complete |
| **Athlete app** — installable PWA at `/client.html` | complete |
| Offline shell (service worker), icons, standalone display | complete |
| Persian/Jalali UI, Persian PDF assessment + receipt | complete |
| Windows install + Start Menu/Desktop shortcuts | complete (script installer) |
| Android install | complete **as a PWA** — see below |
| Native `.apk` / `.exe` / `.dmg` binaries | **not included** — see below |

## Installing on Android

The two apps are Progressive Web Apps, so they install on Android without a
Play Store listing. Point Chrome at the machine running the core, then install:

1. On the PC: `mp start` (default `http://127.0.0.1:8751`).
2. To reach it from the phone, expose it on the LAN and allow the phone's origin:
   ```bash
   MP_HOST=0.0.0.0 MP_CORS_ORIGINS="http://<pc-ip>:8751" mp start
   ```
3. On the phone (same Wi‑Fi), open `http://<pc-ip>:8751/` → Chrome menu →
   **Install app** / **افزودن به صفحهٔ اصلی**. Repeat on
   `http://<pc-ip>:8751/client.html` to install the athlete app separately.

You get two separate launcher icons (`mp-admin` and `mp-client`), full-screen
with no browser chrome, and the shell loads offline. Data still lives on the PC,
which is the local-first design.

> An `.apk` is **not** provided: building one needs the Android SDK, Gradle and
> a Flutter/Android toolchain, and `dl.google.com`, `storage.googleapis.com` and
> `services.gradle.org` are all unreachable from the build sandbox (verified —
> each returns no response). A PWA install is the supported Android path here.

## Installing on Windows

`install.ps1` creates a virtualenv, installs the app, writes `mp.cmd` and adds
**Start Menu and Desktop shortcuts** (pass `-NoShortcuts` to skip). Double-click
the shortcut, or run `mp start`, then open <http://127.0.0.1:8751> — and
**Install app** from Edge/Chrome to get it as a windowed app with its own icon.

There is no `.exe`/`.msi`: NSIS, Inno Setup and `wine` are absent from the build
environment, and PyInstaller cannot cross-compile a Windows binary from Linux.

## Install

### Linux / macOS

```bash
tar xzf mp-app-0.19.0-linux.tar.gz
cd mp-app-0.19.0
./install.sh
export PATH="$HOME/.muscle-paradise/bin:$PATH"
```

`install.sh` installs into `~/.muscle-paradise` (override with
`MP_PREFIX=/opt/mp`). It needs Python 3.10+.

Add `--with-tests` (PowerShell: `-WithTests`) to also install pytest and
PyMuPDF so `mp test` can run the bundled 239-test suite.

### Windows

```powershell
Expand-Archive .\mp-app-0.19.0-windows.zip -DestinationPath .
cd .\mp-app-0.19.0
powershell -ExecutionPolicy Bypass -File .\install.ps1
set PATH=%USERPROFILE%\.muscle-paradise;%PATH%
```

Windows always resolves dependencies from PyPI, because the bundled wheels in
`wheels/` are built for Linux x86_64 / CPython 3.11. On Linux those wheels are
used and the install works **fully offline**; on any other platform the
installer detects the mismatch and falls back to PyPI (needs internet).

## First run

```bash
MP_OWNER_PIN=4821 mp init      # create your gym + owner account (PIN via env, never argv)
mp demo                        # optional: one demo athlete, MP-DEMO-1 / PIN 1234
mp start                       # http://127.0.0.1:8751
```

Open <http://127.0.0.1:8751> and sign in:

- **کارکنان** — `owner` / the PIN you chose
- **ورزشکار** — `MP-DEMO-1` / `1234` (only if you ran `mp demo`)

`mp init`, `mp demo`, `mp start` and `mp test` are the only subcommands. `mp test`
needs a `--with-tests` install and says so plainly if pytest is missing.

## Configuration (environment variables)

| Variable | Default | Purpose |
|---|---|---|
| `MP_DB_PATH` | `~/.muscle-paradise/mp.db` | SQLite database location |
| `MP_HOST` | `127.0.0.1` | bind address (`0.0.0.0` to expose on the LAN) |
| `MP_PORT` | `8751` | port |
| `MP_STATIC_DIR` | set by the launcher | prebuilt Studio bundle to serve at `/` |
| `MP_OWNER_PIN` | — | required by `mp init`; read from the environment on purpose so it never lands in shell history or the process list |
| `MP_GYM_NAME` | `Muscle Paradise` | gym name |
| `MP_CORS_ORIGINS` | local origins | comma-separated allowlist (no wildcard) |

## Updating (differential)

Every package carries a `MANIFEST.json` (version + sha256 per file) and every
install keeps a copy, so `mp update` writes **only the files that actually
differ** — your database, `venv/` and `bin/` are never touched.

```bash
tar xzf mp-app-0.20.0-linux.tar.gz
mp update --from ./mp-app-0.20.0 --dry-run    # show the plan, write nothing
mp update --from ./mp-app-0.20.0              # apply it
```

```
updated 0.19.0 -> 0.20.0
  files: 1 new, 1 changed, 1 removed, 91 unchanged
```

A **patch archive** (`patch-<old>-to-<new>.tar.gz`, built with
`MP_PATCH_FROM=<previous package> ./packaging/build_dist.sh`) contains only the
changed files and applies the same way — 13 KB where a full package is 684 KB.

The apply is transactional: the current tree is archived first and restored if
post-update verification fails, and protected paths (`venv/`, `bin/`, `*.db*`)
are refused outright. Dependencies are re-installed only when a requirements
file actually changed.

Re-running `./install.sh` over the prefix also works as a blunt full refresh.

## Uninstalling

`rm -rf ~/.muscle-paradise` — back up `mp.db` first, it is your gym's data.

## Verifying the download

```bash
sha256sum -c SHA256SUMS        # Linux / macOS
Get-FileHash .\mp-app-0.19.0-windows.zip   # Windows, compare to SHA256SUMS.txt
```
