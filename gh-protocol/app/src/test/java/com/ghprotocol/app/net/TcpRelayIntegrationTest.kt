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

    /**
     * Requirement 5: the numbers a user sees must describe *application* traffic. The in-tunnel
     * self-test injects a synthetic flow into the same relay, so its bytes have to be reported
     * apart — never silently added to Up/Down/ActiveTCP.
     */
    @Test
    fun selfTestBytesAreReportedApartFromApplicationBytes() {
        TestNet.EchoServer().use { echo ->
            TestNet.SocksServer().use { socks ->
                val sink = RecordingSink()
                val relay = TcpRelay(sink, TestNet.connectorFor(socks), Events(), config())
                try {
                    // 1) A real application flow (source 10.8.0.2, the tunnel address).
                    val payload = "hello-app".toByteArray()
                    runFlow(relay, sink, echo.port, clientIp, 40000, payload)

                    val appOnly = relay.stats().applicationOnly()
                    assertEquals("app up bytes must be exactly what the app sent", payload.size.toLong(), appOnly.bytesUp)
                    assertEquals(payload.size.toLong(), appOnly.bytesDown)
                    assertEquals(0L, relay.stats().probeBytesUp)
                    assertEquals(0L, relay.stats().probeBytesDown)

                    // 2) The in-tunnel self-test against the same relay instance.
                    val selfTest = com.ghprotocol.app.core.net.TunnelSelfTest(relay)
                    val result = selfTest.run(
                        targetIp = "127.0.0.1",
                        targetPort = echo.port,
                        request = "GET /selftest HTTP/1.0\r\n\r\n".toByteArray(),
                        expected = { bytes -> bytes.isNotEmpty() },
                        timeoutMs = 5000
                    )
                    assertTrue("self-test must pass against the echo server: ${result.stage}/${result.detail}", result.ok)

                    val stats = relay.stats()
                    assertTrue("probe bytes must be recorded", stats.probeBytesUp > 0 && stats.probeBytesDown > 0)
                    val visible = stats.applicationOnly()
                    assertEquals(
                        "self-test bytes must never leak into the displayed Up counter",
                        payload.size.toLong(),
                        visible.bytesUp
                    )
                    assertEquals(
                        "self-test bytes must never leak into the displayed Down counter",
                        payload.size.toLong(),
                        visible.bytesDown
                    )
                    assertEquals("probe flows must not be counted as app flows", stats.probeFlowsOpened, 1L)
                } finally {
                    relay.shutdown()
                }
            }
        }
    }

    /**
     * Requirement 2: TLS traffic through the relay. The bytes are a **real** TLS 1.2
     * ClientHello produced by the JDK's own TLS stack (captured from a throwaway handshake),
     * pushed through the relay in relay-sized pieces against an echo upstream and compared
     * byte for byte — so fragmentation, sequence bookkeeping and checksums are exercised on
     * exactly the record layout a browser sends.
     */
    @Test
    fun realTlsClientHelloIsRelayedByteExact() {
        val hello = captureClientHello()
        assertTrue("captured ClientHello looks wrong: ${hello.size} bytes", hello.size > 100)
        assertEquals("first byte must be a TLS handshake record (0x16)", 0x16.toByte(), hello[0])
        TestNet.EchoServer().use { echo ->
            TestNet.SocksServer().use { socks ->
                val sink = RecordingSink()
                val relay = TcpRelay(sink, TestNet.connectorFor(socks), Events(), config())
                try {
                    val isn = 9000L
                    relay.onPacket(
                        TestNet.clientPacket(4, clientIp, clientPort, "127.0.0.1", echo.port, isn, 0, PacketCodec.FLAG_SYN)
                    )
                    val synAck = sink.await { it.isSyn && it.isAck } ?: error("no handshake")
                    val serverNext = PacketCodec.seqAdd(synAck.seq, 1)
                    relay.onPacket(
                        TestNet.clientPacket(4, clientIp, clientPort, "127.0.0.1", echo.port, isn + 1, serverNext, PacketCodec.FLAG_ACK)
                    )
                    // Send the TLS record in 200-byte pieces (a browser segments it the same way).
                    var seq = isn + 1
                    var offset = 0
                    while (offset < hello.size) {
                        val size = minOf(200, hello.size - offset)
                        relay.onPacket(
                            TestNet.clientPacket(
                                4, clientIp, clientPort, "127.0.0.1", echo.port, seq, serverNext,
                                PacketCodec.FLAG_PSH or PacketCodec.FLAG_ACK,
                                hello.copyOfRange(offset, offset + size)
                            )
                        )
                        seq += size
                        offset += size
                    }
                    val received = java.io.ByteArrayOutputStream()
                    var ackSeq = serverNext
                    val deadline = System.currentTimeMillis() + 8000
                    while (received.size() < hello.size && System.currentTimeMillis() < deadline) {
                        val flow = sink.await(500) {
                            it.payload.isNotEmpty() && it.dstPort == clientPort &&
                                PacketCodec.seqDiff(it.seq, ackSeq) == 0L
                        } ?: continue
                        received.write(flow.payload)
                        ackSeq = PacketCodec.seqAdd(ackSeq, flow.payload.size.toLong())
                        relay.onPacket(
                            TestNet.clientPacket(
                                4, clientIp, clientPort, "127.0.0.1", echo.port, seq, ackSeq, PacketCodec.FLAG_ACK
                            )
                        )
                    }
                    assertTrue(
                        "TLS record must come back byte-exact (got ${received.size()} of ${hello.size})",
                        hello.contentEquals(received.toByteArray())
                    )
                    val stats = relay.stats()
                    assertEquals(hello.size.toLong(), stats.bytesUp)
                    assertEquals(hello.size.toLong(), stats.bytesDown)
                    assertEquals(0, stats.retransmits)
                    assertTrue(sink.packets.all { PacketCodec.hasValidTcpChecksum(it) })
                } finally {
                    relay.shutdown()
                }
            }
        }
    }

    /**
     * Produces a real ClientHello: the JDK TLS client connects to a plain loopback listener,
     * the listener keeps the first inbound record and closes. No network, no fixtures.
     */
    private fun captureClientHello(): ByteArray {
        java.net.ServerSocket(0, 1, java.net.InetAddress.getByName("127.0.0.1")).use { server ->
            val captured = java.io.ByteArrayOutputStream()
            val worker = Thread {
                try {
                    server.accept().use { socket ->
                        socket.soTimeout = 5000
                        val input = socket.getInputStream()
                        val buffer = ByteArray(4096)
                        // First read gives the full ClientHello record on loopback.
                        val read = input.read(buffer)
                        if (read > 0) captured.write(buffer, 0, read)
                    }
                } catch (_: Exception) {
                    // the TLS client gives up after we close, that is expected
                }
            }
            worker.isDaemon = true
            worker.start()
            try {
                val context = javax.net.ssl.SSLContext.getInstance("TLSv1.2")
                context.init(null, arrayOf(object : javax.net.ssl.X509TrustManager {
                    override fun checkClientTrusted(c: Array<out java.security.cert.X509Certificate>?, a: String?) = Unit
                    override fun checkServerTrusted(c: Array<out java.security.cert.X509Certificate>?, a: String?) = Unit
                    override fun getAcceptedIssuers(): Array<java.security.cert.X509Certificate> = emptyArray()
                }), null)
                val socket = context.socketFactory.createSocket("127.0.0.1", server.localPort) as javax.net.ssl.SSLSocket
                socket.use {
                    try { it.startHandshake() } catch (_: Exception) { /* server closed after the record */ }
                }
            } catch (_: Exception) {
                // capture is what matters; the handshake cannot complete by design
            }
            worker.join(5000)
            return captured.toByteArray()
        }
    }

    /**
     * `closeFlow()` removes the flow from the map *before* it emits `onFlowClosed`, so a test that
     * waits for `activeFlows == 0` and then reads the event list is racy on a loaded CI runner.
     * Every event assertion goes through this helper instead.
     */
    private fun awaitClose(events: Events, timeoutMs: Long = 4000, predicate: (String) -> Boolean): Boolean {
        val deadline = System.currentTimeMillis() + timeoutMs
        while (System.currentTimeMillis() < deadline) {
            if (events.closed.any(predicate)) return true
            Thread.sleep(10)
        }
        return events.closed.any(predicate)
    }

    /** Runs one complete app flow (handshake, payload, ACK) and returns the received bytes. */
    private fun runFlow(
        relay: TcpRelay,
        sink: RecordingSink,
        originPort: Int,
        srcIp: String,
        srcPort: Int,
        payload: ByteArray
    ) {
        val isn = 7000L
        relay.onPacket(
            TestNet.clientPacket(4, srcIp, srcPort, "127.0.0.1", originPort, isn, 0, PacketCodec.FLAG_SYN)
        )
        val synAck = sink.await { it.isSyn && it.isAck && it.dstPort == srcPort } ?: error("no SYN-ACK")
        val serverNext = PacketCodec.seqAdd(synAck.seq, 1)
        relay.onPacket(
            TestNet.clientPacket(4, srcIp, srcPort, "127.0.0.1", originPort, isn + 1, serverNext, PacketCodec.FLAG_ACK)
        )
        relay.onPacket(
            TestNet.clientPacket(
                4, srcIp, srcPort, "127.0.0.1", originPort,
                isn + 1, serverNext, PacketCodec.FLAG_PSH or PacketCodec.FLAG_ACK, payload
            )
        )
        val response = sink.await { it.payload.isNotEmpty() && it.dstPort == srcPort }
        assertNotNull("no payload came back for $srcIp:$srcPort", response)
        assertEquals(String(payload), String(response?.payload ?: ByteArray(0)))
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
                assertTrue("a failed flow must be reported as a failure", events.failed.isNotEmpty())
                assertTrue(
                    "teardown reason must name the failing stage, got=${events.closed}",
                    awaitClose(events) { it.contains("upstream_") }
                )
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
                    assertTrue(
                        "upstream EOF must be reported, got=${events.closed}",
                        awaitClose(events) { it == "upstream_eof" || it == "half_close_complete" }
                    )
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
                    assertTrue("closing the flow must be reported, got=${events.closed}", awaitClose(events) { true })
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
                    assertEquals(
                        "teardown must be reported, got=${events.closed}",
                        true,
                        awaitClose(events) { it == "idle_timeout" }
                    )
                    assertEquals("idle flow must be torn down", 0, relay.stats().activeFlows)
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
                    assertTrue(
                        "give-up must be reported, got=${events.closed}",
                        awaitClose(events) { it == "client_ack_timeout" }
                    )
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
