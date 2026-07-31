package com.example



import androidx.compose.ui.focus.FocusRequester
import androidx.compose.ui.focus.focusRequester
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.Replay10
import androidx.compose.material.icons.filled.Forward10

import android.content.Intent

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import android.view.View
import com.google.android.exoplayer2.ui.PlayerControlView

import android.app.Activity
import android.content.pm.ActivityInfo
import android.speech.RecognizerIntent
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.material.icons.filled.Mic
import android.content.res.Configuration
import androidx.compose.ui.platform.LocalConfiguration
import androidx.core.view.WindowCompat
import androidx.core.view.WindowInsetsCompat
import androidx.core.view.WindowInsetsControllerCompat
import androidx.compose.ui.platform.LocalView
import androidx.compose.ui.window.DialogWindowProvider
import androidx.activity.compose.BackHandler
import com.google.android.exoplayer2.ui.AspectRatioFrameLayout
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.activity.viewModels
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Search
import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material.icons.filled.Person
import androidx.compose.material.icons.filled.VideoLibrary
import androidx.compose.material.icons.filled.Subscriptions
import androidx.compose.material.icons.filled.AddCircle
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.History
import androidx.compose.material.icons.filled.PlayArrow
import androidx.compose.material.icons.filled.Pause
import androidx.compose.material.icons.filled.Close
import androidx.compose.material3.Scaffold
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.NavigationBarItemDefaults
import androidx.compose.material3.NavigationRail
import androidx.compose.material3.NavigationRailItem
import androidx.compose.material3.NavigationRailItemDefaults
import androidx.compose.material3.NavigationBar
import androidx.compose.material.icons.filled.MoreVert
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.material.icons.filled.Fullscreen
import androidx.compose.material.icons.filled.FullscreenExit
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalFocusManager
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.viewinterop.AndroidView
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import coil.compose.AsyncImage
import com.example.db.AppDatabase
import com.example.db.VideoHistory
import com.example.youtube.VideoItem
import com.example.youtube.VideoResolution
import com.example.youtube.VideoPlaybackInfo
import com.example.youtube.YoutubeSearch
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import com.google.android.exoplayer2.ExoPlayer
import com.google.android.exoplayer2.MediaItem
import com.google.android.exoplayer2.ui.PlayerView
import com.example.youtube.YoutubeExtractor

class MainViewModel(application: android.app.Application) : androidx.lifecycle.AndroidViewModel(application) {
    val exoPlayer = ExoPlayer.Builder(application).build()
    
    private val _searchResults = MutableStateFlow<List<VideoItem>>(emptyList())
    val searchResults = _searchResults.asStateFlow()

    private val _isSearching = MutableStateFlow(false)
    val isSearching = _isSearching.asStateFlow()
    
    private val _homeVideos = MutableStateFlow<List<VideoItem>>(emptyList())
    val homeVideos = _homeVideos.asStateFlow()
    
    private val _isPlaying = MutableStateFlow(false)
    val isPlaying = _isPlaying.asStateFlow()

    init {
        loadHomeVideos()
        exoPlayer.addListener(object : com.google.android.exoplayer2.Player.Listener {
            override fun onIsPlayingChanged(isPlaying: Boolean) {
                _isPlaying.value = isPlaying
            }
        })
    }
    
    private fun loadHomeVideos() {
        viewModelScope.launch(Dispatchers.IO) {
            val h = _history.value
            if (h.isNotEmpty()) {
                val related = com.example.youtube.YoutubeRelated.getRelated(h.first().videoId)
                if (related.isNotEmpty()) {
                    _homeVideos.value = related
                    return@launch
                }
            }
            val defaultSearch = com.example.youtube.YoutubeSearch.search("nhạc trẻ mới nhất")
            _homeVideos.value = defaultSearch
        }
    }

    private val _history = MutableStateFlow<List<VideoItem>>(emptyList())
    val history = _history.asStateFlow()

    private val _isVideoMinimized = MutableStateFlow(false)
    val isVideoMinimized = _isVideoMinimized.asStateFlow()

    fun setVideoMinimized(minimized: Boolean) {
        _isVideoMinimized.value = minimized
    }

    private val _isFullscreen = MutableStateFlow(false)
    val isFullscreen = _isFullscreen.asStateFlow()
    
    private val _currentPlayingTitle = MutableStateFlow<String>("Đang phát video...")
    val currentPlayingTitle = _currentPlayingTitle.asStateFlow()

    private val _currentPlayingVideoId = MutableStateFlow<String?>(null)
    val currentPlayingVideoId = _currentPlayingVideoId.asStateFlow()

