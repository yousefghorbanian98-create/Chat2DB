package com.ghprotocol.app

import com.ghprotocol.app.core.ConfigPatcher
import com.ghprotocol.app.ui.theme.MotionSpec
import org.json.JSONArray
import org.json.JSONObject
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

class ConfigPatcherTest {

    private val sample = JSONObject(
        """
        {
          "version": {"min": "26.6.27"},
          "inbounds": [{"tag": "mixed-in", "port": 10808, "protocol": "mixed"}],
          "outbounds": [
            {"tag": "block", "protocol": "block"},
            {"tag": "tcp-fragment", "protocol": "direct", "streamSettings": {"finalmask": {"tcp": [{"type": "fragment"}]}}},
            {"tag": "tcp-fragment-tls", "protocol": "direct", "streamSettings": {"finalmask": {"tcp": []}}},
            {"tag": "udp-noises", "protocol": "direct", "streamSettings": {"finalmask": {"udp": []}}}
          ],
          "routing": {"rules": [
            {"type": "field", "inboundTag": ["mixed-in"], "outboundTag": ["udp-noises"]},
            {"type": "field", "inboundTag": ["mixed-in"], "outboundTag": ["tcp-fragment"]}
          ]}
        }
        """.trimIndent()
    )

    @Test fun findsInbound() {
        val ib = ConfigPatcher.findInbound(sample)!!
        assertEquals("mixed-in", ib.tag)
        assertEquals(10808, ib.port)
    }

    @Test fun cleanEgressPatchesOnlyAddress() {
        val patched = ConfigPatcher.patchCleanEgress(sample, "104.16.132.229")
        assertEquals(2, patched)
        val frag = sample.getJSONArray("outbounds").getJSONObject(1)
        assertEquals("104.16.132.229", frag.getJSONObject("settings").getString("address"))
        assertTrue(frag.getJSONObject("streamSettings").has("finalmask"))
        val udp = sample.getJSONArray("outbounds").getJSONObject(3)
        assertEquals(0, udp.optJSONObject("settings")?.optString("address", "-")?.let { 1 } ?: 0)
    }

    @Test fun tcpFirstReordersRules() {
        assertTrue(ConfigPatcher.tcpFirstProfile(sample))
        val rules = sample.getJSONObject("routing").getJSONArray("rules")
        val first = rules.getJSONObject(0)
        assertEquals("tcp-fragment", first.getJSONArray("outboundTag").getString(0))
        val second = rules.getJSONObject(1)
        assertEquals("udp-noises", second.getJSONArray("outboundTag").getString(0))
    }

    @Test fun localDnsInboundInjectedOnce() {
        val c = JSONObject("""{"inbounds": [{"tag": "mixed-in", "port": 10808, "protocol": "mixed"}]}""")
        assertTrue(ConfigPatcher.addLocalDnsInbound(c))
        val ibs = c.getJSONArray("inbounds")
        assertEquals(2, ibs.length())
        val dnsIn = ibs.getJSONObject(1)
        assertEquals("dokodemo-door", dnsIn.getString("protocol"))
        assertEquals(ConfigPatcher.DNS_IN_PORT, dnsIn.getInt("port"))
        assertEquals("127.0.0.1", dnsIn.getString("listen"))
        val rules = c.getJSONObject("routing").getJSONArray("rules")
        assertEquals("dns-in", rules.getJSONObject(0).getJSONArray("inboundTag").getString(0))
        assertEquals("dns-out", rules.getJSONObject(0).getString("outboundTag"))
        assertEquals("dns", c.getJSONArray("outbounds").getJSONObject(0).getString("protocol"))
        assertFalse(ConfigPatcher.addLocalDnsInbound(c))
        assertEquals(2, c.getJSONArray("inbounds").length())
        val c2 = JSONObject("""{"inbounds": [{"tag": "x", "port": 15353, "protocol": "dokodemo-door"}]}""")
        assertFalse(ConfigPatcher.addLocalDnsInbound(c2))
    }

    @Test fun stringOutboundTagReorder() {
        val c = JSONObject(
            """{"routing": {"rules": [
                {"outboundTag": "udp-noises", "type": "field"},
                {"outboundTag": "tcp-fragment-tls", "type": "field"},
                {"outboundTag": "block", "type": "field"}
            ]}}"""
        )
        assertTrue(ConfigPatcher.tcpFirstProfile(c))
        val rules = c.getJSONObject("routing").getJSONArray("rules")
        assertEquals("tcp-fragment-tls", rules.getJSONObject(0).getString("outboundTag"))
    }

