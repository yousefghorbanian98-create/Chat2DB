#!/usr/bin/env bash
# Build the Muscle Paradise installer artifacts.
#
#   ./packaging/build_dist.sh            # -> mp-app/dist-release/
#
# Produces, from the working tree only (nothing is fetched except pip wheels):
#   mp-app-<ver>-linux.tar.gz    install.sh + offline wheels (cp311/manylinux)
#   mp-app-<ver>-windows.zip     install.ps1 (resolves deps from PyPI)
#   SHA256SUMS                   checksums for both
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MP="$(dirname "$HERE")"
VENV="${MP_VENV:-$MP/../.venv-mp}"
PY="$VENV/bin/python"
[ -x "$PY" ] || { echo "no venv python at $PY — set MP_VENV" >&2; exit 1; }

VERSION="$(cd "$MP/backend" && "$PY" -c "from app import __version__; print(__version__)")"
OUT="$MP/dist-release"
STAGE="$OUT/mp-app-$VERSION"

echo "==> Building Muscle Paradise $VERSION"
rm -rf "$STAGE"; mkdir -p "$STAGE"

# --- 1. frontend bundle ----------------------------------------------------
if [ ! -f "$MP/studio/dist/index.html" ]; then
  echo "==> Building the Studio bundle (npm run build)"
  (cd "$MP/studio" && npm run build >/dev/null)
fi

# --- 2. assemble -----------------------------------------------------------
cp -R "$MP/backend" "$STAGE/backend"
find "$STAGE/backend" -name __pycache__ -type d -prune -exec rm -rf {} + 2>/dev/null || true
rm -f "$STAGE/backend/.coverage"
cp -R "$MP/studio/dist" "$STAGE/studio-dist"
cp -R "$MP/assets" "$STAGE/assets"     # Persian TTF, resolved via parents[3]
cp -R "$MP/packs"  "$STAGE/packs"      # exercise library seed
cp "$HERE/install.sh" "$HERE/install.ps1" "$HERE/INSTALL.md" "$STAGE/"
chmod +x "$STAGE/install.sh"

# --- 3. offline wheels (Linux x86_64 / CPython 3.11) -----------------------
echo "==> Downloading runtime wheels for offline install"
mkdir -p "$STAGE/wheels"
"$PY" -m pip download --quiet -r "$MP/backend/requirements-runtime.txt" -d "$STAGE/wheels"

# --- 4. artifacts ----------------------------------------------------------
echo "==> Packing"
(cd "$OUT" && tar czf "mp-app-$VERSION-linux.tar.gz" "mp-app-$VERSION")
(cd "$OUT" && zip -qr "mp-app-$VERSION-windows.zip" "mp-app-$VERSION")
rm -rf "$STAGE"
(cd "$OUT" && sha256sum "mp-app-$VERSION-linux.tar.gz" "mp-app-$VERSION-windows.zip" > SHA256SUMS)

echo "==> Done"
ls -lh "$OUT"
cat "$OUT/SHA256SUMS"
