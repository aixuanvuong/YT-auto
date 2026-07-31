import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

content = content.replace("@Composable\n@Composable\n@Composable\nfun VideoPlayerOverlay(", "@Composable\nfun VideoPlayerOverlay(")
content = content.replace("@Composable\n@Composable\nfun VideoPlayerOverlay(", "@Composable\nfun VideoPlayerOverlay(")

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
