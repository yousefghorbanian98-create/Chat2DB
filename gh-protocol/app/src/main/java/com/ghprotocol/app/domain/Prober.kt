package com.ghprotocol.app.domain

import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.net.HttpURLConnection
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
                conn.setRequestProperty("User-Agent", "GhProtocol/0.1 (connectivity-probe)")
                val code = try {
                    conn.responseCode
                } finally {
                    conn.disconnect()
                }
                ProbeResult(url, ok = code in 200..399, latencyMs = System.currentTimeMillis() - t0)
            } catch (e: Exception) {
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
