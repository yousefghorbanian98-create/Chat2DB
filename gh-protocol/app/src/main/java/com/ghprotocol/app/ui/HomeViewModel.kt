package com.ghprotocol.app.ui

import android.app.Application
import android.content.Context
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.ghprotocol.app.core.ConfigPatcher
import com.ghprotocol.app.core.XrayCore
import com.ghprotocol.app.core.xrayVersionOk
import com.ghprotocol.app.domain.NetworkMonitor
import com.ghprotocol.app.domain.NetworkState
import com.ghprotocol.app.domain.Subscription
import com.ghprotocol.app.domain.SubscriptionInfo
import com.ghprotocol.app.domain.SubscriptionRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
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
    val vpnPending: Boolean = false
)

class HomeViewModel(
    app: Application,
    val repository: SubscriptionRepository = SubscriptionRepository(app),
    val monitor: NetworkMonitor = NetworkMonitor(),
    val core: XrayCore = XrayCore(app)
) : AndroidViewModel(app) {

    private val _ui = MutableStateFlow(HomeUiState(subscription = repository.cachedAnyAge()))
    val ui: StateFlow<HomeUiState> = _ui.asStateFlow()

    init {
        _ui.update { it.copy(subscription = repository.cachedAnyAge()) }
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
            val r = repository.update()
            _ui.update {
                if (r.isSuccess) {
                    it.copy(isUpdating = false, subscription = r.getOrNull())
                } else {
                    it.copy(
                        isUpdating = false,
                        subscription = it.subscription ?: repository.cachedAnyAge(),
                        configError = "config_update_failed"
                    )
                }
            }
        }
    }

    /**
     * F-1 → F-2/F-3/F-4: one-tap connect, now real.
     * CHECKING (config fresh) → PREPARING (core extract + version) →
     * TUNNELING (patched config written + Xray started) → vpnPending
     * (Activity establishes VpnService) → CONNECTED.
     */
    private fun diag(msg: String) = android.util.Log.d("GhDiag", msg)

    fun onConnectTap() {
        if (_ui.value.connectPhase != ConnectPhase.IDLE && _ui.value.connectPhase != ConnectPhase.FAILED) return
        viewModelScope.launch {
            diag("connect: tap -> CHECKING (have sub=${_ui.value.subscription != null})")
            _ui.update { it.copy(connectPhase = ConnectPhase.CHECKING, isUpdating = true, tunnelError = null) }
            val sub = if (_ui.value.subscription == null ||
                System.currentTimeMillis() - (_ui.value.subscription?.fetchedAt ?: 0) >
                Subscription.STALE_AFTER_MS
            ) {
                diag("connect: fetching subscription (primary+mirror, timeouts 20s/30s)")
                val r = repository.update()
                diag("connect: fetch result=${r.isSuccess} ${r.exceptionOrNull()?.message ?: ""}")
                r.getOrNull() ?: _ui.value.subscription
            } else {
                _ui.value.subscription
            }
            if (sub == null) {
                diag("connect: FAILED — no subscription available")
                _ui.update {
                    it.copy(isUpdating = false, connectPhase = ConnectPhase.FAILED,
                        configError = "config_update_failed",
                        tunnelError = "config_unavailable")
                }
                return@launch
            }
            diag("connect: sub ok entries=${sub.entries.size} -> PREPARING (core extract+version)")

            _ui.update { it.copy(connectPhase = ConnectPhase.PREPARING) }
            val infoR = core.ensureInstalled()
            val info = infoR.getOrNull()
            diag("connect: ensureInstalled=${infoR.isSuccess} version=${info?.version} err=${infoR.exceptionOrNull()?.message}")
            if (info == null || !xrayVersionOk(info.version, sub.entries.firstOrNull()?.minCoreVersion ?: "26.6.27")) {
                diag("connect: FAILED — core unavailable/old (min=${sub.entries.firstOrNull()?.minCoreVersion})")
                _ui.update {
                    it.copy(connectPhase = ConnectPhase.FAILED,
                        coreVersion = info?.version,
                        tunnelError = "core_unavailable")
                }
                return@launch
            }

            _ui.update { it.copy(connectPhase = ConnectPhase.TUNNELING, coreVersion = info.version) }
            val cfgFile = writeRuntimeConfig(sub)
            diag("connect: config written bytes=${try { cfgFile.length() } catch (e: Exception) { -1L }} path=${cfgFile.path}")
            val started = core.start(cfgFile)
            diag("connect: core.start=${started.isSuccess} ${started.exceptionOrNull()?.message ?: ""}")
            if (started.isSuccess) {
                _ui.update { it.copy(vpnPending = true) }
            } else {
                _ui.update {
                    it.copy(connectPhase = ConnectPhase.FAILED,
                        tunnelError = "core_start_failed")
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
            val prefs = app.getSharedPreferences("gh-settings", Context.MODE_PRIVATE)
            val cleanIp = prefs.getString("clean_ip", null)
            val active = prefs.getInt("active_entry", 0)
            val patched = sub.rawJson.activeEntryConfigJson(active, cleanIp)
            cfg.writeText(patched)
            cfg
        } catch (e: Exception) {
            File(app.filesDir, "missing.json")
        }
    }

    /** Called by the Activity after VpnService.establish() succeeded. */
    fun onVpnEstablished() {
        _ui.update { it.copy(connectPhase = ConnectPhase.CONNECTED, vpnPending = false, tunnelError = null) }
    }

    /** Called by the Activity after the VPN step failed (denied / establish error). */
    fun onVpnFailed(reason: String) {
        _ui.update { it.copy(connectPhase = ConnectPhase.FAILED, vpnPending = false, tunnelError = reason) }
        core.stop()
    }

    /** F-4: disconnect < 3s. */
    fun disconnect() {
        _ui.update { it.copy(connectPhase = ConnectPhase.IDLE, vpnPending = false) }
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
private fun String.activeEntryConfigJson(index: Int, cleanIp: String?): String {
    return try {
        val arr = org.json.JSONArray(this)
        val c = arr.getJSONObject(index.coerceIn(0, (arr.length() - 1).coerceAtLeast(0)))
        if (cleanIp != null) ConfigPatcher.patchCleanEgress(c, cleanIp)
        ConfigPatcher.tcpFirstProfile(c)
        ConfigPatcher.addLocalDnsInbound(c)
        c.toString()
    } catch (e: Exception) {
        this
    }
}
