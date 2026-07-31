package com.example.db

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import kotlinx.coroutines.flow.Flow

/**
 * Data Access Object (DAO) for managing video history records in Room Database.
 */
@Dao
interface VideoHistoryDao {
    
    /**
     * Retrieves recent watch history items sorted by timestamp descending.
     */
    @Query("SELECT * FROM video_history ORDER BY timestamp DESC LIMIT 50")
    fun getHistory(): Flow<List<VideoHistory>>

    /**
     * Inserts or updates a video history record.
     */
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(history: VideoHistory)

    /**
     * Deletes a specific video record by ID.
     */
    @Query("DELETE FROM video_history WHERE videoId = :videoId")
    suspend fun deleteById(videoId: String)

    /**
     * Clears all watch history records.
     */
    @Query("DELETE FROM video_history")
    suspend fun clearHistory()
}
