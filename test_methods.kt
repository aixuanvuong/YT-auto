import com.google.android.exoplayer2.ui.PlayerView
fun getMethods() {
    val clazz = PlayerView::class.java
    for (m in clazz.methods) {
        if (m.name.toLowerCase().contains("full")) {
            println(m.name)
        }
    }
}
fun main() {
    getMethods()
}
