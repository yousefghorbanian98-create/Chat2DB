package com.ghprotocol.app.core

import java.net.Inet4Address
import java.net.Inet6Address
import java.net.InetSocketAddress

/**
 * Minimal in-process SOCKS5 client framing for the VpnService tunnel (F-3).
 * Pure functions — JVM unit-tested. Talks to Xray's `mixed-in` inbound
 * (SOCKS5 + HTTP on 127.0.0.1:10808). No auth (loopback only).
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

    /** Port from a TCP (offset 2) or UDP (offset 0) segment. */
    fun segmentDstPort(segment: ByteArray): Int =
        if (segment.size >= 4) ((segment[2].toInt() and 0xFF) shl 8) or (segment[3].toInt() and 0xFF)
        else 0

    /** Source IP (IPv4) from a segment (offset 12). */
    fun segmentSrcIp(segment: ByteArray): String =
        if (segment.size >= 16)
            listOf(segment[12], segment[13], segment[14], segment[15])
                .joinToString(".") { (it.toInt() and 0xFF).toString() }
        else ""

    /** Source port from a UDP (offset 0) or TCP (offset 2) segment. */
    fun segmentSrcPort(segment: ByteArray, udp: Boolean): Int =
        if (segment.size >= 4) {
            val o = if (udp) 0 else 2
            ((segment[o].toInt() and 0xFF) shl 8) or (segment[o + 1].toInt() and 0xFF)
        } else 0

    /**
     * Build an IPv4+UDP packet (20B IP header, no checksum, 8B UDP header) for
     * injection into the tun — used to route DNS responses back to clients.
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
        val udp = ByteArray(8)
        udp[0] = (srcPort shr 8).toByte(); udp[1] = (srcPort and 0xFF).toByte()
        udp[2] = (dstPort shr 8).toByte(); udp[3] = (dstPort and 0xFF).toByte()
        udp[4] = 8.toByte(); udp[5] = 8.toByte() // len
        return ip + udp + payload.copyOfRange(payloadOff, payloadOff + payloadLen)
    }

    /** 4-tuple key for connection reuse. */
    fun connKey(dstIp: String, dstPort: Int, proto: Int): String = "$proto|$dstIp|$dstPort"

    /** InetSocketAddress for a direct connection (fallback when proxy is down). */
    fun socketAddress(dstIp: String, dstPort: Int): InetSocketAddress =
        InetSocketAddress(dstIp, dstPort)
}
