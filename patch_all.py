import re

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

if "import com.google.android.exoplayer2.ui.AspectRatioFrameLayout" not in content:
    content = content.replace("import android.os.Bundle", "import com.google.android.exoplayer2.ui.AspectRatioFrameLayout\nimport android.os.Bundle")

# 1. Update MainViewModel
if "val pauseSignal" not in content:
    view_model_patch = """class MainViewModel : ViewModel() {
    private val _searchResults = MutableStateFlow<List<VideoItem>>(emptyList())
    val searchResults = _searchResults.asStateFlow()

    private val _isSearching = MutableStateFlow(false)
    val isSearching = _isSearching.asStateFlow()
    
    private val _history = MutableStateFlow<List<VideoItem>>(emptyList())
    val history = _history.asStateFlow()

    private val _pauseSignal = MutableStateFlow(0L)
    val pauseSignal = _pauseSignal.asStateFlow()

    fun pauseVideo() {
        _pauseSignal.value = System.currentTimeMillis()
    }"""
    content = re.sub(r'class MainViewModel : ViewModel\(\) \{.*?val history = _history\.asStateFlow\(\)', view_model_patch, content, flags=re.DOTALL)

# 2. Update InlineVideoPlayer
new_player = """@Composable
fun InlineVideoPlayer(videoId: String, viewModel: MainViewModel, modifier: Modifier = Modifier) {
    val context = LocalContext.current
    val exoPlayer = remember { ExoPlayer.Builder(context).build() }
    var isFullscreen by remember { mutableStateOf(false) }
    var showControls by remember { mutableStateOf(true) }

    val pauseSignal by viewModel.pauseSignal.collectAsState()
    
    LaunchedEffect(pauseSignal) {
        if (pauseSignal > 0) {
            exoPlayer.pause()
        }
    }

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
        BackHandler { isFullscreen = false }
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
            onDismissRequest = { isFullscreen = false },
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
                        resizeMode = AspectRatioFrameLayout.RESIZE_MODE_FIT
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

# 3. Update ModernDarkDashboard to pass viewModel to InlineVideoPlayer and to pauseVideo on Voice Search
# Update InlineVideoPlayer calls:
content = content.replace("InlineVideoPlayer(\n                        videoId = currentPlayingVideoId!!,", "InlineVideoPlayer(\n                        videoId = currentPlayingVideoId!!,\n                        viewModel = viewModel,")

# Update voiceSearchLauncher
voice_launcher_old = """val voiceSearchLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.StartActivityForResult()
    ) { result ->"""
voice_launcher_new = """val voiceSearchLauncher = rememberLauncherForActivityResult(
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
    }"""
# Wait, the voice search launcher is inside ModernDarkDashboard. We also want it to pause video when CLICKED.
# Which is in the IconButton onClick.
icon_button_old = """IconButton(
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
            )"""
icon_button_new = """IconButton(
                onClick = {
                    viewModel.pauseVideo() // Pause the video
                    val intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH).apply {
                        putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
                    }
                    try {
                        voiceSearchLauncher.launch(intent)
                    } catch (e: Exception) {
                        // Ignore
                    }
                }
            )"""
content = content.replace(icon_button_old, icon_button_new)

# Wait, there are TWO instances of the IconButton. 
# Oh wait, we refactored it into `SearchHeader`.
search_header_icon_old = """IconButton(
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
            )"""
search_header_icon_new = """IconButton(
                onClick = {
                    onVoiceSearchClick()
                    val intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH).apply {
                        putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
                    }
                    try {
                        voiceSearchLauncher.launch(intent)
                    } catch (e: Exception) {
                        // Ignore
                    }
                }
            )"""
content = content.replace(search_header_icon_old, search_header_icon_new)

# Update SearchHeader signature
search_header_sig_old = """@Composable
fun SearchHeader(
    searchQuery: String,
    onSearchQueryChange: (String) -> Unit,
    isSearching: Boolean,
    focusManager: androidx.compose.ui.focus.FocusManager,
    voiceSearchLauncher: androidx.activity.result.ActivityResultLauncher<Intent>,
    onSearch: () -> Unit
)"""
search_header_sig_new = """@Composable
fun SearchHeader(
    searchQuery: String,
    onSearchQueryChange: (String) -> Unit,
    isSearching: Boolean,
    focusManager: androidx.compose.ui.focus.FocusManager,
    voiceSearchLauncher: androidx.activity.result.ActivityResultLauncher<Intent>,
    onVoiceSearchClick: () -> Unit = {},
    onSearch: () -> Unit
)"""
content = content.replace(search_header_sig_old, search_header_sig_new)

# Update ModernDarkDashboard calls to SearchHeader
content = content.replace("""voiceSearchLauncher = voiceSearchLauncher,
                        onSearch = { viewModel.search(searchQuery) }""",
                        """voiceSearchLauncher = voiceSearchLauncher,
                        onVoiceSearchClick = { viewModel.pauseVideo() },
                        onSearch = { viewModel.search(searchQuery) }""")

content = content.replace("""voiceSearchLauncher = voiceSearchLauncher,
                    onSearch = { viewModel.search(searchQuery) }""",
                    """voiceSearchLauncher = voiceSearchLauncher,
                    onVoiceSearchClick = { viewModel.pauseVideo() },
                    onSearch = { viewModel.search(searchQuery) }""")

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)

