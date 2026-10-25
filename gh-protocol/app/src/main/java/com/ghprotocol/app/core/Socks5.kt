package com.ghprotocol.app.core

import java.net.Inet4Address
import java.net.Inet6Address
import java.net.InetSocketAddress

/**
 * Minimal in-process SOCKS5 client framing + IPv4/UDP/TCP packet codec for the
 * VpnService tunnel (F-3). Pure functions — JVM unit-tested. Talks to Xray's
 * `mixed-in` inbound (SOCKS5 + HTTP on 127.0.0.1:10808). No auth (loopback only).
 */
object Socks5 {

    val GREETING = byteArrayOf(0x05, 0x01, 0x00)

    /** Parse the server greeting reply: 05 00 (no auth) => true. */
    fun greetingReplyOk(reply: ByteArray): Boolean =
        reply.size >= 2 && reply[0].toInt() == 0x05 && reply[1].toInt() == 0x00

    /** CONNECT request (ATYP: 0x01 IPv4 / 0x03 domain / 0x04 IPv6), no auth. */
    fun connectRequest(address: String, port: Int): ByteArray {
        val ipv4 = address.indexOf('.') > 0 && address.count { it == '.' } == 3
        val head = if (ipv4) {
            byteArrayOf(0x05, 0x01, 0x00, 0x01)
        } else if (address.contains(':')) {
            byteArrayOf(0x05, 0x01, 0x00, 0x04)
        } else {
            byteArrayOf(0x05, 0x01, 0x00, 0x03)
        }
        val addrBytes = when {
            ipv4 -> address.split('.').map { it.toInt().toByte() }.toByteArray()
            address.contains(':') -> Inet6Address.getByName(address).address
            else -> address.toByteArray(Charsets.US_ASCII)
        }
        val domainLen = if (!ipv4 && !address.contains(':')) byteArrayOf(addrBytes.size.toByte()) else ByteArray(0)
        return head + domainLen + addrBytes + port.toByte().let { b -> byteArrayOf(((port shr 8) and 0xFF).toByte(), b) }
    }

    /** CONNECT reply: 05 00 .. => true (success). */
    fun connectReplyOk(reply: ByteArray): Boolean =
        reply.size >= 2 && reply[0].toInt() == 0x05 && reply[1].toInt() == 0x00

    /** UDP ASSOCIATE request: 05 03 00 01 0.0.0.0 0. */
    val UDP_ASSOCIATE_REQUEST = byteArrayOf(0x05, 0x03, 0x00, 0x01, 0, 0, 0, 0, 0, 0)

    /**
     * Parse an IPv4 packet header: returns (protocol, dstIp, length) or null.
     * protocol: 6=TCP 17=UDP.
     */
    fun parseIp4(packet: ByteArray): Triple<Int, String, Int>? {
        if (packet.size < 20) return null
        val version = (packet[0].toInt() shr 4) and 0x0F
        if (version != 4) return null
        val ihl = (packet[0].toInt() and 0x0F) * 4
        if (packet.size < ihl) return null
        val protocol = packet[9].toInt() and 0xFF
        val totalLen = ((packet[2].toInt() and 0xFF) shl 8) or (packet[3].toInt() and 0xFF)
        val dst = listOf(packet[16], packet[17], packet[18], packet[19])
            .joinToString(".") { (it.toInt() and 0xFF).toString() }
        return Triple(protocol, dst, totalLen)
    }

    /** IPv4 header length in bytes (typically 20). */
    fun ipHeaderLen(packet: ByteArray): Int =
        if (packet.isNotEmpty()) ((packet[0].toInt() and 0x0F) * 4).coerceAtLeast(20) else 20

    /** Destination port from a TCP segment (segment = bytes after the IP header). */
    fun segmentDstPort(segment: ByteArray): Int =
        if (segment.size >= 4) ((segment[2].toInt() and 0xFF) shl 8) or (segment[3].toInt() and 0xFF)
        else 0

    /**
     * Source port within a FULL IPv4 packet (IP header + segment).
     */
    fun transportSrcPort(packet: ByteArray, proto: Int = 17): Int =
        transportPortAt(packet, ipHeaderLen(packet))

    /**
     * Destination port within a FULL IPv4 packet.
     */
    fun transportDstPort(packet: ByteArray, proto: Int = 17): Int =
        transportPortAt(packet, ipHeaderLen(packet) + 2)

    private fun transportPortAt(packet: ByteArray, o: Int): Int =
        if (packet.size >= o + 2)
            ((packet[o].toInt() and 0xFF) shl 8) or (packet[o + 1].toInt() and 0xFF)
        else 0

