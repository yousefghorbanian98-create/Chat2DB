package com.ghprotocol.app

import com.ghprotocol.app.core.Socks5
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Test

class Socks5Test {

    @Test fun greetingReply() {
        assertTrue(Socks5.greetingReplyOk(byteArrayOf(0x05, 0x00)))
        assertFalse(Socks5.greetingReplyOk(byteArrayOf(0x05, 0x01)))
    }

    @Test fun connectRequestIpv4() {
        val req = Socks5.connectRequest("93.184.216.34", 443)
        // 05 01 00 01 + 4 addr bytes + 2 port bytes
        assertEquals(0x05, req[0].toInt())
        assertEquals(0x01, req[1].toInt())
        assertEquals(0x00, req[2].toInt())
        assertEquals(0x01, req[3].toInt())
        assertEquals(listOf(93, 184, 216, 34), req.slice(4..7).map { it.toInt() and 0xFF })
        assertEquals(443, ((req[8].toInt() and 0xFF) shl 8) or (req[9].toInt() and 0xFF))
        assertEquals(10, req.size)
    }

    @Test fun connectRequestDomain() {
        val req = Socks5.connectRequest("github.com", 443)
        assertEquals(0x03, req[3].toInt()) // ATYP domain
        assertEquals(10, req[4].toInt())   // len("github.com")
        assertEquals("github.com", req.slice(5..14).joinToString("") { (it.toInt() and 0xFF).toChar().toString() })
    }

    @Test fun connectReply() {
        assertTrue(Socks5.connectReplyOk(byteArrayOf(0x05, 0x00, 0x00, 0x01)))
        assertFalse(Socks5.connectReplyOk(byteArrayOf(0x05, 0x05, 0x00, 0x01)))
    }

    @Test fun parseIp4TcpPacket() {
        // IPv4, IHL=5, proto=6 (TCP), total=42, dst 1.2.3.4 + TCP dst port 443
        val packet = ByteArray(42)
        packet[0] = 0x45.toByte()   // v4, IHL=5
        packet[9] = 6.toByte()      // TCP
        packet[3] = 42.toByte()     // total length = 42
        packet[16] = 1.toByte(); packet[17] = 2.toByte(); packet[18] = 3.toByte(); packet[19] = 4.toByte()  // dst 1.2.3.4
        packet[22] = (443 shr 8).toByte()   // TCP dst port high
        packet[23] = (443 and 0xFF).toByte() // TCP dst port low
        val (proto, dst, len) = Socks5.parseIp4(packet)!!
        assertEquals(6, proto)
        assertEquals("1.2.3.4", dst)
        assertEquals(42, len)
        assertEquals(443, Socks5.segmentDstPort(packet.copyOfRange(20, 42)))
        assertEquals(443, Socks5.transportDstPort(packet, 6))
    }

    @Test fun parseIp4RejectsV6OrShort() {
        val v6 = ByteArray(40); v6[0] = 0x60.toByte()
        assertNull(Socks5.parseIp4(v6))
        assertNull(Socks5.parseIp4(ByteArray(5)))
    }

    @Test fun buildUdpSegmentRoundTrip() {
        val payload = byteArrayOf(0x12, 0x34, 0x01, 0x00, 0xAB.toByte(), 0xCD.toByte())
        val pkt = Socks5.buildUdpSegment("10.8.0.1", 53, "10.8.0.5", 41000, payload)
        assertEquals(20 + 8 + payload.size, pkt.size)
        // IPv4 header sanity
        assertEquals(0x45, pkt[0].toInt())
        assertEquals(17, pkt[9].toInt() and 0xFF)
        assertEquals("10.8.0.1", Socks5.ipSrcIp(pkt))
        assertEquals("10.8.0.5", Socks5.parseIp4(pkt)!!.second)
        // UDP header (full-packet offsets)
        assertEquals(53, Socks5.transportSrcPort(pkt, 17))
        assertEquals(41000, Socks5.transportDstPort(pkt, 17))
        // payload intact
        assertEquals(payload.toList(), pkt.copyOfRange(28, 28 + payload.size).toList())
    }

    @Test fun fullPacketUdpSrcDst() {
        // full 28B packet: src 10.8.0.7:5353 -> dst 10.8.0.1:53
        val pkt = ByteArray(28)
        pkt[0] = 0x45.toByte()
        pkt[3] = 28.toByte()
        pkt[9] = 17.toByte()
        pkt[12] = 10.toByte(); pkt[13] = 8.toByte(); pkt[14] = 0.toByte(); pkt[15] = 7.toByte()  // src
        pkt[16] = 10.toByte(); pkt[17] = 8.toByte(); pkt[18] = 0.toByte(); pkt[19] = 1.toByte()  // dst
        pkt[20] = (5353 shr 8).toByte(); pkt[21] = (5353 and 0xFF).toByte()  // udp src port
        pkt[22] = (53 shr 8).toByte(); pkt[23] = (53 and 0xFF).toByte()      // udp dst port
        assertEquals("10.8.0.7", Socks5.ipSrcIp(pkt))
        assertEquals(5353, Socks5.transportSrcPort(pkt, 17))
        assertEquals(53, Socks5.transportDstPort(pkt, 17))
    }
}
