#!/usr/bin/env bash
set -euo pipefail
# 17.6 a11y + reduced-motion parity
grep -rq "prefers-reduced-motion" ce-app/frontend/src/styles || { echo "missing reduced-motion"; exit 1; }
cd ce-app/frontend && npm run test:ui --silent
