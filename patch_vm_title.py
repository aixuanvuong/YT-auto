import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Add currentPlayingTitle to MainViewModel
if "val currentPlayingTitle =" not in content:
    title_state = """    private val _currentPlayingTitle = MutableStateFlow<String>("Đang phát video...")
    val currentPlayingTitle = _currentPlayingTitle.asStateFlow()
"""
    content = content.replace("    private val _currentPlayingVideoId = MutableStateFlow<String?>(null)", title_state + "\n    private val _currentPlayingVideoId = MutableStateFlow<String?>(null)")

# Update in playVideo
content = content.replace("_currentPlayingVideoId.value = videoId\n        _isVideoMinimized.value = false", "_currentPlayingTitle.value = title\n        _currentPlayingVideoId.value = videoId\n        _isVideoMinimized.value = false")

# Update in Dashboard
content = content.replace("val isPlaying by viewModel.isPlaying.collectAsState()", "val isPlaying by viewModel.isPlaying.collectAsState()\n    val currentPlayingTitle by viewModel.currentPlayingTitle.collectAsState()")
content = content.replace('text = "Đang phát video...", // We can use the current video title if we store it', 'text = currentPlayingTitle,')

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
