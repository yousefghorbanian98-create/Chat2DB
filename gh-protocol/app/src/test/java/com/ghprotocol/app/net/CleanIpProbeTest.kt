package com.ghprotocol.app.net

import com.ghprotocol.app.core.net.CleanIpPool
import com.ghprotocol.app.core.net.IpProbeResult
import com.ghprotocol.app.core.net.TlsHttpProbe
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNotNull
import org.junit.Assert.assertTrue
import org.junit.Test
import java.net.InetSocketAddress
import java.net.ServerSocket
import java.net.Socket

class CleanIpProbeTest {

    private fun probeFor(port: Int, timeoutMs: Int = 2000) = TlsHttpProbe(
        sni = "localhost",
        port = port,
        hostHeader = "localhost",
        timeoutMs = timeoutMs,
        sslSocketFactory = { TestNet.trustAllFactory(TestNet.testSslContext()) },
        validatePoolEntry = false,
        connect = { ip, p, timeout ->
            Socket().apply {
                tcpNoDelay = true
                connect(InetSocketAddress(ip, p), timeout)
            }
        }
    )

    @Test
    fun poolRejectsPrivateReservedAndNonLiteralEntries() {
        for (bad in listOf(
            "127.0.0.1", "10.0.0.1", "192.168.1.1", "172.16.5.5", "169.254.1.1",
            "0.0.0.0", "224.0.0.1", "255.255.255.255", "100.64.0.1",
            "192.0.2.1", "198.51.100.7", "203.0.113.9", "198.18.0.1",
            "cloudflare.com", "2606:4700::1111", ""
        )) {
            assertFalse("$bad must be rejected", CleanIpPool.isValid(bad))
        }
        assertTrue(CleanIpPool.isValid("104.16.248.249"))
        assertTrue(CleanIpPool.isValid("172.64.32.229"))
        assertTrue("default pool must only contain valid public IPv4 edges",
            CleanIpPool.CLOUDFLARE_EDGES.all { CleanIpPool.isValid(it) })
        assertTrue(CleanIpPool.CLOUDFLARE_EDGES.size >= 8)
        assertFalse("1.1.1.1:443 is IP-blocked on Iranian ISPs", CleanIpPool.CLOUDFLARE_EDGES.contains("1.1.1.1"))
    }

    @Test
    fun acceptsOnlyTlsHttpWithCloudflareMarker() {
        TestNet.TlsHttpServer().use { server ->
            val result = probeFor(server.port).probe("127.0.0.1")
            assertTrue(result.stage + ":" + result.detail, result.ok)
            assertEquals(IpProbeResult.STAGE_OK, result.stage)
            assertTrue("must prove the peer is a Cloudflare edge", result.cloudflareEdge)
            assertEquals(403, result.httpStatus)
            assertTrue(server.accepts >= 1)
        }
    }

    @Test
    fun rejectsServerWithoutCloudflareMarker() {
        TestNet.TlsHttpServer(extraHeaders = listOf("server: nginx")).use { server ->
            val result = probeFor(server.port).probe("127.0.0.1")
            assertFalse("a generic TLS server is not a clean Cloudflare edge", result.ok)
            assertEquals(IpProbeResult.STAGE_CF_RAY, result.stage)
        }
    }

    @Test
    fun plainTcpListenerIsNeverConsideredHealthy() {
        // Accepts TCP, never speaks TLS: the old probe would have scored this as "healthy".
        TestNet.SilentServer().use { silent ->
            val result = probeFor(silent.port, timeoutMs = 600).probe("127.0.0.1")
            assertFalse(result.ok)
            assertEquals(IpProbeResult.STAGE_TLS, result.stage)
        }
    }

    @Test
    fun tlsWithoutHttpResponseIsRejected() {
        ServerSocket(0).use { raw ->
            val acceptor = Thread {
                try {
                    raw.accept().use { client ->
                        client.getInputStream().read(ByteArray(1024))
                    }
                } catch (_: Exception) {
                }
            }.apply { isDaemon = true; start() }
            val result = probeFor(raw.localPort, timeoutMs = 500).probe("127.0.0.1")
            assertFalse(result.ok)
            assertNotNull(result.stage)
            assertTrue(result.stage == IpProbeResult.STAGE_TLS || result.stage == IpProbeResult.STAGE_HTTP)
            acceptor.interrupt()
        }
    }

    @Test
    fun invalidIpIsRejectedBeforeAnyNetworkCall() {
        var connected = false
        val probe = TlsHttpProbe(
            sni = "localhost", port = 443, hostHeader = "localhost", timeoutMs = 100,
            connect = { _, _, _ -> connected = true; error("must not connect") }
        )
        val result = probe.probe("10.1.2.3")
        assertFalse(result.ok)
        assertEquals(IpProbeResult.STAGE_INVALID, result.stage)
        assertFalse(connected)
    }
}
