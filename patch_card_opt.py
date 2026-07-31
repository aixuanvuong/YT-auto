import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

old_card = """@Composable
fun YouTubeVideoCard(
    title: String,
    subtitle: String,
    videoId: String,
    isTabletGrid: Boolean = false,
    onClick: () -> Unit = {}
) {"""

new_card = """@Composable
fun YouTubeVideoCard(
    title: String,
    subtitle: String,
    videoId: String,
    isTabletGrid: Boolean = false,
    onClick: () -> Unit = {}
) {
    val imageUrl = remember(videoId) { "https://img.youtube.com/vi/$videoId/hqdefault.jpg" }
"""
content = content.replace(old_card, new_card)

old_image_model = """        AsyncImage(
            model = "https://img.youtube.com/vi/$videoId/hqdefault.jpg",
            contentDescription = null,"""
            
new_image_model = """        AsyncImage(
            model = imageUrl,
            contentDescription = null,"""
content = content.replace(old_image_model, new_image_model)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
