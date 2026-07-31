import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.background
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.foundation.layout.Box
import androidx.compose.ui.viewinterop.AndroidView
import com.google.android.exoplayer2.ui.PlayerView
import androidx.compose.runtime.*
import com.google.android.exoplayer2.ExoPlayer

@Composable
fun TestDialog(exoPlayer: ExoPlayer, modifier: Modifier) {
    var isFullscreen by remember { mutableStateOf(false) }
    
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
                            setFullscreenButtonClickListener {
                                isFullscreen = !isFullscreen
                            }
                        }
                    },
                    modifier = Modifier.fillMaxSize()
                )
            }
        }
    } else {
        AndroidView(
            factory = { ctx ->
                PlayerView(ctx).apply {
                    player = exoPlayer
                    useController = true
                    setFullscreenButtonClickListener {
                        isFullscreen = !isFullscreen
                    }
                }
            },
            modifier = modifier
        )
    }
}
