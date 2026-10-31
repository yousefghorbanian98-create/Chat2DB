package com.ghprotocol.app

import android.app.Application
import android.os.Looper
import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.ui.platform.LocalLayoutDirection
import androidx.compose.ui.unit.LayoutDirection
import androidx.test.core.app.ApplicationProvider
import com.github.takahirom.roborazzi.ExperimentalRoborazziApi
import com.github.takahirom.roborazzi.RoborazziComposeCaptureOption
import com.github.takahirom.roborazzi.RoborazziComposeOptions
import com.github.takahirom.roborazzi.RoborazziOptions
import com.github.takahirom.roborazzi.RoborazziRule
import com.github.takahirom.roborazzi.ThresholdValidator
import com.github.takahirom.roborazzi.captureRoboImage
import com.ghprotocol.app.domain.NetworkMonitor
import com.ghprotocol.app.domain.NetworkState
import com.ghprotocol.app.domain.ProbeResult
import com.ghprotocol.app.domain.Probes
import com.ghprotocol.app.domain.Prober
import com.ghprotocol.app.ui.AboutScreen
import com.ghprotocol.app.ui.ConfigHubScreen
import com.ghprotocol.app.ui.FirstRunScreen
import com.ghprotocol.app.ui.GuideScreen
import com.ghprotocol.app.ui.HomeScreen
import com.ghprotocol.app.ui.HomeViewModel
import com.ghprotocol.app.ui.QrScreen
import com.ghprotocol.app.ui.RadarScreen
import com.ghprotocol.app.ui.SettingsScreen
import com.ghprotocol.app.ui.theme.GhProtocolTheme
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.Shadows.shadowOf
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode

/** Deterministic prober: first N urls of each set answer OK (no network). */
class InstantProber(private val intlOk: Int, private val domOk: Int) : Prober {
    override suspend fun probe(url: String, timeoutMs: Int): ProbeResult {
        val inDom = url in Probes.DOMESTIC
        val idx = if (inDom) Probes.DOMESTIC.indexOf(url) else Probes.INTERNATIONAL.indexOf(url)
        val okCount = if (inDom) domOk else intlOk
        return ProbeResult(url, ok = idx < okCount, latencyMs = if (idx < okCount) 42 else -1)
    }
}

private const val SEED_JSON = """
[
  {
    "remarks": "Serverless-v52-fragA",
    "version": {"min": "26.6.27"},
    "inbounds": [{"tag": "mixed-in", "port": 10808, "protocol": "mixed"}],
    "outbounds": [{"tag": "tcp-fragment"}, {"tag": "tcp-fragment-tls"}, {"tag": "udp-noises"}, {"tag": "dns"}]
  },
  {
    "remarks": "Serverless-v52-fragB",
    "version": {"min": "26.6.27"},
    "inbounds": [{"tag": "mixed-in", "port": 10808, "protocol": "mixed"}],
    "outbounds": [{"tag": "tcp-fragment"}]
  }
]
"""

/** G1 golden: 12 pages x 2 themes x (360x640 + 1080x1920), RTL, 0.5% pixel threshold.
 *
 *  Pages: home_connected, home_degraded, home_cutoff, first_run, settings, config,
 *  scanner, balancer, prep, guide, about, qr.
 *
 *  Modes (gradle tasks, see .github/workflows/gh-protocol.yml):
 *   - record: :app:recordRoborazziDebug  (produces references in app/src/test/snapshots)
 *   - verify: :app:verifyRoborazziDebug  (compares, fails beyond 0.5%)
 */
@RunWith(RobolectricTestRunner::class)
@OptIn(ExperimentalRoborazziApi::class)
class GoldenScreensTest {

    @get:Rule
    val roborazziRule = RoborazziRule(
        options = RoborazziRule.Options(
            roborazziOptions = RoborazziOptions(
                compareOptions = RoborazziOptions.CompareOptions(resultValidator = ThresholdValidator(0.005f))
            )
        )
    )

