#!/usr/bin/env bash
set -euo pipefail
# 16.3 Auto-diagnose — failure -> root cause -> patch proposal
cd ce-app/backend && python -m pytest tests/test_brain_upgrade.py tests/test_editor_brain.py -q
