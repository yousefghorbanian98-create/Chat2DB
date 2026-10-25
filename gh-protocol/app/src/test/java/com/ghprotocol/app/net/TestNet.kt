package com.ghprotocol.app.net

import com.ghprotocol.app.core.Socks5
import com.ghprotocol.app.core.net.PacketCodec
import com.ghprotocol.app.core.net.SocksConnectResult
import com.ghprotocol.app.core.net.SocksConnector
import java.io.DataInputStream
import java.io.InputStream
import java.io.OutputStream
import java.net.InetAddress
import java.net.InetSocketAddress
import java.net.ServerSocket
import java.net.Socket
import java.security.KeyStore
import javax.net.ssl.KeyManagerFactory
import javax.net.ssl.SSLContext
import javax.net.ssl.SSLServerSocket

/**
 * Test-only network doubles. Everything runs on 127.0.0.1 with ephemeral ports so the
 * whole suite is hermetic on a CI runner (and on a laptop) with no external egress.
 */
object TestNet {

    /** Real loopback SOCKS5 server (RFC 1928, CONNECT, no auth) → plain TCP to the target. */
    class SocksServer(
        val failWith: Int = 0x00,
        val failOnPort: Int = -1,
        val refuseConnect: Boolean = false
    ) : AutoCloseable {
        private val server = ServerSocket(0, 16, InetAddress.getByName("127.0.0.1"))
        private val threads = ArrayList<Thread>()
        @Volatile
        var connections = 0
            private set
        @Volatile
        var lastTarget: String? = null
            private set

        val port: Int get() = server.localPort

        init {
            val acceptThread = Thread({
                while (!server.isClosed) {
                    val client = try {
                        server.accept()
                    } catch (_: Exception) {
                        break
                    }
                    connections++
                    Thread({ handle(client) }, "test-socks-conn").apply { isDaemon = true; start() }
                }
            }, "test-socks-accept").apply { isDaemon = true }
            acceptThread.start()
            threads.add(acceptThread)
        }

        private fun handle(client: Socket) {
            client.use { socket ->
                socket.tcpNoDelay = true
                val input = DataInputStream(socket.getInputStream())
                val out = socket.getOutputStream()
                val greeting = ByteArray(2)
                input.readFully(greeting)
                val methods = ByteArray(greeting[1].toInt() and 0xFF)
                input.readFully(methods)
                out.write(byteArrayOf(0x05, 0x00))
                out.flush()

                val head = ByteArray(4)
                input.readFully(head)
                val atyp = head[3].toInt() and 0xFF
                val host: String = when (atyp) {
                    1 -> {
                        val bytes = ByteArray(4); input.readFully(bytes)
                        InetAddress.getByAddress(bytes).hostAddress ?: "0.0.0.0"
                    }
                    4 -> {
                        val bytes = ByteArray(16); input.readFully(bytes)
                        InetAddress.getByAddress(bytes).hostAddress ?: "::"
                    }
                    3 -> {
                        val length = input.readUnsignedByte()
                        val name = ByteArray(length); input.readFully(name)
                        String(name, Charsets.US_ASCII)
                    }
                    else -> {
                        out.write(byteArrayOf(0x05, 0x08, 0x00, 0x01, 0, 0, 0, 0, 0, 0))
                        out.flush()
                        return
                    }
                }
                val targetPort = input.readUnsignedShort()
                lastTarget = "$host:$targetPort"
                if (refuseConnect || (failOnPort > 0 && failOnPort == targetPort)) {
                    val code = if (failWith != 0) failWith else 0x05
                    out.write(byteArrayOf(0x05, code.toByte(), 0x00, 0x01, 0, 0, 0, 0, 0, 0))
                    out.flush()
                    return
                }
                val upstream = try {
                    Socket().apply {
                        tcpNoDelay = true
                        connect(InetSocketAddress(host, targetPort), 3000)
                    }
                } catch (_: Exception) {
                    out.write(byteArrayOf(0x05, 0x05, 0x00, 0x01, 0, 0, 0, 0, 0, 0))
                    out.flush()
                    return
                }
                out.write(byteArrayOf(0x05, 0x00, 0x00, 0x01, 0x7f, 0, 0, 1, 0, 0))
                out.flush()
                upstream.use { target ->
                    // One direction in a background thread, the other inline: the sockets must
                    // stay open for the whole exchange (closing them early broke every test).
                    val back = Thread({
                        copy(target.getInputStream(), socket.getOutputStream())
                        try { socket.shutdownOutput() } catch (_: Exception) { }
                    }, "test-socks-back").apply { isDaemon = true; start() }
                    copy(socket.getInputStream(), target.getOutputStream())
                    try { target.shutdownOutput() } catch (_: Exception) { }
                    back.join(5000)
                }
            }
        }

        override fun close() {
            try { server.close() } catch (_: Exception) { }
        }
    }

