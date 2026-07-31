package com.example.db

import androidx.room.Entity
import androidx.room.PrimaryKey
import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import androidx.room.Database
import androidx.room.RoomDatabase
import kotlinx.coroutines.flow.Flow

@Entity(tableName = "video_history")
data class VideoHistory(
    @PrimaryKey val videoId: String,
    val title: String,
    val channel: String,
    val timestamp: Long
)

@Dao
interface VideoHistoryDao {
    @Query("SELECT * FROM video_history ORDER BY timestamp DESC LIMIT 20")
    fun getHistory(): Flow<List<VideoHistory>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(history: VideoHistory)
}

@Database(entities = [VideoHistory::class], version = 1, exportSchema = false)
abstract class AppDatabase : RoomDatabase() {
    abstract fun videoHistoryDao(): VideoHistoryDao
}
