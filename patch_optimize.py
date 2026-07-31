import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Replace VideoListContent to add keys and avoid reversing history inside items block
list_content_start = content.find("@Composable\nfun VideoListContent(")
list_content_end = content.find("@Composable\nfun YouTubeVideoCard(")

if list_content_start != -1 and list_content_end != -1:
    new_list_content = """@Composable
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
    content = content[:list_content_start] + new_list_content + content[list_content_end:]
    
    with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
        f.write(content)
        print("Patched VideoListContent successfully.")
