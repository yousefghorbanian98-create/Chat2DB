package com.ghprotocol.app.core.net

import java.io.InputStream
import java.io.OutputStream
import java.net.Socket
import java.util.ArrayDeque
import java.util.concurrent.ConcurrentHashMap
import java.util.concurrent.atomic.AtomicLong

/** Output side of the tunnel (the TUN file descriptor in production, a recorder in tests). */
interface TunSink {
    fun write(packet: ByteArray): Boolean
}

/** Per-connection tuning. Defaults are production values; tests override the timers. */
data class RelayConfig(
    /** MSS advertised in SYN-ACK — keeps client segments inside our read buffer. */
    val mss: Int = 1300,
    val connectTimeoutMs: Int = 8000,
    val connectReplyTimeoutMs: Int = 12_000,
    val idleTimeoutMs: Long = 300_000,
    val retransmitIntervalMs: Long = 400,
    val maxRetransmits: Int = 6,
    val maxFlows: Int = 512,
    /** Backpressure: stop ACKing new client data above this many buffered upstream bytes. */
    val maxBufferedUpstreamBytes: Int = 262_144,
    val advertisedWindow: Int = 65535,
    val tickerIntervalMs: Long = 100,
    /** Time a half-closed flow is kept around so the peer can finish its FIN exchange. */
    val halfCloseGraceMs: Long = 5_000
)

data class RelayStats(
    val flowsOpened: Long = 0,
    val flowsEstablished: Long = 0,
    val flowsClosed: Long = 0,
    val connectFailures: Long = 0,
    val activeFlows: Int = 0,
    val bytesUp: Long = 0,
    val bytesDown: Long = 0,
    val segmentsUp: Long = 0,
    val segmentsDown: Long = 0,
    val retransmits: Long = 0,
    val droppedFragments: Long = 0,
    val parseFailures: Long = 0,
    val closeReasons: Map<String, Long> = emptyMap()
)

/** Observability hooks — implementations must never throw into the data path. */
interface RelayEvents {
    fun onFlowOpened(key: String, dstIp: String, dstPort: Int) {}
    fun onFlowEstablished(key: String, connectMs: Long) {}
    fun onFlowFailed(key: String, stage: String, detail: String) {}
    fun onFlowClosed(key: String, reason: String, upBytes: Long, downBytes: Long, durationMs: Long) {}
    fun onTraffic(upBytes: Long, downBytes: Long, activeFlows: Int) {}
    fun onStats(stats: RelayStats) {}
    fun onWarning(stage: String, detail: String) {}
}

/**
 * Userspace TCP relay for the VpnService TUN device (IPv4 **and** IPv6).
 *
 * Responsibilities, each covered by a JVM integration test against a real SOCKS5 server:
 *  1. complete the three-way handshake only after the upstream SOCKS5 CONNECT succeeded
 *     (a failed upstream sends RST so apps fail fast instead of hanging);
 *  2. forward client payload upstream with strict sequence tracking, duplicate/gap
 *     handling and bounded buffering (backpressure instead of silent drops);
 *  3. forward upstream payload back into the TUN with correct seq/ack, a bounded
 *     unacknowledged queue and retransmission when the client does not ACK;
 *  4. tear flows down on FIN/RST/EOF/idle/timeout and always report *why*;
 *  5. expose counters that match the bytes actually forwarded (up/down/active flows).
 */
