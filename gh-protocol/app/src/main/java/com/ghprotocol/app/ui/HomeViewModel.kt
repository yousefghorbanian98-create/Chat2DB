package com.ghprotocol.app.ui

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.ghprotocol.app.domain.NetworkMonitor
import com.ghprotocol.app.domain.NetworkState
import com.ghprotocol.app.domain.SubscriptionInfo
import com.ghprotocol.app.domain.SubscriptionRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

enum class ConnectPhase { IDLE, CHECKING, READY, TUNNEL_PENDING }

data class HomeUiState(
    val network: NetworkState = NetworkState.UNKNOWN,
    val subscription: SubscriptionInfo? = null,
    val configError: String? = null,      // F-5 honest message
    val isUpdating: Boolean = false,
    val connectPhase: ConnectPhase = ConnectPhase.IDLE
)

class HomeViewModel(app: Application) : AndroidViewModel(app) {

    val repository = SubscriptionRepository(app)
    val monitor = NetworkMonitor()

    private val _ui = MutableStateFlow(HomeUiState(subscription = repository.cachedAnyAge()))
    val ui: StateFlow<HomeUiState> = _ui.asStateFlow()

    init {
        _ui.update { it.copy(subscription = repository.cachedAnyAge()) }
        // F-12: instant re-sync when international link recovers
        monitor.start(viewModelScope) {
            viewModelScope.launch { refreshConfig() }
        }
        if (_ui.value.subscription == null) {
            viewModelScope.launch { refreshConfig() }
        }
    }

    fun refreshConfig() {
        viewModelScope.launch {
            _ui.update { it.copy(isUpdating = true, configError = null) }
            when (val r = repository.update()) {
                is Result.Success -> _ui.update {
                    it.copy(isUpdating = false, subscription = r.getOrNull())
                }
                is Result.Failure -> _ui.update {
                    it.copy(
                        isUpdating = false,
                        subscription = it.subscription ?: repository.cachedAnyAge(),
                        configError = "config_update_failed"
                    )
                }
            }
        }
    }

    /** F-1: one-tap connect flow (P1: everything up to the tunnel stage). */
    fun onConnectTap() {
        if (_ui.value.connectPhase != ConnectPhase.IDLE) return
        viewModelScope.launch {
            _ui.update { it.copy(connectPhase = ConnectPhase.CHECKING, isUpdating = true) }
            val fresh = if (_ui.value.subscription == null ||
                System.currentTimeMillis() - (_ui.value.subscription?.fetchedAt ?: 0) >
                    com.ghprotocol.app.domain.Subscription.STALE_AFTER_MS
            ) {
                repository.update().getOrNull() ?: _ui.value.subscription
            } else {
                _ui.value.subscription
            }
            _ui.update {
                it.copy(
                    isUpdating = false,
                    subscription = fresh,
                    connectPhase = if (fresh != null) ConnectPhase.READY else ConnectPhase.IDLE,
                    configError = if (fresh == null) "config_update_failed" else null
                )
            }
        }
    }

    fun resetConnect() {
        _ui.update { it.copy(connectPhase = ConnectPhase.IDLE) }
    }

    override fun onCleared() {
        monitor.stop()
        super.onCleared()
    }
}
