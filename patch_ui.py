import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

dashboard_old = """    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(bgGradient)
            .windowInsetsPadding(WindowInsets.systemBars)
    ) {
        Column(modifier = Modifier.fillMaxSize()) {
            SearchHeader(
                searchQuery = searchQuery,
                onSearchQueryChange = { 
                    searchQuery = it 
                    viewModel.search(it)
                },
                isSearching = isSearching,
                focusManager = focusManager,
                voiceSearchLauncher = voiceSearchLauncher,
                onVoiceSearchClick = { viewModel.pauseVideo() },
                onSearch = { viewModel.search(searchQuery) }
            )
            
            if (currentPlayingVideoId != null) {
                InlineVideoPlayer(
                    exoPlayer = viewModel.exoPlayer,
                    isFullscreen = isFullscreen,
                    onFullscreenToggle = { viewModel.setFullscreen(it) },
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(start = 24.dp, end = 24.dp, bottom = 16.dp)
                        .aspectRatio(16f / 9f)
                        .clip(RoundedCornerShape(12.dp))
                        .background(Color.Black)
                )
            }
            
            VideoListContent(
                searchQuery = searchQuery,
                history = history,
                searchResults = searchResults,
                relatedVideos = relatedVideos,
                currentPlayingVideoId = currentPlayingVideoId,
                playVideo = { videoId, title, channel -> viewModel.playVideo(videoId, title, channel) }
            )
        }
    }"""

dashboard_new = """    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(bgGradient)
            .windowInsetsPadding(WindowInsets.systemBars)
    ) {
        Column(modifier = Modifier.fillMaxSize()) {
            Spacer(modifier = Modifier.height(16.dp))
            if (currentPlayingVideoId != null) {
                InlineVideoPlayer(
                    exoPlayer = viewModel.exoPlayer,
                    isFullscreen = isFullscreen,
                    onFullscreenToggle = { viewModel.setFullscreen(it) },
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(start = 24.dp, end = 24.dp, bottom = 16.dp)
                        .aspectRatio(16f / 9f)
                        .clip(RoundedCornerShape(12.dp))
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
                modifier = Modifier.weight(1f) // Ensure it takes available space
            )
            Spacer(modifier = Modifier.height(80.dp)) // Leave space for FloatingSearchBar
        }
        
        FloatingSearchBar(
            searchQuery = searchQuery,
            onSearchQueryChange = { 
                searchQuery = it 
                viewModel.search(it)
            },
            isSearching = isSearching,
            focusManager = focusManager,
            voiceSearchLauncher = voiceSearchLauncher,
            onVoiceSearchClick = { viewModel.pauseVideo() },
            onSearch = { viewModel.search(searchQuery) },
            modifier = Modifier.align(Alignment.BottomCenter).padding(bottom = 16.dp)
        )
    }"""
content = content.replace(dashboard_old, dashboard_new)

search_header_old = """@Composable
fun SearchHeader(
    searchQuery: String,
    onSearchQueryChange: (String) -> Unit,
    isSearching: Boolean,
    focusManager: androidx.compose.ui.focus.FocusManager,
    voiceSearchLauncher: androidx.activity.result.ActivityResultLauncher<Intent>,
    onVoiceSearchClick: () -> Unit = {},
    onSearch: () -> Unit
) {
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
                onValueChange = onSearchQueryChange,
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
                    onVoiceSearchClick() // Pause the video
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
        }
    }
}"""

search_header_new = """@Composable
fun FloatingSearchBar(
    searchQuery: String,
    onSearchQueryChange: (String) -> Unit,
    isSearching: Boolean,
    focusManager: androidx.compose.ui.focus.FocusManager,
    voiceSearchLauncher: androidx.activity.result.ActivityResultLauncher<Intent>,
    onVoiceSearchClick: () -> Unit = {},
    onSearch: () -> Unit,
    modifier: Modifier = Modifier
) {
    Box(
        modifier = modifier
            .fillMaxWidth()
            .padding(horizontal = 24.dp)
            .height(52.dp)
            .clip(RoundedCornerShape(26.dp))
            .background(Color(0xFF1E293B).copy(alpha = 0.95f))
            .border(1.dp, Color.White.copy(alpha = 0.15f), RoundedCornerShape(26.dp)),
        contentAlignment = Alignment.Center
    ) {
        Row(
            modifier = Modifier.fillMaxSize().padding(horizontal = 8.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Icon(
                imageVector = Icons.Default.Search,
                contentDescription = "Search",
                tint = Color.Gray,
                modifier = Modifier.padding(start = 8.dp)
            )
            
            TextField(
                value = searchQuery,
                onValueChange = onSearchQueryChange,
                placeholder = { Text("Tìm kiếm YouTube...", color = Color.Gray, fontSize = 14.sp) },
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
            
            if (isSearching) {
                CircularProgressIndicator(
                    color = Color.White,
                    modifier = Modifier.size(20.dp),
                    strokeWidth = 2.dp
                )
                Spacer(modifier = Modifier.width(12.dp))
            } else {
                IconButton(
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
                ) {
                    Icon(
                        imageVector = Icons.Default.Mic,
                        contentDescription = "Voice Search",
                        tint = Color.White
                    )
                }
            }
        }
    }
}"""
content = content.replace(search_header_old, search_header_new)

video_content_old = """@Composable
fun VideoListContent(
    searchQuery: String,
    history: List<VideoItem>,
    searchResults: List<VideoItem>,
    relatedVideos: List<VideoItem>,
    currentPlayingVideoId: String?,
    playVideo: (String, String, String) -> Unit
) {
    LazyColumn(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 24.dp),
        contentPadding = PaddingValues(bottom = 16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {"""

video_content_new = """@Composable
fun VideoListContent(
    searchQuery: String,
    history: List<VideoItem>,
    searchResults: List<VideoItem>,
    relatedVideos: List<VideoItem>,
    currentPlayingVideoId: String?,
    playVideo: (String, String, String) -> Unit,
    modifier: Modifier = Modifier
) {
    LazyColumn(
        modifier = modifier
            .fillMaxWidth()
            .padding(horizontal = 24.dp),
        contentPadding = PaddingValues(bottom = 16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {"""

content = content.replace(video_content_old, video_content_new)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)

