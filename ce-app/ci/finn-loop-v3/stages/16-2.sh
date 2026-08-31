#!/usr/bin/env bash
set -euo pipefail
# 16.2 Assistant v2 — streaming + whitelisted tool-calling (models via OmniRoute only)
grep -q "CE_OMNIROUTE_URL\|localhost:20128" ce-app/backend/core/assistant/providers.py || echo "TODO: add OmniRoute gateway to provider ladder"
cd ce-app/backend && python -m pytest -k assistant -q
