# Muscle Paradise 0.19.0 — installer

Local-first gym OS. **Everything runs on your own machine** against a SQLite
file; there is no cloud account and no telemetry.

## What this package contains

| Component | State |
|---|---|
| Core API (FastAPI + SQLite, migrations, PDF receipts, encrypted backups) | complete — 239 tests, 90.9% coverage |
| Studio shell (coach) — prebuilt static bundle | complete |
| Athlete shell (`ClientShell`) — prebuilt in the same bundle | complete |
| Persian/Jalali UI, Persian PDF assessment + receipt | complete |
| Windows `.exe` / macOS `.dmg` / Electron desktop app | **not included** — see below |
| Native Flutter athlete app | **not included** — see below |

**Why there is no `.exe`/`.dmg`/APK:** the build sandbox has no Electron
runtime, no `electron-builder`, no NSIS/Inno Setup and no Flutter SDK (all
verified absent). This installer therefore ships the app in its supported form:
one local service on one port, which you open in a browser. It is not a
native-desktop build, and it is not labelled as one.

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

## Updating / uninstalling

Re-run `./install.sh` over the existing prefix; your `mp.db` is untouched.
To remove everything: `rm -rf ~/.muscle-paradise` (back up `mp.db` first — it is
your gym's data).

## Verifying the download

```bash
sha256sum -c SHA256SUMS        # Linux / macOS
Get-FileHash .\mp-app-0.19.0-windows.zip   # Windows, compare to SHA256SUMS.txt
```
