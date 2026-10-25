package com.ghprotocol.app.core

import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.net.InetSocketAddress
import java.net.Socket

/**
 * F-17: clean-IP recovery (Nova Radar / Simorgh 2026 pattern).
 * When the default route is dirty (blackholed), scan a pool of well-known
 * Cloudflare egress IPs with a real TCP/TLS ClientHello probe on :443. The
 * cleanest (lowest latency) IP is cached; only the egress address is swapped
 * in the config — SNI/Host/Path stay untouched.
 */
class CleanIpScanner(
    private val pool: List<String> = DEFAULT_POOL,
    private val probeFn: (String, Int) -> Boolean = ::defaultTlsProbe
) {

    companion object {
        /**
         * Well-known Cloudflare Anycast egress IPs (prioritizing `challenges.cloudflare.com`
         * edges `104.18.94.41` / `104.18.95.41` which remain open on Iranian ISPs).
         * Excludes `1.1.1.1` / `1.0.0.1` because port 443 is IP-blocked on Iranian ISPs.
         */
        val DEFAULT_POOL = listOf(
            "104.18.94.41", "104.18.95.41",
            "104.16.132.229", "104.16.133.229",
            "172.64.32.229", "172.64.33.229",
            "104.18.12.149", "104.18.13.149",
            "188.114.96.229", "188.114.97.229",
            "190.93.240.229", "198.41.200.229"
        )

        /**
         * Minimal RFC 5246 TLS 1.2 ClientHello record (51 bytes) advertising standard
         * ECDHE/RSA + TLS 1.3 cipher suites (0xC02F, 0xC02B, 0x009C, 0x1301) so the server
         * responds with a TLS Handshake (0x16) or TLS Alert (0x15) record.
         */
        internal val MINIMAL_CLIENT_HELLO = byteArrayOf(
            0x16, 0x03, 0x01, 0x00, 0x2E, // TLS Handshake record, version 3.1, len 46
            0x01, 0x00, 0x00, 0x2A,       // ClientHello, len 42
            0x03, 0x03,                   // TLS 1.2
            // 32-byte client random
            0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08,
            0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x10,
            0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18,
            0x19, 0x1A, 0x1B, 0x1C, 0x1D, 0x1E, 0x1F, 0x20,
            0x00,                         // session ID len 0
            0x00, 0x08,                   // cipher suites len 8
            0xC0.toByte(), 0x2F.toByte(), // TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256
            0xC0.toByte(), 0x2B.toByte(), // TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256
            0x00, 0x9C.toByte(),          // TLS_RSA_WITH_AES_128_GCM_SHA256
            0x13, 0x01,                   // TLS_AES_128_GCM_SHA256
            0x01, 0x00                    // compression methods: null
        )

        fun defaultTlsProbe(ip: String, timeoutMs: Int): Boolean {
            try {
                Socket().use { s ->
                    s.connect(InetSocketAddress(ip, 443), timeoutMs)
                    s.soTimeout = timeoutMs
                    s.tcpNoDelay = true
                    val out = s.getOutputStream()
                    out.write(MINIMAL_CLIENT_HELLO)
                    out.flush()
                    // TLS record type: 0x16 (Handshake / ServerHello) or 0x15 (Alert from live TLS stack)
                    val b = s.getInputStream().read()
                    if (b == 0x16 || b == 0x15) return true
                }
            } catch (_: Exception) {}
            return try {
                Socket().use { s ->
                    s.connect(InetSocketAddress(ip, 80), timeoutMs)
                    s.soTimeout = timeoutMs
                    s.tcpNoDelay = true
                    val out = s.getOutputStream()
                    out.write("HEAD / HTTP/1.1\r\nHost: challenges.cloudflare.com\r\nConnection: close\r\n\r\n".toByteArray())
                    out.flush()
                    val b = s.getInputStream().read()
                    b == 'H'.code
                }
            } catch (_: Exception) {
                false
            }
        }
    }

    data class ScanResult(val ip: String, val latencyMs: Long)
    data class Report(val best: ScanResult?, val healthy: List<ScanResult>)

    suspend fun scan(timeoutMs: Int = 1500): Report = withContext(Dispatchers.IO) {
        val results = mutableListOf<ScanResult>()
        for (ip in pool) {
            val t0 = System.currentTimeMillis()
            val ok = probeFn(ip, timeoutMs)
            if (ok) results.add(ScanResult(ip, (System.currentTimeMillis() - t0).coerceAtLeast(1L)))
        }
        val best = results.minByOrNull { it.latencyMs }
        Report(best, results.sortedBy { it.latencyMs })
    }

    /** Cache the best clean IP across launches. */
    fun saveBest(ip: String?, context: android.content.Context) {
        context.getSharedPreferences("gh-settings", android.content.Context.MODE_PRIVATE)
            .edit().putString("clean_ip", ip).apply()
    }

    fun loadBest(context: android.content.Context): String? =
        context.getSharedPreferences("gh-settings", android.content.Context.MODE_PRIVATE)
            .getString("clean_ip", null)
}
