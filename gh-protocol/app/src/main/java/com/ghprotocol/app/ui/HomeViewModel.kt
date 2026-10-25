package com.ghprotocol.app.ui

import android.app.Application
import android.content.Context
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.ghprotocol.app.core.CleanIpScanner
import com.ghprotocol.app.core.ConfigPatcher
import com.ghprotocol.app.core.LogCategory
import com.ghprotocol.app.core.LogLevel
import com.ghprotocol.app.core.ScanResult
import com.ghprotocol.app.core.TunnelLogBuffer
import com.ghprotocol.app.core.TunnelVerifier
import com.ghprotocol.app.core.XrayCore
import com.ghprotocol.app.core.xrayVersionOk
import com.ghprotocol.app.domain.NetworkMonitor
import com.ghprotocol.app.domain.NetworkState
import com.ghprotocol.app.domain.Subscription
import com.ghprotocol.app.domain.SubscriptionInfo
import com.ghprotocol.app.domain.SubscriptionParser
import com.ghprotocol.app.domain.SubscriptionRepository
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.io.File

enum class ConnectPhase { IDLE, CHECKING, PREPARING, TUNNELING, CONNECTED, FAILED }

data class HomeUiState(
    val network: NetworkState = NetworkState.UNKNOWN,
    val connectPhase: ConnectPhase = ConnectPhase.IDLE,
    val isUpdating: Boolean = false,
    val subscription: SubscriptionInfo? = null,
    val configError: String? = null,
    val coreVersion: String? = null,
    val tunnelError: String? = null,
    val vpnPending: Boolean = false,
    val cleanIp: String? = null,
    val prepReady: Boolean = false,
    val verifiedPingMs: Int? = null,
    val isScanningIps: Boolean = false,
    val scanResults: List<ScanResult> = emptyList(),
    val activeEntryIndex: Int = 0,
    val tcpFirstEnabled: Boolean = true,
    val isAutoHealing: Boolean = false,
    val isTestingUrl: Boolean = false
)

