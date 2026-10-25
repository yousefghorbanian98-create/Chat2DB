package com.ghprotocol.app.net

import com.ghprotocol.app.core.net.DnsCache
import com.ghprotocol.app.core.net.DnsMessage
import com.ghprotocol.app.core.net.DnsResolution
import com.ghprotocol.app.core.net.DnsResolver
import com.ghprotocol.app.core.net.DnsTransport
import com.ghprotocol.app.core.net.DnsTransportResult
import com.ghprotocol.app.core.net.DohEndpoint
import com.ghprotocol.app.core.net.DohTransport
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNotNull
import org.junit.Assert.assertTrue
import org.junit.Test
import java.util.Collections
import java.util.concurrent.atomic.AtomicLong

class DnsResolverTest {

    private class FakeTransport(
        override val name: String,
        private val delayMs: Long = 0,
        private val behaviour: (ByteArray) -> DnsTransportResult
    ) : DnsTransport {
        val calls = Collections.synchronizedList(ArrayList<Int>())
        override fun exchange(query: ByteArray, timeoutMs: Int): DnsTransportResult {
            calls.add(timeoutMs)
            if (delayMs > 0) Thread.sleep(delayMs)
            return behaviour(query)
        }
    }

    private val query = TestDns.query("example.com", DnsMessage.TYPE_A, id = 0x1111)

    @Test
    fun acceptsValidatedAnswerAndCachesWithRealTtl() {
        val valid = TestDns.response(query, listOf("93.184.216.34"), ttl = 30)
        val transport = FakeTransport("doh:test") { DnsTransportResult(valid, "ok", 5) }
        val cache = DnsCache()
        val resolver = DnsResolver(listOf(transport), cache = cache)
        val first = resolver.resolve(query)
        assertTrue(first.ok)
        assertEquals("doh:test", first.path)
        assertFalse(first.fromCache)
        assertEquals(1, transport.calls.size)

        val second = resolver.resolve(query)
        assertTrue(second.fromCache)
        assertEquals("cache", second.path)
        assertEquals(1, transport.calls.size)

        // A different transaction ID still gets the cached answer, rewritten to its own ID.
        val otherId = TestDns.query("example.com", DnsMessage.TYPE_A, id = 0x2222)
        val third = resolver.resolve(otherId)
        assertEquals(0x2222, com.ghprotocol.app.core.net.PacketCodec.readU16(third.response, 0))
        assertTrue(DnsMessage.isResponseTo(third.response, otherId))
    }

    @Test
    fun rejectsMismatchedTransactionIdAndFallsThrough() {
        val wrongId = TestDns.responseWithId(query, 0x9999)
        val good = TestDns.response(query, listOf("1.2.3.4"))
        val bad = FakeTransport("doh:bad") { DnsTransportResult(wrongId, "ok", 3) }
        val second = FakeTransport("doh:good") { DnsTransportResult(good, "ok", 4) }
        val resolution = DnsResolver(listOf(bad, second)).resolve(query)
        assertTrue(resolution.ok)
        assertEquals("doh:good", resolution.path)
        assertFalse("a response with the wrong transaction ID must not be accepted", resolution.attempts.first().ok)
        assertTrue(resolution.attempts.first().detail.startsWith("transaction_id_mismatch"))
    }

    @Test
    fun rejectsResponseToAnotherQuestion() {
        val otherQuery = TestDns.query("evil.example", DnsMessage.TYPE_A, id = 0x1111)
        val answer = TestDns.response(otherQuery)
        val transport = FakeTransport("doh:wrong-question") { DnsTransportResult(answer, "ok", 2) }
        val resolution = DnsResolver(listOf(transport)).resolve(query)
        assertTrue("must degrade to SERVFAIL, never a wrong answer", resolution.isServfail)
        assertEquals(DnsResolution.PATH_SERVFAIL, resolution.path)
        assertTrue(resolution.attempts.first().detail.contains("question"))
    }

    @Test
    fun returnsRealServfailWhenEveryPathFails() {
        val a = FakeTransport("doh:a") { DnsTransportResult(null, "timeout", 2500) }
        val b = FakeTransport("tcp:b") { DnsTransportResult(null, "refused", 100) }
        val resolution = DnsResolver(listOf(a, b), budgetMs = 4000).resolve(query)
        assertTrue(resolution.isServfail)
        assertNotNull(resolution.response)
        val view = DnsMessage.parse(resolution.response) ?: error("unparseable servfail")
        assertEquals(DnsMessage.RCODE_SERVFAIL, view.rcode)
        assertEquals(0x1111, view.id)
        assertTrue(DnsMessage.isResponseTo(resolution.response, query))
        assertEquals(2, resolution.attempts.size)
        assertTrue(resolution.ms >= 0)
    }

    @Test
    fun budgetIsEnforcedSoNoAppQueryCanHang() {
        // Three paths, each trying to consume far more time than the global budget.
        val slow = FakeTransport("slow", delayMs = 400) { DnsTransportResult(null, "timeout", 10_000) }
        val resolution = DnsResolver(listOf(slow, slow, slow, slow), budgetMs = 700, perPathMaxMs = 400).resolve(query)
        assertTrue(resolution.isServfail)
        assertTrue("must stop early, took ${resolution.ms}ms", resolution.ms < 2500)
        assertTrue(resolution.attempts.size < 4)
    }

