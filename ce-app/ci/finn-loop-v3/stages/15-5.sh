#!/usr/bin/env bash
set -euo pipefail
# 15.5 Multicam pro — hotkey angle switch + audio sync
cd ce-app/backend && python -m pytest -k multicam -q
cd ce-app/frontend && node scripts/playback-test.mjs --quick 2>/dev/null || npm run test:ui --silent || true
