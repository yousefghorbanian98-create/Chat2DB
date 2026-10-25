package com.ghprotocol.app.core.net

/**
 * RFC 1035 DNS message helpers: *validation-first* parsing used by the tunnel's resolver.
 *
 * The resolver must never hand an app a response that does not belong to its query, and it
 * must never invent answers. Everything here is pure and unit-tested with real byte strings.
 */
object DnsMessage {

    const val RCODE_NOERROR = 0
    const val RCODE_FORMERR = 1
    const val RCODE_SERVFAIL = 2
    const val RCODE_NXDOMAIN = 3
    const val RCODE_NOTIMP = 4
    const val RCODE_REFUSED = 5

    const val TYPE_A = 1
    const val TYPE_AAAA = 28
    const val TYPE_OPT = 41

    data class Question(val name: String, val type: Int, val qclass: Int)

    data class View(
        val id: Int,
        val isResponse: Boolean,
        val opcode: Int,
        val rcode: Int,
        val authoritative: Boolean,
        val truncated: Boolean,
        val recursionDesired: Boolean,
        val recursionAvailable: Boolean,
        val questionCount: Int,
        val answerCount: Int,
        val questions: List<Question>,
        /** Byte range of the question section (header excluded). */
        val questionEnd: Int,
        /** EDNS0 advertised UDP payload size, or 512 when no OPT record is present. */
        val udpPayloadSize: Int
    )

    fun rcodeName(rcode: Int): String = when (rcode) {
        RCODE_NOERROR -> "NOERROR"
        RCODE_FORMERR -> "FORMERR"
        RCODE_SERVFAIL -> "SERVFAIL"
        RCODE_NXDOMAIN -> "NXDOMAIN"
        RCODE_NOTIMP -> "NOTIMP"
        RCODE_REFUSED -> "REFUSED"
        else -> "RCODE_$rcode"
    }

    fun typeName(type: Int): String = when (type) {
        TYPE_A -> "A"
        TYPE_AAAA -> "AAAA"
        TYPE_OPT -> "OPT"
        5 -> "CNAME"
        12 -> "PTR"
        16 -> "TXT"
        33 -> "SRV"
        65 -> "HTTPS"
        64 -> "SVCB"
        else -> "TYPE_$type"
    }

    fun parse(message: ByteArray): View? {
        if (message.size < 12) return null
        val id = PacketCodec.readU16(message, 0)
        val flags = PacketCodec.readU16(message, 2)
        val qdCount = PacketCodec.readU16(message, 4)
        val anCount = PacketCodec.readU16(message, 6)
        val arCount = PacketCodec.readU16(message, 10)
        val questions = ArrayList<Question>(qdCount)
        var offset = 12
        for (i in 0 until qdCount) {
            val read = readName(message, offset) ?: return null
            val name = read.first
            offset = read.second
            if (offset + 4 > message.size) return null
            val type = PacketCodec.readU16(message, offset)
            val qclass = PacketCodec.readU16(message, offset + 2)
            offset += 4
            questions.add(Question(name, type, qclass))
        }
        val questionEnd = offset
        var udpPayloadSize = 512
        var scan = questionEnd
        var walkedAll = true
        for (section in intArrayOf(anCount, PacketCodec.readU16(message, 8), arCount)) {
            for (i in 0 until section) {
                val record = readRecord(message, scan)
                if (record == null) {
                    walkedAll = false
                    break
                }
                if (record.type == TYPE_OPT && record.rclass in 512..4096) {
                    udpPayloadSize = record.rclass
                }
                scan = record.end
            }
            if (!walkedAll) break
        }
        return View(
            id = id,
            isResponse = (flags and 0x8000) != 0,
            opcode = (flags shr 11) and 0x0F,
            rcode = flags and 0x0F,
            authoritative = (flags and 0x0400) != 0,
            truncated = (flags and 0x0200) != 0,
            recursionDesired = (flags and 0x0100) != 0,
            recursionAvailable = (flags and 0x0080) != 0,
            questionCount = qdCount,
            answerCount = anCount,
            questions = questions,
            questionEnd = questionEnd,
            udpPayloadSize = udpPayloadSize
        )
    }

    /** True when [response] is a well-formed reply to [query]: QR=1, same ID, same question. */
    fun isResponseTo(response: ByteArray, query: ByteArray): Boolean {
        val resp = parse(response) ?: return false
        val req = parse(query) ?: return false
        if (!resp.isResponse) return false
        if (resp.id != req.id) return false
        if (resp.opcode != req.opcode) return false
        if (resp.questionCount != req.questionCount) return false
        if (resp.questions != req.questions) return false
        return true
    }

    /** Explains why [response] is not a valid answer to [query] (for diagnostics). */
    fun mismatchReason(response: ByteArray, query: ByteArray): String? {
        val resp = parse(response) ?: return "response_unparseable"
        val req = parse(query) ?: return "query_unparseable"
        if (!resp.isResponse) return "not_a_response"
        if (resp.id != req.id) return "transaction_id_mismatch(${resp.id}!=${req.id})"
        if (resp.opcode != req.opcode) return "opcode_mismatch"
        if (resp.questionCount != req.questionCount) return "question_count_mismatch"
        if (resp.questions != req.questions) return "question_mismatch"
        return null
    }

    /** Cache key: the question section (names lowercased) — never the transaction ID. */
    fun cacheKey(query: ByteArray): String? {
        val view = parse(query) ?: return null
        if (view.questions.isEmpty()) return null
        return view.questions.joinToString("|") { "${it.name.lowercase()}/${it.type}/${it.qclass}" }
    }

