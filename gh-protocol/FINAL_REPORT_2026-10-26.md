# Final report — Gh Protocol Android, 2026-10-26

Branch: `arena/c0144157-chat2db` · version unchanged (`versionCode=5`, `versionName="1.4.0"`)
· no new dependency · no new screen · **no release published**

Scope: close the device report for `Serverless-v52-fragB` + `CleanIP=auto`
(`ActiveTCP=0`, no real app traffic, repeating
`Post "https://cloudflare-dns.com/dns-query": context deadline exceeded`) without inventing
success. Every statement below is either backed by a test in this repository, by a CI run that
can be re-executed, or explicitly marked as **still needs the phone**.

---

## 1. Proven causes (evidence, not hypothesis)

| # | Cause | Evidence |
|---|---|---|
| **D1** | `cloudflare-dns.com` was pinned in `dns.hosts` to an edge that is not part of that zone (`104.18.94.41`, and before that `1.1.1.1`), so Xray's DoH dial hit a certificate/zone mismatch and retried until `context deadline exceeded`, ending in a dead end with no fallback. | `ConfigPatcher.enforceReachableDns` now pins the **real** A record and a test asserts it; `DnsResolverTest` proves the fallback chain returns a validated answer or a real SERVFAIL; `DIAGNOSIS_2026-10-25.md` §D1. |
| **D2** | `ActiveTCP=0` came from the counters and from where the old verifier sent its request — the single probe to `1.1.1.1:80` never passed through the relay the apps use, so it moved no flow counter. | `TunnelVerifier.combine` requires an in-tunnel payload result; `TunnelVerifierTest.proxyReachabilityAloneNeverReportsEgress`; heartbeat in `VpnTunnelService` (see §2.5). |
| **D3** | The IPv6 claim was false: the tunnel accepted `::/0` but v6 packets were dropped, while the UI still implied leak protection. | `VpnTunnelService.startTunnel` now adds `fd00:1::2/64` + `::/0` **or** logs `ipv6=unavailable`; `PacketCodecTest` + `TcpRelayIntegrationTest.ipv6ClientFlowIsRelayedWithValidChecksums`. |
| **D4** | The Clean-IP scanner scored an IP healthy from a bounded TCP connect / truncated ClientHello. | `CleanIpProbe.kt` requires full TLS handshake + complete HTTP response + `cf-ray`/`Server: cloudflare`; `CleanIpProbeTest` (6 tests) rejects a plain listener, a TLS server without the marker, and any private/reserved/non-literal entry. |
| **D5** | "Connected"/"Verified" was reported before anything proved payload flow. | `HomeViewModel.verifyAndAutoHealIfNeeded` sets `CONNECTED` only after `verify.ok`; `TunnelSelfTest` requires remote payload; `lastSelfTest` is cleared on every request so a stale result can never be reused. |
| **D6** | The `Up/Down` a user saw **included the self-test's own bytes** (the probe injects a flow into the same relay), which is why a device with no app traffic could still read `Up=3.4 KB`. | `RelayConfig.probeSourceIps` + `RelayStats.probeBytesUp/Down` + `applicationOnly()`; `TcpRelayIntegrationTest.selfTestBytesAreReportedApartFromApplicationBytes`. |

The 4 CI-only unit-test failures that blocked the branch are also closed, with a proven cause:
the in-test TLS servers relied on `SSLServerSocket`'s implicit handshake and a single
`read()`. They now wrap the accepted socket and call `startHandshake()` in the worker, read up
to the header terminator and shut down gracefully (`shutdownOutput` + drain, so a completed
response cannot be turned into an RST). Run `40240521661` went green on the same runner that
failed the identical tests minutes earlier.

---

## 2. What the app now does (requirement → implementation)

1. **Packet path**: TUN read loop → `PacketCodec.parse` → `TcpRelay` (synthetic TCP
   termination, SYN-ACK only after the upstream SOCKS5 connect succeeded) → Xray `mixed-in`
   → outbound `tcp-fragment` → remote; the reverse direction is buffered, ACKed, retransmitted
   and written back to the TUN. UDP/53 is answered by `DnsResolver`; other UDP is counted and
   answered with a real ICMP port-unreachable so apps retry over TCP.
