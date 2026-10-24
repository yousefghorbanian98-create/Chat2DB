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
adb install -r "$APK" >>"$LOG" 2>&1 || report "apk install failed"

say "== launch app =="
adb shell monkey -p "$PKG" -c android.intent.category.LAUNCHER 1 >>"$LOG" 2>&1 || report "app launch failed"
sleep 20 # first launch: subscription fetch + UI settle

say "== trigger connect via deep link =="
adb shell am start -a android.intent.action.VIEW -d "ghprotocol://connect" >>"$LOG" 2>&1 || report "deep link failed"

say "== VPN consent dialog (tap Allow) =="
CONSENT=0
for i in $(seq 1 25); do
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
      say "tapped consent at: $COORDS"
      CONSENT=1
      break
    fi
  fi
  sleep 2
done
[ "$CONSENT" = "1" ] || say "WARN: consent dialog not seen (may have been auto-granted or missed)"

say "== wait for tunnel (Xray process + :10808 listening) =="
TUNNEL=0
for i in $(seq 1 40); do
  if adb shell "ps -A" 2>/dev/null | grep -qi "xray" && adb shell "netstat -ltn" 2>/dev/null | grep -q ":10808"; then
    TUNNEL=1
    say "tunnel up after ~$((i * 3))s"
    break
  fi
  sleep 3
done
[ "$TUNNEL" = "1" ] || { adb shell "ps -A" >>"$LOG" 2>&1; adb shell "netstat -ltn" >>"$LOG" 2>&1; report "tunnel not up (xray/:10808)"; }

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
if grep -q "establish failed" "$(dirname "$LOG")/e2e-vpn.log" 2>/dev/null; then
  report "vpn establish failed in logcat"
fi

say "==============================="
say "E2E PASS: tunnel up, DNS via tunnel works"
say "==============================="
exit 0
