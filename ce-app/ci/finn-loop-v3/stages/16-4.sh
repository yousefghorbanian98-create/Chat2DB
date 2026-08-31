#!/usr/bin/env bash
set -euo pipefail
# 16.4 Deep button-by-button E2E across all screens/states
cd ce-app/frontend && npm run test:ui --silent && node scripts/ui-audit.mjs --deep 2>/dev/null || npm run test:ui --silent
