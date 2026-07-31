import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

start_idx = content.find("fun VideoListContent(")
end_idx = content.find("@Composable\nfun YouTubeVideoCard(")

if start_idx != -1 and end_idx != -1:
    new_content = """fun VideoListContent(
    selectedTab: Int,
    searchQuery: String,
    history: List<VideoItem>,
    homeVideos: List<VideoItem>,
    searchResults: List<VideoItem>,
    relatedVideos: List<VideoItem>,
    currentPlayingVideoId: String?,
    playVideo: (String, String, String) -> Unit,
    modifier: Modifier = Modifier
) {
    LazyColumn(
        modifier = modifier.fillMaxWidth(),
        contentPadding = PaddingValues(bottom = 16.dp),
        verticalArrangement = Arrangement.spacedBy(0.dp)
    ) {
        if (selectedTab == 1) {
            item {
                Text(
                    text = "LỊCH SỬ XEM",
                    fontSize = 12.sp,
                    fontWeight = FontWeight.Bold,
                    letterSpacing = 1.2.sp,
                    color = Color.Gray,
                    modifier = Modifier.padding(start = 12.dp, bottom = 8.dp, top = 8.dp)
                )
            }
            if (history.isEmpty()) {
                item {
                    Box(modifier = Modifier.fillMaxWidth().padding(32.dp), contentAlignment = Alignment.Center) {
                        Text(
                            text = "Chưa có lịch sử xem",
                            color = Color.Gray,
                            fontSize = 14.sp
                        )
                    }
                }
            } else {
                items(history.reversed()) { video ->
                    YouTubeVideoCard(
                        title = video.title,
                        subtitle = video.channel,
                        videoId = video.videoId,
                        onClick = { playVideo(video.videoId, video.title, video.channel) }
                    )
                }
            }
        } else {
            if (searchQuery.isNotBlank()) {
                item {
                    Text(
                        text = "KẾT QUẢ TÌM KIẾM",
                        fontSize = 12.sp,
                        fontWeight = FontWeight.Bold,
                        letterSpacing = 1.2.sp,
                        color = Color.Gray,
                        modifier = Modifier.padding(start = 12.dp, bottom = 8.dp, top = 8.dp)
                    )
                }
                items(searchResults) { video ->
                    YouTubeVideoCard(
                        title = video.title,
                        subtitle = video.channel,
                        videoId = video.videoId,
                        onClick = { playVideo(video.videoId, video.title, video.channel) }
                    )
                }
            } else if (currentPlayingVideoId != null) {
                item {
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
                    item {
                        Box(modifier = Modifier.fillMaxWidth().padding(32.dp), contentAlignment = Alignment.Center) {
                            CircularProgressIndicator(color = Color.White, modifier = Modifier.size(24.dp))
                        }
                    }
                } else {
                    items(relatedVideos) { video ->
                        YouTubeVideoCard(
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
                        text = "ĐỀ XUẤT",
                        fontSize = 12.sp,
                        fontWeight = FontWeight.Bold,
                        letterSpacing = 1.2.sp,
                        color = Color.Gray,
                        modifier = Modifier.padding(start = 12.dp, bottom = 8.dp, top = 8.dp)
                    )
                }
                if (homeVideos.isEmpty()) {
                    item {
                        Box(modifier = Modifier.fillMaxWidth().padding(32.dp), contentAlignment = Alignment.Center) {
                            CircularProgressIndicator(color = Color.White, modifier = Modifier.size(24.dp))
                        }
                    }
                } else {
                    items(homeVideos) { video ->
                        YouTubeVideoCard(
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
}
"""
    content = content[:start_idx] + new_content + content[end_idx:]
    with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
        f.write(content)

