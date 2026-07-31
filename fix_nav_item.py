import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Replace fully qualified NavigationBarItem
content = content.replace("androidx.compose.material3.NavigationBarItem(", "NavigationBarItem(")

# Also add import for NavigationBarItem and NavigationBarItemDefaults if not present
if "import androidx.compose.material3.NavigationBarItem" not in content:
    content = content.replace("import androidx.compose.material3.TopAppBar", "import androidx.compose.material3.TopAppBar\nimport androidx.compose.material3.NavigationBarItem\nimport androidx.compose.material3.NavigationBarItemDefaults\nimport androidx.compose.material3.NavigationBar")
    
# Remove fully qualified NavigationBar Item Defaults
content = content.replace("androidx.compose.material3.NavigationBarItemDefaults.colors", "NavigationBarItemDefaults.colors")
content = content.replace("androidx.compose.material3.NavigationBar(", "NavigationBar(")

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
