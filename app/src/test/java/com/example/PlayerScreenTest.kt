package com.example

import android.content.Intent
import androidx.car.app.CarContext
import androidx.car.app.ScreenManager
import androidx.car.app.testing.TestCarContext
import androidx.test.core.app.ApplicationProvider
import com.example.car.PlayerScreen
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.annotation.Config

@RunWith(RobolectricTestRunner::class)
@Config(sdk = [33])
class PlayerScreenTest {
    @Test
    fun testInit() {
        val carContext = TestCarContext.createCarContext(ApplicationProvider.getApplicationContext())
        val screen = PlayerScreen(carContext, "dQw4w9WgXcQ", "Title")
        screen.onGetTemplate()
    }
}