    @Test fun dropsDanglingFakeDnsReferences() {
        val c = JSONObject(
            """{"inbounds": [{"tag": "mixed-in", "protocol": "mixed", "port": 10808,
                 "sniffing": {"enabled": true, "destOverride": ["fakedns", "tls", "http"]}}],
                "dns": {"servers": ["fakedns", "https://cloudflare-dns.com/dns-query", "localhost"]}}"""
        )
        assertEquals(3, ConfigPatcher.ensureConsistentDns(c))
        val servers = c.getJSONObject("dns").getJSONArray("servers")
        assertEquals(1, servers.length())
        assertEquals("https://cloudflare-dns.com/dns-query", servers.getString(0))
        val ov = c.getJSONArray("inbounds").getJSONObject(0)
            .getJSONObject("sniffing").getJSONArray("destOverride")
        assertEquals(2, ov.length())
        assertEquals("tls", ov.getString(0))
        assertEquals(0, ConfigPatcher.ensureConsistentDns(c))
    }

    @Test fun keepsFakeDnsWhenEnginePresent() {
        val c = JSONObject(
            """{"inbounds": [{"tag": "fakedns", "protocol": "fakedns", "port": 0,
                 "sniffing": {"destOverride": ["fakedns"]}}],
                "dns": {"servers": ["fakedns"]}}"""
        )
        assertEquals(0, ConfigPatcher.ensureConsistentDns(c))
        assertEquals(1, c.getJSONObject("dns").getJSONArray("servers").length())
    }

    @Test fun importValidation() {
        val raw = JSONArray().put(sample).toString()
        val r = ConfigPatcher.validateImport(raw).getOrThrow()
        assertEquals(10808, r.inbound.port)
        assertEquals("26.6.27", r.minCoreVersion)
        assertTrue(ConfigPatcher.validateImport("not json").isFailure)
        assertTrue(ConfigPatcher.validateImport("[]").isFailure)
    }

    @Test fun vlessUriConvertsWithFragmentAndCleanIpOverride() {
        val uri = "vless://11111111-2222-3333-4444-555555555555@edge.example.com:443?type=ws&security=tls&sni=sni.example.com&host=cdn.example.com&path=%2Fws&fp=chrome#Iran-CF-Node"
        val cfg = ConfigPatcher.parseUriToConfig(uri, cleanIp = "104.16.132.229").getOrThrow()
        assertEquals("Iran-CF-Node", cfg.getString("remarks"))
        val proxy = cfg.getJSONArray("outbounds").getJSONObject(0)
        assertEquals("vless", proxy.getString("protocol"))
        val vnext = proxy.getJSONObject("settings").getJSONArray("vnext").getJSONObject(0)
        // Clean IP overrides address while SNI and Host header remain intact
        assertEquals("104.16.132.229", vnext.getString("address"))
        assertEquals(443, vnext.getInt("port"))
        assertEquals("11111111-2222-3333-4444-555555555555", vnext.getJSONArray("users").getJSONObject(0).getString("id"))
        val ss = proxy.getJSONObject("streamSettings")
        assertEquals("tcp-fragment", ss.getJSONObject("sockopt").getString("dialerProxy"))
        assertEquals("sni.example.com", ss.getJSONObject("tlsSettings").getString("serverName"))
        assertEquals("cdn.example.com", ss.getJSONObject("wsSettings").getJSONObject("headers").getString("Host"))
        assertEquals("/ws", ss.getJSONObject("wsSettings").getString("path"))
        // Fragment outbound injected
        val frag = cfg.getJSONArray("outbounds").getJSONObject(1)
        assertEquals("tcp-fragment", frag.getString("tag"))
        assertEquals("tlshello", frag.getJSONObject("settings").getJSONObject("fragment").getString("packets"))
    }

    @Test fun trojanAndRealityUrisNormalizeAndValidate() {
        val batch = """
            vless://aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee@198.51.100.10:443?security=reality&sni=www.cloudflare.com&pbk=PUBKEY123&sid=01ab&type=tcp&flow=xtls-rprx-vision#Reality1
            trojan://my-secret-pass@trojan.example.com:8443?type=grpc&security=tls&sni=trojan.example.com&serviceName=grpc-tun#Trojan1
        """.trimIndent()
        val info = ConfigPatcher.validateImport(batch).getOrThrow()
        assertEquals(2, info.entries)
        assertEquals(10808, info.inbound.port)
        val arr = JSONArray(ConfigPatcher.normalizeImport(batch).getOrThrow())
        val realitySs = arr.getJSONObject(0).getJSONArray("outbounds").getJSONObject(0).getJSONObject("streamSettings")
        assertEquals("PUBKEY123", realitySs.getJSONObject("realitySettings").getString("publicKey"))
        val trojanOb = arr.getJSONObject(1).getJSONArray("outbounds").getJSONObject(0)
        assertEquals("trojan", trojanOb.getString("protocol"))
        assertEquals("grpc-tun", trojanOb.getJSONObject("streamSettings").getJSONObject("grpcSettings").getString("serviceName"))
    }

