import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Make sure isMinimized defaults properly on VideoPlayerOverlay
if "fun VideoPlayerOverlay(" in content:
    content = content.replace("fun VideoPlayerOverlay(", "@Composable\nfun VideoPlayerOverlay(")

# Wait, VideoPlayerOverlay doesn't have isMinimized. The patch I applied before handled it:
# if (!isMinimized) { VideoPlayerOverlay(...) }

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
