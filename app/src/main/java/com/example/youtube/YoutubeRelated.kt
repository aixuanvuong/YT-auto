package com.example.youtube

import org.schabi.newpipe.extractor.ServiceList
import org.schabi.newpipe.extractor.stream.StreamInfoItem
import org.schabi.newpipe.extractor.NewPipe
import org.schabi.newpipe.extractor.localization.Localization

object YoutubeRelated {
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

    fun getRelated(videoId: String): List<VideoItem> {
        val list = mutableListOf<VideoItem>()
        initIfNeeded()
        try {
            val url = "https://www.youtube.com/watch?v=$videoId"
            val service = ServiceList.YouTube
            val extractor = service.getStreamExtractor(url)
            extractor.fetchPage()
            
            val relatedItems = extractor.relatedItems
            if (relatedItems != null) {
                for (item in relatedItems.items) {
                    if (item is StreamInfoItem) {
                        val itemUrl = item.url
                        val id = itemUrl.substringAfter("watch?v=").substringBefore("&")
                        list.add(
                            VideoItem(
                                item.name ?: "Unknown",
                                item.uploaderName ?: "Unknown",
                                id
                            )
                        )
                    }
                }
            }
        } catch (e: Throwable) {
            e.printStackTrace()
        }
        return list
    }
}
