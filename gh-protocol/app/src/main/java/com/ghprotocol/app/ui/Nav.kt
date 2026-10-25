package com.ghprotocol.app.ui

import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.Info
import androidx.compose.material.icons.filled.Search
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material3.Icon
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.navigation.NavGraph.Companion.findStartDestination
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController

object Routes {
    const val HOME = "home"
    const val RADAR = "radar"
    const val LOGS = "logs"
    const val HUB = "hub"
    const val FIRST_RUN = "first-run"
    const val CONFIG = "config"
    const val GUIDE = "guide"
    const val SCANNER = "scanner"
    const val BALANCER = "balancer"
    const val PREP = "prep"
    const val ABOUT = "about"
    const val QR = "qr"
    const val SETTINGS = "settings"
}

private data class BottomTab(
    val route: String,
    val label: String,
    val icon: androidx.compose.ui.graphics.vector.ImageVector
)

private val MAIN_TABS = listOf(
    BottomTab(Routes.HOME, "اتصال", Icons.Filled.Home),
    BottomTab(Routes.RADAR, "رادار و مسیر", Icons.Filled.Search),
    BottomTab(Routes.LOGS, "لاگ زنده", Icons.Filled.Info),
    BottomTab(Routes.HUB, "کانفیگ و راهنما", Icons.Filled.Settings)
)

@Composable
fun GhNavHost(
    modifier: Modifier = Modifier,
    viewModel: HomeViewModel
) {
    val nav = rememberNavController()
    val backStack by nav.currentBackStackEntryAsState()
    val currentRoute = backStack?.destination?.route ?: Routes.HOME

    fun switchTab(route: String) {
        nav.navigate(route) {
            popUpTo(nav.graph.findStartDestination().id) {
                saveState = true
            }
            launchSingleTop = true
            restoreState = true
        }
    }

    Scaffold(
        modifier = modifier,
        bottomBar = {
            NavigationBar {
                MAIN_TABS.forEach { tab ->
                    val selected = currentRoute == tab.route
                    NavigationBarItem(
                        selected = selected,
                        onClick = { switchTab(tab.route) },
                        icon = { Icon(tab.icon, contentDescription = tab.label) },
                        label = { Text(tab.label) }
                    )
                }
            }
        }
    ) { innerPadding ->
        NavHost(
            navController = nav,
            startDestination = Routes.HOME,
            modifier = Modifier.padding(innerPadding)
        ) {
            composable(Routes.HOME) {
                HomeScreen(
                    viewModel = viewModel,
                    showEnhancedDashboard = true,
                    onOpenConfig = { switchTab(Routes.HUB) },
                    onOpenGuide = { nav.navigate(Routes.GUIDE) },
                    onOpenQr = { nav.navigate(Routes.QR) },
                    onOpenScanner = { switchTab(Routes.RADAR) },
                    onOpenBalancer = { switchTab(Routes.RADAR) },
                    onOpenPrep = { switchTab(Routes.HUB) },
                    onOpenSettings = { nav.navigate(Routes.SETTINGS) },
                    onOpenLogs = { switchTab(Routes.LOGS) }
                )
            }
            composable(Routes.RADAR) {
                RadarScreen(viewModel = viewModel)
            }
            composable(Routes.LOGS) {
                LiveLogScreen(viewModel = viewModel)
            }
            composable(Routes.HUB) {
                ConfigHubScreen(
                    viewModel = viewModel,
                    onOpenQr = { nav.navigate(Routes.QR) },
                    onOpenGuide = { nav.navigate(Routes.GUIDE) },
                    onOpenSettings = { nav.navigate(Routes.SETTINGS) },
                    onOpenAbout = { nav.navigate(Routes.ABOUT) }
                )
            }
            composable(Routes.FIRST_RUN) { FirstRunScreen(onGetStarted = { nav.popBackStack() }) }
            composable(Routes.CONFIG) { ConfigScreen(viewModel = viewModel) }
            composable(Routes.GUIDE) { GuideScreen() }
            composable(Routes.SCANNER) { ScannerScreen() }
            composable(Routes.BALANCER) { BalancerScreen() }
            composable(Routes.PREP) { PrepScreen() }
            composable(Routes.ABOUT) { AboutScreen() }
            composable(Routes.QR) { QrScreen() }
            composable(Routes.SETTINGS) { SettingsScreen() }
        }
    }
}
