import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

old_focus = """                                    val focusRequester = remember { FocusRequester() }
                                    LaunchedEffect(Unit) {
                                        focusRequester.requestFocus()
                                    }"""
new_focus = """                                    val focusRequester = remember { FocusRequester() }
                                    val keyboardController = androidx.compose.ui.platform.LocalSoftwareKeyboardController.current
                                    LaunchedEffect(Unit) {
                                        kotlinx.coroutines.delay(100) // Small delay to ensure TextField is composed
                                        focusRequester.requestFocus()
                                        keyboardController?.show()
                                    }"""
content = content.replace(old_focus, new_focus)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
