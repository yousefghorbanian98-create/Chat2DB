package com.ghprotocol.app.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Card
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import com.ghprotocol.app.R

private fun phase2Card(title: String, body: String, feature: String, modifier: Modifier = Modifier) {
    Scaffold(topBar = { TopAppBar(title = { Text(title) }) }, modifier = modifier) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(24.dp),
            verticalArrangement = Arrangement.Center,
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Card(Modifier.fillMaxWidth()) {
                Column(Modifier.padding(24.dp), horizontalAlignment = Alignment.CenterHorizontally) {
                    Text(feature, style = MaterialTheme.typography.titleMedium, color = MaterialTheme.colorScheme.primary)
                    Spacer(Modifier.height(12.dp))
                    Text(body, style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant, textAlign = TextAlign.Center)
                    Spacer(Modifier.height(12.dp))
                    Text(stringResource(R.string.phase2_badge), style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.outline)
                }
            }
        }
    }
}

@Composable
fun ScannerScreen(modifier: Modifier = Modifier) =
    phase2Card(stringResource(R.string.clean_ip_title), stringResource(R.string.clean_ip_body), "F-17", modifier)

@Composable
fun BalancerScreen(modifier: Modifier = Modifier) =
    phase2Card(stringResource(R.string.routes_title), stringResource(R.string.routes_body), "F-18", modifier)

@Composable
fun PrepScreen(modifier: Modifier = Modifier) =
    phase2Card(stringResource(R.string.blackout_prep_title), stringResource(R.string.blackout_prep_body), "F-13", modifier)
