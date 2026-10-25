package com.ghprotocol.app.core

import com.ghprotocol.app.core.net.RelayStats
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

/** Truthful connection states. `VERIFIED` requires remote payload through the relay. */
enum class TunnelState {
    IDLE,
    STARTING,
    CORE_READY,
    VERIFYING,
    VERIFIED,
    DEGRADED,
    FAILED
}

/**
 * Live telemetry and log store for the UI, in the Psiphon / v2rayNG / Hiddify style.
 *
 * Invariants (v1.6, see DIAGNOSIS 2026-10-25 §D5):
 *  - `bytesUp` / `bytesDown` / `activeTcpSessions` are **copied from the relay's counters**
 *    ([setRelayStats]); nothing else may add to them, so they always equal the bytes the
 *    datapath really forwarded.
 *  - `dnsQueriesHandled` counts answered queries; `dnsQueriesFailed` counts real SERVFAILs.
 *  - `payloadVerified` is only true after [com.ghprotocol.app.core.net.TunnelSelfTest].
 *  - destination IPs in logs are masked ([sanitizeLine]).
 */
object TunnelLogBuffer {

    private const val MAX_LOGS = 250
    private const val RATE_WINDOW_MS = 700L

    private val seq = AtomicLong(1)
    private val lock = Any()

    private val _logs = MutableStateFlow<List<TunnelLogEntry>>(emptyList())
    val logs: StateFlow<List<TunnelLogEntry>> = _logs.asStateFlow()

    private val _telemetry = MutableStateFlow(TunnelTelemetry())
    val telemetry: StateFlow<TunnelTelemetry> = _telemetry.asStateFlow()

    private var lastRateTimeMs = System.currentTimeMillis()
    private var lastRateUp = 0L
    private var lastRateDown = 0L

    fun log(
        level: LogLevel,
        category: LogCategory,
        messageFa: String,
        rawTech: String = messageFa
    ) {
        val entry = TunnelLogEntry(
            id = seq.getAndIncrement(),
            timeText = SimpleDateFormat("HH:mm:ss", Locale.US).format(Date()),
            level = level,
            category = category,
            messageFa = messageFa,
            rawTech = sanitizeLine(rawTech)
        )
        synchronized(lock) {
            _logs.value = (_logs.value + entry).takeLast(MAX_LOGS)
        }
    }

    fun clear() {
        synchronized(lock) { _logs.value = emptyList() }
    }

    // ---------------------------------------------------------------- state / progress

    fun updateStep(stepIndex: Int, stepTitleFa: String, isAutoHealing: Boolean = false) {
        _telemetry.value = _telemetry.value.copy(
            stepIndex = stepIndex,
            stepTitleFa = stepTitleFa,
            isAutoHealing = isAutoHealing
        )
    }

    fun updateProfile(profile: String, cleanIp: String?) {
        _telemetry.value = _telemetry.value.copy(activeProfile = profile, activeCleanIp = cleanIp)
    }

    fun setTunnelState(state: TunnelState, detail: String, payloadVerified: Boolean = false) {
        _telemetry.value = _telemetry.value.copy(
            tunnelState = state,
            tunnelDetail = sanitizeLine(detail).take(300),
            payloadVerified = payloadVerified
        )
    }

    fun setIpv6Mode(mode: String) {
        _telemetry.value = _telemetry.value.copy(ipv6Mode = mode)
    }

    /** Backwards-compatible combined update used by the view model. */
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

    fun setVerifiedPing(ms: Int?) {
        _telemetry.value = _telemetry.value.copy(verifiedPingMs = ms)
    }

