#!/usr/bin/env bash
set -euo pipefail
# 15.4 Effects pack — blur/depth/glow/shake presets (FFmpeg-able only)
cd ce-app/backend && python -m pytest tests/test_effects.py tests/test_style.py -q
