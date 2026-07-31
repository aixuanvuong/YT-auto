import re

with open('app/src/main/java/com/example/youtube/YoutubeExtractor.kt', 'r') as f:
    content = f.read()

new_struct = """data class VideoResolution(
    val resolution: String,
    val url: String
)

data class VideoPlaybackInfo(
    val autoUrl: String?, // Could be DASH or HLS or best progressive
    val resolutions: List<VideoResolution>
)
"""

if "data class VideoResolution" not in content:
    content = content.replace("object YoutubeExtractor", new_struct + "\nobject YoutubeExtractor")

new_func = """    fun getPlaybackInfo(videoId: String): VideoPlaybackInfo? {
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
            
            // Try to find dash or hls for auto, else pick 720p or 480p or 360p
            var autoUrl = extractor.dashMpdUrl
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
    }"""
    
content = content.replace("    fun getStream", new_func + "\n\n    fun getStream")

with open('app/src/main/java/com/example/youtube/YoutubeExtractor.kt', 'w') as f:
    f.write(content)

