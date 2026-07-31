@file:DependsOn("com.squareup.okhttp3:okhttp:4.11.0")

import okhttp3.OkHttpClient
import okhttp3.Request

fun main() {
    val client = OkHttpClient()
    val request = Request.Builder()
        .url("https://youtubei.googleapis.com/youtubei/v1/visitor_id?prettyPrint=false")
        .addHeader("User-Agent", "Mozilla/5.0")
        .build()
    val response = client.newCall(request).execute()
    println(response.code)
    println(response.body?.string()?.take(500))
}
