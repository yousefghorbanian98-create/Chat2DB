package com.ghprotocol.app.core.net

import java.net.Inet4Address
import java.net.Inet6Address
import java.net.InetAddress

/**
 * Pure IPv4/IPv6 + TCP/UDP codec for the VpnService data path.
 *
 * Design rules (Finn-loop v1.6):
 *  - **No Android imports, no coroutines** so the whole codec (and the relay built on it)
 *    is executable in plain JVM unit/integration tests. The Android shell
 *    (`VpnTunnelService`) only moves bytes.
 *  - Every builder emits a *fully valid* packet: IPv4 header checksum, mandatory TCP/UDP
 *    checksums (UDP checksum is mandatory for IPv6 and we always compute it), correct
 *    total-length fields, and no reliance on the kernel to "fix" anything.
 *  - Parsing is defensive: truncated packets, non-first IP fragments and unknown
 *    transport protocols are reported as `null`/`protocol` so the caller can *count* them
 *    instead of silently dropping traffic.
 */
object PacketCodec {

    const val PROTO_TCP = 6
    const val PROTO_UDP = 17
    const val PROTO_ICMP = 1
    const val PROTO_ICMPV6 = 58

    const val FLAG_FIN = 0x01
    const val FLAG_SYN = 0x02
    const val FLAG_RST = 0x04
    const val FLAG_PSH = 0x08
    const val FLAG_ACK = 0x10

    const val SEQ_MASK = 0xFFFFFFFFL

    /** A parsed IP packet carrying a TCP or UDP segment (IPv4 or IPv6). */
    data class IpFlow(
        val family: Int,
        val protocol: Int,
        val srcIp: String,
        val dstIp: String,
        val srcPort: Int,
        val dstPort: Int,
        val tcpFlags: Int,
        val seq: Long,
        val ack: Long,
        val window: Int,
        val payload: ByteArray,
        val totalLength: Int,
        /** True when the packet is an IP fragment we cannot relay (non-first / more-fragments). */
        val fragmented: Boolean = false,
        /** The exact bytes of the packet (the ICMP quote needs them). */
        val raw: ByteArray = ByteArray(0)
    ) {
        val isSyn: Boolean get() = (tcpFlags and FLAG_SYN) != 0
        val isAck: Boolean get() = (tcpFlags and FLAG_ACK) != 0
        val isFin: Boolean get() = (tcpFlags and FLAG_FIN) != 0
        val isRst: Boolean get() = (tcpFlags and FLAG_RST) != 0
        val isPsh: Boolean get() = (tcpFlags and FLAG_PSH) != 0
    }

    /** Signed difference of two 32-bit sequence numbers (RFC 1982 style serial arithmetic). */
    fun seqDiff(a: Long, b: Long): Long {
        val d = (a - b) and SEQ_MASK
        return if (d >= 0x80000000L) d - 0x100000000L else d
    }

    fun seqAdd(a: Long, inc: Long): Long = (a + inc) and SEQ_MASK

    fun isIpLiteral(text: String): Boolean {
        val trimmed = text.trim()
        if (trimmed.isEmpty()) return false
        // Avoid getByName() on names: only accept strings that parse as a literal address.
        val looksV4 = trimmed.count { it == '.' } == 3 && trimmed.all { it.isDigit() || it == '.' }
        val looksV6 = trimmed.contains(':') && trimmed.all { it.isLetterOrDigit() || it == ':' || it == '.' }
        return looksV4 || looksV6
    }

    /** Numeric address bytes (4 or 16). Returns null for hostnames — never resolves DNS. */
    fun ipBytes(addr: String): ByteArray? {
        if (!isIpLiteral(addr)) return null
        return try {
            when (val ia = InetAddress.getByName(addr)) {
                is Inet4Address -> ia.address
                is Inet6Address -> ia.address
                else -> null
            }
        } catch (_: Exception) {
            null
        }
    }

    /** Parse a raw packet from the TUN device. */
    fun parse(packet: ByteArray, length: Int = packet.size): IpFlow? {
        if (length < 20 || packet.isEmpty()) return null
        val version = (packet[0].toInt() ushr 4) and 0x0F
        return when (version) {
            4 -> parseIpv4(packet, length)
            6 -> parseIpv6(packet, length)
            else -> null
        }
    }

