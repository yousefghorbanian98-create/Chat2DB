package com.ghprotocol.app.ui

import android.content.ClipData
import android.content.ClipboardManager
import android.content.Context
import androidx.compose.animation.AnimatedContent
import androidx.compose.animation.core.tween
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.togetherWith
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.CheckCircle
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material.icons.filled.Warning
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FilterChip
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextDirection
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.ghprotocol.app.core.LogCategory
import com.ghprotocol.app.core.LogLevel
import com.ghprotocol.app.core.TunnelLogBuffer
import com.ghprotocol.app.core.TunnelLogEntry
import com.ghprotocol.app.ui.theme.GhBlue
import com.ghprotocol.app.ui.theme.GhGreen
import com.ghprotocol.app.ui.theme.MotionSpec

private val LogEmerald = Color(0xFF34D399)
private val LogCyan = Color(0xFF22D3EE)
private val LogAmber = Color(0xFFF5A524)
private val LogRed = Color(0xFFE5484D)
private val TerminalBg = Color(0xFF060A14)
private val TerminalBorder = Color(0xFF1E293B)

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun LiveLogScreen(
    viewModel: HomeViewModel,
    modifier: Modifier = Modifier
) {
    val ui by viewModel.ui.collectAsState()
    val logs by TunnelLogBuffer.logs.collectAsState()
    val telemetry by TunnelLogBuffer.telemetry.collectAsState()
    val context = LocalContext.current

    var terminalMode by remember { mutableStateOf(false) }
    var selectedCategory by remember { mutableStateOf<LogCategory?>(null) }
    var copiedToast by remember { mutableStateOf(false) }

    val animMs = MotionSpec.durationMs(context, 220)

    DefyxMainScreenBackground(
        phase = ui.connectPhase,
        isAutoHealing = ui.isAutoHealing,
        modifier = modifier
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .verticalScroll(rememberScrollState())
                .padding(horizontal = 16.dp, vertical = 14.dp)
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Column {
                    Text(
                        text = "لاگ زنده و مانیتور ترافیک",
                        style = MaterialTheme.typography.titleLarge,
                        fontWeight = FontWeight.ExtraBold,
                        color = Color.White
                    )
                    Text(
                        text = "پروفایل: ${telemetry.activeProfile} · IP: ${telemetry.activeCleanIp ?: "خودکار"}",
                        style = MaterialTheme.typography.labelSmall,
                        color = Color.White.copy(alpha = 0.72f)
                    )
                }
            }

            Spacer(Modifier.height(10.dp))

            // 1. n8n-Inspired 5-Node Live Pipeline + Waveform Oscilloscope
            N8nPipelineFlowCard(
                telemetry = telemetry,
                isConnected = ui.connectPhase == ConnectPhase.CONNECTED
            )

            Spacer(Modifier.height(10.dp))

            LiveTrafficWaveformCard(telemetry = telemetry)

            Spacer(Modifier.height(10.dp))

            // 2. Real-time Traffic & Ping Telemetry Cards
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(10.dp)
            ) {
                TelemetryMiniCard(
                    title = "پینگ واقعی تونل",
                    value = telemetry.verifiedPingMs?.let { "$it ms" } ?: "—",
                    sub = if (telemetry.verifiedPingMs != null) "تاییدشده از داخل تونل" else "تست نشده",
                    accent = if (telemetry.verifiedPingMs != null) DefyxColors.DownloadGreen else DefyxColors.UploadCyan,
                    modifier = Modifier.weight(1f)
                )
                TelemetryMiniCard(
                    title = "ترافیک جلسه",
                    value = "↓ ${TunnelLogBuffer.formatBytes(telemetry.bytesDown)}",
                    sub = "↑ ${TunnelLogBuffer.formatBytes(telemetry.bytesUp)} · DNS: ${telemetry.dnsQueriesHandled}",
                    accent = DefyxColors.UploadCyan,
                    modifier = Modifier.weight(1f)
                )
            }

            Spacer(Modifier.height(12.dp))

            // 3. Dual-Mode Segmented Switch (Persian Step-by-Step vs Technical Terminal)
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .clip(RoundedCornerShape(12.dp))
                    .background(Color.Black.copy(alpha = 0.35f))
                    .padding(4.dp),
                horizontalArrangement = Arrangement.spacedBy(6.dp)
            ) {
                ModeTabButton(
                    text = "نمای گام‌به‌گام فارسی",
                    selected = !terminalMode,
                    onClick = { terminalMode = false },
                    modifier = Modifier.weight(1f)
                )
                ModeTabButton(
                    text = "ترمینال فنی Xray / TUN",
                    selected = terminalMode,
                    onClick = { terminalMode = true },
                    modifier = Modifier.weight(1f)
                )
            }

            Spacer(Modifier.height(12.dp))

            // 4. VengeanceUI RadialGlowButtons for Real Ping Test + Copy Log (with ic_defyx_copy) + Clear
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                VengeanceRadialGlowButton(
                    text = if (ui.isTestingUrl) "در حال تست..." else "تست پینگ واقعی",
                    iconRes = com.ghprotocol.app.R.drawable.ic_defyx_speed,
                    accentColor = DefyxColors.DownloadGreen,
                    onClick = { viewModel.runUrlPingTest() },
                    modifier = Modifier.weight(1.2f)
                )
                VengeanceRadialGlowButton(
                    text = if (copiedToast) "کپی شد ✓" else "کپی لاگ",
                    iconRes = com.ghprotocol.app.R.drawable.ic_defyx_copy,
                    accentColor = DefyxColors.BrandGold,
                    onClick = {
                        val cm = context.getSystemService(Context.CLIPBOARD_SERVICE) as? ClipboardManager
                        cm?.setPrimaryClip(ClipData.newPlainText("gh-protocol-log", TunnelLogBuffer.exportAllText()))
                        copiedToast = true
                    },
                    modifier = Modifier.weight(1f)
                )
                OutlinedButton(onClick = { TunnelLogBuffer.clear(); copiedToast = false }) {
                    Text("پاک", color = Color.White)
                }
            }

            Spacer(Modifier.height(14.dp))

            AnimatedContent(
                targetState = terminalMode,
                transitionSpec = {
                    fadeIn(tween(animMs)) togetherWith fadeOut(tween(animMs))
                },
                label = "log-mode-switch"
            ) { isTerminal ->
                if (!isTerminal) {
                    StepByStepPersianView(
                        stepIndex = telemetry.stepIndex,
                        stepTitle = telemetry.stepTitleFa,
                        isAutoHealing = telemetry.isAutoHealing,
                        verifiedPingMs = telemetry.verifiedPingMs,
                        logs = logs
                    )
                } else {
                    TechnicalTerminalView(
                        logs = logs,
                        selectedCategory = selectedCategory,
                        onSelectCategory = { selectedCategory = it }
                    )
                }
            }
        }
    }
}

