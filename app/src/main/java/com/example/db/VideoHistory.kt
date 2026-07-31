package com.example.db

import androidx.room.Entity
import androidx.room.PrimaryKey

/**
 * Room Entity representing a video entry in the watch history database.
 *
 * @property videoId Unique YouTube video ID used as primary key.
 * @property title Title of the video.
 * @property channel Name of the channel/uploader.
 * @property timestamp Epoch timestamp (ms) when the video was last watched.
 */
@Entity(tableName = "video_history")
data class VideoHistory(
    @PrimaryKey 
    val videoId: String,
    val title: String,
    val channel: String,
    val timestamp: Long = System.currentTimeMillis()
)
