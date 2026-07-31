import android.content.Context
import com.google.android.exoplayer2.ui.PlayerView

fun test(ctx: Context) {
    PlayerView(ctx).apply {
        setControllerOnFullScreenModeChangedListener { isFullScreen ->
            println(isFullScreen)
        }
    }
}
