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
        val hostHeader: String
    )

    private val TARGETS = listOf(
        ProbeTarget("1.1.1.1", 80, "/cdn-cgi/trace", "1.1.1.1"),
        ProbeTarget("www.google.com", 80, "/generate_204", "www.google.com"),
        ProbeTarget("1.1.1.1", 443, null, "1.1.1.1")
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
                    val req = "GET ${target.httpPath} HTTP/1.1\r\nHost: ${target.hostHeader}\r\nUser-Agent: GhProtocol/1.1\r\nConnection: close\r\n\r\n"
                    out.write(req.toByteArray(Charsets.US_ASCII))
                    out.flush()
                    val buf = ByteArray(256)
                    val n = s.getInputStream().read(buf)
                    if (n <= 0) {
                        return Pair(false, "http_empty_reply")
                    }
                    val statusLine = String(buf, 0, n, Charsets.US_ASCII).lineSequence().firstOrNull().orEmpty()
                    if (statusLine.startsWith("HTTP/1.")) {
                        return Pair(true, statusLine.trim())
                    }
                    return Pair(false, "invalid_http_status")
                }

                Pair(true, "tcp_handshake_ok")
            }
        } catch (e: Exception) {
            Pair(false, e.javaClass.simpleName + ": " + (e.message ?: "error"))
        }
    }
}
