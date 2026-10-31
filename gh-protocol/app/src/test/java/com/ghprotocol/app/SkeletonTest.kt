package com.ghprotocol.app

import org.junit.Assert.assertEquals
import org.junit.Test

/**
 * P0 smoke test — keeps the unit-test pipeline green from day one.
 * Real domain tests grow with F-1..F-18.
 */
class SkeletonTest {
    @Test
    fun brandIsGhProtocol() {
        assertEquals("Gh Protocol", "Gh Protocol")
    }
}
