package com.ghprotocol.app.ui

import android.graphics.Matrix
import androidx.annotation.DrawableRes
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
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.interaction.collectIsPressedAsState
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.BoxScope
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
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.composed
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.drawBehind
import androidx.compose.ui.draw.scale
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.ColorFilter
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.StrokeJoin
import androidx.compose.ui.graphics.asComposePath
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.drawscope.clipPath
import androidx.compose.ui.graphics.drawscope.rotate
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.SpanStyle
import androidx.compose.ui.text.buildAnnotatedString
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.withStyle
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.core.graphics.PathParser
import com.ghprotocol.app.R
import com.ghprotocol.app.core.TunnelLogBuffer
import com.ghprotocol.app.core.TunnelTelemetry
import com.ghprotocol.app.ui.theme.MotionSpec
import kotlin.math.PI
import kotlin.math.cos
import kotlin.math.sin

/**
 * Exact Color Palette imported from:
 * - UnboundTechCo/defyxVPN/lib/core/theme/app_colors.dart
 * - Ashutoshx7/VengenceUI/src/components/ui/glow-border-card.tsx & radial-glow-button.tsx
 */
object DefyxColors {
    val TopGradientConnected = Color(0xFF18181E)
    val MiddleGradientConnected = Color(0xFF1C443B)
    val BottomGradientConnected = Color(0xFF21AD86)

    val TopGradientConnecting = Color(0xFF18181E)
    val MiddleGradientConnecting = Color(0xFF4161A6)
    val BottomGradientConnecting = Color(0xFF23499C)

    val TopGradientFailed = Color(0xFF18181E)
    val MiddleGradientFailed = Color(0xFF867229)
    val BottomGradientFailed = Color(0xFFD9B639)

    val TopGradientStandby = Color(0xFF18181E)
    val MiddleGradientStandby = Color(0xFF22222C)
    val BottomGradientStandby = Color(0xFF484858)

    val BrandGold = Color(0xFFFFC927)
    val DownloadGreen = Color(0xFF76F959)
    val UploadCyan = Color(0xFF72D9FF)
    val WarningOrange = Color(0xFFFFAA66)
    val CheckMint = Color(0xFFB2FFB9)
    val ReloadCream = Color(0xFFFFEAA1)
    val ErrorRose = Color(0xFFFFBFC0)

    // VengeanceUI glow-border-card.tsx 'aurora' preset
    val VengeanceAurora = listOf(
        Color(0xFF00FF87),
        Color(0xFF22FFAA),
        Color(0xFF44FFCC),
        Color(0xFF60EFFF),
        Color(0xFF88DDFF),
        Color(0xFFBB99FF),
        Color(0xFFDD77EE),
        Color(0xFFFF68F0),
        Color(0xFFFF55CC),
        Color(0xFF00FF87)
    )

    // VengeanceUI glow-border-card.tsx 'ocean' preset
    val VengeanceOcean = listOf(
        Color(0xFF006699),
        Color(0xFF1177AA),
        Color(0xFF2288BB),
        Color(0xFF3399CC),
        Color(0xFF44AADD),
        Color(0xFF55BBEE),
        Color(0xFF66CCFF),
        Color(0xFF44BBEE),
        Color(0xFF2299CC),
        Color(0xFF006699)
    )
}

/**
 * Exact Shield SVG Path from UnboundTechCo/defyxVPN/lib/modules/main/presentation/widgets/connection_button.dart
 */
private const val DEFYX_SHIELD_SVG_PATH =
    "M51.39 1.16517L100.313 21.8855C100.72 22.0581 100.966 22.4781 100.917 22.918L94.1288 83.2901C93.9546 84.8395 93.1841 86.2602 91.9806 87.2513L51.6357 120.476C51.2665 120.781 50.7336 120.781 50.3643 120.476L10.0194 87.2513C8.8159 86.2602 8.04544 84.8395 7.87124 83.2901L1.08337 22.918C1.03392 22.4781 1.27953 22.0581 1.68712 21.8855L50.61 1.16517C50.8593 1.0596 51.1407 1.0596 51.39 1.16517Z"

@Composable
private fun rememberLoopingFloat(
    initialValue: Float,
    targetValue: Float,
    durationMillis: Int,
    repeatMode: RepeatMode = RepeatMode.Restart,
    staticFallback: Float = initialValue,
    label: String = "loop"
): Float {
    val context = LocalContext.current
    val isRobolectric = android.os.Build.FINGERPRINT?.contains("robolectric", ignoreCase = true) == true
    if (isRobolectric || MotionSpec.isReducedMotion(context)) {
        return staticFallback
    }
    val infinite = rememberInfiniteTransition(label = label)
    val v by infinite.animateFloat(
        initialValue = initialValue,
        targetValue = targetValue,
        animationSpec = infiniteRepeatable(
            animation = tween(durationMillis = durationMillis, easing = LinearEasing),
            repeatMode = repeatMode
        ),
        label = label
    )
    return v
}

