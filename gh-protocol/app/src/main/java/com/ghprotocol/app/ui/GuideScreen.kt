package com.ghprotocol.app.ui

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import com.ghprotocol.app.R

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun GuideScreen(modifier: Modifier = Modifier) {
    Scaffold(topBar = { TopAppBar(title = { Text(stringResource(R.string.guide)) }) }) { padding ->
        Column(
            modifier = modifier
                .fillMaxSize()
                .padding(padding)
                .verticalScroll(rememberScrollState())
                .padding(24.dp)
        ) {
            SectionTitle(stringResource(R.string.guide_steps))
            Item("1", stringResource(R.string.guide_step1_t), stringResource(R.string.guide_step1_b))
            Item("2", stringResource(R.string.guide_step2_t), stringResource(R.string.guide_step2_b))
            Item("3", stringResource(R.string.guide_step3_t), stringResource(R.string.guide_step3_b))
            Spacer(Modifier.height(12.dp))
            SectionTitle(stringResource(R.string.guide_tips))
            Item("•", stringResource(R.string.guide_tip1_t), stringResource(R.string.guide_tip1_b))
            Item("•", stringResource(R.string.guide_tip2_t), stringResource(R.string.guide_tip2_b))
            Item("•", stringResource(R.string.guide_tip3_t), stringResource(R.string.guide_tip3_b))
            Spacer(Modifier.height(16.dp))
            HorizontalDivider()
            Spacer(Modifier.height(16.dp))
            SectionTitle(stringResource(R.string.guide_alt_title))
            Text(stringResource(R.string.guide_alt_note), style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.outline)
            Spacer(Modifier.height(8.dp))
            Item("a", stringResource(R.string.alt_pro_t), stringResource(R.string.alt_pro_b))
            Item("b", stringResource(R.string.alt_sim_t), stringResource(R.string.alt_sim_b))
            Item("c", stringResource(R.string.alt_sat_t), stringResource(R.string.alt_sat_b))
            Item("d", stringResource(R.string.alt_tools_t), stringResource(R.string.alt_tools_b))
        }
    }
}

@Composable
private fun SectionTitle(text: String) {
    Text(text, style = MaterialTheme.typography.titleMedium, color = MaterialTheme.colorScheme.primary)
    Spacer(Modifier.height(8.dp))
}

@Composable
private fun Item(marker: String, title: String, body: String) {
    Column(Modifier.padding(vertical = 6.dp)) {
        Text("$marker. $title", style = MaterialTheme.typography.titleSmall)
        Text(body, style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
    }
}
