package com.ghprotocol.app.domain

import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.net.HttpURLConnection
import java.net.InetSocketAddress
import java.net.Socket
import java.net.URL

interface Prober {
    suspend fun probe(url: String, timeoutMs: Int): ProbeResult
}

/** Real probe: plain HttpURLConnection (zero extra deps), runs on IO. */
class HttpProber : Prober {
    override suspend fun probe(url: String, timeoutMs: Int): ProbeResult =
        withContext(Dispatchers.IO) {
            val t0 = System.currentTimeMillis()
            try {
                val conn = URL(url).openConnection() as HttpURLConnection
                conn.connectTimeout = timeoutMs
                conn.readTimeout = timeoutMs
                conn.instanceFollowRedirects = true
                conn.requestMethod = "GET"
                conn.setRequestProperty("User-Agent", "GhProtocol/1.3 (connectivity-probe)")
                val code = try {
                    conn.responseCode
                } finally {
                    conn.disconnect()
                }
                if (code in 200..399) {
                    return@withContext ProbeResult(url, ok = true, latencyMs = System.currentTimeMillis() - t0)
                }
            } catch (_: Exception) {
                // Fall through to fast TCP liveness check below
            }
            // Fallback TCP reachability check so ISP HTTPS filtering on mci.ir/iplc.ir
            // does not falsely classify an online phone as NetworkState.OFFLINE.
            val tcpTarget = when {
                url.contains("mci.ir") || url.contains("iplc.ir") -> Pair("8.8.8.8", 53)
                url.contains("cloudflare") || url.contains("1.1.1.1") -> Pair("104.18.12.149", 80)
                else -> Pair("8.8.8.8", 53)
            }
            try {
                Socket().use { s ->
                    s.connect(InetSocketAddress(tcpTarget.first, tcpTarget.second), timeoutMs.coerceAtMost(2000))
                }
                ProbeResult(url, ok = true, latencyMs = (System.currentTimeMillis() - t0).coerceAtLeast(1L))
            } catch (_: Exception) {
                ProbeResult(url, ok = false, latencyMs = -1)
            }
        }
}

/** Default probe sets. International trio + domestic liveness (works in the
 *  national-intranet regime, e.g. during a full international cutoff). */
object Probes {
    const val TIMEOUT_MS = 3000
    val INTERNATIONAL = listOf(
        "https://www.google.com/generate_204",
        "https://1.1.1.1/cdn-cgi/trace",
        "https://github.com"
    )
    val DOMESTIC = listOf(
        "https://www.mci.ir",
        "https://www.iplc.ir"
    )
}
