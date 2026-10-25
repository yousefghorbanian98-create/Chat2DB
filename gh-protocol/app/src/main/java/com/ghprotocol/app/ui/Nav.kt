package com.ghprotocol.app.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.navigation.NavGraph.Companion.findStartDestination
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import com.ghprotocol.app.R

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

private val MAIN_DOCK_ITEMS = listOf(
    VengeanceDockItem(Routes.HOME, "اتصال", R.drawable.ic_defyx_shield),
    VengeanceDockItem(Routes.RADAR, "رادار و مسیر", R.drawable.ic_vengeance_radar),
    VengeanceDockItem(Routes.LOGS, "لاگ زنده", R.drawable.ic_vengeance_terminal),
    VengeanceDockItem(Routes.HUB, "کانفیگ و ابزار", R.drawable.ic_vengeance_layers)
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

    Box(
        modifier = modifier
            .fillMaxSize()
            .background(DefyxColors.TopGradientStandby)
            .statusBarsPadding()
            .navigationBarsPadding()
    ) {
        NavHost(
            navController = nav,
            startDestination = Routes.HOME,
            modifier = Modifier
                .fillMaxSize()
                .padding(bottom = 78.dp)
        ) {
            composable(Routes.HOME) {
                HomeScreen(
                    viewModel = viewModel,
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
            composable(Routes.CONFIG) {
                ConfigHubScreen(
                    viewModel = viewModel,
                    onOpenQr = { nav.navigate(Routes.QR) },
                    onOpenGuide = { nav.navigate(Routes.GUIDE) },
                    onOpenSettings = { nav.navigate(Routes.SETTINGS) },
                    onOpenAbout = { nav.navigate(Routes.ABOUT) }
                )
            }
            composable(Routes.SCANNER) { RadarScreen(viewModel = viewModel) }
            composable(Routes.BALANCER) { RadarScreen(viewModel = viewModel) }
            composable(Routes.PREP) {
                ConfigHubScreen(
                    viewModel = viewModel,
                    onOpenQr = { nav.navigate(Routes.QR) },
                    onOpenGuide = { nav.navigate(Routes.GUIDE) },
                    onOpenSettings = { nav.navigate(Routes.SETTINGS) },
                    onOpenAbout = { nav.navigate(Routes.ABOUT) }
                )
            }
            composable(Routes.GUIDE) { GuideScreen() }
            composable(Routes.ABOUT) { AboutScreen() }
            composable(Routes.QR) { QrScreen() }
            composable(Routes.SETTINGS) { SettingsScreen() }
        }

        // Floating VengeanceUI GlassDock at the bottom of the screen
        VengeanceGlassDock(
            items = MAIN_DOCK_ITEMS,
            currentRoute = when (currentRoute) {
                Routes.SCANNER, Routes.BALANCER -> Routes.RADAR
                Routes.CONFIG, Routes.PREP, Routes.GUIDE, Routes.QR, Routes.SETTINGS, Routes.ABOUT -> Routes.HUB
                else -> currentRoute
            },
            onSelect = { switchTab(it) },
            modifier = Modifier.align(Alignment.BottomCenter)
        )
    }
}
