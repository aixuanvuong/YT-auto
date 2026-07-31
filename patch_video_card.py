import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Replace YouTubeVideoCard
old_card = """@Composable
fun YouTubeVideoCard(
    title: String,
    subtitle: String,
    videoId: String,
    onClick: () -> Unit = {}
) {"""

new_card = """@Composable
fun YouTubeVideoCard(
    title: String,
    subtitle: String,
    videoId: String,
    isTabletGrid: Boolean = false,
    onClick: () -> Unit = {}
) {"""
content = content.replace(old_card, new_card)

# Let's add clipping if isTabletGrid
old_image = """        AsyncImage(
            model = "https://img.youtube.com/vi/$videoId/hqdefault.jpg",
            contentDescription = null,
            contentScale = ContentScale.Crop,
            modifier = Modifier
                .fillMaxWidth()
                .aspectRatio(16f / 9f)
                .background(Color.DarkGray)
        )"""

new_image = """        AsyncImage(
            model = "https://img.youtube.com/vi/$videoId/hqdefault.jpg",
            contentDescription = null,
            contentScale = ContentScale.Crop,
            modifier = Modifier
                .fillMaxWidth()
                .aspectRatio(16f / 9f)
                .background(Color.DarkGray)
                .then(if (isTabletGrid) Modifier.clip(RoundedCornerShape(12.dp)) else Modifier)
        )"""
content = content.replace(old_image, new_image)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
    print("Patched YouTubeVideoCard")
