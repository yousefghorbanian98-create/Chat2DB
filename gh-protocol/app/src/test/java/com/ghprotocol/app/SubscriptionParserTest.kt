package com.ghprotocol.app

import com.ghprotocol.app.domain.SubscriptionParser
import org.junit.Assert.assertEquals
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
}
