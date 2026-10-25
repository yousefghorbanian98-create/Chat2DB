package com.ghprotocol.app.core

import com.ghprotocol.app.core.net.DnsMessage
import com.ghprotocol.app.core.net.DnsResolver
import com.ghprotocol.app.core.net.PacketCodec
import com.ghprotocol.app.core.net.Socks5Connector
import com.ghprotocol.app.core.net.SocksConnectResult
import com.ghprotocol.app.core.net.SocksConnector
import com.ghprotocol.app.core.net.TunnelEndpoints
import com.ghprotocol.app.core.net.TunnelSelfTestResult

/** One hop of a verification run, with the stage name and the measured time. */
data class VerifyStage(
    val name: String,
    val ok: Boolean,
    val detail: String,
    val ms: Long
)

/**
 * Result of a verification run.
 *
 * [egressOk] means *Xray answered with real remote bytes* through its SOCKS inbound. It does
 * **not** prove the phone's datapath works — that needs [payloadVerified], which is only set
 * by a [com.ghprotocol.app.core.net.TunnelSelfTest] executed against the live relay.
 */
data class TunnelVerifyResult(
    val egressOk: Boolean,
    val payloadVerified: Boolean,
    val latencyMs: Int,
    val target: String,
    val detail: String,
    val stages: List<VerifyStage> = emptyList(),
    val requestBytes: Int = 0,
    val responseBytes: Int = 0
) {
    /** True only when real remote payload crossed the tunnel (never a handshake alone). */
    val ok: Boolean get() = egressOk && payloadVerified

    fun summary(): String = stages.joinToString(" | ") {
        "${it.name}=" + (if (it.ok) "ok" else it.detail)
    }
}

/**
 * Egress verification through Xray's loopback SOCKS5 inbound, staged so a failure names the
 * broken hop instead of timing out anonymously:
 * `socks_greeting` → `socks_connect` → `payload_request` → `payload_response`.
 *
 * Every target must return *real application bytes* (an HTTP status line or a DNS reply that
 * matches the query), so an open port or a half handshake can never be reported as success.
 * Byte counters are not touched here; the relay owns them.
 */
object TunnelVerifier {

    private data class Target(
        val ip: String,
        val port: Int,
        val hostHeader: String,
        val path: String?
    )

    private val TARGETS = listOf(
        Target("1.1.1.1", 80, "one.one.one.one", "/cdn-cgi/trace"),
        Target("104.16.248.249", 80, "cp.cloudflare.com", "/cdn-cgi/trace"),
        Target("8.8.8.8", 53, "dns.google", null)
    )

    fun connector(
        proxyHost: String = TunnelEndpoints.PROXY_HOST,
        proxyPort: Int = TunnelEndpoints.PROXY_PORT
    ): SocksConnector = Socks5Connector(proxyHost, proxyPort)

    /**
     * Stage 1 only: does the loopback port speak SOCKS5 and accept a CONNECT? This proves the
     * core is listening — *not* that any traffic can flow, and never sets `payloadVerified`.
     */
    fun verifyProxyReachable(
        proxyHost: String = TunnelEndpoints.PROXY_HOST,
        proxyPort: Int = TunnelEndpoints.PROXY_PORT,
        targetHost: String = "127.0.0.1",
        targetPort: Int = 80,
        timeoutMs: Int = 1500
    ): TunnelVerifyResult {
        val started = System.currentTimeMillis()
        val connect = connector(proxyHost, proxyPort).connect(targetHost, targetPort, timeoutMs, timeoutMs)
        closeQuietly(connect)
        val ms = (System.currentTimeMillis() - started).coerceAtLeast(1L)
        val stage = VerifyStage(
            "socks_greeting",
            connect.ok,
            if (connect.ok) "ok" else "${connect.stage}:${connect.detail}",
            ms
        )
        return TunnelVerifyResult(
            egressOk = false,
            payloadVerified = false,
            latencyMs = if (connect.ok) ms.toInt() else -1,
            target = "$proxyHost:$proxyPort",
            detail = stage.detail,
            stages = listOf(stage)
        )
    }

