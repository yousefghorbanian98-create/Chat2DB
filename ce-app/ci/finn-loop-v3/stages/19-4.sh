#!/usr/bin/env bash
set -uo pipefail
# 19.4 Default Style Match when key+consent; offline path preserved
cd ce-app/backend && python -m pytest -k "brain and not upgrade" -q
