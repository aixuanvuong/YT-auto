import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Replace ModernDarkDashboard
dashboard_start = content.find("fun ModernDarkDashboard(")
dashboard_end = content.find("fun FloatingSearchBar(")

if dashboard_start != -1 and dashboard_end != -1:
    old_dashboard = content[dashboard_start:dashboard_end]
    
    new_dashboard = """@OptIn(androidx.compose.material3.ExperimentalMaterial3Api::class)
fun ModernDarkDashboard(viewModel: MainViewModel) {
    val context = LocalContext.current
    var searchQuery by remember { mutableStateOf("") }
    var isSearchExpanded by remember { mutableStateOf(false) }
    
    val searchResults by viewModel.searchResults.collectAsState()
    val isSearching by viewModel.isSearching.collectAsState()
    val history by viewModel.history.collectAsState()
    val focusManager = LocalFocusManager.current
    
    val currentPlayingVideoId by viewModel.currentPlayingVideoId.collectAsState()
    val isFullscreen by viewModel.isFullscreen.collectAsState()
    val relatedVideos by viewModel.relatedVideos.collectAsState()
    val availableResolutions by viewModel.availableResolutions.collectAsState()
    val currentResolution by viewModel.currentResolution.collectAsState()

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
                isSearchExpanded = false
            }
        }
    }

    Scaffold(
        topBar = {
            if (!isFullscreen) {
                androidx.compose.material3.TopAppBar(
                    title = {
                        if (isSearchExpanded) {
                            TextField(
                                value = searchQuery,
                                onValueChange = { 
                                    searchQuery = it
                                    viewModel.search(it)
                                },
                                placeholder = { Text("Tìm kiếm YouTube...", color = Color.Gray) },
                                colors = TextFieldDefaults.colors(
                                    focusedContainerColor = Color.Transparent,
                                    unfocusedContainerColor = Color.Transparent,
                                    focusedIndicatorColor = Color.Transparent,
                                    unfocusedIndicatorColor = Color.Transparent,
                                    focusedTextColor = Color.White,
                                    unfocusedTextColor = Color.White
                                ),
                                singleLine = true,
                                keyboardOptions = KeyboardOptions(imeAction = ImeAction.Search),
                                keyboardActions = KeyboardActions(onSearch = { focusManager.clearFocus() })
                            )
                        } else {
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Icon(
                                    imageVector = androidx.compose.material.icons.Icons.Default.PlayArrow,
                                    contentDescription = "Logo",
                                    tint = Color.Red,
                                    modifier = Modifier.size(32.dp).background(Color.White, CircleShape)
                                )
                                Spacer(modifier = Modifier.width(8.dp))
                                Text(
                                    "YouTube",
                                    color = Color.White,
                                    fontWeight = FontWeight.Bold,
                                    fontSize = 20.sp,
                                    letterSpacing = (-1).sp
                                )
                            }
                        }
                    },
                    actions = {
                        if (isSearchExpanded) {
                            IconButton(onClick = { 
                                isSearchExpanded = false
                                searchQuery = ""
                                viewModel.search("")
                            }) {
                                Icon(Icons.Default.Close, "Close Search", tint = Color.White)
                            }
                        } else {
                            IconButton(onClick = { isSearchExpanded = true }) {
                                Icon(Icons.Default.Search, "Search", tint = Color.White)
                            }
                            IconButton(
                                onClick = {
                                    val intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH).apply {
                                        putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
                                    }
                                    try {
                                        voiceSearchLauncher.launch(intent)
                                    } catch (e: Exception) {}
                                }
                            ) {
                                Icon(Icons.Default.Mic, "Voice Search", tint = Color.White)
                            }
                        }
                    },
                    colors = androidx.compose.material3.TopAppBarDefaults.topAppBarColors(
                        containerColor = Color(0xFF0F0F0F)
                    )
                )
            }
        },
        containerColor = Color(0xFF0F0F0F),
        modifier = Modifier.fillMaxSize()
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
        ) {
            if (currentPlayingVideoId != null) {
                InlineVideoPlayer(
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
                )
            }
            
            VideoListContent(
                searchQuery = searchQuery,
                history = history,
                searchResults = searchResults,
                relatedVideos = relatedVideos,
                currentPlayingVideoId = currentPlayingVideoId,
                playVideo = { videoId, title, channel -> viewModel.playVideo(videoId, title, channel) },
                modifier = Modifier.weight(1f)
            )
        }
    }
}
"""
    content = content[:dashboard_start] + new_dashboard + content[dashboard_end:]

    if "import androidx.compose.material.icons.filled.PlayArrow" not in content:
        content = content.replace("import androidx.compose.material.icons.filled.Person", "import androidx.compose.material.icons.filled.Person\nimport androidx.compose.material.icons.filled.PlayArrow\nimport androidx.compose.material.icons.filled.Close\nimport androidx.compose.material3.Scaffold\nimport androidx.compose.material3.TopAppBar")
    
    with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
        f.write(content)
        print("Updated ModernDarkDashboard")
else:
    print("Could not find ModernDarkDashboard")