    @Test fun motionSpecRespectsReducedMotionAndCap() {
        assertEquals(0, MotionSpec.resolveDurationMs(0f, 200))
        assertEquals(200, MotionSpec.resolveDurationMs(1f, 200))
        assertEquals(300, MotionSpec.resolveDurationMs(2f, 250))
    }

    @Test fun embeddedFallbackHasTlsHelloFragmentAndDohHosts() {
        val arr = JSONArray(com.ghprotocol.app.domain.Subscription.EMBEDDED_FALLBACK_JSON)
        assertEquals(2, arr.length())
        val first = arr.getJSONObject(0)
        val frag = first.getJSONArray("outbounds").getJSONObject(0)
            .getJSONObject("settings").getJSONObject("fragment")
        assertEquals("tlshello", frag.getString("packets"))
        val dns = first.getJSONObject("dns")
        val hosts = dns.getJSONObject("hosts")
        // cloudflare-dns.com is bootstrapped to its own anycast address, never to the
        // IP-blocked 1.1.1.1/1.0.0.1 and never to another zone's edge (DIAGNOSIS §D1).
        assertEquals(ConfigPatcher.DOH_BOOTSTRAP_IPV4, hosts.getString("cloudflare-dns.com"))
        assertEquals("UseIPv4", dns.getString("queryStrategy"))
        val servers = dns.getJSONArray("servers")
        val addresses = (0 until servers.length()).map { servers.optString(it, "") }
        assertFalse(addresses.any { it.equals("fakedns", ignoreCase = true) })
        assertFalse(hosts.keys().asSequence().any { hosts.optString(it) == "1.1.1.1" })
        assertFalse(hosts.keys().asSequence().any { hosts.optString(it) == "1.0.0.1" })
    }

    @Test fun tunnelLogBufferMasksPrivateDestinationIpsAndTracksTelemetry() {
        com.ghprotocol.app.core.TunnelLogBuffer.clear()
        com.ghprotocol.app.core.TunnelLogBuffer.resetSessionStats()
        com.ghprotocol.app.core.TunnelLogBuffer.log(
            com.ghprotocol.app.core.LogLevel.INFO,
            com.ghprotocol.app.core.LogCategory.TUN,
            "بسته ارسال شد",
            "dial tcp 142.250.185.78:443 via 1.1.1.1"
        )
        val entries = com.ghprotocol.app.core.TunnelLogBuffer.logs.value
        assertEquals(1, entries.size)
        assertTrue(entries[0].rawTech.contains("142.250.x.x"))
        assertTrue(entries[0].rawTech.contains("1.1.1.1"))
        com.ghprotocol.app.core.TunnelLogBuffer.recordTraffic(2048, 4096, 3)
        val t = com.ghprotocol.app.core.TunnelLogBuffer.telemetry.value
        assertEquals(2048L, t.bytesUp)
        assertEquals(4096L, t.bytesDown)
        assertEquals(3, t.activeTcpSessions)
    }

