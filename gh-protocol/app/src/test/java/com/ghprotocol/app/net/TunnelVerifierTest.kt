package com.ghprotocol.app.net

import com.ghprotocol.app.core.TunnelVerifier
import com.ghprotocol.app.core.net.SocksConnectResult
import com.ghprotocol.app.core.net.SocksConnector
import com.ghprotocol.app.core.net.TunnelEndpoints
import com.ghprotocol.app.core.net.TunnelSelfTestResult
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

/**
 * Verifier rules (requirement 5): a reachable socket, an open SOCKS port or a bare TCP
 * connect is never "verified". Only a real remote payload — and, for the tunnel state, only
 * a self-test through the relay — may report success.
 */
class TunnelVerifierTest {

    /** Rewrites every CONNECT to a local origin so the test never needs real egress. */
    private class RedirectingConnector(
        private val delegate: SocksConnector,
        private val host: String,
        private val port: Int
    ) : SocksConnector {
        override fun connect(host: String, port: Int, connectTimeoutMs: Int, replyTimeoutMs: Int): SocksConnectResult =
            delegate.connect(this.host, this.port, connectTimeoutMs, replyTimeoutMs)
    }

    @Test
    fun realHttpPayloadThroughSocksIsAccepted() {
        TestNet.HttpServer().use { origin ->
            TestNet.SocksServer().use { socks ->
                val result = TunnelVerifier.verifyThroughSocks5(
                    timeoutMs = 4000,
                    connector = RedirectingConnector(
                        TestNet.standaloneConnector(socks.port), "127.0.0.1", origin.port
                    )
                )
                assertTrue("real HTTP payload must be accepted", result.egressOk)
                assertTrue("response bytes must be counted", result.responseBytes > 0)
                assertTrue("request bytes must be counted", result.requestBytes > 0)
                assertTrue(origin.requests == 1)
                assertTrue(result.stages.any { it.name.startsWith("payload_response") && it.ok })
                // Egress alone is still not "verified": the tunnel self-test must pass too.
                assertFalse(result.payloadVerified)
                assertFalse(result.ok)
            }
        }
    }

    @Test
    fun silentPeerIsNotAcceptedAsPayload() {
        TestNet.SilentServer().use { silent ->
            TestNet.SocksServer().use { socks ->
                val result = TunnelVerifier.verifyThroughSocks5(
                    timeoutMs = 800,
                    connector = RedirectingConnector(
                        TestNet.standaloneConnector(socks.port), "127.0.0.1", silent.port
                    )
                )
                assertFalse("an accepted socket with no payload is not success", result.egressOk)
                assertEquals(0, result.responseBytes)
            }
        }
    }

    @Test
    fun unreachableProxyIsReportedAsStageNotAsSuccess() {
        val failing = object : SocksConnector {
            override fun connect(host: String, port: Int, connectTimeoutMs: Int, replyTimeoutMs: Int): SocksConnectResult =
                SocksConnectResult(null, "tcp_proxy", "ConnectException:connection refused", 3)
        }
        val result = TunnelVerifier.verifyThroughSocks5(timeoutMs = 500, connector = failing)
        assertFalse(result.egressOk)
        assertEquals(-1, result.latencyMs)
        assertTrue(result.stages.first().name.startsWith("socks_connect"))
        assertTrue(result.stages.first().detail.contains("tcp_proxy"))
    }

    @Test
    fun proxyReachabilityAloneNeverReportsEgress() {
        TestNet.SocksServer().use { socks ->
            TestNet.HttpServer().use { origin ->
                val result = TunnelVerifier.verifyProxyReachable(
                    proxyHost = "127.0.0.1",
                    proxyPort = socks.port,
                    targetHost = "127.0.0.1",
                    targetPort = origin.port,
                    timeoutMs = 2000
                )
                assertTrue("SOCKS5 greeting+CONNECT must succeed", result.stages.first().ok)
                assertFalse("a SOCKS greeting is not egress proof", result.egressOk)
                assertFalse(result.payloadVerified)
            }
        }
    }

    @Test
    fun combineDemandsTunnelPayload() {
        val egressOnly = TunnelVerifier.verifyProxyReachable("127.0.0.1", 1, timeoutMs = 50)
        val noPayload = TunnelVerifier.combine(egressOnly, null)
        assertFalse(noPayload.payloadVerified)
        assertFalse(noPayload.ok)

        val failedSelfTest = TunnelSelfTestResult(
            ok = false, stage = "syn_ack", detail = "no_syn_ack", target = "1.1.1.1:80",
            latencyMs = 9000, requestBytes = 40, responseBytes = 0,
            synAckMs = -1, firstByteMs = -1, upBytesDelta = 0, downBytesDelta = 0, checksumErrors = 0
        )
        assertFalse(TunnelVerifier.combine(egressOnly, failedSelfTest).ok)

        val okSelfTest = failedSelfTest.copy(
            ok = true, stage = "ok", detail = "payload_ok", responseBytes = 64,
            upBytesDelta = 40, downBytesDelta = 64, latencyMs = 120
        )
        val combined = TunnelVerifier.combine(egressOnly, okSelfTest)
        assertTrue(combined.payloadVerified)
        assertTrue(combined.stages.any { it.name == "relay_payload" && it.ok })
    }

    @Test
    fun selfTestRequestsAreWellFormedAndRepliesValidated() {
        val httpTarget = TunnelEndpoints.SelfTestTarget("1.1.1.1", 80, "one.one.one.one", "/cdn-cgi/trace")
        val request = String(TunnelEndpoints.selfTestRequest(httpTarget), Charsets.US_ASCII)
        assertTrue(request.startsWith("GET /cdn-cgi/trace HTTP/1.0\r\n"))
        assertTrue(request.contains("Host: one.one.one.one\r\n"))
        assertTrue(TunnelEndpoints.isExpectedReply(httpTarget, "HTTP/1.0 200 OK\r\n".toByteArray()))
        assertFalse(TunnelEndpoints.isExpectedReply(httpTarget, "SSH-2.0-OpenSSH".toByteArray()))
        assertFalse(TunnelEndpoints.isExpectedReply(httpTarget, ByteArray(0)))

        val dnsTarget = TunnelEndpoints.SelfTestTarget("8.8.8.8", 53, "dns.google", null)
        val query = TunnelEndpoints.selfTestRequest(dnsTarget, "example.com")
        val reply = com.ghprotocol.app.core.net.DnsMessage.buildFailure(
            query,
            com.ghprotocol.app.core.net.DnsMessage.RCODE_SERVFAIL
        )
        assertTrue("a real DNS reply is an acceptable payload", TunnelEndpoints.isExpectedReply(dnsTarget, reply))
        assertFalse(TunnelEndpoints.isExpectedReply(dnsTarget, ByteArray(4)))
    }

    @Test
    fun masksDestinationsForLogs() {
        assertEquals("142.250.x.x", TunnelVerifier.masked("142.250.185.78"))
        assertTrue(TunnelVerifier.masked("2001:db8::1").contains(":"))
    }
}
