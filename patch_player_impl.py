import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Replace InlineVideoPlayer body and VideoPlayerOverlay
start_idx = content.find("fun InlineVideoPlayer(")
end_idx = content.find("@Composable\nfun YouTubeVideoCard(")

if start_idx != -1 and end_idx != -1:
    new_code = """fun InlineVideoPlayer(
    exoPlayer: ExoPlayer, 
    title: String,
    isFullscreen: Boolean, 
    onFullscreenToggle: (Boolean) -> Unit, 
    availableResolutions: List<com.example.youtube.VideoResolution>,
    currentResolution: String,
    onResolutionSelect: (String) -> Unit,
    modifier: Modifier = Modifier,
    isMinimized: Boolean = false
) {
    val context = LocalContext.current
    var showControls by remember { mutableStateOf(true) }
    var isPlaying by remember { mutableStateOf(exoPlayer.isPlaying) }
    
    DisposableEffect(exoPlayer) {
        val listener = object : com.google.android.exoplayer2.Player.Listener {
            override fun onIsPlayingChanged(playing: Boolean) {
                isPlaying = playing
            }
        }
        exoPlayer.addListener(listener)
        onDispose { exoPlayer.removeListener(listener) }
    }

    LaunchedEffect(showControls, isPlaying) {
        if (showControls && isPlaying) {
            delay(3500)
            showControls = false
        }
    }

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
        }
    } else {
        Box(
            modifier = modifier
                .clickable(
                    interactionSource = remember { MutableInteractionSource() },
                    indication = null
                ) { if (!isMinimized) showControls = !showControls }
        ) {
            AndroidView(
                factory = { ctx ->
                    PlayerView(ctx).apply {
                        player = exoPlayer
                        useController = false
                        resizeMode = AspectRatioFrameLayout.RESIZE_MODE_FIT
                    }
                },
                modifier = Modifier.matchParentSize()
            )
            
            if (!isMinimized) {
                VideoPlayerOverlay(
                    exoPlayer = exoPlayer,
                    title = title,
                    isPlaying = isPlaying,
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
}

@Composable
fun VideoPlayerOverlay(
    exoPlayer: ExoPlayer,
    title: String,
    isPlaying: Boolean,
    showControls: Boolean,
    isFull: Boolean,
    onFullscreenToggle: (Boolean) -> Unit,
    availableResolutions: List<com.example.youtube.VideoResolution>,
    currentResolution: String,
    onResolutionSelect: (String) -> Unit
) {
    var position by remember { mutableLongStateOf(0L) }
    var duration by remember { mutableLongStateOf(0L) }
    var buffered by remember { mutableLongStateOf(0L) }
    
    LaunchedEffect(isPlaying, showControls) {
        while (true) {
            position = exoPlayer.currentPosition
            duration = exoPlayer.duration.coerceAtLeast(0L)
            buffered = exoPlayer.bufferedPosition
            delay(1000)
        }
    }

    AnimatedVisibility(
        visible = showControls,
        enter = fadeIn(),
        exit = fadeOut(),
        modifier = Modifier.fillMaxSize()
    ) {
        Box(
            modifier = Modifier
                .fillMaxSize()
                .background(Color.Black.copy(alpha = 0.5f))
        ) {
            // Top Bar
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .align(Alignment.TopCenter)
                    .padding(horizontal = 16.dp, vertical = 8.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                if (isFull) {
                    IconButton(onClick = { onFullscreenToggle(false) }) {
                        Icon(Icons.Default.ArrowBack, contentDescription = "Back", tint = Color.White)
                    }
                }
                Text(
                    text = title,
                    color = Color.White,
                    fontSize = 16.sp,
                    fontWeight = FontWeight.Medium,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis,
                    modifier = Modifier.weight(1f).padding(start = if (isFull) 8.dp else 0.dp)
                )
                
                var menuExpanded by remember { mutableStateOf(false) }
                Box {
                    IconButton(onClick = { menuExpanded = true }) {
                        Icon(Icons.Default.Settings, contentDescription = "Settings", tint = Color.White)
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
            }
            
            // Center Play/Pause
            Row(
                modifier = Modifier.align(Alignment.Center),
                horizontalArrangement = Arrangement.spacedBy(32.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                IconButton(
                    onClick = { 
                        exoPlayer.seekTo((exoPlayer.currentPosition - 10000).coerceAtLeast(0L))
                        position = exoPlayer.currentPosition
                    },
                    modifier = Modifier.size(48.dp)
                ) {
                    Icon(androidx.compose.material.icons.Icons.Default.Replay10, contentDescription = "Rewind 10s", tint = Color.White, modifier = Modifier.size(36.dp))
                }
                
                IconButton(
                    onClick = {
                        if (isPlaying) exoPlayer.pause() else exoPlayer.play()
                    },
                    modifier = Modifier
                        .size(64.dp)
                        .background(Color.Black.copy(alpha = 0.4f), CircleShape)
                ) {
                    Icon(
                        imageVector = if (isPlaying) androidx.compose.material.icons.Icons.Default.Pause else androidx.compose.material.icons.Icons.Default.PlayArrow,
                        contentDescription = "Play/Pause",
                        tint = Color.White,
                        modifier = Modifier.size(40.dp)
                    )
                }
                
                IconButton(
                    onClick = { 
                        exoPlayer.seekTo((exoPlayer.currentPosition + 10000).coerceAtMost(duration))
                        position = exoPlayer.currentPosition
                    },
                    modifier = Modifier.size(48.dp)
                ) {
                    Icon(androidx.compose.material.icons.Icons.Default.Forward10, contentDescription = "Forward 10s", tint = Color.White, modifier = Modifier.size(36.dp))
                }
            }
            
            // Bottom Bar
            Column(
                modifier = Modifier
                    .align(Alignment.BottomCenter)
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp, vertical = 8.dp)
            ) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text(
                        text = formatTime(position),
                        color = Color.White,
                        fontSize = 12.sp
                    )
                    
                    Slider(
                        value = if (duration > 0) position.toFloat() / duration.toFloat() else 0f,
                        onValueChange = { 
                            val newPos = (it * duration).toLong()
                            exoPlayer.seekTo(newPos)
                            position = newPos
                        },
                        colors = androidx.compose.material3.SliderDefaults.colors(
                            thumbColor = Color.Red,
                            activeTrackColor = Color.Red,
                            inactiveTrackColor = Color.White.copy(alpha = 0.3f)
                        ),
                        modifier = Modifier
                            .weight(1f)
                            .padding(horizontal = 12.dp)
                    )
                    
                    Text(
                        text = formatTime(duration),
                        color = Color.White,
                        fontSize = 12.sp
                    )
                    
                    Spacer(modifier = Modifier.width(8.dp))
                    
                    IconButton(onClick = { onFullscreenToggle(!isFull) }, modifier = Modifier.size(28.dp)) {
                        Icon(
                            imageVector = if (isFull) Icons.Default.FullscreenExit else Icons.Default.Fullscreen,
                            contentDescription = "Fullscreen",
                            tint = Color.White,
                            modifier = Modifier.size(24.dp)
                        )
                    }
                }
            }
        }
    }
}

fun formatTime(timeMs: Long): String {
    val totalSeconds = timeMs / 1000
    val seconds = totalSeconds % 60
    val minutes = (totalSeconds / 60) % 60
    val hours = totalSeconds / 3600
    
    return if (hours > 0) {
        String.format("%d:%02d:%02d", hours, minutes, seconds)
    } else {
        String.format("%02d:%02d", minutes, seconds)
    }
}

"""
    content = content[:start_idx] + new_code + content[end_idx:]
    
    with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
        f.write(content)
        print("Updated InlineVideoPlayer and VideoPlayerOverlay")
