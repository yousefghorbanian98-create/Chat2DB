package com.ghprotocol.app.core.net

import java.io.DataInputStream
import java.io.InputStream
import java.net.DatagramPacket
import java.net.DatagramSocket
import java.net.InetAddress
import java.net.Socket
import javax.net.ssl.SSLSocket
import javax.net.ssl.SSLSocketFactory

/** One DNS exchange attempt result. [response] is only set when bytes were received. */
data class DnsTransportResult(val response: ByteArray?, val detail: String, val ms: Long)

/** A DNS upstream path (DoH / DNS-over-TCP / UDP). Implementations must be blocking + bounded. */
interface DnsTransport {
    val name: String
    fun exchange(query: ByteArray, timeoutMs: Int): DnsTransportResult
}

/**
 * DoH endpoint definition.
 *
 * [bootstrapIps] are the IPs the TLS connection is dialled to; [host] is used for the TLS
 * SNI, the certificate check and the HTTP `Host` header. They must belong to the same zone —
 * mapping `cloudflare-dns.com` onto an unrelated Cloudflare edge silently breaks the
 * handshake, which is exactly the failure mode documented in DIAGNOSIS (2026-10-25).
 */
data class DohEndpoint(
    val displayName: String,
    val host: String,
    val path: String = "/dns-query",
    val bootstrapIps: List<String>,
    val port: Int = 443
)

/**
 * RFC 8484 DNS-over-HTTPS through the tunnel's SOCKS5 inbound, so the query leaves the
 * device inside the same (fragmented) TLS outbound that app traffic uses.
 */
class DohTransport(
    private val connector: SocksConnector,
    private val endpoint: DohEndpoint,
    private val sslSocketFactory: () -> SSLSocketFactory = {
        SSLSocketFactory.getDefault() as SSLSocketFactory
    },
    private val verifyHostname: Boolean = true,
    override val name: String = "doh:${endpoint.host}"
) : DnsTransport {

    override fun exchange(query: ByteArray, timeoutMs: Int): DnsTransportResult {
        val started = System.currentTimeMillis()
        val failures = ArrayList<String>(2)
        for (ip in endpoint.bootstrapIps) {
            val elapsed = { (System.currentTimeMillis() - started).coerceAtLeast(0L) }
            val connect = connector.connect(
                host = ip,
                port = endpoint.port,
                connectTimeoutMs = minOf(4000, timeoutMs),
                replyTimeoutMs = timeoutMs
            )
            val raw = connect.socket
            if (raw == null) {
                failures.add("$ip:tcp+${connect.stage}:${connect.detail}")
                continue
            }
            try {
                raw.soTimeout = timeoutMs
                raw.tcpNoDelay = true
                val ssl = sslSocketFactory().createSocket(raw, endpoint.host, endpoint.port, true) as SSLSocket
                ssl.use { tls ->
                    tls.soTimeout = timeoutMs
                    if (verifyHostname) {
                        val params = tls.sslParameters
                        params.endpointIdentificationAlgorithm = "HTTPS"
                        tls.sslParameters = params
                    }
                    tls.startHandshake()
                    val request = (
                        "POST ${endpoint.path} HTTP/1.1\r\n" +
                            "Host: ${endpoint.host}\r\n" +
                            "Content-Type: application/dns-message\r\n" +
                            "Accept: application/dns-message\r\n" +
                            "Content-Length: ${query.size}\r\n" +
                            "User-Agent: GhProtocol/1.6\r\n" +
                            "Connection: close\r\n\r\n"
                        ).toByteArray(Charsets.US_ASCII)
                    val out = tls.getOutputStream()
                    out.write(request)
                    out.write(query)
                    out.flush()
                    val body = readHttpBody(tls.getInputStream(), timeoutMs, failures, ip)
                    if (body == null) continue
                    return DnsTransportResult(body, "ok ip=$ip sni=${endpoint.host}", elapsed())
                }
            } catch (e: Exception) {
                failures.add("$ip:${e.javaClass.simpleName}:${e.message ?: "error"}")
            } finally {
                try { raw.close() } catch (_: Exception) { /* already closed */ }
            }
        }
        return DnsTransportResult(null, failures.joinToString("; "), (System.currentTimeMillis() - started))
    }

    private fun readHttpBody(
        input: InputStream,
        timeoutMs: Int,
        failures: MutableList<String>,
        ip: String
    ): ByteArray? {
        val deadline = System.currentTimeMillis() + timeoutMs
        val headerBuffer = java.io.ByteArrayOutputStream()
        var sep = -1
        while (System.currentTimeMillis() < deadline) {
            val b = input.read()
            if (b < 0) break
            headerBuffer.write(b)
            val size = headerBuffer.size()
            if (size >= 4) {
                val data = headerBuffer.toByteArray()
                if (data[size - 4] == '\r'.code.toByte() && data[size - 3] == '\n'.code.toByte() &&
                    data[size - 2] == '\r'.code.toByte() && data[size - 1] == '\n'.code.toByte()
                ) {
                    sep = size
                    break
                }
            }
            if (size > 16 * 1024) break
        }
        if (sep < 0) {
            failures.add("$ip:no_http_headers")
            return null
        }
        val headerBytes = headerBuffer.toByteArray()
        val headers = String(headerBytes, 0, sep, Charsets.ISO_8859_1)
        val statusLine = headers.lineSequence().firstOrNull().orEmpty()
        if (!statusLine.startsWith("HTTP/1.1 200") && !statusLine.startsWith("HTTP/1.0 200")) {
            failures.add("$ip:http_status:${statusLine.take(40)}")
            return null
        }
        val lower = headers.lowercase()
        val contentLength = Regex("content-length:\\s*(\\d+)").find(lower)?.groupValues?.getOrNull(1)?.toIntOrNull()
        if (lower.contains("transfer-encoding: chunked")) {
            val body = readChunked(input, deadline) ?: run {
                failures.add("$ip:chunked_body_invalid")
                return null
            }
            return body
        }
        if (contentLength != null) {
            if (contentLength <= 0 || contentLength > 65535) {
                failures.add("$ip:content_length_invalid:$contentLength")
                return null
            }
            val body = ByteArray(contentLength)
            if (readFully(input, body, deadline) == null) {
                failures.add("$ip:body_truncated")
                return null
            }
            return body
        }
        // No framing headers: read until EOF with a hard cap.
        val buffer = java.io.ByteArrayOutputStream()
        val chunk = ByteArray(1024)
        while (System.currentTimeMillis() < deadline && buffer.size() < 65535) {
            val read = input.read(chunk)
            if (read < 0) break
            buffer.write(chunk, 0, read)
        }
        if (buffer.size() == 0) {
            failures.add("$ip:empty_body")
            return null
        }
        return buffer.toByteArray()
    }

    private fun readFully(input: InputStream, target: ByteArray, deadline: Long): ByteArray? {
        var read = 0
        while (read < target.size && System.currentTimeMillis() < deadline) {
            val n = input.read(target, read, target.size - read)
            if (n < 0) return null
            read += n
        }
        return if (read == target.size) target else null
    }

    private fun readChunked(input: InputStream, deadline: Long): ByteArray? {
        val out = java.io.ByteArrayOutputStream()
        while (System.currentTimeMillis() < deadline && out.size() < 65535) {
            val line = readAsciiLine(input, deadline) ?: return null
            val size = line.trim().substringBefore(';').toIntOrNull(16) ?: return null
            if (size == 0) return out.toByteArray()
            val chunk = ByteArray(size)
            readFully(input, chunk, deadline) ?: return null
            out.write(chunk)
            readAsciiLine(input, deadline) ?: return null // trailing CRLF
        }
        return out.toByteArray()
    }

    private fun readAsciiLine(input: InputStream, deadline: Long): String? {
        val out = StringBuilder()
        while (System.currentTimeMillis() < deadline && out.length < 512) {
            val b = input.read()
            if (b < 0) return null
            if (b == '\n'.code) return out.toString().trimEnd('\r')
            out.append(b.toChar())
        }
        return null
    }
}

