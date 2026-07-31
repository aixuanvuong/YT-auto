import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Delete FloatingSearchBar completely since we are not using it
start_idx = content.find("fun FloatingSearchBar(")
end_idx = content.find("@Composable\nfun VideoListContent(")
if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + content[end_idx:]

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
