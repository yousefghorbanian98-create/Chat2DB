package com.ghprotocol.app.ui

import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.spring
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
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
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material.icons.filled.Warning
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.scale
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.ghprotocol.app.R
import com.ghprotocol.app.core.TunnelLogBuffer
import com.ghprotocol.app.domain.NetworkState
import com.ghprotocol.app.ui.theme.GhBlue
import com.ghprotocol.app.ui.theme.GhGreen
import com.ghprotocol.app.ui.theme.MotionSpec

private val Amber = Color(0xFFF5A524)
private val Red = Color(0xFFE5484D)

@OptIn(ExperimentalMaterial3Api::class, ExperimentalLayoutApi::class)
@Composable
fun HomeScreen(
    modifier: Modifier = Modifier,
    viewModel: HomeViewModel = viewModel(),
    onOpenConfig: () -> Unit = {},
    onOpenGuide: () -> Unit = {},
    onOpenQr: () -> Unit = {},
    onOpenScanner: () -> Unit = {},
    onOpenBalancer: () -> Unit = {},
    onOpenPrep: () -> Unit = {},
    onOpenSettings: () -> Unit = {},
    onOpenLogs: () -> Unit = {},
    showEnhancedDashboard: Boolean = false
) {
    val ui by viewModel.ui.collectAsState()
    val context = LocalContext.current
    val vpnLauncher = rememberLauncherForActivityResult(
        ActivityResultContracts.StartActivityForResult()
    ) { result ->
        if (result.resultCode == android.app.Activity.RESULT_OK) {
            context.startService(android.content.Intent(context, com.ghprotocol.app.core.VpnTunnelService::class.java))
            viewModel.onVpnEstablished()
        } else {
            viewModel.onVpnFailed("vpn_denied")
        }
    }
    LaunchedEffect(ui.vpnPending) {
        if (ui.vpnPending) {
            val prep = try {
                android.net.VpnService.prepare(context)
            } catch (e: Exception) {
                null
            }
            if (prep == null) {
                context.startService(android.content.Intent(context, com.ghprotocol.app.core.VpnTunnelService::class.java))
                viewModel.onVpnEstablished()
            } else {
                vpnLauncher.launch(prep)
            }
        }
    }
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(stringResource(R.string.app_name)) },
                actions = {
                    IconButton(onClick = onOpenSettings) {
                        Icon(Icons.Filled.Settings, contentDescription = stringResource(R.string.settings))
                    }
                }
            )
        }
    ) { padding ->
        if (!showEnhancedDashboard) {
            Column(
                modifier = modifier
                    .fillMaxSize()
                    .padding(padding)
                    .verticalScroll(rememberScrollState())
                    .padding(24.dp),
                verticalArrangement = Arrangement.Center,
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                StatusCard(state = ui.network)

                Spacer(Modifier.height(20.dp))

                ConnectArea(
                    phase = ui.connectPhase,
                    isUpdating = ui.isUpdating,
                    hasConfig = ui.subscription != null,
                    onTap = { viewModel.onConnectTap() },
                    onDisconnect = {
                        context.stopService(android.content.Intent(context, com.ghprotocol.app.core.VpnTunnelService::class.java))
                        viewModel.disconnect()
                    }
                )

                if (ui.configError != null) {
                    Spacer(Modifier.height(12.dp))
                    Text(
                        text = stringResource(R.string.config_update_failed),
                        color = Amber,
                        style = MaterialTheme.typography.bodyMedium
                    )
                    OutlinedButton(onClick = { viewModel.refreshConfig() }) {
                        Text(stringResource(R.string.retry))
                    }
                }

                ui.subscription?.let { sub ->
                    Spacer(Modifier.height(16.dp))
                    Text(
                        text = stringResource(R.string.config_line, sub.entries.joinToString(" · ") { it.remarks }),
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }

                Spacer(Modifier.height(24.dp))
                FlowRow(
                    horizontalArrangement = Arrangement.spacedBy(12.dp),
                    verticalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    OutlinedButton(onClick = onOpenConfig) { Text(stringResource(R.string.config_source)) }
                    OutlinedButton(onClick = onOpenGuide) { Text(stringResource(R.string.guide)) }
                    OutlinedButton(onClick = onOpenQr) { Text(stringResource(R.string.qr_share)) }
                    OutlinedButton(onClick = onOpenScanner) { Text(stringResource(R.string.clean_ip_short)) }
                    OutlinedButton(onClick = onOpenBalancer) { Text(stringResource(R.string.routes_short)) }
                    OutlinedButton(onClick = onOpenPrep) { Text(stringResource(R.string.blackout_prep_short)) }
                }
            }
        } else {
            WorldClassConnectHub(
                ui = ui,
                viewModel = viewModel,
                onDisconnect = {
                    context.stopService(android.content.Intent(context, com.ghprotocol.app.core.VpnTunnelService::class.java))
                    viewModel.disconnect()
                },
                onOpenRadar = onOpenScanner,
                onOpenLogs = onOpenLogs,
                onOpenConfig = onOpenConfig,
                modifier = modifier
                    .fillMaxSize()
                    .padding(padding)
            )
        }
    }
}

