package com.ghprotocol.app.core

import android.content.Context
import java.io.File

/**
 * F-2: Xray-core lifecycle.
 * The official android binary (MPL-2.0, XTLS/Xray-core) ships as an APK asset
 * (downloaded + SHA-256 verified in CI). At runtime it is extracted to
 * filesDir/xray and executed as a child process.
 */
class XrayCore(private val context: Context) {

    private val dir = File(context.filesDir, "xray")

    private val assetAbi: String = run {
        val arch = android.os.Build.SUPPORTED_ABIS.firstOrNull().orEmpty()
        when (arch) {
            "arm64-v8a" -> "arm64-v8a"
            "armeabi-v7a", "armeabi" -> "arm64-v8a" // 32-bit devices: no 32-bit release; fail at version check
            else -> "amd64" // x86_64 emulators
        }
    }

    private val binary = File(dir, "Xray")

    private var process: Process? = null

    data class Info(val path: File, val version: String)

    /** Extract asset -> verify executable -> report version. */
    fun ensureInstalled(): Result<Info> {
        return try {
            if (!binary.exists()) {
                dir.mkdirs()
                extractAssets()
            }
            if (!binary.exists()) return Result.failure(IllegalStateException("Xray binary missing after extraction"))
            binary.setExecutable(true, false)
            val v = version()
            if (v == "unknown") return Result.failure(IllegalStateException("Xray version unreadable"))
            Result.success(Info(binary, v))
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    /** `Xray version` -> "Xray 26.10.21 (android...) ..." */
    fun version(): String = try {
        val p = Runtime.getRuntime().exec(arrayOf(binary.absolutePath, "version"), null, dir)
        val out = p.inputStream.bufferedReader().readText().trim().lineSequence().firstOrNull().orEmpty()
        p.waitFor()
        out.substringAfter("Xray ").substringBefore(' ').ifBlank { "unknown" }
    } catch (e: Exception) {
        "unknown"
    }

    fun isRunning(): Boolean = process?.let { it.isAlive } ?: false

    /**
     * F-2/F-3: start the core with the given config (stderr -> filesDir/xray/xray-err.log).
     * Android's ProcessBuilder has no directory(); Xray resolves geo assets from the
     * XRAY_LOCATION_ASSET env (falls back to the executable dir — same place here).
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
            try { it.waitFor(2, java.util.concurrent.TimeUnit.SECONDS) } catch (_: InterruptedException) {}
            if (it.isAlive) it.destroyForcibly()
        }
        process = null
    }

    fun close() = stop()

    private fun extractAssets() {
        val names = context.assets.list("xray") ?: emptyArray()
        for (name in names) {
            val out = File(dir, name)
            context.assets.open("xray/$name").use { input -> out.outputStream().use { input.copyTo(it) } }
        }
        val abiBinary = File(dir, "Xray-$assetAbi")
        if (abiBinary.exists() && !binary.exists()) {
            abiBinary.renameTo(binary)
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
