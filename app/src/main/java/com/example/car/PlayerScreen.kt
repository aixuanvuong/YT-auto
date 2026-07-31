package com.example.car

import android.os.Handler
import android.os.Looper
import androidx.car.app.AppManager
import androidx.car.app.CarContext
import androidx.car.app.Screen
import androidx.car.app.SurfaceCallback
import androidx.car.app.SurfaceContainer
import androidx.car.app.model.Action
import androidx.car.app.model.ActionStrip
import androidx.car.app.model.CarIcon
import androidx.car.app.model.Template
import androidx.car.app.navigation.model.NavigationTemplate
import androidx.core.graphics.drawable.IconCompat
import com.example.R
import com.example.youtube.YoutubeExtractor
import com.google.android.exoplayer2.ExoPlayer
import com.google.android.exoplayer2.MediaItem
import com.google.android.exoplayer2.Player

class PlayerScreen(carContext: CarContext, private val videoId: String, private val title: String) : Screen(carContext), SurfaceCallback {
    private var player: ExoPlayer? = null
    private var surfaceContainer: SurfaceContainer? = null
    private var isPlaying = false
    private var isLoading = true
    
    init {
        carContext.getCarService(AppManager::class.java).setSurfaceCallback(this)
        
        lifecycle.addObserver(object : androidx.lifecycle.DefaultLifecycleObserver {
            override fun onDestroy(owner: androidx.lifecycle.LifecycleOwner) {
                player?.stop()
                player?.release()
                player = null
            }
        })
        
        // Start playback
        Thread {
            val stream = YoutubeExtractor.getStream(videoId)
            if (stream != null) {
                Handler(Looper.getMainLooper()).post {
                    if (player == null) {
                        player = ExoPlayer.Builder(carContext).build()
                        player?.setMediaItem(MediaItem.fromUri(stream))
                        surfaceContainer?.surface?.let {
                            player?.setVideoSurface(it)
                        }
                        
                        player?.addListener(object : Player.Listener {
                            override fun onIsPlayingChanged(playing: Boolean) {
                                if (isPlaying != playing) {
                                    isPlaying = playing
                                    isLoading = false
                                    invalidate()
                                }
                            }
                            override fun onPlaybackStateChanged(playbackState: Int) {
                                if (playbackState == Player.STATE_READY) {
                                    if (isLoading) {
                                        isLoading = false
                                        invalidate()
                                    }
                                } else if (playbackState == Player.STATE_BUFFERING) {
                                    if (!isLoading) {
                                        isLoading = true
                                        invalidate()
                                    }
                                }
                            }
                        })
                        
                        player?.prepare()
                        player?.play()
                    }
                }
            }
        }.start()
    }

    override fun onSurfaceAvailable(container: SurfaceContainer) {
        this.surfaceContainer = container
        player?.setVideoSurface(container.surface)
    }

    override fun onSurfaceDestroyed(container: SurfaceContainer) {
        if (this.surfaceContainer == container) {
            player?.setVideoSurface(null)
            this.surfaceContainer = null
        }
    }

    override fun onGetTemplate(): Template {
        val playPauseIconRes = if (isPlaying) R.drawable.ic_pause_car else R.drawable.ic_play_car
        
        val playPauseAction = Action.Builder()
            .setIcon(CarIcon.Builder(IconCompat.createWithResource(carContext, playPauseIconRes)).build())
            .setOnClickListener {
                if (isPlaying) {
                    player?.pause()
                } else {
                    player?.play()
                }
            }.build()

        val nextAction = Action.Builder()
            .setIcon(CarIcon.Builder(IconCompat.createWithResource(carContext, R.drawable.ic_next_car)).build())
            .setOnClickListener {
                // Seek forward 10 seconds
                player?.let { it.seekTo(it.currentPosition + 10000) }
            }.build()

        val prevAction = Action.Builder()
            .setIcon(CarIcon.Builder(IconCompat.createWithResource(carContext, R.drawable.ic_prev_car)).build())
            .setOnClickListener {
                // Seek back 10 seconds
                player?.let { it.seekTo(it.currentPosition - 10000) }
            }.build()

        val backAction = Action.Builder()
            .setTitle("Back")
            .setOnClickListener {
                player?.stop()
                player?.release()
                player = null
                screenManager.pop()
            }.build()

        val actionStrip = ActionStrip.Builder()
            .addAction(prevAction)
            .addAction(playPauseAction)
            .addAction(nextAction)
            .addAction(backAction)
            .build()

        return NavigationTemplate.Builder()
            .setActionStrip(actionStrip)
            .build()
    }
}
