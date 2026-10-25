package com.ghprotocol.app.core.net

import java.io.InputStream
import java.net.InetSocketAddress
import java.net.Socket
import javax.net.ssl.SSLSocket
import javax.net.ssl.SSLSocketFactory

/** Structural validity of a clean-IP candidate (no DNS, no network). */
object CleanIpPool {

    /**
     * Public unicast IPv4 ranges only. Private, loopback, link-local, CGNAT, multicast,
     * broadcast, "this network" and documentation ranges are rejected before any probe runs.
     */
    fun rejectReason(ip: String): String? {
        val bytes = PacketCodec.ipBytes(ip) ?: return "not_a_literal_ip"
        if (bytes.size != 4) return "not_ipv4"
        val a = bytes[0].toInt() and 0xFF
        val b = bytes[1].toInt() and 0xFF
        val c = bytes[2].toInt() and 0xFF
        val d = bytes[3].toInt() and 0xFF
        return when {
            a == 0 -> "this_network"
            a == 10 -> "private"
            a == 127 -> "loopback"
            a == 169 && b == 254 -> "link_local"
            a == 172 && b in 16..31 -> "private"
            a == 192 && b == 168 -> "private"
            a == 100 && b in 64..127 -> "cgnat"
            a in 224..239 -> "multicast"
            a >= 240 -> "reserved"
            a == 255 && b == 255 && c == 255 && d == 255 -> "broadcast"
            a == 192 && b == 0 && c == 2 -> "documentation"
            a == 198 && (b == 18 || b == 19) -> "benchmarking"
            a == 198 && b == 51 && c == 100 -> "documentation"
            a == 203 && b == 0 && c == 113 -> "documentation"
            else -> null
        }
    }

    fun isValid(ip: String): Boolean = rejectReason(ip) == null

    /**
     * Cloudflare anycast edges. Kept deliberately small and real: every entry is an
     * address that Cloudflare answers TLS on. `1.1.1.1` / `1.0.0.1` are excluded on purpose
     * (their :443 is IP-blocked on several Iranian ISPs, see DIAGNOSIS §D1).
     */
    val CLOUDFLARE_EDGES: List<String> = listOf(
        "104.16.248.249", "104.16.249.249", // cloudflare-dns.com itself
        "104.18.94.41", "104.18.95.41",     // challenges.cloudflare.com
        "104.16.132.229", "104.16.133.229",
        "104.18.12.149", "104.18.13.149",
        "172.64.32.229", "172.64.33.229",
        "188.114.96.229", "188.114.97.229",
        "190.93.240.229", "198.41.200.229"
    ).filter { isValid(it) }.distinct()
}

data class IpProbeResult(
    val ip: String,
    val ok: Boolean,
    val stage: String,
    val detail: String,
    val latencyMs: Long,
    val httpStatus: Int = -1,
    val cloudflareEdge: Boolean = false,
    val certificateSubject: String? = null
) {
    companion object {
        const val STAGE_INVALID = "invalid_ip"
        const val STAGE_TCP = "tcp"
        const val STAGE_TLS = "tls"
        const val STAGE_HTTP = "http"
        const val STAGE_CF_RAY = "cf_ray"
        const val STAGE_OK = "ok"
    }
}

/** Injectable seam so the scanner (and its tests) never depend on a concrete TLS client. */
interface IpProbe {
    fun probe(ip: String): IpProbeResult
}

/**
 * Clean-IP probe: a real TLS handshake (validating the certificate chain against the system
 * trust store) followed by a complete HTTP/1.1 exchange, and — because this app only swaps
 * the egress address of Cloudflare-fronted destinations — proof that the peer really is a
 * Cloudflare edge (`cf-ray` header / `Server: Cloudflare`).
 *
 * A TCP connect or a partial ClientHello is *never* treated as a healthy IP.
 */