    private val _relatedVideos = MutableStateFlow<List<VideoItem>>(emptyList())
    val relatedVideos = _relatedVideos.asStateFlow()

    private var relatedJob: Job? = null

    private val _availableResolutions = MutableStateFlow<List<VideoResolution>>(emptyList())
    val availableResolutions = _availableResolutions.asStateFlow()
    
    private val _currentResolution = MutableStateFlow<String>("Auto")
    val currentResolution = _currentResolution.asStateFlow()
    
    private var playbackInfo: VideoPlaybackInfo? = null
    
    private var videoThread: Thread? = null

    fun playVideo(videoId: String, title: String, channel: String) {
        addHistory(VideoItem(title, channel, videoId))
        _currentPlayingTitle.value = title
        _currentPlayingVideoId.value = videoId
        _isVideoMinimized.value = false
        
        exoPlayer.stop()
        exoPlayer.clearMediaItems()
        
        videoThread?.interrupt()
        videoThread = Thread {
            val info = YoutubeExtractor.getPlaybackInfo(videoId)
            // Need to run on main thread
            android.os.Handler(android.os.Looper.getMainLooper()).post {
                if (info != null && videoThread?.isInterrupted == false) {
                    playbackInfo = info
                    _availableResolutions.value = info.resolutions
                    _currentResolution.value = "Auto"
                    val url = info.autoUrl ?: info.resolutions.firstOrNull()?.url
                    if (url != null) {
                        val mediaItem = MediaItem.fromUri(url)
                        exoPlayer.setMediaItem(mediaItem)
                        exoPlayer.prepare()
                        exoPlayer.play()
                    }
                }
            }
        }
        videoThread?.start()
        
        relatedJob?.cancel()
        relatedJob = viewModelScope.launch(Dispatchers.IO) {
            val related = com.example.youtube.YoutubeRelated.getRelated(videoId)
            _relatedVideos.value = related
        }
    }

    fun setResolution(res: String) {
        _currentResolution.value = res
        val position = exoPlayer.currentPosition
        val info = playbackInfo ?: return
        val url = if (res == "Auto") info.autoUrl else info.resolutions.find { it.resolution == res }?.url
        if (url != null) {
            val mediaItem = MediaItem.fromUri(url)
            exoPlayer.setMediaItem(mediaItem)
            exoPlayer.seekTo(position)
            exoPlayer.prepare()
            exoPlayer.play()
        }
    }

    fun setFullscreen(full: Boolean) {
        _isFullscreen.value = full
    }

    fun closeVideo() {
        exoPlayer.stop()
        exoPlayer.clearMediaItems()
        _currentPlayingVideoId.value = null
        _isFullscreen.value = false
        _isVideoMinimized.value = false
    }

    fun pauseVideo() {
        exoPlayer.pause()
    }
    
    override fun onCleared() {
        super.onCleared()
        videoThread?.interrupt()
        exoPlayer.release()
    }

    private var searchJob: Job? = null
    
    private var db: AppDatabase? = null
    
    fun initDb(database: AppDatabase) {
        db = database
        viewModelScope.launch(Dispatchers.IO) {
            database.videoHistoryDao().getHistory().collect { historyList ->
                _history.value = historyList.map { VideoItem(it.title, it.channel, it.videoId) }
            }
        }
    }

    fun search(query: String) {
        if (query.isBlank()) {
            _searchResults.value = emptyList()
            return
        }

        searchJob?.cancel()
        searchJob = viewModelScope.launch {
            _isSearching.value = true
            delay(500) // debounce
            try {
                val results = withContext(Dispatchers.IO) {
                    YoutubeSearch.search(query)
                }
                _searchResults.value = results
            } catch (e: Exception) {
                // Handle error
            } finally {
                _isSearching.value = false
            }
        }
    }
    
    fun addHistory(video: VideoItem) {
        viewModelScope.launch(Dispatchers.IO) {
            db?.videoHistoryDao()?.insert(
                VideoHistory(
                    videoId = video.videoId,
                    title = video.title,
                    channel = video.channel,
                    timestamp = System.currentTimeMillis()
                )
            )
        }
    }
}

class MainActivity : ComponentActivity() {
    private val viewModel: MainViewModel by viewModels()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        val db = androidx.room.Room.databaseBuilder(
            applicationContext,
            AppDatabase::class.java, "app-database"
        ).build()
        viewModel.initDb(db)
        
        handleIntent(intent)
        
