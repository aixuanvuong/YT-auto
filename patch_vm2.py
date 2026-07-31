import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

if "import com.example.youtube.VideoResolution" not in content:
    content = content.replace("import com.example.youtube.VideoItem", "import com.example.youtube.VideoItem\nimport com.example.youtube.VideoResolution\nimport com.example.youtube.VideoPlaybackInfo")

vm_new_state = """    private val _availableResolutions = MutableStateFlow<List<VideoResolution>>(emptyList())
    val availableResolutions = _availableResolutions.asStateFlow()
    
    private val _currentResolution = MutableStateFlow<String>("Auto")
    val currentResolution = _currentResolution.asStateFlow()
    
    private var playbackInfo: VideoPlaybackInfo? = null
    
    private var videoThread: Thread? = null"""

content = content.replace("    private var videoThread: Thread? = null", vm_new_state)

play_video_old = """        videoThread = Thread {
            val stream = YoutubeExtractor.getStream(videoId)
            // Need to run on main thread
            android.os.Handler(android.os.Looper.getMainLooper()).post {
                if (stream != null && videoThread?.isInterrupted == false) {
                    val mediaItem = MediaItem.fromUri(stream)
                    exoPlayer.setMediaItem(mediaItem)
                    exoPlayer.prepare()
                    exoPlayer.play()
                }
            }
        }"""

play_video_new = """        videoThread = Thread {
            val info = YoutubeExtractor.getPlaybackInfo(videoId)
            // Need to run on main thread
            android.os.Handler(android.os.Looper.getMainLooper()).post {
                if (info != null && videoThread?.isInterrupted == false) {
                    playbackInfo = info
                    _availableResolutions.value = info.resolutions
                    _currentResolution.value = "Auto"
                    val url = info.autoUrl ?: info.resolutions.firstOrNull()?.url
                    if (url != null) {
                        val mediaItem = MediaItem.fromUri(url)
                        exoPlayer.setMediaItem(mediaItem)
                        exoPlayer.prepare()
                        exoPlayer.play()
                    }
                }
            }
        }"""

content = content.replace(play_video_old, play_video_new)

set_res = """    fun setResolution(res: String) {
        _currentResolution.value = res
        val position = exoPlayer.currentPosition
        val info = playbackInfo ?: return
        val url = if (res == "Auto") info.autoUrl else info.resolutions.find { it.resolution == res }?.url
        if (url != null) {
            val mediaItem = MediaItem.fromUri(url)
            exoPlayer.setMediaItem(mediaItem)
            exoPlayer.seekTo(position)
            exoPlayer.prepare()
            exoPlayer.play()
        }
    }
"""

content = content.replace("    fun setFullscreen(full: Boolean) {", set_res + "\n    fun setFullscreen(full: Boolean) {")

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)

