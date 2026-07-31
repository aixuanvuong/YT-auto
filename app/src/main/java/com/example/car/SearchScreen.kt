package com.example.car

import android.graphics.Bitmap
import androidx.car.app.CarContext
import androidx.car.app.Screen
import androidx.car.app.model.Action
import androidx.car.app.model.CarIcon
import androidx.car.app.model.ItemList
import androidx.car.app.model.Row
import androidx.car.app.model.SearchTemplate
import androidx.car.app.model.Template
import androidx.core.graphics.drawable.IconCompat
import androidx.lifecycle.lifecycleScope
import androidx.room.Room
import com.example.R
import com.example.db.AppDatabase
import com.example.db.VideoHistory
import com.example.youtube.VideoItem
import com.example.youtube.YoutubeSearch
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.async
import kotlinx.coroutines.awaitAll
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

class SearchScreen(carContext: CarContext, private val initialQuery: String? = null) : Screen(carContext) {
    private var results: List<VideoItem> = emptyList()
    private var history: List<VideoHistory> = emptyList()
    private var isSearching = false
    private var currentQuery = initialQuery ?: ""
    private var searchJob: Job? = null
    private val bitmaps = mutableMapOf<String, Bitmap>()

    private val db by lazy {
        Room.databaseBuilder(
            carContext,
            AppDatabase::class.java, "app-database"
        ).build()
    }

    init {
        lifecycleScope.launch(Dispatchers.IO) {
            db.videoHistoryDao().getHistory().collect {
                history = it
                if (currentQuery.isBlank()) {
                    loadThumbnails(it.map { h -> h.videoId })
                }
            }
        }
        if (!initialQuery.isNullOrBlank()) {
            performSearch(initialQuery)
        }
    }

    private fun performSearch(query: String) {
        if (query.isBlank()) {
            results = emptyList()
            isSearching = false
            invalidate()
            return
        }
        currentQuery = query
        isSearching = true
        invalidate()
        
        searchJob?.cancel()
        searchJob = lifecycleScope.launch {
            delay(500) // Debounce
            val res = withContext(Dispatchers.IO) {
                YoutubeSearch.search(query)
            }
            results = res
            isSearching = false
            invalidate()
            loadThumbnails(res.map { it.videoId })
        }
    }

    private fun loadThumbnails(videoIds: List<String>) {
        lifecycleScope.launch {
            val jobs = videoIds.take(6).map { videoId ->
                async {
                    if (!bitmaps.containsKey(videoId)) {
                        val url = "https://img.youtube.com/vi/$videoId/default.jpg" // default.jpg is 120x90, smaller and faster than mqdefault
                        val bmp = ImageLoader.loadBitmap(url)
                        if (bmp != null) {
                            bitmaps[videoId] = bmp
                        }
                    }
                }
            }
            jobs.awaitAll()
            invalidate() // Invalidate only once after all are loaded
        }
    }

    override fun onGetTemplate(): Template {
        val listBuilder = ItemList.Builder()

        if (isSearching) {
            listBuilder.addItem(
                Row.Builder()
                    .setTitle("Đang tìm kiếm...")
                    .build()
            )
        } else if (currentQuery.isNotBlank() && results.isEmpty()) {
            listBuilder.addItem(
                Row.Builder()
                    .setTitle("Không có kết quả")
                    .addText("Hãy thử tìm kiếm một từ khóa khác")
                    .build()
            )
        } else if (currentQuery.isNotBlank()) {
            val playIcon = CarIcon.Builder(IconCompat.createWithResource(carContext, R.drawable.ic_play_car)).build()
            results.take(6).forEach { video ->
                val bmp = bitmaps[video.videoId]
                val icon = if (bmp != null) CarIcon.Builder(IconCompat.createWithBitmap(bmp)).build() else playIcon
                listBuilder.addItem(
                    Row.Builder()
                        .setTitle(video.title)
                        .addText(video.channel)
                        .setImage(icon)
                        .setOnClickListener {
                            playVideo(video)
                        }
                        .build()
                )
            }
        } else {
            // Show history
            if (history.isEmpty()) {
                listBuilder.addItem(
                    Row.Builder()
                        .setTitle("Chưa có lịch sử tìm kiếm")
                        .build()
                )
            } else {
                val playIcon = CarIcon.Builder(IconCompat.createWithResource(carContext, R.drawable.ic_play_car)).build()
                history.take(6).forEach { video ->
                    val bmp = bitmaps[video.videoId]
                    val icon = if (bmp != null) CarIcon.Builder(IconCompat.createWithBitmap(bmp)).build() else playIcon
                    listBuilder.addItem(
                        Row.Builder()
                            .setTitle(video.title)
                            .addText(video.channel)
                            .setImage(icon)
                            .setOnClickListener {
                                playVideo(VideoItem(video.title, video.channel, video.videoId))
                            }
                            .build()
                    )
                }
            }
        }

        return SearchTemplate.Builder(object : SearchTemplate.SearchCallback {
            override fun onSearchSubmitted(searchText: String) {
                performSearch(searchText)
            }
            override fun onSearchTextChanged(searchText: String) {
                performSearch(searchText)
            }
        })
            .setHeaderAction(Action.BACK)
            .setShowKeyboardByDefault(true)
            .setSearchHint("Tìm trên YouTube...")
            .setItemList(listBuilder.build())
            .apply {
                if (currentQuery.isNotBlank()) {
                    setInitialSearchText(currentQuery)
                }
            }
            .build()
    }

    private fun playVideo(video: VideoItem) {
        lifecycleScope.launch(Dispatchers.IO) {
            db.videoHistoryDao().insert(
                VideoHistory(
                    videoId = video.videoId,
                    title = video.title,
                    channel = video.channel,
                    timestamp = System.currentTimeMillis()
                )
            )
        }
        screenManager.push(PlayerScreen(carContext, video.videoId, video.title))
    }
}
