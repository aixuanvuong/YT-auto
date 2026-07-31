import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Modify InlineVideoPlayer
player_def_old = """fun InlineVideoPlayer(
    exoPlayer: ExoPlayer, 
    isFullscreen: Boolean, 
    onFullscreenToggle: (Boolean) -> Unit, 
    availableResolutions: List<com.example.youtube.VideoResolution>,
    currentResolution: String,
    onResolutionSelect: (String) -> Unit,
    modifier: Modifier = Modifier
) {"""

player_def_new = """fun InlineVideoPlayer(
    exoPlayer: ExoPlayer, 
    isFullscreen: Boolean, 
    onFullscreenToggle: (Boolean) -> Unit, 
    availableResolutions: List<com.example.youtube.VideoResolution>,
    currentResolution: String,
    onResolutionSelect: (String) -> Unit,
    modifier: Modifier = Modifier,
    isMinimized: Boolean = false
) {"""
content = content.replace(player_def_old, player_def_new)

# Modify AndroidView apply blocks inside else branch of InlineVideoPlayer
else_block_old = """    } else {
        Box(modifier = modifier) {
            AndroidView(
                factory = { ctx ->
                    PlayerView(ctx).apply {
                        player = exoPlayer
                        useController = true
                        resizeMode = AspectRatioFrameLayout.RESIZE_MODE_FIT
                        setControllerVisibilityListener(PlayerControlView.VisibilityListener { visibility -> 
                            showControls = (visibility == View.VISIBLE)
                        })
                    }
                },
                modifier = Modifier.matchParentSize()
            )
            
            VideoPlayerOverlay(
                showControls = showControls,
                isFull = false,
                onFullscreenToggle = onFullscreenToggle,
                availableResolutions = availableResolutions,
                currentResolution = currentResolution,
                onResolutionSelect = onResolutionSelect
            )
        }
    }"""

else_block_new = """    } else {
        Box(modifier = modifier) {
            AndroidView(
                factory = { ctx ->
                    PlayerView(ctx).apply {
                        player = exoPlayer
                        useController = !isMinimized
                        resizeMode = AspectRatioFrameLayout.RESIZE_MODE_FIT
                        setControllerVisibilityListener(PlayerControlView.VisibilityListener { visibility -> 
                            showControls = (visibility == View.VISIBLE)
                        })
                    }
                },
                update = { view ->
                    view.useController = !isMinimized
                },
                modifier = Modifier.matchParentSize()
            )
            
            if (!isMinimized) {
                VideoPlayerOverlay(
                    showControls = showControls,
                    isFull = false,
                    onFullscreenToggle = onFullscreenToggle,
                    availableResolutions = availableResolutions,
                    currentResolution = currentResolution,
                    onResolutionSelect = onResolutionSelect
                )
            }
        }
    }"""
content = content.replace(else_block_old, else_block_new)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
