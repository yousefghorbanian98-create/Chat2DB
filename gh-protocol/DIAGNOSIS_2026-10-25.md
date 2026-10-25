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

53 hermetic JVM tests (loopback only, no external network):

| suite | what it proves |
|---|---|
| `TcpRelayIntegrationTest` (8) | SYN→SYN-ACK→payload→response, multi-segment, IPv6 flow, checksums, retransmit, idle timeout, both close directions, counters == real bytes |
| `DnsResolverTest` (11) | DoH over TLS handshake + HTTP exchange, transaction/question validation, budget enforcement, cache TTL, real SERVFAIL, **no synthesised AAAA** |
| `DnsMessageTest` (7) | RFC 1035 parse/validate, SERVFAIL/TC construction |
| `PacketCodecTest` (9) | IPv4/IPv6 TCP/UDP checksums, sequence wrap, MAS options, fragment rejection |
| `CleanIpProbeTest` (6) | only full TLS+HTTP+CF marker is healthy; private/invalid IPs never probed |
| `TunnelSelfTestTest` (4) | self-test needs real payload and moves the relay's counters |
| `TunnelVerifierTest` (6) | stages, bare-connect is not success, `combine` requires tunnel payload |

## 6. What still requires the phone (cannot be substituted by CI)

Run the build, connect with `fragB` + `CleanIP=auto`, then:

```
adb logcat -c && adb logcat -s GhDiag GhVpnTunnel > gh.log
# connect, open a browser page, then:
grep -E "relay_selftest|dns_reply|dns_failed|flow_open|flow_closed|tun v" gh.log
```

Required evidence for "it works":

1. `relay_selftest=PASS … down=<n>` with `n > 0` (also `responseBytes>0`) — real payload through
   the relay, not a handshake.
2. `dns_reply … path=doh:cloudflare-dns.com ...` (or `doh:google` / `tcp:…`) for the app's own
   queries — i.e. DNS working for real apps, and no repeating `context deadline exceeded`.
3. `flow_open` / `flow_closed … up=<n> down=<m>` pairs whose sum equals the Up/Down counters.

If `relay_selftest` fails, the log now names the stage (`syn_ack`, `payload`, `content`,
`checksum`) and the target; if DNS fails it lists every attempted path with its error.