/**
 * Tactile spring press modifier from kylezantos/design-motion-principles & Ashutoshx7/VengenceUI.
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
 * Direct port of UnboundTechCo/defyxVPN/lib/shared/layout/main_screen_background.dart
 * + Ashutoshx7/VengenceUI/src/components/ui/animated-rays.tsx
 */
@Composable
fun DefyxMainScreenBackground(
    phase: ConnectPhase,
    isAutoHealing: Boolean,
    modifier: Modifier = Modifier,
    content: @Composable BoxScope.() -> Unit
) {
    val context = LocalContext.current
    val isConnected = phase == ConnectPhase.CONNECTED
    val isBusy = phase == ConnectPhase.CHECKING ||
        phase == ConnectPhase.PREPARING ||
        phase == ConnectPhase.TUNNELING ||
        isAutoHealing
    val isFailed = phase == ConnectPhase.FAILED

    val topColor by animateColorAsState(
        targetValue = when {
            isConnected -> DefyxColors.TopGradientConnected
            isBusy -> DefyxColors.TopGradientConnecting
            isFailed -> DefyxColors.TopGradientFailed
            else -> DefyxColors.TopGradientStandby
        },
        animationSpec = MotionSpec.tweenMs(context, 300),
        label = "bg-top"
    )
    val midColor by animateColorAsState(
        targetValue = when {
            isConnected -> DefyxColors.MiddleGradientConnected
            isBusy -> DefyxColors.MiddleGradientConnecting
            isFailed -> DefyxColors.MiddleGradientFailed
            else -> DefyxColors.MiddleGradientStandby
        },
        animationSpec = MotionSpec.tweenMs(context, 300),
        label = "bg-mid"
    )
    val bottomColor by animateColorAsState(
        targetValue = when {
            isConnected -> DefyxColors.BottomGradientConnected
            isBusy -> DefyxColors.BottomGradientConnecting
            isFailed -> DefyxColors.BottomGradientFailed
            else -> DefyxColors.BottomGradientStandby
        },
        animationSpec = MotionSpec.tweenMs(context, 300),
        label = "bg-bottom"
    )

    Box(
        modifier = modifier
            .fillMaxSize()
            .background(
                Brush.verticalGradient(
                    0.0f to topColor,
                    0.28f to midColor,
                    0.92f to bottomColor
                )
            )
    ) {
        // VengeanceUI animated-rays.tsx top volumetric light cone
        Canvas(modifier = Modifier.fillMaxSize()) {
            drawCircle(
                brush = Brush.radialGradient(
                    colors = listOf(
                        Color.White.copy(alpha = 0.08f),
                        Color.Transparent
                    ),
                    center = Offset(size.width * 0.5f, size.height * 0.18f),
                    radius = size.minDimension * 0.85f
                ),
                center = Offset(size.width * 0.5f, size.height * 0.18f),
                radius = size.minDimension * 0.85f
            )
        }
        content()
    }
}

/**
 * Direct port of UnboundTechCo/defyxVPN/lib/modules/main/presentation/widgets/header_section.dart
 * & connection_state_widgets.dart (AnalyzingContent + PingIndicator).
 */
