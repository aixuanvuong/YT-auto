import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

content = content.replace("@OptIn(androidx.compose.material3.ExperimentalMaterial3Api::class)\n@OptIn(androidx.compose.material3.ExperimentalMaterial3Api::class)", "@OptIn(androidx.compose.material3.ExperimentalMaterial3Api::class)")

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
