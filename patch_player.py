import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# 1. Update InlineVideoPlayer definition
old_inline_def = """fun InlineVideoPlayer(
    exoPlayer: ExoPlayer, 
    isFullscreen: Boolean, 
    onFullscreenToggle: (Boolean) -> Unit, 
    availableResolutions: List<com.example.youtube.VideoResolution>,
    currentResolution: String,
    onResolutionSelect: (String) -> Unit,
    modifier: Modifier = Modifier,
    isMinimized: Boolean = false
) {"""

new_inline_def = """fun InlineVideoPlayer(
    exoPlayer: ExoPlayer, 
    title: String,
    isFullscreen: Boolean, 
    onFullscreenToggle: (Boolean) -> Unit, 
    availableResolutions: List<com.example.youtube.VideoResolution>,
    currentResolution: String,
    onResolutionSelect: (String) -> Unit,
    modifier: Modifier = Modifier,
    isMinimized: Boolean = false
) {"""

content = content.replace(old_inline_def, new_inline_def)

# 2. Update InlineVideoPlayer usages in ModernDarkDashboard
content = content.replace("""InlineVideoPlayer(
                                    exoPlayer = viewModel.exoPlayer,
                                    isFullscreen = false,
                                    onFullscreenToggle = {},
                                    availableResolutions = emptyList(),
                                    currentResolution = "Auto",
                                    onResolutionSelect = {},
                                    isMinimized = true,
                                    modifier = Modifier.fillMaxSize()
                                )""", """InlineVideoPlayer(
                                    exoPlayer = viewModel.exoPlayer,
                                    title = currentPlayingTitle,
                                    isFullscreen = false,
                                    onFullscreenToggle = {},
                                    availableResolutions = emptyList(),
                                    currentResolution = "Auto",
                                    onResolutionSelect = {},
                                    isMinimized = true,
                                    modifier = Modifier.fillMaxSize()
                                )""")

content = content.replace("""InlineVideoPlayer(
                                    exoPlayer = viewModel.exoPlayer,
                                    isFullscreen = isFullscreen,
                                    onFullscreenToggle = { viewModel.setFullscreen(it) },
                                    availableResolutions = availableResolutions,
                                    currentResolution = currentResolution,
                                    onResolutionSelect = { viewModel.setResolution(it) },
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .aspectRatio(16f / 9f)
                                        .background(Color.Black)
                                )""", """InlineVideoPlayer(
                                    exoPlayer = viewModel.exoPlayer,
                                    title = currentPlayingTitle,
                                    isFullscreen = isFullscreen,
                                    onFullscreenToggle = { viewModel.setFullscreen(it) },
                                    availableResolutions = availableResolutions,
                                    currentResolution = currentResolution,
                                    onResolutionSelect = { viewModel.setResolution(it) },
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .aspectRatio(16f / 9f)
                                        .background(Color.Black)
                                )""")

content = content.replace("""InlineVideoPlayer(
                                exoPlayer = viewModel.exoPlayer,
                                isFullscreen = isFullscreen,
                                onFullscreenToggle = { viewModel.setFullscreen(it) },
                                availableResolutions = availableResolutions,
                                currentResolution = currentResolution,
                                onResolutionSelect = { viewModel.setResolution(it) },
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .aspectRatio(16f / 9f)
                                    .background(Color.Black)
                            )""", """InlineVideoPlayer(
                                exoPlayer = viewModel.exoPlayer,
                                title = currentPlayingTitle,
                                isFullscreen = isFullscreen,
                                onFullscreenToggle = { viewModel.setFullscreen(it) },
                                availableResolutions = availableResolutions,
                                currentResolution = currentResolution,
                                onResolutionSelect = { viewModel.setResolution(it) },
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .aspectRatio(16f / 9f)
                                    .background(Color.Black)
                            )""")


with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
