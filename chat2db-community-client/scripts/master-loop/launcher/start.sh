#!/usr/bin/env sh
# Motion Package — one-command launcher (macOS / Linux)
cd "$(dirname "$0")"
if ! command -v node >/dev/null 2>&1; then
  echo "Node.js not found. Install it from https://nodejs.org then run this again."
  exit 1
fi
node serve-dist.cjs --open
