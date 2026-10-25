package com.ghprotocol.app.ui

import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.core.LinearEasing
import androidx.compose.animation.core.RepeatMode
import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.rememberInfiniteTransition
import androidx.compose.animation.core.spring
import androidx.compose.animation.core.tween
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.interaction.collectIsPressedAsState
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.composed
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.scale
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.drawscope.rotate
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.ghprotocol.app.core.TunnelLogBuffer
import com.ghprotocol.app.core.TunnelTelemetry
import com.ghprotocol.app.ui.theme.GhBlue
import com.ghprotocol.app.ui.theme.GhGreen
import com.ghprotocol.app.ui.theme.MotionSpec
import kotlin.math.PI
import kotlin.math.cos
import kotlin.math.sin

private val OrbCyan = Color(0xFF22D3EE)
private val OrbEmerald = Color(0xFF34D399)
private val OrbAmber = Color(0xFFF5A524)
private val OrbRed = Color(0xFFE5484D)

/**
 * Framer Motion / 21st.dev tactile spring press modifier.
 * Compresses to [pressedScale] on touch-down and rebounds with physical spring dynamics.
 */
fun Modifier.springPressClickable(
    enabled: Boolean = true,
    pressedScale: Float = 0.94f,
    onClick: () -> Unit
): Modifier = composed {
    val context = LocalContext.current
    val interactionSource = remember { MutableInteractionSource() }
    val isPressed by interactionSource.collectIsPressedAsState()
    val reduced = MotionSpec.isReducedMotion(context)
    val scale by animateFloatAsState(
        targetValue = if (isPressed && !reduced) pressedScale else 1f,
        animationSpec = spring(dampingRatio = 0.65f, stiffness = 420f),
        label = "spring-press"
    )
    this
        .scale(scale)
        .clickable(
            interactionSource = interactionSource,
            indication = null,
            enabled = enabled,
            onClick = onClick
        )
}

/**
 * Hero Orb Button combining:
 * - Particles Casberry orbital particle field (18 GPU-accelerated Canvas particles)
 * - Vengeance UI rotating SweepGradient energy border
 * - Framer Motion tactile spring press
 */
