package com.ghprotocol.app.core

import java.io.File

/**
 * Pluggable anti-censorship core interface (Finn-loop v1.4).
 * v1 ships [XrayCore] (XTLS/Xray-core v26.10.21 with TLS fragment & finalmask);
 * interface allows seamless addition of SingBoxEngine / Hysteria2Engine in v1.1.
 */
interface TunnelEngine {
    val name: String
    fun ensureInstalled(): Result<XrayCore.Info>
    fun version(): String
    fun start(configPath: File): Result<Process>
    fun stop()
    fun isRunning(): Boolean
    fun isHealthy(port: Int = 10808, timeoutMs: Int = 500): Boolean
}