@Composable
private fun WorldClassConnectHub(
    ui: HomeUiState,
    viewModel: HomeViewModel,
    onDisconnect: () -> Unit,
    onOpenRadar: () -> Unit,
    onOpenLogs: () -> Unit,
    onOpenConfig: () -> Unit,
    modifier: Modifier = Modifier
) {
    val telemetry by TunnelLogBuffer.telemetry.collectAsState()
    val logs by TunnelLogBuffer.logs.collectAsState()
    val context = LocalContext.current

    val isConnected = ui.connectPhase == ConnectPhase.CONNECTED
    val isBusy = ui.connectPhase == ConnectPhase.CHECKING ||
        ui.connectPhase == ConnectPhase.PREPARING ||
        ui.connectPhase == ConnectPhase.TUNNELING ||
        ui.isAutoHealing

    val ringColor by animateColorAsState(
        targetValue = when {
            isConnected && ui.verifiedPingMs != null -> GhGreen
            isConnected -> GhBlue
            isBusy -> Amber
            ui.connectPhase == ConnectPhase.FAILED -> Red
            else -> GhBlue.copy(alpha = 0.65f)
        },
        animationSpec = MotionSpec.tweenMs(context, 250),
        label = "hero-ring-color"
    )

    val heroScale by animateFloatAsState(
        targetValue = if (isConnected) 1.03f else 1.0f,
        animationSpec = spring(dampingRatio = 0.78f, stiffness = 380f),
        label = "hero-scale"
    )

    Column(
        modifier = modifier
            .verticalScroll(rememberScrollState())
            .padding(horizontal = 20.dp, vertical = 12.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(14.dp)
    ) {
        // 1. Honest Network Status Card
        StatusCard(state = ui.network)

        // 2. Hero Circular Connect Button with 5-Step Progress Ring (Defyx / Outline / 21st.dev style)
        Box(
            modifier = Modifier
                .padding(vertical = 8.dp)
                .size(184.dp)
                .scale(heroScale),
            contentAlignment = Alignment.Center
        ) {
            val stepProgress = when (ui.connectPhase) {
                ConnectPhase.IDLE -> 0.15f
                ConnectPhase.CHECKING -> 0.30f
                ConnectPhase.PREPARING -> 0.55f
                ConnectPhase.TUNNELING -> 0.80f
                ConnectPhase.CONNECTED -> 1.0f
                ConnectPhase.FAILED -> 1.0f
            }
            CircularProgressIndicator(
                progress = { stepProgress },
                modifier = Modifier.size(180.dp),
                color = ringColor,
                strokeWidth = 6.dp,
                trackColor = ringColor.copy(alpha = 0.14f)
            )
            Box(
                modifier = Modifier
                    .size(152.dp)
                    .clip(CircleShape)
                    .background(ringColor.copy(alpha = 0.14f))
                    .border(2.dp, ringColor.copy(alpha = 0.55f), CircleShape)
                    .clickable {
                        if (isConnected) onDisconnect() else viewModel.onConnectTap()
                    }
                    .padding(16.dp),
                contentAlignment = Alignment.Center
            ) {
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    Text(
                        text = when {
                            isConnected -> "قطع اتصال"
                            isBusy -> "در حال اتصال..."
                            ui.connectPhase == ConnectPhase.FAILED -> "تلاش مجدد"
                            else -> "اتصال"
                        },
                        style = MaterialTheme.typography.titleLarge,
                        fontWeight = FontWeight.ExtraBold,
                        color = ringColor,
                        textAlign = TextAlign.Center
                    )
                    Spacer(Modifier.height(4.dp))
                    Text(
                        text = when {
                            isConnected && ui.verifiedPingMs != null -> "${ui.verifiedPingMs} ms · تاییدشده"
                            isConnected && ui.isAutoHealing -> "Auto-Heal..."
                            isConnected -> "تونل فعال"
                            isBusy -> "گام ${telemetry.stepIndex} از ۵"
                            else -> "یک تپ · بدون سرور"
                        },
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        textAlign = TextAlign.Center
                    )
                }
            }
        }

        // 3. Psiphon-style Mini Live-Log Strip (tappable -> jumps to Live Log tab)
        val latestLog = logs.lastOrNull()
        Card(
            modifier = Modifier
                .fillMaxWidth()
                .clickable(onClick = onOpenLogs),
            colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.35f)),
            shape = RoundedCornerShape(14.dp)
        ) {
            Row(
                modifier = Modifier.padding(horizontal = 14.dp, vertical = 12.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Box(
                    modifier = Modifier
                        .size(10.dp)
                        .clip(CircleShape)
                        .background(ringColor)
                )
                Spacer(Modifier.width(10.dp))
                Column(Modifier.weight(1f)) {
                    Text(
                        text = telemetry.stepTitleFa,
                        style = MaterialTheme.typography.bodyMedium,
                        fontWeight = FontWeight.Bold,
                        color = MaterialTheme.colorScheme.onSurface
                    )
                    Text(
                        text = latestLog?.let { "[${it.timeText}] ${it.rawTech}" }
                            ?: "برای مشاهدهٔ لاگ زندهٔ اتصال (به سبک سایفون) اینجا بزنید",
                        style = MaterialTheme.typography.labelSmall,
                        fontFamily = FontFamily.Monospace,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        maxLines = 1
                    )
                }
                Spacer(Modifier.width(8.dp))
                Text("لاگ زنده ←", style = MaterialTheme.typography.labelMedium, color = GhBlue, fontWeight = FontWeight.Bold)
            }
        }

        // 4. Bento Grid: Active Route/Clean IP + Live Traffic & URL Ping Test
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(10.dp)
        ) {
            Card(
                modifier = Modifier
                    .weight(1f)
                    .clickable(onClick = onOpenRadar),
                colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.28f)),
                shape = RoundedCornerShape(14.dp)
            ) {
                Column(Modifier.padding(14.dp)) {
                    Text("مسیر و IP تمیز", style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    Spacer(Modifier.height(4.dp))
                    val activeRemark = ui.subscription?.entries?.getOrNull(ui.activeEntryIndex)?.remarks
                        ?: ui.subscription?.entries?.firstOrNull()?.remarks
                        ?: "Serverless-v52"
                    Text(activeRemark, style = MaterialTheme.typography.bodyMedium, fontWeight = FontWeight.Bold, maxLines = 1)
                    Text(
                        text = "IP: ${ui.cleanIp ?: "خودکار (Auto)"}",
                        style = MaterialTheme.typography.labelSmall,
                        color = GhBlue
                    )
                }
            }

            Card(
                modifier = Modifier
                    .weight(1f)
                    .clickable { viewModel.runUrlPingTest() },
                colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.28f)),
                shape = RoundedCornerShape(14.dp)
            ) {
                Column(Modifier.padding(14.dp)) {
                    Text("تست پینگ و ترافیک", style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    Spacer(Modifier.height(4.dp))
                    Text(
                        text = when {
                            ui.isTestingUrl -> "در حال تست..."
                            ui.verifiedPingMs != null -> "${ui.verifiedPingMs} ms ✓"
                            else -> "تست پینگ (تپ کنید)"
                        },
                        style = MaterialTheme.typography.bodyMedium,
                        fontWeight = FontWeight.Bold,
                        color = if (ui.verifiedPingMs != null) GhGreen else GhBlue
                    )
                    Text(
                        text = "↓ ${TunnelLogBuffer.formatBytes(telemetry.bytesDown)} · ↑ ${TunnelLogBuffer.formatBytes(telemetry.bytesUp)}",
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
            }
        }
    }
}

