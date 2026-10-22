package com.ghprotocol.app

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import com.ghprotocol.app.ui.HomeScreen
import com.ghprotocol.app.ui.theme.GhProtocolTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            GhProtocolTheme {
                HomeScreen()
            }
        }
    }
}