/** RFC 1035 §4.2.2 DNS over TCP (2-byte length prefix) — used as a secondary path. */
class TcpDnsTransport(
    private val connector: SocksConnector,
    private val dnsHost: String,
    private val port: Int = 53,
    override val name: String = "tcp:$dnsHost:$port"
) : DnsTransport {

    override fun exchange(query: ByteArray, timeoutMs: Int): DnsTransportResult {
        val started = System.currentTimeMillis()
        val connect = connector.connect(dnsHost, port, minOf(4000, timeoutMs), timeoutMs)
        val socket = connect.socket
            ?: return DnsTransportResult(null, "tcp+${connect.stage}:${connect.detail}", System.currentTimeMillis() - started)
        return try {
            socket.soTimeout = timeoutMs
            socket.use { s ->
                val out = s.getOutputStream()
                val din = DataInputStream(s.getInputStream())
                out.write(byteArrayOf(((query.size shr 8) and 0xFF).toByte(), (query.size and 0xFF).toByte()))
                out.write(query)
                out.flush()
                val length = din.readUnsignedShort()
                if (length !in 12..4096) {
                    return DnsTransportResult(null, "bad_length_$length", System.currentTimeMillis() - started)
                }
                val answer = ByteArray(length)
                din.readFully(answer)
                DnsTransportResult(answer, "ok", System.currentTimeMillis() - started)
            }
        } catch (e: Exception) {
            DnsTransportResult(null, e.javaClass.simpleName + ":" + (e.message ?: ""), System.currentTimeMillis() - started)
        }
    }
}

/**
 * Plain UDP DNS, either through Xray's `dns-in` dokodemo-door (127.0.0.1:15353) or with a
 * VpnService-protected socket. Last resort only: plain port 53 is what gets poisoned.
 */
class UdpDnsTransport(
    private val host: String,
    private val port: Int,
    private val protectSocket: ((DatagramSocket) -> Unit)? = null,
    override val name: String = "udp:$host:$port"
) : DnsTransport {

    override fun exchange(query: ByteArray, timeoutMs: Int): DnsTransportResult {
        val started = System.currentTimeMillis()
        return try {
            DatagramSocket().use { socket ->
                protectSocket?.invoke(socket)
                socket.soTimeout = timeoutMs
                val address = InetAddress.getByName(host)
                socket.send(DatagramPacket(query, query.size, address, port))
                val buffer = ByteArray(4096)
                val packet = DatagramPacket(buffer, buffer.size)
                socket.receive(packet)
                val answer = packet.data.copyOfRange(packet.offset, packet.offset + packet.length)
                DnsTransportResult(answer, "ok", System.currentTimeMillis() - started)
            }
        } catch (e: Exception) {
            DnsTransportResult(null, e.javaClass.simpleName + ":" + (e.message ?: ""), System.currentTimeMillis() - started)
        }
    }
}