    // settle before each capture: async QR bitmap, Vazir font load, layout
    private val composeOptions = RoborazziComposeOptions {
        addOption(object : RoborazziComposeCaptureOption {
            override fun beforeCapture() {
                Thread.sleep(700)
                shadowOf(Looper.getMainLooper()).idle()
            }
            override fun afterCapture() {}
        })
    }

    private fun seedCache() {
        val app = ApplicationProvider.getApplicationContext<Application>()
        java.io.File(app.filesDir, "subscription.json").writeText(SEED_JSON)
        java.io.File(app.filesDir, "subscription.meta")
            .writeText((System.currentTimeMillis() - 60_000).toString())
    }

    private fun homeVm(intl: Int, dom: Int): HomeViewModel {
        val app = ApplicationProvider.getApplicationContext<Application>()
        val vm = HomeViewModel(app, monitor = NetworkMonitor(InstantProber(intl, dom), intervalMs = 200))
        // wait for the deterministic first probe pass (no network involved)
        var guard = 0
        while (vm.ui.value.network == NetworkState.UNKNOWN && guard < 300) {
            shadowOf(Looper.getMainLooper()).idle()
            Thread.sleep(5)
            guard++
        }
        return vm
    }

    @Composable
    private fun themed(dark: Boolean, content: @Composable () -> Unit) =
        CompositionLocalProvider(LocalLayoutDirection provides LayoutDirection.Rtl) {
            GhProtocolTheme(forceDark = dark) { content() }
        }

    private fun home(name: String, intl: Int, dom: Int, size: String) {
        seedCache()
        val vm = homeVm(intl, dom)
        captureRoboImage("${name}_${size}_light.png", roborazziComposeOptions = composeOptions) {
            themed(false) { HomeScreen(viewModel = vm) }
        }
        captureRoboImage("${name}_${size}_dark.png", roborazziComposeOptions = composeOptions) {
            themed(true) { HomeScreen(viewModel = vm) }
        }
    }

    private fun plain(name: String, size: String, content: @Composable () -> Unit) {
        seedCache()
        captureRoboImage("${name}_${size}_light.png", roborazziComposeOptions = composeOptions) {
            themed(false) { content() }
        }
        captureRoboImage("${name}_${size}_dark.png", roborazziComposeOptions = composeOptions) {
            themed(true) { content() }
        }
    }

    // --- 360x640 ---
    @Test @Config(qualifiers = "w360dp-h640dp") @GraphicsMode(GraphicsMode.Mode.NATIVE)
    fun home_connected_360x640() = home("home_connected", 3, 1, "360x640")

    @Test @Config(qualifiers = "w360dp-h640dp") @GraphicsMode(GraphicsMode.Mode.NATIVE)
    fun home_degraded_360x640() = home("home_degraded", 1, 2, "360x640")

    @Test @Config(qualifiers = "w360dp-h640dp") @GraphicsMode(GraphicsMode.Mode.NATIVE)
    fun home_cutoff_360x640() = home("home_cutoff", 0, 1, "360x640")

    @Test @Config(qualifiers = "w360dp-h640dp") @GraphicsMode(GraphicsMode.Mode.NATIVE)
    fun first_run_360x640() = plain("first_run", "360x640") { FirstRunScreen(onGetStarted = {}) }

    @Test @Config(qualifiers = "w360dp-h640dp") @GraphicsMode(GraphicsMode.Mode.NATIVE)
    fun settings_360x640() = plain("settings", "360x640") { SettingsScreen() }

    @Test @Config(qualifiers = "w360dp-h640dp") @GraphicsMode(GraphicsMode.Mode.NATIVE)
    fun config_360x640() = plain("config", "360x640") { ConfigHubScreen(viewModel = homeVm(3, 1)) }

    @Test @Config(qualifiers = "w360dp-h640dp") @GraphicsMode(GraphicsMode.Mode.NATIVE)
    fun scanner_360x640() = plain("scanner", "360x640") { RadarScreen(viewModel = homeVm(3, 1)) }

