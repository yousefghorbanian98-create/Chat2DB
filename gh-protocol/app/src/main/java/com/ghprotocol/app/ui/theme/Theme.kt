package com.ghprotocol.app.ui.theme

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.ui.graphics.Color
import androidx.compose.runtime.Composable

private val DarkColors = darkColorScheme(
    primary = GhBlueDark,
    onPrimary = GhInk,
    secondary = GhBlue,
    background = GhInk,
    surface = GhInkSurface,
    onSurface = GhInkOn,
    onSurfaceVariant = GhInkOnVariant,
    outline = GhInkOutline
)

private val LightColors = lightColorScheme(
    primary = GhBlue,
    onPrimary = Color(0xFFFFFFFF),
    secondary = GhInk,
    background = GhLightBg,
    surface = GhLightBg,
    onSurface = GhLightOn,
    onSurfaceVariant = GhLightOnVariant,
    outline = GhLightOutline
)

@Composable
fun GhProtocolTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    forceDark: Boolean? = null,
    content: @Composable () -> Unit
) {
    val isDark = forceDark ?: darkTheme
    MaterialTheme(
        colorScheme = if (isDark) DarkColors else LightColors,
        typography = GhTypography,
        content = content
    )
}