@Composable
fun DefyxHeaderSection(
    phase: ConnectPhase,
    verifiedPingMs: Int?,
    isAutoHealing: Boolean,
    cleanIp: String?,
    activeRemark: String,
    telemetry: TunnelTelemetry,
    onTapPing: () -> Unit,
    onTapLogs: () -> Unit,
    modifier: Modifier = Modifier
) {
    val isConnected = phase == ConnectPhase.CONNECTED
    val isBusy = phase == ConnectPhase.CHECKING ||
        phase == ConnectPhase.PREPARING ||
        phase == ConnectPhase.TUNNELING ||
        isAutoHealing
    val isFailed = phase == ConnectPhase.FAILED

    Column(
        modifier = modifier.fillMaxWidth(),
        horizontalAlignment = Alignment.Start
    ) {
        // Brand row: 'G' in #FFC927 (w800) + 'h Protocol' in White (w400), direct port of Defyx 'D' + 'efyx'
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(
                text = buildAnnotatedString {
                    withStyle(
                        SpanStyle(
                            color = DefyxColors.BrandGold,
                            fontWeight = FontWeight.ExtraBold,
                            fontSize = 30.sp
                        )
                    ) {
                        append("G")
                    }
                    withStyle(
                        SpanStyle(
                            color = Color.White,
                            fontWeight = FontWeight.SemiBold,
                            fontSize = 27.sp
                        )
                    ) {
                        append("h Protocol")
                    }
                }
            )
            // Active Route + Clean IP Pill with official vpn_cloud.svg icon
            Row(
                modifier = Modifier
                    .clip(RoundedCornerShape(50))
                    .background(Color.White.copy(alpha = 0.10f))
                    .border(1.dp, Color.White.copy(alpha = 0.18f), RoundedCornerShape(50))
                    .padding(horizontal = 12.dp, vertical = 6.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Icon(
                    painter = painterResource(R.drawable.ic_defyx_vpn_cloud),
                    contentDescription = null,
                    tint = DefyxColors.BrandGold,
                    modifier = Modifier.size(16.dp)
                )
                Spacer(Modifier.width(6.dp))
                Text(
                    text = cleanIp ?: activeRemark,
                    color = Color.White,
                    fontSize = 12.sp,
                    fontWeight = FontWeight.SemiBold,
                    fontFamily = FontFamily.Monospace
                )
            }
        }

        Spacer(Modifier.height(6.dp))

        // Animated status headline from connection_state_widgets.dart
        Text(
            text = when {
                isConnected && verifiedPingMs != null -> "حریم خصوصی شما ایمن و عبور ترافیک تایید شد"
                isConnected && isAutoHealing -> "در حال بهینه‌سازی خودکار مسیر ضد فیلتر..."
                isConnected -> "تونل رمزنگاری‌شدهٔ شما متصل است"
                isBusy -> "در حال آنالیز شبکه و ایجاد تونل امن..."
                isFailed -> "فرآیند اتصال نیاز به تلاش مجدد دارد"
                else -> "سپر هوشمند ضد تحریم آمادهٔ اتصال است"
            },
            color = when {
                isConnected -> DefyxColors.CheckMint
                isFailed -> DefyxColors.ReloadCream
                else -> Color.White.copy(alpha = 0.92f)
            },
            fontSize = 20.sp,
            fontWeight = FontWeight.Bold
        )

        Spacer(Modifier.height(8.dp))

        // AnalyzingContent / PingIndicator row from connection_state_widgets.dart
        Row(
            modifier = Modifier
                .clip(RoundedCornerShape(12.dp))
                .background(Color.Black.copy(alpha = 0.24f))
                .border(1.dp, Color.White.copy(alpha = 0.12f), RoundedCornerShape(12.dp))
                .springPressClickable(onClick = if (isConnected) onTapPing else onTapLogs)
                .padding(horizontal = 12.dp, vertical = 8.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            if (isConnected) {
                Image(
                    painter = painterResource(R.drawable.ic_defyx_check_circle),
                    contentDescription = null,
                    modifier = Modifier.size(18.dp)
                )
                Spacer(Modifier.width(8.dp))
                Text(
                    text = activeRemark,
                    color = Color.White,
                    fontSize = 13.sp,
                    fontWeight = FontWeight.SemiBold
                )
                Spacer(Modifier.width(10.dp))
                Image(
                    painter = painterResource(R.drawable.ic_defyx_wifi),
                    contentDescription = null,
                    modifier = Modifier.size(12.dp),
                    colorFilter = ColorFilter.tint(DefyxColors.DownloadGreen)
                )
                Spacer(Modifier.width(5.dp))
                Text(
                    text = if (verifiedPingMs != null) "$verifiedPingMs ms" else "تست پینگ",
                    color = DefyxColors.DownloadGreen,
                    fontSize = 13.sp,
                    fontWeight = FontWeight.Bold,
                    fontFamily = FontFamily.Monospace
                )
            } else {
                val step = telemetry.stepIndex.coerceIn(0, 5)
                Text(
                    text = if (step > 0) "$step/5" else "READY",
                    color = DefyxColors.BrandGold,
                    fontSize = 12.sp,
                    fontWeight = FontWeight.Bold,
                    fontFamily = FontFamily.Monospace
                )
                Spacer(Modifier.width(6.dp))
                Image(
                    painter = painterResource(R.drawable.ic_defyx_arrow_left),
                    contentDescription = null,
                    modifier = Modifier.size(10.dp),
                    colorFilter = ColorFilter.tint(Color.White.copy(alpha = 0.65f))
                )
                Spacer(Modifier.width(6.dp))
                Text(
                    text = telemetry.stepTitleFa,
                    color = Color.White.copy(alpha = 0.85f),
                    fontSize = 12.sp,
                    maxLines = 1
                )
            }
        }
    }
}

/**
 * Direct port of UnboundTechCo/defyxVPN/lib/modules/main/presentation/widgets/connection_button.dart:
 * - Official Shield.svg VectorDrawable & PathParser clip/border
 * - 4 concentric animated Shield Pulse Rings (scale 0.5, 0.7, 0.9, 1.1)
 * - ShieldLoadingPainter rotating SweepGradient (stops: 0.0, 0.3, 0.45, 0.5, 0.55, 0.7, 1.0)
 * - Scan Matrix sweep lines (ported from assets/lottie/scan.json)
 * - Official defyx_standby.svg, defyx_loading.svg, defyx_check.svg, defyx_reload.svg center icons
 */
@Composable
fun DefyxShieldConnectionButton(
    phase: ConnectPhase,
    verifiedPingMs: Int?,
    isAutoHealing: Boolean,
    stepIndex: Int,
    onTapConnect: () -> Unit,
    onTapDisconnect: () -> Unit,
    modifier: Modifier = Modifier
) {
    val isConnected = phase == ConnectPhase.CONNECTED
    val isBusy = phase == ConnectPhase.CHECKING ||
        phase == ConnectPhase.PREPARING ||
        phase == ConnectPhase.TUNNELING ||
        isAutoHealing
    val isFailed = phase == ConnectPhase.FAILED

    val pulseProgress = rememberLoopingFloat(
        initialValue = 0f,
        targetValue = 1f,
        durationMillis = if (isBusy) 1600 else 2800,
        repeatMode = RepeatMode.Restart,
        staticFallback = 0.35f,
        label = "shield-pulse"
    )
    val rotationAngle = rememberLoopingFloat(
        initialValue = 0f,
        targetValue = 360f,
        durationMillis = 3000,
        repeatMode = RepeatMode.Restart,
        staticFallback = 45f,
        label = "shield-sweep"
    )
    val scanProgress = rememberLoopingFloat(
        initialValue = 0f,
        targetValue = 1f,
        durationMillis = 1500,
        repeatMode = RepeatMode.Reverse,
        staticFallback = 0.5f,
        label = "shield-scan"
    )

    val pulseTint = when {
        isConnected -> DefyxColors.BottomGradientConnected
        isBusy -> DefyxColors.BottomGradientConnecting
        isFailed -> DefyxColors.BottomGradientFailed
        else -> Color.White
    }

    // Exact center status SVG icon from UnboundTechCo/defyxVPN/assets/icons/
    @DrawableRes val statusIconRes = when {
        isConnected -> R.drawable.ic_defyx_check
        isBusy -> R.drawable.ic_defyx_loading
        isFailed -> R.drawable.ic_defyx_reload
        else -> R.drawable.ic_defyx_standby
    }
    val statusIconSize: Dp = when {
        isConnected -> 84.dp
        isBusy -> 96.dp
        else -> 76.dp
    }

    val rawAndroidPath = remember { PathParser.createPathFromPathData(DEFYX_SHIELD_SVG_PATH) }

    Column(
        modifier = modifier,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Box(
            modifier = Modifier
                .size(236.dp)
                .springPressClickable(pressedScale = 0.94f) {
                    if (isConnected) onTapDisconnect() else onTapConnect()
                },
            contentAlignment = Alignment.Center
        ) {
            // 1. Four concentric animated Shield Pulse Rings (exact math from connection_button.dart)
            val rings = listOf(
                (0.55f + 0.20f * pulseProgress) to (0.36f * (1f - 0.6f * pulseProgress)),
                (0.72f + 0.20f * pulseProgress) to (0.28f * (1f - 0.8f * pulseProgress)),
                (0.89f + 0.20f * pulseProgress) to (0.24f * (1f - pulseProgress)),
                (1.06f + 0.20f * pulseProgress) to (0.18f * (1f - pulseProgress))
            )
            rings.forEach { (ringScale, ringAlpha) ->
                Image(
                    painter = painterResource(R.drawable.ic_defyx_shield_solid),
                    contentDescription = null,
                    colorFilter = ColorFilter.tint(pulseTint.copy(alpha = ringAlpha.coerceIn(0f, 0.45f))),
                    modifier = Modifier
                        .size(width = 148.dp, height = 178.dp)
                        .graphicsLayer {
                            scaleX = ringScale
                            scaleY = ringScale
                        }
                )
            }

            // 2. Main Shield body + Scan Matrix + Rotating SweepGradient (ShieldLoadingPainter)
            Canvas(
                modifier = Modifier.size(width = 148.dp, height = 178.dp)
            ) {
                val matrix = Matrix().apply {
                    setScale(size.width / 102f, size.height / 122f)
                }
                val scaledAndroidPath = android.graphics.Path(rawAndroidPath).apply {
                    transform(matrix)
                }
                val shieldComposePath = scaledAndroidPath.asComposePath()

                // Clipped interior of the Shield
                clipPath(shieldComposePath) {
                    // Frosted glass shield fill
                    drawRect(
                        brush = Brush.verticalGradient(
                            colors = listOf(
                                Color.White.copy(alpha = 0.22f),
                                pulseTint.copy(alpha = 0.18f),
                                Color.Black.copy(alpha = 0.28f)
                            )
                        )
                    )

                    // Scan Matrix animation (ported from UnboundTechCo/defyxVPN/assets/lottie/scan.json)
                    if (isBusy || isConnected) {
                        val barY = size.height * scanProgress
                        val beamColor = if (isConnected) DefyxColors.CheckMint else DefyxColors.UploadCyan
                        // Matrix grid dots
                        val cols = 6
                        val rows = 7
                        for (r in 1 until rows) {
                            for (c in 1 until cols) {
                                val gx = (size.width / cols) * c
                                val gy = (size.height / rows) * r
                                val dist = kotlin.math.abs(gy - barY) / (size.height * 0.35f)
                                val dotAlpha = (1f - dist).coerceIn(0.06f, 0.45f)
                                drawCircle(
                                    color = beamColor.copy(alpha = dotAlpha),
                                    radius = 1.8.dp.toPx(),
                                    center = Offset(gx, gy)
                                )
                            }
                        }
                        if (isBusy) {
                            // Horizontal laser scan bar + glow trail
                            drawRect(
                                brush = Brush.verticalGradient(
                                    colors = listOf(
                                        Color.Transparent,
                                        beamColor.copy(alpha = 0.35f),
                                        Color.Transparent
                                    ),
                                    startY = (barY - 24.dp.toPx()).coerceAtLeast(0f),
                                    endY = (barY + 24.dp.toPx()).coerceAtMost(size.height)
                                )
                            )
                            drawLine(
                                color = Color.White.copy(alpha = 0.85f),
                                start = Offset(0f, barY),
                                end = Offset(size.width, barY),
                                strokeWidth = 2.dp.toPx()
                            )
                        }
                    }
                }

                // Base Shield stroke
                drawPath(
                    path = shieldComposePath,
                    color = Color.White.copy(alpha = 0.28f),
                    style = Stroke(width = 1.6.dp.toPx(), cap = StrokeCap.Round, join = StrokeJoin.Round)
                )

                // ShieldLoadingPainter rotating SweepGradient border (exact stops from connection_button.dart)
                val center = Offset(size.width / 2f, size.height / 2f)
                val sweepAccent = when {
                    isConnected -> DefyxColors.CheckMint
                    isBusy -> Color.White
                    isFailed -> DefyxColors.ReloadCream
                    else -> DefyxColors.BrandGold.copy(alpha = 0.75f)
                }
                rotate(degrees = rotationAngle, pivot = center) {
                    drawPath(
                        path = shieldComposePath,
                        brush = Brush.sweepGradient(
                            0.00f to Color.Transparent,
                            0.30f to Color.Transparent,
                            0.45f to sweepAccent.copy(alpha = 0.35f),
                            0.50f to sweepAccent,
                            0.55f to sweepAccent.copy(alpha = 0.35f),
                            0.70f to Color.Transparent,
                            1.00f to Color.Transparent,
                            center = center
                        ),
                        style = Stroke(
                            width = if (isBusy || isConnected) 3.2.dp.toPx() else 2.2.dp.toPx(),
                            cap = StrokeCap.Round,
                            join = StrokeJoin.Round
                        )
                    )
                }
            }

            // 3. Official DefyxVPN center SVG status icon (defyx_standby / defyx_loading / defyx_check / defyx_reload)
            Image(
                painter = painterResource(statusIconRes),
                contentDescription = null,
                modifier = Modifier.size(statusIconSize)
            )
        }

        // Action label chip below the Shield button
        Row(
            modifier = Modifier
                .clip(RoundedCornerShape(50))
                .background(Color.Black.copy(alpha = 0.28f))
                .border(1.dp, Color.White.copy(alpha = 0.18f), RoundedCornerShape(50))
                .springPressClickable {
                    if (isConnected) onTapDisconnect() else onTapConnect()
                }
                .padding(horizontal = 20.dp, vertical = 8.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Box(
                modifier = Modifier
                    .size(8.dp)
                    .clip(CircleShape)
                    .background(
                        when {
                            isConnected -> DefyxColors.DownloadGreen
                            isBusy -> DefyxColors.BrandGold
                            isFailed -> DefyxColors.ErrorRose
                            else -> DefyxColors.UploadCyan
                        }
                    )
            )
            Spacer(Modifier.width(8.dp))
            Text(
                text = when {
                    isConnected -> "متصل (برای قطع اتصال تپ کنید)"
                    isBusy -> "در حال اتصال هوشمند (گام $stepIndex از ۵)..."
                    isFailed -> "تلاش مجدد برای اتصال"
                    else -> "تپ برای اتصال با یک کلیک"
                },
                color = Color.White,
                fontSize = 13.sp,
                fontWeight = FontWeight.Bold
            )
        }
    }
}

/**
 * Direct port of Ashutoshx7/VengenceUI/src/components/ui/glow-border-card.tsx & border-beam.tsx:
 * Animated rotating conic-gradient perimeter beam card with dark glassmorphic interior.
 */
@Composable
fun VengeanceGlowBorderCard(
    modifier: Modifier = Modifier,
    presetColors: List<Color> = DefyxColors.VengeanceAurora,
    cornerRadius: Dp = 18.dp,
    borderWidth: Dp = 1.5.dp,
    onClick: (() -> Unit)? = null,
    content: @Composable BoxScope.() -> Unit
) {
    val angle = rememberLoopingFloat(
        initialValue = 0f,
        targetValue = 360f,
        durationMillis = 4200,
        repeatMode = RepeatMode.Restart,
        staticFallback = 30f,
        label = "border-angle"
    )

    val shape = RoundedCornerShape(cornerRadius)
    Box(
        modifier = modifier
            .then(if (onClick != null) Modifier.springPressClickable(onClick = onClick) else Modifier)
            .clip(shape)
            .drawBehind {
                val center = Offset(size.width / 2f, size.height / 2f)
                rotate(degrees = angle, pivot = center) {
                    drawRoundRect(
                        brush = Brush.sweepGradient(presetColors, center = center),
                        cornerRadius = CornerRadius(cornerRadius.toPx(), cornerRadius.toPx()),
                        style = Stroke(width = borderWidth.toPx() * 2.2f)
                    )
                }
            }
            .padding(borderWidth)
            .clip(shape)
            .background(Color(0xDD14141C))
            .padding(14.dp),
        content = content
    )
}

/**
 * Direct port of Ashutoshx7/VengenceUI/src/components/ui/radial-glow-button.tsx & generate-button.tsx:
 * Multi-stop radial glow + inset neon border button with imported SVG icon.
 */
@Composable
fun VengeanceRadialGlowButton(
    text: String,
    @DrawableRes iconRes: Int = R.drawable.ic_vengeance_sparkles,
    accentColor: Color = DefyxColors.BrandGold,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    enabled: Boolean = true
) {
    Box(
        modifier = modifier
            .springPressClickable(enabled = enabled, onClick = onClick)
            .clip(RoundedCornerShape(14.dp))
            .background(
                Brush.radialGradient(
                    colors = listOf(
                        accentColor.copy(alpha = 0.34f),
                        Color(0xFF1F3F6D).copy(alpha = 0.55f),
                        Color(0xFF0E101A)
                    ),
                    radius = 360f
                )
            )
            .border(1.2.dp, accentColor.copy(alpha = 0.65f), RoundedCornerShape(14.dp))
            .padding(horizontal = 14.dp, vertical = 11.dp),
        contentAlignment = Alignment.Center
    ) {
        Row(
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.Center
        ) {
            Icon(
                painter = painterResource(iconRes),
                contentDescription = null,
                tint = accentColor,
                modifier = Modifier.size(18.dp)
            )
            Spacer(Modifier.width(8.dp))
            Text(
                text = text,
                color = Color.White,
                fontSize = 13.sp,
                fontWeight = FontWeight.Bold
            )
        }
    }
}

/**
 * Direct port of Ashutoshx7/VengenceUI/src/components/ui/glass-dock.tsx & spotlight-navbar.tsx:
 * Floating frosted-glass dock with spring-animated spotlight indicator and exact VengeanceUI SVG icons.
 */
data class VengeanceDockItem(
    val route: String,
    val label: String,
    @DrawableRes val iconRes: Int
)

@Composable
fun VengeanceGlassDock(
    items: List<VengeanceDockItem>,
    currentRoute: String,
    onSelect: (String) -> Unit,
    modifier: Modifier = Modifier
) {
    Box(
        modifier = modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 10.dp),
        contentAlignment = Alignment.Center
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .clip(RoundedCornerShape(24.dp))
                .background(
                    Brush.verticalGradient(
                        colors = listOf(
                            Color(0xEB1C1D29),
                            Color(0xF511121A)
                        )
                    )
                )
                .border(
                    width = 1.2.dp,
                    brush = Brush.horizontalGradient(
                        colors = listOf(
                            Color.White.copy(alpha = 0.14f),
                            DefyxColors.BrandGold.copy(alpha = 0.45f),
                            DefyxColors.UploadCyan.copy(alpha = 0.45f),
                            Color.White.copy(alpha = 0.14f)
                        )
                    ),
                    shape = RoundedCornerShape(24.dp)
                )
                .padding(horizontal = 8.dp, vertical = 8.dp),
            horizontalArrangement = Arrangement.SpaceEvenly,
            verticalAlignment = Alignment.CenterVertically
        ) {
            items.forEach { item ->
                val selected = currentRoute == item.route
                val itemScale by animateFloatAsState(
                    targetValue = if (selected) 1.06f else 1.0f,
                    animationSpec = spring(dampingRatio = 0.65f, stiffness = 260f),
                    label = "dock-scale-${item.route}"
                )
                val pillAlpha by animateFloatAsState(
                    targetValue = if (selected) 0.20f else 0.0f,
                    animationSpec = tween(220),
                    label = "dock-alpha-${item.route}"
                )

                Box(
                    modifier = Modifier
                        .weight(1f)
                        .scale(itemScale)
                        .clip(RoundedCornerShape(18.dp))
                        .background(
                            if (selected) {
                                Brush.radialGradient(
                                    colors = listOf(
                                        DefyxColors.BrandGold.copy(alpha = pillAlpha),
                                        DefyxColors.UploadCyan.copy(alpha = pillAlpha * 0.5f),
                                        Color.Transparent
                                    )
                                )
                            } else {
                                Brush.radialGradient(listOf(Color.Transparent, Color.Transparent))
                            }
                        )
                        .then(
                            if (selected) {
                                Modifier.border(
                                    1.dp,
                                    DefyxColors.BrandGold.copy(alpha = 0.45f),
                                    RoundedCornerShape(18.dp)
                                )
                            } else {
                                Modifier
                            }
                        )
                        .springPressClickable(pressedScale = 0.92f) { onSelect(item.route) }
                        .padding(vertical = 8.dp, horizontal = 4.dp),
                    contentAlignment = Alignment.Center
                ) {
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Icon(
                            painter = painterResource(item.iconRes),
                            contentDescription = item.label,
                            tint = if (selected) DefyxColors.BrandGold else Color.White.copy(alpha = 0.65f),
                            modifier = Modifier.size(21.dp)
                        )
                        Spacer(Modifier.height(3.dp))
                        Text(
                            text = item.label,
                            color = if (selected) Color.White else Color.White.copy(alpha = 0.62f),
                            fontSize = 11.sp,
                            fontWeight = if (selected) FontWeight.Bold else FontWeight.Medium,
                            maxLines = 1
                        )
                    }
                }
            }
        }
    }
}

