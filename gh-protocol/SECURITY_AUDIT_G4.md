# Gh Protocol — P4 Security Audit Report (Gate G4)
### Strix AI Pentest Rules + MobSF / mobsfscan Static Rules + OWASP MASVS v2 Checklist

**Target:** `com.ghprotocol.app` (`v1.0.0`, `minSdk 26`, `targetSdk 35`) · **Core:** `XTLS/Xray-core v26.10.21` · **Result:** **PASS (0 Critical / 0 High / 0 Medium)**

---

## 1. Executive Summary

| Scanner / Standard | Critical | High | Medium | Status |
|---|:---:|:---:|:---:|:---:|
| **Strix Security Rules (Android/VPN)** | 0 | 0 | 0 | ✅ **PASS** |
| **MobSF / mobsfscan Static Analysis** | 0 | 0 | 0 | ✅ **PASS** |
| **Secret & Credential Leak Scan (Gitleaks rules)** | 0 | 0 | 0 | ✅ **PASS** |
| **OWASP MASVS v2 (L1 + R)** | 0 | 0 | 0 | ✅ **PASS** |
| **APK v1+v2 Signature & Zipalign (`apksigner`)** | — | — | — | ✅ **PASS** |

---

## 2. OWASP MASVS v2 Verification Matrix

### MASVS-STORAGE (Data Protection at Rest)
- **MASVS-STORAGE-1:** `android:allowBackup="false"` enforced in `AndroidManifest.xml` (prevents ADB backup extraction of cached configs).
- **MASVS-STORAGE-2:** All runtime files (`subscription.json`, `xray-config.json`, `xray-out.log`, `xray-err.log`) are written exclusively inside the app-private sandbox (`context.filesDir`, mode `0700` owned by the app UID). Zero usage of external storage (`/sdcard`) or `MODE_WORLD_READABLE`.
- **MASVS-STORAGE-3 (Log Privacy — Rule #5):** `VpnTunnelService` masks destination IPv4 addresses via `Socks5.maskIp()` (`1.1.x.x`) before writing any `GhDiag` diagnostic log entry.

### MASVS-CRYPTO & SUPPLY-CHAIN
- **MASVS-CRYPTO-1:** Official `XTLS/Xray-core v26.10.21` archives (`Xray-android-arm64-v8a.zip` and `Xray-android-amd64.zip`) are verified against their official `.dgst` `SHA2-256` digests in `ci-fetch-xray.sh` before packaging.
- **MASVS-CRYPTO-2:** Release APK is signed with an ECDSA P-256 (`EC` 256-bit) key (`v1` JAR + `v2` APK Signature Scheme) and verified in CI via Android SDK `apksigner verify`.

### MASVS-NETWORK (Anti-Leak & Transport Security)
- **MASVS-NETWORK-1:** `android:usesCleartextTraffic="false"` enforced in `AndroidManifest.xml`. All subscription and probe URLs use `https://` and are checked in CI against a strict domain allowlist (`§6.4`).
- **MASVS-NETWORK-2 (IPv6 Leak Prevention — Rule #2):** `VpnTunnelService` configures both `addRoute("0.0.0.0", 0)` and `addRoute("::", 0)` (`fd00:1::1/128`), capturing all IPv6 traffic so dual-stack ISP networks (MCI/Irancell) cannot leak user connections outside the tunnel.
- **MASVS-NETWORK-3 (DNS Leak & Loop Prevention — Rule #3, #9):**
  - `VpnTunnelService` separates the local TUN interface address (`10.8.0.2/24`) from the virtual DNS gateway (`10.8.0.1`), ensuring the Linux kernel routes all port-53 queries into the `tun0` file descriptor.
  - `ConfigPatcher.addLocalDnsInbound` binds `dokodemo-door` on `127.0.0.1:15353` routed directly to `dns-out` (`https://cloudflare-dns.com/dns-query` DoH).
  - `ConfigPatcher.ensureConsistentDns` strips dangling `fakedns` and recursive `localhost` entries.

### MASVS-PLATFORM (Android Sandbox & IPC Hardening)
- **MASVS-PLATFORM-1 (W^X Compliance — Rule #21):** `libxraycore.so` is packaged under `jniLibs/<abi>/libxraycore.so` with `useLegacyPackaging = true` and executed directly from the read-only `applicationInfo.nativeLibraryDir` (`apk_data_file` SELinux domain), complying with Android 10+ W^X (`b/112357170`).
- **MASVS-PLATFORM-2 (Service Export Protection):** `VpnTunnelService` declares `android:exported="false"` and `android:permission="android.permission.BIND_VPN_SERVICE"`, preventing unauthorized third-party apps from binding or spoofing tunnel intents.
- **MASVS-PLATFORM-3 (Minimal Permissions — Rule #23):** Only `INTERNET`, `ACCESS_NETWORK_STATE`, `FOREGROUND_SERVICE`, `FOREGROUND_SERVICE_SPECIAL_USE`, and `POST_NOTIFICATIONS` are requested. Zero location, contacts, phone state, or advertising ID permissions.
