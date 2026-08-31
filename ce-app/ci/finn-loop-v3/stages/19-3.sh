#!/usr/bin/env bash
set -uo pipefail
# 19.3 A/B harness on 3 fixtures; rule: no key metric worse by >10%
if [ -z "${CE_NVIDIA_API_KEY:-}" ]; then echo "PENDING-NEEDS-KEY"; exit 0; fi
cd ce-app/backend && python -m pytest tests/test_ab_harness.py -q