    private fun copy(input: InputStream, output: OutputStream) {
        val buffer = ByteArray(8192)
        try {
            while (true) {
                val read = input.read(buffer)
                if (read < 0) break
                output.write(buffer, 0, read)
                output.flush()
            }
        } catch (_: Exception) {
            // peer closed
        }
    }

    /** Plain TCP server that replies with a fixed payload after the first request bytes. */
    class ReplyServer(private val reply: ByteArray, val readBytes: Int = 1) : AutoCloseable {
        private val server = ServerSocket(0, 16, InetAddress.getByName("127.0.0.1"))
        @Volatile
        var received = 0
            private set
        @Volatile
        var lastRequest: ByteArray = ByteArray(0)
            private set
        val port: Int get() = server.localPort

        init {
            Thread({
                while (!server.isClosed) {
                    val client = try { server.accept() } catch (_: Exception) { break }
                    Thread({
                        client.use { socket ->
                            socket.soTimeout = 10_000
                            val input = socket.getInputStream()
                            val buffer = ByteArray(64 * 1024)
                            val read = input.read(buffer)
                            if (read > 0) {
                                lastRequest = buffer.copyOfRange(0, read)
                                received = read
                                socket.getOutputStream().write(reply)
                                socket.getOutputStream().flush()
                            }
                        }
                    }, "test-reply").apply { isDaemon = true; start() }
                }
            }, "test-reply-accept").apply { isDaemon = true; start() }
        }

        override fun close() {
            try { server.close() } catch (_: Exception) { }
        }
    }

    /** TCP server that closes immediately (upstream EOF path). */
    class CloseServer : AutoCloseable {
        private val server = ServerSocket(0, 16, InetAddress.getByName("127.0.0.1"))
        val port: Int get() = server.localPort

        init {
            Thread({
                while (!server.isClosed) {
                    val client = try { server.accept() } catch (_: Exception) { break }
                    try { client.close() } catch (_: Exception) { }
                }
            }, "test-close-accept").apply { isDaemon = true; start() }
        }

        override fun close() {
            try { server.close() } catch (_: Exception) { }
        }
    }

    /** TCP echo server (mirrors every received byte). */
    class EchoServer(host: String = "127.0.0.1") : AutoCloseable {
        private val server = ServerSocket(0, 16, InetAddress.getByName(host))
        val port: Int get() = server.localPort
        @Volatile
        var echoBytes = 0L
            private set

        init {
            Thread({
                while (!server.isClosed) {
                    val client = try { server.accept() } catch (_: Exception) { break }
                    Thread({
                        client.use { socket ->
                            val buffer = ByteArray(8192)
                            try {
                                while (true) {
                                    val read = socket.getInputStream().read(buffer)
                                    if (read < 0) break
                                    echoBytes += read
                                    socket.getOutputStream().write(buffer, 0, read)
                                    socket.getOutputStream().flush()
                                }
                            } catch (_: Exception) {
                                // closed
                            }
                        }
                    }, "test-echo").apply { isDaemon = true; start() }
                }
            }, "test-echo-accept").apply { isDaemon = true; start() }
        }

        override fun close() {
            try { server.close() } catch (_: Exception) { }
        }
    }

