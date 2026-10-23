package com.ghprotocol.app

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.lifecycle.viewmodel.compose.viewModel
import com.ghprotocol.app.ui.GhNavHost
import com.ghprotocol.app.ui.HomeViewModel
import com.ghprotocol.app.ui.theme.GhProtocolTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            GhProtocolTheme {
                val vm: HomeViewModel = viewModel()
                GhNavHost(viewModel = vm)
            }
        }
    }
}
