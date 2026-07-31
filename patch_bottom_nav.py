import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Add bottomBar to Scaffold
scaffold_old = """        containerColor = Color(0xFF0F0F0F),
        modifier = Modifier.fillMaxSize()
    ) { paddingValues ->"""

scaffold_new = """        bottomBar = {
            if (!isFullscreen) {
                androidx.compose.material3.NavigationBar(
                    containerColor = Color(0xFF0F0F0F),
                    contentColor = Color.White
                ) {
                    androidx.compose.material3.NavigationBarItem(
                        selected = true,
                        onClick = { },
                        icon = { Icon(androidx.compose.material.icons.Icons.Default.Home, contentDescription = "Home") },
                        label = { Text("Home") },
                        colors = androidx.compose.material3.NavigationBarItemDefaults.colors(
                            selectedIconColor = Color.White,
                            unselectedIconColor = Color.Gray,
                            selectedTextColor = Color.White,
                            unselectedTextColor = Color.Gray,
                            indicatorColor = Color.Transparent
                        )
                    )
                    androidx.compose.material3.NavigationBarItem(
                        selected = false,
                        onClick = { },
                        icon = { Icon(androidx.compose.material.icons.Icons.Default.PlayArrow, contentDescription = "Shorts") },
                        label = { Text("Shorts") },
                        colors = androidx.compose.material3.NavigationBarItemDefaults.colors(
                            selectedIconColor = Color.White,
                            unselectedIconColor = Color.Gray,
                            selectedTextColor = Color.White,
                            unselectedTextColor = Color.Gray,
                            indicatorColor = Color.Transparent
                        )
                    )
                    androidx.compose.material3.NavigationBarItem(
                        selected = false,
                        onClick = { },
                        icon = { Icon(androidx.compose.material.icons.Icons.Default.AddCircle, contentDescription = "Add") },
                        label = { },
                        colors = androidx.compose.material3.NavigationBarItemDefaults.colors(
                            selectedIconColor = Color.White,
                            unselectedIconColor = Color.Gray,
                            selectedTextColor = Color.White,
                            unselectedTextColor = Color.Gray,
                            indicatorColor = Color.Transparent
                        )
                    )
                    androidx.compose.material3.NavigationBarItem(
                        selected = false,
                        onClick = { },
                        icon = { Icon(androidx.compose.material.icons.Icons.Default.Subscriptions, contentDescription = "Subscriptions") },
                        label = { Text("Subscriptions", maxLines = 1, overflow = TextOverflow.Ellipsis) },
                        colors = androidx.compose.material3.NavigationBarItemDefaults.colors(
                            selectedIconColor = Color.White,
                            unselectedIconColor = Color.Gray,
                            selectedTextColor = Color.White,
                            unselectedTextColor = Color.Gray,
                            indicatorColor = Color.Transparent
                        )
                    )
                    androidx.compose.material3.NavigationBarItem(
                        selected = false,
                        onClick = { },
                        icon = { Icon(androidx.compose.material.icons.Icons.Default.VideoLibrary, contentDescription = "Library") },
                        label = { Text("Library") },
                        colors = androidx.compose.material3.NavigationBarItemDefaults.colors(
                            selectedIconColor = Color.White,
                            unselectedIconColor = Color.Gray,
                            selectedTextColor = Color.White,
                            unselectedTextColor = Color.Gray,
                            indicatorColor = Color.Transparent
                        )
                    )
                }
            }
        },
        containerColor = Color(0xFF0F0F0F),
        modifier = Modifier.fillMaxSize()
    ) { paddingValues ->"""
content = content.replace(scaffold_old, scaffold_new)

missing = [
    "import androidx.compose.material.icons.filled.Home",
    "import androidx.compose.material.icons.filled.AddCircle",
    "import androidx.compose.material.icons.filled.Subscriptions",
    "import androidx.compose.material.icons.filled.VideoLibrary"
]

for mi in missing:
    if mi not in content:
        content = content.replace("import androidx.compose.material.icons.filled.Person", "import androidx.compose.material.icons.filled.Person\n" + mi)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