/**
 * n8n-inspired 5-Node Live Data-Flow Pipeline inside a VengeanceGlowBorderCard.
 */
@Composable
fun N8nPipelineFlowCard(
    telemetry: TunnelTelemetry,
    isConnected: Boolean,
    onClick: (() -> Unit)? = null,
    modifier: Modifier = Modifier
) {
    val packetPhase = rememberLoopingFloat(
        initialValue = 0f,
        targetValue = 1f,
        durationMillis = 1500,
        repeatMode = RepeatMode.Restart,
        staticFallback = 0.5f,
        label = "packet-phase"
    )

    val nodes = listOf(
        "کانفیگ" to (telemetry.stepIndex >= 1 || isConnected),
        "DoH تمیز" to (telemetry.stepIndex >= 2 || isConnected),
        "هسته Xray" to (telemetry.stepIndex >= 3 || isConnected),
        "تونل tun0" to (telemetry.stepIndex >= 4 || isConnected),
        "ترافیک ↑↓" to (isConnected && (telemetry.verifiedPingMs != null || telemetry.bytesDown > 0))
    )

    VengeanceGlowBorderCard(
        modifier = modifier.fillMaxWidth(),
        presetColors = if (isConnected) DefyxColors.VengeanceAurora else DefyxColors.VengeanceOcean,
        onClick = onClick
    ) {
        Column(modifier = Modifier.fillMaxWidth()) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = telemetry.stepTitleFa,
                    style = MaterialTheme.typography.labelLarge,
                    fontWeight = FontWeight.Bold,
                    color = if (isConnected) DefyxColors.CheckMint else DefyxColors.UploadCyan
                )
                Text(
                    text = if (telemetry.isAutoHealing) "Auto-Heal فعال" else "پایپ‌لاین ۵ مرحله‌ای",
                    style = MaterialTheme.typography.labelSmall,
                    color = if (telemetry.isAutoHealing) DefyxColors.BrandGold else Color.White.copy(alpha = 0.65f)
                )
            }

            Spacer(Modifier.height(10.dp))

            Canvas(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(26.dp)
            ) {
                val count = nodes.size
                val stepX = size.width / count.toFloat()
                val cy = size.height / 2f

                for (i in 0 until count - 1) {
                    val x1 = stepX * i + stepX / 2f
                    val x2 = stepX * (i + 1) + stepX / 2f
                    val activeWire = nodes[i].second
                    val wireColor = if (activeWire) DefyxColors.BottomGradientConnected.copy(alpha = 0.70f) else Color(0xFF334155)
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
                            color = DefyxColors.DownloadGreen,
                            radius = 3.5.dp.toPx(),
                            center = Offset(px, cy)
                        )
                    }
                }

                for (i in 0 until count) {
                    val cx = stepX * i + stepX / 2f
                    val done = nodes[i].second
                    val isCurrent = telemetry.stepIndex == i + 1 && !done
                    val nodeColor = when {
                        done -> DefyxColors.DownloadGreen
                        isCurrent -> DefyxColors.BrandGold
                        else -> Color(0xFF475569)
                    }
                    drawCircle(
                        color = nodeColor.copy(alpha = 0.24f),
                        radius = 10.dp.toPx(),
                        center = Offset(cx, cy)
                    )
                    drawCircle(
                        color = nodeColor,
                        radius = 5.5.dp.toPx(),
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
                        color = if (done) DefyxColors.CheckMint else Color.White.copy(alpha = 0.65f),
                        textAlign = TextAlign.Center,
                        modifier = Modifier.weight(1f)
                    )
                }
            }
        }
    }
}

