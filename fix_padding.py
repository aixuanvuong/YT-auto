with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

content = content.replace(
    ".padding(horizontal = 24.dp, bottom = 16.dp)",
    ".padding(start = 24.dp, end = 24.dp, bottom = 16.dp)"
)

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
