package com.ghprotocol.app.ui

import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.background
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
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.ghprotocol.app.R
import com.ghprotocol.app.core.TunnelLogBuffer

/**
 * Gh Protocol Main Connect Screen:
 * Built directly from UnboundTechCo/defyxVPN (main_screen.dart, connection_button.dart,
 * header_section.dart, main_screen_background.dart) + Ashutoshx7/VengenceUI
 * (glow-border-card.tsx, radial-glow-button.tsx, border-beam.tsx).
 * All legacy v1.0.0 UI (StatusCard, TopAppBar, ConnectArea, PhaseSpinner) has been removed.
 */
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
    onOpenLogs: () -> Unit = {}
) {
    val ui by viewModel.ui.collectAsState()
    val telemetry by TunnelLogBuffer.telemetry.collectAsState()
    val logs by TunnelLogBuffer.logs.collectAsState()
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
            } catch (_: Exception) {
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

    val isConnected = ui.connectPhase == ConnectPhase.CONNECTED
    val activeRemark = ui.subscription?.entries?.getOrNull(ui.activeEntryIndex)?.remarks
        ?: ui.subscription?.entries?.firstOrNull()?.remarks
        ?: "Serverless-v52"

    DefyxMainScreenBackground(
        phase = ui.connectPhase,
        isAutoHealing = ui.isAutoHealing,
        modifier = modifier.fillMaxSize()
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .verticalScroll(rememberScrollState())
                .padding(horizontal = 20.dp, vertical = 16.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            // 1. DefyxVPN Header Section (G + h Protocol brand, status headline, step/ping bar)
            DefyxHeaderSection(
                phase = ui.connectPhase,
                verifiedPingMs = ui.verifiedPingMs,
                isAutoHealing = ui.isAutoHealing,
                cleanIp = ui.cleanIp,
                activeRemark = activeRemark,
                telemetry = telemetry,
                onTapPing = { viewModel.runUrlPingTest() },
                onTapLogs = onOpenLogs
            )

            // 2. DefyxVPN Shield Connection Button (4 concentric shield pulse rings + ShieldLoadingPainter + Scan Matrix + official defyx_*.svg icons)
            DefyxShieldConnectionButton(
                phase = ui.connectPhase,
                verifiedPingMs = ui.verifiedPingMs,
                isAutoHealing = ui.isAutoHealing,
                stepIndex = telemetry.stepIndex,
                onTapConnect = { viewModel.onConnectTap() },
                onTapDisconnect = {
                    context.stopService(android.content.Intent(context, com.ghprotocol.app.core.VpnTunnelService::class.java))
                    viewModel.disconnect()
                }
            )

            // 3. VengeanceUI RadialGlowButtons for instant Radar Scan & Real Tunnel Ping Test
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(10.dp)
            ) {
                VengeanceRadialGlowButton(
                    text = "رادار IP تمیز",
                    iconRes = R.drawable.ic_defyx_vpn_cloud,
                    accentColor = DefyxColors.BrandGold,
                    onClick = onOpenScanner,
                    modifier = Modifier.weight(1f)
                )
                VengeanceRadialGlowButton(
                    text = when {
                        ui.isTestingUrl -> "در حال تست..."
                        ui.verifiedPingMs != null -> "پینگ: ${ui.verifiedPingMs} ms"
                        else -> "تست پینگ واقعی"
                    },
                    iconRes = R.drawable.ic_defyx_speed,
                    accentColor = DefyxColors.DownloadGreen,
                    onClick = { viewModel.runUrlPingTest() },
                    modifier = Modifier.weight(1f)
                )
            }

            // 4. n8n-Inspired 5-Node Live Data-Flow Pipeline inside VengeanceGlowBorderCard
            N8nPipelineFlowCard(
                telemetry = telemetry,
                isConnected = isConnected,
                onClick = onOpenLogs
            )

            // 5. DefyxVPN + VengeanceUI Live Traffic Waveform Card (#76F959 download, #72D9FF upload)
            LiveTrafficWaveformCard(telemetry = telemetry)

            // 6. Psiphon-style Live Log Strip inside VengeanceGlowBorderCard
            val latestLog = logs.lastOrNull()
            VengeanceGlowBorderCard(
                modifier = Modifier.fillMaxWidth(),
                presetColors = DefyxColors.VengeanceAurora,
                onClick = onOpenLogs
            ) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Box(
                        modifier = Modifier
                            .size(10.dp)
                            .clip(CircleShape)
                            .background(if (isConnected) DefyxColors.DownloadGreen else DefyxColors.BrandGold)
                    )
                    Spacer(Modifier.width(10.dp))
                    Column(Modifier.weight(1f)) {
                        Text(
                            text = latestLog?.messageFa ?: telemetry.stepTitleFa,
                            style = MaterialTheme.typography.bodyMedium,
                            fontWeight = FontWeight.Bold,
                            color = Color.White,
                            maxLines = 1
                        )
                        Text(
                            text = latestLog?.let { "[${it.timeText}] ${it.rawTech}" }
                                ?: "مشاهدهٔ ترمینال زندهٔ هستهٔ Xray و تونل ضد فیلتر",
                            fontSize = 11.sp,
                            fontFamily = FontFamily.Monospace,
                            color = Color.White.copy(alpha = 0.68f),
                            maxLines = 1
                        )
                    }
                    Spacer(Modifier.width(8.dp))
                    Icon(
                        painter = painterResource(R.drawable.ic_vengeance_terminal),
                        contentDescription = null,
                        tint = DefyxColors.BrandGold,
                        modifier = Modifier.size(18.dp)
                    )
                }
            }
        }
    }
}
