#!/usr/bin/env bash
set -euo pipefail
# 15.3 Motion tracking v2 — attach text/objects to tracked motion
cd ce-app/backend && python -m pytest -k "motion or pose or face" -q
