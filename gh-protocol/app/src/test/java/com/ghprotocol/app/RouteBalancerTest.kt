package com.ghprotocol.app

import com.ghprotocol.app.core.Route
import com.ghprotocol.app.core.RouteBalancer
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Test

class RouteBalancerTest {

    private fun balancer() = RouteBalancer(
        mutableListOf(
            Route("tcp-fragment", 120, true),
            Route("tcp-fragment-tls", 80, true),
            Route("udp-noises", 40, true)
        )
    )

    @Test fun picksLowestLatencyHealthy() {
        val b = balancer()
        b.refreshAll({ name -> when (name) { "udp-noises" -> 40; "tcp-fragment-tls" -> 80; else -> 120 } })
        assertEquals("udp-noises", b.active?.name)
    }

    @Test fun deadActiveRotates() {
        val b = balancer()
        b.refreshAll({ name -> when (name) { "udp-noises" -> 40; else -> if (name == "tcp-fragment-tls") 80 else 120 } })
        assertEquals("udp-noises", b.active?.name)
        val next = b.onRouteDead(b.routes0("udp-noises"))!!
        assertEquals("tcp-fragment-tls", next.name)
    }

    @Test fun udpDegradedPrefersTcp() {
        val b = balancer()
        b.refreshAll({ name -> when (name) { "udp-noises" -> 40; else -> if (name == "tcp-fragment-tls") 80 else 120 } })
        b.udpDegraded(udpOk = false)
        assertEquals("tcp-fragment-tls", b.active?.name)
        assertFalse(b.routes0("udp-noises").healthy)
    }

    @Test fun allDeadNoActive() {
        val b = RouteBalancer(mutableListOf(Route("tcp-fragment")))
        b.refreshAll({ -1 })
        assertNull(b.active)
    }
}

private fun RouteBalancer.routes0(name: String): Route = routes.first { it.name == name }
