package com.ghprotocol.app.core

import org.json.JSONArray
import org.json.JSONObject
import java.net.URI
import java.net.URLDecoder

/**
 * Pure JSON transforms over the Xray config (JVM unit-tested).
 *
 * F-17: replace the egress address only — SNI/Host/Path untouched.
 * F-15: TCP-first profile when UDP is dropped.
 * F-16: validate & normalize imported custom configs (JSON array, single JSON
 *       object, or Simorgh-pattern `vless://` and `trojan://` URIs with automatic
 *       TLS fragmentation injection and optional clean-IP address override).
 */
object ConfigPatcher {

    /**
     * Loopback port the VpnService relays client DNS to. MUST be > 1024:
     * Android denies binding privileged ports to apps
     * ("listen tcp 127.0.0.1:53: bind: permission denied", verified on API 34).
     * Also avoids 5353 (the system mDNS daemon already owns it).
     */
    const val DNS_IN_PORT = 15353

    data class InboundInfo(val tag: String, val port: Int, val protocol: String)

    fun findInbound(json: JSONObject): InboundInfo? {
        val inbounds = json.optJSONArray("inbounds") ?: return null
        for (i in 0 until inbounds.length()) {
            val ib = inbounds.getJSONObject(i)
            val port = ib.optInt("port", -1)
            if (port > 0) return InboundInfo(ib.optString("tag", ""), port, ib.optString("protocol", ""))
        }
        return null
    }

    /**
     * F-17: point the given outbound tags at [cleanIp] (egress replacement).
     * Only `settings.address` (or vnext/servers address) is touched;
     * SNI/Host/Path/finalmask stay untouched.
     * Returns the number of outbounds patched.
     */
    fun patchCleanEgress(
        json: JSONObject,
        cleanIp: String,
        tags: List<String> = listOf("tcp-fragment", "tcp-fragment-tls", "proxy")
    ): Int {
        val outbounds = json.optJSONArray("outbounds") ?: return 0
        var patched = 0
        for (i in 0 until outbounds.length()) {
            val ob = outbounds.getJSONObject(i)
            if (!tags.contains(ob.optString("tag", ""))) continue
            val settings = ob.optJSONObject("settings") ?: JSONObject().also { ob.put("settings", it) }
            val vnext = settings.optJSONArray("vnext")
            val servers = settings.optJSONArray("servers")
            when {
                vnext != null && vnext.length() > 0 -> {
                    vnext.getJSONObject(0).put("address", cleanIp)
                    patched++
                }
                servers != null && servers.length() > 0 -> {
                    servers.getJSONObject(0).put("address", cleanIp)
                    patched++
                }
                else -> {
                    settings.put("address", cleanIp)
                    patched++
                }
            }
        }
        return patched
    }

    /**
     * Smart Clean-IP application (v1.2):
     * - For proxy outbounds (`vless`, `trojan`, `vmess`, `shadowsocks` with `vnext`/`servers`),
     *   replaces the server `address` with [cleanIp].
     * - For `direct`/`freedom` outbounds (`Serverless-for-Iran.json`'s `tcp-fragment` and
     *   `tcp-fragment-tls`), NEVER sets `settings.address` (which would hijack all non-Cloudflare
     *   internet traffic to Cloudflare and cause `Down=0 B`); instead injects [cleanIp] into
     *   `dns.hosts` for `cloudflare-dns.com` and `challenges.cloudflare.com` so DoH uses the
     *   fastest verified Clean IP while `tcp-fragment-tls` connects to each site's real IP.
     */
    fun applySmartCleanIp(json: JSONObject, cleanIp: String): Int {
        var patched = 0
        val outbounds = json.optJSONArray("outbounds")
        if (outbounds != null) {
            for (i in 0 until outbounds.length()) {
                val ob = outbounds.getJSONObject(i)
                val proto = ob.optString("protocol", "").lowercase()
                val settings = ob.optJSONObject("settings")
                val vnext = settings?.optJSONArray("vnext")
                val servers = settings?.optJSONArray("servers")
                when {
                    vnext != null && vnext.length() > 0 -> {
                        vnext.getJSONObject(0).put("address", cleanIp)
                        patched++
                    }
                    servers != null && servers.length() > 0 -> {
                        servers.getJSONObject(0).put("address", cleanIp)
                        patched++
                    }
                    proto == "direct" || proto == "freedom" -> {
                        // Ensure direct/fragment outbounds never hijack non-Cloudflare destination IPs
                        settings?.remove("address")
                    }
                }
            }
        }
        // The clean IP is an *egress* address for Cloudflare-fronted destinations. Pointing the
        // DoH hostname (cloudflare-dns.com) at it would send the DoH TLS handshake to an edge
        // whose certificate/zone does not match the SNI — the exact failure fixed in v1.6.
        // DoH bootstrap is handled by [enforceReachableDns] with the zone's real IPs instead.
        return patched
    }

