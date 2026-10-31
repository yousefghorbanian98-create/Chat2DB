package com.ghprotocol.app

import com.ghprotocol.app.core.CleanIpScanner
import com.ghprotocol.app.domain.Subscription
import com.ghprotocol.app.domain.SubscriptionParser
import kotlinx.coroutines.test.runTest
import org.junit.Assert.assertEquals
import org.junit.Assert.assertNotNull
import org.junit.Assert.assertTrue
import org.junit.Test

class SubscriptionParserTest {
    private val sample = """
    [
      {
        "remarks": "Serverless-v52-fragA",
        "version": {"min": "26.6.27"},
        "inbounds": [{"tag": "mixed-in", "port": 10808, "protocol": "mixed"}],
        "outbounds": [
          {"tag": "block"},
          {"tag": "tcp-fragment"},
          {"tag": "tcp-fragment-tls"},
          {"tag": "udp-noises"},
          {"tag": "dns"}
        ]
      },
      {
        "remarks": "Serverless-v52-fragB",
        "version": {"min": "26.6.27"},
        "inbounds": [{"tag": "mixed-in", "port": 10808, "protocol": "mixed"}],
        "outbounds": [{"tag": "tcp-fragment"}]
      }
    ]
    """.trimIndent()

    @Test fun parsesTwoEntries() {
        val info = SubscriptionParser.parse(sample)
        assertEquals(2, info.entries.size)
        assertEquals("Serverless-v52-fragA", info.entries[0].remarks)
        assertEquals("26.6.27", info.entries[0].minCoreVersion)
        assertEquals(10808, info.entries[0].inboundPort)
        assertTrue(info.entries[0].features.containsAll(listOf("fragment", "fragment-tls", "noises")))
        assertEquals(listOf("fragment"), info.entries[1].features)
    }

    @Test fun embeddedFallbackConfigIsValid() {
        val info = SubscriptionParser.parse(Subscription.EMBEDDED_FALLBACK_JSON)
        assertEquals(2, info.entries.size)
        assertEquals(10808, info.entries[0].inboundPort)
        assertEquals("26.6.27", info.entries[0].minCoreVersion)
    }

    @Test fun cleanIpScannerPicksFastestHealthy() = runTest {
        val probe = object : com.ghprotocol.app.core.net.IpProbe {
            override fun probe(ip: String): com.ghprotocol.app.core.net.IpProbeResult =
                if (ip == "104.16.132.229") {
                    // Bare TCP works but TLS does not: must never be reported as healthy.
                    com.ghprotocol.app.core.net.IpProbeResult(
                        ip, false, com.ghprotocol.app.core.net.IpProbeResult.STAGE_TLS, "tls_failed", 12
                    )
                } else {
                    com.ghprotocol.app.core.net.IpProbeResult(
                        ip, true, com.ghprotocol.app.core.net.IpProbeResult.STAGE_OK, "headers_ok",
                        30, httpStatus = 200, cloudflareEdge = true
                    )
                }
        }
        val scanner = CleanIpScanner(
            pool = listOf("104.16.132.229", "1.1.1.1", "198.41.200.229", "10.0.0.1"),
            probe = probe
        )
        val report = scanner.scan()
        assertEquals(2, report.healthy.size)
        assertNotNull(report.best)
        // 10.0.0.1 is private and is rejected before any probe runs.
        assertEquals(3, report.examined)
    }
}
