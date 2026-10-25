package com.ghprotocol.app.core.net

import java.io.ByteArrayOutputStream
import java.util.Collections

data class TunnelSelfTestResult(
    val ok: Boolean,
    val stage: String,
    val detail: String,
    val target: String,
    val latencyMs: Long,
    val requestBytes: Int,
    val responseBytes: Int,
    val synAckMs: Long,
    val firstByteMs: Long,
    val upBytesDelta: Long,
    val downBytesDelta: Long,
    val checksumErrors: Int
) {
    companion object {
        const val STAGE_SYN_ACK = "syn_ack"
        const val STAGE_PAYLOAD = "payload"
        const val STAGE_CONTENT = "content"
        const val STAGE_OK = "ok"
    }
}

/**
 * In-tunnel self-test: injects a **synthetic client flow** into the very same [TcpRelay]
 * instance that carries app traffic and requires real remote payload back.
 *
 * A local SOCKS5 handshake only proves the core is listening; this proves
 * parse → flow → upstream → remote → segment build → TUN write for the same code path apps
 * use, and the byte counters of the relay have to move for it to pass.
 */
class TunnelSelfTest(
    private val relay: TcpRelay,
    private val clientIp: String = "10.8.0.99",
    private val clientPort: Int = 41_234,
    private val clock: () -> Long = { System.currentTimeMillis() }
) {

    private data class Observed(val raw: ByteArray, val flow: PacketCodec.IpFlow)

    fun run(
        targetIp: String,
        targetPort: Int,
        request: ByteArray,
        expected: (ByteArray) -> Boolean,
        timeoutMs: Int = 8000
    ): TunnelSelfTestResult {
        val started = clock()
        val before = relay.stats()
        val queue = Collections.synchronizedList(ArrayList<Observed>())
        val previousObserver = relay.packetObserver
        relay.packetObserver = { packet ->
            val flow = PacketCodec.parse(packet)
            if (flow != null && flow.protocol == PacketCodec.PROTO_TCP &&
                flow.srcIp == targetIp && flow.srcPort == targetPort &&
                flow.dstIp == clientIp && flow.dstPort == clientPort
            ) {
                queue.add(Observed(packet, flow))
            }
            previousObserver?.invoke(packet)
        }
        fun restore() {
            relay.packetObserver = previousObserver
        }
        fun result(
            ok: Boolean,
            stage: String,
            detail: String,
            responseBytes: Int = 0,
            synAckMs: Long = -1,
            firstByteMs: Long = -1,
            checksumErrors: Int = 0
        ): TunnelSelfTestResult {
            val after = relay.stats()
            return TunnelSelfTestResult(
                ok = ok, stage = stage, detail = detail,
                target = "$targetIp:$targetPort",
                latencyMs = clock() - started,
                requestBytes = request.size,
                responseBytes = responseBytes,
                synAckMs = synAckMs,
                firstByteMs = firstByteMs,
                upBytesDelta = after.bytesUp - before.bytesUp,
                downBytesDelta = after.bytesDown - before.bytesDown,
                checksumErrors = checksumErrors
            )
        }

        try {
            val family = if (targetIp.contains(':')) 6 else 4
            val isn = ((Math.random() * 0x7FFFFFFF).toLong()) and PacketCodec.SEQ_MASK
            val deadline = clock() + timeoutMs
            val syn = PacketCodec.buildTcp(
                family = family,
                srcIp = clientIp, srcPort = clientPort,
                dstIp = targetIp, dstPort = targetPort,
                seq = isn, ack = 0L, flags = PacketCodec.FLAG_SYN,
                window = 65535, mss = 1200
            ) ?: return result(false, "build", "cannot_build_syn")
            relay.onPacket(syn)

            val synAck = await(queue, deadline) { it.flow.isSyn && it.flow.isAck }
                ?: return result(false, TunnelSelfTestResult.STAGE_SYN_ACK, "no_syn_ack")
            if (!PacketCodec.hasValidTcpChecksum(synAck.raw)) {
                return result(false, "checksum", "syn_ack_checksum_invalid")
            }
            if (synAck.flow.ack != PacketCodec.seqAdd(isn, 1)) {
                return result(
                    false, TunnelSelfTestResult.STAGE_SYN_ACK,
                    "bad_ack_${synAck.flow.ack}_expected_${PacketCodec.seqAdd(isn, 1)}"
                )
            }
            val synAckMs = clock() - started
            var clientNext = PacketCodec.seqAdd(isn, 1)
            var serverNext = PacketCodec.seqAdd(synAck.flow.seq, 1)

            sendClientPacket(family, targetIp, targetPort, clientNext, serverNext, PacketCodec.FLAG_ACK, ByteArray(0))

            // Two segments: exercises multi-segment upstream forwarding, not just one happy write.
            val split = (request.size / 2).coerceAtLeast(1).coerceAtMost(request.size)
            val parts = listOf(request.copyOfRange(0, split), request.copyOfRange(split, request.size))
            for (part in parts) {
                if (part.isEmpty()) continue
                sendClientPacket(
                    family, targetIp, targetPort, clientNext, serverNext,
                    PacketCodec.FLAG_PSH or PacketCodec.FLAG_ACK, part
                )
                clientNext = PacketCodec.seqAdd(clientNext, part.size.toLong())
            }

            val accumulated = ByteArrayOutputStream()
            var checksumErrors = 0
            var firstByteMs = -1L
            var contentOk = false
            while (clock() < deadline) {
                val observed = await(queue, minOf(deadline, clock() + 300)) { it.flow.payload.isNotEmpty() } ?: continue
                if (!PacketCodec.hasValidTcpChecksum(observed.raw)) {
                    checksumErrors++
                    continue
                }
                val diff = PacketCodec.seqDiff(observed.flow.seq, serverNext)
                if (diff > 0) {
                    // Gap: ACK what we already have so the relay retransmits the missing segment.
                    sendClientPacket(
                        family, targetIp, targetPort, clientNext, serverNext,
                        PacketCodec.FLAG_ACK, ByteArray(0)
                    )
                    continue
                }
                if (diff < 0) {
                    // Duplicate of an already delivered segment.
                    sendClientPacket(
                        family, targetIp, targetPort, clientNext, serverNext,
                        PacketCodec.FLAG_ACK, ByteArray(0)
                    )
                    continue
                }
                accumulated.write(observed.flow.payload)
                serverNext = PacketCodec.seqAdd(serverNext, observed.flow.payload.size.toLong())
                if (firstByteMs < 0) firstByteMs = clock() - started
                sendClientPacket(family, targetIp, targetPort, clientNext, serverNext, PacketCodec.FLAG_ACK, ByteArray(0))
                if (expected(accumulated.toByteArray())) {
                    contentOk = true
                    break
                }
            }

            sendClientPacket(
                family, targetIp, targetPort, clientNext, serverNext,
                PacketCodec.FLAG_FIN or PacketCodec.FLAG_ACK, ByteArray(0)
            )

            val body = accumulated.toByteArray()
            restore()
            if (checksumErrors > 0) {
                return result(false, "checksum", "checksum_errors_$checksumErrors", body.size, synAckMs, firstByteMs, checksumErrors)
            }
            if (body.isEmpty()) {
                return result(false, TunnelSelfTestResult.STAGE_PAYLOAD, "no_response_bytes", 0, synAckMs, firstByteMs)
            }
            if (!contentOk) {
                return result(false, TunnelSelfTestResult.STAGE_CONTENT, "unexpected_content", body.size, synAckMs, firstByteMs)
            }
            return result(true, TunnelSelfTestResult.STAGE_OK, "payload_ok", body.size, synAckMs, firstByteMs)
        } catch (e: Exception) {
            restore()
            return result(false, "exception", e.javaClass.simpleName + ": " + (e.message ?: ""))
        }
    }

    private fun sendClientPacket(
        family: Int,
        targetIp: String,
        targetPort: Int,
        seq: Long,
        ack: Long,
        flags: Int,
        payload: ByteArray
    ) {
        val packet = PacketCodec.buildTcp(
            family = family,
            srcIp = clientIp, srcPort = clientPort,
            dstIp = targetIp, dstPort = targetPort,
            seq = seq, ack = ack, flags = flags,
            payload = payload, window = 65535
        ) ?: return
        relay.onPacket(packet)
    }

    private fun await(
        queue: MutableList<Observed>,
        deadline: Long,
        predicate: (Observed) -> Boolean
    ): Observed? {
        while (clock() < deadline) {
            synchronized(queue) {
                while (queue.isNotEmpty()) {
                    val observed = queue.removeAt(0)
                    if (predicate(observed)) return observed
                }
            }
            try {
                Thread.sleep(5)
            } catch (_: InterruptedException) {
                return null
            }
        }
        return null
    }
}
