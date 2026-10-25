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
 * (127.0.0.1:10808) -> relay. TCP per 4-tuple with idle reuse; client DNS
 * (UDP to 10.8.0.1:53) is relayed to Xray's local DNS inbound on 127.0.0.1:15353.
 */
class VpnTunnelService : VpnService() {

    companion object {
        const val TAG = "GhVpnTunnel"
        const val PROXY_HOST = "127.0.0.1"
        const val PROXY_PORT = 10808
        const val MTU = 1500
        const val TUNNEL_GW = "10.8.0.1"
        const val DNS_UPSTREAM_HOST = "127.0.0.1"
        const val DNS_UPSTREAM_PORT = ConfigPatcher.DNS_IN_PORT
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
        Log.d("GhDiag", "tunnel: startTunnel called (running=$running)")
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
        Log.d("GhDiag", "tunnel: established fd=$fd — relay loop started")
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
            val pkt = buf.copyOfRange(0, n)
            val ip = Socks5.parseIp4(pkt) ?: continue
            val (proto, dstIp, totalLen) = ip
            val len: Int = if (totalLen < n) totalLen else n
            if (proto == 17) {
                // UDP: DNS to the tunnel gateway is relayed into Xray's dns inbound;
                // other UDP is dropped in v1 (F-15 TCP-first profile anyway).
                val port = Socks5.transportDstPort(pkt, 17)
                if (port == 53 && dstIp == TUNNEL_GW) {
                    sendUdp(pkt, Socks5.ipSrcIp(pkt), Socks5.transportSrcPort(pkt, 17))
                }
            } else if (proto == 6) {
                val port = Socks5.transportDstPort(pkt, 6)
                handleTcp(dstIp, port, buf.copyOfRange(20, len))
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
            // consume the bound-address block (ATYP: 1=IPv4 4B, 4=IPv6 16B, 3=domain)
            val atyp = head[3].toInt() and 0xFF
            val bindAddrLen = when (atyp) {
                1 -> 4
                4 -> 16
                3 -> 1 + (din.readByte().toInt() and 0xFF)
                else -> 0
            }
            din.readFully(ByteArray(bindAddrLen))
            din.readShort() // bound port — consumed
            s
        } catch (e: Exception) {
            Log.w(TAG, "socks5 connect failed: ${e.message}")
            null
        }
    }

    /**
     * DNS relay: client query (dst 10.8.0.1:53) -> Xray dns inbound (127.0.0.1:15353)
     * -> response routed back to the client address via the tunnel.
     */
    private fun sendUdp(udpPacket: ByteArray, clientIp: String, clientPort: Int) {
        // udpPacket = full IPv4+UDP packet (IP header 20B + UDP header 8B + payload)
        if (udpPacket.size < 28 || clientIp.isEmpty() || clientPort == 0) return
        Thread {
            var ds: java.net.DatagramSocket? = null
            var out: java.net.DatagramSocket? = null
            try {
                ds = java.net.DatagramSocket()
                ds.soTimeout = 2500
                val payload = udpPacket.copyOfRange(28, udpPacket.size)
                ds.send(java.net.DatagramPacket(
                    payload, payload.size,
                    java.net.InetAddress.getByName(DNS_UPSTREAM_HOST), DNS_UPSTREAM_PORT
                ))
                val respBuf = ByteArray(1500)
                val resp = java.net.DatagramPacket(respBuf, 0, respBuf.size)
                ds.receive(resp)
                val reply = Socks5.buildUdpSegment(TUNNEL_GW, DNS_UPSTREAM_PORT, clientIp, clientPort, resp.data, resp.offset, resp.length)
                out = java.net.DatagramSocket()
                out.send(java.net.DatagramPacket(reply, 0, reply.size, java.net.InetAddress.getByName(clientIp), clientPort))
            } catch (e: Exception) {
                Log.w(TAG, "dns relay failed: ${e.message}")
            } finally {
                try { ds?.close() } catch (_: Exception) {}
                try { out?.close() } catch (_: Exception) {}
            }
        }.apply { isDaemon = true }.start()
    }
}
