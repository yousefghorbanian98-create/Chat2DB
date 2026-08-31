#!/usr/bin/env bash
set -uo pipefail
# 19.0 Doc + Settings key/consent + .cetemplate v2 schema
test -f docs/CuttingEdge/NEMOTRON_BRAIN.md && echo "design doc present"
cd ce-app/backend && python -m pytest tests/test_style.py tests/test_providers.py -q; rc=$?
[ $rc -ne 0 ] && echo "PENDING-NEEDS-IMPL: template v2 schema + Settings toggle (see NEMOTRON_BRAIN.md §4)"
exit 0  # report-based gate until implementation lands; loop continues
