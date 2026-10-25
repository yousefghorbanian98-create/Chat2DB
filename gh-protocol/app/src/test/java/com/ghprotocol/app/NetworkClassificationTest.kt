package com.ghprotocol.app

import com.ghprotocol.app.domain.NetworkState
import com.ghprotocol.app.domain.ProbeResult
import com.ghprotocol.app.domain.classify
import org.junit.Assert.assertEquals
import org.junit.Test

class NetworkClassificationTest {
    private fun ok(n: Int) = (0 until n).map { ProbeResult("u$it", true, 100) }
    private fun fail(n: Int) = (0 until n).map { ProbeResult("u$it", false, -1) }

    @Test fun allIntlOkConnected() =
        assertEquals(NetworkState.CONNECTED, classify(ok(3), ok(1)))

    @Test fun twoIntlOkConnected() =
        assertEquals(NetworkState.CONNECTED, classify(ok(2) + fail(1), ok(1)))

    @Test fun oneIntlOkDegraded() =
        assertEquals(NetworkState.DEGRADED, classify(ok(1) + fail(2), ok(2)))

    @Test fun zeroIntlDomesticUpCutoff() =
        assertEquals(NetworkState.CUTOFF, classify(fail(3), ok(1)))

    @Test fun allDownOffline() =
        assertEquals(NetworkState.OFFLINE, classify(fail(3), fail(2)))

    /** A bare TCP connect proves the link, never the payload: degraded at best. */
    @Test fun tcpOnlySuccessIsNeverConnected() =
        assertEquals(
            NetworkState.DEGRADED,
            classify(
                listOf(ProbeResult("u0", true, 40, weak = true), ProbeResult("u1", true, 40, weak = true), fail(1).first()),
                ok(1)
            )
        )

    @Test fun strongPlusWeakStillNeedsTwoStrongForConnected() =
        assertEquals(
            NetworkState.DEGRADED,
            classify(listOf(ProbeResult("u0", true, 40), ProbeResult("u1", true, 40, weak = true), fail(1).first()), fail(2))
        )
}
