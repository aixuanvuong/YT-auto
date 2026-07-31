import re

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Add relatedVideos to MainViewModel
if "val relatedVideos =" not in content:
    vm_add_related = """    private val _currentPlayingVideoId = MutableStateFlow<String?>(null)
    val currentPlayingVideoId = _currentPlayingVideoId.asStateFlow()

    private val _relatedVideos = MutableStateFlow<List<VideoItem>>(emptyList())
    val relatedVideos = _relatedVideos.asStateFlow()

    private var relatedJob: Job? = null"""
    
    content = content.replace("    private val _currentPlayingVideoId = MutableStateFlow<String?>(null)\n    val currentPlayingVideoId = _currentPlayingVideoId.asStateFlow()", vm_add_related)

# Modify playVideo to fetch related videos
play_video_old = """    fun playVideo(videoId: String, title: String, channel: String) {
        addHistory(VideoItem(title, channel, videoId))
        _currentPlayingVideoId.value = videoId
        
        exoPlayer.stop()
        exoPlayer.clearMediaItems()
        
        videoThread?.interrupt()
        videoThread = Thread {
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
        }
        videoThread?.start()
    }"""

play_video_new = """    fun playVideo(videoId: String, title: String, channel: String) {
        addHistory(VideoItem(title, channel, videoId))
        _currentPlayingVideoId.value = videoId
        
        exoPlayer.stop()
        exoPlayer.clearMediaItems()
        
        videoThread?.interrupt()
        videoThread = Thread {
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
        }
        videoThread?.start()
        
        relatedJob?.cancel()
        relatedJob = viewModelScope.launch(Dispatchers.IO) {
            val related = com.example.youtube.YoutubeRelated.getRelated(videoId)
            _relatedVideos.value = related
        }
    }"""
    
content = content.replace(play_video_old, play_video_new)

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)

