package com.ghprotocol.app.domain

/**
 * Honest network state (F-11). Classification is deliberately conservative:
 * - CONNECTED: >=2 of 3 international probes succeed
 * - DEGRADED:  exactly 1 international probe succeeds (throttling / partial)
 * - CUTOFF:    international down but domestic net up (national gateway cut —
 *              the 2026 blackout regime; no client-side tool can help)
 * - OFFLINE:   everything down (device has no network at all)
 */
enum class NetworkState {
    UNKNOWN, CONNECTED, DEGRADED, CUTOFF, OFFLINE
}

data class ProbeResult(val url: String, val ok: Boolean, val latencyMs: Long)

/** Pure function — unit-tested without any Android dependency. */
fun classify(intl: List<ProbeResult>, domestic: List<ProbeResult>): NetworkState {
    val intlOk = intl.count { it.ok }
    val domOk = domestic.count { it.ok }
    return when {
        intlOk >= 2 -> NetworkState.CONNECTED
        intlOk == 1 -> NetworkState.DEGRADED
        intlOk == 0 && domOk >= 1 -> NetworkState.CUTOFF
        else -> NetworkState.OFFLINE
    }
}
