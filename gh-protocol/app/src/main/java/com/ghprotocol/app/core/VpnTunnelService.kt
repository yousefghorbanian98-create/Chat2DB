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
import com.ghprotocol.app.core.net.DnsMessage
import com.ghprotocol.app.core.net.DnsResolver
import com.ghprotocol.app.core.net.DnsUpstreams
import com.ghprotocol.app.core.net.PacketCodec
import com.ghprotocol.app.core.net.RelayConfig
import com.ghprotocol.app.core.net.RelayEvents
import com.ghprotocol.app.core.net.RelayStats
import com.ghprotocol.app.core.net.Socks5Connector
import com.ghprotocol.app.core.net.TcpRelay
import com.ghprotocol.app.core.net.TunSink
import com.ghprotocol.app.core.net.TunnelSelfTest
import com.ghprotocol.app.core.net.TunnelSelfTestResult
import java.io.FileInputStream
import java.io.FileOutputStream
import java.util.concurrent.ArrayBlockingQueue
import java.util.concurrent.ThreadPoolExecutor
import java.util.concurrent.TimeUnit
import java.util.concurrent.atomic.AtomicBoolean
import java.util.concurrent.atomic.AtomicInteger

/**
 * Android shell around the tested userspace datapath.
 *
 * What lives here (and only here): VpnService lifecycle, tun file descriptor, packet pump.
 * Everything that can be proven on a plain JVM lives in `com.ghprotocol.app.core.net`:
 *  - [TcpRelay]       IPv4 **and** IPv6 TCP ⇄ SOCKS5 (Xray :10808), with real counters
 *  - [DnsResolver]    validated DoH → TCP DNS → Xray dns-in, hard budget, real SERVFAIL
 *  - [TunnelSelfTest] the ONLY source of the `VERIFIED` state (real remote payload)
 *
 * v1.6 fixes (DIAGNOSIS 2026-10-25): IPv6 is either really tunneled or explicitly reported
 * as unavailable (never silently dropped while claiming leak protection); byte counters are
 * copied from the relay; UDP that cannot be relayed is counted *and* answered with ICMP
 * port-unreachable so QUIC apps fall back to TCP instead of hanging.
 */
class VpnTunnelService : VpnService() {

    companion object {
        const val TAG = "GhVpnTunnel"
        const val ACTION_CONNECT = "com.ghprotocol.app.action.CONNECT"
        const val ACTION_SELF_TEST = "com.ghprotocol.app.action.SELF_TEST"

        const val PROXY_HOST = "127.0.0.1"
        const val PROXY_PORT = 10808
        const val DNS_IN_PORT = ConfigPatcher.DNS_IN_PORT
        const val MTU = 1500
        const val TUNNEL_ADDR = "10.8.0.2"
        const val TUNNEL_GW = "10.8.0.1"
        const val TUNNEL_ADDR_V6 = "fd00:1::2"
        const val TUNNEL_GW_V6 = "fd00:1::1"

        private const val NOTIF_CHANNEL_ID = "gh_vpn_tunnel"
        private const val NOTIF_ID = 1001

        /** Result of the last in-tunnel payload test (single VpnService per process). */
        @Volatile
        var lastSelfTest: TunnelSelfTestResult? = null

        data class SelfTestTarget(val ip: String, val port: Int, val hostHeader: String, val path: String?)

        /** Targets used to prove real payload through the tunnel, in preference order. */
        val SELF_TEST_TARGETS = listOf(
            SelfTestTarget("1.1.1.1", 80, "one.one.one.one", "/cdn-cgi/trace"),
            SelfTestTarget("104.16.248.249", 80, "cp.cloudflare.com", "/cdn-cgi/trace"),
            SelfTestTarget("8.8.8.8", 53, "dns.google", null)
        )

        @Volatile
        var isRunning: Boolean = false
            private set

        /**
         * Ask the running service for a *fresh* in-tunnel payload test. Clears the previous
         * result first so callers can never read a stale "verified" from before a restart.
         */
        fun requestSelfTest(context: android.content.Context) {
            if (!isRunning) return
            lastSelfTest = null
            try {
                val intent = Intent(context, VpnTunnelService::class.java).setAction(ACTION_SELF_TEST)
                context.startService(intent)
            } catch (e: Exception) {
                Log.w(TAG, "cannot request self-test: ${e.message}")
            }
        }
    }

    private var vpnFd: ParcelFileDescriptor? = null
    private var tunInput: FileInputStream? = null
    private var tunOutput: FileOutputStream? = null
    private val running = AtomicBoolean(false)
    private val tunWriteLock = Any()