    /** Copy the relay's authoritative counters (never accumulate per call site). */
    fun setRelayStats(stats: RelayStats) {
        val now = System.currentTimeMillis()
        val elapsed = now - lastRateTimeMs
        var upRate = _telemetry.value.rateUpBps
        var downRate = _telemetry.value.rateDownBps
        if (elapsed >= RATE_WINDOW_MS) {
            upRate = ((stats.bytesUp - lastRateUp) * 1000L / elapsed).coerceAtLeast(0L)
            downRate = ((stats.bytesDown - lastRateDown) * 1000L / elapsed).coerceAtLeast(0L)
            lastRateTimeMs = now
            lastRateUp = stats.bytesUp
            lastRateDown = stats.bytesDown
        }
        _telemetry.value = _telemetry.value.copy(
            bytesUp = stats.bytesUp,
            bytesDown = stats.bytesDown,
            rateUpBps = upRate,
            rateDownBps = downRate,
            activeTcpSessions = stats.activeFlows,
            relayFlowsOpened = stats.flowsOpened,
            relayFlowsClosed = stats.flowsClosed,
            relayConnectFailures = stats.connectFailures,
            relayRetransmits = stats.retransmits,
            relaySegmentsUp = stats.segmentsUp,
            relaySegmentsDown = stats.segmentsDown,
            relayUdpFragmentsDropped = stats.droppedFragments,
            closeReasons = stats.closeReasons
        )
    }

    /** Legacy delta API (kept for the telemetry test): adds to the totals. */
    @Synchronized
    fun recordTraffic(upDelta: Int, downDelta: Int, activeSessions: Int) {
        val up = _telemetry.value.bytesUp + upDelta.coerceAtLeast(0)
        val down = _telemetry.value.bytesDown + downDelta.coerceAtLeast(0)
        _telemetry.value = _telemetry.value.copy(
            bytesUp = up,
            bytesDown = down,
            activeTcpSessions = activeSessions
        )
    }

    fun recordDnsHandled() {
        _telemetry.value = _telemetry.value.copy(dnsQueriesHandled = _telemetry.value.dnsQueriesHandled + 1)
    }

    /** One finished query: counts as handled, and as failed when it produced a SERVFAIL. */
    fun recordDnsResult(path: String, ms: Long, ok: Boolean, detail: String = "") {
        val current = _telemetry.value
        _telemetry.value = current.copy(
            dnsQueriesHandled = current.dnsQueriesHandled + 1,
            lastDnsPath = path,
            lastDnsLatencyMs = ms,
            dnsQueriesFailed = if (ok) current.dnsQueriesFailed else current.dnsQueriesFailed + 1,
            lastDnsDetail = detail.take(200)
        )
    }

    fun recordUdpDropped() {
        _telemetry.value = _telemetry.value.copy(udpDropped = _telemetry.value.udpDropped + 1)
    }

    fun resetSessionStats() = resetSession()

    fun resetSession() {
        _telemetry.value = TunnelTelemetry()
        lastRateTimeMs = System.currentTimeMillis()
        lastRateUp = 0
        lastRateDown = 0
    }

    // ---------------------------------------------------------------- export / ingest

    fun exportText(): String {
        val t = _telemetry.value
        val header = buildString {
            appendLine("=== Gh Protocol diagnostics ===")
            appendLine("profile=${t.activeProfile} cleanIp=${t.activeCleanIp ?: "auto"} state=${t.tunnelState}")
            appendLine("payloadVerified=${t.payloadVerified} detail=${t.tunnelDetail}")
            appendLine("bytesUp=${t.bytesUp} bytesDown=${t.bytesDown} activeTcp=${t.activeTcpSessions}")
            appendLine("relay opened=${t.relayFlowsOpened} closed=${t.relayFlowsClosed} connectFailures=${t.relayConnectFailures} retransmits=${t.relayRetransmits}")
            appendLine("closeReasons=${t.closeReasons}")
            appendLine("dns handled=${t.dnsQueriesHandled} failed=${t.dnsQueriesFailed} lastPath=${t.lastDnsPath ?: "-"} lastMs=${t.lastDnsLatencyMs}")
            appendLine("udpDropped=${t.udpDropped} ipv6=${t.ipv6Mode} verifiedPingMs=${t.verifiedPingMs ?: -1}")
            appendLine("--------------------------------")
        }
        val body = _logs.value.joinToString("\n") {
            "[${it.timeText}] ${it.level}/${it.category} ${it.messageFa} :: ${it.rawTech}"
        }
        return header + body
    }

