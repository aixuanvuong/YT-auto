import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

content = content.replace("package com.exampleimport androidx.compose.ui.zIndex.zIndex", "package com.example\n\nimport androidx.compose.ui.zIndex.zIndex")
content = content.replace("package com.exampleimport", "package com.example\nimport")

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
