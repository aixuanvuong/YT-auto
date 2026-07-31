package com.example.youtube
import org.schabi.newpipe.extractor.ServiceList
import org.schabi.newpipe.extractor.stream.StreamInfoItem
import org.schabi.newpipe.extractor.NewPipe
import org.schabi.newpipe.extractor.localization.Localization
fun main() {
    NewPipe.init(OkHttpDownloader(), Localization.DEFAULT)
    val url = "https://www.youtube.com/watch?v=kJQP7kiw5Fk"
    val service = ServiceList.YouTube
    val extractor = service.getStreamExtractor(url)
    extractor.fetchPage()
    val related = extractor.relatedItems
    if (related != null) {
        for (item in related.items) {
            if (item is StreamInfoItem) {
                println(item.name)
            }
        }
    }
}
