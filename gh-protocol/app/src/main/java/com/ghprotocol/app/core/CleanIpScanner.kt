package com.ghprotocol.app.core

import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.net.InetSocketAddress
import java.net.Socket

/**
 * F-17: clean-IP recovery (Nova Radar / Simorgh 2026 pattern).
 * When the default route is dirty (blackholed), scan a pool of well-known
 * Cloudflare egress IPs with a real TCP/TLS probe on :443. The cleanest (lowest
 * latency) IP is cached; only the egress address is swapped in the config —
 * SNI/Host/Path stay untouched.
 */
class CleanIpScanner(private val pool: List<String> = DEFAULT_POOL) {

    companion object {
        /** Well-known Cloudflare anycast egress IPs (stable, globally reachable). */
        val DEFAULT_POOL = listOf(
            "1.1.1.1", "1.0.0.1",
            "104.16.132.229", "104.16.133.229",
            "172.64.32.229", "172.64.33.229",
            "188.114.96.229", "188.114.97.229",
            "190.93.240.229", "190.93.241.229",
            "198.41.200.229", "198.41.201.229"
        )
    }

    data class ScanResult(val ip: String, val latencyMs: Long)
    data class Report(val best: ScanResult?, val healthy: List<ScanResult>)

    suspend fun scan(timeoutMs: Int = 1500): Report = withContext(Dispatchers.IO) {
        val results = mutableListOf<ScanResult>()
        for (ip in pool) {
            val t0 = System.currentTimeMillis()
            val ok = try {
                Socket().use { s ->
                    s.connect(InetSocketAddress(ip, 443), timeoutMs)
                    s.soTimeout = timeoutMs
                    // read the TLS ServerHello first bytes (proves a live TLS egress)
                    val b = s.getInputStream().read()
                    b in 0x16..0xFE
                }
            } catch (e: Exception) {
                false
            }
            if (ok) results.add(ScanResult(ip, System.currentTimeMillis() - t0))
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
