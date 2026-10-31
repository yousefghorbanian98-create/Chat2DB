package com.ghprotocol.app.net

import com.ghprotocol.app.core.net.PacketCodec
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNotNull
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Test

class PacketCodecTest {

    @Test
    fun ipv4TcpRoundTripHasValidChecksums() {
        val payload = "GET / HTTP/1.1\r\nHost: x\r\n\r\n".toByteArray(Charsets.US_ASCII)
        val packet = PacketCodec.buildTcp(
            family = 4,
            srcIp = "93.184.216.34", srcPort = 443,
            dstIp = "10.8.0.2", dstPort = 40000,
            seq = 0xFFFFFFF0L, ack = 0x12345678L,
            flags = PacketCodec.FLAG_PSH or PacketCodec.FLAG_ACK,
            payload = payload,
            mss = null
        )
        assertNotNull(packet)
        val bytes = packet ?: return
        assertEquals(20 + 20 + payload.size, bytes.size)
        assertTrue(PacketCodec.hasValidIpv4HeaderChecksum(bytes))
        assertTrue(PacketCodec.hasValidTcpChecksum(bytes))
        val flow = PacketCodec.parse(bytes)
        assertNotNull(flow)
        assertEquals(4, flow?.family)
        assertEquals("93.184.216.34", flow?.srcIp)
        assertEquals(443, flow?.srcPort)
        assertEquals("10.8.0.2", flow?.dstIp)
        assertEquals(40000, flow?.dstPort)
        assertEquals(0xFFFFFFF0L, flow?.seq)
        assertEquals(0x12345678L, flow?.ack)
        assertEquals(payload.toList(), flow?.payload?.toList())
        assertFalse(flow?.fragmented ?: true)
    }

    @Test
    fun synAckCarriesMssOptionAndTextBookOffsets() {
        val packet = PacketCodec.buildTcp(
            family = 4,
            srcIp = "1.1.1.1", srcPort = 80,
            dstIp = "10.8.0.2", dstPort = 41000,
            seq = 1000L, ack = 2001L,
            flags = PacketCodec.FLAG_SYN or PacketCodec.FLAG_ACK,
            mss = 1300
        ) ?: error("null packet")
        // data offset must reflect the 4-byte MSS option
        assertEquals(6, (packet[32].toInt() and 0xF0) shr 4)
        assertEquals(2, packet[40].toInt()) // kind = MSS
        assertEquals(4, packet[41].toInt()) // length = 4
        assertEquals(1300, ((packet[42].toInt() and 0xFF) shl 8) or (packet[43].toInt() and 0xFF))
        assertTrue(PacketCodec.hasValidTcpChecksum(packet))
    }

    @Test
    fun ipv6TcpRoundTripAndPseudoHeaderChecksum() {
        val payload = byteArrayOf(0x17, 0x03, 0x03, 0x00, 0x10, 1, 2, 3, 4, 5)
        val packet = PacketCodec.buildTcp(
            family = 6,
            srcIp = "2606:4700:4700::1111", srcPort = 443,
            dstIp = "fd00:1::2", dstPort = 51000,
            seq = 7L, ack = 9L,
            flags = PacketCodec.FLAG_ACK or PacketCodec.FLAG_PSH,
            payload = payload
        ) ?: error("null packet")
        assertEquals(40 + 20 + payload.size, packet.size)
        val flow = PacketCodec.parse(packet) ?: error("unparseable")
        assertEquals(6, flow.family)
        assertEquals(PacketCodec.PROTO_TCP, flow.protocol)
        assertEquals(443, flow.srcPort)
        assertEquals(51000, flow.dstPort)
        assertEquals(payload.toList(), flow.payload.toList())
        assertTrue("IPv6 TCP checksum invalid", PacketCodec.hasValidTcpChecksum(packet))
    }

    @Test
    fun ipv4AndIpv6UdpCarryMandatoryChecksums() {
        val payload = byteArrayOf(0x12, 0x34, 0x01, 0x00, 0, 1, 0, 0, 0, 0, 0, 0)
        val v4 = PacketCodec.buildUdp(4, "10.8.0.1", 53, "10.8.0.2", 5353, payload) ?: error("v4")
        assertTrue(PacketCodec.hasValidUdpChecksum(v4))
        val v6 = PacketCodec.buildUdp(6, "fd00:1::1", 53, "fd00:1::2", 5353, payload) ?: error("v6")
        assertTrue(PacketCodec.hasValidUdpChecksum(v6))
        val checksumOffset = 40 + 6
        assertFalse(v6[checksumOffset].toInt() == 0 && v6[checksumOffset + 1].toInt() == 0)
    }

    @Test
    fun sequenceArithmeticWrapsCorrectly() {
        assertEquals(5L, PacketCodec.seqDiff(5L, 0L))
        assertEquals(-5L, PacketCodec.seqDiff(0L, 5L))
        assertEquals(1L, PacketCodec.seqDiff(0L, 0xFFFFFFFFL))
        assertEquals(-1L, PacketCodec.seqDiff(0xFFFFFFFFL, 0L))
        assertEquals(0L, PacketCodec.seqAdd(0xFFFFFFFFL, 1L))
        assertEquals(2L, PacketCodec.seqAdd(0xFFFFFFF0L, 18L))
    }

    @Test
    fun parserRejectsTruncatedAndNonIpPackets() {
        assertNull(PacketCodec.parse(ByteArray(10)))
        assertNull(PacketCodec.parse(byteArrayOf(0x60, 0, 0, 0)))
        // version 4 but total length smaller than the header
        val broken = ByteArray(20)
        broken[0] = 0x45
        broken[3] = 10
        assertNull(PacketCodec.parse(broken))
    }

    @Test
    fun fragmentedPacketsAreFlaggedNotRelayedSilently() {
        val packet = PacketCodec.buildTcp(
            family = 4, srcIp = "1.2.3.4", srcPort = 80,
            dstIp = "10.8.0.2", dstPort = 9000,
            seq = 1, ack = 2, flags = PacketCodec.FLAG_ACK
        ) ?: error("null")
        // set MF + fragment offset in the IPv4 header
        packet[6] = 0x20
        packet[7] = 0x01
        val flow = PacketCodec.parse(packet) ?: error("unparseable")
        assertTrue(flow.fragmented)
    }

    @Test
    fun ipLiteralDetectionNeverResolvesHostnames() {
        assertTrue(PacketCodec.isIpLiteral("1.1.1.1"))
        assertTrue(PacketCodec.isIpLiteral("2606:4700::1111"))
        assertFalse(PacketCodec.isIpLiteral("cloudflare-dns.com"))
        assertFalse(PacketCodec.isIpLiteral(""))
        assertNull(PacketCodec.ipBytes("example.com"))
        assertEquals(4, PacketCodec.ipBytes("104.16.248.249")?.size)
        assertEquals(16, PacketCodec.ipBytes("2606:4700::1111")?.size)
    }

    @Test
    fun maskingNeverLeaksFullDestinationAddress() {
        assertEquals("142.250.x.x", PacketCodec.maskIp("142.250.185.78"))
        assertTrue(PacketCodec.maskIp("2606:4700:4700::1111").startsWith("2606:4700"))
    }
}
