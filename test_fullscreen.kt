import android.os.Bundle
import android.content.Intent
import androidx.activity.ComponentActivity
import com.google.android.exoplayer2.ExoPlayer
import com.google.android.exoplayer2.ui.PlayerView

class TestActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val view = PlayerView(this)
        view.setFullscreenButtonClickListener { isFullScreen ->
            // do something
        }
    }
}
