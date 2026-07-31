import re

with open('app/src/main/java/com/example/youtube/YoutubeExtractor.kt', 'r') as f:
    content = f.read()

# We need to clean up YoutubeExtractor object to only have one getPlaybackInfo and one getStream (or just one function)
content = re.sub(r'    fun getPlaybackInfo.*?    fun getStream', '    fun getStream', content, flags=re.DOTALL)
content = re.sub(r'    fun getPlaybackInfo.*?    fun getStream', '    fun getStream', content, flags=re.DOTALL)

# Re-apply correctly
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
    }"""
content = content.replace("    fun getStream", new_func + "\n\n    fun getStream")

with open('app/src/main/java/com/example/youtube/YoutubeExtractor.kt', 'w') as f:
    f.write(content)

