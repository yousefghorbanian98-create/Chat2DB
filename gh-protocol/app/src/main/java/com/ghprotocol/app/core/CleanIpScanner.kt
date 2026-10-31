package com.ghprotocol.app.core

import com.ghprotocol.app.core.net.CleanIpPool
import com.ghprotocol.app.core.net.IpProbe
import com.ghprotocol.app.core.net.IpProbeResult
import com.ghprotocol.app.core.net.TlsHttpProbe
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.async
import kotlinx.coroutines.coroutineScope
import kotlinx.coroutines.withContext

/**
 * F-17: clean-IP recovery, judged only on real evidence.
 *
 * A candidate survives only when, in this order:
 *  1. it is a *valid* public unicast IPv4 literal ([CleanIpPool]),
 *  2. a full TLS handshake completes against a trusted certificate,
 *  3. a complete HTTP/1.x response arrives,
 *  4. the peer proves it is a Cloudflare edge (`cf-ray` / `Server: Cloudflare`).
 *
 * A bare TCP connect — or the 51-byte partial ClientHello this class used before v1.6 —
 * is never reported as healthy (see DIAGNOSIS 2026-10-25, D4).
 */
class CleanIpScanner(
    private val pool: List<String> = CleanIpPool.CLOUDFLARE_EDGES,
    private val probe: IpProbe = TlsHttpProbe(),
    private val concurrency: Int = 6,
    /** Hard cap for the whole scan; results collected so far are still returned. */
    private val scanBudgetMs: Long = 8000
) {

    companion object {
        val DEFAULT_POOL: List<String> = CleanIpPool.CLOUDFLARE_EDGES
    }

    data class ScanResult(val ip: String, val latencyMs: Long)

    data class Report(
        val best: ScanResult?,
        val healthy: List<ScanResult>,
        val rejected: List<String> = emptyList(),
        val examined: Int = 0
    )

    /** Full per-IP outcome, for logs and the diagnostics screen. */
    data class DetailedReport(val results: List<IpProbeResult>) {
        val healthy: List<IpProbeResult> get() = results.filter { it.ok }
        val best: IpProbeResult? get() = healthy.minByOrNull { it.latencyMs }

        fun summary(): String = results.joinToString(", ") {
            "${it.ip}:" + if (it.ok) "ok(${it.latencyMs}ms)" else "${it.stage}(${it.detail.take(40)})"
        }
    }

    suspend fun scanDetailed(): DetailedReport = coroutineScope {
        val started = System.currentTimeMillis()
        val candidates = pool.distinct()
        val rejected = candidates.filterNot { CleanIpPool.isValid(it) }
        val valid = candidates.filter { CleanIpPool.isValid(it) }
        if (rejected.isNotEmpty()) {
            TunnelLogBuffer.log(
                LogLevel.WARN, LogCategory.PROBE,
                "چند ورودی غیرمعتبر در فهرست IP تمیز رد شد",
                "cleanIp pool rejected=${rejected.joinToString(",")}"
            )
        }
        val results = ArrayList<IpProbeResult>(valid.size)
        for (chunk in valid.chunked(concurrency.coerceAtLeast(1))) {
            if (System.currentTimeMillis() - started > scanBudgetMs) break
            val running = chunk.map { ip -> async(Dispatchers.IO) { probe.probe(ip) } }
            running.forEach { results.add(it.await()) }
            if (results.any { it.ok }) break // one verified edge is enough
        }
        DetailedReport(results)
    }

    suspend fun scan(): Report = withContext(Dispatchers.IO) {
        val detailed = scanDetailed()
        val healthy = detailed.healthy.sortedBy { it.latencyMs }.map { ScanResult(it.ip, it.latencyMs) }
        Report(
            best = healthy.firstOrNull(),
            healthy = healthy,
            rejected = detailed.results.filterNot { it.ok }.map { "${it.ip}:${it.stage}" },
            examined = detailed.results.size
        )
    }
}
