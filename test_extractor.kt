package com.example.youtube
import org.schabi.newpipe.extractor.ServiceList
import org.schabi.newpipe.extractor.NewPipe
import org.schabi.newpipe.extractor.localization.Localization
fun main() {
    NewPipe.init(OkHttpDownloader(), Localization.DEFAULT)
    val url = "https://www.youtube.com/watch?v=kJQP7kiw5Fk"
    val service = ServiceList.YouTube
    val extractor = service.getStreamExtractor(url)
    extractor.fetchPage()
    println("Video streams: " + extractor.videoStreams?.size)
    println("Video only streams: " + extractor.videoOnlyStreams?.size)
    println("Hls url: " + extractor.hlsUrl)
    println("Dash url: " + extractor.dashMpdUrl)
}
