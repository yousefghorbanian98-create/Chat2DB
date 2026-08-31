#!/usr/bin/env bash
set -uo pipefail
# 19.5 Extend to editor_brain/critic via same adapter
cd ce-app/backend && python -m pytest tests/test_editor_brain.py tests/test_brain.py -q
