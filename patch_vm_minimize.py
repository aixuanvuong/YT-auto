import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Add isVideoMinimized to MainViewModel
if "val isVideoMinimized" not in content:
    minimized_state = """    private val _isVideoMinimized = MutableStateFlow(false)
    val isVideoMinimized = _isVideoMinimized.asStateFlow()

    fun setVideoMinimized(minimized: Boolean) {
        _isVideoMinimized.value = minimized
    }
"""
    content = content.replace("    private val _isFullscreen", minimized_state + "\n    private val _isFullscreen")

# In playVideo, reset isVideoMinimized
if "_isVideoMinimized.value = false" not in content:
    content = content.replace("_currentPlayingVideoId.value = videoId", "_currentPlayingVideoId.value = videoId\n        _isVideoMinimized.value = false")

# In closeVideo, we can keep it as is, or also reset isVideoMinimized
content = content.replace("_isFullscreen.value = false", "_isFullscreen.value = false\n        _isVideoMinimized.value = false")

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
