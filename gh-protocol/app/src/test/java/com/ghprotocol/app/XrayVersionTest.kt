package com.ghprotocol.app

import com.ghprotocol.app.core.xrayVersionOk
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

class XrayVersionTest {
    @Test fun meetsMinimum() = assertTrue(xrayVersionOk("26.10.21", "26.6.27"))
    @Test fun equalsMinimum() = assertTrue(xrayVersionOk("26.6.27", "26.6.27"))
    @Test fun belowMinimum() = assertFalse(xrayVersionOk("26.5.99", "26.6.27"))
    @Test fun higherMajor() = assertTrue(xrayVersionOk("27.0.1", "26.6.27"))
    @Test fun garbage() = assertFalse(xrayVersionOk("unknown", "26.6.27"))
}
