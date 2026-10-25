package com.ghprotocol.app.domain

/** One variant in the official subscription (e.g. Serverless-v52-fragA). */
data class EntryInfo(
    val remarks: String,
    val minCoreVersion: String,
    val inboundPort: Int,
    val features: List<String>
)

/** Parsed subscription snapshot. */
data class SubscriptionInfo(
    val entries: List<EntryInfo>,
    val fetchedAt: Long,
    val source: String,
    val rawJson: String
)

/**
 * Parser for the official Serverless-for-Iran subscription format
 * (JSON array of full Xray configs). Pure + unit-tested.
 */
object SubscriptionParser {
    fun parse(raw: String): SubscriptionInfo {
        val root = org.json.JSONArray(raw)
        val entries = mutableListOf<EntryInfo>()
        for (i in 0 until root.length()) {
            val e = root.getJSONObject(i)
            val remarks = e.optString("remarks", "entry-$i")
            val minCore = e.optJSONObject("version")?.optString("min", "unknown") ?: "unknown"
            var port = 0
            val inbounds = e.optJSONArray("inbounds")
            if (inbounds != null && inbounds.length() > 0) {
                port = inbounds.getJSONObject(0).optInt("port", 0)
            }
            val features = mutableListOf<String>()
            val outbounds = e.optJSONArray("outbounds")
            if (outbounds != null) {
                for (j in 0 until outbounds.length()) {
                    val tag = outbounds.getJSONObject(j).optString("tag", "")
                    if (tag.startsWith("tcp-fragment") || tag.startsWith("udp-")) {
                        features.add(tag.removePrefix("tcp-").removePrefix("udp-"))
                    }
                }
            }
            entries.add(EntryInfo(remarks, minCore, port, features.distinct()))
        }
        return SubscriptionInfo(entries, System.currentTimeMillis(), Subscription.SUBSCRIPTION_URL, raw)
    }
}

object Subscription {
    const val SUBSCRIPTION_URL =
        "https://raw.githubusercontent.com/patterniha/Serverless-for-Iran/refs/heads/main/Subscription/Serverless-for-Iran.json"
    /** GitHub mirror failover (F-6, Nova pattern): same file, different edge. */
    const val MIRROR_URL =
        "https://github.com/patterniha/Serverless-for-Iran/raw/main/Subscription/Serverless-for-Iran.json"
    const val STALE_AFTER_MS = 12L * 60 * 60 * 1000 // 12h (F-6)

    /**
     * Rule #13: Embedded fallback Serverless-for-Iran config with full TLS ClientHello
     * fragmentation and DoH bootstrap hosts so first-launch users can establish a
     * working fragmented tunnel even when GitHub edges are blocked.
     */
    val EMBEDDED_FALLBACK_JSON: String = """
    [
      {
        "remarks": "Serverless-v52-fragA",
        "version": {"min": "26.6.27"},
        "log": {"loglevel": "warning"},
        "dns": {
          "hosts": {"cloudflare-dns.com": "1.1.1.1", "dns.google": "8.8.8.8"},
          "servers": ["https://cloudflare-dns.com/dns-query", "1.1.1.1", "8.8.8.8"]
        },
        "inbounds": [
          {
            "tag": "mixed-in",
            "listen": "127.0.0.1",
            "port": 10808,
            "protocol": "mixed",
            "settings": {"udp": true},
            "sniffing": {"enabled": true, "destOverride": ["tls", "http"]}
          }
        ],
        "outbounds": [
          {
            "tag": "tcp-fragment",
            "protocol": "freedom",
            "settings": {
              "domainStrategy": "UseIP",
              "fragment": {"packets": "tlshello", "length": "10-20", "interval": "10-20"}
            },
            "streamSettings": {
              "sockopt": {"tcpNoDelay": true}
            }
          },
          {"tag": "dns-out", "protocol": "dns"},
          {"tag": "block", "protocol": "blackhole"}
        ],
        "routing": {
          "domainStrategy": "IPIfNonMatch",
          "rules": [
            {"type": "field", "inboundTag": ["mixed-in"], "outboundTag": "tcp-fragment"}
          ]
        }
      },
      {
        "remarks": "Serverless-v52-fragB",
        "version": {"min": "26.6.27"},
        "log": {"loglevel": "warning"},
        "dns": {
          "hosts": {"cloudflare-dns.com": "1.0.0.1", "dns.google": "8.8.4.4"},
          "servers": ["https://cloudflare-dns.com/dns-query", "1.0.0.1", "8.8.4.4"]
        },
        "inbounds": [
          {
            "tag": "mixed-in",
            "listen": "127.0.0.1",
            "port": 10808,
            "protocol": "mixed",
            "settings": {"udp": true},
            "sniffing": {"enabled": true, "destOverride": ["tls", "http"]}
          }
        ],
        "outbounds": [
          {
            "tag": "tcp-fragment",
            "protocol": "freedom",
            "settings": {
              "domainStrategy": "UseIP",
              "fragment": {"packets": "tlshello", "length": "5-15", "interval": "15-30"}
            },
            "streamSettings": {
              "sockopt": {"tcpNoDelay": true}
            }
          },
          {"tag": "dns-out", "protocol": "dns"},
          {"tag": "block", "protocol": "blackhole"}
        ],
        "routing": {
          "domainStrategy": "IPIfNonMatch",
          "rules": [
            {"type": "field", "inboundTag": ["mixed-in"], "outboundTag": "tcp-fragment"}
          ]
        }
      }
    ]
    """.trimIndent()
}