        enableEdgeToEdge()
        setContent {
            MaterialTheme(colorScheme = darkColorScheme()) {
                ModernDarkDashboard(viewModel)
            }
        }
    }

    override fun onNewIntent(intent: Intent) {
        super.onNewIntent(intent)
        handleIntent(intent)
    }
    
    private fun handleIntent(intent: Intent) {
        if (intent.action == Intent.ACTION_SEARCH || intent.action == "com.google.android.gms.actions.SEARCH_ACTION") {
            val query = intent.getStringExtra(Intent.EXTRA_TEXT) ?: intent.getStringExtra(android.app.SearchManager.QUERY) ?: intent.getStringExtra("query")
            if (query != null) {
                viewModel.search(query)
            }
        }
    }
}

@OptIn(androidx.compose.material3.ExperimentalMaterial3Api::class)
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
                                    val focusRequester = remember { FocusRequester() }
                                    val keyboardController = androidx.compose.ui.platform.LocalSoftwareKeyboardController.current
                                    LaunchedEffect(Unit) {
                                        kotlinx.coroutines.delay(100) // Small delay to ensure TextField is composed
                                        focusRequester.requestFocus()
                                        keyboardController?.show()
                                    }
                                    TextField(
                                        value = searchQuery,
                                        onValueChange = { 
                                            searchQuery = it
                                            viewModel.search(it)
                                        },
                                        placeholder = { Text("Tìm kiếm YouTube...", color = Color.Gray) },
                                        modifier = Modifier.focusRequester(focusRequester),
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
                            if (!isFullscreen) {
                                Box(modifier = Modifier.weight(2f).fillMaxHeight()) {
                                    InlineVideoPlayer(
                                        exoPlayer = viewModel.exoPlayer,
                                        title = currentPlayingTitle,
                                        isFullscreen = false,
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
                        if (currentPlayingVideoId != null && !isVideoMinimized && !isFullscreen) {
                            InlineVideoPlayer(
                                exoPlayer = viewModel.exoPlayer,
                                title = currentPlayingTitle,
                                isFullscreen = false,
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
        
        if (isFullscreen && currentPlayingVideoId != null) {
            Box(modifier = Modifier.fillMaxSize()) {
                InlineVideoPlayer(
                    exoPlayer = viewModel.exoPlayer,
                    title = currentPlayingTitle,
                    isFullscreen = true,
                    onFullscreenToggle = { viewModel.setFullscreen(it) },
                    availableResolutions = availableResolutions,
                    currentResolution = currentResolution,
                    onResolutionSelect = { viewModel.setResolution(it) },
                    modifier = Modifier.fillMaxSize().background(Color.Black)
                )
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


@Composable
fun InlineVideoPlayer(
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
        Box(
            modifier = modifier
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
                    Icon(Icons.Default.Replay10, contentDescription = "Rewind 10s", tint = Color.White, modifier = Modifier.size(36.dp))
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
                    Icon(Icons.Default.Forward10, contentDescription = "Forward 10s", tint = Color.White, modifier = Modifier.size(36.dp))
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

@Composable
fun YouTubeVideoCard(
    title: String,
    subtitle: String,
    videoId: String,
    isTabletGrid: Boolean = false,
    onClick: () -> Unit = {}
) {
    val imageUrl = remember(videoId) { "https://img.youtube.com/vi/$videoId/mqdefault.jpg" }

    Column(
        modifier = Modifier
            .fillMaxWidth()
            .clickable { onClick() }
            .padding(bottom = 16.dp)
    ) {
        AsyncImage(
            model = imageUrl,
            contentDescription = null,
            contentScale = ContentScale.Crop,
            modifier = Modifier
                .fillMaxWidth()
                .aspectRatio(16f / 9f)
                .background(Color.DarkGray)
                .then(if (isTabletGrid) Modifier.clip(RoundedCornerShape(12.dp)) else Modifier)
        )
        
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(12.dp),
            verticalAlignment = Alignment.Top
        ) {
            Box(
                modifier = Modifier
                    .size(40.dp)
                    .clip(CircleShape)
                    .background(Color.Gray)
            ) {
                Icon(
                    imageVector = Icons.Default.Person,
                    contentDescription = null,
                    tint = Color.White,
                    modifier = Modifier.align(Alignment.Center)
                )
            }
            
            Spacer(modifier = Modifier.width(12.dp))
            
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = title,
                    fontSize = 16.sp,
                    fontWeight = FontWeight.Medium,
                    color = Color.White,
                    maxLines = 2,
                    overflow = TextOverflow.Ellipsis
                )
                Spacer(modifier = Modifier.height(4.dp))
                Text(
                    text = subtitle + " • 1M views • 1 day ago",
                    fontSize = 13.sp,
                    color = Color.Gray,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
            }
            
            IconButton(onClick = {  }) {
                Icon(
                    imageVector = Icons.Default.MoreVert,
                    contentDescription = "More",
                    tint = Color.White
                )
            }
        }
    }
}