@Composable
private fun StatusCard(state: NetworkState, modifier: Modifier = Modifier) {
    val spec = when (state) {
        NetworkState.CONNECTED -> StatusSpec(Icons.Filled.CheckCircle, GhBlue, R.string.st_connected, R.string.st_connected_body)
        NetworkState.DEGRADED -> StatusSpec(Icons.Filled.Warning, Amber, R.string.st_degraded, R.string.st_degraded_body)
        NetworkState.CUTOFF -> StatusSpec(Icons.Filled.Close, Red, R.string.st_cutoff, R.string.st_cutoff_body)
        NetworkState.OFFLINE -> StatusSpec(Icons.Filled.Close, Red, R.string.st_offline, R.string.st_offline_body)
        NetworkState.UNKNOWN -> StatusSpec(Icons.Filled.Refresh, Color(0xFF9AA7C0), R.string.st_unknown, R.string.st_unknown_body)
    }
    Card(
        modifier = modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(containerColor = spec.color.copy(alpha = 0.12f))
    ) {
        Row(
            modifier = Modifier.padding(20.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Icon(spec.icon, contentDescription = null, tint = spec.color, modifier = Modifier.size(32.dp))
            Spacer(Modifier.size(16.dp))
            Column(Modifier.weight(1f)) {
                Text(stringResource(spec.titleRes), style = MaterialTheme.typography.titleMedium, color = spec.color)
                Text(stringResource(spec.bodyRes), style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurface)
            }
        }
    }
}

private data class StatusSpec(
    val icon: androidx.compose.ui.graphics.vector.ImageVector,
    val color: Color,
    val titleRes: Int,
    val bodyRes: Int
)

@Composable
private fun PhaseSpinner(text: String) {
    Column(horizontalAlignment = Alignment.CenterHorizontally) {
        CircularProgressIndicator()
        Spacer(Modifier.height(12.dp))
        Text(text, style = MaterialTheme.typography.bodyMedium)
    }
}

@Composable
private fun ConnectArea(
    phase: ConnectPhase,
    isUpdating: Boolean,
    hasConfig: Boolean,
    onTap: () -> Unit,
    onDisconnect: () -> Unit
) {
    when (phase) {
        ConnectPhase.CHECKING -> PhaseSpinner(stringResource(R.string.connect_checking))
        ConnectPhase.PREPARING -> PhaseSpinner(stringResource(R.string.connect_preparing))
        ConnectPhase.TUNNELING -> PhaseSpinner(stringResource(R.string.connect_tunneling))
        ConnectPhase.CONNECTED -> Column(horizontalAlignment = Alignment.CenterHorizontally) {
            Button(onClick = onDisconnect, modifier = Modifier.fillMaxWidth()) {
                Text(stringResource(R.string.disconnect), style = MaterialTheme.typography.titleMedium)
            }
            Spacer(Modifier.height(8.dp))
            Text(
                stringResource(R.string.connect_connected),
                style = MaterialTheme.typography.labelSmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                textAlign = TextAlign.Center
            )
        }
        ConnectPhase.FAILED -> Column(horizontalAlignment = Alignment.CenterHorizontally) {
            Text(
                stringResource(R.string.connect_failed),
                color = Red,
                style = MaterialTheme.typography.bodyMedium
            )
            Spacer(Modifier.height(12.dp))
            Button(onClick = onTap, modifier = Modifier.fillMaxWidth()) {
                Text(stringResource(R.string.retry), style = MaterialTheme.typography.titleMedium)
            }
        }
        ConnectPhase.IDLE -> Button(
            onClick = onTap,
            enabled = !isUpdating,
            modifier = Modifier.fillMaxWidth()
        ) {
            Text(stringResource(R.string.connect), style = MaterialTheme.typography.titleMedium)
        }
    }
}
