package com.example.youtube

import org.schabi.newpipe.extractor.ServiceList
import org.schabi.newpipe.extractor.stream.StreamInfoItem
import org.schabi.newpipe.extractor.search.SearchExtractor
import org.schabi.newpipe.extractor.NewPipe
import org.schabi.newpipe.extractor.localization.Localization

object YoutubeSearch {

    private var initialized = false

    private fun initIfNeeded() {
        if (!initialized) {
            try {
                NewPipe.init(OkHttpDownloader(), Localization.DEFAULT)
                initialized = true
            } catch (e: Throwable) {
                e.printStackTrace()
            }
        }
    }

    fun search(query: String): List<VideoItem> {
        val list = mutableListOf<VideoItem>()
        initIfNeeded()
        try {
            val service = ServiceList.YouTube
            val searchExtractor = service.getSearchExtractor(query)
            searchExtractor.fetchPage()
            val initialPage = searchExtractor.initialPage
            val items = initialPage.items
            
            for (item in items) {
                if (item is StreamInfoItem) {
                    val url = item.url
                    val videoId = url.substringAfter("watch?v=").substringBefore("&")
                    list.add(
                        VideoItem(
                            item.name ?: "Unknown",
                            item.uploaderName ?: "Unknown",
                            videoId
                        )
                    )
                }
            }
        } catch (e: Throwable) {
            e.printStackTrace()
        }
        return list
    }
}