    @Volatile
    private var relay: TcpRelay? = null

    @Volatile
    private var dnsResolver: DnsResolver? = null

    private val diagBudget = AtomicInteger(30)

    /** Bounded DNS executor: a DNS storm must never create unbounded threads. */
    private val dnsPool = ThreadPoolExecutor(
        1, 2, 30L, TimeUnit.SECONDS, ArrayBlockingQueue(96),
        { runnable -> Thread(runnable, "gh-dns").apply { isDaemon = true } },
        ThreadPoolExecutor.DiscardPolicy()
    )

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        promoteToForeground()
        when (intent?.action) {
            ACTION_SELF_TEST -> runSelfTestAsync()
            else -> if (!running.get()) startTunnel()
        }
        return START_STICKY
    }

    override fun onRevoke() {
        Log.w(TAG, "VPN revoked by the system — stopping")
        TunnelLogBuffer.log(
            LogLevel.WARN, LogCategory.TUN,
            "دسترسی VPN توسط سیستم لغو شد (تونل بسته شد)",
            "VpnService.onRevoke()"
        )
        stopTunnel()
    }

    private fun promoteToForeground() {
        try {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                val manager = getSystemService(NotificationManager::class.java)
                manager?.createNotificationChannel(
                    NotificationChannel(NOTIF_CHANNEL_ID, "Gh Protocol VPN", NotificationManager.IMPORTANCE_LOW)
                )
                val notification = Notification.Builder(this, NOTIF_CHANNEL_ID)
                    .setContentTitle("Gh Protocol")
                    .setContentText("تونل فعال است")
                    .setSmallIcon(android.R.drawable.ic_lock_lock)
                    .setOngoing(true)
                    .build()
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.UPSIDE_DOWN_CAKE) {
                    startForeground(NOTIF_ID, notification, ServiceInfo.FOREGROUND_SERVICE_TYPE_SPECIAL_USE)
                } else {
                    startForeground(NOTIF_ID, notification)
                }
            }
        } catch (e: Exception) {
            Log.w(TAG, "foreground promotion skipped: ${e.message}")
        }
    }

    /** Establish tun0 and start the datapath. Returns false when the platform refused. */
    fun startTunnel(): Boolean {
        if (running.get()) return true
        TunnelLogBuffer.setTunnelState(TunnelState.STARTING, "establishing tun0")
        val builder = Builder()
            .setSession("gh-protocol")
            .setMtu(MTU)
            .addAddress(TUNNEL_ADDR, 24)
            .addDnsServer(TUNNEL_GW)
            .addRoute("0.0.0.0", 0)

        // IPv6: really tunneled (TCP + DNS) when the platform accepts the address, otherwise
        // reported as unavailable so no "IPv6 leak protection" claim is made for dropped v6.
        val ipv6 = try {
            builder.addAddress(TUNNEL_ADDR_V6, 64)
            builder.addRoute("::", 0)
            builder.addDnsServer(TUNNEL_GW_V6)
            true
        } catch (e: Exception) {
            Log.w(TAG, "IPv6 address/route rejected: ${e.message}")
            false
        }

        try {
            // Xray runs in this UID: it must reach the network directly or its outbound would
            // be captured by our own tun0 (classic VPN loop).
            builder.addDisallowedApplication(packageName)
            TunnelLogBuffer.log(
                LogLevel.INFO, LogCategory.TUN,
                "هستهٔ Xray از تونل مستثنی شد (جلوگیری از لوپ شبکه)",
                "Builder.addDisallowedApplication($packageName)"
            )
        } catch (e: Exception) {
            Log.w(TAG, "addDisallowedApplication failed: ${e.message}")
        }

        val fd = try {
            builder.establish()
        } catch (e: Exception) {
            Log.e(TAG, "establish threw", e)
            TunnelLogBuffer.log(
                LogLevel.ERROR, LogCategory.TUN,
                "ایجاد رابط tun0 با خطا مواجه شد",
                "establish() threw ${e.javaClass.simpleName}: ${e.message}"
            )
            TunnelLogBuffer.setTunnelState(TunnelState.FAILED, "establish_threw")
            return false
        }
        if (fd == null) {
            TunnelLogBuffer.log(
                LogLevel.ERROR, LogCategory.TUN,
                "سیستم اجازهٔ ساخت تونل را نداد (fd=null)",
                "establish() returned null"
            )
            TunnelLogBuffer.setTunnelState(TunnelState.FAILED, "establish_null")
            return false
        }

        val input = FileInputStream(fd.fileDescriptor)
        val output = FileOutputStream(fd.fileDescriptor)
        vpnFd = fd
        tunInput = input
        tunOutput = output
        running.set(true)
        isRunning = true

        TunnelLogBuffer.setIpv6Mode(if (ipv6) "tunneled" else "unavailable")
        TunnelLogBuffer.log(
            LogLevel.SUCCESS, LogCategory.TUN,
            if (ipv6) {
                "رابط tun0 برقرار شد — IPv4 و IPv6 هر دو تونل می‌شوند"
            } else {
                "رابط tun0 برقرار شد (فقط IPv4)؛ IPv6 در این دستگاه تونل نمی‌شود"
            },
            "tun0 established ipv4=$TUNNEL_ADDR/24 ipv6=" +
                (if (ipv6) "$TUNNEL_ADDR_V6/64 route=::/0" else "unavailable") +
                " dns=$TUNNEL_GW mtu=$MTU"
        )

        Log.d(
            "GhDiag",
            "tun0 established ipv4=$TUNNEL_ADDR/24 ipv6=" +
                (if (ipv6) "$TUNNEL_ADDR_V6/64 route=::/0" else "unavailable") +
                " dns=$TUNNEL_GW mtu=$MTU"
        )
        buildDatapath(output)
        TunnelLogBuffer.setTunnelState(TunnelState.CORE_READY, "tun_up ipv6=$ipv6")
        Thread({ readLoop(input, output) }, "gh-tun-read").apply { isDaemon = true; start() }
        runSelfTestAsync()
        return true
    }

    private fun buildDatapath(output: FileOutputStream) {
        val connector = Socks5Connector(PROXY_HOST, PROXY_PORT)
        val sink = object : TunSink {
            override fun write(packet: ByteArray): Boolean = writeTun(output, packet)
        }
        relay = TcpRelay(
            sink = sink,
            connector = connector,
            events = RelayEventsImpl(),
            config = RelayConfig(
                mss = 1300,
                connectTimeoutMs = 8_000,
                connectReplyTimeoutMs = 12_000,
                idleTimeoutMs = 300_000L
            )
        )
        dnsResolver = DnsResolver(
            transports = DnsUpstreams.defaultChain(connector, DNS_IN_PORT),
            budgetMs = 5_000,
            perPathMaxMs = 2_500,
            events = DnsEventsImpl()
        )
        TunnelLogBuffer.log(
            LogLevel.INFO, LogCategory.DNS,
            "زنجیرهٔ DNS فعال: DoH کلادفلر → DoH گوگل → DNS روی TCP → dns-in هسته",
            "dns_chain=" + DnsUpstreams.defaultChain(connector, DNS_IN_PORT).joinToString(",") { it.name }
        )
    }

    /** Tear down tun0 and every flow; bounded to a few hundred milliseconds. */
    fun stopTunnel() {
        running.set(false)
        isRunning = false
        relay?.shutdown("tunnel_stopped")
        relay = null
        dnsResolver = null
        try { tunInput?.close() } catch (_: Exception) { }
        try { tunOutput?.close() } catch (_: Exception) { }
        tunInput = null
        tunOutput = null
        try { vpnFd?.close() } catch (_: Exception) { }
        vpnFd = null
        TunnelLogBuffer.setRelayStats(RelayStats())
        TunnelLogBuffer.setTunnelState(TunnelState.IDLE, "stopped")
    }

    override fun onDestroy() {
        stopTunnel()
        dnsPool.shutdownNow()
        super.onDestroy()
    }

    private fun writeTun(output: FileOutputStream, packet: ByteArray): Boolean {
        synchronized(tunWriteLock) {
            return try {
                output.write(packet)
                output.flush()
                true
            } catch (e: Exception) {
                if (running.get()) Log.w(TAG, "tun write failed: ${e.message}")
                false
            }
        }
    }

    private fun readLoop(input: FileInputStream, output: FileOutputStream) {
        val buffer = ByteArray(MTU + 512)
        while (running.get()) {
            val read = try {
                input.read(buffer)
            } catch (e: Exception) {
                if (running.get()) Log.w(TAG, "tun read failed: ${e.message}")
                break
            }
            if (read <= 0) continue
            val packet = PacketCodec.parse(buffer, read)
            if (packet == null) {
                Log.d("GhDiag", "tun_parse_fail len=$read")
                continue
            }
            if (diagBudget.getAndDecrement() > 0) {
                Log.d(
                    "GhDiag",
                    "tun v${packet.family} proto=${packet.protocol} " +
                        "dst=${PacketCodec.maskIp(packet.dstIp)}:${packet.dstPort} len=$read"
                )
            }
            when (packet.protocol) {
                PacketCodec.PROTO_TCP -> {
                    val active = relay
                    if (active != null) {
                        active.onPacket(buffer.copyOf(read))
                    } else {
                        Log.d("GhDiag", "tcp packet dropped: relay not running")
                    }
                }
                PacketCodec.PROTO_UDP -> if (packet.dstPort == 53) {
                    handleDns(packet, output)
                } else {
                    // QUIC / other UDP is not relayed: counted, and answered with a real ICMP
                    // port-unreachable so the app retries over TCP instead of hanging.
                    TunnelLogBuffer.recordUdpDropped()
                    PacketCodec.buildPortUnreachable(packet)?.let { writeTun(output, it) }
                }
                else -> TunnelLogBuffer.recordUdpDropped()
            }
        }
        Log.d("GhDiag", "tun read loop exited")
    }

    /**
     * DNS: every port-53 UDP query is answered by [DnsResolver] (validated DoH through the
     * tunnel's SOCKS5 → TCP DNS → Xray dns-in) or with a real SERVFAIL for that transaction.
     * No answer is fabricated, AAAA is never special-cased.
     */
    private fun handleDns(packet: PacketCodec.IpFlow, output: FileOutputStream) {
        val resolver = dnsResolver ?: return
        val query = packet.payload
        if (query.size < 12) return
        val started = System.currentTimeMillis()
        dnsPool.execute {
            try {
                val resolution = resolver.resolve(query)
                val reply = PacketCodec.buildUdp(
                    family = packet.family,
                    srcIp = packet.dstIp, srcPort = packet.dstPort,
                    dstIp = packet.srcIp, dstPort = packet.srcPort,
                    payload = resolution.response
                )
                if (reply != null) writeTun(output, reply)
                if (diagBudget.get() > -10) {
                    Log.d(
                        "GhDiag",
                        "dns_reply ${System.currentTimeMillis() - started}ms path=${resolution.path} " +
                            "bytes=${resolution.response.size}"
                    )
                }
            } catch (e: Exception) {
                Log.w(TAG, "dns relay failed: ${e.message}")
            }
        }
    }

    private inner class DnsEventsImpl : com.ghprotocol.app.core.net.DnsEvents {
        override fun onResolved(query: ByteArray, resolution: com.ghprotocol.app.core.net.DnsResolution) {
            val view = DnsMessage.parse(resolution.response)
            TunnelLogBuffer.recordDnsResult(
                path = resolution.path,
                ms = resolution.ms,
                ok = true,
                detail = "rcode=${view?.rcode ?: -1} answers=${view?.answerCount ?: -1}"
            )
            Log.d("GhDiag", "dns_ok path=${resolution.path} ms=${resolution.ms}")
        }

        override fun onFailed(query: ByteArray, attempts: List<com.ghprotocol.app.core.net.DnsAttempt>) {
            val detail = attempts.joinToString(",") { "${it.path}:${it.detail.take(40)}" }
            TunnelLogBuffer.recordDnsResult(
                path = "servfail",
                ms = 0,
                ok = false,
                detail = detail
            )
            Log.w("GhDiag", "dns_failed attempts=[$detail]")
            TunnelLogBuffer.log(
                LogLevel.WARN, LogCategory.DNS,
                "پاسخ DNS از هیچ مسیری نیامد — SERVFAIL واقعی به برنامه برگشت",
                "dns_servfail attempts=[${detail.take(300)}]"
            )
        }
    }

    private inner class RelayEventsImpl : RelayEvents {
        override fun onFlowOpened(key: String, dstIp: String, dstPort: Int) {
            Log.d("GhDiag", "flow_open ${PacketCodec.maskIp(dstIp)}:$dstPort")
        }

        override fun onFlowEstablished(key: String, connectMs: Long) {
            Log.d("GhDiag", "flow_established ${connectMs}ms")
        }

        override fun onFlowFailed(key: String, stage: String, detail: String) {
            Log.w("GhDiag", "flow_failed stage=$stage detail=$detail")
            TunnelLogBuffer.log(
                LogLevel.WARN, LogCategory.TUN,
                "اتصال TCP برقرار نشد (مرحلهٔ $stage)",
                "flow_failed stage=$stage detail=$detail key=$key"
            )
        }

        override fun onFlowClosed(key: String, reason: String, upBytes: Long, downBytes: Long, durationMs: Long) {
            Log.d("GhDiag", "flow_closed reason=$reason up=$upBytes down=$downBytes ms=$durationMs")
        }

        override fun onTraffic(upBytes: Long, downBytes: Long, activeFlows: Int) {
            // Absolute values from the relay — the UI never accumulates on its own.
            val stats = relay?.stats()
            if (stats != null) TunnelLogBuffer.setRelayStats(stats)
        }

        override fun onWarning(stage: String, detail: String) {
            Log.w("GhDiag", "relay_warning stage=$stage detail=$detail")
        }
    }

    // ------------------------------------------------------------------ verification

    private fun runSelfTestAsync() {
        Thread({
            val result = runSelfTest()
            lastSelfTest = result
            Log.d(
                "GhDiag",
                "relay_selftest ok=${result.ok} stage=${result.stage} target=${result.target} " +
                    "up=${result.upBytesDelta} down=${result.downBytesDelta} response=${result.responseBytes} " +
                    "synAckMs=${result.synAckMs} firstByteMs=${result.firstByteMs} checksums=${result.checksumErrors}"
            )
            if (result.ok) {
                TunnelLogBuffer.setVerifiedPing(result.latencyMs.toInt())
                TunnelLogBuffer.setTunnelState(
                    TunnelState.VERIFIED,
                    "selftest probe=${result.target} down=${result.downBytesDelta}",
                    payloadVerified = true
                )
                TunnelLogBuffer.updateStep(5, "متصل و تاییدشده (دریافت واقعی داده از راه دور)")
                TunnelLogBuffer.log(
                    LogLevel.SUCCESS, LogCategory.PROBE,
                    "✓ عبور واقعی داده از تونل تایید شد (${result.target} · ↓${result.responseBytes} بایت · ${result.latencyMs} ms)",
                    "relay_selftest=PASS target=${result.target} responseBytes=${result.responseBytes} " +
                        "up=${result.upBytesDelta} down=${result.downBytesDelta} checksumErrors=${result.checksumErrors}"
                )
            } else {
                TunnelLogBuffer.setVerifiedPing(null)
                TunnelLogBuffer.setTunnelState(
                    TunnelState.DEGRADED,
                    "selftest ${result.stage}: ${result.detail}"
                )
                TunnelLogBuffer.log(
                    LogLevel.WARN, LogCategory.PROBE,
                    "تست عبور دادهٔ واقعی ناموفق بود (مرحلهٔ ${result.stage})",
                    "relay_selftest=FAIL stage=${result.stage} detail=${result.detail} " +
                        "up=${result.upBytesDelta} down=${result.downBytesDelta} target=${result.target}"
                )
            }
        }, "gh-selftest").apply { isDaemon = true; start() }
    }

    /** Runs a real payload exchange through the relay (blocking; call off the main thread). */
    fun runSelfTest(): TunnelSelfTestResult {
        val activeRelay = relay
            ?: return TunnelSelfTestResult(
                ok = false, stage = "not_running", detail = "tunnel_not_established",
                target = "-", latencyMs = 0, requestBytes = 0, responseBytes = 0,
                synAckMs = -1, firstByteMs = -1, upBytesDelta = 0, downBytesDelta = 0, checksumErrors = 0
            )
        val selfTest = TunnelSelfTest(activeRelay)
        var last: TunnelSelfTestResult? = null
        for (target in SELF_TEST_TARGETS) {
            val request = if (target.path != null) {
                (
                    "GET ${target.path} HTTP/1.0\r\n" +
                        "Host: ${target.hostHeader}\r\n" +
                        "User-Agent: GhProtocol-selftest/1.6\r\n\r\n"
                    ).toByteArray(Charsets.US_ASCII)
            } else {
                DnsMessage.buildQuery("example.com")
            }
            val expected: (ByteArray) -> Boolean = { bytes ->
                if (target.path != null) {
                    val text = String(bytes, Charsets.ISO_8859_1)
                    text.startsWith("HTTP/1.")
                } else {
                    val view = DnsMessage.parse(bytes)
                    view != null && view.isResponse && view.answerCount > 0
                }
            }
            val result = selfTest.run(
                targetIp = target.ip,
                targetPort = target.port,
                request = request,
                expected = expected,
                timeoutMs = 9_000
            )
            last = result
            if (result.ok) return result
            Log.d("GhDiag", "selftest ${target.ip}:${target.port} failed at ${result.stage}: ${result.detail}")
        }
        return last ?: TunnelSelfTestResult(
            ok = false, stage = "no_target", detail = "no_self_test_target",
            target = "-", latencyMs = 0, requestBytes = 0, responseBytes = 0,
            synAckMs = -1, firstByteMs = -1, upBytesDelta = 0, downBytesDelta = 0, checksumErrors = 0
        )
    }
}
