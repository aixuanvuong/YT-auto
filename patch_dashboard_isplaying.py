import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

content = content.replace("val isVideoMinimized by viewModel.isVideoMinimized.collectAsState()", "val isVideoMinimized by viewModel.isVideoMinimized.collectAsState()\n    val isPlaying by viewModel.isPlaying.collectAsState()")

content = content.replace("if (viewModel.exoPlayer.isPlaying) viewModel.exoPlayer.pause()", "if (isPlaying) viewModel.exoPlayer.pause()")
content = content.replace("else viewModel.exoPlayer.play()", "else viewModel.exoPlayer.play()")
content = content.replace("imageVector = if (viewModel.exoPlayer.isPlaying) androidx.compose.material.icons.Icons.Default.Pause else androidx.compose.material.icons.Icons.Default.PlayArrow", "imageVector = if (isPlaying) androidx.compose.material.icons.Icons.Default.Pause else androidx.compose.material.icons.Icons.Default.PlayArrow")

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
