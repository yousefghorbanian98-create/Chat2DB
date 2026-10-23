package com.ghprotocol.app.domain

import android.content.Context
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.net.HttpURLConnection
import java.net.URL
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

/**
 * F-5/F-6/F-12: subscription with on-device cache.
 * - First launch offline: falls back to cache, honest "couldn't update" message
 * - Auto re-sync on link recovery (NetworkMonitor hook) and every 12h (in-app)
 * - Mirror failover when the primary edge is filtered
 */
class SubscriptionRepository(private val context: Context) {

    private fun cacheFile() = java.io.File(context.filesDir, "subscription.json")
    private fun metaFile() = java.io.File(context.filesDir, "subscription.meta")

    /** Cached snapshot if fresh enough, else null. */
    fun cached(): SubscriptionInfo? = try {
        val raw = cacheFile().takeIf { it.exists() }?.readText() ?: return null
        val meta = metaFile().readText().trim().toLongOrNull() ?: return null
        if (System.currentTimeMillis() - meta > Subscription.STALE_AFTER_MS) null
        else SubscriptionParser.parse(raw).copy(fetchedAt = meta)
    } catch (e: Exception) {
        null
    }

    /** Cached snapshot regardless of freshness (offline first-launch, F-5). */
    fun cachedAnyAge(): SubscriptionInfo? = try {
        val raw = cacheFile().takeIf { it.exists() }?.readText() ?: return null
        val meta = metaFile().readText().trim().toLongOrNull() ?: 0L
        SubscriptionParser.parse(raw).copy(fetchedAt = meta)
    } catch (e: Exception) {
        null
    }

    suspend fun update(): Result<SubscriptionInfo> = withContext(Dispatchers.IO) {
        for (url in listOf(Subscription.SUBSCRIPTION_URL, Subscription.MIRROR_URL)) {
            try {
                val raw = fetch(url)
                val parsed = SubscriptionParser.parse(raw)
                cacheFile().writeText(raw)
                metaFile().writeText(parsed.fetchedAt.toString())
                return@withContext Result.success(parsed)
            } catch (e: Exception) {
                // try next source (mirror failover)
            }
        }
        Result.failure(java.io.IOException("subscription update failed (primary + mirror)"))
    }

    private fun fetch(url: String): String {
        val conn = URL(url).openConnection() as HttpURLConnection
        conn.connectTimeout = 20_000
        conn.readTimeout = 30_000
        conn.instanceFollowRedirects = true
        conn.setRequestProperty("User-Agent", "GhProtocol/0.1")
        val code = try {
            conn.responseCode
        } finally {
            conn.disconnect()
        }
        require(code in 200..299) { "HTTP $code from $url" }
        return conn.inputStream.bufferedReader().use { it.readText() }
    }

    fun lastUpdateText(): String? = try {
        val t = metaFile().takeIf { it.exists() }?.readText()?.trim()?.toLongOrNull() ?: return null
        val fmt = SimpleDateFormat("dd MMM yyyy, HH:mm", Locale.getDefault())
        fmt.format(Date(t))
    } catch (e: Exception) {
        null
    }
}
