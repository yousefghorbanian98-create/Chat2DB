#!/usr/bin/env bash
set -uo pipefail
# 19.1 NemotronProvider — OpenAI-compat integrate.api.nvidia.com/v1 in the ladder
if [ -z "${CE_NVIDIA_API_KEY:-}" ]; then echo "PENDING-NEEDS-KEY: export CE_NVIDIA_API_KEY (free: build.nvidia.com)"; exit 0; fi
cd ce-app/backend && python -m pytest tests/test_providers_nvidia.py -q
