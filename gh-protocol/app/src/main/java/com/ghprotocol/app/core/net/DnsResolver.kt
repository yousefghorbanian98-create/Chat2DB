package com.ghprotocol.app.core.net

import java.util.concurrent.ConcurrentHashMap

data class DnsAttempt(
    val path: String,
    val ok: Boolean,
    val ms: Long,
    val detail: String,
    val rcode: Int = -1,
    val answers: Int = -1
)

/**
 * Resolver outcome. [response] is **always** a syntactically valid DNS reply for the query:
 * either a validated upstream answer or a real SERVFAIL built from the query itself.
 * [path] says which upstream produced it (`cache`, `doh:…`, `tcp:…`, `servfail`).
 */
data class DnsResolution(
    val response: ByteArray,
    val path: String,
    val ms: Long,
    val fromCache: Boolean,
    val attempts: List<DnsAttempt>
) {
    val ok: Boolean get() = path != PATH_SERVFAIL
    val isServfail: Boolean get() = path == PATH_SERVFAIL

    companion object {
        const val PATH_SERVFAIL = "servfail"
    }
}

interface DnsEvents {
    fun onResolved(query: ByteArray, resolution: DnsResolution) {}
    fun onFailed(query: ByteArray, attempts: List<DnsAttempt>) {}
}

/** TTL-respecting cache of validated upstream answers (keyed by question section only). */
class DnsCache(
    private val maxEntries: Int = 256,
    private val maxTtlSeconds: Long = 300,
    private val minTtlSeconds: Long = 10,
    private val clock: () -> Long = { System.currentTimeMillis() }
) {
    private class Entry(val response: ByteArray, val expiresAtMs: Long)

    private val entries = ConcurrentHashMap<String, Entry>()

    fun get(key: String): ByteArray? {
        val entry = entries[key] ?: return null
        if (entry.expiresAtMs <= clock()) {
            entries.remove(key)
            return null
        }
        return entry.response
    }

    fun put(key: String, response: ByteArray, ttlSeconds: Long) {
        if (entries.size > maxEntries) entries.clear()
        val ttl = ttlSeconds.coerceIn(minTtlSeconds, maxTtlSeconds)
        entries[key] = Entry(response.copyOf(), clock() + ttl * 1000)
    }

    fun clear() = entries.clear()

    fun size(): Int = entries.size
}

/**
 * Bounded multi-path DNS resolver for the tunnel.
 *
 * Contract (each point is unit/integration-tested):
 *  - a response is accepted **only** when it parses, is a response, matches the transaction
 *    ID *and* the question section of the query;
 *  - the whole resolution has a hard budget ([budgetMs]); every path gets the remaining
 *    time capped by [perPathMaxMs], so a blocked upstream can never hang an app;
 *  - answers are cached with their real TTL (clamped), never longer;
 *  - on total failure the caller still receives a valid SERVFAIL for the same query, so the
 *    app fails fast instead of waiting for its own timeout;
 *  - no AAAA (or any other) answer is ever synthesised.
 */
