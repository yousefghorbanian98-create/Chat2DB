package com.ghprotocol.app.service

import android.content.Intent
import android.os.IBinder
import android.net.VpnService

/**
 * P0 placeholder for the VPN data path.
 *
 * Real implementation (P2, F-3): VpnService -> tun2socks -> Xray-core SOCKS5 :10808,
 * driven by the official Serverless-for-Iran subscription config.
 * Kept as a no-op in P0 so the permission/manifest surface is locked in from day one.
 */
class GhVpnService : VpnService() {
    override fun onBind(intent: Intent?): IBinder? = null

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        // P0: no-op. The UI button is disabled until P2 (F-3).
        stopSelf()
        return START_NOT_STICKY
    }
}
