import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Modify ModernDarkDashboard
start_idx = content.find("fun ModernDarkDashboard(")
end_idx = content.find("fun VideoListContent(")
if start_idx != -1 and end_idx != -1:
    old_dashboard = content[start_idx:end_idx]
    
    # We will replace it with a new one
    new_dashboard = """fun ModernDarkDashboard(viewModel: MainViewModel) {
    val context = LocalContext.current
    var searchQuery by remember { mutableStateOf("") }
    var isSearchExpanded by remember { mutableStateOf(false) }
    var selectedTab by remember { mutableStateOf(0) }
    
    val searchResults by viewModel.searchResults.collectAsState()
    val isSearching by viewModel.isSearching.collectAsState()
    val history by viewModel.history.collectAsState()
    val homeVideos by viewModel.homeVideos.collectAsState()
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
                selectedTab = 0
            }
        }
    }
    
    if (currentPlayingVideoId != null && !isFullscreen) {
        BackHandler {
            viewModel.closeVideo()
        }
    }

    Scaffold(
        topBar = {
            if (!isFullscreen) {
                TopAppBar(
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
                            IconButton(onClick = { isSearchExpanded = true; selectedTab = 0 }) {
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
        bottomBar = {
            if (!isFullscreen) {
                NavigationBar(
                    containerColor = Color(0xFF0F0F0F),
                    contentColor = Color.White
                ) {
                    NavigationBarItem(
                        selected = selectedTab == 0,
                        onClick = { selectedTab = 0 },
                        icon = { Icon(androidx.compose.material.icons.Icons.Default.Home, contentDescription = "Trang chủ") },
                        label = { Text("Trang chủ") },
                        colors = NavigationBarItemDefaults.colors(
                            selectedIconColor = Color.White,
                            unselectedIconColor = Color.Gray,
                            selectedTextColor = Color.White,
                            unselectedTextColor = Color.Gray,
                            indicatorColor = Color.Transparent
                        )
                    )
                    NavigationBarItem(
                        selected = selectedTab == 1,
                        onClick = { selectedTab = 1 },
                        icon = { Icon(androidx.compose.material.icons.Icons.Default.History, contentDescription = "Lịch sử") },
                        label = { Text("Lịch sử") },
                        colors = NavigationBarItemDefaults.colors(
                            selectedIconColor = Color.White,
                            unselectedIconColor = Color.Gray,
                            selectedTextColor = Color.White,
                            unselectedTextColor = Color.Gray,
                            indicatorColor = Color.Transparent
                        )
                    )
                }
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
                selectedTab = selectedTab,
                searchQuery = searchQuery,
                history = history,
                homeVideos = homeVideos,
                searchResults = searchResults,
                relatedVideos = relatedVideos,
                currentPlayingVideoId = currentPlayingVideoId,
                playVideo = { videoId, title, channel -> viewModel.playVideo(videoId, title, channel) },
                modifier = Modifier.weight(1f)
            )
        }
    }
}
@Composable
"""
    # Just be careful not to double the @Composable for VideoListContent. It's safe since we replace up to "fun VideoListContent("
    content = content[:start_idx] + new_dashboard + content[end_idx:]
    
    # Add history icon
    if "import androidx.compose.material.icons.filled.History" not in content:
        content = content.replace("import androidx.compose.material.icons.filled.Home", "import androidx.compose.material.icons.filled.Home\nimport androidx.compose.material.icons.filled.History")

    with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
        f.write(content)