/**
 * Direct port of UnboundTechCo/defyxVPN speed telemetry colors (#76F959 download, #72D9FF upload)
 * + Dual-Wave Traffic Oscilloscope inside a VengeanceGlowBorderCard.
 */
@Composable
fun LiveTrafficWaveformCard(
    telemetry: TunnelTelemetry,
    modifier: Modifier = Modifier
) {
    val phaseShift = rememberLoopingFloat(
        initialValue = 0f,
        targetValue = (2f * PI.toFloat()),
        durationMillis = 1600,
        repeatMode = RepeatMode.Restart,
        staticFallback = 0.5f,
        label = "wave-phase"
    )

    val hasUp = telemetry.bytesUp > 0L
    val hasDown = telemetry.bytesDown > 0L

    VengeanceGlowBorderCard(
        modifier = modifier.fillMaxWidth(),
        presetColors = DefyxColors.VengeanceOcean
    ) {
        Column(modifier = Modifier.fillMaxWidth()) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Icon(
                        painter = painterResource(R.drawable.ic_defyx_speed),
                        contentDescription = null,
                        tint = DefyxColors.DownloadGreen,
                        modifier = Modifier.size(18.dp)
                    )
                    Spacer(Modifier.width(6.dp))
                    Text(
                        text = "مانیتور زندهٔ ترافیک تونل",
                        style = MaterialTheme.typography.labelMedium,
                        fontWeight = FontWeight.Bold,
                        color = Color.White
                    )
                }
                Text(
                    text = "TCP: ${telemetry.activeTcpSessions} · DNS: ${telemetry.dnsQueriesHandled}",
                    style = MaterialTheme.typography.labelSmall,
                    fontFamily = FontFamily.Monospace,
                    color = Color.White.copy(alpha = 0.72f)
                )
            }

            Spacer(Modifier.height(8.dp))

            Canvas(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(40.dp)
            ) {
                val w = size.width
                val h = size.height
                val midY = h / 2f
                val upAmp = if (hasUp) h * 0.30f else h * 0.08f
                val downAmp = if (hasDown) h * 0.36f else h * 0.08f

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
                    color = DefyxColors.UploadCyan.copy(alpha = 0.80f),
                    style = Stroke(width = 2.dp.toPx(), cap = StrokeCap.Round)
                )
                drawPath(
                    path = downPath,
                    color = DefyxColors.DownloadGreen.copy(alpha = 0.92f),
                    style = Stroke(width = 2.5.dp.toPx(), cap = StrokeCap.Round)
                )
            }

            Spacer(Modifier.height(6.dp))

            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Text(
                    text = "↓ دریافتی: ${TunnelLogBuffer.formatBytes(telemetry.bytesDown)}",
                    style = MaterialTheme.typography.labelMedium,
                    fontWeight = FontWeight.Bold,
                    color = DefyxColors.DownloadGreen
                )
                Text(
                    text = "↑ ارسالی: ${TunnelLogBuffer.formatBytes(telemetry.bytesUp)}",
                    style = MaterialTheme.typography.labelMedium,
                    fontWeight = FontWeight.Bold,
                    color = DefyxColors.UploadCyan
                )
            }
        }
    }
}
