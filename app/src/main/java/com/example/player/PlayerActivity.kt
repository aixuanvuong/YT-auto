package com.example.player

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import com.google.android.exoplayer2.ExoPlayer
import com.google.android.exoplayer2.MediaItem
import com.google.android.exoplayer2.ui.PlayerView
import com.example.youtube.YoutubeExtractor

class PlayerActivity : AppCompatActivity() {

    private lateinit var player: ExoPlayer

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val playerView = PlayerView(this)
        setContentView(playerView)

        val videoId = intent.getStringExtra("VIDEO_ID") ?: return

        Thread {
            val stream = YoutubeExtractor.getStream(videoId)

            runOnUiThread {
                if (stream != null) {
                    player = ExoPlayer.Builder(this).build()
                    playerView.player = player

                    val mediaItem = MediaItem.fromUri(stream)
                    player.setMediaItem(mediaItem)

                    player.prepare()
                    player.play()
                }
            }
        }.start()
    }

    override fun onDestroy() {
        super.onDestroy()
        if (::player.isInitialized) {
            player.release()
        }
    }
}
