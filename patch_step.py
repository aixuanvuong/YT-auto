import re

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Add imports
imports = """
import android.app.Activity
import android.content.pm.ActivityInfo
import android.speech.RecognizerIntent
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.material.icons.filled.Mic
"""
content = content.replace("import android.os.Bundle", imports + "import android.os.Bundle")

# Patch InlineVideoPlayer
new_player = """@Composable
fun InlineVideoPlayer(videoId: String, modifier: Modifier = Modifier) {
    val context = LocalContext.current
    val exoPlayer = remember { ExoPlayer.Builder(context).build() }
    var isFullscreen by remember { mutableStateOf(false) }
    var showControls by remember { mutableStateOf(true) }

    DisposableEffect(videoId) {
        exoPlayer.stop()
        exoPlayer.clearMediaItems()
        
        var thread: Thread? = null
        thread = Thread {
            val stream = YoutubeExtractor.getStream(videoId)
            (context as? ComponentActivity)?.runOnUiThread {
                if (stream != null && thread?.isInterrupted == false) {
                    val mediaItem = MediaItem.fromUri(stream)
                    exoPlayer.setMediaItem(mediaItem)
                    exoPlayer.prepare()
                    exoPlayer.play()
                }
            }
        }
        thread?.start()

        onDispose {
            thread?.interrupt()
        }
    }
    
    DisposableEffect(Unit) {
        onDispose {
            exoPlayer.release()
        }
    }

    if (isFullscreen) {
        DisposableEffect(Unit) {
            val activity = context as? Activity
            activity?.requestedOrientation = ActivityInfo.SCREEN_ORIENTATION_SENSOR_LANDSCAPE
            onDispose {
                activity?.requestedOrientation = ActivityInfo.SCREEN_ORIENTATION_UNSPECIFIED
            }
        }
        Dialog(
            onDismissRequest = { isFullscreen = false },
            properties = DialogProperties(
                usePlatformDefaultWidth = false,
                decorFitsSystemWindows = false
            )
        ) {
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
                            setControllerVisibilityListener(PlayerControlView.VisibilityListener { visibility -> 
                                showControls = (visibility == View.VISIBLE)
                            })
                        }
                    },
                    modifier = Modifier.fillMaxSize()
                )
                AnimatedVisibility(
                    visible = showControls,
                    enter = fadeIn(),
                    exit = fadeOut(),
                    modifier = Modifier
                        .align(Alignment.TopEnd)
                        .padding(16.dp)
                ) {
                    IconButton(
                        onClick = { isFullscreen = false },
                        modifier = Modifier
                            .background(Color.Black.copy(alpha = 0.5f), CircleShape)
                    ) {
                        Icon(
                            imageVector = Icons.Default.FullscreenExit,
                            contentDescription = "Exit Fullscreen",
                            tint = Color.White
                        )
                    }
                }
            }
        }
    } else {
        Box(modifier = modifier) {
            AndroidView(
                factory = { ctx ->
                    PlayerView(ctx).apply {
                        player = exoPlayer
                        useController = true
                        setControllerVisibilityListener(PlayerControlView.VisibilityListener { visibility -> 
                            showControls = (visibility == View.VISIBLE)
                        })
                    }
                },
                modifier = Modifier.fillMaxSize()
            )
            AnimatedVisibility(
                visible = showControls,
                enter = fadeIn(),
                exit = fadeOut(),
                modifier = Modifier
                    .align(Alignment.TopEnd)
                    .padding(8.dp)
            ) {
                IconButton(
                    onClick = { isFullscreen = true },
                    modifier = Modifier
                        .background(Color.Black.copy(alpha = 0.5f), CircleShape)
                ) {
                    Icon(
                        imageVector = Icons.Default.Fullscreen,
                        contentDescription = "Fullscreen",
                        tint = Color.White
                    )
                }
            }
        }
    }
}"""

content = re.sub(r'@Composable\s+fun InlineVideoPlayer.*?@Composable\s+fun ModernDarkDashboard', new_player + "\n\n@Composable\nfun ModernDarkDashboard", content, flags=re.DOTALL)


