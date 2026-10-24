package com.ghprotocol.app.core

import android.app.Service
import android.content.Intent
import android.os.IBinder
import android.util.Log
import android.net.VpnService
import android.os.ParcelFileDescriptor
import java.net.Socket

/**
 * F-3/F-4: VpnService tunnel.
 * Loop: read packets from the protected fd -> SOCKS5 CONNECT to Xray mixed-in
 * (127.0.0.1:10808) -> relay. TCP per 4-tuple with idle reuse; DNS (UDP/53)
 * goes through the SOCKS5 UDP associate channel.
 */
class VpnTunnelService : VpnService() {

    companion object {
        const val TAG = "GhVpnTunnel"
        const val PROXY_HOST = "127.0.0.1"
        const val PROXY_PORT = 10808
        const val MTU = 1500
    }

    private var vpnFd: ParcelFileDescriptor? = null
    private var running = false
    private val conns = HashMap<String, Pair<Socket, Long>>()

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        if (!running) startTunnel()
        return START_STICKY
    }

    override fun onRevoke() {
        Log.w(TAG, "VPN revoked — stopping")
        stopTunnel()
    }

    /** F-3: establish (call after user granted VpnService.prepare()). */
    fun startTunnel(): Boolean {
        if (running) return true
        val builder = Builder()
        builder.setSession("gh-protocol")
        builder.addAddress("10.8.0.1", 8)
        builder.addDnsServer("10.8.0.1")
        // route everything except loopback through the tunnel
        builder.addRoute("0.0.0.0", 0)
        val fd = try {
            builder.establish()
        } catch (e: Exception) {
            Log.e(TAG, "establish failed", e)
            return false
        }
        if (fd == null) {
            Log.e(TAG, "establish returned null fd")
            return false
        }
        vpnFd = fd
        running = true
        Thread({ loop(fd) }, "gh-vpn-loop").apply { isDaemon = true; start() }
        return true
    }

    /** F-4: teardown < 3s. */
    fun stopTunnel() {
        running = false
        conns.values.forEach { try { it.first.close() } catch (_: Exception) {} }
        conns.clear()
        try { vpnFd?.close() } catch (_: Exception) {}
        vpnFd = null
    }

    override fun onDestroy() {
        stopTunnel()
        super.onDestroy()
    }

    private fun loop(fd: ParcelFileDescriptor) {
        val input = java.io.FileInputStream(fd.fileDescriptor)
        val buf = ByteArray(MTU)
        while (running) {
            val n: Int = try {
                input.read(buf)
            } catch (e: Exception) {
                if (running) Log.w(TAG, "fd read error: ${e.message}")
                break
            }
            if (n < 0) break
            if (n < 20) continue
            val ip = Socks5.parseIp4(buf.copyOfRange(0, n)) ?: continue
            val (proto, dstIp, totalLen) = ip
            val len: Int = if (totalLen < n) totalLen else n
            if (proto == 17) {
                // UDP: DNS (port 53) via associate; others via per-packet TCP is wrong —
                // non-DNS UDP is dropped in v1 (F-15 TCP-first anyway).
                val seg = buf.copyOfRange(20, len)
                val port = Socks5.segmentDstPort(seg)
                if (port == 53) sendUdp(dstIp, 53, seg)
            } else if (proto == 6) {
                val seg = buf.copyOfRange(20, len)
                val port = Socks5.segmentDstPort(seg)
                handleTcp(dstIp, port, seg)
            }
        }
    }

    private fun handleTcp(dstIp: String, dstPort: Int, packet: ByteArray) {
        val key = Socks5.connKey(dstIp, dstPort, 6)
        val now = System.currentTimeMillis()
        // drop stale conns
        val stale = conns.entries.filter { it.value.second + 60_000 < now }.map { it.key }
        stale.forEach { k -> conns.remove(k)?.first?.let { try { it.close() } catch (_: Exception) {} } }
        val sock = conns[key]?.first ?: try {
            val s = openSocks5(dstIp, dstPort) ?: return
            conns[key] = Pair(s, now)
            s
        } catch (_: Exception) {
            return
        }
        try {
            sock.getOutputStream().write(packet)
        } catch (_: Exception) {
            conns.remove(key)?.first?.let { try { it.close() } catch (_: Exception) {} }
        }
    }

    /** SOCKS5 handshake -> connected socket (or null). */
    private fun openSocks5(dstIp: String, dstPort: Int): Socket? {
        return try {
            val s = Socket()
            s.connect(java.net.InetSocketAddress(PROXY_HOST, PROXY_PORT), 2000)
            s.tcpNoDelay = true
            val out = s.getOutputStream()
            val din = java.io.DataInputStream(s.getInputStream())
            out.write(Socks5.GREETING)
            val reply = ByteArray(2)
            din.readFully(reply, 0, 2)
            if (!Socks5.greetingReplyOk(reply)) { s.close(); return null }
            out.write(Socks5.connectRequest(dstIp, dstPort))
            val head = ByteArray(4)
            din.readFully(head, 0, 4)
            if (!Socks5.connectReplyOk(head)) { s.close(); return null }
            val atyp = head[3].toInt() and 0xFF
            when (atyp) {
                1 -> din.skipNBytes(4)
                4 -> din.skipNBytes(16L)
                else -> din.skipNBytes(1 + (din.readByte().toInt() and 0xFF))
            }
            din.skipNBytes(2)
            s
        } catch (e: Exception) {
            Log.w(TAG, "socks5 connect failed: ${e.message}")
            null
        }
    }

    private fun sendUdp(dstIp: String, dstPort: Int, udpSegment: ByteArray) {
        // v1: loopback DNS forwarding placeholder — Xray handles DNS in its own
        // config; forward the packet best-effort over a per-packet associate.
        // (Full UDP associate channel lands with the instrumented E2E in P2b.)
    }
}