    /** Source IP (IPv4) from a full packet (IP header offset 12). */
    fun ipSrcIp(packet: ByteArray): String =
        if (packet.size >= 16)
            listOf(packet[12], packet[13], packet[14], packet[15])
                .joinToString(".") { (it.toInt() and 0xFF).toString() }
        else ""

    /** TCP flags byte (SYN=0x02, ACK=0x10, FIN=0x01, RST=0x04, PSH=0x08). */
    fun tcpFlags(packet: ByteArray): Int {
        val ihl = ipHeaderLen(packet)
        return if (packet.size >= ihl + 14) packet[ihl + 13].toInt() and 0xFF else 0
    }

    /** TCP 32-bit unsigned sequence number from a full IPv4+TCP packet. */
    fun tcpSeq(packet: ByteArray): Long {
        val ihl = ipHeaderLen(packet)
        if (packet.size < ihl + 8) return 0L
        return ((packet[ihl + 4].toLong() and 0xFFL) shl 24) or
            ((packet[ihl + 5].toLong() and 0xFFL) shl 16) or
            ((packet[ihl + 6].toLong() and 0xFFL) shl 8) or
            (packet[ihl + 7].toLong() and 0xFFL)
    }

    /** TCP 32-bit unsigned acknowledgment number from a full IPv4+TCP packet. */
    fun tcpAck(packet: ByteArray): Long {
        val ihl = ipHeaderLen(packet)
        if (packet.size < ihl + 12) return 0L
        return ((packet[ihl + 8].toLong() and 0xFFL) shl 24) or
            ((packet[ihl + 9].toLong() and 0xFFL) shl 16) or
            ((packet[ihl + 10].toLong() and 0xFFL) shl 8) or
            (packet[ihl + 11].toLong() and 0xFFL)
    }

    /** Extract TCP payload bytes after IPv4 header + TCP header (including TCP options). */
    fun tcpPayload(packet: ByteArray): ByteArray {
        val ihl = ipHeaderLen(packet)
        if (packet.size < ihl + 20) return ByteArray(0)
        val dataOff = ((packet[ihl + 12].toInt() shr 4) and 0x0F) * 4
        val start = ihl + dataOff.coerceAtLeast(20)
        val totalLen = ((packet[2].toInt() and 0xFF) shl 8) or (packet[3].toInt() and 0xFF)
        val end = minOf(packet.size, if (totalLen >= start) totalLen else packet.size)
        return if (end > start) packet.copyOfRange(start, end) else ByteArray(0)
    }

    /** Standard RFC 1071 16-bit one's complement IPv4 header checksum. */
    fun ipv4Checksum(header: ByteArray, offset: Int = 0, length: Int = 20): Int {
        var sum = 0L
        var i = 0
        while (i + 1 < length) {
            if (i != 10) {
                val word = ((header[offset + i].toInt() and 0xFF) shl 8) or
                    (header[offset + i + 1].toInt() and 0xFF)
                sum += word
            }
            i += 2
        }
        while ((sum shr 16) != 0L) {
            sum = (sum and 0xFFFFL) + (sum shr 16)
        }
        return (sum.inv() and 0xFFFFL).toInt()
    }

    /**
     * Build an IPv4+UDP packet (20B IP header with valid checksum, 8B UDP header)
     * for injection into the tun — used to route DNS responses back to clients.
     */
    fun buildUdpSegment(
        srcIp: String, srcPort: Int,
        dstIp: String, dstPort: Int,
        payload: ByteArray, payloadOff: Int = 0, payloadLen: Int = payload.size
    ): ByteArray {
        val total = 20 + 8 + payloadLen
        val ip = ByteArray(20)
        ip[0] = 0x45
        ip[2] = (total shr 8).toByte()
        ip[3] = (total and 0xFF).toByte()
        ip[8] = 64.toByte()   // TTL
        ip[9] = 17.toByte()   // UDP
        val src = Inet4Address.getByName(srcIp).address
        val dst = Inet4Address.getByName(dstIp).address
        System.arraycopy(src, 0, ip, 12, 4)
        System.arraycopy(dst, 0, ip, 16, 4)
        val csum = ipv4Checksum(ip)
        ip[10] = (csum shr 8).toByte()
        ip[11] = (csum and 0xFF).toByte()
        val udpLen = 8 + payloadLen
        val udp = ByteArray(8)
        udp[0] = (srcPort shr 8).toByte(); udp[1] = (srcPort and 0xFF).toByte()
        udp[2] = (dstPort shr 8).toByte(); udp[3] = (dstPort and 0xFF).toByte()
        udp[4] = (udpLen shr 8).toByte(); udp[5] = (udpLen and 0xFF).toByte()
        return ip + udp + payload.copyOfRange(payloadOff, payloadOff + payloadLen)
    }

