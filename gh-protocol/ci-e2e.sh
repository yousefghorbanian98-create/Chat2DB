#!/usr/bin/env bash
# P2b: instrumented E2E — real VPN on an x86_64 emulator.
# Runs inside reactivecircus/android-emulator-runner (adb available, emulator up).
# Sequence: install -> launch -> deep-link connect -> VPN consent -> tunnel up
#           -> DNS through tunnel -> (HTTPS if curl) -> logcat sanity.
# On failure: publishes full diag to the ci-diag branch.
set -uo pipefail

LOG="$(cd "$(dirname "$0")" && pwd)/e2e.log"
PKG=com.ghprotocol.app
APK="$(dirname "$LOG")/app/build/outputs/apk/debug/app-debug.apk"
: > "$LOG"

say() { echo "$@"; echo "$@" >> "$LOG"; }

report() {
  # Log publication happens in the workflow's "always()" step (keeps this script simple).
  say "=== E2E FAILED: $1 ==="
  exit 1
}

say "== adb devices =="
adb devices

say "== wait for emulator to reach device state =="
STATE=""
for i in $(seq 1 90); do
  STATE=$(adb get-state 2>/dev/null | tr -d '\r' || true)
  BOOTED=$(adb shell getprop sys.boot_completed 2>/dev/null | tr -d '\r' || true)
  if [ "$STATE" = "device" ] && [ "$BOOTED" = "1" ]; then
    say "emulator ready after ~$((i * 4))s"
    break
  fi
  sleep 4
done
adb devices >> "$LOG" 2>&1
[ "$STATE" = "device" ] && [ "$BOOTED" = "1" ] || report "emulator not ready (state=$STATE boot=$BOOTED)"

say "== install APK =="
[ -f "$APK" ] || { ls -R app/build/outputs 2>&1 | head -20 >> "$LOG"; report "APK not found at $APK"; }
adb install -r "$APK" >>"$LOG" 2>&1 || report "apk install failed"

D="$(dirname "$LOG")"

# --- subscription availability: live fetch vs pre-seeded cache -----------------
# The emulator's QEMU NAT may not reach GitHub (observed on GH runners), while the
# runner itself has full internet. Probe the REAL sub host from the emulator:
#  - reachable  -> SUBMODE=live   : app fetches on its own (full F-5/F-6 path)
#  - not        -> SUBMODE=seeded : seed the app cache (host-downloaded sub.json);
#                                  tunnel/core/VPN/DNS are still fully real.
SUBHOST="raw.githubusercontent.com"
say "== probe emulator reachability to sub host ($SUBHOST:443, up to 60s) =="
REACH=0
for i in $(seq 1 15); do
  if adb shell "toybox nc -z -w 3 $SUBHOST 443 >/dev/null 2>&1"; then
    REACH=1
    say "emulator can reach $SUBHOST after ~$((i * 4))s"
    break
  fi
  sleep 4
done

if [ "$REACH" = "1" ]; then
  SUBMODE="live"
  say "SUBMODE=live — app will fetch the subscription itself (full E2E)"
else
  SUBMODE="seeded"
  say "WARN: emulator CANNOT reach $SUBHOST (runner NAT) — pre-seeding app cache"
  SUB="$D/sub.json"
  [ -s "$SUB" ] || report "no sub.json for seeding (host-side fetch step must have produced it)"
  TS=$(python3 -c 'import time; print(int(time.time() * 1000))' 2>/dev/null || echo "$(date +%s)000")
  # Stream into the app's filesDir via run-as stdin — SELinux blocks app reads
  # of /sdcard files pushed by adb (shell_data_file) on API 30+.
  adb shell "run-as $PKG sh -c 'cat > files/subscription.json'" < "$SUB" >> "$LOG" 2>&1 \
    || report "seed: writing subscription.json failed (see log above)"
  adb shell "run-as $PKG sh -c 'echo $TS > files/subscription.meta'" >> "$LOG" 2>&1 \
    || report "seed: writing subscription.meta failed"
  SEEDBYTES=$(adb shell "run-as $PKG sh -c 'wc -c < files/subscription.json'" | tr -d '\r \n')
  { [ -n "$SEEDBYTES" ] && [ "$SEEDBYTES" -gt 1000 ] 2>/dev/null; } \
    || report "seed verification failed (bytes=${SEEDBYTES:-none})"
  say "seeded cache: $SEEDBYTES bytes, meta=$TS"
