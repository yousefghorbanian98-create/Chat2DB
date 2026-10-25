package com.ghprotocol.app.net

import com.ghprotocol.app.core.net.PacketCodec
import com.ghprotocol.app.core.net.RelayConfig
import com.ghprotocol.app.core.net.RelayEvents
import com.ghprotocol.app.core.net.RelayStats
import com.ghprotocol.app.core.net.TcpRelay
import com.ghprotocol.app.core.net.TunSink
import org.junit.Assert.assertEquals
import org.junit.Assert.assertNotNull
import org.junit.Assert.assertTrue
import org.junit.Test
import java.util.Collections

/**
 * End-to-end tests of the *real* relay code against a *real* loopback SOCKS5 server and real
 * TCP servers: handshake, payload, multi-segment forwarding, ACK/sequence/checksum
 * correctness, upstream failure, timeouts and both close directions.
 */
class TcpRelayIntegrationTest {

    private val clientIp = "10.8.0.2"
    private val clientPort = 40000

    private class RecordingSink : TunSink {
        val packets: MutableList<ByteArray> = Collections.synchronizedList(ArrayList())
        override fun write(packet: ByteArray): Boolean {
            packets.add(packet)
            return true
        }

        fun flows(): List<PacketCodec.IpFlow> = synchronized(packets) {
            packets.mapNotNull { PacketCodec.parse(it) }
        }

        fun toClient(): List<PacketCodec.IpFlow> = flows().filter { it.dstPort == 40000 }

        fun await(timeoutMs: Long = 4000, predicate: (PacketCodec.IpFlow) -> Boolean): PacketCodec.IpFlow? {
            val deadline = System.currentTimeMillis() + timeoutMs
            while (System.currentTimeMillis() < deadline) {
                toClient().lastOrNull(predicate)?.let { return it }
                Thread.sleep(5)
            }
            return null
        }
    }

    private class Events : RelayEvents {
        val closed = Collections.synchronizedList(ArrayList<String>())
        val failed = Collections.synchronizedList(ArrayList<String>())
        val warnings = Collections.synchronizedList(ArrayList<String>())
        @Volatile var lastStats: RelayStats? = null

        override fun onFlowClosed(key: String, reason: String, upBytes: Long, downBytes: Long, durationMs: Long) {
            closed.add(reason)
        }

        override fun onFlowFailed(key: String, stage: String, detail: String) {
            failed.add("$stage:$detail")
        }

        override fun onWarning(stage: String, detail: String) {
            warnings.add(stage)
        }

        override fun onStats(stats: RelayStats) {
            lastStats = stats
        }
    }

    private fun config(
        idleTimeoutMs: Long = 300_000,
        retransmitIntervalMs: Long = 400,
        maxRetransmits: Int = 6,
        halfCloseGraceMs: Long = 200
    ) = RelayConfig(
        mss = 512,
        connectTimeoutMs = 2000,
        connectReplyTimeoutMs = 3000,
        idleTimeoutMs = idleTimeoutMs,
        retransmitIntervalMs = retransmitIntervalMs,
        maxRetransmits = maxRetransmits,
        halfCloseGraceMs = halfCloseGraceMs,
        tickerIntervalMs = 25
    )

