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

        /**
         * IPv6 policy (requirement 4), as three states that are measured, never assumed:
         *  - `unavailable` — the platform refused `fd00:1::2/64` + `::/0`: no v6 claim is made;
         *  - `route_only`  — the address/route exist but no v6 flow was ever proven to carry
         *                    payload (this was the state an E2E run could not distinguish before);
         *  - `verified`    — a v6 TCP flow through the relay received real remote bytes.
         */
        const val IPV6_UNAVAILABLE = "unavailable"
        const val IPV6_ROUTE_ONLY = "route_only"
        const val IPV6_VERIFIED = "verified"

        /** Targets used to prove real payload through the tunnel, in preference order. */
        val SELF_TEST_TARGETS = listOf(
            SelfTestTarget("1.1.1.1", 80, "one.one.one.one", "/cdn-cgi/trace"),
            SelfTestTarget("104.16.248.249", 80, "cp.cloudflare.com", "/cdn-cgi/trace"),
            SelfTestTarget("8.8.8.8", 53, "dns.google", null)
        )

        /**
         * IPv6 counterpart of [SELF_TEST_TARGETS]: Cloudflare's v6 anycast edge. Only used to
         * *measure* whether IPv6 really passes payload; an unreachable v6 path leaves the mode at
         * [IPV6_ROUTE_ONLY] instead of pretending it is protected.
         */
        val SELF_TEST_TARGET_V6 = SelfTestTarget("2606:4700:4700::1111", 80, "one.one.one.one", "/cdn-cgi/trace")

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

    /** True when the platform accepted the v6 address + `::/0` route for this session. */
    @Volatile
    private var hasIpv6Route: Boolean = false

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

    // Datapath counters for the adb heartbeat below: they separate "apps sent nothing into tun0"
    // from "apps sent packets but the relay failed", which is exactly what ActiveTCP=0 hides.
    private val tunPackets = java.util.concurrent.atomic.AtomicLong(0)
    private val tunTcpPackets = java.util.concurrent.atomic.AtomicLong(0)
    private val tunDnsPackets = java.util.concurrent.atomic.AtomicLong(0)
    private val tunOtherUdp = java.util.concurrent.atomic.AtomicLong(0)

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

        hasIpv6Route = ipv6
        TunnelLogBuffer.setIpv6Mode(if (ipv6) IPV6_ROUTE_ONLY else IPV6_UNAVAILABLE)
        TunnelLogBuffer.log(
            LogLevel.SUCCESS, LogCategory.TUN,
            if (ipv6) {
                "رابط tun0 برقرار شد — IPv4 تونل شد و IPv6 در حال سنجش است"
            } else {
                "رابط tun0 برقرار شد (فقط IPv4)؛ IPv6 در این دستگاه تونل نمی‌شود"
            },
            "tun0 established ipv4=$TUNNEL_ADDR/24 ipv6=" +
                (if (ipv6) "$TUNNEL_ADDR_V6/64 route=::/0 state=$IPV6_ROUTE_ONLY" else IPV6_UNAVAILABLE) +
                " dns=$TUNNEL_GW mtu=$MTU"
        )

        Log.d(
            "GhDiag",
            "tun0 established ipv4=$TUNNEL_ADDR/24 ipv6=" +
                (if (ipv6) "$TUNNEL_ADDR_V6/64 route=::/0 state=$IPV6_ROUTE_ONLY" else IPV6_UNAVAILABLE) +
                " dns=$TUNNEL_GW mtu=$MTU"
        )
        buildDatapath(output)
        TunnelLogBuffer.setTunnelState(TunnelState.CORE_READY, "tun_up ipv6=$ipv6")
        startStatsHeartbeat()
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
                idleTimeoutMs = 300_000L,
                // Everything inside our own tunnel subnet (TUN address + gateway + the local DNS
                // listener) is unreachable through the upstream proxy: reset it locally instead
                // of dialling 10.8.0.1/fd00:1::1 through SOCKS (E2E 2026-10-25: Android Private
                // DNS tried 10.8.0.1:853 and fd00:1::1:853 and both ended in `upstream_eof`).
                localDestinationPrefixes = listOf("10.8.0.", "fd00:1:")
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

    /**
     * `ip:port->ip:port` with both addresses masked, so flow logs can be shared and still show
     * which peer (and which family) carried the bytes.
     */
    private fun maskFlowKey(key: String): String = key.split("->").joinToString("->") { side ->
        val idx = side.lastIndexOf(':')
        if (idx <= 0) {
            side
        } else {
            PacketCodec.maskIp(side.substring(0, idx)) + ":" + side.substring(idx + 1)
        }
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

    /**
     * Requirement-1 evidence, one line every 5 s on `adb logcat -s GhDiag:D`:
     *
     *   stats t=15s packets=.. tcp=.. dns53=.. otherUdp=.. activeTcp=.. flowsOpened=..
     *         flowsEstablished=.. connectFailures=.. up=.. down=.. dnsOk=.. dnsFail=.. state=..
     *
     * Every byte/flow number is the relay's **absolute** counter, never a UI-side accumulator, so
     * a reported Up/Down/ActiveTCP can be compared with the wire. If packets stays 0 while the
     * tunnel is up, no application traffic ever entered tun0 — that is the measured cause of
     * ActiveTCP=0, and it is logged as such instead of being guessed.
     */
    private fun startStatsHeartbeat() {
        Thread({
            var ticks = 0
            while (running.get()) {
                try {
                    Thread.sleep(5_000L)
                } catch (_: InterruptedException) {
                    break
                }
                if (!running.get()) break
                ticks++
                val stats = relay?.stats()
                val telemetry = TunnelLogBuffer.telemetry.value
                Log.d(
                    "GhDiag",
                    "stats t=${ticks * 5}s packets=${tunPackets.get()} tcp=${tunTcpPackets.get()} " +
                        "dns53=${tunDnsPackets.get()} otherUdp=${tunOtherUdp.get()} " +
                        "activeTcp=${stats?.activeFlows ?: -1} flowsOpened=${stats?.flowsOpened ?: 0} " +
                        "flowsEstablished=${stats?.flowsEstablished ?: 0} " +
                        "connectFailures=${stats?.connectFailures ?: 0} retransmits=${stats?.retransmits ?: 0} " +
                        "appUp=${stats?.applicationOnly()?.bytesUp ?: 0} appDown=${stats?.applicationOnly()?.bytesDown ?: 0} " +
                        "probeUp=${stats?.probeBytesUp ?: 0} probeDown=${stats?.probeBytesDown ?: 0} " +
                        "probeFlows=${stats?.probeActiveFlows ?: 0} " +
                        "dnsOk=${telemetry.dnsQueriesHandled} dnsFail=${telemetry.dnsQueriesFailed} " +
                        "state=${telemetry.tunnelState} ipv6=${telemetry.ipv6Mode}"
                )
                if (ticks == 2 && tunPackets.get() == 0L) {
                    Log.w(
                        "GhDiag",
                        "no_app_packets after 10s: nothing entered tun0 — ActiveTCP stays 0 because " +
                            "no application sends through the tunnel (verifier/self-test traffic is " +
                            "excluded from these counters)"
                    )
                    TunnelLogBuffer.log(
                        LogLevel.WARN, LogCategory.TUN,
                        "هیچ بستهٔ برنامه‌ای وارد تونل نشد — دلیل ActiveTCP=0 نبودِ ترافیک برنامه است",
                        "heartbeat tun0_up_10s packets=0 tcp=0 dns53=0"
                    )
                }
            }
            Log.d("GhDiag", "stats heartbeat exited")
        }, "gh-stats").apply { isDaemon = true; start() }
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
            tunPackets.incrementAndGet()
            when (packet.protocol) {
                PacketCodec.PROTO_TCP -> tunTcpPackets.incrementAndGet()
                PacketCodec.PROTO_UDP -> if (packet.dstPort == 53) {
                    tunDnsPackets.incrementAndGet()
                } else {
                    tunOtherUdp.incrementAndGet()
                }
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
        /** One warning per reason: Private DNS retries can be frequent. */
        private val loggedRejections = java.util.Collections.synchronizedSet(mutableSetOf<String>())

        override fun onFlowRejected(key: String, reason: String) {
            Log.d("GhDiag", "flow_rejected reason=$reason dst=${maskFlowKey(key)}")
            if (loggedRejections.add(reason)) {
                TunnelLogBuffer.log(
                    LogLevel.WARN, LogCategory.TUN,
                    "اتصال به آدرس داخلی خود تونل رد شد (به‌جای انتظار بی‌نتیجه)",
                    "flow_rejected reason=$reason count=${relay?.stats()?.localRejects ?: -1} note=" +
                        "tunnel-local destination is not reachable through the proxy; " +
                        "client gets a real RST and falls back (UDP 53 is served by DnsResolver)"
                )
            }
        }

        override fun onFlowOpened(key: String, dstIp: String, dstPort: Int) {
            Log.d(
                "GhDiag",
                "flow_open v${if (dstIp.contains(':')) 6 else 4} " +
                    "dst=${PacketCodec.maskIp(dstIp)}:$dstPort probe=${dstPort == 0}"
            )
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

        override fun onFlowClosed(
            key: String,
            reason: String,
            upBytes: Long,
            downBytes: Long,
            durationMs: Long,
            probe: Boolean
        ) {
            // Masked destination keeps the log shareable while still proving which family and
            // which peer got the bytes (requirement 1/4: v4 vs v6 evidence from a phone log).
            Log.d(
                "GhDiag",
                "flow_closed dst=${maskFlowKey(key)} reason=$reason " +
                    "up=$upBytes down=$downBytes ms=$durationMs probe=$probe"
            )
        }

        override fun onTraffic(upBytes: Long, downBytes: Long, activeFlows: Int) {
            // Absolute values from the relay — the UI never accumulates on its own. Self-test
            // bytes are excluded so "Up/Down/ActiveTCP" describe application traffic only
            // (requirement 5); the probe share is logged by the heartbeat below.
            val stats = relay?.stats()
            if (stats != null) TunnelLogBuffer.setRelayStats(stats.applicationOnly())
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

    /**
     * One v6 TCP flow through the relay. Success promotes the IPv6 state to [IPV6_VERIFIED];
     * failure keeps it at [IPV6_ROUTE_ONLY] and logs the stage, so no log or UI ever claims v6
     * protection that was not measured.
     */
    private fun measureIpv6Payload(selfTest: TunnelSelfTest) {
        if (!hasIpv6Route) {
            TunnelLogBuffer.setIpv6Mode(IPV6_UNAVAILABLE)
            Log.d("GhDiag", "ipv6_state=$IPV6_UNAVAILABLE reason=no_route")
            return
        }
        val target = SELF_TEST_TARGET_V6
        val request = (
            "GET ${target.path} HTTP/1.0\r\n" +
                "Host: ${target.hostHeader}\r\n" +
                "User-Agent: GhProtocol-selftest/1.6\r\n\r\n"
            ).toByteArray(Charsets.US_ASCII)
        val result = selfTest.run(
            targetIp = target.ip,
            targetPort = target.port,
            request = request,
            expected = { bytes -> String(bytes, Charsets.ISO_8859_1).startsWith("HTTP/1.") },
            timeoutMs = 9_000
        )
        if (result.ok) {
            TunnelLogBuffer.setIpv6Mode(IPV6_VERIFIED)
            Log.d(
                "GhDiag",
                "relay_selftest_v6 ok=true target=${result.target} up=${result.upBytesDelta} " +
                    "down=${result.downBytesDelta} checksums=${result.checksumErrors}"
            )
            TunnelLogBuffer.log(
                LogLevel.SUCCESS, LogCategory.TUN,
                "عبور واقعی IPv6 هم تایید شد (${result.target})",
                "ipv6_state=$IPV6_VERIFIED target=${result.target} down=${result.downBytesDelta}"
            )
        } else {
            TunnelLogBuffer.setIpv6Mode(IPV6_ROUTE_ONLY)
            Log.d("GhDiag", "relay_selftest_v6 ok=false stage=${result.stage} detail=${result.detail}")
            TunnelLogBuffer.log(
                LogLevel.WARN, LogCategory.TUN,
                "IPv6 تونل شد اما عبور دادهٔ واقعی آن تایید نشد",
                "ipv6_state=$IPV6_ROUTE_ONLY stage=${result.stage} detail=${result.detail}"
            )
        }
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
            if (result.ok) {
                // v4 works — still measure IPv6 before returning, so the "ipv6" state in the
                // heartbeat is evidence-based rather than a copy of the accepted route.
                measureIpv6Payload(selfTest)
                return result
            }
            Log.d("GhDiag", "selftest ${target.ip}:${target.port} failed at ${result.stage}: ${result.detail}")
        }
        measureIpv6Payload(selfTest)
        return last ?: TunnelSelfTestResult(
            ok = false, stage = "no_target", detail = "no_self_test_target",
            target = "-", latencyMs = 0, requestBytes = 0, responseBytes = 0,
            synAckMs = -1, firstByteMs = -1, upBytesDelta = 0, downBytesDelta = 0, checksumErrors = 0
        )
    }
}
