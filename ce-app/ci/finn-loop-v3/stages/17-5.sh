#!/usr/bin/env bash
set -euo pipefail
# 17.5 Taste Skill full gate + anti-slop audit
grep -rniE "lorem|placeholder-text|TODO-STYLE" ce-app/frontend/src --include=*.tsx --include=*.css | grep -v node_modules && { echo "anti-slop found"; exit 1; } || echo "anti-slop clean"