@Composable
private fun TelemetryMiniCard(
    title: String,
    value: String,
    sub: String,
    accent: Color,
    modifier: Modifier = Modifier
) {
    Card(
        modifier = modifier,
        colors = CardDefaults.cardColors(containerColor = accent.copy(alpha = 0.10f)),
        shape = RoundedCornerShape(14.dp)
    ) {
        Column(Modifier.padding(14.dp)) {
            Text(title, style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
            Spacer(Modifier.height(4.dp))
            Text(value, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, color = accent)
            Spacer(Modifier.height(2.dp))
            Text(sub, style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
        }
    }
}

@Composable
private fun ModeTabButton(
    text: String,
    selected: Boolean,
    onClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    val bg = if (selected) GhBlue.copy(alpha = 0.22f) else Color.Transparent
    val fg = if (selected) GhBlue else MaterialTheme.colorScheme.onSurfaceVariant
    Box(
        modifier = modifier
            .clip(RoundedCornerShape(10.dp))
            .background(bg)
            .clickable(onClick = onClick)
            .padding(vertical = 10.dp, horizontal = 8.dp),
        contentAlignment = Alignment.Center
    ) {
        Text(text, style = MaterialTheme.typography.labelLarge, color = fg, fontWeight = if (selected) FontWeight.Bold else FontWeight.Normal)
    }
}

@Composable
private fun StepByStepPersianView(
    stepIndex: Int,
    stepTitle: String,
    isAutoHealing: Boolean,
    verifiedPingMs: Int?,
    logs: List<TunnelLogEntry>
) {
    val steps = listOf(
        1 to "۱. دریافت و اعتبارسنجی کانفیگ ضدسانسور (Serverless / Custom)",
        2 to "۲. راه‌اندازی هستهٔ رسمی Xray-core v26.10.21 در حافظهٔ امن",
        3 to "۳. باز کردن درگاه پروکسی محلی (SOCKS5 :10808) و DNS امن (:15353)",
        4 to "۴. ایجاد رابط تونل ایزوله (tun0) با مستثنی‌سازی هسته از لوپ شبکه",
        5 to "۵. تست واقعی عبور ترافیک (HTTP 204) و خودترمیمی با IP تمیز"
    )

    Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
        Card(
            modifier = Modifier.fillMaxWidth(),
            colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.35f)),
            shape = RoundedCornerShape(14.dp)
        ) {
            Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
                Text(
                    text = stepTitle,
                    style = MaterialTheme.typography.titleMedium,
                    color = if (verifiedPingMs != null) GhGreen else GhBlue,
                    fontWeight = FontWeight.Bold
                )
                steps.forEach { (idx, label) ->
                    val done = stepIndex > idx || (stepIndex == 5 && idx == 5 && verifiedPingMs != null)
                    val active = stepIndex == idx && !done
                    val color = when {
                        done -> LogEmerald
                        active && isAutoHealing -> LogAmber
                        active -> LogCyan
                        else -> MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.6f)
                    }
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Icon(
                            imageVector = when {
                                done -> Icons.Filled.CheckCircle
                                active && isAutoHealing -> Icons.Filled.Warning
                                active -> Icons.Filled.Refresh
                                else -> Icons.Filled.CheckCircle
                            },
                            contentDescription = null,
                            tint = color,
                            modifier = Modifier.size(20.dp)
                        )
                        Spacer(Modifier.width(10.dp))
                        Text(label, style = MaterialTheme.typography.bodyMedium, color = color)
                    }
                }
            }
        }

        Text("رویدادهای زندهٔ اتصال (به ترتیب زمان):", style = MaterialTheme.typography.labelLarge, color = MaterialTheme.colorScheme.onSurfaceVariant)

        if (logs.isEmpty()) {
            Card(
                modifier = Modifier.fillMaxWidth(),
                colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.2f))
            ) {
                Text(
                    text = "هنوز رویدادی ثبت نشده است. روی دکمهٔ «اتصال» در تب اول یا «تست پینگ واقعی» بزنید.",
                    modifier = Modifier.padding(16.dp),
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
        } else {
            logs.asReversed().take(30).forEach { entry ->
                val accent = when (entry.level) {
                    LogLevel.SUCCESS -> LogEmerald
                    LogLevel.WARN -> LogAmber
                    LogLevel.ERROR -> LogRed
                    LogLevel.INFO -> LogCyan
                }
                Card(
                    modifier = Modifier.fillMaxWidth(),
                    colors = CardDefaults.cardColors(containerColor = accent.copy(alpha = 0.08f)),
                    shape = RoundedCornerShape(10.dp)
                ) {
                    Row(
                        modifier = Modifier.padding(12.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Box(
                            modifier = Modifier
                                .size(8.dp)
                                .clip(CircleShape)
                                .background(accent)
                        )
                        Spacer(Modifier.width(10.dp))
                        Column(Modifier.weight(1f)) {
                            Text(entry.messageFa, style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurface)
                            Text(
                                text = "${entry.timeText} · ${entry.category.name}",
                                style = MaterialTheme.typography.labelSmall,
                                color = MaterialTheme.colorScheme.onSurfaceVariant
                            )
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun TechnicalTerminalView(
    logs: List<TunnelLogEntry>,
    selectedCategory: LogCategory?,
    onSelectCategory: (LogCategory?) -> Unit
) {
    Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .horizontalScroll(rememberScrollState()),
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            FilterChip(
                selected = selectedCategory == null,
                onClick = { onSelectCategory(null) },
                label = { Text("همه (${logs.size})") }
            )
            FilterChip(
                selected = selectedCategory == LogCategory.XRAY,
                onClick = { onSelectCategory(LogCategory.XRAY) },
                label = { Text("هسته Xray") }
            )
            FilterChip(
                selected = selectedCategory == LogCategory.TUN,
                onClick = { onSelectCategory(LogCategory.TUN) },
                label = { Text("تونل tun0") }
            )
            FilterChip(
                selected = selectedCategory == LogCategory.PROBE,
                onClick = { onSelectCategory(LogCategory.PROBE) },
                label = { Text("پروب و IP تمیز") }
            )
        }

        val filtered = if (selectedCategory == null) logs else logs.filter { it.category == selectedCategory }

        Box(
            modifier = Modifier
                .fillMaxWidth()
                .clip(RoundedCornerShape(12.dp))
                .background(TerminalBg)
                .border(1.dp, TerminalBorder, RoundedCornerShape(12.dp))
                .padding(12.dp)
        ) {
            if (filtered.isEmpty()) {
                Text(
                    text = "[gh-protocol@xray ~]$ waiting for tunnel events...",
                    fontFamily = FontFamily.Monospace,
                    fontSize = 12.sp,
                    color = Color(0xFF64748B)
                )
            } else {
                Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
                    filtered.takeLast(60).forEach { e ->
                        val c = when (e.level) {
                            LogLevel.SUCCESS -> LogEmerald
                            LogLevel.WARN -> LogAmber
                            LogLevel.ERROR -> LogRed
                            LogLevel.INFO -> LogCyan
                        }
                        Text(
                            text = "[${e.timeText}] [${e.category.name}] ${e.rawTech}",
                            fontFamily = FontFamily.Monospace,
                            fontSize = 11.5.sp,
                            color = c,
                            style = MaterialTheme.typography.bodySmall.copy(textDirection = TextDirection.Ltr)
                        )
                    }
                }
            }
        }
    }
}
