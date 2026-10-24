#!/usr/bin/env bash
# Fetch + SHA-256-verify Xray-core Android builds into app assets.
# Self-diagnosing: on ANY failure, commits fetch-diag.log to the ci-diag branch.
set -uo pipefail

VERSION="26.10.21"
REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
DIAG="${REPO_DIR}/fetch-diag.log"
: > "$DIAG"
log() { echo "$@"; echo "$@" >> "$DIAG"; }

publish_diag() {
  local rc=$1
  [ "$rc" -eq 0 ] && return 0
  log "=== fetch script exiting rc=${rc} — publishing diag ==="
  cd "$REPO_DIR" || return 1
  git config user.name "gh-protocol-ci"
  git config user.email "gh-protocol-ci@users.noreply.github.com"
  git checkout -B ci-diag >>"$DIAG" 2>&1 || true
  mkdir -p gh-protocol
  {
    echo "## gh-protocol Xray fetch diag — $(date -u +%FT%TZ) (exit=${rc})"
    echo
    cat "$DIAG"
  } > gh-protocol/ci-failure.log
  git add gh-protocol/ci-failure.log
  git commit -m "ci-diag: fetch diag $(date -u +%Y%m%d-%H%M%S)" --allow-empty >>"$DIAG" 2>&1 || true
  git push origin HEAD:ci-diag --force >>"$DIAG" 2>&1 || true
  log "diag published (push rc=$?)"
  return 1
}
trap 'publish_diag $?' EXIT

log "== tools =="
for t in curl unzip sha256sum git tr cut grep; do
  if command -v "$t" >/dev/null 2>&1; then log "have $t: $(command -v $t)"; else log "MISSING $t"; fi
done
unzip -v 2>/dev/null | head -1 >> "$DIAG" 2>&1 || log "unzip -v failed"

for ABI in arm64-v8a amd64; do
  ZIP="Xray-android-${ABI}.zip"
  DEST="app/src/main/assets/xray/Xray-${ABI}"
  log "== ${ZIP} =="
  if ! curl -fSL --retry 3 --retry-delay 2 -o "/tmp/${ZIP}" \
       "https://github.com/XTLS/Xray-core/releases/download/${VERSION}/${ZIP}"; then
    log "FATAL: curl download failed for ${ZIP}"
    exit 41
  fi
  if ! curl -fSL --retry 3 --retry-delay 2 -o "/tmp/${ZIP}.dgst" \
       "https://github.com/XTLS/Xray-core/releases/download/${VERSION}/${ZIP}.dgst"; then
    log "FATAL: curl download failed for ${ZIP}.dgst"
    exit 41
  fi
  log "dgst file: $(cat /tmp/${ZIP}.dgst | tr '\n' '|')"
  EXPECTED=$(grep "^SHA2-256=" "/tmp/${ZIP}.dgst" | cut -d= -f2 | tr -d " " | tr "[:upper:]" "[:lower:]")
  ACTUAL=$(sha256sum "/tmp/${ZIP}" | awk '{print $1}')
  log "expected=${EXPECTED} actual=${ACTUAL}"
  if [ -z "$EXPECTED" ] || [ "$EXPECTED" != "$ACTUAL" ]; then
    log "FATAL: SHA-256 MISMATCH for ${ZIP}"
    exit 43
  fi
  log "sha256 verified ${ZIP}"
  rm -rf "/tmp/xray-${ABI}" && mkdir -p "/tmp/xray-${ABI}"
  if ! unzip -o "/tmp/${ZIP}" -d "/tmp/xray-${ABI}" >> "$DIAG" 2>&1; then
    log "FATAL: unzip failed; zip layout:"
    ls -la /tmp/ | grep -i xray >> "$DIAG" 2>&1
    head -c 300 "/tmp/${ZIP}" | od -c | head -5 >> "$DIAG" 2>&1
    exit 44
  fi
  BIN=$(find "/tmp/xray-${ABI}" -type f -name "Xray*" | head -n 1)
  if [ -z "$BIN" ]; then
    log "FATAL: no Xray binary in ${ZIP}; extracted files:"
    find "/tmp/xray-${ABI}" -type f | head -20 >> "$DIAG" 2>&1
    exit 45
  fi
  log "binary: ${BIN} ($(du -h "$BIN" | cut -f1))"
  mkdir -p "$(dirname "$DEST")"
  cp "$BIN" "$DEST"
  for DAT in /tmp/xray-${ABI}/*.dat; do [ -f "$DAT" ] && cp "$DAT" "$(dirname "$DEST")"; done
  chmod 755 "$DEST"
  log "installed ${ZIP} -> ${DEST}"
done

log "ALL FETCHES OK"
exit 0
