package com.ghprotocol.app.net

import com.ghprotocol.app.core.net.RelayConfig
import com.ghprotocol.app.core.net.TunnelSelfTest
import com.ghprotocol.app.core.net.TunnelSelfTestResult
import com.ghprotocol.app.core.net.RelayStats
import com.ghprotocol.app.core.net.TcpRelay
import com.ghprotocol.app.core.net.TunSink
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

/**
 * Proves the "verified" criterion: real remote payload must come back *through the relay*
 * and the relay's own byte counters must move.
 */
class TunnelSelfTestTest {

    private class DiscardingSink : TunSink {
        override fun write(packet: ByteArray): Boolean = true
    }

    private fun relayFor(socksPort: Int): TcpRelay = TcpRelay(
        sink = DiscardingSink(),
        connector = TestNet.standaloneConnector(socksPort),
        config = RelayConfig(
            mss = 1024,
            connectTimeoutMs = 2000,
            connectReplyTimeoutMs = 3000,
            tickerIntervalMs = 25,
            halfCloseGraceMs = 100
        )
    )

    @Test
    fun selfTestPassesOnlyWhenRemotePayloadArrives() {
        val body = "HTTP/1.1 301 Moved Permanently\r\nLocation: https://x/\r\nContent-Length: 0\r\n\r\n"
        TestNet.ReplyServer(body.toByteArray()).use { origin ->
            TestNet.SocksServer().use { socks ->
                val relay = relayFor(socks.port)
                try {
                    val request = "GET /cdn-cgi/trace HTTP/1.1\r\nHost: one.one.one.one\r\n\r\n".toByteArray()
                    val result = TunnelSelfTest(relay).run(
                        targetIp = "127.0.0.1",
                        targetPort = origin.port,
                        request = request,
                        expected = { bytes -> String(bytes).startsWith("HTTP/1.1 301") },
                        timeoutMs = 5000
                    )
                    assertTrue("self-test failed at ${result.stage}: ${result.detail}", result.ok)
                    assertEquals(TunnelSelfTestResult.STAGE_OK, result.stage)
                    assertTrue(result.responseBytes >= body.length)
                    assertEquals(request.size.toLong(), result.upBytesDelta)
                    assertTrue("down bytes must be counted", result.downBytesDelta > 0)
                    assertTrue(result.synAckMs in 0..5000)
                    assertTrue(result.firstByteMs >= 0)
                } finally {
                    relay.shutdown()
                }
            }
        }
    }

    @Test
    fun selfTestFailsFastWhenTheUpstreamIsUnreachable() {
        TestNet.SocksServer(refuseConnect = true).use { socks ->
            val relay = relayFor(socks.port)
            try {
                val result = TunnelSelfTest(relay).run(
                    targetIp = "127.0.0.1",
                    targetPort = 65001,
                    request = "x".toByteArray(),
                    expected = { true },
                    timeoutMs = 3000
                )
                assertFalse(result.ok)
                assertEquals(TunnelSelfTestResult.STAGE_SYN_ACK, result.stage)
                assertEquals(0L, result.downBytesDelta)
            } finally {
                relay.shutdown()
            }
        }
    }

    @Test
    fun selfTestRejectsUnexpectedContent() {
        TestNet.ReplyServer("GARBAGE".toByteArray()).use { origin ->
            TestNet.SocksServer().use { socks ->
                val relay = relayFor(socks.port)
                try {
                    val result = TunnelSelfTest(relay).run(
                        targetIp = "127.0.0.1",
                        targetPort = origin.port,
                        request = "GET / HTTP/1.0\r\n\r\n".toByteArray(),
                        expected = { bytes -> String(bytes).startsWith("HTTP/1.") },
                        timeoutMs = 2000
                    )
                    assertFalse(result.ok)
                    assertEquals(TunnelSelfTestResult.STAGE_CONTENT, result.stage)
                    assertTrue(result.responseBytes > 0)
                } finally {
                    relay.shutdown()
                }
            }
        }
    }

    @Test
    fun selfTestCountersAreVisibleToTheRelayOwner() {
        TestNet.EchoServer().use { echo ->
            TestNet.SocksServer().use { socks ->
                val relay = relayFor(socks.port)
                try {
                    val result = TunnelSelfTest(relay).run(
                        targetIp = "127.0.0.1",
                        targetPort = echo.port,
                        request = "ping-payload".toByteArray(),
                        expected = { String(it) == "ping-payload" },
                        timeoutMs = 4000
                    )
                    assertTrue(result.ok)
                    val stats: RelayStats = relay.stats()
                    assertEquals("ping-payload".length.toLong(), stats.bytesUp)
                    assertEquals("ping-payload".length.toLong(), stats.bytesDown)
                    assertEquals(1L, stats.flowsOpened)
                } finally {
                    relay.shutdown()
                }
            }
        }
    }
}
