package com.ghprotocol.app.core

import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import java.io.File
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale
import java.util.concurrent.atomic.AtomicLong

enum class LogLevel { INFO, SUCCESS, WARN, ERROR }

enum class LogCategory { STEP, XRAY, TUN, DNS, PROBE }

data class TunnelLogEntry(
    val id: Long,
    val timeText: String,
    val level: LogLevel,
    val category: LogCategory,
    val messageFa: String,
    val rawTech: String
)

data class TunnelTelemetry(
    val bytesUp: Long = 0L,
    val bytesDown: Long = 0L,
    val rateUpBps: Long = 0L,
    val rateDownBps: Long = 0L,
    val activeTcpSessions: Int = 0,
    val dnsQueriesHandled: Int = 0,
    val verifiedPingMs: Int? = null,
    val activeCleanIp: String? = null,
    val activeProfile: String = "Serverless-v52-fragA",
    val stepIndex: Int = 0,
    val stepTitleFa: String = "آمادهٔ اتصال",
    val isAutoHealing: Boolean = false
)

/**
 * Thread-safe live connection log and real-time traffic telemetry store
 * (Psiphon / v2rayNG / Hiddify pattern, privacy-masked).
 */
object TunnelLogBuffer {

    private const val MAX_LOGS = 250
    private val seqGen = AtomicLong(1L)
    private val totalUp = AtomicLong(0L)
    private val totalDown = AtomicLong(0L)
    private val dnsCount = AtomicLong(0L)
    @Volatile
    private var lastSampleTimeMs: Long = System.currentTimeMillis()
    @Volatile
    private var lastSampleUp: Long = 0L
    @Volatile
    private var lastSampleDown: Long = 0L

    private val _logs = MutableStateFlow<List<TunnelLogEntry>>(emptyList())
    val logs: StateFlow<List<TunnelLogEntry>> = _logs.asStateFlow()

    private val _telemetry = MutableStateFlow(TunnelTelemetry())
    val telemetry: StateFlow<TunnelTelemetry> = _telemetry.asStateFlow()

    private val lock = Any()

    fun log(
        level: LogLevel,
        category: LogCategory,
        messageFa: String,
        rawTech: String = messageFa
    ) {
        val timeFmt = SimpleDateFormat("HH:mm:ss", Locale.US).format(Date())
        val entry = TunnelLogEntry(
            id = seqGen.getAndIncrement(),
            timeText = timeFmt,
            level = level,
            category = category,
            messageFa = messageFa,
            rawTech = sanitizeLine(rawTech)
        )
        synchronized(lock) {
            val next = (_logs.value + entry).takeLast(MAX_LOGS)
            _logs.value = next
        }
    }

    fun updateStep(
        stepIndex: Int,
        stepTitleFa: String,
        isAutoHealing: Boolean = _telemetry.value.isAutoHealing
    ) {
        _telemetry.value = _telemetry.value.copy(
            stepIndex = stepIndex,
            stepTitleFa = stepTitleFa,
            isAutoHealing = isAutoHealing
        )
    }

    fun updatePingAndProfile(
        pingMs: Int?,
        cleanIp: String? = _telemetry.value.activeCleanIp,
        profile: String = _telemetry.value.activeProfile
    ) {
        _telemetry.value = _telemetry.value.copy(
            verifiedPingMs = pingMs,
            activeCleanIp = cleanIp,
            activeProfile = profile
        )
    }

    fun recordTraffic(upDelta: Int, downDelta: Int, activeSessions: Int) {
        val u = if (upDelta > 0) totalUp.addAndGet(upDelta.toLong()) else totalUp.get()
        val d = if (downDelta > 0) totalDown.addAndGet(downDelta.toLong()) else totalDown.get()
        val now = System.currentTimeMillis()
        val elapsedMs = (now - lastSampleTimeMs).coerceAtLeast(1L)
        var rateUp = _telemetry.value.rateUpBps
        var rateDown = _telemetry.value.rateDownBps
        if (elapsedMs >= 800L) {
            rateUp = ((u - lastSampleUp) * 1000L) / elapsedMs
            rateDown = ((d - lastSampleDown) * 1000L) / elapsedMs
            lastSampleTimeMs = now
            lastSampleUp = u
            lastSampleDown = d
        }
        _telemetry.value = _telemetry.value.copy(
            bytesUp = u,
            bytesDown = d,
            rateUpBps = rateUp.coerceAtLeast(0L),
            rateDownBps = rateDown.coerceAtLeast(0L),
            activeTcpSessions = activeSessions
        )
    }