@Composable
fun OrbParticleHeroButton(
    phase: ConnectPhase,
    verifiedPingMs: Int?,
    isAutoHealing: Boolean,
    stepIndex: Int,
    onTapConnect: () -> Unit,
    onTapDisconnect: () -> Unit,
    modifier: Modifier = Modifier
) {
    val context = LocalContext.current
    val reduced = MotionSpec.isReducedMotion(context)
    val isConnected = phase == ConnectPhase.CONNECTED
    val isBusy = phase == ConnectPhase.CHECKING ||
        phase == ConnectPhase.PREPARING ||
        phase == ConnectPhase.TUNNELING ||
        isAutoHealing

    val primaryColor by animateColorAsState(
        targetValue = when {
            isConnected && verifiedPingMs != null -> OrbEmerald
            isConnected -> GhBlue
            isBusy -> OrbAmber
            phase == ConnectPhase.FAILED -> OrbRed
            else -> OrbCyan
        },
        animationSpec = MotionSpec.tweenMs(context, 250),
        label = "orb-primary-color"
    )

    val infinite = rememberInfiniteTransition(label = "orb-infinite")
    val angleDeg by infinite.animateFloat(
        initialValue = 0f,
        targetValue = if (reduced) 0f else 360f,
        animationSpec = infiniteRepeatable(
            animation = tween(durationMillis = if (isBusy) 2200 else 5600, easing = LinearEasing),
            repeatMode = RepeatMode.Restart
        ),
        label = "orb-angle"
    )
    val pulse by infinite.animateFloat(
        initialValue = 0.92f,
        targetValue = if (reduced) 0.95f else 1.08f,
        animationSpec = infiniteRepeatable(
            animation = tween(durationMillis = if (isBusy) 850 else 1800, easing = LinearEasing),
            repeatMode = RepeatMode.Reverse
        ),
        label = "orb-pulse"
    )

    Box(
        modifier = modifier
            .size(220.dp)
            .springPressClickable(pressedScale = 0.93f) {
                if (isConnected) onTapDisconnect() else onTapConnect()
            },
        contentAlignment = Alignment.Center
    ) {
        Canvas(modifier = Modifier.fillMaxSize()) {
            val center = Offset(size.width / 2f, size.height / 2f)
            val baseRadius = size.minDimension * 0.34f

            // 1. Outer sonar aura rings
            drawCircle(
                color = primaryColor.copy(alpha = 0.08f),
                radius = baseRadius * 1.32f * pulse,
                center = center
            )
            drawCircle(
                color = primaryColor.copy(alpha = 0.14f),
                radius = baseRadius * 1.16f * (2f - pulse),
                center = center,
                style = Stroke(width = 1.5.dp.toPx())
            )

            // 2. Particles Casberry: 18 orbital glowing particles across 3 rings
            val particleCount = 18
            val radBase = (angleDeg * PI / 180.0).toFloat()
            for (i in 0 until particleCount) {
                val ring = i % 3
                val orbitR = baseRadius * (1.08f + ring * 0.11f)
                val speedMul = if (ring == 1) -1.2f else (1f + ring * 0.35f)
                val theta = radBase * speedMul + (i * (2.0 * PI / particleCount)).toFloat()
                val px = center.x + cos(theta) * orbitR
                val py = center.y + sin(theta) * orbitR
                val dotRadius = (if (ring == 0) 3.2.dp else if (ring == 1) 2.4.dp else 1.8.dp).toPx()
                val alpha = if (isConnected || isBusy) 0.85f - ring * 0.18f else 0.55f - ring * 0.12f
                drawCircle(
                    color = primaryColor.copy(alpha = alpha.coerceIn(0.15f, 0.95f)),
                    radius = dotRadius,
                    center = Offset(px, py)
                )
            }

            // 3. Vengeance UI rotating SweepGradient energy border
            rotate(degrees = angleDeg, pivot = center) {
                drawCircle(
                    brush = Brush.sweepGradient(
                        colors = listOf(
                            primaryColor.copy(alpha = 0.15f),
                            primaryColor.copy(alpha = 0.95f),
                            OrbCyan.copy(alpha = 0.75f),
                            primaryColor.copy(alpha = 0.15f)
                        ),
                        center = center
                    ),
                    radius = baseRadius,
                    center = center,
                    style = Stroke(width = 5.dp.toPx(), cap = StrokeCap.Round)
                )
            }
        }

        // 4. Inner glassmorphic core orb
        Box(
            modifier = Modifier
                .size(144.dp)
                .clip(CircleShape)
                .background(
                    Brush.radialGradient(
                        colors = listOf(
                            primaryColor.copy(alpha = 0.26f),
                            primaryColor.copy(alpha = 0.08f)
                        )
                    )
                )
                .border(1.5.dp, primaryColor.copy(alpha = 0.55f), CircleShape)
                .padding(14.dp),
            contentAlignment = Alignment.Center
        ) {
            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                Text(
                    text = when {
                        isConnected -> "قطع اتصال"
                        isBusy -> "در حال اتصال"
                        phase == ConnectPhase.FAILED -> "تلاش مجدد"
                        else -> "اتصال"
                    },
                    style = MaterialTheme.typography.titleLarge,
                    fontWeight = FontWeight.ExtraBold,
                    color = primaryColor,
                    textAlign = TextAlign.Center
                )
                Spacer(Modifier.height(4.dp))
                Text(
                    text = when {
                        isConnected && verifiedPingMs != null -> "${verifiedPingMs} ms · تاییدشده ✓"
                        isConnected && isAutoHealing -> "خودترمیمی (Auto-Heal)..."
                        isConnected -> "تونل فعال"
                        isBusy -> "گام $stepIndex از ۵"
                        else -> "یک تپ · ضد تحریم"
                    },
                    style = MaterialTheme.typography.labelSmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    textAlign = TextAlign.Center
                )
            }
        }
    }
}

