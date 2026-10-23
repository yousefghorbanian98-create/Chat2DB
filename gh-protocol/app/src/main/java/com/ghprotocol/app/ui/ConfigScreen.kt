package com.ghprotocol.app.ui

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Card
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.ghprotocol.app.R
import com.ghprotocol.app.domain.Subscription

@Composable
fun ConfigScreen(viewModel: HomeViewModel = viewModel(), modifier: Modifier = Modifier) {
    val ui by viewModel.ui.collectAsState()
    Scaffold(topBar = { TopAppBar(title = { Text(stringResource(R.string.config_source)) }) }) { padding ->
        Column(
            modifier = modifier
                .fillMaxSize()
                .padding(padding)
                .verticalScroll(rememberScrollState())
                .padding(24.dp)
        ) {
            Text(stringResource(R.string.config_url), style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
            Text(Subscription.SUBSCRIPTION_URL, style = MaterialTheme.typography.bodyMedium)
            Spacer(Modifier.height(4.dp))
            Text(stringResource(R.string.config_mirror), style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
            Text(Subscription.MIRROR_URL, style = MaterialTheme.typography.bodyMedium)
            Spacer(Modifier.height(20.dp))
            val sub = ui.subscription
            if (sub == null) {
                Text(stringResource(R.string.config_none), style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
            } else {
                for (e in sub.entries) {
                    Card(modifier = Modifier.fillMaxWidth()) {
                        Column(Modifier.padding(16.dp)) {
                            Text(e.remarks, style = MaterialTheme.typography.titleMedium)
                            Text(
                                stringResource(R.string.config_entry_meta, e.minCoreVersion, e.inboundPort, e.features.joinToString(" · ")),
                                style = MaterialTheme.typography.bodySmall,
                                color = MaterialTheme.colorScheme.onSurfaceVariant
                            )
                        }
                    }
                    Spacer(Modifier.height(8.dp))
                }
            }
            Spacer(Modifier.height(16.dp))
            Text(
                stringResource(R.string.config_last_update, viewModel.repository.lastUpdateText() ?: "—"),
                style = MaterialTheme.typography.labelSmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
            Spacer(Modifier.height(12.dp))
            OutlinedButton(onClick = { viewModel.refreshConfig() }, enabled = !ui.isUpdating, modifier = Modifier.fillMaxWidth()) {
                Text(if (ui.isUpdating) stringResource(R.string.connect_checking) else stringResource(R.string.update_now))
            }
            Spacer(Modifier.height(12.dp))
            Text(
                stringResource(R.string.config_autorefresh),
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.outline,
                textAlign = TextAlign.Center
            )
        }
    }
}