    /** Full egress check: SOCKS5 CONNECT + real HTTP/DNS payload from the remote end. */
    fun verifyThroughSocks5(
        proxyHost: String = TunnelEndpoints.PROXY_HOST,
        proxyPort: Int = TunnelEndpoints.PROXY_PORT,
        timeoutMs: Int = 4500,
        connector: SocksConnector = connector(proxyHost, proxyPort)
    ): TunnelVerifyResult {
        val stages = ArrayList<VerifyStage>()
        var lastDetail = "no_probe_target"
        var sent = 0
        var received = 0
        val started = System.currentTimeMillis()
        for (target in TARGETS) {
            val outcome = probe(connector, target, timeoutMs, stages)
            if (outcome.ok) {
                return TunnelVerifyResult(
                    egressOk = true,
                    payloadVerified = false,
                    latencyMs = (System.currentTimeMillis() - started).toInt().coerceAtLeast(1),
                    target = "${target.ip}:${target.port}",
                    detail = outcome.detail,
                    stages = stages.toList(),
                    requestBytes = outcome.sent,
                    responseBytes = outcome.received
                )
            }
            lastDetail = outcome.detail
            sent += outcome.sent
            received += outcome.received
        }
        return TunnelVerifyResult(
            egressOk = false,
            payloadVerified = false,
            latencyMs = -1,
            target = "$proxyHost:$proxyPort",
            detail = lastDetail,
            stages = stages.toList(),
            requestBytes = sent,
            responseBytes = received
        )
    }

    /**
     * Attach the in-tunnel self-test outcome. [ok] stays false unless remote payload really
     * came back through the datapath the apps use.
     */
    fun combine(egress: TunnelVerifyResult, selfTest: TunnelSelfTestResult?): TunnelVerifyResult {
        val extra = ArrayList(egress.stages)
        if (selfTest == null) {
            extra.add(VerifyStage("relay_payload", false, "not_run", 0))
        } else {
            extra.add(
                VerifyStage(
                    name = "relay_payload",
                    ok = selfTest.ok,
                    detail = if (selfTest.ok) "ok" else "${selfTest.stage}:${selfTest.detail}",
                    ms = selfTest.latencyMs
                )
            )
        }
        val verified = selfTest?.ok == true
        return egress.copy(
            payloadVerified = verified,
            stages = extra,
            latencyMs = if (egress.latencyMs > 0) egress.latencyMs else (selfTest?.latencyMs?.toInt() ?: -1)
        )
    }

    private data class Outcome(val ok: Boolean, val detail: String, val sent: Int, val received: Int)

