import re

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Make sure we add necessary imports for AnimatedVisibility, fadeIn, fadeOut
imports = """
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import android.view.View
import com.google.android.exoplayer2.ui.PlayerControlView
"""
content = content.replace("import android.os.Bundle", imports + "import android.os.Bundle")

new_player = """@Composable
fun InlineVideoPlayer(videoId: String, modifier: Modifier = Modifier) {
    val context = LocalContext.current
    val exoPlayer = remember { ExoPlayer.Builder(context).build() }
    var isFullscreen by remember { mutableStateOf(false) }
    var showControls by remember { mutableStateOf(true) }

    DisposableEffect(videoId) {
        exoPlayer.stop()
        exoPlayer.clearMediaItems()
        
        var thread: Thread? = null
        thread = Thread {
            val stream = YoutubeExtractor.getStream(videoId)
            (context as? ComponentActivity)?.runOnUiThread {
                if (stream != null && thread?.isInterrupted == false) {
                    val mediaItem = MediaItem.fromUri(stream)
                    exoPlayer.setMediaItem(mediaItem)
                    exoPlayer.prepare()
                    exoPlayer.play()
                }
            }
        }
        thread?.start()

        onDispose {
            thread?.interrupt()
        }
    }
    
    DisposableEffect(Unit) {
        onDispose {
            exoPlayer.release()
        }
    }

    if (isFullscreen) {
        Dialog(
            onDismissRequest = { isFullscreen = false },
            properties = DialogProperties(
                usePlatformDefaultWidth = false,
                decorFitsSystemWindows = false
            )
        ) {
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .background(Color.Black)
            ) {
                AndroidView(
                    factory = { ctx ->
                        PlayerView(ctx).apply {
                            player = exoPlayer
                            useController = true
                            setControllerVisibilityListener(PlayerControlView.VisibilityListener { visibility -> 
                                showControls = (visibility == View.VISIBLE)
                            })
                        }
                    },
                    modifier = Modifier.fillMaxSize()
                )
                AnimatedVisibility(
                    visible = showControls,
                    enter = fadeIn(),
                    exit = fadeOut(),
                    modifier = Modifier
                        .align(Alignment.TopEnd)
                        .padding(16.dp)
                ) {
                    IconButton(
                        onClick = { isFullscreen = false },
                        modifier = Modifier
                            .background(Color.Black.copy(alpha = 0.5f), CircleShape)
                    ) {
                        Icon(
                            imageVector = Icons.Default.FullscreenExit,
                            contentDescription = "Exit Fullscreen",
                            tint = Color.White
                        )
                    }
                }
            }
        }
    } else {
        Box(modifier = modifier) {
            AndroidView(
                factory = { ctx ->
                    PlayerView(ctx).apply {
                        player = exoPlayer
                        useController = true
                        setControllerVisibilityListener(PlayerControlView.VisibilityListener { visibility -> 
                            showControls = (visibility == View.VISIBLE)
                        })
                    }
                },
                modifier = Modifier.fillMaxSize()
            )
            AnimatedVisibility(
                visible = showControls,
                enter = fadeIn(),
                exit = fadeOut(),
                modifier = Modifier
                    .align(Alignment.TopEnd)
                    .padding(8.dp)
            ) {
                IconButton(
                    onClick = { isFullscreen = true },
                    modifier = Modifier
                        .background(Color.Black.copy(alpha = 0.5f), CircleShape)
                ) {
                    Icon(
                        imageVector = Icons.Default.Fullscreen,
                        contentDescription = "Fullscreen",
                        tint = Color.White
                    )
                }
            }
        }
    }
}"""

old_player_pattern = re.compile(r'@Composable\s+fun InlineVideoPlayer.*?@Composable\s+fun ModernDarkDashboard', re.DOTALL)
content = old_player_pattern.sub(new_player + "\n\n@Composable\nfun ModernDarkDashboard", content)

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
