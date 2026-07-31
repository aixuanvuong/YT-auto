import android.content.Context
import com.google.android.exoplayer2.ui.PlayerView

fun test(ctx: Context) {
    PlayerView(ctx).setControllerVisibilityListener { visibility ->
        println(visibility)
    }
}