    /**
     * F-15: TCP-first profile — move TCP fragment rules ahead of UDP noise rules
     * in the routing table when `udp-noises` is present, without moving catch-all
     * `0.0.0.0/0` rules ahead of `dns-out`, `10.10.34.0/24`, or `domain:ir`.
     */
    fun tcpFirstProfile(json: JSONObject): Boolean {
        val routing = json.optJSONObject("routing") ?: return false
        val rules = routing.optJSONArray("rules") ?: return false
        val list = (0 until rules.length()).map { rules.getJSONObject(it) }
        val tagged = list.map { r ->
            val outArr = r.optJSONArray("outboundTag")
            val tags: List<String> = when {
                outArr != null -> (0 until outArr.length()).map { outArr.getString(it) }
                r.has("outboundTag") -> listOf(r.getString("outboundTag"))
                else -> emptyList()
            }
            r to tags
        }
        val hasUdpNoises = tagged.any { (_, tags) -> tags.any { it.startsWith("udp-noise") } }
        if (!hasUdpNoises) {
            return true
        }
        val scored = tagged.map { (r, tags) ->
            val score = when {
                tags.any { it.startsWith("tcp-fragment") || it == "proxy" } -> 0
                tags.any { it.startsWith("udp-") } -> 1
                else -> 2
            }
            score to r
        }
        val ordered = scored.sortedBy { it.first }.map { it.second }
        val newRules = JSONArray()
        ordered.forEach { newRules.put(it) }
        routing.put("rules", newRules)
        return true
    }

    /**
     * Inject a loopback DNS inbound (127.0.0.1:15353, tag `dns-in`) so the VpnService
     * can relay client DNS queries into Xray's own resolver (config dns.servers).
     * Idempotent: returns false if such an inbound already exists.
     */
    fun addLocalDnsInbound(json: JSONObject): Boolean {
        val inbounds = json.optJSONArray("inbounds") ?: return false
        for (i in 0 until inbounds.length()) {
            val ib = inbounds.getJSONObject(i)
            val proto = ib.optString("protocol")
            if (ib.optString("tag") == "dns-in") return false
            if (ib.optInt("port", -1) == DNS_IN_PORT && proto == "dokodemo-door") return false
        }
        inbounds.put(
            JSONObject()
                .put("tag", "dns-in")
                .put("protocol", "dokodemo-door")
                .put("listen", "127.0.0.1")
                .put("port", DNS_IN_PORT)
                .put("settings", JSONObject()
                    .put("address", "127.0.0.1")
                    .put("port", 53)
                    .put("network", "tcp,udp")
                    .put("userLevel", 12))
        )

        var dnsTag: String? = null
        val outbounds = json.optJSONArray("outbounds")
        if (outbounds != null) {
            for (i in 0 until outbounds.length()) {
                val ob = outbounds.getJSONObject(i)
                if (ob.optString("protocol") == "dns") dnsTag = ob.optString("tag", "dns-out")
            }
        }
        if (dnsTag == null) {
            dnsTag = "dns-out"
            val ob = json.optJSONArray("outbounds") ?: JSONArray().also { json.put("outbounds", it) }
            ob.put(JSONObject().put("tag", dnsTag).put("protocol", "dns"))
        }

        val routing = json.optJSONObject("routing") ?: JSONObject().also { json.put("routing", it) }
        val rules = routing.optJSONArray("rules") ?: JSONArray().also { routing.put("rules", it) }
        val newRules = JSONArray()
        newRules.put(
            JSONObject().put("type", "field")
                .put("inboundTag", JSONArray().put("dns-in"))
                .put("outboundTag", dnsTag)
        )
        for (i in 0 until rules.length()) newRules.put(rules.getJSONObject(i))
        routing.put("rules", newRules)
        return true
    }

