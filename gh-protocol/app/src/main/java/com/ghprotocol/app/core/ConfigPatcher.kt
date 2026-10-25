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
        val dns = json.optJSONObject("dns") ?: JSONObject().also { json.put("dns", it) }
        val hosts = dns.optJSONObject("hosts") ?: JSONObject().also { dns.put("hosts", it) }
        hosts.put("cloudflare-dns.com", cleanIp)
        hosts.put("challenges.cloudflare.com", cleanIp)
        hosts.put("one.one.one.one", cleanIp)
        patched++
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
            val hosts = dns.optJSONObject("hosts") ?: JSONObject().also { dns.put("hosts", it) }
            val cfHost = hosts.optString("cloudflare-dns.com", "")
            // Map cloudflare-dns.com / challenges.cloudflare.com to the real unblocked
            // challenges.cloudflare.com Anycast IPv4 (104.18.94.41) rather than 1.1.1.1
            // (since 1.1.1.1:443 is IP-blocked for HTTPS/DoH on Iranian ISPs).
            val cfIp = if (cfHost.isNotBlank() && cfHost.first().isDigit()) cfHost else "104.18.94.41"
            hosts.put("cloudflare-dns.com", cfIp)
            val chHost = hosts.optString("challenges.cloudflare.com", "")
            if (chHost.isBlank() || !chHost.first().isDigit()) {
                hosts.put("challenges.cloudflare.com", cfIp)
            }
            if (!hosts.has("dns.google")) hosts.put("dns.google", "8.8.8.8")
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