/**
 * n8n-inspired 5-Node Live Data-Flow Pipeline Card:
 * [۱. کانفیگ] ➔ [۲. DoH تمیز] ➔ [۳. هسته Xray] ➔ [۴. تونل tun0] ➔ [۵. ترافیک ↑↓]
 * Shows live node completion and animated packet dots moving across the wire.
 */
@Composable
fun N8nPipelineFlowCard(
    telemetry: TunnelTelemetry,
    isConnected: Boolean,
    onClick: (() -> Unit)? = null,
    modifier: Modifier = Modifier
) {
    val context = LocalContext.current
    val reduced = MotionSpec.isReducedMotion(context)
    val infinite = rememberInfiniteTransition(label = "n8n-flow")
    val packetPhase by infinite.animateFloat(
        initialValue = 0f,
        targetValue = if (reduced) 0.5f else 1f,
        animationSpec = infiniteRepeatable(
            animation = tween(durationMillis = 1500, easing = LinearEasing),
            repeatMode = RepeatMode.Restart
        ),
        label = "packet-phase"
    )

    val nodes = listOf(
        "کانفیگ" to (telemetry.stepIndex >= 1 || isConnected),
        "DoH تمیز" to (telemetry.stepIndex >= 2 || isConnected),
        "هسته Xray" to (telemetry.stepIndex >= 3 || isConnected),
        "تونل tun0" to (telemetry.stepIndex >= 4 || isConnected),
        "ترافیک ↑↓" to (isConnected && (telemetry.verifiedPingMs != null || telemetry.bytesDown > 0))
    )

    Card(
        modifier = modifier
            .fillMaxWidth()
            .then(if (onClick != null) Modifier.springPressClickable(onClick = onClick) else Modifier),
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.32f)
        ),
        shape = RoundedCornerShape(16.dp)
    ) {
        Column(modifier = Modifier.padding(horizontal = 14.dp, vertical = 12.dp)) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = telemetry.stepTitleFa,
                    style = MaterialTheme.typography.labelLarge,
                    fontWeight = FontWeight.Bold,
                    color = if (isConnected && telemetry.verifiedPingMs != null) GhGreen else GhBlue
                )
                Text(
                    text = if (telemetry.isAutoHealing) "Auto-Heal فعال" else "گراف جریان داده",
                    style = MaterialTheme.typography.labelSmall,
                    color = if (telemetry.isAutoHealing) OrbAmber else MaterialTheme.colorScheme.onSurfaceVariant
                )
            }

            Spacer(Modifier.height(10.dp))

            // Animated n8n Node-Wire Canvas
            Canvas(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(28.dp)
            ) {
                val count = nodes.size
                val stepX = size.width / count.toFloat()
                val cy = size.height / 2f

                // Draw wires and flowing packets between nodes
                for (i in 0 until count - 1) {
                    val x1 = stepX * i + stepX / 2f
                    val x2 = stepX * (i + 1) + stepX / 2f
                    val activeWire = nodes[i].second
                    val wireColor = if (activeWire) OrbEmerald.copy(alpha = 0.55f) else Color(0xFF334155)
                    drawLine(
                        color = wireColor,
                        start = Offset(x1, cy),
                        end = Offset(x2, cy),
                        strokeWidth = 2.5.dp.toPx(),
                        cap = StrokeCap.Round
                    )
                    if (activeWire) {
                        val px = x1 + (x2 - x1) * packetPhase
                        drawCircle(
                            color = OrbCyan,
                            radius = 3.5.dp.toPx(),
                            center = Offset(px, cy)
                        )
                    }
                }

                // Draw node circles
                for (i in 0 until count) {
                    val cx = stepX * i + stepX / 2f
                    val done = nodes[i].second
                    val isCurrent = telemetry.stepIndex == i + 1 && !done
                    val nodeColor = when {
                        done -> OrbEmerald
                        isCurrent && telemetry.isAutoHealing -> OrbAmber
                        isCurrent -> OrbCyan
                        else -> Color(0xFF475569)
                    }
                    drawCircle(
                        color = nodeColor.copy(alpha = 0.22f),
                        radius = 11.dp.toPx(),
                        center = Offset(cx, cy)
                    )
                    drawCircle(
                        color = nodeColor,
                        radius = 6.dp.toPx(),
                        center = Offset(cx, cy)
                    )
                }
            }

            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                nodes.forEach { (title, done) ->
                    Text(
                        text = title,
                        fontSize = 10.sp,
                        fontWeight = if (done) FontWeight.Bold else FontWeight.Normal,
                        color = if (done) OrbEmerald else MaterialTheme.colorScheme.onSurfaceVariant,
                        textAlign = TextAlign.Center,
                        modifier = Modifier.weight(1f)
                    )
                }
            }
        }
    }
}

