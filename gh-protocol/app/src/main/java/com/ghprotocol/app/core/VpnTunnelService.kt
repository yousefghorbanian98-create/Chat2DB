package com.ghprotocol.app.core

import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.content.Intent
import android.content.pm.ServiceInfo
import android.net.VpnService
import android.os.Build
import android.os.IBinder
import android.os.ParcelFileDescriptor
import android.util.Log
import java.io.DataInputStream
import java.io.FileInputStream
import java.io.FileOutputStream
import java.net.DatagramPacket
import java.net.DatagramSocket
import java.net.InetAddress
import java.net.InetSocketAddress
import java.net.Socket
import java.util.concurrent.ConcurrentHashMap

/**
 * F-3/F-4: Bidirectional VpnService tunnel (Finn-loop v1.5).
 *
 * Key real-device fixes:
 * 1. Calls `builder.addDisallowedApplication(packageName)` so the child `libxraycore.so`
 *    process (which shares the app UID) never routes its own outbound sockets back
 *    into `tun0` (preventing self-loop and RST-kill on real phones).
 * 2. Strict TCP sequence validation (`seq == session.clientNextSeq`), pre-connect payload
 *    buffering, and remote-EOF `FIN-ACK` injection so multi-segment TLS 1.3 (post-quantum
 *    ClientHello) and HTTPS streams never corrupt or hang.
 * 3. DNS relay via Xray `dns-in` (:15353) + RFC 1035 DNS-over-TCP through Xray SOCKS5
 *    (:10808 -> 1.1.1.1:53) + GFW poisoned-IP filter (`10.10.34.*` rejected).
 * 4. Real-time telemetry and step logs pushed to [TunnelLogBuffer].
 */
class VpnTunnelService : VpnService() {

    companion object {
        const val TAG = "GhVpnTunnel"
        const val PROXY_HOST = "127.0.0.1"
        const val PROXY_PORT = 10808
        const val MTU = 1500
        const val TUNNEL_ADDR = "10.8.0.2"
        const val TUNNEL_GW = "10.8.0.1"
        const val TUNNEL_GW_V6 = "fd00:1::1"
        const val DNS_UPSTREAM_HOST = "127.0.0.1"
        const val DNS_UPSTREAM_PORT = ConfigPatcher.DNS_IN_PORT
        private const val NOTIF_CHANNEL_ID = "gh_vpn_tunnel"
        private const val NOTIF_ID = 1001
    }

    private class TcpSession(
        val key: String,
        val clientIp: String,
        val clientPort: Int,
        val dstIp: String,
        val dstPort: Int,
        @Volatile var serverSeq: Long,
        @Volatile var clientNextSeq: Long,
        @Volatile var socket: Socket? = null,
        @Volatile var handshakeSent: Boolean = false,
        @Volatile var finSent: Boolean = false,
        @Volatile var lastActive: Long = System.currentTimeMillis()
    ) {
        val pendingPayloads = ArrayList<ByteArray>(2)
    }

