package com.example

import com.example.youtube.YoutubeExtractor
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner

@RunWith(RobolectricTestRunner::class)
class ExampleRobolectricTest {
    @Test
    fun testYoutubeExtractor() {
        try {
            val url = YoutubeExtractor.getStream("dQw4w9WgXcQ")
            println("RESULTS: " + url)
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }
}
