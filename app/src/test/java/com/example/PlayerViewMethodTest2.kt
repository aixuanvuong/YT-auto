package com.example

import org.junit.Test
import android.content.Context
import androidx.test.core.app.ApplicationProvider
import com.google.android.exoplayer2.ui.PlayerView
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner

@RunWith(RobolectricTestRunner::class)
class PlayerViewMethodTest2 {
    @Test
    fun testMethods() {
        val ctx: Context = ApplicationProvider.getApplicationContext()
        PlayerView(ctx).setFullscreenButtonClickListener { isFullScreen ->
        }
    }
}