    /**
     * Strip dangling `fakedns` and recursive `localhost` DNS references when no
     * `fakedns` inbound is present.
     */
    fun ensureConsistentDns(json: JSONObject): Int {
        var removed = 0
        val ibs = json.optJSONArray("inbounds") ?: return 0
        var hasFakeDnsEngine = false
        for (i in 0 until ibs.length()) {
            if (ibs.getJSONObject(i).optString("protocol") == "fakedns") hasFakeDnsEngine = true
        }
        if (hasFakeDnsEngine) return 0

        val dns = json.optJSONObject("dns")
        val servers = dns?.optJSONArray("servers")
        if (servers != null) {
            val kept = JSONArray()
            for (i in 0 until servers.length()) {
                val s = servers.opt(i)
                val addr = if (s is JSONObject) s.optString("address", "") else s?.toString().orEmpty()
                if (addr.equals("fakedns", ignoreCase = true)) { removed++; continue }
                if (addr.equals("localhost", ignoreCase = true)) { removed++; continue }
                if (s is JSONObject && s.optInt("timeoutMs", 0) > 4000) {
                    s.put("timeoutMs", 4000)
                }
                kept.put(s)
            }
            if (kept.length() == 0) {
                kept.put("https://cloudflare-dns.com/dns-query")
                kept.put("1.1.1.1")
                kept.put("8.8.8.8")
            }
            dns.put("servers", kept)
            dns.put("queryStrategy", "UseIPv4")
            // Bootstrap hosts are canonicalised by [enforceReachableDns]; nothing here may map
            // a DoH hostname onto an unrelated edge (see DIAGNOSIS 2026-10-25, D1).
        }
        if (json.has("fakedns")) {
            json.remove("fakedns")
        }
        for (i in 0 until ibs.length()) {
            val sniff = ibs.getJSONObject(i).optJSONObject("sniffing") ?: continue
            sniff.put("routeOnly", true)
            val ov = sniff.optJSONArray("destOverride") ?: continue
            val kept = JSONArray()
            for (j in 0 until ov.length()) {
                val v = ov.optString(j, "")
                if (v.equals("fakedns", ignoreCase = true)) { removed++; continue }
                kept.put(v)
            }
            sniff.put("destOverride", kept)
        }
        // Prevent Xray router from invoking app/dns (IPOnDemand/IPIfNonMatch) on TCP flows
        // that already have a numeric destination IP from VpnTunnelService.
        val routing = json.optJSONObject("routing")
        if (routing != null) {
            val ds = routing.optString("domainStrategy", "")
            if (ds.isNotEmpty() && !ds.equals("AsIs", ignoreCase = true)) {
                routing.put("domainStrategy", "AsIs")
            }
            val rules = routing.optJSONArray("rules")
            if (rules != null) {
                for (i in 0 until rules.length()) {
                    val r = rules.getJSONObject(i)
                    if (r.optString("outboundTag") == "dns-out" && r.has("port") && !r.has("inboundTag")) {
                        r.put("inboundTag", JSONArray().put("dns-in"))
                    }
                }
            }
        }
        val obs = json.optJSONArray("outbounds")
        if (obs != null) {
            for (i in 0 until obs.length()) {
                val ob = obs.getJSONObject(i)
                val proto = ob.optString("protocol", "").lowercase()
                val sockopt = ob.optJSONObject("streamSettings")?.optJSONObject("sockopt")
                sockopt?.optJSONObject("happyEyeballs")?.put("prioritizeIPv6", false)
                // Critical fix for Serverless-for-Iran.json:
                // In Xray-core transport/internet/dialer.go, DialSystem checks:
                //   if sockopt.DomainStrategy.HasStrategy() && dest.Address.Family().IsDomain()
                // With sniffing.routeOnly=true on mixed-in, all app TCP connections keep their
                // numeric IPv4 target (IsDomain()==false), so "UseIPv4" NEVER calls app/dns on
                // app traffic, while still resolving "cloudflare-dns.com" via dns.hosts ->
                // 104.18.94.41 when no-filter-dns dials tcp:cloudflare-dns.com:443!
                if ((proto == "direct" || proto == "freedom") && sockopt != null && sockopt.has("domainStrategy")) {
                    sockopt.put("domainStrategy", "UseIPv4")
                }
            }
        }
        return removed
    }

