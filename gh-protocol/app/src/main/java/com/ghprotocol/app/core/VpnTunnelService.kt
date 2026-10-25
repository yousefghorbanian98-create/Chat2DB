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
 * F-3/F-4: Bidirectional VpnService tunnel (Finn-loop v1.4).
 *
 * - Routes both IPv4 (0.0.0.0/0) and IPv6 (::/0) into the TUN to prevent IPv6 leaks.
 * - Performs real IPv4+TCP 3-way handshake (SYN -> SYN-ACK -> PSH-ACK/FIN-ACK)
 *   on the TUN file descriptor while relaying stream payloads over SOCKS5 to
 *   Xray's `mixed-in` (127.0.0.1:10808).
 * - Intercepts UDP port-53 DNS queries on the TUN and relays them to Xray's
 *   `dns-in` dokodemo-door (127.0.0.1:15353), with a VpnService.protect()ed
 *   fallback resolver when hypervisor NAT blocks outbound DoH.
 * - Guards against recursive outbound dials when Xray shares the app UID.
 */
class VpnTunnelService : VpnService() {

    companion object {
        const val TAG = "GhVpnTunnel"
        const val PROXY_HOST = "127.0.0.1"
        const val PROXY_PORT = 10808
        const val MTU = 1500
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
        @Volatile var lastActive: Long = System.currentTimeMillis()
    )

