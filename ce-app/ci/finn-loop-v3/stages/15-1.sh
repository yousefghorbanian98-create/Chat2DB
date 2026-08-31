#!/usr/bin/env bash
set -euo pipefail
# 15.1 Keyframe Engine v2 — bezier/velocity curves (editor + export)
grep -q "bezier" ce-app/frontend/src/editor/model.ts || echo "TODO(model.ts): add bezier easing + velocity curves to Keyframe type"
grep -q "bezier" ce-app/backend/core/engine/compose.py || echo "TODO(compose.py): map bezier easing to FFmpeg expressions"
cd ce-app/backend && python -m pytest -k keyframes -q