    /**
     * v1.6: make the *effective* DNS plan reachable and auditable.
     *
     * Fixes the fragB failure mode from DIAGNOSIS 2026-10-25 §D1:
     *  - `dns.hosts["cloudflare-dns.com"]` must be the **zone's own** anycast IPs
     *    (`104.16.248.249` / `104.16.249.249`, the A records of the name), never
     *    `1.1.1.1`/`1.0.0.1` (their :443 is IP-blocked on several Iranian ISPs and they
     *    answer DoH only under `one.one.one.one`) and never an arbitrary clean IP
     *    (certificate/zone mismatch → the `context deadline exceeded` loop);
     *  - `dns.queryStrategy` is pinned to `UseIPv4` so Xray never emits AAAA lookups that
     *    time out on an IPv4-only tunnel;
     *  - every HTTPS (RFC 8484 DoH) DNS server is reported with its resolved bootstrap IP and
     *    the outbound that will carry it, so the plan can be logged and asserted in tests.
     *
     * Idempotent. Returns the number of mutated fields.
     */
    fun enforceReachableDns(json: JSONObject): Int {
        var mutated = 0
        val dns = json.optJSONObject("dns") ?: return 0
        val hosts = dns.optJSONObject("hosts") ?: JSONObject().also {
            dns.put("hosts", it)
            mutated++
        }
        val existing = hosts.optString(DOH_HOST, "")
        if (existing != DOH_BOOTSTRAP_IPV4) {
            hosts.put(DOH_HOST, DOH_BOOTSTRAP_IPV4)
            mutated++
        }
        // A hostname mapped onto a hostname is a resolution loop; remove it.
        val challenge = hosts.opt("challenges.cloudflare.com")
        if (challenge is String && !challenge.first().isDigit()) {
            hosts.remove("challenges.cloudflare.com")
            mutated++
        }
        if (dns.optString("queryStrategy", "") != "UseIPv4") {
            dns.put("queryStrategy", "UseIPv4")
            mutated++
        }
        return mutated
    }

    /** Machine-checkable view of the DNS configuration that will actually run. */
    data class DnsPlan(
        val servers: List<String>,
        val hosts: Map<String, String>,
        val queryStrategy: String,
        val dohEndpoints: List<String>,
        val dohBootstrapIps: List<String>,
        val dohOutbound: String?,
        val notes: List<String>
    ) {
        fun describe(): String = buildString {
            append("servers=").append(servers.joinToString(","))
            append(" hosts=").append(hosts.entries.joinToString(",") { "${it.key}->${it.value}" })
            append(" strategy=").append(queryStrategy)
            append(" doh=").append(dohEndpoints.joinToString(",").ifEmpty { "none" })
            append(" dohIps=").append(dohBootstrapIps.joinToString(",").ifEmpty { "none" })
            append(" dohOutbound=").append(dohOutbound ?: "default")
            if (notes.isNotEmpty()) append(" notes=").append(notes.joinToString("; "))
        }
    }

    const val DOH_HOST = "cloudflare-dns.com"

    /** Real A records of cloudflare-dns.com (verified 2026-10-25: 104.16.248.249/249). */
    const val DOH_BOOTSTRAP_IPV4 = "104.16.248.249"
    val DOH_ZONE_IPV4 = listOf(DOH_BOOTSTRAP_IPV4, "104.16.249.249")

