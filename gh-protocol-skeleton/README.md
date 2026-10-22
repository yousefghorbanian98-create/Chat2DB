# Gh Protocol

**همیشه متصل. — Stay connected.**

Gh Protocol is an open-source Android client for staying connected in restricted
networks. It runs the official **Serverless-for-Iran** subscription on the
official **Xray-core** (XTLS), inside a native `VpnService` tunnel — one tap,
zero config, zero telemetry.

> ## Honest positioning (read this)
> Gh Protocol maximizes your chance of staying connected in **normal, degraded,
> and partially restricted** network conditions. It **cannot** create a
> connection during a **full national internet cutoff** — no client-side
> software can (proven by the 88-day 2026 blackout, where packets were
> discarded at the national gateway's forwarding plane). The app detects this
> state and tells you the truth instead of promising miracles.

## Status

**P0 — skeleton.** CI builds a signed empty APK. Connectivity (F-1..F-3) lands
in P1/P2. No release yet.

## Architecture (target)

```
User tap ──> Compose UI ──> VpnService (TUN)
                          └─> tun2socks ──> Xray-core SOCKS5 :10808
                                            └─> official Serverless-for-Iran config
```

- **Client:** Kotlin 2 + Jetpack Compose + Material 3, RTL-first, Vazirmatn.
- **Core:** official `Xray-core` Android binary (MPL-2.0), version-checked ≥ 26.6.27.
- **Privacy:** zero telemetry, zero analytics, exactly the permissions the
  tunnel needs (`INTERNET`, `VPN`, `NOTIFICATIONS`). No accounts, no cloud.

## Features (roadmap)

| # | Feature | Phase |
|---|---------|-------|
| F-1 | One-tap connect (auto subscription) | P1 |
| F-2 | Xray-core bootstrap (version-checked) | P2 |
| F-3 | VpnService one-tap tunnel | P2 |
| F-6 | Auto config update (12h) + GitHub mirror failover | P2 |
| F-11 | Blackout detection + honest status | P1 |
| F-12 | Offline survival + instant re-sync | P1 |
| F-13 | Pre-blackout preparation | P2 |
| F-14 | Alternative connectivity guide (informational) | P1 |
| F-15 | Protocol adaptation (UDP-drop aware) | P2 |
| F-16 | Import any valid config (serverless / vless:// / trojan://) | P2 |
| F-17 | Clean-IP scanner (dirty-IP recovery) | P2 |
| F-18 | Smart balancer (auto route selection/rotation) | P2 |

## Building

```bash
./gradlew assembleRelease   # needs KEYSTORE_PASS + keystore (CI: GitHub Secrets)
```

Releases are built and signed in GitHub Actions (public repo, unlimited
minutes). SHA-256 checksums are published with every release.

## Security notes

- Fully open source (MIT). The Xray core is the official XTLS build (MPL-2.0).
- The release keystore lives in GitHub Actions Secrets (never in the repo).
- No third-party endpoints other than the official XTLS releases and the
  official Serverless-for-Iran subscription.

## License

MIT (app) + MPL-2.0 (bundled Xray-core binary, per XTLS).
