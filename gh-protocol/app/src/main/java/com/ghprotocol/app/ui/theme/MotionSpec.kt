package com.ghprotocol.app.ui.theme

import android.content.Context
import android.provider.Settings

/**
 * P3 Motion specification (`design-motion-principles`, Emil Kowalski lens):
 * - All transitions <= 300ms (default 200ms).
 * - Respects Android system `ANIMATOR_DURATION_SCALE == 0f` (`reduced-motion`).
 * - Pure scale calculation is unit-tested on JVM.
 */
object MotionSpec {
    const val DEFAULT_DURATION_MS = 200
    const val MAX_DURATION_MS = 300

    fun resolveDurationMs(scale: Float, baseMs: Int = DEFAULT_DURATION_MS): Int {
        if (scale <= 0f) return 0
        val clampedBase = baseMs.coerceIn(0, MAX_DURATION_MS)
        return (clampedBase * scale).toInt().coerceIn(0, MAX_DURATION_MS)
    }

    fun isReducedMotion(context: Context): Boolean = try {
        val scale = Settings.Global.getFloat(
            context.contentResolver,
            Settings.Global.ANIMATOR_DURATION_SCALE,
            1f
        )
        scale <= 0f
    } catch (_: Exception) {
        false
    }

    fun durationMs(context: Context, baseMs: Int = DEFAULT_DURATION_MS): Int = try {
        val scale = Settings.Global.getFloat(
            context.contentResolver,
            Settings.Global.ANIMATOR_DURATION_SCALE,
            1f
        )
        resolveDurationMs(scale, baseMs)
    } catch (_: Exception) {
        baseMs.coerceIn(0, MAX_DURATION_MS)
    }
}