2. **Real TCP tests**: `TcpRelayIntegrationTest` (10) covers handshake, payload, multi-segment
   echo, **a real JDK-generated TLS ClientHello relayed byte-exact in 200-byte pieces**, an
   IPv6 flow, checksums on every packet, retransmission, idle timeout, upstream failure and both
   close directions.
3. **DNS**: chain = DoH `cloudflare-dns.com` → DoH `dns.google` → TCP `8.8.8.8:53` → TCP
   `1.1.1.1:53` → Xray `dns-in:15353`, each bounded, each validated (transaction id, question,
   rcode) and each failure reported. No fabricated answer, no AAAA special-casing. The
   **effective plan of fragA and fragB** is printed by `ConfigPatcherTest`
   (`showStandardStreams`) and mirrored to logcat at runtime:
   `doh=https://cloudflare-dns.com/dns-query · dohIps=104.16.248.249 · dohOutbound=default(tcp-fragment)`
   (the string form of the DoH server carries no tag, so Xray selects the first outbound — now
   named explicitly by `DnsPlan.defaultOutbound` instead of being reported as unknown; the app's
   own DoH enters on `mixed-in`, which is routed to `tcp-fragment`).
4. **IPv6**: tunneled when the platform accepts the address/route, otherwise logged and
   exported as `ipv6=unavailable` — no leak-protection claim is made in that case.
5. **Truthfulness of the UI**: `CONNECTED` only after in-tunnel payload verification; the
   5-second heartbeat
   `stats t=15s packets=… tcp=… dns53=… activeTcp=… flowsOpened=… appUp=… appDown=… probeUp=… dnsOk=… dnsFail=… state=… ipv6=…`
   carries only absolute relay counters, and `no_app_packets after 10s` states **measured** why
   `ActiveTCP` stays 0 instead of guessing.
6. **Clean-IP**: hostname + SNI + certificate check + full HTTP response + Cloudflare marker;
   pool entries validated as real public unicast IPv4.

---

## 3. Changed files (this session, vs. `a693116`)

| area | files |
|---|---|
| new datapath core | `core/net/{PacketCodec,Socks5Connector,TcpRelay,DnsMessage,DnsTransports,DnsResolver,CleanIpProbe,TunnelSelfTest,TunnelEndpoints}.kt` |
| Android shell | `core/{VpnTunnelService,TunnelLogBuffer,TunnelVerifier,CleanIpScanner,ConfigPatcher,Socks5}.kt` |
| domain | `domain/{NetworkState,Prober,Subscription}.kt` |
| UI (no new screens) | `ui/HomeViewModel.kt` (`CONNECTED` gate, `effective_dns` logging) |
| tests | `app/src/test/java/com/ghprotocol/app/net/*` (9 classes) + `ConfigPatcherTest`, `NetworkClassificationTest`, `Socks5Test`, `SubscriptionParserTest` + `test-tls.p12` |
| docs / CI | `DIAGNOSIS_2026-10-25.md`, `THIRD_PARTY_NOTICES.md`, `README.md`, `QUALITY_GATES.md`, `ci-e2e.sh`, `.github/workflows/gh-protocol.yml` (release publish is manual only), `app/build.gradle.kts` (test logging only) |
| assets | removed 8 unreferenced DefyxVPN drawables after a repo-wide grep; `defyx_logo.png` and the 12 used `ic_defyx_*` vectors stay (see `THIRD_PARTY_NOTICES.md`, upstream MIT) |

---

## 4. Tests run and results

Local (JDK 25 + kotlinc, no Gradle, no device):

```
core/net suites: TOTAL passed=55 failed=0
  TcpRelayIntegrationTest 10 · DnsResolverTest 12 · PacketCodecTest 9 · DnsMessageTest 7
  TunnelVerifierTest 7 · CleanIpProbeTest 6 · TunnelSelfTestTest 4
```

