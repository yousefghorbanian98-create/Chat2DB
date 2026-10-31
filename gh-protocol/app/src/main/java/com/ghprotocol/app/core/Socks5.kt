package com.ghprotocol.app.core

import java.net.Inet4Address
import java.net.Inet6Address
import java.net.InetAddress

/**
 * Minimal SOCKS5 **framing** (RFC 1928) used by the tunnel and by the verifier.
 *
 * Packet (IPv4/IPv6/TCP/UDP) codec lives in [com.ghprotocol.app.core.net.PacketCodec];
 * the client handshake lives in [com.ghprotocol.app.core.net.Socks5Connector].
 * Everything here is pure and JVM unit-tested against a real loopback SOCKS5 server.
 */
object Socks5 {

    val GREETING = byteArrayOf(0x05, 0x01, 0x00)

    /** CONNECT reply codes (RFC 1928 §6). */
    fun replyCodeName(code: Int): String = when (code) {
        0x00 -> "succeeded"
        0x01 -> "general_socks_server_failure"
        0x02 -> "connection_not_allowed_by_ruleset"
        0x03 -> "network_unreachable"
        0x04 -> "host_unreachable"
        0x05 -> "connection_refused"
        0x06 -> "ttl_expired"
        0x07 -> "command_not_supported"
        0x08 -> "address_type_not_supported"
        else -> "unknown_$code"
    }

    /** Parse the server greeting reply: 05 00 (no auth) => true. */
    fun greetingReplyOk(reply: ByteArray): Boolean =
        reply.size >= 2 && reply[0].toInt() == 0x05 && reply[1].toInt() == 0x00

    /**
     * CONNECT request (ATYP 0x01 IPv4 / 0x04 IPv6 / 0x03 domain), no auth.
     * Hostnames are sent as domains; numeric literals are sent as raw address bytes so
     * Xray never has to resolve anything for app traffic.
     */
    fun connectRequest(address: String, port: Int): ByteArray {
        val literal = com.ghprotocol.app.core.net.PacketCodec.ipBytes(address)
        val head: ByteArray
        val addrBytes: ByteArray
        if (literal != null) {
            head = byteArrayOf(0x05, 0x01, 0x00, if (literal.size == 4) 0x01 else 0x04)
            addrBytes = literal
        } else {
            head = byteArrayOf(0x05, 0x01, 0x00, 0x03)
            val name = address.toByteArray(Charsets.US_ASCII)
            addrBytes = byteArrayOf(name.size.toByte()) + name
        }
        val portBytes = byteArrayOf(((port shr 8) and 0xFF).toByte(), (port and 0xFF).toByte())
        return head + addrBytes + portBytes
    }

    /** CONNECT reply: 05 00 .. => true (success). */
    fun connectReplyOk(reply: ByteArray): Boolean =
        reply.size >= 2 && reply[0].toInt() == 0x05 && reply[1].toInt() == 0x00

    /** Length of the BND.ADDR field for a given ATYP, or -1 for an unsupported ATYP. */
    fun bindAddressLength(atyp: Int): Int = when (atyp) {
        1 -> 4
        4 -> 16
        3 -> -2 // variable: caller must read one length byte first
        else -> -1
    }

    /** True when the string is a numeric IPv4/IPv6 literal (no DNS needed). */
    fun isLiteralAddress(address: String): Boolean =
        com.ghprotocol.app.core.net.PacketCodec.isIpLiteral(address)

    /** Canonical text form of a numeric address literal (for 4-tuple keys). */
    fun canonicalAddress(address: String): String {
        val bytes = com.ghprotocol.app.core.net.PacketCodec.ipBytes(address) ?: return address
        return try {
            when (val ia = InetAddress.getByAddress(bytes)) {
                is Inet4Address, is Inet6Address -> ia.hostAddress ?: address
                else -> address
            }
        } catch (_: Exception) {
            address
        }
    }
}