    /**
     * Compute the effective DNS plan (after patching) so both fragA and fragB can be
     * printed, logged and asserted. Pure.
     */
    fun effectiveDnsPlan(json: JSONObject): DnsPlan {
        val dns = json.optJSONObject("dns")
        val notes = mutableListOf<String>()
        val servers = mutableListOf<String>()
        val serverTags = mutableMapOf<String, String>()
        dns?.optJSONArray("servers")?.let { arr ->
            for (i in 0 until arr.length()) {
                val item = arr.opt(i)
                when (item) {
                    is JSONObject -> {
                        val address = item.optString("address", "")
                        if (address.isNotEmpty()) {
                            servers.add(address)
                            val tag = item.optString("tag", "")
                            if (tag.isNotEmpty()) serverTags[address] = tag
                        }
                    }
                    is String -> servers.add(item)
                }
            }
        }
        val hosts = mutableMapOf<String, String>()
        dns?.optJSONObject("hosts")?.let { h ->
            val keys = h.keys()
            while (keys.hasNext()) {
                val key = keys.next()
                hosts[key] = h.optString(key, "")
            }
        }
        val strategies = mutableListOf<String>()
        servers.forEach { address ->
            if (address.startsWith("https://")) {
                val host = address.removePrefix("https://").substringBefore('/')
                val mapped = hosts[host] ?: ""
                if (mapped.isEmpty()) {
                    notes.add("doh_host_without_bootstrap:$host")
                } else if (!mapped.first().isDigit()) {
                    notes.add("doh_bootstrap_is_domain:$host->$mapped")
                } else if (mapped == "1.1.1.1" || mapped == "1.0.0.1") {
                    notes.add("doh_bootstrap_ip_blocked_in_ir:$mapped")
                } else if (DOH_ZONE_IPV4.contains(mapped)) {
                    notes.add("doh_bootstrap_zone_ok:$host->$mapped")
                } else {
                    notes.add("doh_bootstrap_foreign_edge:$host->$mapped")
                }
            } else if (address == "fakedns" || address == "localhost") {
                notes.add("dns_server_unresolvable:$address")
            } else {
                strategies.add(address)
            }
        }
        val dohEndpoints = servers.filter { it.startsWith("https://") }
        val dohBootstrapIps = dohEndpoints.mapNotNull { endpoint ->
            val host = endpoint.removePrefix("https://").substringBefore('/')
            hosts[host]?.takeIf { it.isNotEmpty() && it.first().isDigit() }
        }.distinct()
        val dohOutbound = dohEndpoints.firstOrNull()?.let { endpoint ->
            val host = endpoint.removePrefix("https://").substringBefore('/')
            val tag = serverTags[endpoint] ?: host
            findOutboundForInbound(json, tag)
        }
        return DnsPlan(
            servers = servers,
            hosts = hosts,
            queryStrategy = dns?.optString("queryStrategy", "UseSystem") ?: "UseSystem",
            dohEndpoints = dohEndpoints,
            dohBootstrapIps = dohBootstrapIps,
            dohOutbound = dohOutbound,
            notes = notes
        )
    }

    /** The outbound that carries traffic tagged with [inboundTag] (first matching rule). */
    fun findOutboundForInbound(json: JSONObject, inboundTag: String): String? {
        val rules = json.optJSONObject("routing")?.optJSONArray("rules") ?: return null
        for (i in 0 until rules.length()) {
            val rule = rules.optJSONObject(i) ?: continue
            val inbound = rule.optJSONArray("inboundTag") ?: continue
            for (j in 0 until inbound.length()) {
                if (inbound.optString(j, "") == inboundTag) {
                    val tag = rule.optString("outboundTag", "")
                    return if (tag.isEmpty()) null else tag
                }
            }
        }
        return null
    }

