#!/usr/bin/env bash
set -uo pipefail
# 19.2 brain/nemotron.py + Style Match v2 "style why" fields
if [ -z "${CE_NVIDIA_API_KEY:-}" ]; then echo "PENDING-NEEDS-KEY"; exit 0; fi
cd ce-app/backend && python -m pytest tests/test_style_template_v2.py -k style -q