    @Test
    fun neverSynthesisesAaaaAnswers() {
        val aaaaQuery = TestDns.query("example.com", DnsMessage.TYPE_AAAA, id = 0x3333)
        val transport = FakeTransport("doh:test") { DnsTransportResult(null, "timeout", 1) }
        val resolution = DnsResolver(listOf(transport)).resolve(aaaaQuery)
        assertTrue(resolution.isServfail)
        val view = DnsMessage.parse(resolution.response) ?: error("unparseable")
        assertEquals("AAAA failure must be SERVFAIL, never a fake NODATA", DnsMessage.RCODE_SERVFAIL, view.rcode)
        assertEquals(0, view.answerCount)
    }

    @Test
    fun nonOkRcodesAreNotCachedButStillReturned() {
        val nxdomain = TestDns.response(query, answers = emptyList(), rcode = DnsMessage.RCODE_NXDOMAIN)
        val transport = FakeTransport("doh:nx") { DnsTransportResult(nxdomain, "ok", 1) }
        val cache = DnsCache()
        val resolver = DnsResolver(listOf(transport), cache = cache)
        val first = resolver.resolve(query)
        assertTrue(first.ok)
        val second = resolver.resolve(query)
        assertFalse(second.fromCache)
        assertEquals(2, transport.calls.size)
    }

    @Test
    fun clientUdpSizeTruncatesInsteadOfOverflowing() {
        val answers = (1..40).map { "10.0.0.$it" }
        val big = TestDns.response(query, answers)
        assertTrue(big.size > 512)
        val transport = FakeTransport("doh:big") { DnsTransportResult(big, "ok", 1) }
        val resolution = DnsResolver(listOf(transport)).resolve(query)
        assertTrue("reply must fit the 512-byte default client buffer", resolution.response.size <= 512)
        val view = DnsMessage.parse(resolution.response) ?: error("unparseable")
        assertTrue(view.truncated)
    }

    @Test
    fun malformedQueryGetsFormerr() {
        val resolution = DnsResolver(emptyList()).resolve(byteArrayOf(1, 2, 3))
        assertTrue(resolution.isServfail)
        assertTrue(resolution.attempts.first().detail == "malformed_query")
    }

    @Test
    fun testClockIsHonouredForCacheExpiry() {
        val now = AtomicLong(0)
        val cache = DnsCache(clock = { now.get() })
        val valid = TestDns.response(query, listOf("93.184.216.34"), ttl = 10)
        val transport = FakeTransport("doh:test") { DnsTransportResult(valid, "ok", 1) }
        val resolver = DnsResolver(listOf(transport), cache = cache, clock = { now.get() })
        resolver.resolve(query)
        now.set(5_000)
        assertTrue(resolver.resolve(query).fromCache)
        now.set(11_000)
        assertFalse("cache must expire at the answer TTL", resolver.resolve(query).fromCache)
    }

    @Test
    fun dohTransportCompletesRealTlsHandshakeAndHttpExchange() {
        TestNet.DohServer(answer = { request -> TestDns.response(request, listOf("93.184.216.34")) }).use { server ->
            TestNet.SocksServer().use { socks ->
                val endpoint = DohEndpoint(
                    displayName = "test-doh",
                    host = "localhost",
                    path = "/dns-query",
                    bootstrapIps = listOf("127.0.0.1"),
                    port = server.port
                )
                val context = TestNet.testSslContext()
                val transport = DohTransport(
                    connector = TestNet.connectorFor(socks),
                    endpoint = endpoint,
                    sslSocketFactory = { TestNet.trustAllFactory(context) },
                    verifyHostname = false
                )
                val result = transport.exchange(query, 3000)
                assertNotNull("DoH transport returned no bytes: ${result.detail}", result.response)
                val response = result.response ?: ByteArray(0)
                assertTrue(DnsMessage.isResponseTo(response, query))
                assertEquals(1, server.requests)
                assertEquals("/dns-query", server.lastPath)
                assertTrue("TCP+TLS+HTTP must all have happened", socks.connections >= 1)
            }
        }
    }

    @Test
    fun dohTransportSurvivesWrongPathAndReportsFailure() {
        TestNet.DohServer(answer = { req -> TestDns.response(req) }, responseCode = 200).use { server ->
            TestNet.SocksServer().use { socks ->
                val endpoint = DohEndpoint("test-doh", "localhost", "/wrong", listOf("127.0.0.1"), server.port)
                val context = TestNet.testSslContext()
                val transport = DohTransport(
                    TestNet.connectorFor(socks), endpoint,
                    sslSocketFactory = { TestNet.trustAllFactory(context) },
                    verifyHostname = false
                )
                val result = transport.exchange(query, 2000)
                assertTrue("non-200 must not be accepted", result.response == null)
                assertTrue(result.detail.contains("404") || result.detail.contains("http_status"))
            }
        }
    }
}