    /**
     * F-16 (Simorgh pattern): Convert a `vless://` or `trojan://` URI into a complete
     * Xray JSON config with mixed-in :10808, TLS ClientHello fragmentation, and
     * optional [cleanIp] address override (preserving SNI/Host/Path).
     */
    fun parseUriToConfig(rawUri: String, cleanIp: String? = null): Result<JSONObject> = try {
        val trimmed = rawUri.trim()
        val u = URI(trimmed)
        val scheme = u.scheme?.lowercase().orEmpty()
        require(scheme == "vless" || scheme == "trojan") { "unsupported URI scheme: $scheme" }
        val cred = u.rawUserInfo?.let { URLDecoder.decode(it, "UTF-8") }.orEmpty()
        require(cred.isNotBlank()) { "missing credential in $scheme URI" }
        val origHost = u.host ?: throw IllegalArgumentException("missing host in $scheme URI")
        val port = if (u.port > 0) u.port else 443
        val params = parseQueryParams(u.rawQuery.orEmpty())
        val remark = u.rawFragment?.let { URLDecoder.decode(it, "UTF-8") }?.takeIf { it.isNotBlank() }
            ?: "$scheme-$origHost"

        val connectHost = if (!cleanIp.isNullOrBlank()) cleanIp.trim() else origHost
        val sni = params["sni"]?.takeIf { it.isNotBlank() } ?: origHost
        val wsHost = params["host"]?.takeIf { it.isNotBlank() } ?: origHost
        val netType = params["type"]?.lowercase() ?: "tcp"
        val security = params["security"]?.lowercase() ?: "tls"
        val fp = params["fp"]?.takeIf { it.isNotBlank() } ?: "chrome"

        val settings = if (scheme == "vless") {
            val user = JSONObject()
                .put("id", cred)
                .put("encryption", params["encryption"] ?: "none")
            params["flow"]?.takeIf { it.isNotBlank() }?.let { user.put("flow", it) }
            JSONObject().put(
                "vnext",
                JSONArray().put(
                    JSONObject()
                        .put("address", connectHost)
                        .put("port", port)
                        .put("users", JSONArray().put(user))
                )
            )
        } else {
            JSONObject().put(
                "servers",
                JSONArray().put(
                    JSONObject()
                        .put("address", connectHost)
                        .put("port", port)
                        .put("password", cred)
                )
            )
        }

        val streamSettings = JSONObject()
            .put("network", netType)
            .put("security", security)
            .put("sockopt", JSONObject().put("dialerProxy", "tcp-fragment").put("tcpNoDelay", true))

        if (security == "tls") {
            streamSettings.put(
                "tlsSettings",
                JSONObject()
                    .put("serverName", sni)
                    .put("fingerprint", fp)
            )
        } else if (security == "reality") {
            streamSettings.put(
                "realitySettings",
                JSONObject()
                    .put("serverName", sni)
                    .put("fingerprint", fp)
                    .put("publicKey", params["pbk"].orEmpty())
                    .put("shortId", params["sid"].orEmpty())
                    .put("spiderX", params["spx"] ?: "/")
            )
        }

        if (netType == "ws") {
            streamSettings.put(
                "wsSettings",
                JSONObject()
                    .put("path", params["path"] ?: "/")
                    .put("headers", JSONObject().put("Host", wsHost))
            )
        } else if (netType == "grpc") {
            streamSettings.put(
                "grpcSettings",
                JSONObject().put("serviceName", params["serviceName"].orEmpty())
            )
        }

        val proxyOutbound = JSONObject()
            .put("tag", "proxy")
            .put("protocol", scheme)
            .put("settings", settings)
            .put("streamSettings", streamSettings)

        val fragmentOutbound = JSONObject()
            .put("tag", "tcp-fragment")
            .put("protocol", "freedom")
            .put(
                "settings",
                JSONObject().put(
                    "fragment",
                    JSONObject()
                        .put("packets", "tlshello")
                        .put("length", "10-20")
                        .put("interval", "10-20")
                )
            )

        val cfg = JSONObject()
            .put("remarks", remark)
            .put("version", JSONObject().put("min", "26.6.27"))
            .put("dns", JSONObject().put("servers", JSONArray().put("https://cloudflare-dns.com/dns-query").put("8.8.8.8")))
            .put(
                "inbounds",
                JSONArray().put(
                    JSONObject()
                        .put("tag", "mixed-in")
                        .put("listen", "127.0.0.1")
                        .put("port", 10808)
                        .put("protocol", "mixed")
                        .put("settings", JSONObject().put("udp", true))
                        .put("sniffing", JSONObject().put("enabled", true).put("destOverride", JSONArray().put("tls").put("http")))
                )
            )
            .put(
                "outbounds",
                JSONArray()
                    .put(proxyOutbound)
                    .put(fragmentOutbound)
                    .put(JSONObject().put("tag", "dns-out").put("protocol", "dns"))
                    .put(JSONObject().put("tag", "block").put("protocol", "blackhole"))
            )
            .put(
                "routing",
                JSONObject().put(
                    "rules",
                    JSONArray().put(
                        JSONObject()
                            .put("type", "field")
                            .put("inboundTag", JSONArray().put("mixed-in"))
                            .put("outboundTag", "proxy")
                    )
                )
            )
        addLocalDnsInbound(cfg)
        Result.success(cfg)
    } catch (e: Exception) {
        Result.failure(e)
    }