    private var vpnFd: ParcelFileDescriptor? = null
    @Volatile
    private var running = false
    private val tunWriteLock = Any()
    /** First N relay decisions are logged under GhDiag (privacy-masked destination IPs). */
    @Volatile
    private var diagBudget = 20
    private val sessions = ConcurrentHashMap<String, TcpSession>()
    /** Recursion guard: "$dstIp:$dstPort" -> (originClientPort to timestampMs). */
    private val activeTargetDials = ConcurrentHashMap<String, Pair<Int, Long>>()

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        promoteToForeground()
        if (!running) startTunnel()
        return START_STICKY
    }

    override fun onRevoke() {
        Log.w(TAG, "VPN revoked — stopping")
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
            .addAddress(TUNNEL_GW, 8)
            .addAddress(TUNNEL_GW_V6, 128)
            .addDnsServer(TUNNEL_GW)
            .addRoute("0.0.0.0", 0)
            .addRoute("::", 0) // Rule #2: prevent IPv6 leak
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
        sessions.values.forEach { s ->
            try { s.socket?.close() } catch (_: Exception) {}
        }
        sessions.clear()
        activeTargetDials.clear()
        try { vpnFd?.close() } catch (_: Exception) {}
        vpnFd = null
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
            val ip = Socks5.parseIp4(pkt) ?: continue // IPv6 packets captured by ::/0 are safely dropped (no leak)
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
                // Intercept all UDP DNS queries (port 53) and relay safely
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
            return
        }

        // SYN (new connection)
        if ((flags and 0x02) != 0 && (flags and 0x10) == 0) {
            val targetKey = "$dstIp:$dstPort"
            val existingDial = activeTargetDials[targetKey]
            if (existingDial != null && existingDial.first != clientPort && now - existingDial.second < 2000L) {
                // Recursive outbound dial from Xray sharing the app UID: reject with RST-ACK to prevent loop
                val rst = Socks5.buildTcpSegment(
                    srcIp = dstIp, srcPort = dstPort,
                    dstIp = clientIp, dstPort = clientPort,
                    seq = 0L, ack = (seq + 1L) and 0xFFFFFFFFL,
                    flags = 0x14
                )
                writeTun(tunOut, rst)
                return
            }
            activeTargetDials[targetKey] = Pair(clientPort, now)

            val existing = sessions[key]
            if (existing?.socket != null) {
                val synAck = Socks5.buildTcpSegment(
                    srcIp = dstIp, srcPort = dstPort,
                    dstIp = clientIp, dstPort = clientPort,
                    seq = 1000L, ack = (seq + 1L) and 0xFFFFFFFFL,
                    flags = 0x12
                )
                writeTun(tunOut, synAck)
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

            Thread({
                val sock = openSocks5(dstIp, dstPort)
                if (sock == null) {
                    sessions.remove(key)
                    val rst = Socks5.buildTcpSegment(
                        srcIp = dstIp, srcPort = dstPort,
                        dstIp = clientIp, dstPort = clientPort,
                        seq = 0L, ack = clientNext,
                        flags = 0x14
                    )
                    writeTun(tunOut, rst)
                    return@Thread
                }
                session.socket = sock
                session.lastActive = System.currentTimeMillis()
                if (diagBudget > 0) {
                    diagBudget--
                    Log.d("GhDiag", "relay tcp ${Socks5.maskIp(dstIp)}:$dstPort -> socks5 ok")
                }
                // Complete TCP 3-way handshake with SYN-ACK (seq=1000, ack=clientIsn+1)
                val synAck = Socks5.buildTcpSegment(
                    srcIp = dstIp, srcPort = dstPort,
                    dstIp = clientIp, dstPort = clientPort,
                    seq = 1000L, ack = clientNext,
                    flags = 0x12
                )
                writeTun(tunOut, synAck)
                pumpRemoteToTun(tunOut, session, sock)
            }, "gh-tcp-$clientPort").apply { isDaemon = true; start() }
            return
        }

        val session = sessions[key] ?: return
        session.lastActive = now

        if (payload.isNotEmpty()) {
            session.clientNextSeq = (seq + payload.size.toLong()) and 0xFFFFFFFFL
            val ackPkt = Socks5.buildTcpSegment(
                srcIp = dstIp, srcPort = dstPort,
                dstIp = clientIp, dstPort = clientPort,
                seq = session.serverSeq, ack = session.clientNextSeq,
                flags = 0x10
            )
            writeTun(tunOut, ackPkt)
            try {
                session.socket?.getOutputStream()?.let { out ->
                    out.write(payload)
                    out.flush()
                }
            } catch (_: Exception) {
                sessions.remove(key)?.let { s ->
                    try { s.socket?.close() } catch (_: Exception) {}
                }
                return
            }
        }

        if ((flags and 0x01) != 0) {
            // FIN from client -> reply FIN-ACK and close
            session.clientNextSeq = (session.clientNextSeq + 1L) and 0xFFFFFFFFL
            val finAck = Socks5.buildTcpSegment(
                srcIp = dstIp, srcPort = dstPort,
                dstIp = clientIp, dstPort = clientPort,
                seq = session.serverSeq, ack = session.clientNextSeq,
                flags = 0x11
            )
            writeTun(tunOut, finAck)
            sessions.remove(key)?.let { s ->
                try { s.socket?.close() } catch (_: Exception) {}
            }
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
        } catch (_: Exception) {
            // socket closed or reset
        } finally {
            try { sock.close() } catch (_: Exception) {}
            sessions.remove(session.key)
        }
    }

    /** SOCKS5 handshake -> connected socket (or null). */
    private fun openSocks5(dstIp: String, dstPort: Int): Socket? {
        val s = Socket()
        return try {
            s.connect(InetSocketAddress(PROXY_HOST, PROXY_PORT), 2500)
            s.soTimeout = 10_000
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
     * DNS relay: client UDP query on port 53 -> Xray dns-in (127.0.0.1:15353),
     * with a VpnService.protect()ed fallback to 10.0.2.3 / 8.8.8.8 when QEMU NAT
     * filters outbound DoH -> response injected directly into the TUN fd.
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
            val answer = queryUdpDns(DNS_UPSTREAM_HOST, DNS_UPSTREAM_PORT, payload, protectSocket = false, timeoutMs = 1500)
                ?: queryUdpDns("10.0.2.3", 53, payload, protectSocket = true, timeoutMs = 1500)
                ?: queryUdpDns("8.8.8.8", 53, payload, protectSocket = true, timeoutMs = 1500)
            if (answer != null && answer.isNotEmpty()) {
                val reply = Socks5.buildUdpSegment(
                    srcIp = dnsServerIp, srcPort = 53,
                    dstIp = clientIp, dstPort = clientPort,
                    payload = answer
                )
                if (diagBudget > 0) {
                    diagBudget--
                    Log.d("GhDiag", "relay dns -> ${answer.size}B ok")
                }
                writeTun(tunOut, reply)
            }
        }, "gh-dns-$clientPort").apply { isDaemon = true; start() }
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