class DnsResolver(
    private val transports: List<DnsTransport>,
    private val budgetMs: Long = 6000,
    private val perPathMaxMs: Long = 2500,
    private val cache: DnsCache = DnsCache(),
    private val clock: () -> Long = { System.currentTimeMillis() },
    private val events: DnsEvents = object : DnsEvents {}
) {

    fun resolve(query: ByteArray): DnsResolution {
        val started = clock()
        val view = DnsMessage.parse(query)
        if (view == null || view.isResponse || view.opcode != 0 || view.questions.isEmpty()) {
            return DnsResolution(
                response = DnsMessage.buildFailure(query, DnsMessage.RCODE_FORMERR),
                path = DnsResolution.PATH_SERVFAIL,
                ms = 0,
                fromCache = false,
                attempts = listOf(DnsAttempt("validate_query", false, 0, "malformed_query"))
            )
        }
        val key = DnsMessage.cacheKey(query)
        val attempts = ArrayList<DnsAttempt>(transports.size)

        if (key != null) {
            val cached = cache.get(key)
            if (cached != null && DnsMessage.isResponseTo(cached, query)) {
                val answer = fitToClient(query, view.udpPayloadSize, DnsMessage.withTransactionId(cached, query))
                return DnsResolution(answer, "cache", clock() - started, true, attempts)
            }
        }

        for (transport in transports) {
            val elapsed = clock() - started
            val remaining = budgetMs - elapsed
            if (remaining < 250) {
                attempts.add(DnsAttempt(transport.name, false, 0, "budget_exhausted"))
                break
            }
            val timeout = minOf(perPathMaxMs, remaining).toInt()
            val result = try {
                transport.exchange(query, timeout)
            } catch (e: Exception) {
                DnsTransportResult(null, e.javaClass.simpleName + ":" + (e.message ?: ""), 0)
            }
            val response = result.response
            if (response == null) {
                attempts.add(DnsAttempt(transport.name, false, result.ms, result.detail))
                continue
            }
            val mismatch = DnsMessage.mismatchReason(response, query)
            if (mismatch != null) {
                attempts.add(DnsAttempt(transport.name, false, result.ms, mismatch))
                continue
            }
            val answerView = DnsMessage.parse(response)
            if (answerView == null) {
                attempts.add(DnsAttempt(transport.name, false, result.ms, "unparseable_response"))
                continue
            }
            attempts.add(
                DnsAttempt(
                    transport.name, true, result.ms, result.detail,
                    rcode = answerView.rcode, answers = answerView.answerCount
                )
            )
            if (key != null && answerView.rcode == DnsMessage.RCODE_NOERROR && answerView.answerCount > 0) {
                cache.put(key, response, DnsMessage.minAnswerTtlSeconds(response))
            }
            val answer = fitToClient(query, view.udpPayloadSize, DnsMessage.withTransactionId(response, query))
            val resolution = DnsResolution(answer, transport.name, clock() - started, false, attempts)
            events.onResolved(query, resolution)
            return resolution
        }

        events.onFailed(query, attempts)
        return DnsResolution(
            response = DnsMessage.buildFailure(query, DnsMessage.RCODE_SERVFAIL),
            path = DnsResolution.PATH_SERVFAIL,
            ms = clock() - started,
            fromCache = false,
            attempts = attempts
        )
    }

    /** Keep the reply inside the client's advertised UDP size (TC=1 otherwise, no fake data). */
    private fun fitToClient(query: ByteArray, udpPayloadSize: Int, response: ByteArray): ByteArray {
        val limit = udpPayloadSize.coerceIn(512, 4096)
        if (response.size <= limit) return response
        return DnsMessage.truncateTo(query, response, limit)
    }

    /** Human-readable summary of a resolution, safe for logs (no answer contents). */
    fun describe(resolution: DnsResolution): String {
        val view = DnsMessage.parse(resolution.response)
        val rcode = if (view != null) DnsMessage.rcodeName(view.rcode) else "unparseable"
        val answers = view?.answerCount ?: -1
        val attempts = resolution.attempts.joinToString(",") {
            "${it.path}=" + (if (it.ok) "ok" else it.detail).take(80)
        }
        val cache = if (resolution.fromCache) " cache=hit" else ""
        return "dns path=${resolution.path} rcode=$rcode answers=$answers ms=${resolution.ms}$cache" +
            if (attempts.isNotEmpty()) " attempts=[$attempts]" else ""
    }
}

/**
 * The production upstream list for the tunnel, built from validated constants.
 *
 * `cloudflare-dns.com` is hosted on 104.16.248.249 / 104.16.249.249; `1.1.1.1` / `1.0.0.1`
 * answer DoH only under the `one.one.one.one` names and are IP-blocked on several Iranian
 * ISPs, which is why they are not used as bootstrap addresses here.
 */
object DnsUpstreams {

    val CLOUDFLARE_DOH_IPS = listOf("104.16.248.249", "104.16.249.249")
    val GOOGLE_DOH_IPS = listOf("8.8.8.8", "8.8.4.4")

    fun cloudflareDoh(connector: SocksConnector): DohTransport = DohTransport(
        connector = connector,
        endpoint = DohEndpoint(
            displayName = "cloudflare-doh",
            host = "cloudflare-dns.com",
            path = "/dns-query",
            bootstrapIps = CLOUDFLARE_DOH_IPS
        )
    )

    fun googleDoh(connector: SocksConnector): DohTransport = DohTransport(
        connector = connector,
        endpoint = DohEndpoint(
            displayName = "google-doh",
            host = "dns.google",
            path = "/dns-query",
            bootstrapIps = GOOGLE_DOH_IPS
        )
    )

    fun tcpDns(connector: SocksConnector, host: String, port: Int = 53): DnsTransport =
        TcpDnsTransport(connector, host, port)

    /** Xray's own resolver (dokodemo-door `dns-in`) — last resort, validated like any other. */
    fun xrayDnsIn(host: String = "127.0.0.1", port: Int = 15353): DnsTransport =
        UdpDnsTransport(host, port)

    fun defaultChain(connector: SocksConnector, dnsInPort: Int = 15353): List<DnsTransport> = listOf(
        cloudflareDoh(connector),
        googleDoh(connector),
        tcpDns(connector, "8.8.8.8"),
        tcpDns(connector, "1.1.1.1"),
        xrayDnsIn(port = dnsInPort)
    )
}
