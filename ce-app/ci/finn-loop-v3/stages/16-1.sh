#!/usr/bin/env bash
set -euo pipefail
# 16.1 Brain upgrade — planner<->critic with long-term memory
cd ce-app/backend && python -m pytest -k brain -q
