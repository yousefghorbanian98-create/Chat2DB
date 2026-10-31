package com.ghprotocol.app.domain

import android.content.Context

/** P1 user preferences (theme, language). Plain SharedPreferences. */
class SettingsStore(context: Context) {
    private val sp = context.applicationContext.getSharedPreferences("gh-settings", Context.MODE_PRIVATE)

    /** "system" | "light" | "dark" */
    var theme: String
        get() = sp.getString("theme", "system") ?: "system"
        set(value) = sp.edit().putString("theme", value).apply()

    /** "system" | "fa" | "en" */
    var language: String
        get() = sp.getString("language", "system") ?: "system"
        set(value) = sp.edit().putString("language", value).apply()
}
