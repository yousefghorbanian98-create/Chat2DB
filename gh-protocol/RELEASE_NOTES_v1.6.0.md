# Gh Protocol 1.6.0 (Android)

`versionCode 6` · built from `main` by the `gh-protocol-build` workflow after the full test
suite and the quality gates went green.

## What changed in this release

### The data path is real, and it is measured
- **New relay core** (`core/net/`): the TUN read loop parses every IPv4/IPv6 packet, terminates
  TCP in user space (`TcpRelay`), and forwards through Xray's SOCKS5 inbound. SYN-ACK is only
  sent after the upstream SOCKS5 connect succeeded, so a dead upstream produces a RST instead of
  a black hole.
- **"Connected" now means payload.** `CONNECTED` and `Verified` are set only after the in-tunnel
  self-test received **real remote bytes** through the same relay the apps use. A local SOCKS
  handshake or a single HTTP probe no longer counts.
- **Up / Down / ActiveTCP are application traffic only.** The self-test's own bytes are reported
  separately (`probeUp` / `probeDown`); previously they were mixed into the user-visible totals.
- **5-second datapath heartbeat** (`adb logcat -s GhDiag:D`, lines starting with `stats t=`):
  packets / tcp / dns53 / activeTcp / flowsOpened / connectFailures / retransmits / appUp /
  appDown / dnsOk / dnsFail / state / ipv6. If nothing enters the tunnel it says so
  (`no_app_packets`), which is the measured answer for "ActiveTCP = 0".

### DNS
- **`cloudflare-dns.com` is no longer a dead end.** `dns.hosts` is pinned to the name's own
  anycast address (`104.16.248.249`) instead of an unrelated edge or the IP-blocked
  `1.1.1.1`/`1.0.0.1`.
- **Five path DNS chain**, each bounded and each validated (transaction id + question + rcode):
  DoH Cloudflare → DoH Google → TCP 8.8.8.8 → TCP 1.1.1.1 → Xray `dns-in:15353`. When every
  path fails the app returns a **real SERVFAIL** for that transaction — it never fabricates an
  answer and never special-cases AAAA.
- The **effective DNS plan of both embedded profiles** is logged at connect time
  (`effective_dns … doh=… dohIps=… dohOutbound=…`).

### IPv6
- Measured in three states: `unavailable` (platform refused the route — no leak claim),
  `route_only` (tunnelled, but no v6 payload proven) and `verified` (a v6 flow received real
  remote bytes). When v6 egress is proven absent, new v6 flows are reset immediately
  (`ipv6_no_egress`) instead of hanging for five minutes while apps wait in Happy Eyeballs.

### Clean-IP scanner
- A candidate is "healthy" only after a full TLS handshake with certificate validation, a
  complete HTTP response **and** a Cloudflare marker (`cf-ray` / `Server: Cloudflare`). A bare
  TCP connect — or the 51-byte truncated ClientHello of the previous version — is never accepted.
  Pool entries must be real public unicast IPv4 literals.

### Fixes found on a device (emulator E2E)
- Self-test no longer collides with its own previous flow (rotating source port).
- Android Private DNS dialling the tunnel's own gateway (`10.8.0.1:853`, `fd00:1::1:853`) is
  now reset locally instead of being sent to SOCKS (`upstream_eof` before).
- The IPv6 self-test builds v6 packets with a v6 source and compares canonical addresses.

### Diagnostics
- Flow logs carry the masked peer and the address family (`flow_open v6 dst=…`, `flow_closed
  dst=… reason=… up=… down=… probe=…`), plus one-time warnings for `flow_rejected`.

## Verification for this build
- 129 unit/integration test cases (59 hermetic data-path tests locally + the Android suites) on
  the CI runner, plus the quality gates (dependency freeze, `https://` whitelist, null-safety,
  secret scan, APK size).
- Emulator E2E with a real `VpnService`: tunnel established, DoH answers received, in-tunnel
  payload self-test green, and application bytes counted (`appUp > 0`).

## Install
1. Download `GhProtocol-v1.6.0-arm64-v8a.apk` (the `universal` file is a fallback).
2. If the previous install was signed with a different key, uninstall it first — otherwise
   Android reports `App not installed`.
3. Verify the download if you want: `sha256sum -c SHA256SUMS`.

## Known limitations (no claim is made beyond these)
- QUIC/HTTP-3 is not relayed: non-DNS UDP is counted and answered with ICMP port-unreachable so
  apps fall back to TCP. ICMP echo (`ping`) inside the tunnel is not relayed.
- Android's Private DNS (DoT, port 853) is not terminated by the app; it is reset locally so the
  system falls back to UDP 53, which the app's resolver answers.
- IPv6 payload depends on the underlying network having IPv6 egress (Xray dials outside the
  tunnel); the app reports `route_only` in that case and claims nothing more.
- Carrier-level confirmation (whether a specific Iranian ISP passes the fragmented TLS outbound)
  requires an on-device `adb logcat` capture — see `FINAL_REPORT_2026-10-26.md` §6.
