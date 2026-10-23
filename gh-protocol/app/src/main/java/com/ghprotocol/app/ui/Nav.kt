package com.ghprotocol.app.ui

import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController

object Routes {
    const val HOME = "home"
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

@Composable
fun GhNavHost(
    modifier: Modifier = Modifier,
    viewModel: HomeViewModel
) {
    val nav = rememberNavController()
    NavHost(navController = nav, startDestination = Routes.HOME, modifier = modifier) {
        composable(Routes.HOME) {
            HomeScreen(
                viewModel = viewModel,
                onOpenConfig = { nav.navigate(Routes.CONFIG) },
                onOpenGuide = { nav.navigate(Routes.GUIDE) },
                onOpenQr = { nav.navigate(Routes.QR) },
                onOpenScanner = { nav.navigate(Routes.SCANNER) },
                onOpenBalancer = { nav.navigate(Routes.BALANCER) },
                onOpenPrep = { nav.navigate(Routes.PREP) },
                onOpenSettings = { nav.navigate(Routes.SETTINGS) }
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