    private fun parseQueryParams(rawQuery: String): Map<String, String> {
        if (rawQuery.isBlank()) return emptyMap()
        val map = mutableMapOf<String, String>()
        for (part in rawQuery.split('&')) {
            val idx = part.indexOf('=')
            if (idx > 0) {
                val k = URLDecoder.decode(part.substring(0, idx), "UTF-8")
                val v = URLDecoder.decode(part.substring(idx + 1), "UTF-8")
                map[k] = v
            }
        }
        return map
    }

    /**
     * The **runtime** transform pipeline for one subscription entry — used by the app *and*
     * by the tests that dump the effective fragA/fragB DNS configuration:
     * tcp-first ordering → loopback DNS inbound → DNS consistency → reachable DoH bootstrap
     * → optional clean egress. Pure and idempotent.
     */
    fun runtimeConfigForEntry(
        rawJson: String,
        index: Int,
        cleanIp: String? = null,
        tcpFirst: Boolean = true
    ): Result<JSONObject> = try {
        val array = JSONArray(rawJson)
        require(array.length() > 0) { "empty config list" }
        val cfg = array.getJSONObject(index.coerceIn(0, array.length() - 1))
        if (tcpFirst) tcpFirstProfile(cfg)
        addLocalDnsInbound(cfg)
        ensureConsistentDns(cfg)
        enforceReachableDns(cfg)
        if (!cleanIp.isNullOrBlank()) applySmartCleanIp(cfg, cleanIp)
        enforceReachableDns(cfg)
        Result.success(cfg)
    } catch (e: Exception) {
        Result.failure(e)
    }

    /** Human-readable per-profile DNS audit for logs and bug reports. */
    fun runtimeDnsAudit(rawJson: String, index: Int, cleanIp: String? = null): String {
        val cfg = runtimeConfigForEntry(rawJson, index, cleanIp).getOrNull() ?: return "config_parse_failed"
        val remarks = cfg.optString("remarks", "entry-$index")
        return "$remarks :: " + effectiveDnsPlan(cfg).describe()
    }

    /**
     * Normalize any supported user import (JSON array, single JSON object, or
     * newline-separated `vless://` / `trojan://` URIs) into a canonical JSONArray string.
     */
    fun normalizeImport(raw: String, cleanIp: String? = null): Result<String> = try {
        val text = raw.trim()
        require(text.isNotEmpty()) { "empty import" }
        val arr = when {
            text.startsWith("[") -> JSONArray(text)
            text.startsWith("{") -> JSONArray().put(JSONObject(text))
            else -> {
                val lines = text.lineSequence()
                    .map { it.trim() }
                    .filter { it.startsWith("vless://", ignoreCase = true) || it.startsWith("trojan://", ignoreCase = true) }
                    .toList()
                require(lines.isNotEmpty()) { "not a JSON config or vless/trojan URI" }
                val built = JSONArray()
                for (line in lines) {
                    built.put(parseUriToConfig(line, cleanIp).getOrThrow())
                }
                built
            }
        }
        require(arr.length() > 0) { "empty config list" }
        Result.success(arr.toString())
    } catch (e: Exception) {
        Result.failure(e)
    }

    data class ImportInfo(val inbound: InboundInfo, val minCoreVersion: String, val entries: Int)

    /** F-16: validate a pasted/imported Xray config (JSON array/object or vless/trojan URIs). */
    fun validateImport(raw: String): Result<ImportInfo> = try {
        val normalized = normalizeImport(raw).getOrThrow()
        val parsed = JSONArray(normalized)
        require(parsed.length() > 0) { "empty config list" }
        val first = parsed.getJSONObject(0)
        val inbound = findInbound(first) ?: return Result.failure(IllegalArgumentException("no inbound with a port"))
        val min = first.optJSONObject("version")?.optString("min", "") ?: ""
        Result.success(ImportInfo(inbound, min, parsed.length()))
    } catch (e: Exception) {
        Result.failure(e)
    }
}