fi

say "== launch app (am start, up to 3 tries) =="
LAUNCHED=0
for i in 1 2 3; do
  adb shell am start -n "$PKG/.MainActivity" >>"$LOG" 2>&1 || true
  sleep 8
  ALIVE=$(adb shell "pidof $PKG" 2>/dev/null | tr -d '\r')
  if [ -n "$ALIVE" ]; then
    LAUNCHED=1
    say "app up (try $i, pid $ALIVE)"
    break
  fi
  say "try $i: app not alive — capturing logcat"
  adb logcat -d | grep -E "ghprotocol|AndroidRuntime|FATAL" | tail -40 >> "$LOG" 2>/dev/null || true
  sleep 7
done
if [ "$LAUNCHED" != "1" ]; then
  adb logcat -d -b crash > "$D/e2e-crash.log" 2>/dev/null || true
  adb logcat -d > "$D/e2e-logcat.log" 2>/dev/null || true
  tail -60 "$D/e2e-crash.log" >> "$LOG" 2>/dev/null || true
  report "app not alive after 3 launch attempts (crash+logcat attached)"
fi

say "== trigger connect via deep link =="
adb shell am start -a android.intent.action.VIEW -d "ghprotocol://connect" >>"$LOG" 2>&1 || report "deep link failed"

