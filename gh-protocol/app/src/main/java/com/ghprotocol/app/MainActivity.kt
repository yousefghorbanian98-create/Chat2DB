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
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
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

    private fun applyLocale(locale: Locale) {
        val res = resources
        val metrics: DisplayMetrics = res.displayMetrics
        val config: Configuration = res.configuration
        config.setLocale(locale)
        res.updateConfiguration(config, metrics)
    }
}
