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

/**
 * [weak] marks a probe that only proved *TCP reachability* (the HTTPS request itself failed,
 * e.g. an ISP filter). A weak probe proves the link exists but never proves payload flow, so
 * it can never produce [NetworkState.CONNECTED] on its own.
 */
data class ProbeResult(val url: String, val ok: Boolean, val latencyMs: Long, val weak: Boolean = false)

/** Pure function — unit-tested without any Android dependency. */
fun classify(intl: List<ProbeResult>, domestic: List<ProbeResult>): NetworkState {
    val intlStrong = intl.count { it.ok && !it.weak }
    val intlWeak = intl.count { it.ok && it.weak }
    val domOk = domestic.count { it.ok }
    return when {
        intlStrong >= 2 -> NetworkState.CONNECTED
        intlStrong == 1 -> NetworkState.DEGRADED
        // Only TCP-reachable endpoints: the link exists but no payload was proven.
        intlWeak >= 1 -> NetworkState.DEGRADED
        intlStrong == 0 && domOk >= 1 -> NetworkState.CUTOFF
        else -> NetworkState.OFFLINE
    }
}