    private fun probe(
        connector: SocksConnector,
        target: Target,
        timeoutMs: Int,
        stages: MutableList<VerifyStage>
    ): Outcome {
        val started = System.currentTimeMillis()
        fun elapsed() = (System.currentTimeMillis() - started).coerceAtLeast(0L)
        val connect = connector.connect(target.ip, target.port, timeoutMs, timeoutMs)
        val socket = connect.socket
        if (socket == null) {
            stages.add(VerifyStage("socks_connect ${target.ip}", false, "${connect.stage}:${connect.detail}", elapsed()))
            return Outcome(false, "${connect.stage}:${connect.detail}", 0, 0)
        }
        stages.add(VerifyStage("socks_connect ${target.ip}:${target.port}", true, "ok", connect.elapsedMs))
        try {
            socket.soTimeout = timeoutMs
            socket.tcpNoDelay = true
            val out = socket.getOutputStream()
            val input = socket.getInputStream()
            if (target.path == null) {
                // DNS over TCP through the tunnel (fallback probe).
                val query = DnsMessage.buildQuery("example.com")
                out.write(byteArrayOf(((query.size shr 8) and 0xFF).toByte(), (query.size and 0xFF).toByte()))
                out.write(query)
                out.flush()
                stages.add(VerifyStage("payload_request ${target.ip}", true, "${query.size}B", elapsed()))
                val length = readUnsignedShort(input)
                if (length !in 12..4096) {
                    stages.add(VerifyStage("payload_response ${target.ip}", false, "bad_length_$length", elapsed()))
                    return Outcome(false, "dns_bad_length", query.size + 2, 0)
                }
                val answer = ByteArray(length)
                var read = 0
                while (read < length) {
                    val n = input.read(answer, read, length - read)
                    if (n < 0) break
                    read += n
                }
                val mismatch = if (read == length) DnsMessage.mismatchReason(answer, query) else "short_read"
                if (mismatch != null) {
                    stages.add(VerifyStage("payload_response ${target.ip}", false, mismatch, elapsed()))
                    return Outcome(false, mismatch, query.size + 2, read)
                }
                stages.add(VerifyStage("payload_response ${target.ip}", true, "dns_ok_${length}B", elapsed()))
                return Outcome(true, "dns_tcp_ok", query.size + 2, length)
            }
            val request = (
                "GET ${target.path} HTTP/1.0\r\n" +
                    "Host: ${target.hostHeader}\r\n" +
                    "User-Agent: GhProtocol-verify/1.6\r\n\r\n"
                ).toByteArray(Charsets.US_ASCII)
            out.write(request)
            out.flush()
            stages.add(VerifyStage("payload_request ${target.ip}", true, "${request.size}B", elapsed()))
            val buffer = ByteArray(1520)
            val read = try {
                input.read(buffer)
            } catch (e: Exception) {
                val detail = describe(e)
                stages.add(VerifyStage("payload_response ${target.ip}", false, detail, elapsed()))
                return Outcome(false, detail, request.size, 0)
            }
            if (read <= 0) {
                stages.add(VerifyStage("payload_response ${target.ip}", false, "empty_reply", elapsed()))
                return Outcome(false, "empty_reply", request.size, 0)
            }
            val text = String(buffer, 0, read, Charsets.ISO_8859_1)
            val statusLine = text.lineSequence().firstOrNull().orEmpty().trim()
            val ok = statusLine.startsWith("HTTP/1.")
            stages.add(
                VerifyStage(
                    "payload_response ${target.ip}", ok,
                    if (ok) statusLine else "invalid_status:${statusLine.take(40)}", elapsed()
                )
            )
            return Outcome(ok, statusLine.ifEmpty { "invalid_status" }, request.size, read)
        } catch (e: Exception) {
            val detail = describe(e)
            stages.add(VerifyStage("payload ${target.ip}", false, detail, elapsed()))
            return Outcome(false, detail, 0, 0)
        } finally {
            closeQuietly(connect)
        }
    }

    /** DNS-only check used by the diagnostics screen (never fabricates an answer). */
    fun verifyDns(resolver: DnsResolver, name: String = "example.com"): TunnelVerifyResult {
        val query = DnsMessage.buildQuery(name)
        val resolution = resolver.resolve(query)
        val view = DnsMessage.parse(resolution.response)
        val answers = view?.answerCount ?: -1
        val valid = resolution.ok && view != null && view.isResponse && answers > 0 &&
            DnsMessage.mismatchReason(resolution.response, query) == null
        return TunnelVerifyResult(
            egressOk = valid,
            payloadVerified = false,
            latencyMs = resolution.ms.toInt(),
            target = "dns:$name",
            detail = resolver.describe(resolution),
            stages = listOf(
                VerifyStage("dns_resolve $name", valid, resolution.path + " answers=$answers", resolution.ms)
            ),
            requestBytes = query.size,
            responseBytes = resolution.response.size
        )
    }

    private fun readUnsignedShort(input: java.io.InputStream): Int {
        val hi = input.read()
        val lo = input.read()
        if (hi < 0 || lo < 0) return -1
        return ((hi and 0xFF) shl 8) or (lo and 0xFF)
    }

    private fun describe(e: Exception): String =
        e.javaClass.simpleName + ":" + (e.message ?: "error")

    private fun closeQuietly(connect: SocksConnectResult) {
        try {
            connect.socket?.close()
        } catch (_: Exception) {
            // already closed
        }
    }

    /** Masked destination helper re-exported for the UI/log layer. */
    fun masked(ip: String): String = PacketCodec.maskIp(ip)
}
