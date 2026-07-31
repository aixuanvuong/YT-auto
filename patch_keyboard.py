import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Add imports
imports_to_add = """
import androidx.compose.ui.focus.FocusRequester
import androidx.compose.ui.focus.focusRequester
"""
import_idx = content.find("import ")
if import_idx != -1:
    content = content[:import_idx] + imports_to_add.strip() + "\n" + content[import_idx:]

# Modify TextField in ModernDarkDashboard
old_code = """                                if (isSearchExpanded) {
                                    TextField(
                                        value = searchQuery,
                                        onValueChange = { 
                                            searchQuery = it
                                            viewModel.search(it)
                                        },
                                        placeholder = { Text("Tìm kiếm YouTube...", color = Color.Gray) },"""

new_code = """                                if (isSearchExpanded) {
                                    val focusRequester = remember { FocusRequester() }
                                    LaunchedEffect(Unit) {
                                        focusRequester.requestFocus()
                                    }
                                    TextField(
                                        value = searchQuery,
                                        onValueChange = { 
                                            searchQuery = it
                                            viewModel.search(it)
                                        },
                                        placeholder = { Text("Tìm kiếm YouTube...", color = Color.Gray) },
                                        modifier = Modifier.focusRequester(focusRequester),"""

content = content.replace(old_code, new_code)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
