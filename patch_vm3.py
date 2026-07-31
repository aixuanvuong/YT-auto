import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Add closeVideo
if "fun closeVideo()" not in content:
    close_video = """    fun closeVideo() {
        exoPlayer.stop()
        exoPlayer.clearMediaItems()
        _currentPlayingVideoId.value = null
        _isFullscreen.value = false
    }"""
    content = content.replace("    fun pauseVideo() {", close_video + "\n\n    fun pauseVideo() {")

# Add homeVideos
if "val homeVideos" not in content:
    home_videos = """    private val _homeVideos = MutableStateFlow<List<VideoItem>>(emptyList())
    val homeVideos = _homeVideos.asStateFlow()
    
    init {
        loadHomeVideos()
    }
    
    private fun loadHomeVideos() {
        viewModelScope.launch(Dispatchers.IO) {
            val h = _history.value
            if (h.isNotEmpty()) {
                val related = com.example.youtube.YoutubeRelated.getRelated(h.first().videoId)
                if (related.isNotEmpty()) {
                    _homeVideos.value = related
                    return@launch
                }
            }
            val defaultSearch = com.example.youtube.YoutubeSearch.search("nhạc trẻ mới nhất")
            _homeVideos.value = defaultSearch
        }
    }
"""
    content = content.replace("    private val _history", home_videos + "\n    private val _history")

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
