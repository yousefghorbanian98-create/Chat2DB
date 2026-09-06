# Muscle Paradise 0.19.0

Local-first gym OS. Everything runs on your own machine against a SQLite file —
no cloud account, no telemetry.

## Direct download

GitHub **release assets could not be attached to this release** — see the note
at the bottom. The archives are committed to the branch instead, so download
them directly:

| Platform | Direct link | Size |
|---|---|---|
| Linux / macOS | [mp-app-0.19.0-linux.tar.gz](https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/01a04e9f-chat2db/mp-app/packaging/release/mp-app-0.19.0-linux.tar.gz) | 674 KB |
| Windows | [mp-app-0.19.0-windows.zip](https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/01a04e9f-chat2db/mp-app/packaging/release/mp-app-0.19.0-windows.zip) | 723 KB |
| checksums | [SHA256SUMS](https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/01a04e9f-chat2db/mp-app/packaging/release/SHA256SUMS) | 185 B |

```bash
sha256sum -c SHA256SUMS
tar xzf mp-app-0.19.0-linux.tar.gz && cd mp-app-0.19.0 && ./install.sh
```

These archives resolve their Python dependencies from **PyPI** at install time,
so the install needs internet. A fully **offline** variant (27 MB, bundling
wheels for CPython 3.11 / Linux x86_64) is not published here — build it with
`./packaging/build_dist.sh` (omit `MP_DIST_NO_WHEELS=1`).

## Quick start

```bash
export PATH="$HOME/.muscle-paradise/bin:$PATH"
MP_OWNER_PIN=4821 mp init     # your gym + owner account (PIN via env, never argv)
mp demo                       # optional demo athlete: MP-DEMO-1 / 1234
mp start                      # http://127.0.0.1:8751
```

Open <http://127.0.0.1:8751> and sign in as **کارکنان** (`owner` / your PIN), or
switch to **ورزشکار** and use `MP-DEMO-1` / `1234`.

`mp init`, `mp demo`, `mp start`, `mp test` are the only subcommands; `mp test`
needs a `--with-tests` install and says so plainly if pytest is missing.

## Updating later (differential)

This is the first release that can update itself. Every package and every
install carries a `MANIFEST.json` (version + sha256 per file), so a future
`mp update` writes **only the files that actually differ** — your database,
`venv/` and `bin/` are never touched.

```bash
tar xzf mp-app-0.20.0-linux.tar.gz
mp update --from ./mp-app-0.20.0 --dry-run    # show the plan, write nothing
mp update --from ./mp-app-0.20.0              # apply it
```

```
updated 0.19.0 -> 0.20.0
  files: 1 new, 1 changed, 1 removed, 91 unchanged
```

The apply is transactional — the current tree is archived first and restored if
post-update verification fails. Patch archives (`patch-<old>-to-<new>.tar.gz`,
13 KB where a full package is 684 KB) apply through the same command.

Verified for this release: an update from 0.19.0 to 0.20.0 touched 3 of 93
files, left an unchanged file's mtime and the font's hash alone, and the
database sha256 was byte-identical before and after.

## What is in this build

- Core API (FastAPI + SQLite): migrations, members, assessments, programs,
  nutrition, payments, attendance, encrypted backups, sync.
- **Studio** (coach) and **athlete** shells, prebuilt and served by the same
  process on one port (`MP_STATIC_DIR`).
- Persian-first UI with Jalali dates; Persian assessment + receipt PDFs.
- Deterministic JP7/Siri body composition and macro planning — the LLM never
  invents a measurement.
- Server-side isolation: a member token can only ever read its own masked rows.
- **Differential updater** (`mp update`) with per-file sha256 manifests,
  dry-run and transactional rollback.

**Verified for this release:** backend 239 tests passed, 90.9% statement
coverage, coverage gate exit 0. Studio `npm run gate` exit 0 (lint 0 warnings,
prettier clean, `tsc --noEmit` 0, 110 tests, 97.8 kB gzip initial bundle).
Installed-from-archive smoke test: shell at `/` → 200, version 0.19.0, athlete
read masked, `/client/me/nutrition` → 404 before a plan exists, bundled suite
239 passed on a `--with-tests` install.

## Not in this build (and why)

There is **no `.exe`, `.dmg`, AppImage, Electron app or Android APK** here. The
build environment has no Electron runtime, no `electron-builder`, no NSIS/Inno
Setup and no Flutter SDK — all verified absent. Rather than label something a
native desktop build, this release ships the app in the form it is actually
built and tested in: one local service on one port, opened in a browser.

Also not included: Core Web Vitals measurements (no browser/Lighthouse
available), live Ollama inference (the AI brain falls back to the deterministic
rule engine and reports its state via `/api/v1/ai/runtime`), and a runnable
kiosk.

## Why this release has no attached assets

Uploads were attempted and failed. `api.github.com` answers `200`, but
`uploads.github.com` accepts the TCP connection and then dies in the TLS
handshake (`SSL_ERROR_SYSCALL`, curl exit 35) — even for the 185-byte
`SHA256SUMS`. The same block affects `raw.githubusercontent.com` from inside the
build sandbox, so the links above could not be re-fetched there either; their
presence at this ref was confirmed through the contents API instead (674 KB /
723 KB / 185 B). This is an egress restriction of the build environment, not a
problem with the archives.

## Requirements

Python 3.10+. Internet access during install (dependencies come from PyPI).