    /** Lowest TTL among answer records; [fallback] when the section cannot be walked. */
    fun minAnswerTtlSeconds(response: ByteArray, fallback: Long = 60L): Long {
        val view = parse(response) ?: return fallback
        if (view.answerCount == 0) return fallback
        var offset = view.questionEnd
        var min = Long.MAX_VALUE
        for (i in 0 until view.answerCount) {
            val record = readRecord(response, offset) ?: return fallback
            if (record.type != TYPE_OPT && record.ttl < min) min = record.ttl
            offset = record.end
        }
        if (min == Long.MAX_VALUE) return fallback
        return min
    }

    /** Rewrite only the transaction ID so a cached/validated answer matches the new query. */
    fun withTransactionId(response: ByteArray, query: ByteArray): ByteArray {
        if (response.size < 2 || query.size < 2) return response
        val copy = response.copyOf()
        copy[0] = query[0]
        copy[1] = query[1]
        return copy
    }

    /**
     * Build a real SERVFAIL reply (same ID, question echoed, empty answer sections).
     * Used when every upstream path failed so the app fails *fast* instead of hanging.
     */
    fun buildFailure(query: ByteArray, rcode: Int = RCODE_SERVFAIL): ByteArray {
        val view = parse(query)
        val questionEnd = view?.questionEnd ?: minOf(query.size, 12)
        val out = ByteArray(questionEnd)
        if (questionEnd > 0) System.arraycopy(query, 0, out, 0, questionEnd)
        if (out.size >= 12) {
            val flags = PacketCodec.readU16(query, 2)
            val responseFlags = 0x8000 or // QR
                (flags and 0x7800) or // opcode
                (flags and 0x0100) or // RD
                0x0080 or // RA
                (rcode and 0x0F)
            PacketCodec.writeU16(out, 2, responseFlags)
            PacketCodec.writeU16(out, 4, view?.questionCount ?: 1)
            PacketCodec.writeU16(out, 6, 0)
            PacketCodec.writeU16(out, 8, 0)
            PacketCodec.writeU16(out, 10, 0)
        }
        return out
    }

    /**
     * RFC 1035 §4.2.1 truncation: when a cached answer does not fit the client's UDP
     * payload size, return the header + question with TC=1 so the client retries over TCP.
     * Only the question is echoed — no answer is invented.
     */
    fun truncateTo(query: ByteArray, response: ByteArray, maxSize: Int): ByteArray {
        val view = parse(response)
        if (view == null || response.size <= maxSize) return response
        val out = buildFailure(query, view.rcode)
        if (out.size >= 12) {
            val flags = PacketCodec.readU16(out, 2)
            PacketCodec.writeU16(out, 2, flags or 0x0200) // TC=1
        }
        return out
    }

    /** Read a (possibly compressed) domain name; returns the name + the offset after it. */
    private fun readName(message: ByteArray, start: Int): Pair<String, Int>? {
        val labels = ArrayList<String>(4)
        var offset = start
        var afterPointer = -1
        var guard = 0
        while (true) {
            if (guard++ > 64) return null
            if (offset >= message.size) return null
            val len = message[offset].toInt() and 0xFF
            if (len == 0) {
                offset += 1
                break
            }
            if ((len and 0xC0) == 0xC0) {
                if (offset + 1 >= message.size) return null
                val pointer = ((len and 0x3F) shl 8) or (message[offset + 1].toInt() and 0xFF)
                if (afterPointer < 0) afterPointer = offset + 2
                if (pointer >= message.size) return null
                offset = pointer
                continue
            }
            if (offset + 1 + len > message.size) return null
            labels.add(String(message, offset + 1, len, Charsets.ISO_8859_1))
            offset += 1 + len
        }
        return labels.joinToString(".") to (if (afterPointer >= 0) afterPointer else offset)
    }

    private class Record(val type: Int, val rclass: Int, val ttl: Long, val end: Int)

    private fun readRecord(message: ByteArray, start: Int): Record? {
        val name = readName(message, start) ?: return null
        val offset = name.second
        if (offset + 10 > message.size) return null
        val type = PacketCodec.readU16(message, offset)
        val rclass = PacketCodec.readU16(message, offset + 2)
        val ttl = PacketCodec.readU32(message, offset + 4)
        val rdLen = PacketCodec.readU16(message, offset + 8)
        val end = offset + 10 + rdLen
        if (end > message.size) return null
        return Record(type, rclass, ttl, end)
    }

    /** Build a query with a fresh random ID (used by the in-app DNS self-test). */
    fun buildQuery(name: String, type: Int = TYPE_A, id: Int = (Math.random() * 65535).toInt()): ByteArray {
        val out = ArrayList<Byte>(32)
        out.add((id shr 8).toByte())
        out.add((id and 0xFF).toByte())
        out.add(0x01) // RD
        out.add(0x00)
        out.add(0x00); out.add(0x01) // QDCOUNT
        for (i in 0 until 6) out.add(0x00)
        for (label in name.split('.')) {
            if (label.isEmpty()) continue
            val bytes = label.toByteArray(Charsets.US_ASCII)
            out.add(bytes.size.toByte())
            for (b in bytes) out.add(b)
        }
        out.add(0x00)
        out.add(((type shr 8) and 0xFF).toByte())
        out.add((type and 0xFF).toByte())
        out.add(0x00); out.add(0x01) // QCLASS IN
        return out.toByteArray()
    }
}
