import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Fix duplicates in imports
def remove_duplicate_imports(text):
    lines = text.split('\n')
    seen = set()
    out = []
    for line in lines:
        if line.startswith('import '):
            if line in seen:
                continue
            seen.add(line)
        out.append(line)
    return '\n'.join(out)

content = remove_duplicate_imports(content)

# Add missing imports
missing_imports = [
    "import androidx.compose.material.icons.filled.Settings",
    "import androidx.compose.material.icons.filled.Check"
]
for mi in missing_imports:
    if mi not in content:
        content = content.replace("import androidx.compose.material.icons.filled.Search", "import androidx.compose.material.icons.filled.Search\n" + mi)

# Fix @Composable for ModernDarkDashboard
content = content.replace("@OptIn(androidx.compose.material3.ExperimentalMaterial3Api::class)\nfun ModernDarkDashboard", "@OptIn(androidx.compose.material3.ExperimentalMaterial3Api::class)\n@Composable\nfun ModernDarkDashboard")

# Fix crossAxisAlignment in YouTubeVideoCard
content = content.replace("crossAxisAlignment = Alignment.Top", "verticalAlignment = Alignment.Top")

# Fix double @Composable in InlineVideoPlayer if any
content = content.replace("@Composable\n@Composable\nfun InlineVideoPlayer", "@Composable\nfun InlineVideoPlayer")

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
