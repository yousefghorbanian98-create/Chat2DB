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
    fun onConnectTap() {
        if (_ui.value.connectPhase != ConnectPhase.IDLE && _ui.value.connectPhase != ConnectPhase.FAILED) return
        viewModelScope.launch {
            _ui.update { it.copy(connectPhase = ConnectPhase.CHECKING, isUpdating = true, tunnelError = null) }
            val sub = if (_ui.value.subscription == null ||
                System.currentTimeMillis() - (_ui.value.subscription?.fetchedAt ?: 0) >
                Subscription.STALE_AFTER_MS
            ) {
                repository.update().getOrNull() ?: _ui.value.subscription
            } else {
                _ui.value.subscription
            }
            if (sub == null) {
                _ui.update {
                    it.copy(isUpdating = false, connectPhase = ConnectPhase.FAILED,
                        configError = "config_update_failed",
                        tunnelError = "config_unavailable")
                }
                return@launch
            }

            _ui.update { it.copy(connectPhase = ConnectPhase.PREPARING) }
            val info = core.ensureInstalled().getOrNull()
            if (info == null || !xrayVersionOk(info.version, sub.entries.firstOrNull()?.minCoreVersion ?: "26.6.27")) {
                _ui.update {
                    it.copy(connectPhase = ConnectPhase.FAILED,
                        coreVersion = info?.version,
                        tunnelError = "core_unavailable")
                }
                return@launch
            }

            _ui.update { it.copy(connectPhase = ConnectPhase.TUNNELING, coreVersion = info.version) }
            val cfgFile = writeRuntimeConfig(sub)
            val started = core.start(cfgFile)
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

    /** F-17/F-15: write the runtime config (official JSON + clean egress + TCP-first). */
    fun writeRuntimeConfig(sub: SubscriptionInfo): File {
        val ctx = getApplication<Application>().filesDir
        val cfg = File(ctx, "xray-config.json")
        return try {
            val cleanIp = ctx.getSharedPreferences("gh-settings", Context.MODE_PRIVATE)
                .getString("clean_ip", null)
            val patched = sub.rawJson.patchesCleanEgress(cleanIp)
            cfg.writeText(patched)
            cfg
        } catch (e: Exception) {
            File(ctx, "missing.json")
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

/** F-17 (clean egress) + F-15 (TCP-first) applied to the raw subscription JSON (best-effort, pure). */
private fun String.patchesCleanEgress(cleanIp: String?): String {
    return try {
        val arr = org.json.JSONArray(this)
        for (i in 0 until arr.length()) {
            val c = arr.getJSONObject(i)
            if (cleanIp != null) ConfigPatcher.patchCleanEgress(c, cleanIp)
            ConfigPatcher.tcpFirstProfile(c)
        }
        arr.toString()
    } catch (e: Exception) {
        this
    }
}