    /** Ingest new lines from Xray's log file (tail only, deduplicated). */
    fun ingestXrayLogTail(file: File, maxLines: Int = 6) {
        if (!file.exists() || file.length() == 0L) return
        val lines = try {
            file.readLines().takeLast(maxLines)
        } catch (_: Exception) {
            return
        }
        val known = synchronized(lock) { _logs.value.map { it.rawTech }.toSet() }
        for (line in lines) {
            val trimmed = line.trim()
            if (trimmed.isEmpty() || trimmed in known) continue
            val level = when {
                trimmed.contains("failed", true) || trimmed.contains("error", true) -> LogLevel.WARN
                trimmed.contains("started", true) -> LogLevel.SUCCESS
                else -> LogLevel.INFO
            }
            log(level, LogCategory.XRAY, "گزارش هستهٔ Xray", trimmed)
        }
    }

    fun formatBytes(bytes: Long): String = when {
        bytes < 1024 -> "$bytes B"
        bytes < 1024 * 1024 -> String.format(Locale.US, "%.1f KB", bytes / 1024.0)
        else -> String.format(Locale.US, "%.2f MB", bytes / (1024.0 * 1024.0))
    }

    /**
     * Mask destination addresses in log lines. Loopback/known anycast addresses stay readable
     * because they identify *our own* components, not the user's destinations.
     */
    fun sanitizeLine(raw: String): String {
        val regex = Regex("""\b(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})\b""")
        return regex.replace(raw) { match ->
            val value = match.value
            val keep = value == "127.0.0.1" || value == "0.0.0.0" ||
                value.startsWith("10.8.0.") || value == "1.1.1.1" || value == "8.8.8.8" ||
                value == "1.0.0.1" || value == "8.8.4.4" || value.startsWith("104.16.248.") ||
                value.startsWith("104.16.249.")
            if (keep) value else "${match.groupValues[1]}.${match.groupValues[2]}.x.x"
        }
    }
}

/**
 * Snapshot of everything the UI shows. All byte fields come from the relay's counters, and
 * `payloadVerified` is only set by a successful in-tunnel self-test.
 */
data class TunnelTelemetry(
    val bytesUp: Long = 0L,
    val bytesDown: Long = 0L,
    val rateUpBps: Long = 0L,
    val rateDownBps: Long = 0L,
    val activeTcpSessions: Int = 0,
    val dnsQueriesHandled: Int = 0,
    val dnsQueriesFailed: Int = 0,
    val lastDnsPath: String? = null,
    val lastDnsLatencyMs: Long = 0L,
    val lastDnsDetail: String = "",
    val verifiedPingMs: Int? = null,
    val activeCleanIp: String? = null,
    val activeProfile: String = "Serverless-v52-fragA",
    val stepIndex: Int = 0,
    val stepTitleFa: String = "آمادهٔ اتصال",
    val isAutoHealing: Boolean = false,
    val tunnelState: TunnelState = TunnelState.IDLE,
    val tunnelDetail: String = "",
    val payloadVerified: Boolean = false,
    val udpDropped: Long = 0L,
    val relayFlowsOpened: Long = 0L,
    val relayFlowsClosed: Long = 0L,
    val relayConnectFailures: Long = 0L,
    val relayRetransmits: Long = 0L,
    val relaySegmentsUp: Long = 0L,
    val relaySegmentsDown: Long = 0L,
    val relayUdpFragmentsDropped: Long = 0L,
    val closeReasons: Map<String, Long> = emptyMap(),
    val ipv6Mode: String = "tunneled"
)