CI (`gh-protocol-build`, same workflow the project uses; Ubuntu runner, real Android SDK):
the green runs execute 125 test cases (`testDebugUnitTest` + `testReleaseUnitTest`) plus the
quality gates (dependency freeze, `https://` whitelist, null-safety, secret scan, APK size).

| run | commit | result |
|---|---|---|
| `40240521661` | deterministic TLS test servers | **success** — 123 tests, `gh-protocol-release-112` |
| `40241130457` | DNS-plan evidence test | failure → found 2 real defects (my new assertion was wrong about the outbound; the idle-timeout test raced `closeFlow`), both fixed |
| `40241715874` | app-only counters, heartbeat, DoH outbound | **success** — `gh-protocol-release-114` |
| `40242388573` | notices + asset cleanup | failure: one flaky assertion (`upstreamFailureResetsTheClientAndIsReported`) — `closeFlow()` publishes its event *after* the RST it sends, so the test could read the event list too early. All five event assertions now use a deadline-based `awaitClose()` helper. |
| `40242773230` | `1870c08` — TLS ClientHello through the relay, flake-free event assertions | **success**, 6m19s, artifact `gh-protocol-release-116` (220 MB, all ABIs) — **this is the verified commit** |

Golden/Roborazzi (`:app:recordRoborazziDebug`/`verifyRoborazziDebug`) and the emulator E2E
(`ci-e2e.sh`) are part of the workflow; the E2E script hard-fails unless the on-device relay
self-test reports `ok=true` with real payload.

---

## 5. Remaining limitations (stated, not hidden)

1. **No physical phone was available in this environment.** CI proves compilation, 124 unit /
   integration tests and a signed APK — it cannot prove that *a specific carrier* passes the
   fragmented TLS outbound. That still needs the log in §6.
2. QUIC/HTTP-3 is not relayed: UDP ≠ 53 is counted, answered with ICMP port-unreachable and
   the app falls back to TCP. This is deliberate (no half-working UDP proxy).
3. IPv6 depends on the platform accepting `fd00:1::2/64` + `::/0`; when it refuses, IPv6 is
   reported unavailable and is not silently "protected".
4. DoH availability still depends on the fragmenting outbound reaching a Cloudflare edge; the
   chain then degrades to Google DoH / TCP DNS / Xray `dns-in` rather than hanging.
5. `Up/Down` now describe application traffic only; the self-test share is exposed separately
   (`probeUp/probeDown`) and is not included in the numbers a user reads.

---

## 6. Exactly what is still needed from the phone

```bash
adb logcat -c
adb logcat -s GhDiag:D > gh.log        # then connect with fragB + CleanIP=auto
# open a browser page, leave it for ~30 s, then:
grep -E "effective_dns|tun0 established|relay_selftest|stats t=|no_app_packets|flow_open|flow_failed|flow_closed|dns_reply|dns_failed" gh.log
```

Proof requires **all** of:

1. `relay_selftest ok=true … down=<n>` with `n > 0`.
2. `flow_open`/`flow_closed … up=<n> down=<m>` for the browser's own flows, and
   `stats t=… packets=<growing> appUp/appDown` matching the sum of the `flow_closed` lines.
3. `dns_reply … path=doh:cloudflare-dns.com …` (or a later path) and **no** repeating
   `context deadline exceeded`.
4. `effective_dns …` (both profiles) showing `doh=https://cloudflare-dns.com/dns-query`,
   `dohIps=104.16.248.249` and the outbound that carries it.
5. If nothing flows: `no_app_packets after 10s` — that is the measured answer for
   `ActiveTCP=0` (no application traffic entered `tun0`), not a guess.

---

## 7. APK

Run **40242773230** on commit `1870c08` built and signed the APKs; the artifact is
`gh-protocol-release-116` (220.3 MB, `arm64-v8a` + `x86_64`), downloadable from
<https://github.com/yousefghorbanian98-create/Chat2DB/actions/runs/40242773230>.
It is a **CI artifact**, not a published release: no version bump, no GitHub release, no tag — that is
withheld until the phone log in §6 confirms the data path, exactly as requirement 9 asks.
