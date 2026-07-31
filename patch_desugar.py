import re

with open('/app/applet/gradle/libs.versions.toml', 'r') as f:
    content = f.read()

if 'desugar_jdk_libs' not in content:
    content = content.replace('[versions]', '[versions]\ndesugar_jdk_libs = "2.1.3"')
    content = content.replace('[libraries]', '[libraries]\ndesugar_jdk_libs = { group = "com.android.tools", name = "desugar_jdk_libs", version.ref = "desugar_jdk_libs" }')
    with open('/app/applet/gradle/libs.versions.toml', 'w') as f:
        f.write(content)

with open('/app/applet/app/build.gradle.kts', 'r') as f:
    content2 = f.read()

if 'isCoreLibraryDesugaringEnabled' not in content2:
    content2 = content2.replace('compileOptions {', 'compileOptions {\n    isCoreLibraryDesugaringEnabled = true')
    content2 = content2.replace('dependencies {', 'dependencies {\n  coreLibraryDesugaring(libs.desugar.jdk.libs)')
    with open('/app/applet/app/build.gradle.kts', 'w') as f:
        f.write(content2)

