import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

content = content.replace('androidx.compose.material.icons.Icons.Default.Replay10', 'Icons.Default.Replay10')
content = content.replace('androidx.compose.material.icons.Icons.Default.Forward10', 'Icons.Default.Forward10')

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