# Patch ModernDarkDashboard for mic icon
new_dashboard = """@Composable
fun ModernDarkDashboard(viewModel: MainViewModel) {
    val context = LocalContext.current
    var searchQuery by remember { mutableStateOf("") }
    val searchResults by viewModel.searchResults.collectAsState()
    val isSearching by viewModel.isSearching.collectAsState()
    val history by viewModel.history.collectAsState()
    val focusManager = LocalFocusManager.current
    
    var currentPlayingVideoId by remember { mutableStateOf<String?>(null) }

    fun playVideo(videoId: String, title: String, channel: String) {
        viewModel.addHistory(VideoItem(title, channel, videoId))
        currentPlayingVideoId = videoId
    }
    
    val voiceSearchLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.StartActivityForResult()
    ) { result ->
        if (result.resultCode == Activity.RESULT_OK) {
            val data = result.data
            val results = data?.getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS)
            val spokenText = results?.get(0)
            if (!spokenText.isNullOrBlank()) {
                searchQuery = spokenText
                viewModel.search(spokenText)
            }
        }
    }

    val bgGradient = Brush.verticalGradient(
        colors = listOf(
            Color(0xFF0F172A),
            Color(0xFF000000)
        )
    )

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(bgGradient)
            .windowInsetsPadding(WindowInsets.systemBars)
    ) {
        // Search Header
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .padding(start = 24.dp, end = 24.dp, top = 16.dp, bottom = 16.dp)
                .background(Color.White.copy(alpha = 0.05f), RoundedCornerShape(24.dp))
                .border(1.dp, Color.White.copy(alpha = 0.1f), RoundedCornerShape(24.dp))
                .padding(horizontal = 16.dp, vertical = 8.dp)
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.CenterVertically
            ) {
                TextField(
                    value = searchQuery,
                    onValueChange = { 
                        searchQuery = it 
                        viewModel.search(it)
                    },
                    placeholder = { Text("Search YouTube...", color = Color.Gray, fontSize = 15.sp) },
                    colors = TextFieldDefaults.colors(
                        focusedContainerColor = Color.Transparent,
                        unfocusedContainerColor = Color.Transparent,
                        focusedIndicatorColor = Color.Transparent,
                        unfocusedIndicatorColor = Color.Transparent,
                        focusedTextColor = Color.White,
                        unfocusedTextColor = Color.White
                    ),
                    modifier = Modifier.weight(1f),
                    singleLine = true,
                    keyboardOptions = KeyboardOptions(imeAction = ImeAction.Search),
                    keyboardActions = KeyboardActions(onSearch = { focusManager.clearFocus() })
                )
                
                IconButton(
                    onClick = {
                        val intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH).apply {
                            putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
                        }
                        try {
                            voiceSearchLauncher.launch(intent)
                        } catch (e: Exception) {
                            // Ignore
                        }
                    }
                ) {
                    Icon(
                        imageVector = Icons.Default.Mic,
                        contentDescription = "Voice Search",
                        tint = Color.White
                    )
                }
                
                Box(
                    modifier = Modifier
                        .size(36.dp)
                        .background(Color.White.copy(alpha = 0.1f), CircleShape)
                        .clickable {
                            if (searchQuery.isNotBlank()) {
                                viewModel.search(searchQuery)
                            }
                        },
                    contentAlignment = Alignment.Center
                ) {
                    if (isSearching) {
                        CircularProgressIndicator(color = Color.White, modifier = Modifier.size(18.dp), strokeWidth = 2.dp)
                    } else {
                        Icon(
                            imageVector = Icons.Default.Search,
                            contentDescription = "Search",
                            tint = Color.White,
                            modifier = Modifier.size(18.dp)
                        )
                    }
                }
            }
        }
        
        if (currentPlayingVideoId != null) {
            InlineVideoPlayer(
                videoId = currentPlayingVideoId!!,
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(start = 24.dp, end = 24.dp, bottom = 16.dp)
                    .aspectRatio(16f / 9f)
                    .clip(RoundedCornerShape(12.dp))
                    .background(Color.Black)
            )
        }

        LazyColumn(
            modifier = Modifier
                .fillMaxWidth()
                .weight(1f)
                .padding(horizontal = 24.dp),
            contentPadding = PaddingValues(bottom = 16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            if (searchQuery.isBlank()) {
                item {
                    Text(
                        text = "LỊCH SỬ TÌM KIẾM",
                        fontSize = 12.sp,
                        fontWeight = FontWeight.Bold,
                        letterSpacing = 1.2.sp,
                        color = Color.Gray,
                        modifier = Modifier.padding(bottom = 8.dp)
                    )
                }
                if (history.isEmpty()) {
                    item {
                        Text(
                            text = "Chưa có lịch sử tìm kiếm",
                            color = Color.Gray,
                            fontSize = 14.sp
                        )
                    }
                } else {
                    items(history) { video ->
                        GlassVideoCard(
                            title = video.title,
                            subtitle = video.channel,
                            videoId = video.videoId,
                            onClick = { playVideo(video.videoId, video.title, video.channel) }
                        )
                    }
                }
            } else {
                item {
                    Text(
                        text = "KẾT QUẢ TÌM KIẾM",
                        fontSize = 12.sp,
                        fontWeight = FontWeight.Bold,
                        letterSpacing = 1.2.sp,
                        color = Color.Gray,
                        modifier = Modifier.padding(bottom = 8.dp)
                    )
                }
                items(searchResults) { video ->
                    GlassVideoCard(
                        title = video.title,
                        subtitle = video.channel,
                        videoId = video.videoId,
                        onClick = { playVideo(video.videoId, video.title, video.channel) }
                    )
                }
            }
        }
    }
}"""

content = re.sub(r'@Composable\s+fun ModernDarkDashboard.*?@Composable\s+fun GlassVideoCard', new_dashboard + "\n\n@Composable\nfun GlassVideoCard", content, flags=re.DOTALL)

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
