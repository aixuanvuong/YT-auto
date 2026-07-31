import re

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

start_index = content.find("@Composable\nfun SearchHeader")
if start_index != -1:
    end_string = '                    contentDescription = "Voice Search",\n                    tint = Color.White\n                )\n            }\n            \n            Box(\n                modifier = Modifier\n                    .size(36.dp)\n                    .background(Color.White.copy(alpha = 0.1f), CircleShape)\n                    .clickable {\n                        if (searchQuery.isNotBlank()) {\n                            onSearch()\n                        }\n                    },\n                contentAlignment = Alignment.Center\n            ) {\n                if (isSearching) {\n                    CircularProgressIndicator(color = Color.White, modifier = Modifier.size(18.dp), strokeWidth = 2.dp)\n                } else {\n                    Icon(\n                        imageVector = Icons.Default.Search,\n                        contentDescription = "Search",\n                        tint = Color.White,\n                        modifier = Modifier.size(18.dp)\n                    )\n                }\n            }\n        }\n    }\n}'
    end_index = content.find(end_string, start_index)
    if end_index != -1:
        end_index += len(end_string)
        search_header_old = content[start_index:end_index]
        
        search_header_new = """@Composable
fun FloatingSearchBar(
    searchQuery: String,
    onSearchQueryChange: (String) -> Unit,
    isSearching: Boolean,
    focusManager: androidx.compose.ui.focus.FocusManager,
    voiceSearchLauncher: androidx.activity.result.ActivityResultLauncher<Intent>,
    onVoiceSearchClick: () -> Unit = {},
    onSearch: () -> Unit,
    modifier: Modifier = Modifier
) {
    Box(
        modifier = modifier
            .fillMaxWidth()
            .padding(horizontal = 24.dp)
            .height(52.dp)
            .clip(RoundedCornerShape(26.dp))
            .background(Color(0xFF1E293B).copy(alpha = 0.95f))
            .border(1.dp, Color.White.copy(alpha = 0.15f), RoundedCornerShape(26.dp)),
        contentAlignment = Alignment.Center
    ) {
        Row(
            modifier = Modifier.fillMaxSize().padding(horizontal = 8.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Icon(
                imageVector = Icons.Default.Search,
                contentDescription = "Search",
                tint = Color.Gray,
                modifier = Modifier.padding(start = 8.dp)
            )
            
            TextField(
                value = searchQuery,
                onValueChange = onSearchQueryChange,
                placeholder = { Text("Tìm kiếm YouTube...", color = Color.Gray, fontSize = 14.sp) },
                colors = TextFieldDefaults.colors(
                    focusedContainerColor = Color.Transparent,
                    unfocusedContainerColor = Color.Transparent,
                    focusedIndicatorColor = Color.Transparent,
                    unfocusedIndicatorColor = Color.Transparent,
                    focusedTextColor = Color.White,
                    unfocusedTextColor = Color.White
                ),
                modifier = Modifier.weight(1f),
                singleLine = true,
                keyboardOptions = KeyboardOptions(imeAction = ImeAction.Search),
                keyboardActions = KeyboardActions(onSearch = { focusManager.clearFocus() })
            )
            
            if (isSearching) {
                CircularProgressIndicator(
                    color = Color.White,
                    modifier = Modifier.size(20.dp),
                    strokeWidth = 2.dp
                )
                Spacer(modifier = Modifier.width(12.dp))
            } else {
                IconButton(
                    onClick = {
                        onVoiceSearchClick()
                        val intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH).apply {
                            putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
                        }
                        try {
                            voiceSearchLauncher.launch(intent)
                        } catch (e: Exception) {
                            // Ignore
                        }
                    }
                ) {
                    Icon(
                        imageVector = Icons.Default.Mic,
                        contentDescription = "Voice Search",
                        tint = Color.White
                    )
                }
            }
        }
    }
}"""
        content = content[:start_index] + search_header_new + content[end_index:]
        
        with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'w') as f:
            f.write(content)
            print("Success")
    else:
        print("Failed to find end string")
else:
    print("Failed to find SearchHeader")

