# Gh Protocol — Finn-Loop v1.4 Quality Gates & Code Review Standard

This document codifies the updated **Finn-loop v1.4** quality gates, the **25-point security/reliability/quality checklist**, and the **verified CI runner constraints** for `Gh Protocol`.

---

## 1. The 6 Quality Gates

### Gate 1: Build & Packaging
- [x] `assembleDebug` and `assembleRelease` succeed on JDK 17 + Gradle 8.10.2
- [x] Official `XTLS/Xray-core` v26.10.21 binary verified by SHA-256 and packaged in `jniLibs/<abi>/libxraycore.so` (`useLegacyPackaging = true`, W^X compliant)
- [x] Per-ABI APK size <= 25 MB

### Gate 2: Static Analysis & Hygiene
- [x] Zero `!!` non-null assertions in `core/` and `domain/`
- [x] Zero empty `catch` blocks without explicit recovery or comment
- [x] All `Socket`, `DatagramSocket`, `Process`, and `ParcelFileDescriptor` instances cleaned up in `use {}` or `try / finally`

### Gate 3: Unit & Golden Tests
- [x] All JVM + Robolectric unit tests pass (`./gradlew test`)
- [x] 48 Roborazzi RTL Golden Screenshots (12 screens × 2 themes × 2 screen sizes) pass within `0.5%` pixel threshold

### Gate 4: Security & Privacy
- [x] **No Secret Leak:** Zero hardcoded private server IPs, API keys, or tokens
- [x] **IPv6 Leak Prevention:** `VpnService.Builder` routes both `0.0.0.0/0` and `::/0`
- [x] **DNS Leak & Loop Prevention:** All TUN port-53 UDP queries intercepted and relayed via `127.0.0.1:15353` (`dokodemo-door` → `dns-out`), with dangling `fakedns` and recursive `localhost` stripped
- [x] **Traffic Correlation Protection:** Destination IPs masked in `Logcat` diagnostics (`1.1.x.x`)
- [x] **Zero Telemetry:** Only `INTERNET`, `ACCESS_NETWORK_STATE`, `FOREGROUND_SERVICE`, `FOREGROUND_SERVICE_SPECIAL_USE`, and `POST_NOTIFICATIONS` permissions

### Gate 5: Instrumented Emulator E2E (P2b — closes G2)
- [x] KVM-accelerated x86_64 API 34 emulator boots in < 60s
- [x] Debug APK installs and launches (`MainActivity` alive)
- [x] `Xray 26.10.21` starts from `nativeLibraryDir` and listens on `127.0.0.1:10808` (`mixed-in`) and `127.0.0.1:15353` (`dns-in`)
- [x] VPN consent dialog auto-tapped and `VpnTunnelService` establishes `tun0` (`10.8.0.1/8` + `fd00:1::1/128`)
- [x] Bidirectional TCP (`SYN → SYN-ACK`) and DNS traffic verified across the tunnel

### Gate 6: Release & Handoff
- [x] Signed release APK + `SHA256SUMS` published
- [x] `HANDOFF.md` and `PRODUCTION_PLAN.md` synchronized with commit SHA

---

## 2. CI Runner Ground-Truth Rules (Do Not Regress)

1. **PR Trigger Rule:** Workflow triggers on `pull_request` targeting `main` (PR #8). Never restrict `pull_request.branches` to `arena/*` (GitHub filters `pull_request.branches` by base branch, which is `main`).
2. **Root KVM Launch Rule:** Never replace the root-launched emulator in `.github/workflows/gh-protocol-e2e-impl.yml` with `reactivecircus/android-emulator-runner@v2` (the action's non-root `/dev/kvm` check falls back to `-accel off` and times out at 600s).
3. **Diagnostic Channel Rule:** Sandbox cannot read Azure Blob job logs; all build/E2E diagnostics must publish to branch `ci-diag`.
4. **No External Paid API Keys in CI:** Never gate CI on `OPENAI_API_KEY` or external paid bots; self-review against the 25-point checklist runs inside every Finn-loop iteration.
