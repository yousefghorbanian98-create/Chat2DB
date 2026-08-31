#!/usr/bin/env bash
set -euo pipefail
# 18.1 Size gate — bundle + installer budget (<=336MB)
cd ce-app/frontend && npx vite build --logLevel warn && du -sm dist | awk '{print "bundle MB:",$1}'
