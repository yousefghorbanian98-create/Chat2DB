package com.ghprotocol.app.ui

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Check
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import com.ghprotocol.app.R
import com.ghprotocol.app.domain.SettingsStore

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SettingsScreen(modifier: Modifier = Modifier) {
    val context = LocalContext.current
    val store = remember { SettingsStore(context) }
    var theme by remember { mutableStateOf(store.theme) }
    var language by remember { mutableStateOf(store.language) }
    Scaffold(topBar = { TopAppBar(title = { Text(stringResource(R.string.settings)) }) }) { padding ->
        Column(
            modifier = modifier
                .fillMaxSize()
                .padding(padding)
                .padding(24.dp)
        ) {
            SectionTitle(stringResource(R.string.settings_theme))
            OptionRow(stringResource(R.string.opt_system), theme == "system") {
                theme = "system"; store.theme = "system"
            }
            OptionRow(stringResource(R.string.opt_light), theme == "light") {
                theme = "light"; store.theme = "light"
            }
            OptionRow(stringResource(R.string.opt_dark), theme == "dark") {
                theme = "dark"; store.theme = "dark"
            }
            Spacer(Modifier.height(20.dp))
            SectionTitle(stringResource(R.string.settings_language))
            OptionRow(stringResource(R.string.opt_system), language == "system") {
                language = "system"; store.language = "system"
            }
            OptionRow(stringResource(R.string.opt_fa), language == "fa") {
                language = "fa"; store.language = "fa"
            }
            OptionRow(stringResource(R.string.opt_en), language == "en") {
                language = "en"; store.language = "en"
            }
            Spacer(Modifier.height(20.dp))
            Text(
                stringResource(R.string.settings_note),
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.outline
            )
        }
    }
}

@Composable
private fun SectionTitle(text: String) {
    Text(text, style = MaterialTheme.typography.titleMedium, color = MaterialTheme.colorScheme.primary)
    Spacer(Modifier.height(8.dp))
}

@Composable
private fun OptionRow(label: String, selected: Boolean, onClick: () -> Unit) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clickable(onClick = onClick)
            .padding(vertical = 10.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Text(label, style = MaterialTheme.typography.bodyLarge, modifier = Modifier.weight(1f))
        if (selected) {
            Icon(Icons.Filled.Check, contentDescription = null, tint = MaterialTheme.colorScheme.primary)
        }
    }
}