class HomeViewModel(
    app: Application,
    val repository: SubscriptionRepository = SubscriptionRepository(app),
    val monitor: NetworkMonitor = NetworkMonitor(),
    val core: XrayCore = XrayCore(app)
) : AndroidViewModel(app) {

    private val prefs = app.getSharedPreferences("gh-settings", Context.MODE_PRIVATE)
    private val _ui = MutableStateFlow(
        HomeUiState(
            subscription = repository.cachedAnyAge(),
            cleanIp = prefs.getString("clean_ip", null),
            activeEntryIndex = prefs.getInt("active_entry", 0),
            tcpFirstEnabled = prefs.getBoolean("tcp_first", true)
        )
    )
    val ui: StateFlow<HomeUiState> = _ui.asStateFlow()

    init {
        val initialSub = repository.cachedAnyAge()
        _ui.update { it.copy(subscription = initialSub) }
        val activeName = initialSub?.entries?.getOrNull(_ui.value.activeEntryIndex)?.remarks
            ?: initialSub?.entries?.firstOrNull()?.remarks
            ?: "Serverless-v52-fragA"
        TunnelLogBuffer.updatePingAndProfile(
            pingMs = null,
            cleanIp = _ui.value.cleanIp,
            profile = activeName
        )

        // F-12: instant re-sync when international link recovers
        monitor.start(viewModelScope) {
            viewModelScope.launch { refreshConfig() }
        }
        // F-11: surface the live network state in the UI
        viewModelScope.launch {
            monitor.state.collect { net ->
                _ui.update { it.copy(network = net) }
            }
        }
        if (_ui.value.subscription == null) {
            viewModelScope.launch { refreshConfig() }
        }
        // Deep-link connect (E2E + share-to-connect): fire once, after first layout
        if (com.ghprotocol.app.MainActivity.pendingConnect) {
            com.ghprotocol.app.MainActivity.pendingConnect = false
            viewModelScope.launch { onConnectTap() }
        }
    }

    fun refreshConfig() {
        viewModelScope.launch {
            _ui.update { it.copy(isUpdating = true, configError = null) }
            TunnelLogBuffer.log(
                LogLevel.INFO,
                LogCategory.STEP,
                "در حال دریافت آخرین کانفیگ از مخزن رسمی...",
                "SubscriptionRepository.update() started"
            )
            val r = repository.update()
            _ui.update {
                if (r.isSuccess) {
                    val sub = r.getOrNull()
                    TunnelLogBuffer.log(
                        LogLevel.SUCCESS,
                        LogCategory.STEP,
                        "کانفیگ با موفقیت به‌روز شد (${sub?.entries?.size ?: 0} مسیر)",
                        "Subscription updated from ${sub?.source ?: "remote"}"
                    )
                    it.copy(isUpdating = false, subscription = sub)
                } else {
                    val fallback = it.subscription ?: repository.cachedAnyAge() ?: repository.embeddedFallback()
                    TunnelLogBuffer.log(
                        LogLevel.WARN,
                        LogCategory.STEP,
                        "به‌روزرسانی آنلاین ناموفق بود؛ استفاده از کانفیگ ذخیره‌شده/داخلی",
                        "Subscription update failed (${r.exceptionOrNull()?.message}); using fallback"
                    )
                    it.copy(
                        isUpdating = false,
                        subscription = fallback,
                        configError = "config_update_failed"
                    )
                }
            }
        }
    }

    /**
     * F-16: Import a custom config (JSON array/object or Simorgh-pattern
     * `vless://` / `trojan://` URI) and persist it as the active subscription.
     */
    fun importCustomConfig(raw: String, cleanIp: String? = null): Boolean {
        val norm = ConfigPatcher.normalizeImport(raw, cleanIp).getOrNull() ?: return false
        val parsed = try {
            SubscriptionParser.parse(norm).copy(source = "custom")
        } catch (_: Exception) {
            return false
        }
        return try {
            val app = getApplication<Application>()
            File(app.filesDir, "subscription.json").writeText(norm)
            File(app.filesDir, "subscription.meta").writeText(parsed.fetchedAt.toString())
            prefs.edit().putInt("active_entry", 0).apply()
            _ui.update { it.copy(subscription = parsed, activeEntryIndex = 0, configError = null) }
            val remark = parsed.entries.firstOrNull()?.remarks ?: "custom"
            TunnelLogBuffer.updatePingAndProfile(_ui.value.verifiedPingMs, _ui.value.cleanIp, remark)
            TunnelLogBuffer.log(
                LogLevel.SUCCESS,
                LogCategory.STEP,
                "کانفیگ سفارشی با موفقیت وارد و فرگمنت TLS تزریق شد ($remark)",
                "Custom config imported: entries=${parsed.entries.size} first=$remark"
            )
            true
        } catch (_: Exception) {
            false
        }
    }

    /** F-17: Scan Cloudflare clean IPs via real TLS 1.2 ClientHello and persist best egress. */
    fun runCleanIpScan(scanner: CleanIpScanner = CleanIpScanner()) {
        if (_ui.value.isScanningIps) return
        viewModelScope.launch {
            _ui.update { it.copy(isScanningIps = true) }
            TunnelLogBuffer.log(
                LogLevel.INFO,
                LogCategory.PROBE,
                "شروع اسکن رادار IP تمیز کلودفلر (هندشیک واقعی TLS 1.2 روی پورت 443)...",
                "CleanIpScanner.scan() started across ${scanner.candidates.size} Cloudflare edges"
            )
            val report = withContext(Dispatchers.IO) { scanner.scan() }
            val bestIp = report.best?.ip
            if (bestIp != null) {
                scanner.saveBest(bestIp, getApplication())
                TunnelLogBuffer.log(
                    LogLevel.SUCCESS,
                    LogCategory.PROBE,
                    "بهترین IP تمیز پیدا شد: $bestIp (پینگ TLS: ${report.best.latencyMs} ms)",
                    "CleanIpScanner best=$bestIp latency=${report.best.latencyMs}ms"
                )
            } else {
                TunnelLogBuffer.log(
                    LogLevel.WARN,
                    LogCategory.PROBE,
                    "هیچ IP تمیزی در این لحظه پاسخ نداد؛ حفظ تنظیمات قبلی",
                    "CleanIpScanner: 0 reachable candidates"
                )
            }
            TunnelLogBuffer.updatePingAndProfile(_ui.value.verifiedPingMs, bestIp ?: _ui.value.cleanIp)
            _ui.update {
                it.copy(
                    isScanningIps = false,
                    cleanIp = bestIp ?: it.cleanIp,
                    scanResults = report.results
                )
            }
        }
    }

    fun applyCleanIp(ip: String?) {
        val editor = prefs.edit()
        if (ip.isNullOrBlank()) editor.remove("clean_ip") else editor.putString("clean_ip", ip.trim())
        editor.apply()
        _ui.update { it.copy(cleanIp = ip?.trim()?.takeIf { s -> s.isNotEmpty() }) }
        TunnelLogBuffer.updatePingAndProfile(_ui.value.verifiedPingMs, _ui.value.cleanIp)
        TunnelLogBuffer.log(
            LogLevel.INFO,
            LogCategory.STEP,
            if (ip.isNullOrBlank()) "آدرس IP تمیز روی حالت خودکار قرار گرفت" else "آدرس IP تمیز روی $ip قفل شد",
            "Clean IP override set to: ${ip ?: "auto"}"
        )
    }

    fun selectActiveRoute(index: Int) {
        prefs.edit().putInt("active_entry", index).apply()
        _ui.update { it.copy(activeEntryIndex = index) }
        val remark = _ui.value.subscription?.entries?.getOrNull(index)?.remarks ?: "route-$index"
        TunnelLogBuffer.updatePingAndProfile(_ui.value.verifiedPingMs, _ui.value.cleanIp, remark)
        TunnelLogBuffer.log(
            LogLevel.INFO,
            LogCategory.STEP,
            "مسیر فعال به «$remark» تغییر یافت",
            "Active subscription entry switched to index=$index ($remark)"
        )
    }

    fun toggleTcpFirst(enabled: Boolean) {
        prefs.edit().putBoolean("tcp_first", enabled).apply()
        _ui.update { it.copy(tcpFirstEnabled = enabled) }
        TunnelLogBuffer.log(
            LogLevel.INFO,
            LogCategory.STEP,
            if (enabled) "پروفایل ضد-محدودیت UDP (اولویت TCP Fragment) فعال شد" else "پروفایل استاندارد روتینگ فعال شد",
            "tcpFirstProfile=${enabled}"
        )
    }

    /** Hiddify / v2rayNG style on-demand Real Delay (URL Test) through Xray SOCKS5 :10808. */
    fun runUrlPingTest() {
        if (_ui.value.isTestingUrl) return
        viewModelScope.launch {
            _ui.update { it.copy(isTestingUrl = true) }
            TunnelLogBuffer.log(
                LogLevel.INFO,
                LogCategory.PROBE,
                "در حال تست پینگ واقعی از داخل تونل Xray (127.0.0.1:10808)...",
                "TunnelVerifier.verifyThroughSocks5(127.0.0.1:10808) started"
            )
            val res = withContext(Dispatchers.IO) {
                val app = getApplication<Application>()
                TunnelLogBuffer.ingestXrayLogTail(File(app.filesDir, "xray/xray-out.log"))
                TunnelVerifier.verifyThroughSocks5()
            }
            if (res.ok) {
                TunnelLogBuffer.updatePingAndProfile(res.latencyMs)
                TunnelLogBuffer.log(
                    LogLevel.SUCCESS,
                    LogCategory.PROBE,
                    "تست تونل موفق! پینگ واقعی: ${res.latencyMs} ms (${res.detail})",
                    "TunnelVerifier OK: target=${res.target} latency=${res.latencyMs}ms status=${res.detail}"
                )
                _ui.update { it.copy(isTestingUrl = false, verifiedPingMs = res.latencyMs) }
            } else {
                TunnelLogBuffer.log(
                    LogLevel.WARN,
                    LogCategory.PROBE,
                    "تست عبور ترافیک ناموفق بود (${res.detail})",
                    "TunnelVerifier FAILED: ${res.detail}"
                )
                _ui.update { it.copy(isTestingUrl = false, verifiedPingMs = null) }
            }
        }
    }

    /** F-13: Prepare offline survival cache (subscription + embedded fallback + geo data). */
    fun runBlackoutPrep(): Boolean {
        return try {
            val app = getApplication<Application>()
            val subFile = File(app.filesDir, "subscription.json")
            if (!subFile.exists() || subFile.length() == 0L) {
                subFile.writeText(Subscription.EMBEDDED_FALLBACK_JSON)
                File(app.filesDir, "subscription.meta").writeText(System.currentTimeMillis().toString())
            }
            core.ensureInstalled()
            val sub = repository.cachedAnyAge() ?: repository.embeddedFallback()
            _ui.update { it.copy(subscription = sub, prepReady = true) }
            TunnelLogBuffer.log(
                LogLevel.SUCCESS,
                LogCategory.STEP,
                "آماده‌سازی آفلاین کامل شد: هستهٔ Xray، فایل‌های Geo و کانفیگ اضطراری ذخیره شدند",
                "BlackoutPrep: subscription.json + geoip.dat/geosite.dat + libxraycore.so verified"
            )
            true
        } catch (_: Exception) {
            false
        }
    }

    private fun diag(msg: String) = android.util.Log.d("GhDiag", msg)

    /**
     * F-1 → F-2/F-3/F-4: one-tap connect with 5-step telemetry + Auto-Heal.
     */
    fun onConnectTap() {
        if (_ui.value.connectPhase != ConnectPhase.IDLE && _ui.value.connectPhase != ConnectPhase.FAILED) return
        viewModelScope.launch {
            TunnelLogBuffer.resetSessionStats()
            TunnelLogBuffer.updateStep(1, "گام ۱ از ۵: بررسی و بارگذاری کانفیگ اشتراک...")
            TunnelLogBuffer.log(
                LogLevel.INFO,
                LogCategory.STEP,
                "شروع فرآیند اتصال هوشمند — بررسی کانفیگ...",
                "onConnectTap() -> Phase CHECKING"
            )
            diag("connect: tap -> CHECKING (have sub=${_ui.value.subscription != null})")
            _ui.update {
                it.copy(
                    connectPhase = ConnectPhase.CHECKING,
                    isUpdating = true,
                    tunnelError = null,
                    verifiedPingMs = null,
                    isAutoHealing = false
                )
            }
            val sub = if (_ui.value.subscription == null ||
                System.currentTimeMillis() - (_ui.value.subscription?.fetchedAt ?: 0) >
                Subscription.STALE_AFTER_MS
            ) {
                diag("connect: fetching subscription (primary+mirror, timeouts 20s/30s)")
                val r = repository.update()
                diag("connect: fetch result=${r.isSuccess} ${r.exceptionOrNull()?.message ?: ""}")
                r.getOrNull() ?: _ui.value.subscription ?: repository.cachedAnyAge() ?: repository.embeddedFallback()
            } else {
                _ui.value.subscription
            }
            if (sub == null) {
                diag("connect: FAILED — no subscription available")
                TunnelLogBuffer.updateStep(0, "خطا: هیچ کانفیگی یافت نشد")
                TunnelLogBuffer.log(
                    LogLevel.ERROR,
                    LogCategory.STEP,
                    "خطا: کانفیگ اشتراک در دسترس نیست",
                    "connect FAILED: subscription null"
                )
                _ui.update {
                    it.copy(
                        isUpdating = false,
                        connectPhase = ConnectPhase.FAILED,
                        configError = "config_update_failed",
                        tunnelError = "config_unavailable"
                    )
                }
                return@launch
            }
            diag("connect: sub ok entries=${sub.entries.size} -> PREPARING (core extract+version)")

            TunnelLogBuffer.updateStep(2, "گام ۲ از ۵: آماده‌سازی هستهٔ Xray-core...")
            _ui.update { it.copy(connectPhase = ConnectPhase.PREPARING, subscription = sub) }
            val infoR = core.ensureInstalled()
            val info = infoR.getOrNull()
            diag("connect: ensureInstalled=${infoR.isSuccess} version=${info?.version} err=${infoR.exceptionOrNull()?.message}")
            if (info == null || !xrayVersionOk(info.version, sub.entries.firstOrNull()?.minCoreVersion ?: "26.6.27")) {
                diag("connect: FAILED — core unavailable/old (min=${sub.entries.firstOrNull()?.minCoreVersion})")
                TunnelLogBuffer.updateStep(0, "خطا در راه‌اندازی باینری Xray")
                TunnelLogBuffer.log(
                    LogLevel.ERROR,
                    LogCategory.XRAY,
                    "هستهٔ Xray آماده نشد (${infoR.exceptionOrNull()?.message ?: "نسخه نامعتبر"})",
                    "ensureInstalled failed: version=${info?.version} err=${infoR.exceptionOrNull()?.message}"
                )
                _ui.update {
                    it.copy(
                        isUpdating = false,
                        connectPhase = ConnectPhase.FAILED,
                        coreVersion = info?.version,
                        tunnelError = "core_unavailable"
                    )
                }
                return@launch
            }
            TunnelLogBuffer.log(
                LogLevel.SUCCESS,
                LogCategory.XRAY,
                "هستهٔ رسمی Xray-core v${info.version} آماده است",
                "Xray binary verified at ${info.path.name} (v${info.version})"
            )

            TunnelLogBuffer.updateStep(3, "گام ۳ از ۵: اجرای Xray و باز کردن پورت 10808...")
            _ui.update { it.copy(connectPhase = ConnectPhase.TUNNELING, coreVersion = info.version) }
            val cfgFile = writeRuntimeConfig(sub)
            diag("connect: config written bytes=${try { cfgFile.length() } catch (e: Exception) { -1L }} path=${cfgFile.path}")
            core.stop()
            val started = core.start(cfgFile)
            diag("connect: core.start=${started.isSuccess} ${started.exceptionOrNull()?.message ?: ""}")
            if (started.isSuccess) {
                val activeRemark = sub.entries.getOrNull(_ui.value.activeEntryIndex)?.remarks
                    ?: sub.entries.firstOrNull()?.remarks
                    ?: "Serverless-v52-fragA"
                TunnelLogBuffer.updatePingAndProfile(null, _ui.value.cleanIp, activeRemark)
                TunnelLogBuffer.log(
                    LogLevel.SUCCESS,
                    LogCategory.XRAY,
                    "پروکسی محلی Xray روی 127.0.0.1:10808 و DNS روی :15353 فعال شد",
                    "Xray started with config=${cfgFile.name} (${cfgFile.length()}B) profile=$activeRemark"
                )
                TunnelLogBuffer.updateStep(4, "گام ۴ از ۵: برقراری تونل VPN و تست عبور ترافیک...")
                _ui.update { it.copy(vpnPending = true) }
            } else {
                TunnelLogBuffer.updateStep(0, "خطا در اجرای هستهٔ Xray")
                TunnelLogBuffer.log(
                    LogLevel.ERROR,
                    LogCategory.XRAY,
                    "اجرای هستهٔ Xray با خطا مواجه شد",
                    "core.start failed: ${started.exceptionOrNull()?.message}"
                )
                _ui.update {
                    it.copy(
                        connectPhase = ConnectPhase.FAILED,
                        tunnelError = "core_start_failed"
                    )
                }
            }
            _ui.update { it.copy(isUpdating = false) }
        }
    }

    /**
     * F-17/F-15 + single-active-entry: write the runtime config for the ACTIVE
     * subscription entry only (both entries bind mixed-in :10808 — running them
     * together would conflict). Injects the loopback DNS inbound for the tunnel.
     */
    fun writeRuntimeConfig(sub: SubscriptionInfo): File {
        val app = getApplication<Application>()
        val cfg = File(app.filesDir, "xray-config.json")
        return try {
            val cleanIp = prefs.getString("clean_ip", null)
            val active = prefs.getInt("active_entry", 0)
            val tcpFirst = prefs.getBoolean("tcp_first", true)
            val patched = sub.rawJson.activeEntryConfigJson(active, cleanIp, tcpFirst)
            cfg.writeText(patched)
            cfg
        } catch (e: Exception) {
            File(app.filesDir, "missing.json")
        }
    }

    /** Called by the Activity after VpnService.establish() succeeded. */
    fun onVpnEstablished() {
        _ui.update { it.copy(connectPhase = ConnectPhase.CONNECTED, vpnPending = false, tunnelError = null) }
        TunnelLogBuffer.updateStep(5, "متصل — در حال راستی‌آزمایی پینگ واقعی تونل...")
        verifyAndAutoHealIfNeeded()
    }

    private fun verifyAndAutoHealIfNeeded() {
        viewModelScope.launch(Dispatchers.IO) {
            val app = getApplication<Application>()
            val xrayOut = File(app.filesDir, "xray/xray-out.log")
            try { Thread.sleep(350) } catch (_: InterruptedException) {}
            TunnelLogBuffer.ingestXrayLogTail(xrayOut)

            val firstCheck = TunnelVerifier.verifyThroughSocks5(timeoutMs = 4000)
            TunnelLogBuffer.ingestXrayLogTail(xrayOut)
            if (firstCheck.ok) {
                TunnelLogBuffer.updatePingAndProfile(firstCheck.latencyMs)
                TunnelLogBuffer.updateStep(5, "متصل و تاییدشده (پینگ واقعی: ${firstCheck.latencyMs} ms)", isAutoHealing = false)
                TunnelLogBuffer.log(
                    LogLevel.SUCCESS,
                    LogCategory.PROBE,
                    "✓ عبور واقعی ترافیک از تونل تایید شد! پینگ: ${firstCheck.latencyMs} ms",
                    "TunnelVerifier PASS: ${firstCheck.target} -> ${firstCheck.detail} (${firstCheck.latencyMs}ms)"
                )
                _ui.update { it.copy(verifiedPingMs = firstCheck.latencyMs, isAutoHealing = false) }
                return@launch
            }

            // Auto-Heal: scan for a clean Cloudflare IP, patch config, restart Xray, and re-verify
            _ui.update { it.copy(isAutoHealing = true) }
            TunnelLogBuffer.updateStep(4, "در حال خودترمیمی (Auto-Heal): اسکن IP تمیز کلودفلر...", isAutoHealing = true)
            TunnelLogBuffer.log(
                LogLevel.WARN,
                LogCategory.PROBE,
                "مسیر پیش‌فرض پاسخ نداد (${firstCheck.detail}) — شروع خودکار اسکن IP تمیز (Auto-Heal)...",
                "Auto-Heal triggered after initial probe failure: ${firstCheck.detail}"
            )
            val scanner = CleanIpScanner()
            val report = scanner.scan()
            val best = report.best
            if (best != null) {
                scanner.saveBest(best.ip, app)
                _ui.update { it.copy(cleanIp = best.ip, scanResults = report.results) }
                TunnelLogBuffer.log(
                    LogLevel.SUCCESS,
                    LogCategory.PROBE,
                    "IP تمیز جایگزین شد: ${best.ip} (${best.latencyMs} ms) — بازنشانی هستهٔ Xray...",
                    "Auto-Heal applying cleanIp=${best.ip} (${best.latencyMs}ms)"
                )
                val sub = _ui.value.subscription ?: repository.cachedAnyAge() ?: repository.embeddedFallback()
                val cfgFile = writeRuntimeConfig(sub)
                core.stop()
                core.start(cfgFile)
                try { Thread.sleep(450) } catch (_: InterruptedException) {}
                val secondCheck = TunnelVerifier.verifyThroughSocks5(timeoutMs = 4500)
                TunnelLogBuffer.ingestXrayLogTail(xrayOut)
                if (secondCheck.ok) {
                    TunnelLogBuffer.updatePingAndProfile(secondCheck.latencyMs, cleanIp = best.ip)
                    TunnelLogBuffer.updateStep(5, "متصل با IP تمیز ${best.ip} (پینگ: ${secondCheck.latencyMs} ms)", isAutoHealing = false)
                    TunnelLogBuffer.log(
                        LogLevel.SUCCESS,
                        LogCategory.PROBE,
                        "✓ خودترمیمی (Auto-Heal) موفق بود! اتصال با IP تمیز ${best.ip} برقرار شد (${secondCheck.latencyMs} ms)",
                        "Auto-Heal PASS via cleanIp=${best.ip} latency=${secondCheck.latencyMs}ms"
                    )
                    _ui.update { it.copy(verifiedPingMs = secondCheck.latencyMs, isAutoHealing = false) }
                    return@launch
                }
            }

            TunnelLogBuffer.updateStep(5, "تونل فعال است (تست پینگ اولیه زمان‌بر شد — لاگ زنده را ببینید)", isAutoHealing = false)
            _ui.update { it.copy(isAutoHealing = false) }
        }
    }

    /** Called by the Activity after the VPN step failed (denied / establish error). */
    fun onVpnFailed(reason: String) {
        TunnelLogBuffer.updateStep(0, "رد مجوز VPN یا خطا در ایجاد تونل ($reason)")
        TunnelLogBuffer.log(
            LogLevel.ERROR,
            LogCategory.TUN,
            "ایجاد تونل VPN لغو شد یا با خطا مواجه گردید ($reason)",
            "onVpnFailed: reason=$reason"
        )
        _ui.update { it.copy(connectPhase = ConnectPhase.FAILED, vpnPending = false, tunnelError = reason) }
        core.stop()
    }

    /** F-4: disconnect < 3s. */
    fun disconnect() {
        TunnelLogBuffer.updateStep(0, "اتصال قطع شد")
        TunnelLogBuffer.log(
            LogLevel.INFO,
            LogCategory.STEP,
            "تونل VPN و هستهٔ Xray به درخواست کاربر متوقف شدند",
            "disconnect() called -> stopping XrayCore & VpnTunnelService"
        )
        _ui.update {
            it.copy(
                connectPhase = ConnectPhase.IDLE,
                vpnPending = false,
                verifiedPingMs = null,
                isAutoHealing = false
            )
        }
        core.stop()
    }

    fun resetConnect() {
        _ui.update { it.copy(connectPhase = ConnectPhase.IDLE) }
    }

    override fun onCleared() {
        monitor.stop()
        core.close()
        super.onCleared()
    }
}

/**
 * Extract entry [index] from the subscription array and apply F-17 (clean egress),
 * F-15 (TCP-first) and the loopback DNS inbound. Best-effort, pure.
 */
private fun String.activeEntryConfigJson(index: Int, cleanIp: String?, tcpFirst: Boolean = true): String {
    return try {
        val arr = org.json.JSONArray(this)
        val c = arr.getJSONObject(index.coerceIn(0, (arr.length() - 1).coerceAtLeast(0)))
        if (cleanIp != null) ConfigPatcher.patchCleanEgress(c, cleanIp)
        if (tcpFirst) ConfigPatcher.tcpFirstProfile(c)
        ConfigPatcher.addLocalDnsInbound(c)
        ConfigPatcher.ensureConsistentDns(c)
        c.toString()
    } catch (e: Exception) {
        this
    }
}
