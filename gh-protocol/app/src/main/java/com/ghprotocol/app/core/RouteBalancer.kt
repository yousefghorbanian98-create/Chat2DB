package com.ghprotocol.app.core

import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import kotlin.math.min

/**
 * F-18: smart route balancer.
 * Routes = the config's masked direct paths (tcp-fragment / tcp-fragment-tls /
 * udp-noises) or the subscription entries (fragA/fragB).
 * - pickBest: lowest latency among healthy
 * - health refresh: every [refreshMs] (15 min default)
 * - onRouteDead: auto-rotate to next healthy
 */
data class Route(
    val name: String,
    var latencyMs: Long = -1,
    var healthy: Boolean = false,
    var lastChecked: Long = 0L
) {
    fun ageMs(now: Long) = now - lastChecked
}

class RouteBalancer(private val all: MutableList<Route>) {

    val routes: List<Route> get() = all

    var active: Route? = null
        private set

    private var refreshJob: Job? = null

    /** Ping all routes (3x, take best) and pick the lowest-latency healthy one. */
    fun refreshAll(ping: (String) -> Long, now: Long = System.currentTimeMillis()) {
        for (r in all) {
            var best = -1L
            repeat(3) {
                val t = ping(r.name)
                if (t >= 0) best = if (best < 0) t else min(best, t)
            }
            r.latencyMs = best
            r.healthy = best >= 0
            r.lastChecked = now
        }
        pickBest()
    }

    fun pickBest() {
        active = all.filter { it.healthy }.minByOrNull { it.latencyMs }
    }

    /** F-18: the active route died — rotate to the next healthy one. */
    fun onRouteDead(dead: Route, now: Long = System.currentTimeMillis()): Route? {
        dead.healthy = false
        dead.lastChecked = now
        active = all
            .filter { it.healthy && it !== active }
            .minByOrNull { it.latencyMs }
        return active
    }

    /** F-15 support: UDP routes degraded — prefer TCP-first ordering. */
    fun udpDegraded(udpOk: Boolean) {
        if (!udpOk) {
            all.filter { it.name.startsWith("udp-") }.forEach { it.healthy = false }
            pickBest()
        }
    }

    fun startRefresh(scope: CoroutineScope, ping: (String) -> Long, refreshMs: Long = 15 * 60 * 1000L) {
        if (refreshJob?.isActive == true) return
        refreshJob = scope.launch {
            while (true) {
                refreshAll(ping)
                delay(refreshMs)
            }
        }
    }

    fun stopRefresh() {
        refreshJob?.cancel()
        refreshJob = null
    }
}
