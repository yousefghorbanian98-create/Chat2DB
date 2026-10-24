package com.ghprotocol.app

import android.os.Bundle
import android.util.DisplayMetrics
import android.content.res.Configuration
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.lifecycle.viewmodel.compose.viewModel
import com.ghprotocol.app.domain.SettingsStore
import com.ghprotocol.app.ui.GhNavHost
import com.ghprotocol.app.ui.HomeViewModel
import com.ghprotocol.app.ui.theme.GhProtocolTheme
import java.util.Locale

class MainActivity : ComponentActivity() {
    companion object {
        const val ACTION_CONNECT = "com.ghprotocol.app.action.CONNECT"
        /** Set by the deep-link (ghprotocol://connect / ACTION_CONNECT) — consumed once by HomeViewModel. */
        @Volatile
        var pendingConnect: Boolean = false
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        if (savedInstanceState == null && wantsConnect(intent)) {
            pendingConnect = true
        }
        enableEdgeToEdge()
        val settings = SettingsStore(this)
        when (settings.language) {
            "fa" -> applyLocale(Locale("fa"))
            "en" -> applyLocale(Locale("en"))
        }
        setContent {
            GhProtocolTheme(
                forceDark = when (settings.theme) {
                    "dark" -> true
                    "light" -> false
                    else -> null
                }
            ) {
                val vm: HomeViewModel = viewModel()
                GhNavHost(viewModel = vm)
            }
        }
    }

    private fun wantsConnect(intent: android.content.Intent?): Boolean {
        if (intent == null) return false
        if (intent.action == ACTION_CONNECT) return true
        if (intent.action == android.content.Intent.ACTION_VIEW) {
            val data = intent.data
            if (data != null && data.scheme == "ghprotocol" && data.host == "connect") return true
        }
        return false
    }

    private fun applyLocale(locale: Locale) {
        val res = resources
        val metrics: DisplayMetrics = res.displayMetrics
        val config: Configuration = res.configuration
        config.setLocale(locale)
        res.updateConfiguration(config, metrics)
    }
}
