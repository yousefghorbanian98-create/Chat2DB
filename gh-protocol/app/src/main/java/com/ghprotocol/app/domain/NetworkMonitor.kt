package com.ghprotocol.app.domain

import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

/**
 * F-11: periodic honest network-state detection.
 * Emits [NetworkState] and calls [onLinkRecovered] when international
 * connectivity returns (F-12 hook: instant config re-sync).
 */
class NetworkMonitor(
    private val prober: Prober = HttpProber(),
    private val intervalMs: Long = 15 * 60 * 1000L
) {
    private val _state = MutableStateFlow(NetworkState.UNKNOWN)
    val state: StateFlow<NetworkState> = _state.asStateFlow()

    private var job: Job? = null

    fun start(scope: CoroutineScope, onLinkRecovered: (() -> Unit)? = null) {
        if (job?.isActive == true) return
        job = scope.launch {
            while (true) {
                val prev = _state.value
                val intl = Probes.INTERNATIONAL.map { prober.probe(it, Probes.TIMEOUT_MS) }
                val dom = Probes.DOMESTIC.map { prober.probe(it, Probes.TIMEOUT_MS) }
                val next = classify(intl, dom)
                _state.update { next }
                if (next == NetworkState.CONNECTED || next == NetworkState.DEGRADED) {
                    if (prev == NetworkState.CUTOFF || prev == NetworkState.OFFLINE) {
                        onLinkRecovered?.invoke()
                    }
                }
                delay(intervalMs)
            }
        }
    }

    fun stop() {
        job?.cancel()
        job = null
    }
}
