package com.ghprotocol.app.ui

import android.content.ClipboardManager
import android.content.Context
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.ghprotocol.app.R
import com.ghprotocol.app.ui.theme.GhBlue
import com.ghprotocol.app.ui.theme.GhGreen

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ConfigHubScreen(
    viewModel: HomeViewModel,
    onOpenQr: () -> Unit = {},
    onOpenGuide: () -> Unit = {},
    onOpenSettings: () -> Unit = {},
    onOpenAbout: () -> Unit = {},
    modifier: Modifier = Modifier
) {
    val ui by viewModel.ui.collectAsState()
    val context = LocalContext.current
    var rawConfigInput by remember { mutableStateOf("") }
    var importFeedback by remember { mutableStateOf<Pair<Boolean, String>?>(null) }

    DefyxMainScreenBackground(
        phase = ui.connectPhase,
        isAutoHealing = ui.isAutoHealing,
        modifier = modifier
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .verticalScroll(rememberScrollState())
                .padding(horizontal = 16.dp, vertical = 14.dp),
            verticalArrangement = Arrangement.spacedBy(14.dp)
        ) {
            Column {
                Text(
                    text = "مرکز کانفیگ، بقای آفلاین و راهنما",
                    style = MaterialTheme.typography.titleLarge,
                    fontWeight = FontWeight.ExtraBold,
                    color = Color.White
                )
                Text(
                    text = "پشتیبانی از اشتراک رسمی + vless:// و trojan:// با فرگمنت خودکار",
                    style = MaterialTheme.typography.labelSmall,
                    color = Color.White.copy(alpha = 0.72f)
                )
            }

            // 1. Custom Config Importer (F-16: vless://, trojan://, JSON) inside VengeanceGlowBorderCard
            VengeanceGlowBorderCard(
                modifier = Modifier.fillMaxWidth(),
                presetColors = DefyxColors.VengeanceAurora
            ) {
                Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                    Text(
                        text = "وارد کردن کانفیگ سفارشی (F-16 — الگوی سیمرغ)",
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.Bold,
                        color = DefyxColors.BrandGold
                    )
                    Text(
                        text = "لینک vless:// یا trojan:// یا JSON کامل Xray را وارد کنید؛ فرگمنت TLS و IP تمیز به‌طور خودکار تزریق می‌شوند:",
                        style = MaterialTheme.typography.bodySmall,
                        color = Color.White.copy(alpha = 0.78f)
                    )
                    OutlinedTextField(
                        value = rawConfigInput,
                        onValueChange = { rawConfigInput = it; importFeedback = null },
                        placeholder = { Text("vless://uuid@domain:443?type=ws&security=tls#MyRoute") },
                        modifier = Modifier.fillMaxWidth(),
                        maxLines = 4
                    )
                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        VengeanceRadialGlowButton(
                            text = "جای‌گذاری کلیپ‌بورد",
                            iconRes = R.drawable.ic_defyx_copy,
                            accentColor = DefyxColors.UploadCyan,
                            onClick = {
                                val cm = context.getSystemService(Context.CLIPBOARD_SERVICE) as? ClipboardManager
                                val pasted = cm?.primaryClip?.getItemAt(0)?.coerceToText(context)?.toString().orEmpty()
                                if (pasted.isNotBlank()) {
                                    rawConfigInput = pasted
                                    val ok = viewModel.importCustomConfig(pasted, ui.cleanIp)
                                    importFeedback = if (ok) {
                                        true to "کانفیگ از کلیپ‌بورد با موفقیت وارد و فعال شد ✓"
                                    } else {
                                        false to "فرمت کلیپ‌بورد معتبر نیست (vless/trojan/JSON)"
                                    }
                                }
                            },
                            modifier = Modifier.weight(1f)
                        )
                        VengeanceRadialGlowButton(
                            text = "ثبت و فعال‌سازی",
                            iconRes = R.drawable.ic_vengeance_sparkles,
                            accentColor = DefyxColors.BrandGold,
                            onClick = {
                                val ok = viewModel.importCustomConfig(rawConfigInput, ui.cleanIp)
                                importFeedback = if (ok) {
                                    true to "کانفیگ سفارشی با موفقیت وارد و فرگمنت تزریق شد ✓"
                                } else {
                                    false to "فرمت واردشده معتبر نیست"
                                }
                            },
                            modifier = Modifier.weight(1f)
                        )
                    }
                    importFeedback?.let { (ok, msg) ->
                        Text(
                            text = msg,
                            style = MaterialTheme.typography.labelMedium,
                            color = if (ok) DefyxColors.DownloadGreen else DefyxColors.ErrorRose,
                            fontWeight = FontWeight.Bold
                        )
                    }
                }
            }

            // 2. Official Subscription & Pre-Blackout Prep (F-1 / F-6 / F-13)
            Card(
                modifier = Modifier.fillMaxWidth(),
                colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.35f)),
                shape = RoundedCornerShape(16.dp)
            ) {
                Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
                    Text(
                        text = "اشتراک رسمی Serverless-for-Iran و آمادگی قطعی (F-6 / F-13)",
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.Bold
                    )
                    Text(
                        text = "آخرین بروزرسانی: ${viewModel.repository.lastUpdateText() ?: "کش داخلی"} · تعداد مسیرها: ${ui.subscription?.entries?.size ?: 0}",
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        Button(
                            onClick = { viewModel.refreshConfig() },
                            enabled = !ui.isUpdating,
                            colors = ButtonDefaults.buttonColors(containerColor = GhGreen),
                            modifier = Modifier.weight(1f)
                        ) {
                            Text(if (ui.isUpdating) "در حال دریافت..." else "بروزرسانی اشتراک رسمی")
                        }
                        OutlinedButton(
                            onClick = { viewModel.runBlackoutPrep() },
                            modifier = Modifier.weight(1f)
                        ) {
                            Text(if (ui.prepReady) "آمادهٔ آفلاین ✓" else "آماده‌سازی قطعی (F-13)")
                        }
                    }
                }
            }

            // 3. Quick Navigation Grid to QR, Guide, Settings, About
            Card(
                modifier = Modifier.fillMaxWidth(),
                colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.25f)),
                shape = RoundedCornerShape(16.dp)
            ) {
                Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
                    Text("ابزارهای جانبی و راهنما", style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.Bold)
                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth()) {
                        OutlinedButton(onClick = onOpenQr, modifier = Modifier.weight(1f)) {
                            Text(stringResource(R.string.qr_share))
                        }
                        OutlinedButton(onClick = onOpenGuide, modifier = Modifier.weight(1f)) {
                            Text(stringResource(R.string.guide))
                        }
                    }
                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth()) {
                        OutlinedButton(onClick = onOpenSettings, modifier = Modifier.weight(1f)) {
                            Text(stringResource(R.string.settings))
                        }
                        OutlinedButton(onClick = onOpenAbout, modifier = Modifier.weight(1f)) {
                            Text("درباره و امنیت")
                        }
                    }
                }
            }
        }
    }
}
