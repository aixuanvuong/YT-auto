import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

old_back = """    if (currentPlayingVideoId != null && !isFullscreen) {
        BackHandler {
            viewModel.closeVideo()
        }
    }"""

new_back = """    if (isSearchExpanded) {
        BackHandler {
            isSearchExpanded = false
            searchQuery = ""
            viewModel.search("")
        }
    } else if (currentPlayingVideoId != null && !isFullscreen) {
        BackHandler {
            viewModel.closeVideo()
        }
    }"""

content = content.replace(old_back, new_back)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
