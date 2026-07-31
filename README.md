# YT Auto - YouTube Player & Android Auto Client 🚗📺

**YT Auto** là ứng dụng Android mã nguồn mở cho phép tìm kiếm và phát video YouTube trực tiếp trên điện thoại cũng như trên màn hình xe hơi thông qua **Android Auto**. Ứng dụng tích hợp trình phát video hiện đại dựa trên **ExoPlayer**, hỗ trợ chuyển đổi chất lượng video, tự động giữ màn hình sáng khi phát video, lưu lịch sử xem video và hỗ trợ điều khiển bằng giọng nói.

---

## 🌟 Tính năng nổi bật (Key Features)

### 📱 Trải nghiệm trên Điện thoại (Phone Experience)
- **Trình phát video nâng cao (ExoPlayer Integration)**:
  - Hỗ trợ xem dạng màn hình nhỏ (Inline / Mini-player) và chế độ xem toàn màn hình (Fullscreen).
  - Tự động giữ màn hình luôn sáng khi video đang phát (**Keep Screen On**).
  - Tùy chọn chuyển đổi độ phân giải video linh hoạt (360p, 480p, 720p, 1080p, v.v.).
- **Tìm kiếm & Khám phá (Search & Discovery)**:
  - Tìm kiếm video thông minh với tính năng tự động gợi ý.
  - Tích hợp **Tìm kiếm bằng giọng nói** (Voice Search).
  - Danh sách Video thịnh hành (Trending Videos) cập nhật liên tục.
- **Lịch sử xem video (Watch History & Persistence)**:
  - Tự động lưu lại các video đã xem vào cơ sở dữ liệu nội bộ (**Room Database**).
  - Xem lại lịch sử và tiếp tục phát video dễ dàng.

### 🚗 Trải nghiệm trên Xe hơi (Android Auto Integration)
- Hỗ trợ giao diện Android Auto chính thức sử dụng thư viện `androidx.car.app`.
- Cho phép tìm kiếm video và chọn danh sách phát ngay trên màn hình trung tâm của xe.
- Trình phát tối ưu cho điều khiển trên xe hơi (Car Head Unit UI).

---

## 🏗️ Kiến trúc & Công nghệ (Architecture & Tech Stack)

- **Ngôn ngữ**: [Kotlin](https://kotlinlang.org/) (100%)
- **Giao diện UI**: [Jetpack Compose](https://developer.android.com/jetpack/compose) & Material Design 3 (M3)
- **Trình phát phương tiện**: [Google ExoPlayer](https://developer.android.com/guide/topics/media/exoplayer)
- **Cơ sở dữ liệu nội bộ**: [Room Database](https://developer.android.com/training/data-storage/room)
- **Trích xuất dữ liệu YouTube**: Bộ trích xuất tùy chỉnh / NewPipe Engine (Không yêu cầu YouTube Data API Key)
- **Mạng (Networking)**: OkHttp 4
- **Android Auto**: `androidx.car.app:app` (Car App API Level 1+)

---

## 📂 Cấu trúc thư mục dự án (Project Structure)

```text
app/src/main/java/com/example/
├── MainActivity.kt            # Màn hình chính & Trình phát Compose
├── car/                       # Các màn hình và Service cho Android Auto
│   ├── MyCarAppService.kt     # Entry point cho Android Auto Service
│   ├── MainScreen.kt          # Màn hình danh sách trên Android Auto
│   ├── SearchScreen.kt        # Màn hình tìm kiếm trên Android Auto
│   └── PlayerScreen.kt        # Màn hình phát video trên Android Auto
├── youtube/                   # Bộ trích xuất & Tìm kiếm dữ liệu YouTube
│   ├── YoutubeSearch.kt       # API tìm kiếm video YouTube
│   ├── YoutubeExtractor.kt    # Trích xuất luồng phát (Video Streams)
│   ├── YoutubeRelated.kt      # Gợi ý video liên quan
│   └── VideoItem.kt           # Data class đối tượng Video
├── db/                        # Quản lý cơ sở dữ liệu Room Database
│   ├── VideoHistory.kt        # Room Entity lưu lịch sử xem video
│   ├── VideoHistoryDao.kt     # Room DAO truy xuất cơ sở dữ liệu
│   └── AppDatabase.kt         # Room Database Singleton (Thread-safe)
└── ui/theme/                  # Cấu hình giao diện Material 3 (Color, Type, Theme)
```

---

## 🚀 Hướng dẫn Biên dịch & Cài đặt (Build & Installation)

### Yêu cầu môi trường (Prerequisites)
- **Android Studio**: Jellyfish / Ladybug hoặc mới hơn
- **JDK**: Java 17 trở lên
- **Android SDK**: Compile SDK 34, Min SDK 24 (Android 7.0+)

### Các bước thực hiện

1. **Clone repository**:
   ```bash
   git clone https://github.com/your-username/yt-auto.git
   cd yt-auto
   ```

2. **Mở dự án trong Android Studio**:
   - Chọn `File` -> `Open` -> Chọn thư mục dự án `yt-auto`.
   - Để Gradle tự động đồng bộ dependencies.

3. **Biên dịch APK Debug**:
   ```bash
   ./gradlew assembleDebug
   ```
   File APK đầu ra nằm tại: `app/build/outputs/apk/debug/app-debug.apk`

4. **Chạy kiểm thử (Unit Tests)**:
   ```bash
   ./gradlew testDebugUnitTest
   ```

---

## 🔒 Giấy phép (License)

Dự án được phát hành theo giấy phép **MIT License**. Bạn có thể tự do sử dụng, chỉnh sửa và phân phối mã nguồn này cho mục đích cá nhân hoặc thương mại.

---
*Cảm ơn bạn đã quan tâm đến dự án YT Auto! Nếu thấy hữu ích, hãy dành tặng repository một ⭐️ trên GitHub nhé!*
