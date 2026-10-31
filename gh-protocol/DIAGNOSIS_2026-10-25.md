# DIAGNOSIS — 2026-10-25 (v1.6)

Scope: the device report for profile **`Serverless-v52-fragB`** with `CleanIP=auto`

```
Xray on 127.0.0.1:10808 · DNS on :15353 · tun0 up
TunnelVerifier: one small HTTP request to 1.1.1.1:80 → 301 (255 ms)
telemetry afterwards: Up=3.4 KB  Down=256 B  ActiveTCP=0  DNS=4
repeating: app/dns: failed to retrieve response … Post "https://cloudflare-dns.com/dns-query":
           context deadline exceeded
```

Every claim below is labelled **[proven]** (code/config + matching log signature, reproducible in
a test), **[inferred]** (consistent with everything observed but needs the on-device log listed
in §6 to be closed), or **[unproven]** (explicitly not claimed).

---

## D1 — `cloudflare-dns.com` DoH was a dead end  **[proven]**

The upstream subscription (`patterniha/Serverless-for-Iran`, both `fragA` and `fragB`) ships:

```json
"dns": {
  "hosts": { "cloudflare-dns.com": "challenges.cloudflare.com" },
  "servers": [
    { "address": "fakedns" },
    { "tag": "no-filter-dns", "address": "https://cloudflare-dns.com/dns-query", "timeoutMs": 12000 },
    { "tag": "domestic-dns",  "address": "localhost" }
  ]
}
```

and the `fakedns` pool contains `full:challenges.cloudflare.com`.

Two independent dead ends follow:

1. **Hostname → hostname → fake IP.** `hosts` maps the DoH hostname onto another *name*, which
   is in the fake-DNS pool. The DoH dialer therefore resolves `cloudflare-dns.com` to a
   `198.18.x.x` fake address and tries to open TLS to it. Nothing is listening there and the
   connection cannot be recovered, so the request dies on its 12 s `timeoutMs`.
2. **v1.4.0's "fix" hit the other trap.** `ConfigPatcher.ensureConsistentDns()` rewrote the
   mapping only when the existing value was *not* a digit, so `fragA` kept `1.1.1.1` and
   `fragB` kept `1.0.0.1`. `*.1.1.1:443` / `1.0.0.1:443` are IP-blocked on several Iranian ISPs
   (the very reason the upstream used a domain mapping). The dial never completes → the exact
   `context deadline exceeded` line from the report, from `fragB`, which is the profile that
   carries `1.0.0.1`.

Both paths end in the same observable: Xray's DNS module cannot answer, so every app name
lookup stalls for up to 12 s and then fails.

**Fix (v1.6, `ConfigPatcher.enforceReachableDns`)**

* `dns.hosts["cloudflare-dns.com"] = 104.16.248.249` — the name's *own* anycast address, so the
  TLS certificate/zone matches the SNI. `104.16.249.249` is the second A record.
* hostname→hostname mappings under `hosts` are deleted (they are resolution loops).
* `dns.queryStrategy = "UseIPv4"`; Xray DNS `timeoutMs` clamped to 4000 ms.
* `fakedns` and `localhost` DNS servers are removed; `sniffing.routeOnly = true` already keeps
  numeric destinations, so `fakedns` only produced addresses this app's userspace relay cannot
  dial (it connects by numeric IP — a fake IP is unroutable by definition).
* **The app no longer depends on Xray's resolver at all.** `VpnTunnelService` answers every
  port-53 query itself (`DnsResolver`): DoH through the tunnel's own SOCKS5 →
  DoH `dns.google` → DNS over TCP `8.8.8.8`/`1.1.1.1` → Xray `dns-in`, with a hard 5 s budget,
  a 2.5 s cap per path, and a real `SERVFAIL` (same transaction ID and question) when all paths
  fail. A blocked upstream can no longer hang an app.
* The effective plan of **both** profiles is logged at connect time and is unit-tested
  (`ConfigPatcherTest.bothEmbeddedProfilesGetAReachableDohPlan`,
  `cleanIpIsNeverWrittenIntoTheDohHostsMap`).

A clean IP is an *egress* choice; it is never written into `dns.hosts` any more (that is what
produced a certificate/zone mismatch when a clean edge was applied).

## D2 — `ActiveTCP = 0` and "no real app traffic"  **[proven for the counters, inferred for the silence]**