class TlsHttpProbe(
    private val sni: String = "cloudflare-dns.com",
    private val port: Int = 443,
    private val path: String = "/",
    private val hostHeader: String = sni,
    private val timeoutMs: Int = 2500,
    private val sslSocketFactory: () -> SSLSocketFactory = { SSLSocketFactory.getDefault() as SSLSocketFactory },
    /**
     * Clean-IP substitution deliberately connects to an IP that is not the zone apex of the
     * SNI, so hostname verification is not required here; the certificate **chain** is still
     * validated by the trusted `SSLSocketFactory`, and the Cloudflare marker proves the edge.
     */
    private val verifyHostname: Boolean = false,
    /** Production always validates the pool entry; tests disable it to probe loopback servers. */
    private val validatePoolEntry: Boolean = true,
    private val connect: (String, Int, Int) -> Socket = { ip, p, timeout ->
        Socket().apply {
            tcpNoDelay = true
            connect(InetSocketAddress(ip, p), timeout)
        }
    }
) : IpProbe {

    override fun probe(ip: String): IpProbeResult {
        val started = System.currentTimeMillis()
        if (validatePoolEntry) {
            CleanIpPool.rejectReason(ip)?.let {
                return IpProbeResult(ip, false, IpProbeResult.STAGE_INVALID, it, 0)
            }
        }
        val raw = try {
            connect(ip, port, timeoutMs)
        } catch (e: Exception) {
            return IpProbeResult(ip, false, IpProbeResult.STAGE_TCP, describe(e), elapsed(started))
        }
        var stage = IpProbeResult.STAGE_TLS
        try {
            raw.soTimeout = timeoutMs
            val ssl = sslSocketFactory().createSocket(raw, sni, port, true) as SSLSocket
            ssl.use { tls ->
                tls.soTimeout = timeoutMs
                if (verifyHostname) {
                    val params = tls.sslParameters
                    params.endpointIdentificationAlgorithm = "HTTPS"
                    tls.sslParameters = params
                }
                tls.startHandshake()
                val subject = try {
                    val cert = tls.session.peerCertificates.firstOrNull()
                    if (cert != null) (cert as? java.security.cert.X509Certificate)?.subjectDN?.name else null
                } catch (_: Exception) {
                    null
                }
                stage = IpProbeResult.STAGE_HTTP
                val out = tls.getOutputStream()
                val request = (
                    "HEAD $path HTTP/1.1\r\n" +
                        "Host: $hostHeader\r\n" +
                        "User-Agent: GhProtocol/1.6 (clean-ip probe)\r\n" +
                        "Accept: */*\r\n" +
                        "Connection: close\r\n\r\n"
                    ).toByteArray(Charsets.US_ASCII)
                out.write(request)
                out.flush()
                val headers = readHeaders(tls.getInputStream(), timeoutMs)
                    ?: return IpProbeResult(
                        ip, false, IpProbeResult.STAGE_HTTP,
                        "no_http_response", elapsed(started), certificateSubject = subject
                    )
                val statusLine = headers.lineSequence().firstOrNull().orEmpty()
                val status = parseStatus(statusLine)
                if (status < 0) {
                    return IpProbeResult(
                        ip, false, IpProbeResult.STAGE_HTTP,
                        "bad_status_line:" + statusLine.take(40), elapsed(started),
                        certificateSubject = subject
                    )
                }
                val lower = headers.lowercase()
                val cloudflare = lower.contains("cf-ray:") || lower.contains("server: cloudflare")
                if (!cloudflare) {
                    return IpProbeResult(
                        ip, false, IpProbeResult.STAGE_CF_RAY,
                        "no_cloudflare_marker", elapsed(started), status, certificateSubject = subject
                    )
                }
                return IpProbeResult(
                    ip, true, IpProbeResult.STAGE_OK, "headers_ok", elapsed(started), status,
                    cloudflareEdge = true, certificateSubject = subject
                )
            }
        } catch (e: Exception) {
            return IpProbeResult(ip, false, stage, describe(e), elapsed(started))
        } finally {
            try { raw.close() } catch (_: Exception) { /* already closed */ }
        }
    }

    private fun readHeaders(input: InputStream, timeoutMs: Int): String? {
        val deadline = System.currentTimeMillis() + timeoutMs
        val buffer = java.io.ByteArrayOutputStream()
        while (System.currentTimeMillis() < deadline) {
            val b = input.read()
            if (b < 0) break
            buffer.write(b)
            val size = buffer.size()
            if (size >= 4) {
                val data = buffer.toByteArray()
                if (data[size - 4] == '\r'.code.toByte() && data[size - 3] == '\n'.code.toByte() &&
                    data[size - 2] == '\r'.code.toByte() && data[size - 1] == '\n'.code.toByte()
                ) {
                    return String(data, 0, size, Charsets.ISO_8859_1)
                }
            }
            if (size > 16 * 1024) break
        }
        return null
    }

    private fun parseStatus(statusLine: String): Int {
        val parts = statusLine.trim().split(' ')
        if (parts.size < 2 || !parts[0].startsWith("HTTP/1.")) return -1
        return parts[1].toIntOrNull() ?: -1
    }

    private fun describe(e: Exception): String = e.javaClass.simpleName + ": " + (e.message ?: "error")

    private fun elapsed(started: Long): Long = (System.currentTimeMillis() - started).coerceAtLeast(1L)
}