    fun recordDnsHandled() {
        val c = dnsCount.incrementAndGet().toInt()
        _telemetry.value = _telemetry.value.copy(dnsQueriesHandled = c)
    }

    fun resetSessionStats() {
        totalUp.set(0L)
        totalDown.set(0L)
        dnsCount.set(0L)
        lastSampleTimeMs = System.currentTimeMillis()
        lastSampleUp = 0L
        lastSampleDown = 0L
        _telemetry.value = TunnelTelemetry(
            activeCleanIp = _telemetry.value.activeCleanIp,
            activeProfile = _telemetry.value.activeProfile
        )
    }

    fun clear() {
        synchronized(lock) {
            _logs.value = emptyList()
        }
    }

    fun exportAllText(): String {
        val t = _telemetry.value
        val header = buildString {
            appendLine("=== Gh Protocol Diagnostic Log ===")
            appendLine("Profile: ${t.activeProfile} | CleanIP: ${t.activeCleanIp ?: "auto"} | VerifiedPing: ${t.verifiedPingMs ?: -1} ms")
            appendLine("Traffic: Up=${formatBytes(t.bytesUp)} Down=${formatBytes(t.bytesDown)} | ActiveTCP=${t.activeTcpSessions} | DNS=${t.dnsQueriesHandled}")
            appendLine("----------------------------------")
        }
        val body = _logs.value.joinToString("\n") { e ->
            "[${e.timeText}] [${e.level.name}/${e.category.name}] ${e.messageFa} | ${e.rawTech}"
        }
        return header + body
    }

    /** Ingest recent lines from Xray's stdout/stderr log file without duplicating. */
    fun ingestXrayLogTail(outFile: File, maxLines: Int = 8) {
        if (!outFile.exists() || outFile.length() == 0L) return
        try {
            val lines = outFile.readLines().takeLast(maxLines)
            val existingRaw = _logs.value.takeLast(30).map { it.rawTech }.toSet()
            for (line in lines) {
                val trimmed = line.trim()
                if (trimmed.isEmpty()) continue
                val sanitized = sanitizeLine(trimmed)
                if (sanitized in existingRaw) continue
                val lvl = when {
                    trimmed.contains("[Error]", ignoreCase = true) || trimmed.contains("failed", ignoreCase = true) -> LogLevel.WARN
                    trimmed.contains("started", ignoreCase = true) -> LogLevel.SUCCESS
                    else -> LogLevel.INFO
                }
                log(
                    level = lvl,
                    category = LogCategory.XRAY,
                    messageFa = "گزارش هستهٔ Xray",
                    rawTech = sanitized
                )
            }
        } catch (_: Exception) {
            // ignore concurrent read errors
        }
    }

    fun formatBytes(bytes: Long): String {
        if (bytes < 1024L) return "${bytes} B"
        val kb = bytes / 1024.0
        if (kb < 1024.0) return String.format(Locale.US, "%.1f KB", kb)
        val mb = kb / 1024.0
        return String.format(Locale.US, "%.2f MB", mb)
    }

    private fun sanitizeLine(raw: String): String {
        val ipRegex = Regex("""\b(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})\b""")
        return ipRegex.replace(raw) { m ->
            val full = m.value
            if (full == "127.0.0.1" || full == "1.1.1.1" || full == "8.8.8.8" || full.startsWith("10.8.0.") || full.startsWith("162.159.") || full.startsWith("104.16.") || full.startsWith("104.18.")) {
                full
            } else {
                "${m.groupValues[1]}.${m.groupValues[2]}.x.x"
            }
        }
    }
}
