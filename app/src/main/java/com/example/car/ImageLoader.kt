package com.example.car

import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.util.LruCache
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.net.URL

object ImageLoader {
    private val memoryCache: LruCache<String, Bitmap>

    init {
        val maxMemory = (Runtime.getRuntime().maxMemory() / 1024).toInt()
        val cacheSize = maxMemory / 8
        memoryCache = object : LruCache<String, Bitmap>(cacheSize) {
            override fun sizeOf(key: String, bitmap: Bitmap): Int {
                return bitmap.byteCount / 1024
            }
        }
    }

    suspend fun loadBitmap(url: String): Bitmap? = withContext(Dispatchers.IO) {
        memoryCache.get(url)?.let { return@withContext it }
        try {
            val stream = URL(url).openStream()
            val bitmap = BitmapFactory.decodeStream(stream)
            if (bitmap != null) {
                memoryCache.put(url, bitmap)
            }
            bitmap
        } catch (e: Exception) {
            null
        }
    }
}
