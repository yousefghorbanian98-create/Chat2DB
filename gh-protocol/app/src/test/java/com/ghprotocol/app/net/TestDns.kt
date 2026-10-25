package com.ghprotocol.app.net

import com.ghprotocol.app.core.net.PacketCodec
import java.io.ByteArrayOutputStream

/** Builds real DNS wire messages (queries answered by local test servers). */
object TestDns {

    fun query(name: String, type: Int = 1, id: Int = 0x1234): ByteArray =
        com.ghprotocol.app.core.net.DnsMessage.buildQuery(name, type, id)

    /** Build a response that echoes the query's ID + question and appends A records. */
    fun response(query: ByteArray, answers: List<String> = listOf("93.184.216.34"), rcode: Int = 0, ttl: Long = 60): ByteArray {
        val view = com.ghprotocol.app.core.net.DnsMessage.parse(query)
            ?: error("unparseable query")
        val out = ByteArrayOutputStream()
        out.write(byteArrayOf(query[0], query[1]))
        val flags = 0x8000 or 0x0080 or (rcode and 0x0F) or (PacketCodec.readU16(query, 2) and 0x0100)
        out.write(byteArrayOf(((flags shr 8) and 0xFF).toByte(), (flags and 0xFF).toByte()))
        out.write(byteArrayOf(0x00, view.questionCount.toByte()))
        out.write(byteArrayOf(0x00, answers.size.toByte()))
        out.write(byteArrayOf(0x00, 0x00, 0x00, 0x00))
        out.write(query, 12, view.questionEnd - 12)
        for (ip in answers) {
            val bytes = PacketCodec.ipBytes(ip) ?: error("bad ip $ip")
            out.write(byteArrayOf(0xC0.toByte(), 0x0C)) // pointer to the question name
            out.write(byteArrayOf(0x00, 0x01)) // TYPE A
            out.write(byteArrayOf(0x00, 0x01)) // CLASS IN
            out.write(byteArrayOf(
                ((ttl shr 24) and 0xFF).toByte(), ((ttl shr 16) and 0xFF).toByte(),
                ((ttl shr 8) and 0xFF).toByte(), (ttl and 0xFF).toByte()
            ))
            out.write(byteArrayOf(0x00, bytes.size.toByte()))
            out.write(bytes)
        }
        return out.toByteArray()
    }

    fun responseWithId(query: ByteArray, newId: Int, answers: List<String> = listOf("93.184.216.34")): ByteArray {
        val response = response(query, answers)
        response[0] = ((newId shr 8) and 0xFF).toByte()
        response[1] = (newId and 0xFF).toByte()
        return response
    }

    /** A minimal but valid TLS 1.2 ClientHello with SNI (proves TLS records cross the relay). */
    fun tlsClientHello(serverName: String): ByteArray {
        val name = serverName.toByteArray(Charsets.US_ASCII)
        val sni = ByteArrayOutputStream().apply {
            write(0x00); write(0x00) // server_name extension type
            write(0x00); write((name.size + 5) and 0xFF) // extension length
            write(0x00); write((name.size + 3) and 0xFF) // server_name_list length
            write(0x00) // host_name type
            write(0x00); write(name.size and 0xFF)
            write(name)
        }.toByteArray()
        val body = ByteArrayOutputStream().apply {
            write(0x03); write(0x03) // TLS 1.2
            write(ByteArray(32) { (it * 7 + 1).toByte() }) // client random
            write(0x00) // session id length
            write(0x00); write(0x04) // cipher suites length
            write(0xC0.toInt()); write(0x2F); write(0xC0.toInt()); write(0x2B)
            write(0x01); write(0x00) // compression methods
            write(0x00); write(sni.size and 0xFF) // extensions length (fits in 1 byte here)
            write(sni)
        }.toByteArray()
        val handshake = ByteArrayOutputStream().apply {
            write(0x01) // client_hello
            val len = body.size
            write((len shr 16) and 0xFF); write((len shr 8) and 0xFF); write(len and 0xFF)
            write(body)
        }.toByteArray()
        return ByteArrayOutputStream().apply {
            write(0x16); write(0x03); write(0x01)
            write((handshake.size shr 8) and 0xFF); write(handshake.size and 0xFF)
            write(handshake)
        }.toByteArray()
    }
}
