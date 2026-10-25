package com.ghprotocol.app.ui

import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.RadioButton
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Switch
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.ghprotocol.app.ui.theme.GhBlue
import com.ghprotocol.app.ui.theme.GhGreen
import com.ghprotocol.app.ui.theme.MotionSpec

private val RadarEmerald = Color(0xFF34D399)
private val RadarCyan = Color(0xFF22D3EE)
private val RadarAmber = Color(0xFFF5A524)

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun RadarScreen(
    viewModel: HomeViewModel,
    modifier: Modifier = Modifier
) {
    val ui by viewModel.ui.collectAsState()
    val context = LocalContext.current

    Scaffold(
        topBar = {
            TopAppBar(
                title = {
                    Column {
                        Text("رادار IP تمیز و بالانسر مسیرها", style = MaterialTheme.typography.titleMedium)
                        Text(
                            text = "اسکن هندشیک واقعی TLS 1.2 کلودفلر + انتخاب هوشمند مسیر",
                            style = MaterialTheme.typography.labelSmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                }
            )
        },
        modifier = modifier
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .verticalScroll(rememberScrollState())
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(14.dp)
        ) {
            // Section 1: Clean IP Scanner (F-17)
            Card(
                modifier = Modifier.fillMaxWidth(),
                colors = CardDefaults.cardColors(containerColor = GhBlue.copy(alpha = 0.10f)),
                shape = RoundedCornerShape(16.dp)
            ) {
                Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Column(Modifier.weight(1f)) {
                            Text("رادار IP تمیز کلودفلر (F-17)", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, color = GhBlue)
                            Text(
                                text = "IP فعال فعلی: ${ui.cleanIp ?: "خودکار (پیش‌فرض کانفیگ)"}",
                                style = MaterialTheme.typography.bodyMedium,
                                color = MaterialTheme.colorScheme.onSurface
                            )
                        }
                    }

                    if (ui.isScanningIps) {
                        LinearProgressIndicator(modifier = Modifier.fillMaxWidth(), color = GhBlue)
                        Text("در حال ارسال ClientHello استاندارد TLS 1.2 به لبه‌های کلودفلر...", style = MaterialTheme.typography.labelSmall, color = GhBlue)
                    }

                    Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                        Button(
                            onClick = { viewModel.runCleanIpScan() },
                            enabled = !ui.isScanningIps,
                            colors = ButtonDefaults.buttonColors(containerColor = GhBlue),
                            modifier = Modifier.weight(1f)
                        ) {
                            Text(if (ui.isScanningIps) "در حال اسکن رادار..." else "شروع اسکن IP تمیز")
                        }
                        if (ui.cleanIp != null) {
                            OutlinedButton(onClick = { viewModel.applyCleanIp(null) }) {
                                Text("حالت خودکار")
                            }
                        }
                    }

                    if (ui.scanResults.isNotEmpty()) {
                        Spacer(Modifier.height(4.dp))
                        Text("نتایج اسکن روی اپراتور فعلی شما:", style = MaterialTheme.typography.labelLarge)
                        ui.scanResults.take(8).forEach { item ->
                            val isSelected = ui.cleanIp == item.ip
                            val color = when {
                                item.latencyMs < 180L -> RadarEmerald
                                item.latencyMs < 350L -> RadarCyan
                                else -> RadarAmber
                            }
                            val fillFraction by animateFloatAsState(
                                targetValue = (1f - (item.latencyMs.coerceAtMost(1000L).toFloat() / 1100f)).coerceIn(0.15f, 1f),
                                animationSpec = MotionSpec.tweenMs(context, 250),
                                label = "ip-bar"
                            )
                            Card(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .clickable { viewModel.applyCleanIp(item.ip) },
                                colors = CardDefaults.cardColors(
                                    containerColor = if (isSelected) RadarEmerald.copy(alpha = 0.16f)
                                    else MaterialTheme.colorScheme.surface.copy(alpha = 0.7f)
                                ),
                                shape = RoundedCornerShape(10.dp)
                            ) {
                                Column(Modifier.padding(10.dp)) {
                                    Row(
                                        modifier = Modifier.fillMaxWidth(),
                                        horizontalArrangement = Arrangement.SpaceBetween,
                                        verticalAlignment = Alignment.CenterVertically
                                    ) {
                                        Text(
                                            text = item.ip + if (isSelected) "  ✓ (فعال)" else "",
                                            fontFamily = FontFamily.Monospace,
                                            fontWeight = FontWeight.Bold,
                                            color = if (isSelected) RadarEmerald else MaterialTheme.colorScheme.onSurface
                                        )
                                        Text(
                                            text = "${item.latencyMs} ms",
                                            style = MaterialTheme.typography.labelMedium,
                                            color = color,
                                            fontWeight = FontWeight.Bold
                                        )
                                    }
                                    Spacer(Modifier.height(6.dp))
                                    Box(
                                        modifier = Modifier
                                            .fillMaxWidth()
                                            .height(5.dp)
                                            .clip(RoundedCornerShape(3.dp))
                                            .background(MaterialTheme.colorScheme.surfaceVariant)
                                    ) {
                                        Box(
                                            modifier = Modifier
                                                .fillMaxWidth(fillFraction)
                                                .height(5.dp)
                                                .clip(RoundedCornerShape(3.dp))
                                                .background(color)
                                        )
                                    }
                                }
                            }
                        }
                    }
                }
            }

            // Section 2: Smart Route Balancer (F-18)
            Card(
                modifier = Modifier.fillMaxWidth(),
                colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.35f)),
                shape = RoundedCornerShape(16.dp)
            ) {
                Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
                    Text("بالانسر و انتخاب مسیر اتصال (F-18)", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, color = GhGreen)
                    Text(
                        text = "مسیر فعال برای هستهٔ Xray را انتخاب کنید (در صورت اختلال در مسیر اول، مسیر دوم فرگمنت عمیق‌تر دارد):",
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                    val entries = ui.subscription?.entries.orEmpty()
                    if (entries.isEmpty()) {
                        Text("در حال بارگذاری مسیرها...", style = MaterialTheme.typography.bodyMedium)
                    } else {
                        entries.forEachIndexed { idx, entry ->
                            val selected = ui.activeEntryIndex == idx
                            Row(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .clip(RoundedCornerShape(10.dp))
                                    .background(if (selected) GhGreen.copy(alpha = 0.14f) else Color.Transparent)
                                    .clickable { viewModel.selectActiveRoute(idx) }
                                    .padding(10.dp),
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                RadioButton(selected = selected, onClick = { viewModel.selectActiveRoute(idx) })
                                Spacer(Modifier.width(8.dp))
                                Column(Modifier.weight(1f)) {
                                    Text(entry.remarks, style = MaterialTheme.typography.bodyLarge, fontWeight = FontWeight.Bold)
                                    Text(
                                        text = "هسته ≥ ${entry.minCoreVersion} · پورت ${entry.inboundPort}",
                                        style = MaterialTheme.typography.labelSmall,
                                        color = MaterialTheme.colorScheme.onSurfaceVariant
                                    )
                                }
                            }
                        }
                    }
                }
            }

            // Section 3: Protocol Adaptation (F-15 TCP-First)
            Card(
                modifier = Modifier.fillMaxWidth(),
                colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.35f)),
                shape = RoundedCornerShape(16.dp)
            ) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(16.dp),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Column(Modifier.weight(1f)) {
                        Text("اولویت TCP Fragmentation (ضد محدودیت UDP — F-15)", style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.Bold)
                        Spacer(Modifier.height(4.dp))
                        Text(
                            text = "در زمان مسدودسازی یا اختلال شدید UDP در اپراتورها، قواعد TCP-Fragment را در صدر جدول روتینگ قرار می‌دهد.",
                            style = MaterialTheme.typography.bodySmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                    Spacer(Modifier.width(12.dp))
                    Switch(
                        checked = ui.tcpFirstEnabled,
                        onCheckedChange = { viewModel.toggleTcpFirst(it) }
                    )
                }
            }
        }
    }
}