    @Test
    fun handshakePayloadAndCountersMatchRealBytes() {
        TestNet.ReplyServer("HTTP/1.1 200 OK\r\nContent-Length: 2\r\n\r\nok".toByteArray()).use { origin ->
            TestNet.SocksServer().use { socks ->
                val sink = RecordingSink()
                val events = Events()
                val relay = TcpRelay(sink, TestNet.connectorFor(socks), events, config())
                try {
                    val request = "GET /probe HTTP/1.0\r\nHost: test\r\n\r\n".toByteArray()
                    val isn = 1000L
                    relay.onPacket(TestNet.clientPacket(4, clientIp, clientPort, "127.0.0.1", origin.port, isn, 0, PacketCodec.FLAG_SYN))

                    val synAck = sink.await { it.isSyn && it.isAck }
                    assertNotNull("no SYN-ACK from relay", synAck)
                    assertTrue(PacketCodec.hasValidTcpChecksum(sink.packets.last()))
                    assertEquals(isn + 1, synAck?.ack)
                    val serverNext = PacketCodec.seqAdd(synAck?.seq ?: 0L, 1)
                    assertEquals("SOCKS5 server must receive the real target", "127.0.0.1:${origin.port}", socks.lastTarget)

                    relay.onPacket(
                        TestNet.clientPacket(
                            4, clientIp, clientPort, "127.0.0.1", origin.port,
                            isn + 1, serverNext, PacketCodec.FLAG_ACK
                        )
                    )
                    relay.onPacket(
                        TestNet.clientPacket(
                            4, clientIp, clientPort, "127.0.0.1", origin.port,
                            isn + 1, serverNext, PacketCodec.FLAG_PSH or PacketCodec.FLAG_ACK, request
                        )
                    )

                    val response = sink.await { it.payload.isNotEmpty() && PacketCodec.seqDiff(it.seq, serverNext) == 0L }
                    assertNotNull("no remote payload came back through the relay", response)
                    val body = response?.payload ?: ByteArray(0)
                    assertTrue("payload must be the real HTTP reply", String(body).startsWith("HTTP/1.1 200"))
                    assertEquals(serverNext, response?.seq)
                    assertTrue("every relay packet must carry a valid TCP checksum", sink.packets.all { PacketCodec.hasValidTcpChecksum(it) })

                    // ACK the downlink so the relay stops retransmitting, then let it settle.
                    relay.onPacket(
                        TestNet.clientPacket(
                            4, clientIp, clientPort, "127.0.0.1", origin.port,
                            isn + 1 + request.size, PacketCodec.seqAdd(serverNext, body.size.toLong()),
                            PacketCodec.FLAG_ACK
                        )
                    )
                    Thread.sleep(100)
                    val stats = relay.stats()
                    assertEquals("up bytes must equal the payload we forwarded", request.size.toLong(), stats.bytesUp)
                    assertTrue("down bytes must be > 0", stats.bytesDown > 0)
                    assertEquals(1, stats.activeFlows)
                    assertEquals(1L, stats.flowsEstablished)
                    assertEquals(1, socks.connections)
                    assertTrue("origin never saw the request", origin.received >= request.size)
                } finally {
                    relay.shutdown()
                }
            }
        }
    }

    @Test
    fun multiSegmentPayloadArrivesIntactThroughEchoServer() {
        TestNet.EchoServer().use { echo ->
            TestNet.SocksServer().use { socks ->
                val sink = RecordingSink()
                val relay = TcpRelay(sink, TestNet.connectorFor(socks), Events(), config())
                try {
                    val payload = ByteArray(3000) { (it % 251).toByte() }
                    val isn = 5000L
                    relay.onPacket(TestNet.clientPacket(4, clientIp, clientPort, "127.0.0.1", echo.port, isn, 0, PacketCodec.FLAG_SYN))
                    val synAck = sink.await { it.isSyn && it.isAck } ?: error("no handshake")
                    val serverNext = PacketCodec.seqAdd(synAck.seq, 1)
                    relay.onPacket(
                        TestNet.clientPacket(4, clientIp, clientPort, "127.0.0.1", echo.port, isn + 1, serverNext, PacketCodec.FLAG_ACK)
                    )
                    var seq = isn + 1
                    var offset = 0
                    val chunk = 700
                    while (offset < payload.size) {
                        val size = minOf(chunk, payload.size - offset)
                        val part = payload.copyOfRange(offset, offset + size)
                        relay.onPacket(
                            TestNet.clientPacket(
                                4, clientIp, clientPort, "127.0.0.1", echo.port,
                                seq, serverNext, PacketCodec.FLAG_PSH or PacketCodec.FLAG_ACK, part
                            )
                        )
                        seq += size
                        offset += size
                    }
                    // Collect the echoed bytes, ACKing in order.
                    val received = java.io.ByteArrayOutputStream()
                    val deadline = System.currentTimeMillis() + 5000
                    var ackSeq = serverNext
                    while (received.size() < payload.size && System.currentTimeMillis() < deadline) {
                        val flow = sink.await(500) { it.payload.isNotEmpty() && PacketCodec.seqDiff(it.seq, ackSeq) == 0L } ?: continue
                        received.write(flow.payload)
                        ackSeq = PacketCodec.seqAdd(ackSeq, flow.payload.size.toLong())
                        relay.onPacket(
                            TestNet.clientPacket(4, clientIp, clientPort, "127.0.0.1", echo.port, seq, ackSeq, PacketCodec.FLAG_ACK)
                        )
                    }
                    assertEquals(payload.size, received.size())
                    assertTrue("echoed bytes differ from what was sent", payload.contentEquals(received.toByteArray()))
                    val stats = relay.stats()
                    assertEquals(payload.size.toLong(), stats.bytesUp)
                    assertEquals(payload.size.toLong(), stats.bytesDown)
                    assertTrue("payload must be split into multiple segments", stats.segmentsDown >= 3)
                    assertEquals(payload.size.toLong(), echo.echoBytes)
                } finally {
                    relay.shutdown()
                }
            }
        }
    }

