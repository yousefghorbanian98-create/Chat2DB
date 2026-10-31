package com.ghprotocol.app.core.net

/**
 * Every address/port constant of the tunnel, in an **Android-free** object so the whole
 * data path (relay, DNS, verifier, self-test) can be compiled and tested on a plain JVM.
 */
object TunnelEndpoints {

    const val PROXY_HOST = "127.0.0.1"
    const val PROXY_PORT = 10808

    /** Xray `dokodemo-door` DNS inbound injected by [com.ghprotocol.app.core.ConfigPatcher]. */
    const val DNS_IN_PORT = 15353

    const val MTU = 1500
    const val TUN_IPV4 = "10.8.0.2"
    const val TUN_IPV4_PREFIX = 24
    const val TUN_GATEWAY_V4 = "10.8.0.1"
    const val TUN_IPV6 = "fd00:1::2"
    const val TUN_IPV6_PREFIX = 64
    const val TUN_GATEWAY_V6 = "fd00:1::1"

    /** A destination used to prove a *real* remote payload inside the tunnel. */
    data class SelfTestTarget(
        val ip: String,
        val port: Int,
        val hostHeader: String,
        val path: String?,
        val tcpDns: Boolean = false
    )

    /**
     * Ordered self-test targets. Each one must produce a remote-to-local payload, not just a
     * handshake: an HTTP status line for the first two, a validated DNS reply for the third.
     */
    val SELF_TEST_TARGETS: List<SelfTestTarget> = listOf(
        SelfTestTarget("1.1.1.1", 80, "one.one.one.one", "/cdn-cgi/trace"),
        SelfTestTarget("104.16.248.249", 80, "cp.cloudflare.com", "/cdn-cgi/trace"),
        SelfTestTarget("8.8.8.8", 53, "dns.google", null, tcpDns = true)
    )

    /** Request bytes for a self-test target (pure, unit-tested). */
    fun selfTestRequest(target: SelfTestTarget, dnsName: String = "example.com"): ByteArray =
        if (target.tcpDns || target.path == null) {
            DnsMessage.buildQuery(dnsName)
        } else {
            (
                "GET ${target.path} HTTP/1.0\r\n" +
                    "Host: ${target.hostHeader}\r\n" +
                    "User-Agent: GhProtocol-selftest/1.6\r\n" +
                    "\r\n"
                ).toByteArray(Charsets.US_ASCII)
        }

    /** True when [bytes] is a real, well-formed remote reply for [target]. */
    fun isExpectedReply(target: SelfTestTarget, bytes: ByteArray): Boolean {
        if (bytes.isEmpty()) return false
        if (target.tcpDns || target.path == null) {
            val view = DnsMessage.parse(bytes) ?: return false
            return view.isResponse
        }
        val text = String(bytes, Charsets.ISO_8859_1)
        return text.startsWith("HTTP/1.")
    }
}
