import re

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# I will replace the entire ModernDarkDashboard function.
new_dashboard = """
@Composable
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
                .padding(horizontal = 24.dp, vertical = 16.dp)
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
                
                Box(
                    modifier = Modifier
                        .size(36.dp)
                        .background(Color.White.copy(alpha = 0.1f), CircleShape),
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
                    .padding(horizontal = 24.dp, bottom = 16.dp)
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
}
"""

dashboard_pattern = re.compile(r'@Composable\s+fun ModernDarkDashboard.*?@Composable\s+fun GlassVideoCard', re.DOTALL)
content = dashboard_pattern.sub(new_dashboard + "\n@Composable\nfun GlassVideoCard", content)

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
