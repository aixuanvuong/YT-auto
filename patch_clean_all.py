import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Replace any sequence of multiple @Composable annotations with a single one
content = re.sub(r'(@Composable\s*)+', '@Composable\n', content)
content = content.replace("@OptIn(androidx.compose.material3.ExperimentalMaterial3Api::class)\n@Composable\n@Composable\nfun", "@OptIn(androidx.compose.material3.ExperimentalMaterial3Api::class)\n@Composable\nfun")
content = content.replace("@OptIn(androidx.compose.material3.ExperimentalMaterial3Api::class)\n@Composable\nfun", "@OptIn(androidx.compose.material3.ExperimentalMaterial3Api::class)\n@Composable\nfun")

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