    @Test @Config(qualifiers = "w360dp-h640dp") @GraphicsMode(GraphicsMode.Mode.NATIVE)
    fun balancer_360x640() = plain("balancer", "360x640") { RadarScreen(viewModel = homeVm(3, 1)) }

    @Test @Config(qualifiers = "w360dp-h640dp") @GraphicsMode(GraphicsMode.Mode.NATIVE)
    fun prep_360x640() = plain("prep", "360x640") { ConfigHubScreen(viewModel = homeVm(3, 1)) }

    @Test @Config(qualifiers = "w360dp-h640dp") @GraphicsMode(GraphicsMode.Mode.NATIVE)
    fun guide_360x640() = plain("guide", "360x640") { GuideScreen() }

    @Test @Config(qualifiers = "w360dp-h640dp") @GraphicsMode(GraphicsMode.Mode.NATIVE)
    fun about_360x640() = plain("about", "360x640") { AboutScreen() }

    @Test @Config(qualifiers = "w360dp-h640dp") @GraphicsMode(GraphicsMode.Mode.NATIVE)
    fun qr_360x640() = plain("qr", "360x640") { QrScreen() }

    // --- 1080x1920 ---
    @Test @Config(qualifiers = "w1080dp-h1920dp") @GraphicsMode(GraphicsMode.Mode.NATIVE)
    fun home_connected_1080x1920() = home("home_connected", 3, 1, "1080x1920")

    @Test @Config(qualifiers = "w1080dp-h1920dp") @GraphicsMode(GraphicsMode.Mode.NATIVE)
    fun home_degraded_1080x1920() = home("home_degraded", 1, 2, "1080x1920")

    @Test @Config(qualifiers = "w1080dp-h1920dp") @GraphicsMode(GraphicsMode.Mode.NATIVE)
    fun home_cutoff_1080x1920() = home("home_cutoff", 0, 1, "1080x1920")

    @Test @Config(qualifiers = "w1080dp-h1920dp") @GraphicsMode(GraphicsMode.Mode.NATIVE)
    fun first_run_1080x1920() = plain("first_run", "1080x1920") { FirstRunScreen(onGetStarted = {}) }

    @Test @Config(qualifiers = "w1080dp-h1920dp") @GraphicsMode(GraphicsMode.Mode.NATIVE)
    fun settings_1080x1920() = plain("settings", "1080x1920") { SettingsScreen() }

    @Test @Config(qualifiers = "w1080dp-h1920dp") @GraphicsMode(GraphicsMode.Mode.NATIVE)
    fun config_1080x1920() = plain("config", "1080x1920") { ConfigHubScreen(viewModel = homeVm(3, 1)) }

    @Test @Config(qualifiers = "w1080dp-h1920dp") @GraphicsMode(GraphicsMode.Mode.NATIVE)
    fun scanner_1080x1920() = plain("scanner", "1080x1920") { RadarScreen(viewModel = homeVm(3, 1)) }

    @Test @Config(qualifiers = "w1080dp-h1920dp") @GraphicsMode(GraphicsMode.Mode.NATIVE)
    fun balancer_1080x1920() = plain("balancer", "1080x1920") { RadarScreen(viewModel = homeVm(3, 1)) }

    @Test @Config(qualifiers = "w1080dp-h1920dp") @GraphicsMode(GraphicsMode.Mode.NATIVE)
    fun prep_1080x1920() = plain("prep", "1080x1920") { ConfigHubScreen(viewModel = homeVm(3, 1)) }

    @Test @Config(qualifiers = "w1080dp-h1920dp") @GraphicsMode(GraphicsMode.Mode.NATIVE)
    fun guide_1080x1920() = plain("guide", "1080x1920") { GuideScreen() }

    @Test @Config(qualifiers = "w1080dp-h1920dp") @GraphicsMode(GraphicsMode.Mode.NATIVE)
    fun about_1080x1920() = plain("about", "1080x1920") { AboutScreen() }

    @Test @Config(qualifiers = "w1080dp-h1920dp") @GraphicsMode(GraphicsMode.Mode.NATIVE)
    fun qr_1080x1920() = plain("qr", "1080x1920") { QrScreen() }
}