    /** Minimal plain-HTTP origin: replies with a canned status line + headers + body. */
    class HttpServer(
        private val statusLine: String = "HTTP/1.1 200 OK",
        private val extraHeaders: String = "cf-ray: 8f00-test\r\nServer: cloudflare\r\n",
        private val body: String = "fl=123abc\nh=104.16.248.249\n"
    ) : AutoCloseable {
        private val server = ServerSocket(0, 16, InetAddress.getByName("127.0.0.1"))
        val port: Int get() = server.localPort

        @Volatile
        var requests = 0
            private set

        @Volatile
        var lastRequest: String = ""
            private set

        init {
            Thread({
                while (!server.isClosed) {
                    val client = try { server.accept() } catch (_: Exception) { break }
                    Thread({
                        client.use { socket ->
                            try {
                                socket.soTimeout = 4000
                                val input = socket.getInputStream()
                                val buffer = StringBuilder()
                                while (!buffer.contains("\r\n\r\n") && buffer.length < 8192) {
                                    val b = input.read()
                                    if (b < 0) break
                                    buffer.append(b.toChar())
                                }
                                requests++
                                lastRequest = buffer.toString()
                                val payload = body.toByteArray(Charsets.US_ASCII)
                                val response = "$statusLine\r\n" +
                                    extraHeaders +
                                    "Content-Length: ${payload.size}\r\n" +
                                    "Connection: close\r\n\r\n"
                                socket.getOutputStream().write(response.toByteArray(Charsets.US_ASCII))
                                socket.getOutputStream().write(payload)
                                socket.getOutputStream().flush()
                            } catch (_: Exception) {
                                // client went away
                            }
                        }
                    }, "test-http").apply { isDaemon = true; start() }
                }
            }, "test-http-accept").apply { isDaemon = true; start() }
        }

        override fun close() {
            try { server.close() } catch (_: Exception) { }
        }
    }

    fun testSslContext(): SSLContext {
        val stream = TestNet::class.java.classLoader!!.getResourceAsStream("test-tls.p12")
            ?: error("test-tls.p12 missing from test resources")
        val keyStore = KeyStore.getInstance("PKCS12")
        stream.use { keyStore.load(it, "testpass".toCharArray()) }
        val factory = KeyManagerFactory.getInstance(KeyManagerFactory.getDefaultAlgorithm())
        factory.init(keyStore, "testpass".toCharArray())
        val context = SSLContext.getInstance("TLS")
        context.init(factory.keyManagers, null, null)
        return context
    }

    /** Trust-all factory for tests: the production code still validates the real chain. */
    fun trustAllFactory(context: SSLContext): javax.net.ssl.SSLSocketFactory {
        val trustAll = object : javax.net.ssl.X509TrustManager {
            override fun checkClientTrusted(chain: Array<out java.security.cert.X509Certificate>?, authType: String?) = Unit
            override fun checkServerTrusted(chain: Array<out java.security.cert.X509Certificate>?, authType: String?) = Unit
            override fun getAcceptedIssuers(): Array<java.security.cert.X509Certificate> = emptyArray()
        }
        val trusting = SSLContext.getInstance("TLS")
        trusting.init(null, arrayOf(trustAll), null)
        // Server side needs our key material, client side only needs the trust override.
        val combined = object : javax.net.ssl.SSLSocketFactory() {
            private val delegate: javax.net.ssl.SSLSocketFactory = trusting.socketFactory
            override fun getDefaultCipherSuites(): Array<String> = delegate.defaultCipherSuites
            override fun getSupportedCipherSuites(): Array<String> = delegate.supportedCipherSuites
            override fun createSocket(s: Socket?, host: String?, port: Int, autoClose: Boolean): Socket =
                delegate.createSocket(s, host, port, autoClose)
            override fun createSocket(host: String?, port: Int): Socket = delegate.createSocket(host, port)
            override fun createSocket(host: String?, port: Int, localHost: InetAddress?, localPort: Int): Socket =
                delegate.createSocket(host, port, localHost, localPort)
            override fun createSocket(host: InetAddress?, port: Int): Socket = delegate.createSocket(host, port)
            override fun createSocket(address: InetAddress?, port: Int, localAddress: InetAddress?, localPort: Int): Socket =
                delegate.createSocket(address, port, localAddress, localPort)
        }
        return combined
    }

