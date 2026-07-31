import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# We need to replace the Dialog block in InlineVideoPlayer
# Since it's a bit complex, let's just replace the whole if (isFullscreen) block up to else

start_str = """    if (isFullscreen) {
        BackHandler { onFullscreenToggle(false) }"""
end_str = """    } else {
        Box(
            modifier = modifier
                .clickable("""

replacement = """    if (isFullscreen) {
        BackHandler { onFullscreenToggle(false) }
        DisposableEffect(Unit) {
            val activity = context as? Activity
            activity?.requestedOrientation = ActivityInfo.SCREEN_ORIENTATION_SENSOR_LANDSCAPE
            
            activity?.window?.let { window ->
                val insetsController = WindowCompat.getInsetsController(window, window.decorView)
                insetsController.hide(WindowInsetsCompat.Type.systemBars())
                insetsController.systemBarsBehavior = WindowInsetsControllerCompat.BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE
            }
            onDispose {
                activity?.requestedOrientation = ActivityInfo.SCREEN_ORIENTATION_UNSPECIFIED
                activity?.window?.let { window ->
                    val insetsController = WindowCompat.getInsetsController(window, window.decorView)
                    insetsController.show(WindowInsetsCompat.Type.systemBars())
                }
            }
        }
        Box(
            modifier = modifier
                .fillMaxSize()
                .background(Color.Black)
                .clickable(
                    interactionSource = remember { MutableInteractionSource() },
                    indication = null
                ) { showControls = !showControls }
        ) {
            AndroidView(
                factory = { ctx ->
                    PlayerView(ctx).apply {
                        player = exoPlayer
                        useController = false
                        resizeMode = AspectRatioFrameLayout.RESIZE_MODE_FIT
                    }
                },
                modifier = Modifier.fillMaxSize()
            )
            
            VideoPlayerOverlay(
                exoPlayer = exoPlayer,
                title = title,
                isPlaying = isPlaying,
                showControls = showControls,
                isFull = true,
                onFullscreenToggle = onFullscreenToggle,
                availableResolutions = availableResolutions,
                currentResolution = currentResolution,
                onResolutionSelect = onResolutionSelect
            )
        }
"""

if start_str in content and end_str in content:
    start_idx = content.find(start_str)
    end_idx = content.find(end_str)
    new_content = content[:start_idx] + replacement + content[end_idx:]
    with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
        f.write(new_content)
    print("Replaced Dialog successfully")
else:
    print("Could not find start/end strings")
