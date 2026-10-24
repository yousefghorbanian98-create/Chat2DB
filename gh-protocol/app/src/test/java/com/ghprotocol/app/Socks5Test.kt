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
        packet[0] = 0x45
        packet[9] = 6
        packet[2] = 0
        packet[3] = 42
        packet[16] = 1; packet[17] = 2; packet[18] = 3; packet[19] = 4
        packet[22] = 0
        packet[23] = 443 shr 8
        packet[24] = (443 and 0xFF).toByte()
        val (proto, dst, len) = Socks5.parseIp4(packet)!!
        assertEquals(6, proto)
        assertEquals("1.2.3.4", dst)
        assertEquals(42, len)
        assertEquals(443, Socks5.segmentDstPort(packet.copyOfRange(20, 42)))
    }

    @Test fun parseIp4RejectsV6OrShort() {
        val v6 = ByteArray(40); v6[0] = 0x60
        assertNull(Socks5.parseIp4(v6))
        assertNull(Socks5.parseIp4(ByteArray(5)))
    }
}
