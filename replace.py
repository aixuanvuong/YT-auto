import re

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# We need to add the imports for Fullscreen and FullscreenExit
content = content.replace(
    "import androidx.compose.material.icons.filled.Search",
    "import androidx.compose.material.icons.filled.Search\nimport androidx.compose.material.icons.filled.Fullscreen\nimport androidx.compose.material.icons.filled.FullscreenExit"
)

# Extract the new InlineVideoPlayer from patch_inline.kt
with open('patch_inline.kt', 'r') as f:
    patch_content = f.read()
    
# Extract from @Composable fun InlineVideoPlayer to the end of file (since it's the last thing in patch_inline.kt)
new_player = re.search(r'(@Composable\s+fun InlineVideoPlayer.*)', patch_content, re.DOTALL).group(1)

# Replace the old InlineVideoPlayer in content
# It starts at @Composable\nfun InlineVideoPlayer and ends before @Composable\nfun ModernDarkDashboard
old_player_pattern = re.compile(r'@Composable\s+fun InlineVideoPlayer.*?@Composable\s+fun ModernDarkDashboard', re.DOTALL)
content = old_player_pattern.sub(new_player + "\n\n@Composable\nfun ModernDarkDashboard", content)

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
