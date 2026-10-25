package com.ghprotocol.app.core

import android.util.Log
import java.io.DataInputStream
import java.net.InetSocketAddress
import java.net.Socket

data class TunnelVerifyResult(
    val ok: Boolean,
    val latencyMs: Int,
    val target: String,
    val detail: String
)

/**
 * Real end-to-end tunnel verification through Xray's loopback SOCKS5 inbound (127.0.0.1:10808),
 * patterned after Hiddify / v2rayNG "Real Delay (URL Test)" & Psiphon tunnel verification.
 */
object TunnelVerifier {

    private data class ProbeTarget(
        val host: String,
        val port: Int,
        val httpPath: String?,
        val hostHeader: String,
        val tcpDnsQuery: Boolean = false
    )

    private val TARGETS = listOf(
        ProbeTarget("1.1.1.1", 80, "/cdn-cgi/trace", "1.1.1.1"),
        ProbeTarget("104.18.12.149", 80, "/cdn-cgi/trace", "cp.cloudflare.com"),
        ProbeTarget("8.8.8.8", 53, null, "dns.google", tcpDnsQuery = true)
    )

    // Minimal RFC 1035 DNS query for example.com A record (29 bytes)
    private val DNS_PROBE_QUERY = byteArrayOf(
        0x12, 0x34, 0x01, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x07, 'e'.code.toByte(), 'x'.code.toByte(), 'a'.code.toByte(), 'm'.code.toByte(),
        'p'.code.toByte(), 'l'.code.toByte(), 'e'.code.toByte(),
        0x03, 'c'.code.toByte(), 'o'.code.toByte(), 'm'.code.toByte(), 0x00,
        0x00, 0x01, 0x00, 0x01
    )

    fun verifyThroughSocks5(
        proxyHost: String = VpnTunnelService.PROXY_HOST,
        proxyPort: Int = VpnTunnelService.PROXY_PORT,
        timeoutMs: Int = 4500
    ): TunnelVerifyResult {
        var lastError = "timeout"
        for (target in TARGETS) {
            val t0 = System.currentTimeMillis()
            val r = probeSingleTarget(proxyHost, proxyPort, target, timeoutMs)
            val dt = (System.currentTimeMillis() - t0).toInt().coerceAtLeast(1)
            if (r.first) {
                Log.d("GhDiag", "relay tcp ${Socks5.maskIp(target.host)}:${target.port} -> socks5 ok (${dt}ms)")
                return TunnelVerifyResult(
                    ok = true,
                    latencyMs = dt,
                    target = "${target.host}:${target.port}",
                    detail = r.second
                )
            } else {
                lastError = r.second
            }
        }
        return TunnelVerifyResult(
            ok = false,
            latencyMs = -1,
            target = "127.0.0.1:$proxyPort",
            detail = lastError
        )
    }

    private fun probeSingleTarget(
        proxyHost: String,
        proxyPort: Int,
        target: ProbeTarget,
        timeoutMs: Int
    ): Pair<Boolean, String> {
        return try {
            Socket().use { s ->
                s.connect(InetSocketAddress(proxyHost, proxyPort), timeoutMs)
                s.soTimeout = timeoutMs
                s.tcpNoDelay = true
                val out = s.getOutputStream()
                val din = DataInputStream(s.getInputStream())

                out.write(Socks5.GREETING)
                out.flush()
                val greet = ByteArray(2)
                din.readFully(greet, 0, 2)
                if (!Socks5.greetingReplyOk(greet)) {
                    return Pair(false, "socks5_greeting_rejected")
                }

                out.write(Socks5.connectRequest(target.host, target.port))
                out.flush()
                val head = ByteArray(4)
                din.readFully(head, 0, 4)
                if (!Socks5.connectReplyOk(head)) {
                    return Pair(false, "socks5_connect_code_${head[1].toInt() and 0xFF}")
                }
                val atyp = head[3].toInt() and 0xFF
                val bindLen = when (atyp) {
                    1 -> 4
                    4 -> 16
                    3 -> (din.readByte().toInt() and 0xFF)
                    else -> 0
                }
                if (bindLen > 0) {
                    din.readFully(ByteArray(bindLen))
                }
                din.readShort()

                if (target.httpPath != null) {
                    val req = "GET ${target.httpPath} HTTP/1.1\r\nHost: ${target.hostHeader}\r\nUser-Agent: GhProtocol/1.3\r\nConnection: close\r\n\r\n"
                    val reqBytes = req.toByteArray(Charsets.US_ASCII)
                    out.write(reqBytes)
                    out.flush()
                    val buf = ByteArray(256)
                    val n = s.getInputStream().read(buf)
                    if (n <= 0) {
                        return Pair(false, "http_empty_reply")
                    }
                    TunnelLogBuffer.recordTraffic(reqBytes.size, n, 1)
                    val statusLine = String(buf, 0, n, Charsets.US_ASCII).lineSequence().firstOrNull().orEmpty()
                    if (statusLine.startsWith("HTTP/1.")) {
                        return Pair(true, statusLine.trim())
                    }
                    return Pair(false, "invalid_http_status")
                }

                if (target.tcpDnsQuery) {
                    val q = DNS_PROBE_QUERY
                    out.write(byteArrayOf(((q.size shr 8) and 0xFF).toByte(), (q.size and 0xFF).toByte()))
                    out.write(q)
                    out.flush()
                    val respLen = din.readUnsignedShort()
                    if (respLen in 12..4096) {
                        val ans = ByteArray(respLen)
                        din.readFully(ans)
                        val rcode = ans[3].toInt() and 0x0F
                        if (rcode == 0 || rcode == 3) {
                            TunnelLogBuffer.recordTraffic(q.size + 2, respLen + 2, 1)
                            return Pair(true, "dns_tcp_ok_${respLen}B")
                        }
                    }
                    return Pair(false, "dns_tcp_invalid")
                }

                Pair(false, "no_probe_payload")
            }
        } catch (e: Exception) {
            Pair(false, e.javaClass.simpleName + ": " + (e.message ?: "error"))
        }
    }
}
