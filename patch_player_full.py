import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# We will replace the entire InlineVideoPlayer function
player_start = content.find("fun InlineVideoPlayer(")
if player_start != -1:
    player_end = content.find("fun ModernDarkDashboard(")
    if player_end != -1:
        # Extract the old function
        old_player = content[player_start:player_end]
        
        new_player = """fun InlineVideoPlayer(
    exoPlayer: ExoPlayer, 
    isFullscreen: Boolean, 
    onFullscreenToggle: (Boolean) -> Unit, 
    availableResolutions: com.example.youtube.VideoResolution?, // We will use List directly, wait.
    modifier: Modifier = Modifier
) {}""" # Just a placeholder
        
        # Actually let's just write the full function
        new_player = """@Composable
fun InlineVideoPlayer(
    exoPlayer: ExoPlayer, 
    isFullscreen: Boolean, 
    onFullscreenToggle: (Boolean) -> Unit, 
    availableResolutions: List<com.example.youtube.VideoResolution>,
    currentResolution: String,
    onResolutionSelect: (String) -> Unit,
    modifier: Modifier = Modifier
) {
    val context = LocalContext.current
    var showControls by remember { mutableStateOf(true) }

    if (isFullscreen) {
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
        Dialog(
            onDismissRequest = { onFullscreenToggle(false) },
            properties = DialogProperties(
                usePlatformDefaultWidth = false,
                decorFitsSystemWindows = false
            )
        ) {
            val view = LocalView.current
            DisposableEffect(view) {
                val dialogWindow = (view.parent as? DialogWindowProvider)?.window
                dialogWindow?.let { window ->
                    window.setLayout(android.view.ViewGroup.LayoutParams.MATCH_PARENT, android.view.ViewGroup.LayoutParams.MATCH_PARENT)
                    WindowCompat.setDecorFitsSystemWindows(window, false)
                    val insetsController = WindowCompat.getInsetsController(window, window.decorView)
                    insetsController.hide(WindowInsetsCompat.Type.systemBars())
                    insetsController.systemBarsBehavior = WindowInsetsControllerCompat.BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE
                }
                onDispose {}
            }

            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .background(Color.Black)
            ) {
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
                    modifier = Modifier.fillMaxSize()
                )
                
                VideoPlayerOverlay(
                    showControls = showControls,
                    isFull = true,
                    onFullscreenToggle = onFullscreenToggle,
                    availableResolutions = availableResolutions,
                    currentResolution = currentResolution,
                    onResolutionSelect = onResolutionSelect
                )
            }
        }
    } else {
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
    }
}

@Composable
fun VideoPlayerOverlay(
    showControls: Boolean,
    isFull: Boolean,
    onFullscreenToggle: (Boolean) -> Unit,
    availableResolutions: List<com.example.youtube.VideoResolution>,
    currentResolution: String,
    onResolutionSelect: (String) -> Unit
) {
    AnimatedVisibility(
        visible = showControls,
        enter = fadeIn(),
        exit = fadeOut(),
        modifier = Modifier
            .fillMaxWidth()
            .padding(16.dp)
    ) {
        Box(modifier = Modifier.fillMaxWidth()) {
            var menuExpanded by remember { mutableStateOf(false) }
            Row(
                modifier = Modifier.align(Alignment.TopEnd),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                Box {
                    IconButton(
                        onClick = { menuExpanded = true },
                        modifier = Modifier
                            .background(Color.Black.copy(alpha = 0.5f), CircleShape)
                    ) {
                        Icon(
                            imageVector = Icons.Default.Settings,
                            contentDescription = "Settings",
                            tint = Color.White
                        )
                    }
                    DropdownMenu(
                        expanded = menuExpanded,
                        onDismissRequest = { menuExpanded = false }
                    ) {
                        DropdownMenuItem(
                            text = { Text("Auto") },
                            trailingIcon = if (currentResolution == "Auto") {
                                { Icon(Icons.Default.Check, "Selected") }
                            } else null,
                            onClick = {
                                onResolutionSelect("Auto")
                                menuExpanded = false
                            }
                        )
                        availableResolutions.forEach { res ->
                            DropdownMenuItem(
                                text = { Text(res.resolution) },
                                trailingIcon = if (currentResolution == res.resolution) {
                                    { Icon(Icons.Default.Check, "Selected") }
                                } else null,
                                onClick = {
                                    onResolutionSelect(res.resolution)
                                    menuExpanded = false
                                }
                            )
                        }
                    }
                }
                
                IconButton(
                    onClick = { onFullscreenToggle(!isFull) },
                    modifier = Modifier
                        .background(Color.Black.copy(alpha = 0.5f), CircleShape)
                ) {
                    Icon(
                        imageVector = if (isFull) Icons.Default.FullscreenExit else Icons.Default.Fullscreen,
                        contentDescription = if (isFull) "Exit Fullscreen" else "Fullscreen",
                        tint = Color.White
                    )
                }
            }
        }
    }
}
"""
        content = content[:player_start] + new_player + content[player_end:]
        with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
            f.write(content)
            print("Successfully updated InlineVideoPlayer")
else:
    print("Could not find InlineVideoPlayer")

