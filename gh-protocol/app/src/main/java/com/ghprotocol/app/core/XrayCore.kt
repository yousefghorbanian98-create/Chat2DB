package com.ghprotocol.app.core

import android.content.Context
import java.io.File
import java.net.InetSocketAddress
import java.net.Socket
import java.util.concurrent.TimeUnit
import java.util.concurrent.atomic.AtomicBoolean
import java.util.concurrent.atomic.AtomicInteger

/**
 * F-2: Xray-core lifecycle implementing [TunnelEngine].
 *
 * Android 10+ enforces W^X (b/112357170): files in the app's own data dir are
 * labelled `app_data_file`, and `execute_no_trans` on them is denied for
 * targetSdk > 28. The read-only native library dir (`applicationInfo.nativeLibraryDir`)
 * is explicitly executable (`apk_data_file`). We ship Xray as
 * `jniLibs/<abi>/libxraycore.so` (`useLegacyPackaging = true`) and exec it directly.
 *
 * Geo data (geoip.dat / geosite.dat) stays in assets and is extracted to
 * `filesDir/xray` (`XRAY_LOCATION_ASSET`).
 */
class XrayCore(private val context: Context) : TunnelEngine {

    override val name: String = "xray-core"

    /** Runtime dir for geo data + logs (app_data_file — data only, never exec'd). */
    private val dir = File(context.filesDir, "xray")

    /**
     * The bundled core. Normally inside the read-only native library dir;
     * falls back to filesDir for environments without one (Robolectric).
     */
    private val binary: File = run {
        val nativeDir = context.applicationInfo?.nativeLibraryDir
        if (nativeDir.isNullOrEmpty()) File(context.filesDir, "libxraycore.so")
        else File(nativeDir, "libxraycore.so")
    }

    @Volatile
    private var process: Process? = null
    private val shouldRun = AtomicBoolean(false)
    private val restartAttempts = AtomicInteger(0)

    data class Info(val path: File, val version: String)

    /** Verify the bundled core + geo assets -> report version. */
    override fun ensureInstalled(): Result<Info> {
        return try {
            dir.mkdirs()
            extractGeoAssets()
            if (!binary.exists()) {
                return Result.failure(IllegalStateException("bundled core missing at ${binary.path}"))
            }
            val v = version()
            if (v == "unknown") return Result.failure(IllegalStateException("Xray version unreadable"))
            Result.success(Info(binary, v))
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    /** `Xray version` -> "26.10.21" (parsed from stdout or stderr). */
    override fun version(): String = try {
        val p = Runtime.getRuntime().exec(arrayOf(binary.absolutePath, "version"), null, dir)
        val out = p.inputStream.bufferedReader().use { it.readText() }
        val err = p.errorStream.bufferedReader().use { it.readText() }
        if (!p.waitFor(10, TimeUnit.SECONDS)) p.destroyForcibly()
        val text = if (out.isNotBlank()) out else err
        val candidate = text.lineSequence().firstOrNull { it.contains("Xray", ignoreCase = true) }
            ?: text.trim().lineSequence().firstOrNull().orEmpty()
        Regex("""(\d+\.\d+\.\d+)""").find(candidate)?.groupValues?.get(1) ?: "unknown"
    } catch (e: Exception) {
        "unknown"
    }

    override fun isRunning(): Boolean = process?.isAlive == true

    /** Rule #8: Real socket health check on loopback mixed-in port (default 10808). */
    override fun isHealthy(port: Int, timeoutMs: Int): Boolean {
        if (!isRunning()) return false
        return try {
            Socket().use { s ->
                s.connect(InetSocketAddress("127.0.0.1", port), timeoutMs)
                true
            }
        } catch (_: Exception) {
            false
        }
    }

    /**
     * F-2/F-3: start the core with the given config and attach a watchdog thread
     * with bounded exponential-backoff restart on unexpected exit.
     */
    override fun start(configPath: File): Result<Process> {
        return try {
            if (isRunning()) return Result.failure(IllegalStateException("Xray already running"))
            if (!ensureInstalled().isSuccess) return Result.failure(IllegalStateException("Xray not installed"))
            shouldRun.set(true)
            restartAttempts.set(0)
            val p = spawnProcess(configPath)
            process = p
            startWatchdog(p, configPath)
            Result.success(p)
        } catch (e: Exception) {
            shouldRun.set(false)
            Result.failure(e)
        }
    }

    private fun spawnProcess(configPath: File): Process {
        val pb = ProcessBuilder(listOf(binary.absolutePath, "run", "-c", configPath.absolutePath))
        val env = pb.environment()
        env["XRAY_LOCATION_ASSET"] = dir.absolutePath
        env["xray.location.asset"] = dir.absolutePath
        pb.redirectOutput(ProcessBuilder.Redirect.appendTo(File(dir, "xray-out.log")))
        pb.redirectError(ProcessBuilder.Redirect.appendTo(File(dir, "xray-err.log")))
        return pb.start()
    }

    private fun startWatchdog(initial: Process, configPath: File) {
        Thread({
            var current = initial
            while (shouldRun.get()) {
                val rc = try { current.waitFor() } catch (_: InterruptedException) { -1 }
                android.util.Log.w("GhDiag", "xray exited rc=$rc shouldRun=${shouldRun.get()}")
                if (!shouldRun.get() || rc == 0) break
                val attempt = restartAttempts.incrementAndGet()
                if (attempt > 4) {
                    android.util.Log.e("GhDiag", "xray exceeded max restart attempts ($attempt)")
                    shouldRun.set(false)
                    break
                }
                val backoffMs = (1000L shl (attempt - 1)).coerceAtMost(16_000L)
                try { Thread.sleep(backoffMs) } catch (_: InterruptedException) { break }
                if (!shouldRun.get()) break
                try {
                    current = spawnProcess(configPath)
                    process = current
                    android.util.Log.i("GhDiag", "xray restarted (attempt=$attempt)")
                } catch (e: Exception) {
                    android.util.Log.e("GhDiag", "xray restart failed: ${e.message}")
                    break
                }
            }
        }, "xray-watchdog").apply { isDaemon = true; start() }
    }

    /** F-4: stop < 3s (kill + wait with timeout). */
    override fun stop() {
        shouldRun.set(false)
        process?.let {
            it.destroy()
            try { it.waitFor(2, TimeUnit.SECONDS) } catch (_: InterruptedException) {}
            if (it.isAlive) it.destroyForcibly()
        }
        process = null
    }

    fun close() = stop()

    /** Copy geoip.dat / geosite.dat (data only) from assets on first use. */
    private fun extractGeoAssets() {
        val names = context.assets.list("xray") ?: emptyArray()
        for (name in names) {
            if (!name.endsWith(".dat")) continue
            val out = File(dir, name)
            if (out.length() > 0) continue
            context.assets.open("xray/$name").use { input -> out.outputStream().use { input.copyTo(it) } }
        }
    }
}

/** F-2: semver-ish check against the subscription's required minimum (26.6.27). */
fun xrayVersionOk(actual: String, min: String): Boolean {
    val a = actual.split('.', '-').mapNotNull { it.toIntOrNull() }
    val m = min.split('.', '-').mapNotNull { it.toIntOrNull() }
    if (a.isEmpty() || m.isEmpty()) return false
    for (i in 0 until maxOf(a.size, m.size)) {
        val x = a.getOrNull(i) ?: 0
        val y = m.getOrNull(i) ?: 0
        if (x != y) return x > y
    }
    return true
}
