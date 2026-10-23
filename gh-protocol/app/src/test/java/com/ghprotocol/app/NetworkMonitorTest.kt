package com.ghprotocol.app

import com.ghprotocol.app.domain.NetworkMonitor
import com.ghprotocol.app.domain.NetworkState
import com.ghprotocol.app.domain.ProbeResult
import com.ghprotocol.app.domain.Probes
import com.ghprotocol.app.domain.Prober
import kotlinx.coroutines.test.runTest
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

class FakeProber(var intlOk: Int, var domOk: Int) : Prober {
    override suspend fun probe(url: String, timeoutMs: Int): ProbeResult {
        val isDom = Probes.DOMESTIC.contains(url)
        val need = if (isDom) domOk else intlOk
        val idx = if (isDom) Probes.DOMESTIC.indexOf(url) else Probes.INTERNATIONAL.indexOf(url)
        return ProbeResult(url, ok = idx < need, latencyMs = if (idx < need) 50 else -1)
    }
}

class NetworkMonitorTest {
    @Test
    fun cutoffThenRecoveryFiresHook() = runTest {
        val fake = FakeProber(intlOk = 0, domOk = 1) // CUTOFF
        val monitor = NetworkMonitor(prober = fake, intervalMs = 1000)
        var recovered = false
        monitor.start(backgroundScope) { recovered = true }

        repeat(4) {
            advanceTimeBy(1000)
            if (monitor.state.value != NetworkState.UNKNOWN) return@repeat
        }
        assertEquals(NetworkState.CUTOFF, monitor.state.value)
        assertFalse(recovered)

        fake.intlOk = 2 // connectivity restored
        repeat(4) {
            advanceTimeBy(1000)
            if (recovered) return@repeat
        }
        assertEquals(NetworkState.CONNECTED, monitor.state.value)
        assertTrue(recovered)
        monitor.stop()
    }
}