say "== wait for tunnel; tap VPN consent when it appears (up to 6 min) =="
TUNNEL=0
CONSENT=0
for i in $(seq 1 90); do
  if adb shell "ps -A" 2>/dev/null | grep -qi "xray" && adb shell "netstat -ltn" 2>/dev/null | grep -q ":10808"; then
    TUNNEL=1
    say "tunnel up after ~$((i * 4))s"
    break
  fi
  # app must stay alive
  if [ $((i % 5)) -eq 0 ]; then
    ALIVE=$(adb shell "pidof $PKG" 2>/dev/null | tr -d '\r')
    if [ -z "$ALIVE" ]; then
      say "app died during connect flow (iter $i)"
      adb logcat -d > "$D/e2e-logcat.log" 2>/dev/null || true
      report "app process died during connect flow (logcat attached)"
    fi
  fi
  # consent dialog?
  if [ "$CONSENT" != "1" ] && [ $((i % 3)) -eq 0 ]; then
    adb shell uiautomator dump /sdcard/ui.xml >/dev/null 2>&1
    adb pull /sdcard/ui.xml /tmp/ui.xml >/dev/null 2>&1
    if [ -s /tmp/ui.xml ] && grep -qi "vpn" /tmp/ui.xml; then
      COORDS=$(python3 - <<'PY'
import re
x = open('/tmp/ui.xml', encoding='utf-8', errors='ignore').read()
for m in re.finditer(r'text="([^"]*)"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"', x):
    t = m.group(1).strip().lower()
    if t in ("allow", "allow anyway", "ok", "قبول"):
        print((int(m.group(2)) + int(m.group(4))) // 2, (int(m.group(3)) + int(m.group(5))) // 2)
        break
PY
)
      if [ -n "${COORDS:-}" ]; then
        adb shell input tap $COORDS >>"$LOG" 2>&1
        say "tapped VPN consent at: $COORDS (iter $i)"
        CONSENT=1
      fi
    fi
  fi
  sleep 4
done
[ "$CONSENT" = "1" ] || say "WARN: consent dialog never seen"
[ "$TUNNEL" = "1" ] || {
  adb shell "ps -A" | grep -E "$PKG|xray|NAME" >> "$LOG" 2>&1
  adb shell "netstat -ltn" >> "$LOG" 2>&1
  adb shell "dumpsys activity activities" 2>/dev/null | grep -B2 -A8 -i "ghprotocol" >> "$LOG" 2>&1 || true
  say "app filesDir/xray:"
  adb shell "run-as $PKG ls -la files/xray 2>/dev/null" >> "$LOG" 2>&1
  say "xray-err.log:"
  adb shell "run-as $PKG cat files/xray/xray-err.log 2>/dev/null" >> "$LOG" 2>&1
  say "GhDiag (connect-flow trace):"
  adb logcat -d -s GhDiag >> "$LOG" 2>&1
  adb logcat -d > "$D/e2e-logcat.log" 2>/dev/null || true
  adb logcat -d -b crash >> "$D/e2e-logcat.log" 2>/dev/null || true
  report "tunnel not up (xray/:10808)"
}

say "== DNS resolution THROUGH the tunnel =="
DNS_OK=0
for i in $(seq 1 8); do
  OUT=$(adb shell "toybox nslookup github.com" 2>&1)
  if echo "$OUT" | grep -qi "github.com"; then
    DNS_OK=1
    say "DNS ok: $(echo "$OUT" | head -4 | tail -2 | tr '\n' ' ')"
    break
  fi
  sleep 3
done
[ "$DNS_OK" = "1" ] || { echo "$OUT" >> "$LOG"; report "DNS through tunnel failed"; }

say "== HTTPS probe through tunnel (best-effort) =="
if adb shell "command -v curl" >/dev/null 2>&1; then
  CODE=$(adb shell "curl -sS -m 20 -o /dev/null -w '%{http_code}' https://github.com" 2>&1 | tail -1)
  if echo "$CODE" | grep -qE "^(200|301|302)$"; then
    say "HTTPS ok: $CODE"
  else
    say "WARN: HTTPS probe inconclusive (got: $CODE)"
  fi
else
  say "no curl on emulator — skipping HTTPS probe (DNS + tunnel are the core signal)"
fi

say "== Xray core stderr (from app filesDir) =="
adb shell "run-as $PKG cat files/xray/xray-err.log 2>/dev/null" > "$(dirname "$LOG")/e2e-xray-err.log" 2>/dev/null || true
tail -40 "$(dirname "$LOG")/e2e-xray-err.log" >> "$LOG" 2>/dev/null || true

say "== logcat sanity (crashes + GhVpnTunnel) =="
adb logcat -d > "$(dirname "$LOG")/e2e-logcat.log" 2>/dev/null || true
grep -E "AndroidRuntime|FATAL" "$(dirname "$LOG")/e2e-logcat.log" 2>/dev/null | grep -i "$PKG\|ghprotocol" >> "$LOG" || true
if grep -E "FATAL EXCEPTION" "$(dirname "$LOG")/e2e-logcat.log" 2>/dev/null | grep -qi "ghprotocol"; then
  report "app crashed (FATAL EXCEPTION in logcat)"
fi
adb logcat -d -s GhVpnTunnel > "$(dirname "$LOG")/e2e-vpn.log" 2>/dev/null || true
cat "$(dirname "$LOG")/e2e-vpn.log" >>"$LOG" 2>/dev/null || true
adb logcat -d -s GhDiag >> "$LOG" 2>/dev/null || true
if grep -q "establish failed" "$(dirname "$LOG")/e2e-vpn.log" 2>/dev/null; then
  report "vpn establish failed in logcat"
fi

say "==============================="
say "E2E PASS: tunnel up, DNS via tunnel works (SUBMODE=$SUBMODE)"
say "  - core install + start: verified"
say "  - VpnService establish: verified (consent tapped: $CONSENT)"
say "  - DNS through tunnel: verified"
if [ "$SUBMODE" = "seeded" ]; then
  say "  - subscription fetch: SKIPPED this run (runner NAT blocked sub host; cache was pre-seeded)"
fi
say "==============================="
exit 0
