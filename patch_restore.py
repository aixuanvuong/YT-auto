import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# I will insert ModernDarkDashboard and VideoListContent at the very end of the file, or right before InlineVideoPlayer.
# Let's put them before InlineVideoPlayer

insert_idx = content.find("@Composable\nfun InlineVideoPlayer(")

dashboard_code = """@OptIn(androidx.compose.material3.ExperimentalMaterial3Api::class)
@Composable
fun ModernDarkDashboard(viewModel: MainViewModel) {
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
    val isVideoMinimized by viewModel.isVideoMinimized.collectAsState()
    val isPlaying by viewModel.isPlaying.collectAsState()
    val currentPlayingTitle by viewModel.currentPlayingTitle.collectAsState()

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
    
    if (isSearchExpanded) {
        BackHandler {
            isSearchExpanded = false
            searchQuery = ""
            viewModel.search("")
        }
    } else if (currentPlayingVideoId != null && !isFullscreen) {
        BackHandler {
            if (!isVideoMinimized) {
                viewModel.setVideoMinimized(true)
            } else {
                viewModel.closeVideo()
            }
        }
    }

    BoxWithConstraints(modifier = Modifier.fillMaxSize()) {
        val isTablet = maxWidth >= 600.dp
        
        Row(modifier = Modifier.fillMaxSize()) {
            if (isTablet && !isFullscreen) {
                NavigationRail(
                    containerColor = Color(0xFF0F0F0F),
                    contentColor = Color.White
                ) {
                    NavigationRailItem(
                        selected = selectedTab == 0,
                        onClick = { selectedTab = 0 },
                        icon = { Icon(androidx.compose.material.icons.Icons.Default.Home, contentDescription = "Trang chủ") },
                        label = { Text("Trang chủ", color = Color.White) },
                        colors = NavigationRailItemDefaults.colors(
                            selectedIconColor = Color.White,
                            unselectedIconColor = Color.Gray,
                            indicatorColor = Color.Transparent
                        )
                    )
                    NavigationRailItem(
                        selected = selectedTab == 1,
                        onClick = { selectedTab = 1 },
                        icon = { Icon(androidx.compose.material.icons.Icons.Default.History, contentDescription = "Lịch sử") },
                        label = { Text("Lịch sử", color = Color.White) },
                        colors = NavigationRailItemDefaults.colors(
                            selectedIconColor = Color.White,
                            unselectedIconColor = Color.Gray,
                            indicatorColor = Color.Transparent
                        )
                    )
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
                        Column {
                            if (currentPlayingVideoId != null && isVideoMinimized) {
                                // Minimized player row
                                Row(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .height(60.dp)
                                        .background(Color(0xFF212121))
                                        .clickable { viewModel.setVideoMinimized(false) }
                                        .padding(end = 8.dp),
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Box(modifier = Modifier.fillMaxHeight().aspectRatio(16f/9f)) {
                                        InlineVideoPlayer(
                                            exoPlayer = viewModel.exoPlayer,
                                            title = currentPlayingTitle,
                                            isFullscreen = false,
                                            onFullscreenToggle = {},
                                            availableResolutions = emptyList(),
                                            currentResolution = "Auto",
                                            onResolutionSelect = {},
                                            isMinimized = true,
                                            modifier = Modifier.fillMaxSize()
                                        )
                                    }
                                    
                                    Spacer(modifier = Modifier.width(12.dp))
                                    
                                    Text(
                                        text = currentPlayingTitle,
                                        color = Color.White,
                                        fontSize = 14.sp,
                                        maxLines = 1,
                                        overflow = TextOverflow.Ellipsis,
                                        modifier = Modifier.weight(1f)
                                    )
                                    
                                    IconButton(onClick = { 
                                        if (isPlaying) viewModel.exoPlayer.pause()
                                        else viewModel.exoPlayer.play()
                                    }) {
                                        Icon(
                                            imageVector = if (isPlaying) androidx.compose.material.icons.Icons.Default.Pause else androidx.compose.material.icons.Icons.Default.PlayArrow,
                                            contentDescription = "Play/Pause",
                                            tint = Color.White
                                        )
                                    }
                                    
                                    IconButton(onClick = { viewModel.closeVideo() }) {
                                        Icon(
                                            imageVector = Icons.Default.Close,
                                            contentDescription = "Close",
                                            tint = Color.White
                                        )
                                    }
                                }
                            }
                            if (!isTablet) {
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
                        }
                    }
                },
                containerColor = Color(0xFF0F0F0F),
                modifier = Modifier.weight(1f)
            ) { paddingValues ->
                Column(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(paddingValues)
                ) {
                    if (isTablet && currentPlayingVideoId != null && !isVideoMinimized) {
                        // Split view on Tablet
                        Row(modifier = Modifier.fillMaxSize()) {
                            // Left side: Video Player
                            Box(modifier = Modifier.weight(2f).fillMaxHeight()) {
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
                            }
                            // Right side: Related Videos (List view, not grid)
                            Box(modifier = Modifier.weight(1f).fillMaxHeight()) {
                                VideoListContent(
                                    selectedTab = selectedTab,
                                    searchQuery = searchQuery,
                                    history = history,
                                    homeVideos = homeVideos,
                                    searchResults = searchResults,
                                    relatedVideos = relatedVideos,
                                    currentPlayingVideoId = currentPlayingVideoId,
                                    playVideo = { videoId, title, channel -> viewModel.playVideo(videoId, title, channel) },
                                    isTabletMode = false, // Keep it as a vertical list when alongside video
                                    modifier = Modifier.fillMaxSize()
                                )
                            }
                        }
                    } else {
                        // Phone or no active video on Tablet
                        if (currentPlayingVideoId != null && !isVideoMinimized) {
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
                            isTabletMode = isTablet,
                            modifier = Modifier.weight(1f)
                        )
                    }
                }
            }
        }
    }
}

@Composable
fun VideoListContent(
    selectedTab: Int,
    searchQuery: String,
    history: List<VideoItem>,
    homeVideos: List<VideoItem>,
    searchResults: List<VideoItem>,
    relatedVideos: List<VideoItem>,
    currentPlayingVideoId: String?,
    playVideo: (String, String, String) -> Unit,
    isTabletMode: Boolean = false,
    modifier: Modifier = Modifier
) {
    val columns = if (isTabletMode) androidx.compose.foundation.lazy.grid.GridCells.Adaptive(300.dp) else androidx.compose.foundation.lazy.grid.GridCells.Fixed(1)
    
    // Reverse history outside of the scroll loop to prevent recalculation
    val reversedHistory = remember(history) { history.reversed() }
    
    androidx.compose.foundation.lazy.grid.LazyVerticalGrid(
        columns = columns,
        modifier = modifier.fillMaxWidth(),
        contentPadding = PaddingValues(bottom = 16.dp),
        horizontalArrangement = Arrangement.spacedBy(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        if (selectedTab == 1) {
            item(span = { androidx.compose.foundation.lazy.grid.GridItemSpan(maxLineSpan) }) {
                Text(
                    text = "LỊCH SỬ XEM",
                    fontSize = 12.sp,
                    fontWeight = FontWeight.Bold,
                    letterSpacing = 1.2.sp,
                    color = Color.Gray,
                    modifier = Modifier.padding(start = 12.dp, bottom = 8.dp, top = 8.dp)
                )
            }
            if (reversedHistory.isEmpty()) {
                item(span = { androidx.compose.foundation.lazy.grid.GridItemSpan(maxLineSpan) }) {
                    Box(modifier = Modifier.fillMaxWidth().padding(32.dp), contentAlignment = Alignment.Center) {
                        Text(
                            text = "Chưa có lịch sử xem",
                            color = Color.Gray,
                            fontSize = 14.sp
                        )
                    }
                }
            } else {
                items(
                    count = reversedHistory.size,
                    key = { index -> "hist_${reversedHistory[index].videoId}_$index" }
                ) { index ->
                    val video = reversedHistory[index]
                    YouTubeVideoCard(
                        title = video.title,
                        subtitle = video.channel,
                        videoId = video.videoId,
                        isTabletGrid = isTabletMode,
                        onClick = { playVideo(video.videoId, video.title, video.channel) }
                    )
                }
            }
        } else {
            if (searchQuery.isNotBlank()) {
                item(span = { androidx.compose.foundation.lazy.grid.GridItemSpan(maxLineSpan) }) {
                    Text(
                        text = "KẾT QUẢ TÌM KIẾM",
                        fontSize = 12.sp,
                        fontWeight = FontWeight.Bold,
                        letterSpacing = 1.2.sp,
                        color = Color.Gray,
                        modifier = Modifier.padding(start = 12.dp, bottom = 8.dp, top = 8.dp)
                    )
                }
                items(
                    count = searchResults.size,
                    key = { index -> "search_${searchResults[index].videoId}_$index" }
                ) { index ->
                    val video = searchResults[index]
                    YouTubeVideoCard(
                        title = video.title,
                        subtitle = video.channel,
                        videoId = video.videoId,
                        isTabletGrid = isTabletMode,
                        onClick = { playVideo(video.videoId, video.title, video.channel) }
                    )
                }
            } else if (currentPlayingVideoId != null) {
                item(span = { androidx.compose.foundation.lazy.grid.GridItemSpan(maxLineSpan) }) {
                    Text(
                        text = "VIDEO LIÊN QUAN",
                        fontSize = 12.sp,
                        fontWeight = FontWeight.Bold,
                        letterSpacing = 1.2.sp,
                        color = Color.Gray,
                        modifier = Modifier.padding(start = 12.dp, bottom = 8.dp, top = 8.dp)
                    )
                }
                if (relatedVideos.isEmpty()) {
                    item(span = { androidx.compose.foundation.lazy.grid.GridItemSpan(maxLineSpan) }) {
                        Box(modifier = Modifier.fillMaxWidth().padding(32.dp), contentAlignment = Alignment.Center) {
                            CircularProgressIndicator(color = Color.White, modifier = Modifier.size(24.dp))
                        }
                    }
                } else {
                    items(
                        count = relatedVideos.size,
                        key = { index -> "related_${relatedVideos[index].videoId}_$index" }
                    ) { index ->
                        val video = relatedVideos[index]
                        YouTubeVideoCard(
                            title = video.title,
                            subtitle = video.channel,
                            videoId = video.videoId,
                            isTabletGrid = isTabletMode,
                            onClick = { playVideo(video.videoId, video.title, video.channel) }
                        )
                    }
                }
            } else {
                item(span = { androidx.compose.foundation.lazy.grid.GridItemSpan(maxLineSpan) }) {
                    Text(
                        text = "ĐỀ XUẤT",
                        fontSize = 12.sp,
                        fontWeight = FontWeight.Bold,
                        letterSpacing = 1.2.sp,
                        color = Color.Gray,
                        modifier = Modifier.padding(start = 12.dp, bottom = 8.dp, top = 8.dp)
                    )
                }
                if (homeVideos.isEmpty()) {
                    item(span = { androidx.compose.foundation.lazy.grid.GridItemSpan(maxLineSpan) }) {
                        Box(modifier = Modifier.fillMaxWidth().padding(32.dp), contentAlignment = Alignment.Center) {
                            CircularProgressIndicator(color = Color.White, modifier = Modifier.size(24.dp))
                        }
                    }
                } else {
                    items(
                        count = homeVideos.size,
                        key = { index -> "home_${homeVideos[index].videoId}_$index" }
                    ) { index ->
                        val video = homeVideos[index]
                        YouTubeVideoCard(
                            title = video.title,
                            subtitle = video.channel,
                            videoId = video.videoId,
                            isTabletGrid = isTabletMode,
                            onClick = { playVideo(video.videoId, video.title, video.channel) }
                        )
                    }
                }
            }
        }
    }
}
"""

if insert_idx != -1:
    content = content[:insert_idx] + dashboard_code + "\n\n" + content[insert_idx:]
    
    # Let's also fix the missing imports
    imports_to_add = """
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.Replay10
import androidx.compose.material.icons.filled.Forward10
"""
    import_idx = content.find("import ")
    if import_idx != -1:
        content = content[:import_idx] + imports_to_add + "\n" + content[import_idx:]
        
    with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
        f.write(content)
        print("Restored missing components")
else:
    print("Could not find insert_idx")
