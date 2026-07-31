package com.example

import org.junit.Test
import com.google.android.exoplayer2.ui.PlayerView
import com.google.android.exoplayer2.ui.PlayerControlView

class PlayerViewMethodTest3 {
    @Test
    fun testMethods() {
        PlayerView::class.java.methods.forEach {
            if (it.name.toLowerCase().contains("controller") && it.name.toLowerCase().contains("visibility")) {
                println("METHODFOUND: " + it.name)
            }
        }
    }
}