    /** Minimal RFC 8484 DoH server over TLS with a controllable answer builder. */
    class DohServer(
        private val answer: (ByteArray) -> ByteArray,
        val requirePath: String = "/dns-query",
        val responseCode: Int = 200
    ) : AutoCloseable {
        private val context = testSslContext()
        private val server = context.serverSocketFactory.createServerSocket(
            0, 16, InetAddress.getByName("127.0.0.1")
        ) as SSLServerSocket
        val port: Int get() = server.localPort
        @Volatile
        var requests = 0
            private set
        @Volatile
        var lastPath: String? = null
            private set

        init {
            Thread({
                while (!server.isClosed) {
                    val client = try { server.accept() } catch (_: Exception) { break }
                    Thread({ handle(client) }, "test-doh").apply { isDaemon = true; start() }
                }
            }, "test-doh-accept").apply { isDaemon = true; start() }
        }

        private fun handle(client: Socket) {
            client.use { socket ->
                socket.soTimeout = 10_000
                try {
                    val input = socket.getInputStream()
                    val headers = readHeaders(input) ?: return
                    val path = headers.lineSequence().firstOrNull()?.split(' ')?.getOrNull(1) ?: "/"
                    lastPath = path
                    val contentLength = Regex("content-length:\\s*(\\d+)", RegexOption.IGNORE_CASE)
                        .find(headers)?.groupValues?.getOrNull(1)?.toIntOrNull() ?: 0
                    val body = ByteArray(contentLength)
                    var read = 0
                    while (read < contentLength) {
                        val n = input.read(body, read, contentLength - read)
                        if (n < 0) break
                        read += n
                    }
                    requests++
                    val out = socket.getOutputStream()
                    if (responseCode != 200 || path != requirePath) {
                        val status = if (responseCode != 200) responseCode else 404
                        out.write("HTTP/1.1 $status Not Found\r\nContent-Length: 0\r\nConnection: close\r\n\r\n".toByteArray())
                        out.flush()
                        return
                    }
                    val answerBytes = answer(body)
                    out.write(
                        (
                            "HTTP/1.1 200 OK\r\nContent-Type: application/dns-message\r\n" +
                                "Content-Length: ${answerBytes.size}\r\nConnection: close\r\n\r\n"
                            ).toByteArray(Charsets.US_ASCII)
                    )
                    out.write(answerBytes)
                    out.flush()
                } catch (_: Exception) {
                    // client disconnected
                }
            }
        }

        private fun readHeaders(input: InputStream): String? {
            val buffer = java.io.ByteArrayOutputStream()
            while (buffer.size() < 16 * 1024) {
                val b = input.read()
                if (b < 0) return null
                buffer.write(b)
                val data = buffer.toByteArray()
                val size = data.size
                if (size >= 4 && data[size - 4] == '\r'.code.toByte() && data[size - 3] == '\n'.code.toByte() &&
                    data[size - 2] == '\r'.code.toByte() && data[size - 1] == '\n'.code.toByte()
                ) {
                    return String(data, Charsets.ISO_8859_1)
                }
            }
            return null
        }

        override fun close() {
            try { server.close() } catch (_: Exception) { }
        }
    }

    /** TLS HTTP server that emits a Cloudflare-like response (or anything else). */
    class TlsHttpServer(
        private val statusLine: String = "HTTP/1.1 403 Forbidden",
        private val extraHeaders: List<String> = listOf("cf-ray: 8a1b2c3d4e5f-TEST")
    ) : AutoCloseable {
        private val context = testSslContext()
        private val server = context.serverSocketFactory.createServerSocket(
            0, 16, InetAddress.getByName("127.0.0.1")
        ) as SSLServerSocket
        val port: Int get() = server.localPort
        @Volatile
        var accepts = 0
            private set

        init {
            Thread({
                while (!server.isClosed) {
                    val client = try { server.accept() } catch (_: Exception) { break }
                    Thread({
                        try {
                            client.soTimeout = 5000
                            accepts++
                            val input = client.getInputStream()
                            val buffer = ByteArray(4096)
                            try { input.read(buffer) } catch (_: Exception) { }
                            val headers = buildString {
                                append(statusLine).append("\r\n")
                                for (header in extraHeaders) append(header).append("\r\n")
                                append("Content-Length: 0\r\nConnection: close\r\n\r\n")
                            }
                            client.getOutputStream().write(headers.toByteArray(Charsets.US_ASCII))
                            client.getOutputStream().flush()
                        } catch (_: Exception) {
                            // closed
                        } finally {
                            try { client.close() } catch (_: Exception) { }
                        }
                    }, "test-tls-http").apply { isDaemon = true; start() }
                }
            }, "test-tls-http-accept").apply { isDaemon = true; start() }
        }

        override fun close() {
            try { server.close() } catch (_: Exception) { }
        }
    }

