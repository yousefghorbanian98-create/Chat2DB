#!/usr/bin/env bash
set -euo pipefail
# 17.1 Motion Token v2 — spring/easing/stagger library (Design Motion Principles)
test -f ce-app/frontend/src/styles/motion-tokens.css || echo "TODO: motion-tokens.css (spring/easing/stagger vars consumed by real rules)"
cd ce-app/backend && python -m pytest tests/test_motion.py -q
