package com.ghprotocol.app.core

import org.json.JSONArray
import org.json.JSONObject

/**
 * Pure JSON transforms over the Xray config (JVM unit-tested).
 *
 * F-17: replace the egress address only — SNI/Host/Path untouched.
 * F-15: TCP-first profile when UDP is dropped.
 * F-16: validate an imported custom config.
 */
object ConfigPatcher {

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
     * Only `settings.address` is touched; SNI/Host/Path/finalmask stay untouched.
     * Returns the number of outbounds patched.
     */
    fun patchCleanEgress(json: JSONObject, cleanIp: String, tags: List<String> = listOf("tcp-fragment", "tcp-fragment-tls")): Int {
        val outbounds = json.optJSONArray("outbounds") ?: return 0
        var patched = 0
        for (i in 0 until outbounds.length()) {
            val ob = outbounds.getJSONObject(i)
            if (tags.contains(ob.optString("tag", ""))) {
                val settings = ob.optJSONObject("settings") ?: JSONObject().also { ob.put("settings", it) }
                settings.put("address", cleanIp)
                patched++
            }
        }
        return patched
    }

    /**
     * F-15: TCP-first profile — move TCP fragment rules ahead of UDP noise rules
     * in the routing table (pure reorder; content untouched).
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
        val scored = tagged.map { (r, tags) ->
            val score = when {
                tags.any { it.startsWith("tcp-fragment") } -> 0
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
     * Inject a loopback DNS inbound (127.0.0.1:53, tag `dns-in`) so the VpnService
     * can relay client DNS queries into Xray's own resolver (fakedns + DoH).
     * Idempotent: returns false if a DNS inbound already exists.
     */
    fun addLocalDnsInbound(json: JSONObject): Boolean {
        val inbounds = json.optJSONArray("inbounds") ?: return false
        for (i in 0 until inbounds.length()) {
            val ib = inbounds.getJSONObject(i)
            if (ib.optString("tag") == "dns-in") return false
            if (ib.optString("protocol") == "dns" && ib.optInt("port", -1) == 53) return false
        }
        inbounds.put(JSONObject().put("tag", "dns-in").put("protocol", "dns").put("listen", "127.0.0.1").put("port", 53))
        return true
    }

    /**
     * Xray refuses to start when `dns.servers` references a FakeDNS engine that
     * no inbound provides. The official subscription lists "fakedns" in
     * `dns.servers` (and in `sniffing.destOverride`) while defining only a
     * `mixed` inbound — a fatal config error ("fakedns not found"), observed as
     * an immediate silent core exit on the emulator. Drop the dangling
     * references; DoH/localhost servers keep DNS working and TLS/HTTP sniffing
     * still drives domain routing.
     * Returns the number of references removed (0 = config was already fine).
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
                kept.put(s)
            }
            dns.put("servers", kept)
        }
        for (i in 0 until ibs.length()) {
            val sniff = ibs.getJSONObject(i).optJSONObject("sniffing") ?: continue
            val ov = sniff.optJSONArray("destOverride") ?: continue
            val kept = JSONArray()
            for (j in 0 until ov.length()) {
                val v = ov.optString(j, "")
                if (v.equals("fakedns", ignoreCase = true)) { removed++; continue }
                kept.put(v)
            }
            sniff.put("destOverride", kept)
        }
        return removed
    }

    data class ImportInfo(val inbound: InboundInfo, val minCoreVersion: String, val entries: Int)

    /** F-16: validate a pasted/imported Xray config (array of one or more configs). */
    fun validateImport(raw: String): Result<ImportInfo> = try {
        val parsed = JSONArray(raw)
        require(parsed.length() > 0) { "empty config list" }
        val first = parsed.getJSONObject(0)
        val inbound = findInbound(first) ?: return Result.failure(IllegalArgumentException("no inbound with a port"))
        val min = first.optJSONObject("version")?.optString("min", "") ?: ""
        Result.success(ImportInfo(inbound, min, parsed.length()))
    } catch (e: Exception) {
        Result.failure(e)
    }
}
