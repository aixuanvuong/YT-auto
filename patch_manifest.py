import re

with open('/app/applet/app/src/main/AndroidManifest.xml', 'r') as f:
    content = f.read()

content = content.replace(
    'android:theme="@style/Theme.MyApplication">',
    'android:theme="@style/Theme.MyApplication"\n            android:configChanges="orientation|screenSize|screenLayout|keyboardHidden">'
)

with open('/app/applet/app/src/main/AndroidManifest.xml', 'w') as f:
    f.write(content)
