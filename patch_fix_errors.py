import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Fix Player.Listener
content = content.replace("androidx.media3.common.Player.Listener", "com.google.android.exoplayer2.Player.Listener")

# Fix missing @Composable on VideoListContent
content = content.replace("fun VideoListContent(", "@Composable\nfun VideoListContent(")

# It might apply multiple times if "fun VideoListContent(" appears in comments, but there are no comments like that.
# Let's make sure it doesn't duplicate @Composable
content = content.replace("@Composable\n@Composable\nfun VideoListContent(", "@Composable\nfun VideoListContent(")

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
