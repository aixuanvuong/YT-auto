import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Add isPlaying state to MainViewModel
if "val isPlaying =" not in content:
    playing_state = """    private val _isPlaying = MutableStateFlow(false)
    val isPlaying = _isPlaying.asStateFlow()

    init {
        exoPlayer.addListener(object : androidx.media3.common.Player.Listener {
            override fun onIsPlayingChanged(isPlaying: Boolean) {
                _isPlaying.value = isPlaying
            }
        })
    }"""
    
    # We already have an init block in MainViewModel
    if "init {" in content:
        # replace the existing init block
        old_init = """    init {
        loadHomeVideos()
    }"""
        new_init = """    init {
        loadHomeVideos()
        exoPlayer.addListener(object : androidx.media3.common.Player.Listener {
            override fun onIsPlayingChanged(isPlaying: Boolean) {
                _isPlaying.value = isPlaying
            }
        })
    }"""
        content = content.replace(old_init, new_init)
        
        # add the _isPlaying property before init
        content = content.replace("    init {", "    private val _isPlaying = MutableStateFlow(false)\n    val isPlaying = _isPlaying.asStateFlow()\n\n    init {")

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
