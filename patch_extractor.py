import re

with open('/app/applet/app/src/main/java/com/example/youtube/YoutubeExtractor.kt', 'r') as f:
    content = f.read()

get_stream_new = """    fun getStream(videoId: String): String? {
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
    }"""
content = re.sub(r'    fun getStream\(videoId: String\): String\? \{.*?\} catch \(e: Exception\) \{\s*e\.printStackTrace\(\)\s*return null\s*\}\s*\}', get_stream_new, content, flags=re.DOTALL)

with open('/app/applet/app/src/main/java/com/example/youtube/YoutubeExtractor.kt', 'w') as f:
    f.write(content)