    private fun parseIpv4(packet: ByteArray, length: Int): IpFlow? {
        val ihl = (packet[0].toInt() and 0x0F) * 4
        if (ihl < 20 || length < ihl) return null
        val totalLen = readU16(packet, 2)
        if (totalLen < ihl) return null
        val end = minOf(length, totalLen)
        val flagsAndOffset = readU16(packet, 6)
        val moreFragments = (flagsAndOffset and 0x2000) != 0
        val fragmentOffset = flagsAndOffset and 0x1FFF
        val protocol = packet[9].toInt() and 0xFF
        val src = addressText(packet, 12, 4)
        val dst = addressText(packet, 16, 4)
        return parseTransport(
            packet = packet, transportOffset = ihl, end = end,
            family = 4, protocol = protocol, srcIp = src, dstIp = dst,
            totalLength = end, fragmented = fragmentOffset != 0 || moreFragments
        )
    }

    private fun parseIpv6(packet: ByteArray, length: Int): IpFlow? {
        if (length < 40) return null
        val payloadLen = readU16(packet, 4)
        val end = minOf(length, 40 + payloadLen)
        var nextHeader = packet[6].toInt() and 0xFF
        var offset = 40
        var fragmented = false
        // Walk common extension headers so plain TCP-over-IPv6 (no fragments) still relays.
        var guard = 0
        while ((nextHeader == 0 || nextHeader == 43 || nextHeader == 60 || nextHeader == 44) && guard++ < 4) {
            if (offset + 8 > end) return null
            if (nextHeader == 44) fragmented = true // fragment header: do not relay
            val extLen = (packet[offset + 1].toInt() and 0xFF) * 8 + 8
            if (extLen <= 0 || offset + extLen > end) return null
            nextHeader = packet[offset].toInt() and 0xFF
            offset += extLen
        }
        val src = addressText(packet, 8, 16)
        val dst = addressText(packet, 24, 16)
        return parseTransport(
            packet = packet, transportOffset = offset, end = end,
            family = 6, protocol = nextHeader, srcIp = src, dstIp = dst,
            totalLength = end, fragmented = fragmented
        )
    }

    private fun parseTransport(
        packet: ByteArray,
        transportOffset: Int,
        end: Int,
        family: Int,
        protocol: Int,
        srcIp: String,
        dstIp: String,
        totalLength: Int,
        fragmented: Boolean
    ): IpFlow? {
        if (transportOffset > end) return null
        if (protocol == PROTO_TCP) {
            if (transportOffset + 20 > end) return null
            val srcPort = readU16(packet, transportOffset)
            val dstPort = readU16(packet, transportOffset + 2)
            val seq = readU32(packet, transportOffset + 4)
            val ack = readU32(packet, transportOffset + 8)
            val dataOffset = ((packet[transportOffset + 12].toInt() ushr 4) and 0x0F) * 4
            if (dataOffset < 20) return null
            val flags = packet[transportOffset + 13].toInt() and 0xFF
            val window = readU16(packet, transportOffset + 14)
            val payloadStart = transportOffset + dataOffset
            val payload = if (payloadStart in 0..end && end > payloadStart) {
                packet.copyOfRange(payloadStart, end)
            } else {
                ByteArray(0)
            }
            return IpFlow(
                family = family, protocol = protocol, srcIp = srcIp, dstIp = dstIp,
                srcPort = srcPort, dstPort = dstPort, tcpFlags = flags,
                seq = seq, ack = ack, window = window, payload = payload,
                totalLength = totalLength, fragmented = fragmented,
                raw = packet.copyOfRange(0, end)
            )
        }
        if (protocol == PROTO_UDP) {
            if (transportOffset + 8 > end) return null
            val srcPort = readU16(packet, transportOffset)
            val dstPort = readU16(packet, transportOffset + 2)
            val udpLen = readU16(packet, transportOffset + 4)
            val payloadStart = transportOffset + 8
            val payloadEnd = if (udpLen >= 8) minOf(end, transportOffset + udpLen) else end
            val payload = if (payloadEnd > payloadStart) {
                packet.copyOfRange(payloadStart, payloadEnd)
            } else {
                ByteArray(0)
            }
            return IpFlow(
                family = family, protocol = protocol, srcIp = srcIp, dstIp = dstIp,
                srcPort = srcPort, dstPort = dstPort, tcpFlags = 0,
                seq = 0L, ack = 0L, window = 0, payload = payload,
                totalLength = totalLength, fragmented = fragmented,
                raw = packet.copyOfRange(0, end)
            )
        }
        return IpFlow(
            family = family, protocol = protocol, srcIp = srcIp, dstIp = dstIp,
            srcPort = 0, dstPort = 0, tcpFlags = 0, seq = 0L, ack = 0L, window = 0,
            payload = ByteArray(0), totalLength = totalLength, fragmented = fragmented,
            raw = packet.copyOfRange(0, end)
        )
    }