    @Test fun serverlessForIranConfigFixesDohLoopAndPreservesDirectOutbounds() {
        val serverless = JSONObject(
            """
            {
              "dns": {
                "hosts": {
                  "geosite:category-ads-all": "#3",
                  "cloudflare-dns.com": "challenges.cloudflare.com"
                },
                "servers": [
                  {"address": "fakedns"},
                  {"tag": "no-filter-dns", "address": "https://cloudflare-dns.com/dns-query"},
                  {"tag": "domestic-dns", "address": "localhost"}
                ]
              },
              "inbounds": [{
                "tag": "mixed-in",
                "port": 10808,
                "protocol": "mixed",
                "sniffing": {"enabled": true, "destOverride": ["fakedns", "tls", "http"], "routeOnly": false}
              }],
              "outbounds": [
                {
                  "tag": "tcp-fragment-tls",
                  "protocol": "direct",
                  "streamSettings": {
                    "finalmask": {"tcp": [{"type": "fragment"}]},
                    "sockopt": {
                      "domainStrategy": "ForceIP",
                      "happyEyeballs": {"prioritizeIPv6": true}
                    }
                  }
                }
              ],
              "routing": {
                "domainStrategy": "IPOnDemand",
                "rules": [
                  {"outboundTag": "dns-out", "port": 53},
                  {"inboundTag": ["no-filter-dns"], "outboundTag": "tcp-fragment-tls"},
                  {"outboundTag": "tcp-fragment-tls", "network": "tcp", "port": "443", "ip": ["0.0.0.0/0"]}
                ]
              }
            }
            """.trimIndent()
        )
        ConfigPatcher.tcpFirstProfile(serverless)
        ConfigPatcher.ensureConsistentDns(serverless)
        ConfigPatcher.applySmartCleanIp(serverless, "172.64.33.229")
        ConfigPatcher.enforceReachableDns(serverless)

        // 1. The DoH bootstrap is pinned to the DoH zone itself, so the TLS handshake cannot
        //    land on an edge with a different zone (the v1.5 `context deadline exceeded` loop).
        val hosts = serverless.getJSONObject("dns").getJSONObject("hosts")
        assertEquals(ConfigPatcher.DOH_BOOTSTRAP_IPV4, hosts.getString("cloudflare-dns.com"))
        // A hostname mapped onto another hostname is a resolution loop: it must be gone.
        assertFalse(hosts.has("challenges.cloudflare.com"))
        // A clean IP is an *egress* choice and must never rewrite the DoH hostname.
        assertFalse(hosts.keys().asSequence().any { hosts.optString(it) == "172.64.33.229" })

        // 2. Direct/fragment outbound must NOT have settings.address hijacked to a Cloudflare IP
        val fragOb = serverless.getJSONArray("outbounds").getJSONObject(0)
        assertFalse(fragOb.optJSONObject("settings")?.has("address") == true)

        // 3. sniffing.routeOnly=true, sockopt.domainStrategy=UseIPv4, routing.domainStrategy=AsIs
        val sniff = serverless.getJSONArray("inbounds").getJSONObject(0).getJSONObject("sniffing")
        assertTrue(sniff.getBoolean("routeOnly"))
        val sockopt = fragOb.getJSONObject("streamSettings").getJSONObject("sockopt")
        assertEquals("UseIPv4", sockopt.getString("domainStrategy"))
        assertEquals("AsIs", serverless.getJSONObject("routing").getString("domainStrategy"))
        assertFalse(sockopt.getJSONObject("happyEyeballs").getBoolean("prioritizeIPv6"))

        // 4. Routing order preserved and the port:53 rule restricted to the dns-in inbound
        val rules = serverless.getJSONObject("routing").getJSONArray("rules")
        assertEquals("dns-out", rules.getJSONObject(0).getString("outboundTag"))
        assertEquals("dns-in", rules.getJSONObject(0).getJSONArray("inboundTag").getString(0))

        // 5. The effective plan is machine-checkable and free of dead ends
        val plan = ConfigPatcher.effectiveDnsPlan(serverless)
        assertEquals("UseIPv4", plan.queryStrategy)
        assertEquals(listOf("https://cloudflare-dns.com/dns-query"), plan.dohEndpoints)
        assertEquals(listOf(ConfigPatcher.DOH_BOOTSTRAP_IPV4), plan.dohBootstrapIps)
        assertTrue(plan.notes.any { it.startsWith("doh_bootstrap_zone_ok") })
        assertTrue(plan.notes.none { it.startsWith("doh_bootstrap_is_domain") })
        // Xray treats a DNS server's tag as an inbound tag for routing: that is the rule
        // which decides the outbound that actually carries the DoH request.
        assertEquals("tcp-fragment-tls", plan.dohOutbound)
        assertFalse(plan.servers.any { it.equals("fakedns", ignoreCase = true) })
        assertFalse(plan.servers.any { it.equals("localhost", ignoreCase = true) })
    }

    @Test fun bothEmbeddedProfilesGetAReachableDohPlan() {
        val raw = com.ghprotocol.app.domain.Subscription.EMBEDDED_FALLBACK_JSON
        for (index in 0..1) {
            val audit = ConfigPatcher.runtimeDnsAudit(raw, index, cleanIp = null)
            assertTrue("audit[$index] must describe the DoH endpoint: $audit", audit.contains("doh=https://cloudflare-dns.com/dns-query"))
            assertTrue("audit[$index] must not keep a domain bootstrap: $audit", !audit.contains("doh_bootstrap_is_domain"))
            assertTrue(
                "audit[$index] must not bootstrap to a blocked IP: $audit",
                !audit.contains("doh_bootstrap_ip_blocked_in_ir")
            )
            assertTrue("audit[$index] must not keep fakedns: $audit", !audit.contains("fakedns"))
        }
    }

    @Test fun cleanIpIsNeverWrittenIntoTheDohHostsMap() {
        val raw = com.ghprotocol.app.domain.Subscription.EMBEDDED_FALLBACK_JSON
        val cfg = ConfigPatcher.runtimeConfigForEntry(raw, 0, cleanIp = "172.64.33.229").getOrThrow()
        val hosts = cfg.getJSONObject("dns").getJSONObject("hosts")
        assertFalse(hosts.keys().asSequence().any { hosts.optString(it) == "172.64.33.229" })
        assertEquals(ConfigPatcher.DOH_BOOTSTRAP_IPV4, hosts.getString("cloudflare-dns.com"))
    }
