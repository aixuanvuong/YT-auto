import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Fix LazyColumn padding
old_lazy = """    LazyColumn(
        modifier = modifier
            .fillMaxWidth()
            .padding(horizontal = 24.dp),
        contentPadding = PaddingValues(bottom = 16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {"""

new_lazy = """    LazyColumn(
        modifier = modifier.fillMaxWidth(),
        contentPadding = PaddingValues(bottom = 16.dp),
        verticalArrangement = Arrangement.spacedBy(0.dp)
    ) {"""
content = content.replace(old_lazy, new_lazy)

# Add padding to section headers
content = content.replace('modifier = Modifier.padding(bottom = 8.dp)', 'modifier = Modifier.padding(start = 12.dp, bottom = 8.dp, top = 8.dp)')
content = content.replace('text = "Chưa có lịch sử tìm kiếm",\n                            color = Color.Gray,\n                            fontSize = 14.sp', 'text = "Chưa có lịch sử tìm kiếm",\n                            color = Color.Gray,\n                            fontSize = 14.sp,\n                            modifier = Modifier.padding(horizontal = 12.dp)')

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)