    /**
     * Build a full IPv4+TCP packet (20B IPv4 header + 20B TCP header + payload)
     * with valid IPv4 header checksum and RFC 793 TCP pseudo-header checksum
     * for injection into the TUN device.
     */
    fun buildTcpSegment(
        srcIp: String, srcPort: Int,
        dstIp: String, dstPort: Int,
        seq: Long, ack: Long,
        flags: Int,
        payload: ByteArray = ByteArray(0)
    ): ByteArray {
        val tcpLen = 20 + payload.size
        val total = 20 + tcpLen
        val ip = ByteArray(20)
        ip[0] = 0x45
        ip[2] = (total shr 8).toByte()
        ip[3] = (total and 0xFF).toByte()
        ip[6] = 0x40.toByte() // DF
        ip[8] = 64.toByte()   // TTL
        ip[9] = 6.toByte()    // TCP
        val src = Inet4Address.getByName(srcIp).address
        val dst = Inet4Address.getByName(dstIp).address
        System.arraycopy(src, 0, ip, 12, 4)
        System.arraycopy(dst, 0, ip, 16, 4)
        val ipCsum = ipv4Checksum(ip)
        ip[10] = (ipCsum shr 8).toByte()
        ip[11] = (ipCsum and 0xFF).toByte()

        val seg = ByteArray(tcpLen)
        seg[0] = (srcPort shr 8).toByte()
        seg[1] = (srcPort and 0xFF).toByte()
        seg[2] = (dstPort shr 8).toByte()
        seg[3] = (dstPort and 0xFF).toByte()
        seg[4] = ((seq shr 24) and 0xFFL).toByte()
        seg[5] = ((seq shr 16) and 0xFFL).toByte()
        seg[6] = ((seq shr 8) and 0xFFL).toByte()
        seg[7] = (seq and 0xFFL).toByte()
        seg[8] = ((ack shr 24) and 0xFFL).toByte()
        seg[9] = ((ack shr 16) and 0xFFL).toByte()
        seg[10] = ((ack shr 8) and 0xFFL).toByte()
        seg[11] = (ack and 0xFFL).toByte()
        seg[12] = 0x50.toByte() // data offset = 5 (20 bytes)
        seg[13] = (flags and 0xFF).toByte()
        seg[14] = 0xFF.toByte() // window = 65535
        seg[15] = 0xFF.toByte()
        if (payload.isNotEmpty()) {
            System.arraycopy(payload, 0, seg, 20, payload.size)
        }

        var sum = 0L
        for (i in 0 until 4 step 2) {
            sum += ((src[i].toInt() and 0xFF) shl 8) or (src[i + 1].toInt() and 0xFF)
            sum += ((dst[i].toInt() and 0xFF) shl 8) or (dst[i + 1].toInt() and 0xFF)
        }
        sum += 6L
        sum += tcpLen.toLong()
        var j = 0
        while (j + 1 < seg.size) {
            sum += ((seg[j].toInt() and 0xFF) shl 8) or (seg[j + 1].toInt() and 0xFF)
            j += 2
        }
        if (j < seg.size) {
            sum += (seg[j].toInt() and 0xFF) shl 8
        }
        while ((sum shr 16) != 0L) {
            sum = (sum and 0xFFFFL) + (sum shr 16)
        }
        val tcpCsum = (sum.inv() and 0xFFFFL).toInt()
        seg[16] = (tcpCsum shr 8).toByte()
        seg[17] = (tcpCsum and 0xFF).toByte()
        return ip + seg
    }

    /** Rule #5: Mask destination IPv4 address for privacy-safe diagnostic logging. */
    fun maskIp(ip: String): String {
        val parts = ip.split('.')
        return if (parts.size == 4) "${parts[0]}.${parts[1]}.x.x" else "x.x.x.x"
    }

    /** 4-tuple key for connection reuse. */
    fun connKey(dstIp: String, dstPort: Int, proto: Int): String = "$proto|$dstIp|$dstPort"

    /** InetSocketAddress for a direct connection (fallback when proxy is down). */
    fun socketAddress(dstIp: String, dstPort: Int): InetSocketAddress =
        InetSocketAddress(dstIp, dstPort)
}