    /**
     * Build a complete IP+TCP packet.
     *
     * @param mss when non-null and SYN is set, an RFC 793 MSS option is emitted so the
     *            client never sends segments larger than our read buffer.
     */
    fun buildTcp(
        family: Int,
        srcIp: String,
        srcPort: Int,
        dstIp: String,
        dstPort: Int,
        seq: Long,
        ack: Long,
        flags: Int,
        payload: ByteArray = ByteArray(0),
        window: Int = 65535,
        ttl: Int = 64,
        mss: Int? = null,
        identification: Int = 0
    ): ByteArray? {
        val src = ipBytes(srcIp) ?: return null
        val dst = ipBytes(dstIp) ?: return null
        if (src.size != dst.size || src.size != if (family == 6) 16 else 4) return null

        val options = ArrayList<Byte>(4)
        if (mss != null && (flags and FLAG_SYN) != 0) {
            options.add(2) // kind = MSS
            options.add(4) // length
            options.add(((mss shr 8) and 0xFF).toByte())
            options.add((mss and 0xFF).toByte())
        }
        val optionsLen = if (options.isEmpty()) 0 else 4
        val tcpHeaderLen = 20 + optionsLen
        val segment = ByteArray(tcpHeaderLen + payload.size)
        writeU16(segment, 0, srcPort)
        writeU16(segment, 2, dstPort)
        writeU32(segment, 4, seq)
        writeU32(segment, 8, ack)
        segment[12] = (((tcpHeaderLen / 4) and 0x0F) shl 4).toByte()
        segment[13] = (flags and 0xFF).toByte()
        writeU16(segment, 14, window.coerceIn(0, 65535))
        if (options.isNotEmpty()) {
            for (i in options.indices) segment[20 + i] = options[i]
        }
        if (payload.isNotEmpty()) System.arraycopy(payload, 0, segment, tcpHeaderLen, payload.size)
        writeU16(segment, 16, transportChecksum(family, src, dst, PROTO_TCP, segment))

        val ip = buildIpHeader(family, src, dst, PROTO_TCP, segment.size, ttl, identification)
        return ip + segment
    }

    /** Build a complete IP+UDP packet with a valid (mandatory for IPv6) UDP checksum. */
    fun buildUdp(
        family: Int,
        srcIp: String,
        srcPort: Int,
        dstIp: String,
        dstPort: Int,
        payload: ByteArray,
        ttl: Int = 64,
        identification: Int = 0
    ): ByteArray? {
        val src = ipBytes(srcIp) ?: return null
        val dst = ipBytes(dstIp) ?: return null
        if (src.size != dst.size || src.size != if (family == 6) 16 else 4) return null
        val udpLen = 8 + payload.size
        val datagram = ByteArray(udpLen)
        writeU16(datagram, 0, srcPort)
        writeU16(datagram, 2, dstPort)
        writeU16(datagram, 4, udpLen)
        if (payload.isNotEmpty()) System.arraycopy(payload, 0, datagram, 8, payload.size)
        var checksum = transportChecksum(family, src, dst, PROTO_UDP, datagram)
        if (checksum == 0) checksum = 0xFFFF // RFC 768: 0 means "no checksum", never emit 0
        writeU16(datagram, 6, checksum)
        val ip = buildIpHeader(family, src, dst, PROTO_UDP, datagram.size, ttl, identification)
        return ip + datagram
    }

