package com.ghprotocol.app

import com.ghprotocol.app.core.ConfigPatcher
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
        val before = sample.toString()
        val patched = ConfigPatcher.patchCleanEgress(sample, "104.16.132.229")
        assertEquals(2, patched)
        val frag = sample.getJSONArray("outbounds").getJSONObject(1)
        assertEquals("104.16.132.229", frag.getJSONObject("settings").getString("address"))
        // SNI/Host/Path untouched: finalmask intact
        assertTrue(frag.getJSONObject("streamSettings").has("finalmask"))
        // udp-noises NOT patched
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
        assertEquals("dns", dnsIn.getString("protocol"))
        assertEquals(53, dnsIn.getInt("port"))
        assertEquals("127.0.0.1", dnsIn.getString("listen"))
        // idempotent
        assertFalse(ConfigPatcher.addLocalDnsInbound(c))
        assertEquals(2, c.getJSONArray("inbounds").length())
        // existing dns:53 inbound not duplicated
        val c2 = JSONObject("""{"inbounds": [{"tag": "x", "port": 53, "protocol": "dns"}]}""")
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

    @Test fun importValidation() {
        val raw = JSONArray().put(sample).toString()
        val r = ConfigPatcher.validateImport(raw).getOrThrow()
        assertEquals(10808, r.inbound.port)
        assertEquals("26.6.27", r.minCoreVersion)
        assertTrue(ConfigPatcher.validateImport("not json").isFailure)
        assertTrue(ConfigPatcher.validateImport("[]").isFailure)
    }
}
