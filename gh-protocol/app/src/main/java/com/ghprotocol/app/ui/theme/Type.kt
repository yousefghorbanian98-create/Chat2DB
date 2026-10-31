package com.ghprotocol.app.ui.theme

import androidx.compose.material3.Typography
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.Font
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.sp
import com.ghprotocol.app.R

val Vazir = FontFamily(
    Font(R.font.vazirmatn_regular, FontWeight.Normal),
    Font(R.font.vazirmatn_medium, FontWeight.Medium),
    Font(R.font.vazirmatn_bold, FontWeight.Bold)
)

val GhTypography = Typography(
    displaySmall = TextStyle(fontFamily = Vazir, fontSize = 34.sp, fontWeight = FontWeight.Bold),
    headlineMedium = TextStyle(fontFamily = Vazir, fontSize = 26.sp, fontWeight = FontWeight.Bold),
    titleMedium = TextStyle(fontFamily = Vazir, fontSize = 18.sp, fontWeight = FontWeight.Medium),
    bodyLarge = TextStyle(fontFamily = Vazir, fontSize = 16.sp),
    bodyMedium = TextStyle(fontFamily = Vazir, fontSize = 14.sp),
    labelSmall = TextStyle(fontFamily = Vazir, fontSize = 12.sp)
)
