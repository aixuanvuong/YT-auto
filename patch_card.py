import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Replace GlassVideoCard with YouTubeVideoCard
old_card_start = content.find("fun GlassVideoCard(")
old_card_end = content.find("fun ", old_card_start + 10)
if old_card_end == -1:
    old_card_end = len(content)

new_card = """fun YouTubeVideoCard(
    title: String,
    subtitle: String,
    videoId: String,
    onClick: () -> Unit = {}
) {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .clickable { onClick() }
            .padding(bottom = 16.dp)
    ) {
        AsyncImage(
            model = "https://img.youtube.com/vi/$videoId/hqdefault.jpg",
            contentDescription = null,
            contentScale = ContentScale.Crop,
            modifier = Modifier
                .fillMaxWidth()
                .aspectRatio(16f / 9f)
                .background(Color.DarkGray)
        )
        
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(12.dp),
            crossAxisAlignment = Alignment.Top
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
"""

content = content[:old_card_start] + new_card + content[old_card_end:]

content = content.replace("GlassVideoCard(", "YouTubeVideoCard(")
if "import androidx.compose.material.icons.filled.Person" not in content:
    content = content.replace("import androidx.compose.material.icons.filled.Search", "import androidx.compose.material.icons.filled.Search\nimport androidx.compose.material.icons.filled.Person\nimport androidx.compose.material.icons.filled.MoreVert\nimport androidx.compose.ui.layout.ContentScale\nimport androidx.compose.ui.text.style.TextOverflow")

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)