    /** TCP server that accepts and never answers (timeout paths). */
    class SilentServer : AutoCloseable {
        private val server = ServerSocket(0, 16, InetAddress.getByName("127.0.0.1"))
        val port: Int get() = server.localPort
        private val held = ArrayList<Socket>()

        init {
            Thread({
                while (!server.isClosed) {
                    val client = try { server.accept() } catch (_: Exception) { break }
                    synchronized(held) { held.add(client) }
                }
            }, "test-silent-accept").apply { isDaemon = true; start() }
        }

        override fun close() {
            try { server.close() } catch (_: Exception) { }
            synchronized(held) { held.forEach { try { it.close() } catch (_: Exception) { } } }
        }
    }

    /** Build a TCP packet as the *client* would send it into the TUN. */
    fun clientPacket(
        family: Int,
        clientIp: String,
        clientPort: Int,
        dstIp: String,
        dstPort: Int,
        seq: Long,
        ack: Long,
        flags: Int,
        payload: ByteArray = ByteArray(0)
    ): ByteArray = PacketCodec.buildTcp(
        family = family,
        srcIp = clientIp, srcPort = clientPort,
        dstIp = dstIp, dstPort = dstPort,
        seq = seq, ack = ack, flags = flags,
        payload = payload, window = 65535
    ) ?: error("cannot build test packet")

    /** SOCKS connector that talks to an in-process [SocksServer]. */
    fun connectorFor(server: SocksServer): SocksConnector =
        standaloneConnector(server.port)

    fun standaloneConnector(socksPort: Int): SocksConnector = object : SocksConnector {
        override fun connect(host: String, port: Int, connectTimeoutMs: Int, replyTimeoutMs: Int): SocksConnectResult {
            val started = System.currentTimeMillis()
            val socket = Socket()
            return try {
                socket.tcpNoDelay = true
                socket.connect(InetSocketAddress("127.0.0.1", socksPort), connectTimeoutMs)
                socket.soTimeout = replyTimeoutMs
                val out = socket.getOutputStream()
                val input = DataInputStream(socket.getInputStream())
                out.write(Socks5.GREETING); out.flush()
                val greeting = ByteArray(2); input.readFully(greeting)
                if (!Socks5.greetingReplyOk(greeting)) {
                    socket.close()
                    return SocksConnectResult(null, "greeting", "rejected", System.currentTimeMillis() - started)
                }
                out.write(Socks5.connectRequest(host, port)); out.flush()
                val head = ByteArray(4); input.readFully(head)
                val code = head[1].toInt() and 0xFF
                val atyp = head[3].toInt() and 0xFF
                when (atyp) {
                    1 -> input.readFully(ByteArray(4))
                    4 -> input.readFully(ByteArray(16))
                    3 -> input.readFully(ByteArray(input.readUnsignedByte()))
                }
                input.readUnsignedShort()
                if (code != 0) {
                    socket.close()
                    return SocksConnectResult(null, "reply", Socks5.replyCodeName(code), System.currentTimeMillis() - started)
                }
                socket.soTimeout = 0
                SocksConnectResult(socket, "done", "connected", System.currentTimeMillis() - started)
            } catch (e: Exception) {
                try { socket.close() } catch (_: Exception) { }
                SocksConnectResult(null, "exception", e.javaClass.simpleName, System.currentTimeMillis() - started)
            }
        }
    }
}
