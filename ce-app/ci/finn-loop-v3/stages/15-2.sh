#!/usr/bin/env bash
set -euo pipefail
# 15.2 Mask & Blend modes in compose
grep -q "maskedmerge" ce-app/backend/core/engine/compose.py || echo "TODO: add mask/blend via maskedmerge + blend filter"
cd ce-app/backend && python -m pytest tests/test_compose.py -q
