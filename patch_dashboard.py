import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# 1. Hide in Scaffold if isFullscreen
# For tablet:
tablet_player = """                            Box(modifier = Modifier.weight(2f).fillMaxHeight()) {
                                InlineVideoPlayer(
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
                                )
                            }"""
tablet_player_new = """                            if (!isFullscreen) {
                                Box(modifier = Modifier.weight(2f).fillMaxHeight()) {
                                    InlineVideoPlayer(
                                        exoPlayer = viewModel.exoPlayer,
                                        title = currentPlayingTitle,
                                        isFullscreen = false,
                                        onFullscreenToggle = { viewModel.setFullscreen(it) },
                                        availableResolutions = availableResolutions,
                                        currentResolution = currentResolution,
                                        onResolutionSelect = { viewModel.setResolution(it) },
                                        modifier = Modifier
                                            .fillMaxWidth()
                                            .aspectRatio(16f / 9f)
                                            .background(Color.Black)
                                    )
                                }
                            }"""
content = content.replace(tablet_player, tablet_player_new)

# For phone:
phone_player = """                        if (currentPlayingVideoId != null && !isVideoMinimized) {
                            InlineVideoPlayer(
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
                            )
                        }"""
phone_player_new = """                        if (currentPlayingVideoId != null && !isVideoMinimized && !isFullscreen) {
                            InlineVideoPlayer(
                                exoPlayer = viewModel.exoPlayer,
                                title = currentPlayingTitle,
                                isFullscreen = false,
                                onFullscreenToggle = { viewModel.setFullscreen(it) },
                                availableResolutions = availableResolutions,
                                currentResolution = currentResolution,
                                onResolutionSelect = { viewModel.setResolution(it) },
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .aspectRatio(16f / 9f)
                                    .background(Color.Black)
                            )
                        }"""
content = content.replace(phone_player, phone_player_new)


# 2. Add full screen overlay at the end of ModernDarkDashboard
overlay = """            }
        }
        
        if (isFullscreen && currentPlayingVideoId != null) {
            Box(modifier = Modifier.fillMaxSize().zIndex(100f)) {
                InlineVideoPlayer(
                    exoPlayer = viewModel.exoPlayer,
                    title = currentPlayingTitle,
                    isFullscreen = true,
                    onFullscreenToggle = { viewModel.setFullscreen(it) },
                    availableResolutions = availableResolutions,
                    currentResolution = currentResolution,
                    onResolutionSelect = { viewModel.setResolution(it) },
                    modifier = Modifier.fillMaxSize().background(Color.Black)
                )
            }
        }
    }
}

@Composable
fun VideoListContent("""

end_dashboard = """            }
        }
    }
}

@Composable
fun VideoListContent("""

content = content.replace(end_dashboard, overlay)

# We need zIndex import
import_idx = content.find("import ")
if "import androidx.compose.ui.zIndex.zIndex" not in content:
    content = content[:import_idx] + "import androidx.compose.ui.zIndex.zIndex\n" + content[import_idx:]

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