    private fun buildIpHeader(
        family: Int,
        src: ByteArray,
        dst: ByteArray,
        protocol: Int,
        payloadLength: Int,
        ttl: Int,
        identification: Int
    ): ByteArray {
        return if (family == 4) {
            val total = 20 + payloadLength
            val header = ByteArray(20)
            header[0] = 0x45
            writeU16(header, 2, total)
            writeU16(header, 4, identification and 0xFFFF)
            header[6] = 0x40 // DF — we never fragment
            header[8] = ttl.toByte()
            header[9] = protocol.toByte()
            System.arraycopy(src, 0, header, 12, 4)
            System.arraycopy(dst, 0, header, 16, 4)
            writeU16(header, 10, checksum16(header, 0, 20, 0L))
            header
        } else {
            val header = ByteArray(40)
            header[0] = 0x60
            writeU16(header, 4, payloadLength)
            header[6] = protocol.toByte()
            header[7] = ttl.toByte()
            System.arraycopy(src, 0, header, 8, 16)
            System.arraycopy(dst, 0, header, 24, 16)
            header
        }
    }

    /** TCP/UDP checksum over pseudo-header + segment (RFC 793 / RFC 8200 §8.1). */
    fun transportChecksum(family: Int, src: ByteArray, dst: ByteArray, protocol: Int, segment: ByteArray): Int {
        var sum = 0L
        var i = 0
        while (i + 1 < src.size) {
            sum += ((src[i].toInt() and 0xFF) shl 8) or (src[i + 1].toInt() and 0xFF)
            i += 2
        }
        i = 0
        while (i + 1 < dst.size) {
            sum += ((dst[i].toInt() and 0xFF) shl 8) or (dst[i + 1].toInt() and 0xFF)
            i += 2
        }
        if (family == 4) {
            sum += protocol.toLong()
            sum += segment.size.toLong()
        } else {
            sum += segment.size.toLong()
            sum += protocol.toLong()
        }
        return checksum16(segment, 0, segment.size, sum)
    }

    /** RFC 1071 one's-complement checksum; [initial] carries a pseudo-header sum. */
    fun checksum16(data: ByteArray, offset: Int, length: Int, initial: Long = 0L): Int {
        var sum = initial
        var i = 0
        val end = minOf(data.size, offset + length)
        while (i + 1 < length && offset + i + 1 < end) {
            sum += ((data[offset + i].toInt() and 0xFF) shl 8) or (data[offset + i + 1].toInt() and 0xFF)
            i += 2
        }
        if (i < length && offset + i < end) {
            sum += (data[offset + i].toInt() and 0xFF) shl 8
        }
        while ((sum ushr 16) != 0L) {
            sum = (sum and 0xFFFF) + (sum ushr 16)
        }
        return (sum.inv() and 0xFFFF).toInt()
    }

    /** Verify the IPv4 header checksum (returns true for IPv6 packets where it does not apply). */
    fun hasValidIpv4HeaderChecksum(packet: ByteArray): Boolean {
        val version = (packet[0].toInt() ushr 4) and 0x0F
        if (version != 4 || packet.size < 20) return true
        val ihl = (packet[0].toInt() and 0x0F) * 4
        if (packet.size < ihl) return false
        var sum = 0L
        var i = 0
        while (i + 1 < ihl) {
            sum += ((packet[i].toInt() and 0xFF) shl 8) or (packet[i + 1].toInt() and 0xFF)
            i += 2
        }
        while ((sum ushr 16) != 0L) sum = (sum and 0xFFFF) + (sum ushr 16)
        return (sum and 0xFFFF) == 0xFFFFL
    }

    /** Verify a TCP segment checksum inside a full IP packet. */
    fun hasValidTcpChecksum(packet: ByteArray): Boolean {
        val flow = parse(packet) ?: return false
        if (flow.protocol != PROTO_TCP) return false
        val headerLen = if (flow.family == 4) (packet[0].toInt() and 0x0F) * 4 else 40
        val src = ipBytes(flow.srcIp) ?: return false
        val dst = ipBytes(flow.dstIp) ?: return false
        val segment = packet.copyOfRange(headerLen, flow.totalLength)
        return transportChecksum(flow.family, src, dst, PROTO_TCP, segment) == 0
    }

