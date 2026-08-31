#!/usr/bin/env bash
set -euo pipefail
# 17.2 Cinematic landing — aurora gradient-mesh + cursor spotlight + particle field (casberry-style)
test -f ce-app/frontend/src/components/LiveGlobe.tsx && echo "globe present; add aurora+spotlight layers behind Home"
cd ce-app/backend && python -m pytest tests/test_motion.py -q
