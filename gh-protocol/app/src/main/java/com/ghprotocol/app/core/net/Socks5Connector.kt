package com.ghprotocol.app.core.net

import com.ghprotocol.app.core.Socks5
import java.io.DataInputStream
import java.net.InetSocketAddress
import java.net.Socket

/**
 * Result of a SOCKS5 CONNECT attempt.
 *
 * [stage] is one of `tcp_proxy`, `greeting`, `request`, `reply`, `done` so callers can
 * report *where* a connection failed instead of a generic "socks5 failed".
 */
data class SocksConnectResult(
    val socket: Socket?,
    val stage: String,
    val detail: String,
    val elapsedMs: Long
) {
    val ok: Boolean get() = socket != null
}

/** Abstraction so the relay can be tested against an in-process SOCKS5 server. */
interface SocksConnector {
    fun connect(host: String, port: Int, connectTimeoutMs: Int = 4000, replyTimeoutMs: Int = 12_000): SocksConnectResult
}

/**
 * Real SOCKS5 client for Xray's `mixed-in` inbound (loopback only, no auth).
 *
 * All sockets are returned *unwrapped* so the caller owns them; on any failure the
 * socket is closed before returning, so no fd leaks into the relay.
 */
class Socks5Connector(
    private val proxyHost: String = "127.0.0.1",
    private val proxyPort: Int = 10808,
    private val socketFactory: () -> Socket = { Socket() }
) : SocksConnector {

    override fun connect(host: String, port: Int, connectTimeoutMs: Int, replyTimeoutMs: Int): SocksConnectResult {
        val started = System.currentTimeMillis()
        val socket = socketFactory()
        fun elapsed() = (System.currentTimeMillis() - started).coerceAtLeast(0L)
        var stage = "tcp_proxy"
        try {
            socket.tcpNoDelay = true
            socket.connect(InetSocketAddress(proxyHost, proxyPort), connectTimeoutMs)
            socket.soTimeout = replyTimeoutMs
            val out = socket.getOutputStream()
            val input = DataInputStream(socket.getInputStream())

            stage = "greeting"
            out.write(Socks5.GREETING)
            out.flush()
            val greeting = ByteArray(2)
            input.readFully(greeting)
            if (!Socks5.greetingReplyOk(greeting)) {
                return closeWith(socket, stage, "method_rejected_${greeting.getOrNull(1)?.toInt() ?: -1}", elapsed())
            }

            stage = "request"
            out.write(Socks5.connectRequest(host, port))
            out.flush()

            stage = "reply"
            val head = ByteArray(4)
            input.readFully(head)
            if (head[0].toInt() != 0x05) {
                return closeWith(socket, stage, "bad_version_${head[0].toInt() and 0xFF}", elapsed())
            }
            val code = head[1].toInt() and 0xFF
            val atyp = head[3].toInt() and 0xFF
            val bindLen = Socks5.bindAddressLength(atyp)
            if (bindLen == -1) {
                return closeWith(socket, stage, "unsupported_atyp_$atyp", elapsed())
            }
            if (bindLen == -2) {
                val nameLen = input.readUnsignedByte()
                if (nameLen > 0) input.readFully(ByteArray(nameLen))
            } else if (bindLen > 0) {
                input.readFully(ByteArray(bindLen))
            }
            input.readUnsignedShort() // BND.PORT
            if (code != 0x00) {
                return closeWith(socket, stage, Socks5.replyCodeName(code), elapsed())
            }
            socket.soTimeout = 0
            return SocksConnectResult(socket, "done", "connected", elapsed())
        } catch (e: Exception) {
            return closeWith(socket, stage, (e.javaClass.simpleName + ": " + (e.message ?: "error")), elapsed())
        }
    }

    private fun closeWith(socket: Socket, stage: String, detail: String, elapsed: Long): SocksConnectResult {
        try {
            socket.close()
        } catch (_: Exception) {
            // already closed — nothing to recover
        }
        return SocksConnectResult(null, stage, detail, elapsed)
    }
}