    /** Verify a UDP datagram checksum inside a full IP packet (IPv6 requires it). */
    fun hasValidUdpChecksum(packet: ByteArray): Boolean {
        val flow = parse(packet) ?: return false
        if (flow.protocol != PROTO_UDP) return false
        val headerLen = if (flow.family == 4) (packet[0].toInt() and 0x0F) * 4 else 40
        val src = ipBytes(flow.srcIp) ?: return false
        val dst = ipBytes(flow.dstIp) ?: return false
        val segment = packet.copyOfRange(headerLen, flow.totalLength)
        if (flow.family == 4 && segment.size > 6 && segment[6].toInt() == 0 && segment[7].toInt() == 0) return true
        return transportChecksum(flow.family, src, dst, PROTO_UDP, segment) == 0
    }

    private fun addressText(packet: ByteArray, offset: Int, size: Int): String {
        return try {
            InetAddress.getByAddress(packet.copyOfRange(offset, offset + size)).hostAddress ?: ""
        } catch (_: Exception) {
            ""
        }
    }

    fun readU16(data: ByteArray, offset: Int): Int {
        if (offset + 1 >= data.size) return 0
        return ((data[offset].toInt() and 0xFF) shl 8) or (data[offset + 1].toInt() and 0xFF)
    }

    fun readU32(data: ByteArray, offset: Int): Long {
        if (offset + 3 >= data.size) return 0L
        return ((data[offset].toLong() and 0xFFL) shl 24) or
            ((data[offset + 1].toLong() and 0xFFL) shl 16) or
            ((data[offset + 2].toLong() and 0xFFL) shl 8) or
            (data[offset + 3].toLong() and 0xFFL)
    }

    fun writeU16(data: ByteArray, offset: Int, value: Int) {
        data[offset] = ((value shr 8) and 0xFF).toByte()
        data[offset + 1] = (value and 0xFF).toByte()
    }

    fun writeU32(data: ByteArray, offset: Int, value: Long) {
        data[offset] = ((value shr 24) and 0xFFL).toByte()
        data[offset + 1] = ((value shr 16) and 0xFFL).toByte()
        data[offset + 2] = ((value shr 8) and 0xFFL).toByte()
        data[offset + 3] = (value and 0xFFL).toByte()
    }

    /**
     * ICMP / ICMPv6 "destination unreachable — port unreachable", quoting [original].
     *
     * Used when a UDP destination cannot be relayed. Telling the client the truth beats a
     * silent drop, and it makes QUIC apps fall back to TCP immediately. No application data
     * is invented — this is standard ICMP signalling about our own limitation.
     */
    fun buildPortUnreachable(original: IpFlow, quoteBytes: Int = 8): ByteArray? {
        val raw = original.raw
        if (raw.isEmpty()) return null
        val src = ipBytes(original.dstIp) ?: return null
        val dst = ipBytes(original.srcIp) ?: return null
        if (original.family == 4) {
            val ihl = (raw[0].toInt() and 0x0F) * 4
            if (ihl < 20 || raw.size < ihl) return null
            val quoteLen = minOf(raw.size, ihl + quoteBytes)
            val icmp = ByteArray(8 + quoteLen)
            icmp[0] = 3 // type: destination unreachable
            icmp[1] = 3 // code: port unreachable
            System.arraycopy(raw, 0, icmp, 8, quoteLen)
            writeU16(icmp, 2, checksum16(icmp, 0, icmp.size))
            val ip = buildIpHeader(4, src, dst, PROTO_ICMP, icmp.size, 64, 0)
            return ip + icmp
        }
        if (original.family == 6) {
            val quoteLen = minOf(raw.size, 40 + quoteBytes)
            val icmp = ByteArray(8 + quoteLen)
            icmp[0] = 1 // type: destination unreachable
            icmp[1] = 4 // code: port unreachable
            System.arraycopy(raw, 0, icmp, 8, quoteLen)
            writeU16(icmp, 2, transportChecksum(6, src, dst, PROTO_ICMPV6, icmp))
            val ip = buildIpHeader(6, src, dst, PROTO_ICMPV6, icmp.size, 64, 0)
            return ip + icmp
        }
        return null
    }

    /** Privacy-safe masking used for all destination logging. */
    fun maskIp(ip: String): String {
        if (ip.contains(':')) {
            val parts = ip.split(':').filter { it.isNotEmpty() }
            return if (parts.size >= 2) "${parts[0]}:${parts[1]}:…" else "x:x:…"
        }
        val parts = ip.split('.')
        return if (parts.size == 4) "${parts[0]}.${parts[1]}.x.x" else "x.x.x.x"
    }
}
