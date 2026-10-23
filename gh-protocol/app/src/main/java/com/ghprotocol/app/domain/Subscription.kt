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
        return SubscriptionInfo(entries, System.currentTimeMillis(), SUBSCRIPTION_URL, raw)
    }
}

object Subscription {
    const val SUBSCRIPTION_URL =
        "https://raw.githubusercontent.com/patterniha/Serverless-for-Iran/refs/heads/main/Subscription/Serverless-for-Iran.json"
    /** GitHub mirror failover (F-6, Nova pattern): same file, different edge. */
    const val MIRROR_URL =
        "https://github.com/patterniha/Serverless-for-Iran/raw/main/Subscription/Serverless-for-Iran.json"
    const val STALE_AFTER_MS = 12L * 60 * 60 * 1000 // 12h (F-6)
}