* **[proven]** The v1.4.0 verification path (`TunnelVerifier.verifyThroughSocks5`) dialled
  `127.0.0.1:10808` **directly**. It never entered `tun0`, and the UI's session counter was
  updated around that probe (increment, then the probe's session was removed on completion).
  A completed probe therefore leaves `ActiveTCP = 0` while still moving `Up`/`Down` — exactly
  the reported shape (`Up`/`Down` non-zero, `ActiveTCP=0`).
* **[inferred]** With Xray's DNS dead (D1), app name resolution failed for up to 12 s per query;
  apps issue almost no TCP flows, so the relay had nothing to carry. Everything that did reach
  the relay was dropped for `QUIC/UDP` (v1.4.0 had no UDP path and logged nothing), so browsers
  showed "no internet" without a single byte of evidence in the log.
* **[unproven]** the exact byte attribution of `3.4 KB / 256 B` to the verifier probe. The new
  build answers this with per-flow logs (`flow_open` / `flow_closed … up= down=`), a per-query
  DNS log (`dns_reply path=… bytes=…`) and counters that are *copied* from the relay
  (`RelayStats`) instead of being accumulated at call sites.

**Fix**

* `TcpRelay` owns every counter. `TunnelLogBuffer.setRelayStats()` copies `bytesUp`, `bytesDown`,
  `activeFlows`, `flowsOpened/Closed`, `connectFailures`, `retransmits` and `closeReasons`
  verbatim, so the UI can no longer drift from reality.
* Every flow logs open/established/failed/closed with its reason and byte counts.
* UDP that cannot be relayed is counted (`udpDropped`) **and** answered with ICMP
  port-unreachable (ICMPv6 type 1 code 4 for v6) so QUIC apps fall back to TCP immediately
  instead of waiting on a silent black hole.

## D3 — IPv6 claim was false  **[proven]**

v1.4.0's `VpnService.Builder` added `10.8.0.2/24` and `route 0.0.0.0/0` only, while
`QUALITY_GATES.md` claimed "routes both `0.0.0.0/0` and `::/0`". With no IPv6 address/route in
`tun0`, IPv6 traffic kept using the physical interface — a real leak, not a protected path.

**Fix (deliberate policy, no silent drop)**

* `tun0` gets `fd00:1::2/64` + `route ::/0` + IPv6 DNS.
* IPv6 TCP is relayed for real (`Socks5.connectRequest` emits `ATYP=4`, `PacketCodec` builds
  IPv6 segments with mandatory checksums) — covered by `TcpRelayIntegrationTest` (loopback `::1`).
* IPv6 DNS is answered by the same resolver (`buildUdp` computes the IPv6 UDP checksum).
* Other IPv6 UDP gets ICMPv6 port-unreachable and is counted.
* If the platform refuses the IPv6 address/route, the app stores `ipv6=unavailable`, says so in
  the log *and* on the log screen, and makes no leak-protection claim.

## D4 — Clean-IP scanner accepted unhealthy IPs  **[proven]**

v1.4.0 "probed" candidates with a **51-byte truncated ClientHello** and treated the first bytes
as success; the pool contained `1.1.1.1` (blocked). Dead or filtered edges were saved as "clean".

**Fix** — `TlsHttpProbe`: full TLS handshake against the system trust store, complete HTTP/1.x
response, and a Cloudflare marker (`cf-ray` / `Server: Cloudflare`); pool entries must be public
unicast IPv4 (`CleanIpPool`). Tests: a bare TCP listener and a TLS server without the marker are
rejected (`CleanIpProbeTest`), and a `tcp`-only result is never healthy (`SubscriptionParserTest`).

## D5 — "Connected" was reported before anything was verified  **[proven]**

`HomeScreen` called `viewModel.onVpnEstablished()` right after the consent dialog returned
(before `establish()` and before any probe); `HomeViewModel` then set `ConnectPhase.CONNECTED`
unconditionally and the shield showed "connected".

**Fix** — the phase only becomes `CONNECTED` after `TunnelSelfTest` received a **real remote
payload through the live relay** (`relay_selftest=PASS … down=>0`). A SOCKS greeting, a local
handshake or a single external probe is not enough (`TunnelVerifierTest.combineDemandsTunnelPayload`).
Everything else stays `TUNNELING`/`DEGRADED` with the failing stage in the log.

---

## 5. Verification performed in this change

59 hermetic JVM tests (loopback only, no external network):

| suite | what it proves |
|---|---|
| `TcpRelayIntegrationTest` (12) | SYN→SYN-ACK→payload→response, multi-segment, IPv6 flow, checksums, retransmit, idle timeout, both close directions, counters == real bytes, **self-test bytes never leak into the app counters** |
| `DnsResolverTest` (12) | DoH over TLS handshake + HTTP exchange, transaction/question validation, budget enforcement, cache TTL, real SERVFAIL, **no synthesised AAAA** |
| `DnsMessageTest` (7) | RFC 1035 parse/validate, SERVFAIL/TC construction |
| `PacketCodecTest` (9) | IPv4/IPv6 TCP/UDP checksums, sequence wrap, MAS options, fragment rejection |
| `CleanIpProbeTest` (6) | only full TLS+HTTP+CF marker is healthy; private/invalid IPs never probed |
| `TunnelSelfTestTest` (6) | self-test needs real payload, moves the relay's counters, and two runs back-to-back must both pass (D7) |
| `TunnelVerifierTest` (7) | stages, bare-connect is not success, `combine` requires tunnel payload |

## 6. D6 — the shown `Up/Down/ActiveTCP` included the self-test's own bytes  **[proven]**

`TunnelSelfTest` injects a synthetic flow (`10.8.0.99:41234 → target`) into the **same**
`TcpRelay` instance that carries app traffic, so `RelayStats.bytesUp/bytesDown/flowsOpened`
counted probe bytes. That is why a device with no app traffic could still report
`Up=3.4 KB` while `ActiveTCP=0`: the counter was real, but it was not *application* traffic.

Fix (tested): `RelayConfig.probeSourceIps` marks probe sources, the relay keeps
`probeBytesUp/probeBytesDown/probeFlowsOpened/probeActiveFlows` separately, and the service
publishes `RelayStats.applicationOnly()` to the UI. `TcpRelayIntegrationTest
.selfTestBytesAreReportedApartFromApplicationBytes` asserts that a 9-byte app flow shows up as
`appUp=appDown=9` even after a successful self-test ran through the same relay.

## 7. CI-only unit-test failure (4 tests) — root cause and fix  **[proven by A/B on the runner]**

Runs `40226735052` / `40227146538` / `40227598599` failed on `testDebugUnitTest` /
`testReleaseUnitTest` only, always the same four:
`CleanIpProbeTest.acceptsOnlyTlsHttpWithCloudflareMarker`,
`...rejectsServerWithoutCloudflareMarker`,
`DnsResolverTest.dohTransportCompletesRealTlsHandshakeAndHttpExchange`,
`...dohTransportSurvivesWrongPathAndReportsFailure`, with `http:no_http_response` /
`127.0.0.1:no_http_headers` — while all 18 tests passed locally and even a green
`testDebugUnitTest` run on the runner was followed by a red `testReleaseUnitTest`.

Cause: both in-test TLS servers relied on the *implicit* handshake of
`SSLServerSocket.accept()` (the handshake only happens on the first read from the accepted
socket) and `TlsHttpServer` did a **single** `input.read(buffer)` before answering. On a loaded
runner the accepted socket then answered with nothing.

Fix: the test servers now accept on a plain loopback `ServerSocket`, wrap the accepted socket
with the server-side `SSLSocketFactory`, set `useClientMode=false`, force TLSv1.2, call
`startHandshake()` inside the worker thread, read the request up to the header terminator, write
+ flush the response, and close via `shutdownOutput()` + bounded drain (a close with unread data
would emit RST and discard the response). Each connection records `stage`, `bytesWritten` and
`lastError`, and every assertion prints them.

Evidence: run `40240521661` — 123 tests, 0 failures, release APK produced, on the same runner
that failed the identical test bodies minutes earlier.

## 8. Emulator E2E evidence (2026-10-25, run 40244228075) — what it proved and what it broke

The P2b workflow boots an x86_64 emulator with a **real VpnService**, taps the consent dialog
and runs the whole app. Its log (published to the `ci-diag` branch, `gh-protocol/e2e-log.md`)
is the first end-to-end evidence from an Android device:

```
effective_dns active   fragA :: doh=https://cloudflare-dns.com/dns-query
        dohIps=104.16.248.249 dohOutbound=tcp-fragment-tls notes=doh_bootstrap_zone_ok
tun0 established ipv4=10.8.0.2/24 ipv6=fd00:1::2/64 route=::/0 dns=10.8.0.1 mtu=1500
relay_selftest ok=true stage=ok target=1.1.1.1:80        up=91  down=402 response=402 checksums=0
relay_selftest ok=true stage=ok target=104.16.248.249:80 up=323 down=794 response=794 checksums=0
dns_ok path=doh:cloudflare-dns.com  (15 answered queries, dnsFail=0)
stats t=5s packets=145 tcp=113 dns53=10 otherUdp=12 activeTcp=9 flowsOpened=16
      flowsEstablished=16 connectFailures=0 retransmits=0
      appUp=38575 appDown=30180 probeUp=184 probeDown=1196 probeFlows=2 dnsOk=10 dnsFail=0
      state=VERIFIED ipv6=tunneled
E2E PASS: real tunnel carrying traffic (SUBMODE=live)
```

So **D1 (DoH dead end) is proven fixed on a device**: 15 real DoH answers, zero failures, no
`context deadline exceeded`. **D6 is proven fixed on a device**: `appUp/appDown` carry only
application bytes (38,575 / 30,180 B) while the self-test's share (184 / 1,196 B) is reported
separately — the exact counter confusion of the original bug report.

The same log exposed two defects that no unit test had covered, both now fixed:

## 9. D7 — the self-test collided with its own previous flow  **[proven, regression test]**

```
23:23:25.440  relay_selftest ok=true  target=1.1.1.1:80            (first run passed)
23:23:25.458  selftest 1.1.1.1:80 failed at syn_ack:
              bad_ack_1477468113_expected_1191517255              (second run, 18 ms later)
```

`TunnelSelfTest` used a fixed source port (`10.8.0.99:41234`). A second run against the same
target — the service re-runs the test after every core restart, and the E2E harness nudges one —
hit the previous flow while it was still inside the half-close grace window. The relay correctly
treated the SYN as a retransmit and replayed the **old** SYN-ACK (old ISN), and the new run
rejected a perfectly healthy tunnel. Fix: every run takes a fresh source port from a rotating
range and runs are serialised (`TunnelSelfTest.nextClientPort`, `runLock`).
Regression test: `TunnelSelfTestTest.consecutiveSelfTestsToTheSameTargetBothPass` — it failed
with the exact message above before the fix and passes now.

## 10. D8 — flows to the tunnel's *own* addresses were dialled upstream  **[proven, regression test]**

```
tun v4 proto=6 dst=10.8.x.x:853   ·  flow_open 10.8.x.x:853
tun v6 proto=6 dst=fd00:1:…:853   ·  flow_open fd00:1:…:853
flow_closed reason=upstream_eof up=517 down=0     (both)
```

Android's opportunistic Private DNS dials the VPN's DNS server (our gateway `10.8.0.1` /
`fd00:1::1`) on 853. Our relay forwarded those to SOCKS5, i.e. asked the upstream proxy to
connect to an address that only exists inside our tunnel; the dial ended in EOF after 517 bytes.
Fix: `RelayConfig.localDestinationPrefixes` marks the tunnel subnet (`10.8.0.`, `fd00:1:`); such
flows are answered with a real RST and counted in `RelayStats.localRejects`, and the service logs
`flow_rejected reason=tunnel_local_destination` once. The client fails fast and falls back to
UDP 53, which [DnsResolver] serves.
Regression test: `TcpRelayIntegrationTest.tunnelLocalDestinationsAreResetWithoutUpstreamDial`
(RST, `socks.connections == 0`, `localRejects == 2`, `connectFailures == 0`).

Also fixed for diagnosability: `flow_open`/`flow_closed` now log the **masked destination and
the address family**, and `flow_closed` carries `probe=<bool>`, so a phone log can prove which
peer (v4 or v6) carried which bytes — previously `flow_closed` had no destination at all, so the
`ipv6=tunneled` claim could not be checked from the log.

## 10b. D9 — the IPv6 self-test could not build a packet, and never matched one  **[proven, regression test]**

Making the IPv6 state measurable (see §D3) immediately produced:

```
relay_selftest_v6 ok=false stage=build detail=cannot_build_syn
```

`TunnelSelfTest` always used the IPv4 probe source (`10.8.0.99`), so a family-6 SYN could not
be constructed at all — IPv6 could therefore never be *proven*, only assumed. After giving it a
v6 source inside the tunnel (`fd00:1::99`) the run then failed at `syn_ack: no_syn_ack`,
because the observer compared the target literal (`::1`) with the canonical form the relay
parses out of the packet bytes (`0:0:0:0:0:0:0:1`) — `InetAddress.getHostAddress()` never
compresses `::`. Fix: `PacketCodec.normalizeIp()` and comparisons on canonical forms in both
the observer and the packet builder.
Regression test: `TunnelSelfTestTest.selfTestReachesAnIpv6TargetWithAnIpv6Source` against a
real `::1` server (13 ms, real v6 payload).

The E2E now reports `ipv6=route_only` when v6 payload is not proven and only `ipv6=verified`
after a real v6 round trip, so the phone log can settle this on a network that actually has
IPv6 egress.

### Why the emulator stayed at `route_only` — and the policy that follows

Run `40254223708` reached `relay_selftest_v6 ok=false stage=payload detail=no_response_bytes`:
the SYN-ACK arrived (the v6 packet path, checksums and SOCKS dial all worked) but no payload
came back. Xray is excluded from the tunnel (`addDisallowedApplication`), so it dials with the
**device's own** network — a QEMU NAT without IPv6, and, for most Iranian mobile carriers, no
IPv6 at all. A tunnel cannot create v6 egress that the underlying network does not have.

Consequence (requirement 4, "choose a safe, tested policy"): when the v6 self-test fails at the
payload stage, the service logs
`ipv6_egress_unproven … action=reject_v6_flows_fast` and sets `TcpRelay.rejectIpv6Flows`, so
new v6 flows are reset immediately (`ipv6_no_egress`) instead of hanging for the 5-minute idle
timeout while apps wait in Happy Eyeballs. IPv4 is untouched. The state remains `route_only`
and **no leak-prevention claim** is made.
Regression test: `TcpRelayIntegrationTest.ipv6FlowsAreRejectedFastOnceEgressIsUnproven`.

## 11. Not relayed on purpose (no claim made)

- **ICMP**: `ping` inside the tunnel is dropped (`E2E: 100% packet loss` in the log). The tunnel
  relays TCP and DNS; it does not answer echo requests.
- **QUIC/HTTP-3** (`otherUdp=12` in the sample): counted and answered with a real ICMP
  port-unreachable so apps fall back to TCP.

## 12. What still requires the phone (cannot be substituted by CI)

Run the build, connect with `fragB` + `CleanIP=auto`, then:

```
adb logcat -c && adb logcat -s GhDiag GhVpnTunnel > gh.log
# connect, open a browser page, then:
grep -E "relay_selftest|dns_reply|dns_failed|flow_open|flow_closed|flow_failed|tun v|stats t=|no_app_packets" gh.log
```

Required evidence for "it works":

1. `relay_selftest=PASS … down=<n>` with `n > 0` (also `responseBytes>0`) — real payload through
   the relay, not a handshake.
2. `dns_reply … path=doh:cloudflare-dns.com ...` (or `doh:google` / `tcp:…`) for the app's own
   queries — i.e. DNS working for real apps, and no repeating `context deadline exceeded`.
3. `flow_open` / `flow_closed … up=<n> down=<m>` pairs whose sum equals the Up/Down counters.
4. the 5-second heartbeat `stats t=15s packets=<n> tcp=<n> dns53=<n> activeTcp=<n>
   flowsOpened=<n> appUp=<n> appDown=<n> probeUp=<n> dnsOk=<n> dnsFail=<n> state=<…>`:
   `packets` must grow once an app sends through the tunnel, and `appUp/appDown` must equal the
   sum of the `flow_closed` lines (self-test bytes appear only in `probeUp/probeDown`).
5. if it never works, `no_app_packets after 10s` is the measured answer for `ActiveTCP=0`:
   nothing entered `tun0` (app bypassing the tunnel / VPN not routed for that UID), which is a
   different failure from "packets entered and the relay failed" — the heartbeat separates them.

If `relay_selftest` fails, the log now names the stage (`syn_ack`, `payload`, `content`,
`checksum`) and the target; if DNS fails it lists every attempted path with its error.
