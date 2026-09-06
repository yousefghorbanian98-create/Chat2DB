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
# `zip` appends to an existing archive instead of replacing it, so a stale
# artifact would silently keep old files. Always start from nothing.
rm -rf "$OUT"; mkdir -p "$OUT"

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
cp -R "$MP/studio/dist" "$STAGE/studio"   # same name as the install layout
cp -R "$MP/assets" "$STAGE/assets"     # Persian TTF, resolved via parents[3]
cp -R "$MP/packs"  "$STAGE/packs"      # exercise library seed
cp "$HERE/install.sh" "$HERE/install.ps1" "$HERE/INSTALL.md" "$STAGE/"
chmod +x "$STAGE/install.sh"

# --- 2b. manifest of what an install copies (drives `mp update`) -----------
(cd "$MP/backend" && "$PY" -c "
from pathlib import Path
from app.updater import INSTALLED_TOP_LEVEL, write_manifest
write_manifest(Path('$STAGE'), '$VERSION', INSTALLED_TOP_LEVEL)
")

# --- 3. offline wheels (Linux x86_64 / CPython 3.11) -----------------------
# MP_DIST_NO_WHEELS=1 omits them: the archive is then ~2 MB instead of ~27 MB
# and the installer resolves dependencies from PyPI at install time.
if [ "${MP_DIST_NO_WHEELS:-0}" = "1" ]; then
  echo "==> Skipping wheels (MP_DIST_NO_WHEELS=1) — installer will use PyPI"
else
  echo "==> Downloading runtime wheels for offline install"
  mkdir -p "$STAGE/wheels"
  "$PY" -m pip download --quiet -r "$MP/backend/requirements-runtime.txt" -d "$STAGE/wheels"
fi

# --- 3b. optional differential (patch) archive -----------------------------
# MP_PATCH_FROM=<dir containing an older MANIFEST.json> also emits an archive
# holding only the files that changed since that version. `mp update --from`
# applies it exactly like a full package.
if [ -n "${MP_PATCH_FROM:-}" ]; then
  echo "==> Building a patch archive against $MP_PATCH_FROM"
  PATCH="$(cd "$MP/backend" && "$PY" - "$STAGE" "$MP_PATCH_FROM" <<'PYSCRIPT'
import json, sys
from pathlib import Path
from app.updater import MANIFEST_NAME, diff_manifests, load_manifest, read_version

stage, previous = Path(sys.argv[1]), Path(sys.argv[2])
old_files = load_manifest(previous / MANIFEST_NAME) or {}
new_files = load_manifest(stage / MANIFEST_NAME)
plan = diff_manifests(old_files, new_files)
out = stage.parent / f"patch-{read_version(previous / MANIFEST_NAME) or 'base'}-to-{read_version(stage / MANIFEST_NAME)}"
out.mkdir(parents=True, exist_ok=True)
for rel in (*plan.added, *plan.changed):
    target = out / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes((stage / rel).read_bytes())
(out / MANIFEST_NAME).write_bytes((stage / MANIFEST_NAME).read_bytes())
(out / "PATCH_INFO.json").write_text(json.dumps({
    "from": read_version(previous / MANIFEST_NAME),
    "to": read_version(stage / MANIFEST_NAME),
    "added": list(plan.added), "changed": list(plan.changed),
    "removed": list(plan.removed), "unchanged": plan.unchanged,
}, indent=2), encoding="utf-8")
print(out.name)
PYSCRIPT
)"
  (cd "$OUT" && tar czf "$PATCH.tar.gz" "$PATCH")
  rm -rf "$OUT/$PATCH"
fi

# --- 4. artifacts ----------------------------------------------------------
echo "==> Packing"
(cd "$OUT" && tar czf "mp-app-$VERSION-linux.tar.gz" "mp-app-$VERSION")
(cd "$OUT" && zip -qr "mp-app-$VERSION-windows.zip" "mp-app-$VERSION")
rm -rf "$STAGE"
(cd "$OUT" && find . -maxdepth 1 \( -name '*.tar.gz' -o -name '*.zip' \) -printf '%f\n' \
  | sort | xargs sha256sum > SHA256SUMS)

echo "==> Done"
ls -lh "$OUT"
cat "$OUT/SHA256SUMS"
