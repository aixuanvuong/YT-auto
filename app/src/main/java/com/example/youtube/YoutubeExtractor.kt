package com.example.youtube

import org.schabi.newpipe.extractor.ServiceList
import org.schabi.newpipe.extractor.NewPipe
import org.schabi.newpipe.extractor.downloader.Downloader
import org.schabi.newpipe.extractor.downloader.Request
import org.schabi.newpipe.extractor.downloader.Response
import okhttp3.OkHttpClient
import okhttp3.RequestBody.Companion.toRequestBody
import java.util.concurrent.TimeUnit
import org.schabi.newpipe.extractor.localization.Localization
import okhttp3.MediaType.Companion.toMediaTypeOrNull

class OkHttpDownloader : Downloader() {
    private val client: OkHttpClient = OkHttpClient.Builder()
        .readTimeout(30, TimeUnit.SECONDS)
        .connectTimeout(30, TimeUnit.SECONDS)
        .build()

    override fun execute(request: Request): Response {
        val httpMethod = request.httpMethod()
        val url = request.url()
        val headers = request.headers()
        val dataToSend = request.dataToSend()

        val requestBuilder = okhttp3.Request.Builder()
            .url(url)
            .addHeader("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)")

        headers.forEach { (key, list) ->
            if (list.isNotEmpty()) {
                requestBuilder.header(key, list[0])
            }
        }

        if (httpMethod == "POST") {
            val bodyData = dataToSend ?: ByteArray(0)
            val contentType = headers["Content-Type"]?.firstOrNull() ?: "application/json; charset=utf-8"
            requestBuilder.post(bodyData.toRequestBody(contentType.toMediaTypeOrNull()))
        } else if (httpMethod == "GET") {
            requestBuilder.get()
        } else {
            requestBuilder.method(httpMethod, dataToSend?.toRequestBody())
        }

        val response = client.newCall(requestBuilder.build()).execute()
        
        val outHeaders = HashMap<String, List<String>>()
        response.headers.names().forEach { name ->
            outHeaders[name] = response.headers.values(name)
        }
        
        val bodyStr = response.body?.string() ?: ""
        
        return Response(response.code, response.message, outHeaders, bodyStr, response.request.url.toString())
    }
}

data class VideoResolution(
    val resolution: String,
    val url: String
)

data class VideoPlaybackInfo(
    val autoUrl: String?, // Could be DASH or HLS or best progressive
    val resolutions: List<VideoResolution>
)

object YoutubeExtractor {
    private var initialized = false

    private fun initIfNeeded() {
        if (!initialized) {
            NewPipe.init(OkHttpDownloader(), Localization.DEFAULT)
            initialized = true
        }
    }

    fun getPlaybackInfo(videoId: String): VideoPlaybackInfo? {
        initIfNeeded()
        try {
            val url = "https://www.youtube.com/watch?v=$videoId"
            val service = ServiceList.YouTube
            val extractor = service.getStreamExtractor(url)
            extractor.fetchPage()
            
            val streams = extractor.videoStreams
            if (streams.isNullOrEmpty()) return null
            
            val resolutions = streams.mapNotNull { stream ->
                stream.resolution?.let { res ->
                    VideoResolution(res, stream.content)
                }
            }.distinctBy { it.resolution }.sortedByDescending { it.resolution.replace("p", "").toIntOrNull() ?: 0 }
            
            var autoUrl: String? = extractor.dashMpdUrl
            if (autoUrl.isNullOrBlank()) {
                autoUrl = extractor.hlsUrl
            }
            if (autoUrl.isNullOrBlank()) {
                val preferredResolutions = listOf("720p", "480p", "360p", "240p", "144p")
                for (res in preferredResolutions) {
                    val stream = streams.firstOrNull { it.resolution == res }
                    if (stream != null) {
                        autoUrl = stream.content
                        break
                    }
                }
            }
            if (autoUrl.isNullOrBlank()) {
                 autoUrl = streams.firstOrNull()?.content
            }
            
            return VideoPlaybackInfo(autoUrl, resolutions)
        } catch (e: Exception) {
            e.printStackTrace()
            return null
        }
    }

    fun getStream(videoId: String): String? {
        initIfNeeded()
        try {
            val url = "https://www.youtube.com/watch?v=$videoId"
            val service = ServiceList.YouTube
            val extractor = service.getStreamExtractor(url)
            extractor.fetchPage()
            
            val streams = extractor.videoStreams
            if (streams.isNullOrEmpty()) return null
            
            // For low-end devices, prefer 360p or 480p or 720p to avoid decoder crash/lag
            val preferredResolutions = listOf("360p", "480p", "720p")
            for (res in preferredResolutions) {
                val stream = streams.firstOrNull { it.resolution == res }
                if (stream != null) return stream.content
            }
            
            // Fallback to lowest resolution if preferred ones are not found, or any if not available
            return streams.minByOrNull { it.resolution.replace("p", "").toIntOrNull() ?: 1000 }?.content ?: streams.firstOrNull()?.content
        } catch (e: Exception) {
            e.printStackTrace()
            return null
        }
    }
}
