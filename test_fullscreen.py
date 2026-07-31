import re

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# 1. Remove the isLandscape branching from ModernDarkDashboard.
# We will just replace ModernDarkDashboard completely.
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

    Box(
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
                    videoId = currentPlayingVideoId!!,
                    viewModel = viewModel,
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
                playVideo = ::playVideo
            )
        }
    }
}"""

content = re.sub(r'@Composable\s+fun ModernDarkDashboard.*?@Composable\s+fun SearchHeader', new_dashboard + "\n\n@Composable\nfun SearchHeader", content, flags=re.DOTALL)

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
