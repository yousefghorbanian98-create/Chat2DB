package com.ghprotocol.app.core

import android.content.Context
import java.io.File
import java.util.concurrent.TimeUnit

/**
 * F-2: Xray-core lifecycle.
 *
 * Android 10+ enforces W^X (b/112357170): files in the app's own data dir are
 * labelled `app_data_file`, and `execute_no_trans` on them is denied for
 * targetSdk > 28 — so the classic "extract the Xray binary to filesDir and
 * Runtime.exec it" approach FAILS on modern Android
 * (`avc: denied { execute_no_trans } ... app_data_file`, seen on API 34 AOSP
 * and GMS images alike).
 *
 * The read-only native library dir (/data/app/.../lib/<abi>/,
 * `applicationInfo.nativeLibraryDir`) is explicitly executable. The official
 * XTLS/Xray-core Android build is therefore shipped as
 * `jniLibs/<abi>/libxraycore.so` — a real ELF executable with a `.so` name —
 * and the installer extracts it there (requires
 * `packaging.jniLibs.useLegacyPackaging = true`, see app/build.gradle.kts).
 * We exec that path directly.
 *
 * Geo data (geoip.dat / geosite.dat) is NOT code: it stays in assets and is
 * extracted to filesDir/xray, pointed at by XRAY_LOCATION_ASSET.
 */
class XrayCore(private val context: Context) {

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

    private var process: Process? = null

    data class Info(val path: File, val version: String)

    /** Verify the bundled core + geo assets -> report version. */
    fun ensureInstalled(): Result<Info> {
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
    fun version(): String = try {
        val p = Runtime.getRuntime().exec(arrayOf(binary.absolutePath, "version"), null, dir)
        val out = p.inputStream.bufferedReader().readText()
        val err = p.errorStream.bufferedReader().readText()
        if (!p.waitFor(10, TimeUnit.SECONDS)) p.destroyForcibly()
        val text = if (out.isNotBlank()) out else err
        val candidate = text.lineSequence().firstOrNull { it.contains("Xray", ignoreCase = true) }
            ?: text.trim().lineSequence().firstOrNull().orEmpty()
        Regex("""(\d+\.\d+\.\d+)""").find(candidate)?.groupValues?.get(1) ?: "unknown"
    } catch (e: Exception) {
        "unknown"
    }

    fun isRunning(): Boolean = process?.let { it.isAlive } ?: false

    /**
     * F-2/F-3: start the core with the given config (stderr -> filesDir/xray/xray-err.log).
     * Geo assets resolve from XRAY_LOCATION_ASSET (also the executable dir default).
     */
    fun start(configPath: File): Result<Process> {
        return try {
            if (isRunning()) return Result.failure(IllegalStateException("Xray already running"))
            if (!ensureInstalled().isSuccess) return Result.failure(IllegalStateException("Xray not installed"))
            val pb = ProcessBuilder(listOf(binary.absolutePath, "run", "-c", configPath.absolutePath))
            val env = pb.environment()
            env["XRAY_LOCATION_ASSET"] = dir.absolutePath
            env["xray.location.asset"] = dir.absolutePath
            pb.redirectError(ProcessBuilder.Redirect.appendTo(File(dir, "xray-err.log")))
            val p = pb.start()
            process = p
            Result.success(p)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    /** F-4: stop < 3s (kill + wait with timeout). */
    fun stop() {
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