    private var vpnFd: ParcelFileDescriptor? = null
    @Volatile
    private var running = false
    private val tunWriteLock = Any()
    @Volatile
    private var diagBudget = 25
    private val sessions = ConcurrentHashMap<String, TcpSession>()

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        promoteToForeground()
        if (!running) startTunnel()
        return START_STICKY
    }

    override fun onRevoke() {
        Log.w(TAG, "VPN revoked — stopping")
        TunnelLogBuffer.log(
            LogLevel.WARN,
            LogCategory.TUN,
            "دسترسی VPN توسط سیستم لغو شد",
            "VpnService.onRevoke() called — stopping tun0"
        )
        stopTunnel()
    }

    private fun promoteToForeground() {
        try {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                val nm = getSystemService(NotificationManager::class.java)
                val ch = NotificationChannel(
                    NOTIF_CHANNEL_ID,
                    "Gh Protocol VPN",
                    NotificationManager.IMPORTANCE_LOW
                )
                nm?.createNotificationChannel(ch)
                val notif = Notification.Builder(this, NOTIF_CHANNEL_ID)
                    .setContentTitle("Gh Protocol")
                    .setContentText("Tunnel active")
                    .setSmallIcon(android.R.drawable.ic_lock_lock)
                    .setOngoing(true)
                    .build()
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.UPSIDE_DOWN_CAKE) {
                    startForeground(NOTIF_ID, notif, ServiceInfo.FOREGROUND_SERVICE_TYPE_SPECIAL_USE)
                } else {
                    startForeground(NOTIF_ID, notif)
                }
            }
        } catch (e: Exception) {
            Log.w(TAG, "foreground promotion skipped: ${e.message}")
        }
    }

    /** F-3: establish (call after user granted VpnService.prepare()). */
    fun startTunnel(): Boolean {
        Log.d("GhDiag", "tunnel: startTunnel called (running=$running)")
        if (running) return true
        val builder = Builder()
            .setSession("gh-protocol")
            .setMtu(MTU)
            .addAddress(TUNNEL_ADDR, 24)
            .addAddress(TUNNEL_GW_V6, 128)
            .addDnsServer(TUNNEL_GW)
            .addRoute("0.0.0.0", 0)
            .addRoute("::", 0) // Rule #2: prevent IPv6 leak

        // CRITICAL FIX: Exclude our own package UID from tun0 so libxraycore.so's
        // outbound sockets exit directly via Wi-Fi/cellular without looping into tun0!
        try {
            builder.addDisallowedApplication(packageName)
            TunnelLogBuffer.log(
                LogLevel.INFO,
                LogCategory.TUN,
                "هستهٔ Xray از تونل مستثنی شد (جلوگیری از لوپ شبکه)",
                "VpnService.Builder: addDisallowedApplication($packageName) OK"
            )
        } catch (e: Exception) {
            Log.w(TAG, "addDisallowedApplication skipped: ${e.message}")
        }

        val fd = try {
            builder.establish()
        } catch (e: Exception) {
            Log.e(TAG, "establish failed", e)
            TunnelLogBuffer.log(
                LogLevel.ERROR,
                LogCategory.TUN,
                "خطا در ایجاد رابط مجازی tun0",
                "VpnService.establish() failed: ${e.message}"
            )
            return false
        }
        if (fd == null) {
            Log.e(TAG, "establish returned null fd")
            TunnelLogBuffer.log(
                LogLevel.ERROR,
                LogCategory.TUN,
                "سیستم اجازهٔ ایجاد تونل را نداد (fd=null)",
                "VpnService.establish() returned null"
            )
            return false
        }
        vpnFd = fd
        running = true
        Log.d("GhDiag", "tunnel: established fd=$fd — relay loop started")
        TunnelLogBuffer.log(
            LogLevel.SUCCESS,
            LogCategory.TUN,
            "رابط تونل tun0 برقرار شد (10.8.0.2/24 · MTU 1500)",
            "tun0 established: ipv4=$TUNNEL_ADDR/24 dns=$TUNNEL_GW ipv6=$TUNNEL_GW_V6/128"
        )
        Thread({ loop(fd) }, "gh-vpn-loop").apply { isDaemon = true; start() }
        return true
    }

    /** F-4: teardown < 3s. */
    fun stopTunnel() {
        running = false
        sessions.values.forEach { s ->
            try { s.socket?.close() } catch (_: Exception) {}
        }
        sessions.clear()
        try { vpnFd?.close() } catch (_: Exception) {}
        vpnFd = null
        TunnelLogBuffer.recordTraffic(0, 0, 0)
    }

    override fun onDestroy() {
        stopTunnel()
        super.onDestroy()
    }

    private fun writeTun(tunOut: FileOutputStream, pkt: ByteArray) {
        synchronized(tunWriteLock) {
            try {
                tunOut.write(pkt)
                tunOut.flush()
            } catch (e: Exception) {
                if (running) Log.w(TAG, "tun write error: ${e.message}")
            }
        }
    }

    private fun loop(fd: ParcelFileDescriptor) {
        val input = FileInputStream(fd.fileDescriptor)
        val output = FileOutputStream(fd.fileDescriptor)
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
            if (diagBudget > 0) {
                diagBudget--
                Log.d("GhDiag", "tun pkt proto=$proto dst=${Socks5.maskIp(dstIp)} len=$n")
            }
            val len: Int = if (totalLen in 20..n) totalLen else n
            val trimmed = if (len == pkt.size) pkt else pkt.copyOfRange(0, len)
            val srcIp = Socks5.ipSrcIp(trimmed)
            val srcPort = Socks5.transportSrcPort(trimmed, proto)
            val dstPort = Socks5.transportDstPort(trimmed, proto)
            if (proto == 17) {
                if (dstPort == 53) {
                    sendUdpDns(output, trimmed, dstIp, srcIp, srcPort)
                }
            } else if (proto == 6) {
                handleTcp(output, trimmed, srcIp, srcPort, dstIp, dstPort)
            }
        }
    }

    private fun handleTcp(
        tunOut: FileOutputStream,
        pkt: ByteArray,
        clientIp: String,
        clientPort: Int,
        dstIp: String,
        dstPort: Int
    ) {
        if (clientPort == 0 || dstPort == 0) return
        val key = "$clientIp:$clientPort->$dstIp:$dstPort"
        val flags = Socks5.tcpFlags(pkt)
        val seq = Socks5.tcpSeq(pkt)
        val payload = Socks5.tcpPayload(pkt)
        val now = System.currentTimeMillis()

        // Evict stale sessions (> 60s idle)
        sessions.entries.removeIf { (_, s) ->
            val expired = s.lastActive + 60_000L < now
            if (expired) {
                try { s.socket?.close() } catch (_: Exception) {}
            }
            expired
        }

        // RST: tear down immediately
        if ((flags and 0x04) != 0) {
            sessions.remove(key)?.let { s ->
                try { s.socket?.close() } catch (_: Exception) {}
            }
            TunnelLogBuffer.recordTraffic(0, 0, sessions.size)
            return
        }

        // SYN (new connection or SYN retransmit)
        if ((flags and 0x02) != 0 && (flags and 0x10) == 0) {
            val existing = sessions[key]
            if (existing != null) {
                existing.lastActive = now
                if (existing.handshakeSent) {
                    val synAck = Socks5.buildTcpSegment(
                        srcIp = dstIp, srcPort = dstPort,
                        dstIp = clientIp, dstPort = clientPort,
                        seq = 1000L, ack = existing.clientNextSeq,
                        flags = 0x12
                    )
                    writeTun(tunOut, synAck)
                }
                return
            }

            val clientNext = (seq + 1L) and 0xFFFFFFFFL
            val session = TcpSession(
                key = key,
                clientIp = clientIp,
                clientPort = clientPort,
                dstIp = dstIp,
                dstPort = dstPort,
                serverSeq = 1001L,
                clientNextSeq = clientNext
            )
            sessions[key] = session
            TunnelLogBuffer.recordTraffic(0, 0, sessions.size)

            Thread({
                val sock = openSocks5(dstIp, dstPort)
                if (sock == null) {
                    sessions.remove(key)
                    TunnelLogBuffer.recordTraffic(0, 0, sessions.size)
                    val rst = Socks5.buildTcpSegment(
                        srcIp = dstIp, srcPort = dstPort,
                        dstIp = clientIp, dstPort = clientPort,
                        seq = 0L, ack = clientNext,
                        flags = 0x14
                    )
                    writeTun(tunOut, rst)
                    return@Thread
                }
                synchronized(session) {
                    session.socket = sock
                    session.handshakeSent = true
                    session.lastActive = System.currentTimeMillis()
                    // Complete TCP 3-way handshake with SYN-ACK (seq=1000, ack=clientIsn+1)
                    val synAck = Socks5.buildTcpSegment(
                        srcIp = dstIp, srcPort = dstPort,
                        dstIp = clientIp, dstPort = clientPort,
                        seq = 1000L, ack = session.clientNextSeq,
                        flags = 0x12
                    )
                    writeTun(tunOut, synAck)
                    if (session.pendingPayloads.isNotEmpty()) {
                        try {
                            val out = sock.getOutputStream()
                            for (chunk in session.pendingPayloads) {
                                out.write(chunk)
                            }
                            out.flush()
                        } catch (_: Exception) {}
                        session.pendingPayloads.clear()
                    }
                }
                Log.d("GhDiag", "relay tcp ${Socks5.maskIp(dstIp)}:$dstPort -> socks5 ok")
                pumpRemoteToTun(tunOut, session, sock)
            }, "gh-tcp-$clientPort").apply { isDaemon = true; start() }
            return
        }

        val session = sessions[key] ?: return
        session.lastActive = now

        if (payload.isNotEmpty()) {
            synchronized(session) {
                if (seq == session.clientNextSeq) {
                    session.clientNextSeq = (seq + payload.size.toLong()) and 0xFFFFFFFFL
                    val ackPkt = Socks5.buildTcpSegment(
                        srcIp = dstIp, srcPort = dstPort,
                        dstIp = clientIp, dstPort = clientPort,
                        seq = session.serverSeq, ack = session.clientNextSeq,
                        flags = 0x10
                    )
                    writeTun(tunOut, ackPkt)
                    val sock = session.socket
                    if (sock != null) {
                        try {
                            val out = sock.getOutputStream()
                            out.write(payload)
                            out.flush()
                            TunnelLogBuffer.recordTraffic(payload.size, 0, sessions.size)
                        } catch (_: Exception) {
                            sessions.remove(key)?.let { s ->
                                try { s.socket?.close() } catch (_: Exception) {}
                            }
                            return
                        }
                    } else {
                        session.pendingPayloads.add(payload)
                    }
                } else {
                    // Retransmitted or out-of-order segment: re-ACK expected sequence without duplicating stream bytes
                    val dupAck = Socks5.buildTcpSegment(
                        srcIp = dstIp, srcPort = dstPort,
                        dstIp = clientIp, dstPort = clientPort,
                        seq = session.serverSeq, ack = session.clientNextSeq,
                        flags = 0x10
                    )
                    writeTun(tunOut, dupAck)
                }
            }
        }

        if ((flags and 0x01) != 0) {
            synchronized(session) {
                session.clientNextSeq = (session.clientNextSeq + 1L) and 0xFFFFFFFFL
                session.finSent = true
                val finAck = Socks5.buildTcpSegment(
                    srcIp = dstIp, srcPort = dstPort,
                    dstIp = clientIp, dstPort = clientPort,
                    seq = session.serverSeq, ack = session.clientNextSeq,
                    flags = 0x11
                )
                session.serverSeq = (session.serverSeq + 1L) and 0xFFFFFFFFL
                writeTun(tunOut, finAck)
            }
            sessions.remove(key)?.let { s ->
                try { s.socket?.close() } catch (_: Exception) {}
            }
            TunnelLogBuffer.recordTraffic(0, 0, sessions.size)
        }
    }

    private fun pumpRemoteToTun(tunOut: FileOutputStream, session: TcpSession, sock: Socket) {
        val readBuf = ByteArray(1360)
        try {
            val ins = sock.getInputStream()
            while (running && !sock.isClosed) {
                val r = ins.read(readBuf)
                if (r < 0) break
                if (r == 0) continue
                val chunk = readBuf.copyOfRange(0, r)
                synchronized(session) {
                    val seg = Socks5.buildTcpSegment(
                        srcIp = session.dstIp, srcPort = session.dstPort,
                        dstIp = session.clientIp, dstPort = session.clientPort,
                        seq = session.serverSeq, ack = session.clientNextSeq,
                        flags = 0x18, // PSH-ACK
                        payload = chunk
                    )
                    session.serverSeq = (session.serverSeq + r.toLong()) and 0xFFFFFFFFL
                    session.lastActive = System.currentTimeMillis()
                    writeTun(tunOut, seg)
                }
                TunnelLogBuffer.recordTraffic(0, r, sessions.size)
            }
            // Send FIN-ACK to client when remote server closes stream cleanly
            synchronized(session) {
                if (running && !session.finSent) {
                    session.finSent = true
                    val finAck = Socks5.buildTcpSegment(
                        srcIp = session.dstIp, srcPort = session.dstPort,
                        dstIp = session.clientIp, dstPort = session.clientPort,
                        seq = session.serverSeq, ack = session.clientNextSeq,
                        flags = 0x11 // FIN-ACK
                    )
                    session.serverSeq = (session.serverSeq + 1L) and 0xFFFFFFFFL
                    writeTun(tunOut, finAck)
                }
            }
        } catch (_: Exception) {
            // socket closed or reset
        } finally {
            try { sock.close() } catch (_: Exception) {}
            sessions.remove(session.key)
            TunnelLogBuffer.recordTraffic(0, 0, sessions.size)
        }
    }

    /** SOCKS5 handshake -> connected socket (or null). */
    private fun openSocks5(dstIp: String, dstPort: Int): Socket? {
        val s = Socket()
        return try {
            s.connect(InetSocketAddress(PROXY_HOST, PROXY_PORT), 4000)
            s.soTimeout = 15_000
            s.tcpNoDelay = true
            val out = s.getOutputStream()
            val din = DataInputStream(s.getInputStream())
            out.write(Socks5.GREETING)
            out.flush()
            val reply = ByteArray(2)
            din.readFully(reply, 0, 2)
            if (!Socks5.greetingReplyOk(reply)) {
                s.close()
                return null
            }
            out.write(Socks5.connectRequest(dstIp, dstPort))
            out.flush()
            val head = ByteArray(4)
            din.readFully(head, 0, 4)
            if (!Socks5.connectReplyOk(head)) {
                s.close()
                return null
            }
            val atyp = head[3].toInt() and 0xFF
            val bindAddrLen = when (atyp) {
                1 -> 4
                4 -> 16
                3 -> (din.readByte().toInt() and 0xFF)
                else -> 0
            }
            if (bindAddrLen > 0) {
                din.readFully(ByteArray(bindAddrLen))
            }
            din.readShort() // bound port
            s
        } catch (e: Exception) {
            try { s.close() } catch (_: Exception) {}
            Log.w(TAG, "socks5 connect failed: ${e.message}")
            null
        }
    }

    /**
     * DNS relay:
     * 1. Xray `dns-in` dokodemo-door (127.0.0.1:15353, 3500ms timeout for cold DoH).
     * 2. RFC 1035 DNS-over-TCP through Xray SOCKS5 (:10808 -> 1.1.1.1:53 / 8.8.8.8:53)
     *    so DNS stays inside the anti-DPI tunnel and avoids UDP port-53 poisoning.
     * 3. Emulator-safe fallback (rejects poisoned 10.10.34.* responses).
     */
    private fun sendUdpDns(
        tunOut: FileOutputStream,
        udpPacket: ByteArray,
        dnsServerIp: String,
        clientIp: String,
        clientPort: Int
    ) {
        val ihl = Socks5.ipHeaderLen(udpPacket)
        if (udpPacket.size <= ihl + 8 || clientIp.isEmpty() || clientPort == 0) return
        val payload = udpPacket.copyOfRange(ihl + 8, udpPacket.size)
        Thread({
            val answer = queryUdpDns(DNS_UPSTREAM_HOST, DNS_UPSTREAM_PORT, payload, protectSocket = false, timeoutMs = 3000)
                ?.takeIf { isUsableDnsResponse(it) }
                ?: queryTcpDnsOverSocks5("1.1.1.1", 53, payload, timeoutMs = 3000)?.takeIf { isUsableDnsResponse(it) }
                ?: queryTcpDnsOverSocks5("8.8.8.8", 53, payload, timeoutMs = 3000)?.takeIf { isUsableDnsResponse(it) }
                ?: queryUdpDns("1.1.1.1", 53, payload, protectSocket = true, timeoutMs = 2000)?.takeIf { isUsableDnsResponse(it) }
                ?: queryUdpDns("8.8.8.8", 53, payload, protectSocket = true, timeoutMs = 2000)?.takeIf { isUsableDnsResponse(it) }
            if (answer != null && answer.isNotEmpty()) {
                val reply = Socks5.buildUdpSegment(
                    srcIp = dnsServerIp, srcPort = 53,
                    dstIp = clientIp, dstPort = clientPort,
                    payload = answer
                )
                Log.d("GhDiag", "relay dns -> ${answer.size}B ok")
                TunnelLogBuffer.recordDnsHandled()
                writeTun(tunOut, reply)
            }
        }, "gh-dns-$clientPort").apply { isDaemon = true; start() }
    }

    /**
     * Reject DNS SERVFAIL (rcode=2), REFUSED (rcode=5), truncated headers,
     * and Iranian ISP DNS-poisoning responses (10.10.34.*).
     */
    private fun isUsableDnsResponse(ans: ByteArray): Boolean {
        if (ans.size < 12) return false
        val rcode = ans[3].toInt() and 0x0F
        if (rcode == 2 || rcode == 4 || rcode == 5) return false
        return !isPoisonedDnsAnswer(ans)
    }

    /** RFC 1035 §4.2.2 DNS-over-TCP (2-byte big-endian length prefix) via Xray SOCKS5. */
    private fun queryTcpDnsOverSocks5(
        dnsHost: String,
        dnsPort: Int,
        payload: ByteArray,
        timeoutMs: Int
    ): ByteArray? {
        val sock = openSocks5(dnsHost, dnsPort) ?: return null
        return try {
            sock.use { s ->
                s.soTimeout = timeoutMs
                val out = s.getOutputStream()
                val din = DataInputStream(s.getInputStream())
                val lenHi = ((payload.size shr 8) and 0xFF).toByte()
                val lenLo = (payload.size and 0xFF).toByte()
                out.write(byteArrayOf(lenHi, lenLo))
                out.write(payload)
                out.flush()
                val respLen = din.readUnsignedShort()
                if (respLen in 12..4096) {
                    val ans = ByteArray(respLen)
                    din.readFully(ans)
                    ans
                } else {
                    null
                }
            }
        } catch (_: Exception) {
            null
        }
    }

    /** Reject Iranian ISP DNS-poisoning responses containing 10.10.34.34 / 10.10.34.35 / 10.10.34.36. */
    private fun isPoisonedDnsAnswer(ans: ByteArray): Boolean {
        if (ans.size < 16) return false
        for (i in 0..(ans.size - 4)) {
            val b0 = ans[i].toInt() and 0xFF
            val b1 = ans[i + 1].toInt() and 0xFF
            val b2 = ans[i + 2].toInt() and 0xFF
            if (b0 == 10 && b1 == 10 && b2 == 34) return true
        }
        return false
    }

    private fun queryUdpDns(
        host: String,
        port: Int,
        payload: ByteArray,
        protectSocket: Boolean,
        timeoutMs: Int
    ): ByteArray? {
        return try {
            DatagramSocket().use { ds ->
                if (protectSocket) {
                    protect(ds)
                }
                ds.soTimeout = timeoutMs
                ds.send(DatagramPacket(payload, payload.size, InetAddress.getByName(host), port))
                val respBuf = ByteArray(1500)
                val resp = DatagramPacket(respBuf, 0, respBuf.size)
                ds.receive(resp)
                resp.data.copyOfRange(resp.offset, resp.offset + resp.length)
            }
        } catch (_: Exception) {
            null
        }
    }
}
