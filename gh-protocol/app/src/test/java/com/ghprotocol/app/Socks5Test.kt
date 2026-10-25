package com.ghprotocol.app

import com.ghprotocol.app.core.Socks5
import com.ghprotocol.app.core.net.PacketCodec
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Test

/**
 * SOCKS5 framing (RFC 1928) + the packet codec that replaced the old hand-rolled helpers.
 *
 * Packet construction/parsing now lives in [PacketCodec] so the same code the relay uses is
 * what the tests check — the duplicated codec that used to live in `Socks5` was deleted
 * (v1.6) after auditing every reference.
 */
class Socks5Test {

    @Test
    fun greetingReply() {
        assertTrue(Socks5.greetingReplyOk(byteArrayOf(0x05, 0x00)))
        assertFalse(Socks5.greetingReplyOk(byteArrayOf(0x05, 0x01)))
        assertFalse(Socks5.greetingReplyOk(byteArrayOf(0x05)))
    }

    @Test
    fun connectRequestIpv4() {
        val req = Socks5.connectRequest("93.184.216.34", 443)
        // 05 01 00 01 + 4 address bytes + 2 port bytes
        assertEquals(0x05, req[0].toInt())
        assertEquals(0x01, req[1].toInt())
        assertEquals(0x00, req[2].toInt())
        assertEquals(0x01, req[3].toInt())
        assertEquals(listOf(93, 184, 216, 34), req.slice(4..7).map { it.toInt() and 0xFF })
        assertEquals(443, ((req[8].toInt() and 0xFF) shl 8) or (req[9].toInt() and 0xFF))
        assertEquals(10, req.size)
    }

    @Test
    fun connectRequestIpv6UsesAtyp4() {
        val req = Socks5.connectRequest("2001:db8::1", 443)
        assertEquals(0x04, req[3].toInt())
        assertEquals(22, req.size) // 4 head + 16 address + 2 port
    }

    @Test
    fun connectRequestDomain() {
        val req = Socks5.connectRequest("github.com", 443)
        assertEquals(0x03, req[3].toInt())
        assertEquals(10, req[4].toInt())
        assertEquals("github.com", req.slice(5..14).joinToString("") { (it.toInt() and 0xFF).toChar().toString() })
    }

    @Test
    fun connectReply() {
        assertTrue(Socks5.connectReplyOk(byteArrayOf(0x05, 0x00, 0x00, 0x01)))
        assertFalse(Socks5.connectReplyOk(byteArrayOf(0x05, 0x05, 0x00, 0x01)))
        assertEquals("connection_refused", Socks5.replyCodeName(0x05))
        assertEquals(4, Socks5.bindAddressLength(1))
        assertEquals(16, Socks5.bindAddressLength(4))
        assertEquals(-2, Socks5.bindAddressLength(3))
        assertEquals(-1, Socks5.bindAddressLength(9))
    }

    @Test
    fun literalDetectionNeverResolvesNames() {
        assertTrue(Socks5.isLiteralAddress("1.2.3.4"))
        assertTrue(Socks5.isLiteralAddress("2001:db8::1"))
        assertFalse(Socks5.isLiteralAddress("example.com"))
        assertNull(PacketCodec.ipBytes("example.com"))
    }

    @Test
    fun packetCodecParsesTcpWithoutTheOldSocks5Helpers() {
        val packet = PacketCodec.buildTcp(
            family = 4,
            srcIp = "10.8.0.1", srcPort = 443,
            dstIp = "10.8.0.2", dstPort = 52345,
            seq = 1000L, ack = 2500000001L,
            flags = 0x18,
            payload = "HEAD / HTTP/1.1\r\n\r\n".toByteArray(Charsets.US_ASCII)
        )
        val flow = PacketCodec.parse(packet ?: ByteArray(0))
        assertEquals(4, flow?.family)
        assertEquals(PacketCodec.PROTO_TCP, flow?.protocol)
        assertEquals("10.8.0.1", flow?.srcIp)
        assertEquals("10.8.0.2", flow?.dstIp)
        assertEquals(443, flow?.srcPort)
        assertEquals(52345, flow?.dstPort)
        assertEquals(0x18, flow?.tcpFlags)
        assertEquals(1000L, flow?.seq)
        assertEquals(2500000001L, flow?.ack)
        assertTrue(flow?.isPsh == true)
        assertTrue(PacketCodec.hasValidTcpChecksum(packet ?: ByteArray(0)))
    }

    @Test
    fun udpRoundTripKeepsPortsAndChecksum() {
        val payload = byteArrayOf(0x12, 0x34, 0x01, 0x00, 0xAB.toByte(), 0xCD.toByte())
        val pkt = PacketCodec.buildUdp(
            family = 4,
            srcIp = "10.8.0.1", srcPort = 53,
            dstIp = "10.8.0.5", dstPort = 41000,
            payload = payload
        ) ?: ByteArray(0)
        val flow = PacketCodec.parse(pkt)
        assertEquals(53, flow?.srcPort)
        assertEquals(41000, flow?.dstPort)
        assertEquals(payload.toList(), flow?.payload?.toList())
        // UDP checksum must be computed (mandatory for IPv6, always set here).
        val checksum = ((pkt[26].toInt() and 0xFF) shl 8) or (pkt[27].toInt() and 0xFF)
        assertTrue(checksum != 0)
    }

    @Test
    fun ipv6UdpAndTcpCarryMandatoryChecksums() {
        val udp = PacketCodec.buildUdp(
            family = 6,
            srcIp = "fd00:1::1", srcPort = 53,
            dstIp = "fd00:1::2", dstPort = 50000,
            payload = ByteArray(12) { it.toByte() }
        ) ?: ByteArray(0)
        val checksumOffset = 40 + 6
        val checksum = ((udp[checksumOffset].toInt() and 0xFF) shl 8) or (udp[checksumOffset + 1].toInt() and 0xFF)
        assertTrue("IPv6 UDP checksum must be non-zero", checksum != 0)

        val tcp = PacketCodec.buildTcp(
            family = 6,
            srcIp = "fd00:1::1", srcPort = 443,
            dstIp = "fd00:1::2", dstPort = 50000,
            seq = 1L, ack = 1L, flags = PacketCodec.FLAG_ACK
        ) ?: ByteArray(0)
        assertTrue(PacketCodec.hasValidTcpChecksum(tcp))
    }
}