class TcpRelay(
    private val sink: TunSink,
    private val connector: SocksConnector,
    private val events: RelayEvents = object : RelayEvents {},
    private val config: RelayConfig = RelayConfig(),
    private val clock: () -> Long = { System.currentTimeMillis() },
    private val random: () -> Long = { (System.nanoTime() xor (Math.random() * 1e12).toLong()) and PacketCodec.SEQ_MASK }
) {

    private class FlowKey(val srcIp: String, val srcPort: Int, val dstIp: String, val dstPort: Int) {
        override fun equals(other: Any?): Boolean =
            other is FlowKey && other.srcIp == srcIp && other.srcPort == srcPort &&
                other.dstIp == dstIp && other.dstPort == dstPort

        override fun hashCode(): Int {
            var h = srcIp.hashCode()
            h = 31 * h + srcPort
            h = 31 * h + dstIp.hashCode()
            h = 31 * h + dstPort
            return h
        }

        override fun toString(): String = "$srcIp:$srcPort->$dstIp:$dstPort"
    }

    private inner class Flow(
        val key: FlowKey,
        val family: Int,
        var clientIsn: Long,
        var clientNextSeq: Long,
        var serverIsn: Long,
        var serverNextSeq: Long
    ) {
        var socket: Socket? = null
        var established = false
        var closed = false
        var clientFin = false
        var serverFinSent = false
        var lastActivityMs: Long = clock()
        var closeAfterMs: Long = 0L
        var upBytes = 0L
        var downBytes = 0L
        var openedAtMs: Long = clock()
        val pendingUp = ArrayDeque<ByteArray>()
        var bufferedUpBytes = 0
        val downQueue = ArrayList<DownSegment>()
        val writerSignal = Object()
        val ackSignal = Object()
        var writerStop = false
    }

    private class DownSegment(
        val seq: Long,
        val payload: ByteArray,
        var sentAtMs: Long,
        var tries: Int
    )

    private val flows = ConcurrentHashMap<FlowKey, Flow>()
    private val flowsOpened = AtomicLong()
    private val flowsEstablished = AtomicLong()
    private val flowsClosed = AtomicLong()
    private val connectFailures = AtomicLong()
    private val upTotal = AtomicLong()
    private val downTotal = AtomicLong()
    private val segmentsUp = AtomicLong()
    private val segmentsDown = AtomicLong()
    private val retransmits = AtomicLong()
    private val droppedFragments = AtomicLong()
    private val parseFailures = AtomicLong()
    private val closeReasons = ConcurrentHashMap<String, AtomicLong>()

    @Volatile
    private var closed = false
    @Volatile
    private var ticker: Thread? = null
    @Volatile
    private var lastStatsPublish = 0L

    /** Optional observer for every packet written to the TUN (used by the in-tunnel self-test). */
    @Volatile
    var packetObserver: ((ByteArray) -> Unit)? = null

    fun stats(): RelayStats = RelayStats(
        flowsOpened = flowsOpened.get(),
        flowsEstablished = flowsEstablished.get(),
        flowsClosed = flowsClosed.get(),
        connectFailures = connectFailures.get(),
        activeFlows = flows.size,
        bytesUp = upTotal.get(),
        bytesDown = downTotal.get(),
        segmentsUp = segmentsUp.get(),
        segmentsDown = segmentsDown.get(),
        retransmits = retransmits.get(),
        droppedFragments = droppedFragments.get(),
        parseFailures = parseFailures.get(),
        closeReasons = closeReasons.mapValues { it.value.get() }
    )

    /**
     * Entry point for every TCP packet read from the TUN.
     * Non-TCP packets are ignored here (UDP/DNS is handled by the service).
     */
    fun onPacket(raw: ByteArray) {
        if (closed) return
        val packet = PacketCodec.parse(raw)
        if (packet == null) {
            parseFailures.incrementAndGet()
            return
        }
        if (packet.protocol != PacketCodec.PROTO_TCP) return
        if (packet.fragmented) {
            droppedFragments.incrementAndGet()
            events.onWarning("relay_fragment_dropped", "${packet.srcIp}:${packet.srcPort}")
            return
        }
        val key = FlowKey(packet.srcIp, packet.srcPort, packet.dstIp, packet.dstPort)
        if (packet.isRst) {
            flows[key]?.let { closeFlow(it, "client_rst", sendRst = false) }
            return
        }
        if (packet.isSyn && !packet.isAck) {
            onSyn(key, packet)
            return
        }
        val flow = flows[key] ?: return
        synchronized(flow) {
            if (flow.closed) return
            flow.lastActivityMs = clock()
            if (packet.isAck) onAck(flow, packet)
            if (packet.payload.isNotEmpty()) onClientPayload(flow, packet)
            if (packet.isFin) onClientFin(flow, packet)
        }
    }

    private fun onSyn(key: FlowKey, packet: PacketCodec.IpFlow) {
        val existing = flows[key]
        if (existing != null) {
            synchronized(existing) {
                if (!existing.closed && existing.established) {
                    // SYN retransmit after our SYN-ACK was lost: replay it with the same ISN.
                    sendSynAck(existing)
                }
            }
            return
        }
        if (flows.size >= config.maxFlows) {
            sendReset(packet.family, key, PacketCodec.seqAdd(packet.seq, 1), 0L, reasonFor = "max_flows")
            return
        }
        val serverIsn = random() and PacketCodec.SEQ_MASK
        val flow = Flow(
            key = key,
            family = packet.family,
            clientIsn = packet.seq,
            clientNextSeq = PacketCodec.seqAdd(packet.seq, 1),
            serverIsn = serverIsn,
            serverNextSeq = PacketCodec.seqAdd(serverIsn, 1)
        )
        flows[key] = flow
        flowsOpened.incrementAndGet()
        events.onFlowOpened(key.toString(), packet.dstIp, packet.dstPort)
        startTicker()
        publishStats(force = true)

        Thread({
            val result = connector.connect(
                packet.dstIp, packet.dstPort,
                connectTimeoutMs = config.connectTimeoutMs,
                replyTimeoutMs = config.connectReplyTimeoutMs
            )
            val socket = result.socket
            if (socket == null || result.stage != "done") {
                connectFailures.incrementAndGet()
                events.onFlowFailed(key.toString(), result.stage, result.detail)
                closeFlow(flow, "upstream_" + result.stage, sendRst = true)
                return@Thread
            }
            synchronized(flow) {
                if (flow.closed) {
                    try { socket.close() } catch (_: Exception) { }
                    return@Thread
                }
                flow.socket = socket
                flow.established = true
            }
            flowsEstablished.incrementAndGet()
            // SYN-ACK is sent *after* the upstream is connected: if the upstream fails we RST
            // instead of accepting a connection we cannot serve.
            synchronized(flow) { sendSynAck(flow) }
            events.onFlowEstablished(key.toString(), result.elapsedMs)
            startWriter(flow, socket)
            startReader(flow, socket)
            publishStats(force = true)
        }, "gh-relay-connect-${key.srcPort}").apply { isDaemon = true; start() }
    }

    private fun sendSynAck(flow: Flow) {
        val packet = PacketCodec.buildTcp(
            family = flow.family,
            srcIp = flow.key.dstIp, srcPort = flow.key.dstPort,
            dstIp = flow.key.srcIp, dstPort = flow.key.srcPort,
            seq = flow.serverIsn,
            ack = flow.clientNextSeq,
            flags = PacketCodec.FLAG_SYN or PacketCodec.FLAG_ACK,
            window = config.advertisedWindow,
            mss = config.mss
        ) ?: return
        writeTun(packet)
    }

    private fun onAck(flow: Flow, packet: PacketCodec.IpFlow) {
        if (flow.downQueue.isEmpty()) return
        val acked = packet.ack
        val iterator = flow.downQueue.iterator()
        var removed = false
        while (iterator.hasNext()) {
            val segment = iterator.next()
            val end = PacketCodec.seqAdd(segment.seq, segment.payload.size.toLong())
            if (PacketCodec.seqDiff(acked, end) >= 0) {
                iterator.remove()
                removed = true
            }
        }
        if (removed) {
            synchronized(flow.ackSignal) { flow.ackSignal.notifyAll() }
        }
    }

    private fun onClientPayload(flow: Flow, packet: PacketCodec.IpFlow) {
        val diff = PacketCodec.seqDiff(packet.seq, flow.clientNextSeq)
        if (diff < 0) {
            // Duplicate (client retransmitted): re-ACK the expected sequence, do not resend bytes.
            sendAck(flow)
            return
        }
        if (diff > 0) {
            // Out-of-order gap: ACK what we have so the client retransmits the missing bytes.
            sendAck(flow)
            return
        }
        if (flow.bufferedUpBytes + packet.payload.size > config.maxBufferedUpstreamBytes) {
            // Backpressure: withhold the ACK; the client retransmits once the queue drains.
            events.onWarning("relay_upstream_backpressure", "buffered=${flow.bufferedUpBytes}")
            return
        }
        flow.clientNextSeq = PacketCodec.seqAdd(flow.clientNextSeq, packet.payload.size.toLong())
        flow.pendingUp.addLast(packet.payload)
        flow.bufferedUpBytes += packet.payload.size
        upTotal.addAndGet(packet.payload.size.toLong())
        segmentsUp.incrementAndGet()
        flow.upBytes += packet.payload.size
        synchronized(flow.writerSignal) { flow.writerSignal.notifyAll() }
        sendAck(flow)
        publishStats()
        events.onTraffic(upTotal.get(), downTotal.get(), flows.size)
    }

    private fun onClientFin(flow: Flow, packet: PacketCodec.IpFlow) {
        if (flow.clientFin) return
        flow.clientFin = true
        flow.clientNextSeq = PacketCodec.seqAdd(flow.clientNextSeq, 1)
        sendFinToClient(flow)
        val socket = flow.socket
        if (socket != null) {
            try {
                socket.shutdownOutput()
            } catch (_: Exception) {
                // reader thread may have closed the socket already
            }
        }
        flow.closeAfterMs = clock() + config.halfCloseGraceMs
    }

    private fun sendFinToClient(flow: Flow) {
        if (flow.serverFinSent) return
        flow.serverFinSent = true
        val fin = PacketCodec.buildTcp(
            family = flow.family,
            srcIp = flow.key.dstIp, srcPort = flow.key.dstPort,
            dstIp = flow.key.srcIp, dstPort = flow.key.srcPort,
            seq = flow.serverNextSeq, ack = flow.clientNextSeq,
            flags = PacketCodec.FLAG_FIN or PacketCodec.FLAG_ACK,
            window = config.advertisedWindow
        )
        if (fin != null) writeTun(fin)
        flow.serverNextSeq = PacketCodec.seqAdd(flow.serverNextSeq, 1)
    }

    private fun onUpstreamEof(flow: Flow) {
        val closeNow: Boolean
        synchronized(flow) {
            if (flow.closed) return
            sendFinToClient(flow)
            closeNow = flow.clientFin
            if (!closeNow) flow.closeAfterMs = clock() + config.halfCloseGraceMs
        }
        if (closeNow) closeFlow(flow, "upstream_eof", sendRst = false)
    }

    private fun onUpstreamData(flow: Flow, buffer: ByteArray, length: Int) {
        var offset = 0
        while (offset < length) {
            // Respect the client's receive window: wait until ACKs free some space.
            waitForAckSpace(flow)
            if (flow.closed || closed) return
            val chunkSize = minOf(config.mss, length - offset)
            val chunk = buffer.copyOfRange(offset, offset + chunkSize)
            synchronized(flow) {
                if (flow.closed) return
                val seq = flow.serverNextSeq
                val packet = PacketCodec.buildTcp(
                    family = flow.family,
                    srcIp = flow.key.dstIp, srcPort = flow.key.dstPort,
                    dstIp = flow.key.srcIp, dstPort = flow.key.srcPort,
                    seq = seq, ack = flow.clientNextSeq,
                    flags = PacketCodec.FLAG_PSH or PacketCodec.FLAG_ACK,
                    payload = chunk,
                    window = config.advertisedWindow
                ) ?: return
                flow.serverNextSeq = PacketCodec.seqAdd(seq, chunkSize.toLong())
                flow.lastActivityMs = clock()
                flow.downQueue.add(DownSegment(seq, chunk, clock(), 0))
                downTotal.addAndGet(chunkSize.toLong())
                segmentsDown.incrementAndGet()
                flow.downBytes += chunkSize
                writeTun(packet)
            }
            offset += chunkSize
        }
        publishStats()
        events.onTraffic(upTotal.get(), downTotal.get(), flows.size)
    }

    private fun outstandingDownBytes(flow: Flow): Int {
        var total = 0
        for (segment in flow.downQueue) total += segment.payload.size
        return total
    }

    private fun waitForAckSpace(flow: Flow) {
        var waited = 0L
        while (!flow.closed && !closed && waited < config.idleTimeoutMs) {
            val outstanding = synchronized(flow) { outstandingDownBytes(flow) }
            if (outstanding <= config.advertisedWindow) return
            synchronized(flow.ackSignal) {
                try {
                    flow.ackSignal.wait(200)
                } catch (_: InterruptedException) {
                    return
                }
            }
            waited += 200
        }
    }

    private fun sendAck(flow: Flow) {
        val ack = PacketCodec.buildTcp(
            family = flow.family,
            srcIp = flow.key.dstIp, srcPort = flow.key.dstPort,
            dstIp = flow.key.srcIp, dstPort = flow.key.srcPort,
            seq = flow.serverNextSeq, ack = flow.clientNextSeq,
            flags = PacketCodec.FLAG_ACK,
            window = config.advertisedWindow
        ) ?: return
        writeTun(ack)
    }

    private fun sendReset(family: Int, key: FlowKey, seq: Long, ack: Long, reasonFor: String) {
        val rst = PacketCodec.buildTcp(
            family = family,
            srcIp = key.dstIp, srcPort = key.dstPort,
            dstIp = key.srcIp, dstPort = key.srcPort,
            seq = seq, ack = ack,
            flags = PacketCodec.FLAG_RST or PacketCodec.FLAG_ACK,
            window = 0
        )
        if (rst != null) writeTun(rst)
        events.onWarning("relay_reset", "$reasonFor $key")
    }

    private fun writeTun(packet: ByteArray) {
        try {
            sink.write(packet)
        } catch (e: Exception) {
            events.onWarning("tun_write_failed", e.javaClass.simpleName + ": " + (e.message ?: ""))
        }
        val observer = packetObserver
        if (observer != null) {
            try {
                observer(packet)
            } catch (_: Exception) {
                // the observer must never break the data path
            }
        }
    }

    private fun startWriter(flow: Flow, socket: Socket) {
        Thread({
            val output: OutputStream = try {
                socket.getOutputStream()
            } catch (e: Exception) {
                closeFlow(flow, "upstream_output_failed", sendRst = true)
                return@Thread
            }
            while (!closed) {
                var chunk: ByteArray? = null
                synchronized(flow.writerSignal) {
                    if (flow.pendingUp.isEmpty() && !flow.writerStop && !flow.closed) {
                        try {
                            flow.writerSignal.wait(200)
                        } catch (_: InterruptedException) {
                            return@Thread
                        }
                    }
                    if (flow.writerStop || (flow.closed && flow.pendingUp.isEmpty())) return@Thread
                    chunk = flow.pendingUp.pollFirst()
                    val taken = chunk
                    if (taken != null) {
                        flow.bufferedUpBytes = (flow.bufferedUpBytes - taken.size).coerceAtLeast(0)
                    }
                }
                val data = chunk
                if (data == null) {
                    continue
                }
                try {
                    output.write(data)
                    output.flush()
                } catch (e: Exception) {
                    closeFlow(flow, "upstream_write_error", sendRst = true)
                    return@Thread
                }
            }
        }, "gh-relay-tx-${flow.key.srcPort}").apply { isDaemon = true; start() }
    }

    private fun startReader(flow: Flow, socket: Socket) {
        Thread({
            val input: InputStream = try {
                socket.getInputStream()
            } catch (e: Exception) {
                closeFlow(flow, "upstream_input_failed", sendRst = true)
                return@Thread
            }
            val buffer = ByteArray(config.mss * 4)
            try {
                while (!closed && !flow.closed) {
                    val read = input.read(buffer)
                    if (read < 0) break
                    if (read == 0) continue
                    onUpstreamData(flow, buffer, read)
                }
                onUpstreamEof(flow)
            } catch (e: Exception) {
                if (!flow.closed) {
                    closeFlow(flow, "upstream_read_error:" + e.javaClass.simpleName, sendRst = true)
                }
            }
        }, "gh-relay-rx-${flow.key.srcPort}").apply { isDaemon = true; start() }
    }

    private fun startTicker() {
        if (ticker != null) return
        synchronized(this) {
            if (ticker != null) return
            val thread = Thread({
                while (!closed) {
                    try {
                        Thread.sleep(config.tickerIntervalMs)
                    } catch (_: InterruptedException) {
                        return@Thread
                    }
                    tick()
                }
            }, "gh-relay-ticker").apply { isDaemon = true; start() }
            ticker = thread
        }
    }

    private fun tick() {
        val now = clock()
        for (flow in flows.values.toList()) {
            var closeReason: String? = null
            var sendRst = false
            synchronized(flow) {
                if (!flow.closed) {
                    if (flow.closeAfterMs in 1..now) {
                        closeReason = "half_close_complete"
                    } else if (flow.established) {
                        val iterator = flow.downQueue.iterator()
                        while (iterator.hasNext()) {
                            val segment = iterator.next()
                            if (now - segment.sentAtMs < config.retransmitIntervalMs) continue
                            if (segment.tries >= config.maxRetransmits) {
                                closeReason = "client_ack_timeout"
                                sendRst = true
                                break
                            }
                            segment.tries += 1
                            segment.sentAtMs = now
                            retransmits.incrementAndGet()
                            val packet = PacketCodec.buildTcp(
                                family = flow.family,
                                srcIp = flow.key.dstIp, srcPort = flow.key.dstPort,
                                dstIp = flow.key.srcIp, dstPort = flow.key.srcPort,
                                seq = segment.seq, ack = flow.clientNextSeq,
                                flags = PacketCodec.FLAG_PSH or PacketCodec.FLAG_ACK,
                                payload = segment.payload,
                                window = config.advertisedWindow
                            )
                            if (packet != null) writeTun(packet)
                        }
                        if (closeReason == null && now - flow.lastActivityMs > config.idleTimeoutMs) {
                            closeReason = "idle_timeout"
                            sendRst = true
                        }
                    }
                }
            }
            val reason = closeReason
            if (reason != null) closeFlow(flow, reason, sendRst)
        }
        publishStats()
    }

    private fun closeFlow(flow: Flow, reason: String, sendRst: Boolean) {
        synchronized(flow) {
            if (flow.closed) return
            flow.closed = true
            flow.writerStop = true
        }
        flows.remove(flow.key)
        closeReasons.getOrPut(reason) { AtomicLong() }.incrementAndGet()
        flowsClosed.incrementAndGet()
        if (sendRst) {
            sendReset(flow.family, flow.key, flow.serverNextSeq, flow.clientNextSeq, reasonFor = reason)
        }
        val socket = flow.socket
        if (socket != null) {
            try {
                socket.close()
            } catch (_: Exception) {
                // already closed by the peer thread
            }
        }
        synchronized(flow.writerSignal) { flow.writerSignal.notifyAll() }
        synchronized(flow.ackSignal) { flow.ackSignal.notifyAll() }
        events.onFlowClosed(
            key = flow.key.toString(),
            reason = reason,
            upBytes = flow.upBytes,
            downBytes = flow.downBytes,
            durationMs = (clock() - flow.openedAtMs).coerceAtLeast(0L)
        )
        publishStats(force = true)
    }

    /** Close every flow (service teardown) and stop the ticker. */
    fun shutdown(reason: String = "tunnel_stopped") {
        closed = true
        for (flow in flows.values.toList()) closeFlow(flow, reason, sendRst = false)
        flows.clear()
        ticker?.interrupt()
        ticker = null
        publishStats(force = true)
    }

    private fun publishStats(force: Boolean = false) {
        val now = clock()
        if (!force && now - lastStatsPublish < 250) return
        lastStatsPublish = now
        try {
            events.onStats(stats())
        } catch (_: Exception) {
            // event consumers must never break the relay
        }
    }
}
