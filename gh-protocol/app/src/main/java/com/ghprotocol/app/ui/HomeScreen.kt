package com.ghprotocol.app.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.CheckCircle
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material.icons.filled.Warning
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.ghprotocol.app.R
import com.ghprotocol.app.domain.NetworkState
import com.ghprotocol.app.ui.theme.GhBlue

private val Amber = Color(0xFFF5A524)
private val Red = Color(0xFFE5484D)

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HomeScreen(
    modifier: Modifier = Modifier,
    viewModel: HomeViewModel = viewModel(),
    onOpenConfig: () -> Unit = {},
    onOpenGuide: () -> Unit = {},
    onOpenQr: () -> Unit = {},
    onOpenScanner: () -> Unit = {},
    onOpenBalancer: () -> Unit = {},
    onOpenPrep: () -> Unit = {}
) {
    val ui by viewModel.ui.collectAsState()
    Scaffold(
        topBar = { TopAppBar(title = { Text(stringResource(R.string.app_name)) }) }
    ) { padding ->
        Column(
            modifier = modifier
                .fillMaxSize()
                .padding(padding)
                .verticalScroll(rememberScrollState())
                .padding(24.dp),
            verticalArrangement = Arrangement.Center,
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            StatusCard(state = ui.network)

            Spacer(Modifier.height(20.dp))

            ConnectArea(
                phase = ui.connectPhase,
                isUpdating = ui.isUpdating,
                hasConfig = ui.subscription != null,
                onTap = { viewModel.onConnectTap() }
            )

            if (ui.configError != null) {
                Spacer(Modifier.height(12.dp))
                Text(
                    text = stringResource(R.string.config_update_failed),
                    color = Amber,
                    style = MaterialTheme.typography.bodyMedium
                )
                OutlinedButton(onClick = { viewModel.refreshConfig() }) {
                    Text(stringResource(R.string.retry))
                }
            }

            ui.subscription?.let { sub ->
                Spacer(Modifier.height(16.dp))
                Text(
                    text = stringResource(R.string.config_line, sub.entries.joinToString(" · ") { it.remarks }),
                    style = MaterialTheme.typography.labelSmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }

            Spacer(Modifier.height(24.dp))
            Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                OutlinedButton(onClick = onOpenConfig) { Text(stringResource(R.string.config_source)) }
                OutlinedButton(onClick = onOpenGuide) { Text(stringResource(R.string.guide)) }
                OutlinedButton(onClick = onOpenQr) { Text(stringResource(R.string.qr_share)) }
            }
            Spacer(Modifier.height(8.dp))
            Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                OutlinedButton(onClick = onOpenScanner) { Text(stringResource(R.string.clean_ip_short)) }
                OutlinedButton(onClick = onOpenBalancer) { Text(stringResource(R.string.routes_short)) }
                OutlinedButton(onClick = onOpenPrep) { Text(stringResource(R.string.blackout_prep_short)) }
            }
        }
    }
}

@Composable
private fun StatusCard(state: NetworkState, modifier: Modifier = Modifier) {
    val spec = when (state) {
        NetworkState.CONNECTED -> StatusSpec(Icons.Filled.CheckCircle, GhBlue, R.string.st_connected, R.string.st_connected_body)
        NetworkState.DEGRADED -> StatusSpec(Icons.Filled.Warning, Amber, R.string.st_degraded, R.string.st_degraded_body)
        NetworkState.CUTOFF -> StatusSpec(Icons.Filled.Close, Red, R.string.st_cutoff, R.string.st_cutoff_body)
        NetworkState.OFFLINE -> StatusSpec(Icons.Filled.Close, Red, R.string.st_offline, R.string.st_offline_body)
        NetworkState.UNKNOWN -> StatusSpec(Icons.Filled.Refresh, Color(0xFF9AA7C0), R.string.st_unknown, R.string.st_unknown_body)
    }
    Card(
        modifier = modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(containerColor = spec.color.copy(alpha = 0.12f))
    ) {
        Row(
            modifier = Modifier.padding(20.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Icon(spec.icon, contentDescription = null, tint = spec.color, modifier = Modifier.size(32.dp))
            Spacer(Modifier.size(16.dp))
            Column(Modifier.weight(1f)) {
                Text(stringResource(spec.titleRes), style = MaterialTheme.typography.titleMedium, color = spec.color)
                Text(stringResource(spec.bodyRes), style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurface)
            }
        }
    }
}

private data class StatusSpec(
    val icon: androidx.compose.ui.graphics.vector.ImageVector,
    val color: Color,
    val titleRes: Int,
    val bodyRes: Int
)

@Composable
private fun ConnectArea(
    phase: ConnectPhase,
    isUpdating: Boolean,
    hasConfig: Boolean,
    onTap: () -> Unit
) {
    when (phase) {
        ConnectPhase.CHECKING -> Column(horizontalAlignment = Alignment.CenterHorizontally) {
            CircularProgressIndicator()
            Spacer(Modifier.height(12.dp))
            Text(stringResource(R.string.connect_checking), style = MaterialTheme.typography.bodyMedium)
        }
        ConnectPhase.READY -> Column(horizontalAlignment = Alignment.CenterHorizontally) {
            Button(onClick = {}, enabled = false) { Text(stringResource(R.string.connect)) }
            Spacer(Modifier.height(8.dp))
            Text(
                stringResource(R.string.connect_tunnel_p2),
                style = MaterialTheme.typography.labelSmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                textAlign = TextAlign.Center
            )
        }
        ConnectPhase.TUNNEL_PENDING -> Column(horizontalAlignment = Alignment.CenterHorizontally) {
            CircularProgressIndicator()
            Spacer(Modifier.height(12.dp))
            Text(stringResource(R.string.connect_tunnel_pending), style = MaterialTheme.typography.bodyMedium)
        }
        ConnectPhase.IDLE -> Button(
            onClick = onTap,
            enabled = !isUpdating,
            modifier = Modifier.fillMaxWidth()
        ) {
            Text(stringResource(R.string.connect), style = MaterialTheme.typography.titleMedium)
        }
    }
}
