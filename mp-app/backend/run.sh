#!/usr/bin/env bash
# Start the MP core on the map-mandated port 8751.
#   MP_DB_PATH=/path/to/mp.db ./run.sh
set -euo pipefail
cd "$(dirname "$0")"

VENV="${MP_VENV:-../../.venv-mp}"
PY="$VENV/bin/python"
[ -x "$PY" ] || { echo "no venv python at $PY — set MP_VENV" >&2; exit 1; }

exec "$PY" -m uvicorn app.main:create_app_from_env --factory \
  --host "${MP_HOST:-127.0.0.1}" --port "${MP_PORT:-8751}"