/**
 * Live Dual-Wave Traffic Oscilloscope (Upload Cyan + Download Emerald Green).
 */
@Composable
fun LiveTrafficWaveformCard(
    telemetry: TunnelTelemetry,
    modifier: Modifier = Modifier
) {
    val context = LocalContext.current
    val reduced = MotionSpec.isReducedMotion(context)
    val infinite = rememberInfiniteTransition(label = "wave-osc")
    val phaseShift by infinite.animateFloat(
        initialValue = 0f,
        targetValue = if (reduced) 0f else (2f * PI.toFloat()),
        animationSpec = infiniteRepeatable(
            animation = tween(durationMillis = 1600, easing = LinearEasing),
            repeatMode = RepeatMode.Restart
        ),
        label = "wave-phase"
    )

    val hasUp = telemetry.bytesUp > 0L
    val hasDown = telemetry.bytesDown > 0L

    Card(
        modifier = modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.28f)
        ),
        shape = RoundedCornerShape(16.dp)
    ) {
        Column(modifier = Modifier.padding(14.dp)) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = "نوسان‌نگار زندهٔ ترافیک تونل",
                    style = MaterialTheme.typography.labelMedium,
                    fontWeight = FontWeight.Bold,
                    color = MaterialTheme.colorScheme.onSurface
                )
                Text(
                    text = "TCP: ${telemetry.activeTcpSessions} · DNS: ${telemetry.dnsQueriesHandled}",
                    style = MaterialTheme.typography.labelSmall,
                    fontFamily = FontFamily.Monospace,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }

            Spacer(Modifier.height(8.dp))

            Canvas(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(44.dp)
            ) {
                val w = size.width
                val h = size.height
                val midY = h / 2f
                val upAmp = if (hasUp) h * 0.32f else h * 0.08f
                val downAmp = if (hasDown) h * 0.38f else h * 0.08f

                val upPath = Path()
                val downPath = Path()
                val samples = 48
                for (i in 0..samples) {
                    val x = (w * i) / samples.toFloat()
                    val t = (i.toFloat() / samples.toFloat()) * (2f * PI.toFloat() * 2.2f)
                    val yUp = midY + sin(t + phaseShift) * upAmp
                    val yDown = midY + cos(t - phaseShift * 1.15f) * downAmp
                    if (i == 0) {
                        upPath.moveTo(x, yUp)
                        downPath.moveTo(x, yDown)
                    } else {
                        upPath.lineTo(x, yUp)
                        downPath.lineTo(x, yDown)
                    }
                }
                drawPath(
                    path = upPath,
                    color = OrbCyan.copy(alpha = 0.70f),
                    style = Stroke(width = 2.dp.toPx(), cap = StrokeCap.Round)
                )
                drawPath(
                    path = downPath,
                    color = OrbEmerald.copy(alpha = 0.90f),
                    style = Stroke(width = 2.5.dp.toPx(), cap = StrokeCap.Round)
                )
            }

            Spacer(Modifier.height(6.dp))

            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Text(
                    text = "↓ دانلود: ${TunnelLogBuffer.formatBytes(telemetry.bytesDown)}",
                    style = MaterialTheme.typography.labelMedium,
                    fontWeight = FontWeight.Bold,
                    color = OrbEmerald
                )
                Text(
                    text = "↑ آپلود: ${TunnelLogBuffer.formatBytes(telemetry.bytesUp)}",
                    style = MaterialTheme.typography.labelMedium,
                    fontWeight = FontWeight.Bold,
                    color = OrbCyan
                )
            }
        }
    }
}
