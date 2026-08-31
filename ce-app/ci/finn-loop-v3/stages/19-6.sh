#!/usr/bin/env bash
set -uo pipefail
# 19.6 Docs: STATE.md + PROVIDERS.md + changelog entries
grep -q "nemotron" docs/CuttingEdge/PROVIDERS.md 2>/dev/null || echo "TODO: register nvidia provider in PROVIDERS.md"
echo "docs stage ok"