    @Test
    fun upstreamFailureResetsTheClientAndIsReported() {
        TestNet.SocksServer(refuseConnect = true).use { socks ->
            val sink = RecordingSink()
            val events = Events()
            val relay = TcpRelay(sink, TestNet.connectorFor(socks), events, config())
            try {
                relay.onPacket(TestNet.clientPacket(4, clientIp, clientPort, "127.0.0.1", 65000, 77, 0, PacketCodec.FLAG_SYN))
                val reset = sink.await { it.isRst }
                assertNotNull("client must receive RST when the upstream cannot be reached", reset)
                assertEquals(0, relay.stats().activeFlows)
                assertEquals(1L, relay.stats().connectFailures)
                assertTrue(events.failed.isNotEmpty())
                assertTrue(events.closed.any { it.contains("upstream_reply") })
            } finally {
                relay.shutdown()
            }
        }
    }

    @Test
    fun upstreamEofSendsFinAndClosesTheFlow() {
        TestNet.CloseServer().use { closing ->
            TestNet.SocksServer().use { socks ->
                val sink = RecordingSink()
                val events = Events()
                val relay = TcpRelay(sink, TestNet.connectorFor(socks), events, config(halfCloseGraceMs = 100))
                try {
                    relay.onPacket(TestNet.clientPacket(4, clientIp, clientPort, "127.0.0.1", closing.port, 900, 0, PacketCodec.FLAG_SYN))
                    val synAck = sink.await { it.isSyn && it.isAck } ?: error("no handshake")
                    relay.onPacket(
                        TestNet.clientPacket(4, clientIp, clientPort, "127.0.0.1", closing.port, 901, PacketCodec.seqAdd(synAck.seq, 1), PacketCodec.FLAG_ACK)
                    )
                    val fin = sink.await { it.isFin }
                    assertNotNull("upstream EOF must produce a FIN for the client", fin)
                    val deadline = System.currentTimeMillis() + 3000
                    while (relay.stats().activeFlows > 0 && System.currentTimeMillis() < deadline) Thread.sleep(20)
                    assertEquals(0, relay.stats().activeFlows)
                    assertTrue(events.closed.any { it == "upstream_eof" || it == "half_close_complete" })
                } finally {
                    relay.shutdown()
                }
            }
        }
    }

    @Test
    fun clientFinIsAcknowledgedAndFlowClosesWithinGrace() {
        TestNet.EchoServer().use { echo ->
            TestNet.SocksServer().use { socks ->
                val sink = RecordingSink()
                val events = Events()
                val relay = TcpRelay(sink, TestNet.connectorFor(socks), events, config(halfCloseGraceMs = 150))
                try {
                    relay.onPacket(TestNet.clientPacket(4, clientIp, clientPort, "127.0.0.1", echo.port, 300, 0, PacketCodec.FLAG_SYN))
                    val synAck = sink.await { it.isSyn && it.isAck } ?: error("no handshake")
                    val serverNext = PacketCodec.seqAdd(synAck.seq, 1)
                    relay.onPacket(
                        TestNet.clientPacket(4, clientIp, clientPort, "127.0.0.1", echo.port, 301, serverNext, PacketCodec.FLAG_ACK)
                    )
                    relay.onPacket(
                        TestNet.clientPacket(
                            4, clientIp, clientPort, "127.0.0.1", echo.port,
                            301, serverNext, PacketCodec.FLAG_FIN or PacketCodec.FLAG_ACK
                        )
                    )
                    val finAck = sink.await { it.isFin && it.isAck }
                    assertNotNull("client FIN must be answered with FIN-ACK", finAck)
                    assertEquals(302L, finAck?.ack)
                    val deadline = System.currentTimeMillis() + 3000
                    while (relay.stats().activeFlows > 0 && System.currentTimeMillis() < deadline) Thread.sleep(20)
                    assertEquals(0, relay.stats().activeFlows)
                    assertTrue(events.closed.isNotEmpty())
                } finally {
                    relay.shutdown()
                }
            }
        }
    }

