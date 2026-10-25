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

### Gate 4a: Data-path truthfulness (v1.6)

- [x] `bytesUp`/`bytesDown`/`activeTcpSessions` are copied from the relay's counters, never
      accumulated per call site, so the UI cannot drift from reality
- [x] `ConnectPhase.CONNECTED` requires a successful in-tunnel self-test; the local handshake
      path can only produce `TUNNELING`
- [x] Clean-IP candidates need a full TLS handshake (system trust store) + complete HTTP response
      + Cloudflare marker; a bare TCP connect or a partial ClientHello is never "healthy"
- [x] UDP that cannot be relayed is counted (`udpDropped`) and answered with ICMP port-unreachable
- [x] 53 hermetic JVM data-path tests (relay, DNS, codec, probes, verifier, self-test)

### Gate 4: Security & Privacy
- [x] **No Secret Leak:** Zero hardcoded private server IPs, API keys, or tokens
- [x] **IPv6 policy is real or honestly reported:** `VpnService.Builder` routes `0.0.0.0/0`; IPv6
      (`fd00:1::2/64` + `::/0`) is added and IPv6 TCP/DNS are relayed through the same datapath.
      When the platform refuses the IPv6 address, the app stores `ipv6=unavailable`, logs it and
      makes **no** leak-prevention claim (v1.6, DIAGNOSIS §D3)
- [x] **DNS Leak & Loop Prevention:** every TUN port-53 query is answered by the app's own
      resolver (DoH over the tunnel's SOCKS5 → DoH Google → TCP DNS → Xray `dns-in`) with a hard
      5 s budget and a real SERVFAIL on failure; responses must match transaction ID *and*
      question; no answer is ever synthesised and AAAA is never special-cased (v1.6, §D1)
- [x] **DoH bootstrap sanity:** `dns.hosts["cloudflare-dns.com"]` is pinned to the name's own
      anycast (`104.16.248.249`), never to `1.1.1.1`/`1.0.0.1` (IP-blocked) and never to an
      unrelated edge or a clean IP (both break TLS SNI)
- [x] **Traffic Correlation Protection:** Destination IPs masked in `Logcat` diagnostics (`1.1.x.x`)
- [x] **Zero Telemetry:** Only `INTERNET`, `ACCESS_NETWORK_STATE`, `FOREGROUND_SERVICE`, `FOREGROUND_SERVICE_SPECIAL_USE`, and `POST_NOTIFICATIONS` permissions

### Gate 5: Instrumented Emulator E2E (P2b — closes G2)
- [x] KVM-accelerated x86_64 API 34 emulator boots in < 60s
- [x] Debug APK installs and launches (`MainActivity` alive)
- [x] `Xray 26.10.21` starts from `nativeLibraryDir` and listens on `127.0.0.1:10808` (`mixed-in`) and `127.0.0.1:15353` (`dns-in`)
- [x] VPN consent dialog auto-tapped and `VpnTunnelService` establishes `tun0` (`10.8.0.1/8` + `fd00:1::1/128`)
- [x] Bidirectional TCP (`SYN → SYN-ACK`) and DNS traffic verified across the tunnel
- [x] **In-tunnel payload self-test** (`relay_self_test` / `relay_selftest=PASS`) carries a real
      remote payload through the live relay; a SOCKS greeting, an open port or a single probe is
      not accepted as proof. The E2E script fails without this line (v1.6, §D5)

### Gate 6: Release & Handoff
- [x] Signed release APK + `SHA256SUMS` published
- [x] `HANDOFF.md` and `PRODUCTION_PLAN.md` synchronized with commit SHA

---

## 2. CI Runner Ground-Truth Rules (Do Not Regress)

1. **PR Trigger Rule:** Workflow triggers on `pull_request` targeting `main` (PR #8). Never restrict `pull_request.branches` to `arena/*` (GitHub filters `pull_request.branches` by base branch, which is `main`).
2. **Root KVM Launch Rule:** Never replace the root-launched emulator in `.github/workflows/gh-protocol-e2e-impl.yml` with `reactivecircus/android-emulator-runner@v2` (the action's non-root `/dev/kvm` check falls back to `-accel off` and times out at 600s).
3. **Diagnostic Channel Rule:** Sandbox cannot read Azure Blob job logs; all build/E2E diagnostics must publish to branch `ci-diag`.
4. **No External Paid API Keys in CI:** Never gate CI on `OPENAI_API_KEY` or external paid bots; self-review against the 25-point checklist runs inside every Finn-loop iteration.
