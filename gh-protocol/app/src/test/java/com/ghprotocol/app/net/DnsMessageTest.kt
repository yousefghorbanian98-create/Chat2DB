package com.ghprotocol.app.net

import com.ghprotocol.app.core.net.DnsMessage
import com.ghprotocol.app.core.net.PacketCodec
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNotNull
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Test

class DnsMessageTest {

    private val query = TestDns.query("example.com", DnsMessage.TYPE_A, id = 0x4d2)

    @Test
    fun parsesQueryAndResponseSections() {
        val view = DnsMessage.parse(query)
        assertNotNull(view)
        assertEquals(0x4d2, view?.id)
        assertFalse(view?.isResponse ?: true)
        assertEquals(1, view?.questionCount)
        assertEquals("example.com", view?.questions?.firstOrNull()?.name)
        assertEquals(DnsMessage.TYPE_A, view?.questions?.firstOrNull()?.type)

        val response = TestDns.response(query, listOf("93.184.216.34", "1.2.3.4"), ttl = 120)
        val responseView = DnsMessage.parse(response)
        assertNotNull(responseView)
        assertTrue(responseView?.isResponse ?: false)
        assertEquals(2, responseView?.answerCount)
        assertEquals(DnsMessage.RCODE_NOERROR, responseView?.rcode)
        assertEquals(120L, DnsMessage.minAnswerTtlSeconds(response))
    }

    @Test
    fun acceptsOnlyRepliesThatMatchIdAndQuestion() {
        val good = TestDns.response(query, listOf("93.184.216.34"))
        assertTrue(DnsMessage.isResponseTo(good, query))
        assertNull(DnsMessage.mismatchReason(good, query))

        val wrongId = TestDns.responseWithId(query, 0x7777)
        assertFalse(DnsMessage.isResponseTo(wrongId, query))
        assertTrue(DnsMessage.mismatchReason(wrongId, query)?.startsWith("transaction_id_mismatch") == true)

        val otherQuery = TestDns.query("example.org", DnsMessage.TYPE_A, id = 0x4d2)
        val wrongQuestion = TestDns.response(query)
        assertFalse(DnsMessage.isResponseTo(wrongQuestion, otherQuery))
        assertTrue(DnsMessage.mismatchReason(wrongQuestion, otherQuery)?.contains("question") == true)

        // A query echoed back as if it were a response must never be accepted.
        assertFalse(DnsMessage.isResponseTo(query, query))
    }

    @Test
    fun buildsRealServfailWithoutInventingRecords() {
        val servfail = DnsMessage.buildFailure(query, DnsMessage.RCODE_SERVFAIL)
        val view = DnsMessage.parse(servfail) ?: error("unparseable servfail")
        assertTrue(view.isResponse)
        assertEquals(DnsMessage.RCODE_SERVFAIL, view.rcode)
        assertEquals(0, view.answerCount)
        assertEquals(1, view.questionCount) // the question is echoed exactly once
        assertEquals("example.com", view.questions.firstOrNull()?.name)
        assertEquals(0x4d2, view.id)
        assertTrue(DnsMessage.isResponseTo(servfail, query))
    }

    @Test
    fun formErrAndNxDomainKeepTheQuestion() {
        for (rcode in listOf(DnsMessage.RCODE_FORMERR, DnsMessage.RCODE_NXDOMAIN, DnsMessage.RCODE_REFUSED)) {
            val answer = DnsMessage.buildFailure(query, rcode)
            val view = DnsMessage.parse(answer) ?: error("unparseable")
            assertEquals(rcode, view.rcode)
            assertEquals("example.com", view.questions.firstOrNull()?.name)
        }
    }

    @Test
    fun truncationSetsTcAndDropsAnswers() {
        val answer = TestDns.response(query, listOf("93.184.216.34"))
        val truncated = DnsMessage.truncateTo(query, answer, 40)
        val view = DnsMessage.parse(truncated) ?: error("unparseable")
        assertTrue(view.truncated)
        assertEquals(0, view.answerCount)
        assertEquals("example.com", view.questions.firstOrNull()?.name)
        assertEquals(answer, query.let { DnsMessage.truncateTo(query, answer, 4096) })
    }

    @Test
    fun cacheKeyIgnoresTransactionIdAndIsCaseInsensitive() {
        val a = TestDns.query("Example.COM", DnsMessage.TYPE_A, id = 1)
        val b = TestDns.query("example.com", DnsMessage.TYPE_A, id = 2)
        assertEquals(DnsMessage.cacheKey(a), DnsMessage.cacheKey(b))
        val aaaa = TestDns.query("example.com", DnsMessage.TYPE_AAAA, id = 3)
        assertTrue(DnsMessage.cacheKey(aaaa) != DnsMessage.cacheKey(a))
    }

    @Test
    fun parsedQuestionEndLetsUsRewriteIdsSafely() {
        val response = TestDns.response(query)
        val rewritten = DnsMessage.withTransactionId(response, TestDns.query("example.com", id = 0xABCD))
        assertEquals(0xABCD, PacketCodec.readU16(rewritten, 0))
        assertTrue(DnsMessage.isResponseTo(rewritten, TestDns.query("example.com", id = 0xABCD)))
    }
}