    @Test
    fun silentUpstreamTimesOutAndResetsInsteadOfHanging() {
        TestNet.SilentServer().use { silent ->
            TestNet.SocksServer().use { socks ->
                val sink = RecordingSink()
                val events = Events()
                val relay = TcpRelay(sink, TestNet.connectorFor(socks), events, config(idleTimeoutMs = 400))
                try {
                    relay.onPacket(TestNet.clientPacket(4, clientIp, clientPort, "127.0.0.1", silent.port, 400, 0, PacketCodec.FLAG_SYN))
                    val synAck = sink.await { it.isSyn && it.isAck } ?: error("no handshake")
                    relay.onPacket(
                        TestNet.clientPacket(4, clientIp, clientPort, "127.0.0.1", silent.port, 401, PacketCodec.seqAdd(synAck.seq, 1), PacketCodec.FLAG_ACK)
                    )
                    val deadline = System.currentTimeMillis() + 4000
                    while (relay.stats().activeFlows > 0 && System.currentTimeMillis() < deadline) Thread.sleep(20)
                    assertEquals("idle flow must be torn down", 0, relay.stats().activeFlows)
                    assertTrue("teardown must be reported", events.closed.contains("idle_timeout"))
                } finally {
                    relay.shutdown()
                }
            }
        }
    }

    @Test
    fun unacknowledgedDownlinkIsRetransmittedThenClosed() {
        val reply = ByteArray(64) { 0x41 }
        TestNet.ReplyServer(reply).use { origin ->
            TestNet.SocksServer().use { socks ->
                val sink = RecordingSink()
                val events = Events()
                val relay = TcpRelay(
                    sink, TestNet.connectorFor(socks), events,
                    config(retransmitIntervalMs = 30, maxRetransmits = 2, idleTimeoutMs = 60_000)
                )
                try {
                    relay.onPacket(TestNet.clientPacket(4, clientIp, clientPort, "127.0.0.1", origin.port, 700, 0, PacketCodec.FLAG_SYN))
                    val synAck = sink.await { it.isSyn && it.isAck } ?: error("no handshake")
                    relay.onPacket(
                        TestNet.clientPacket(4, clientIp, clientPort, "127.0.0.1", origin.port, 701, PacketCodec.seqAdd(synAck.seq, 1), PacketCodec.FLAG_ACK)
                    )
                    relay.onPacket(
                        TestNet.clientPacket(
                            4, clientIp, clientPort, "127.0.0.1", origin.port, 701,
                            PacketCodec.seqAdd(synAck.seq, 1), PacketCodec.FLAG_PSH or PacketCodec.FLAG_ACK,
                            "x".toByteArray()
                        )
                    )
                    val deadline = System.currentTimeMillis() + 5000
                    while (relay.stats().activeFlows > 0 && System.currentTimeMillis() < deadline) Thread.sleep(20)
                    assertTrue("expected retransmissions, got none", relay.stats().retransmits > 0)
                    assertTrue(events.closed.contains("client_ack_timeout"))
                    assertEquals(0, relay.stats().activeFlows)
                } finally {
                    relay.shutdown()
                }
            }
        }
    }

    @Test
    fun ipv6ClientFlowIsRelayedWithValidChecksums() {
        val echo = try {
            TestNet.EchoServer("::1")
        } catch (e: Exception) {
            return // environment without IPv6 loopback: covered by PacketCodecTest
        }
        echo.use {
            TestNet.SocksServer().use { socks ->
                val sink = RecordingSink()
                val relay = TcpRelay(sink, TestNet.connectorFor(socks), Events(), config())
                try {
                    val isn = 1234L
                    relay.onPacket(
                        TestNet.clientPacket(6, "fd00:1::2", clientPort, "::1", echo.port, isn, 0, PacketCodec.FLAG_SYN)
                    )
                    val synAck = sink.await { it.dstPort == clientPort && it.isSyn } ?: error("no IPv6 SYN-ACK")
                    assertEquals(6, synAck.family)
                    assertTrue(PacketCodec.hasValidTcpChecksum(sink.packets.last()))
                    relay.onPacket(
                        TestNet.clientPacket(
                            6, "fd00:1::2", clientPort, "::1", echo.port,
                            isn + 1, PacketCodec.seqAdd(synAck.seq, 1), PacketCodec.FLAG_ACK
                        )
                    )
                    relay.onPacket(
                        TestNet.clientPacket(
                            6, "fd00:1::2", clientPort, "::1", echo.port,
                            isn + 1, PacketCodec.seqAdd(synAck.seq, 1),
                            PacketCodec.FLAG_PSH or PacketCodec.FLAG_ACK, "hello6".toByteArray()
                        )
                    )
                    val echoed = sink.await { it.payload.isNotEmpty() && it.family == 6 }
                    assertNotNull("IPv6 payload did not come back", echoed)
                    assertEquals("hello6", String(echoed?.payload ?: ByteArray(0)))
                } finally {
                    relay.shutdown()
                }
            }
        }
    }
}
