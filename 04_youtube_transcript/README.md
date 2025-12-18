# YouTube视频下载及中文字幕获取工具

[English](#english-version) | [中文](#中文版本)

## 中文版本

### 功能特点

这是一个功能强大的Python工具，可以：

1. **下载YouTube视频** - 支持多种分辨率和格式
2. **获取中文字幕** - 自动获取简体/繁体中文字幕
3. **自动翻译** - 如果没有中文字幕，自动将其他语言翻译成中文
4. **灵活配置** - 可以只下载视频、只获取字幕，或两者都要

### 安装步骤

#### 1. 安装系统依赖

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip ffmpeg
```

**macOS:**
```bash
brew install python3 ffmpeg
```

**Windows:**
- 安装 [Python 3.7+](https://www.python.org/downloads/)
- 安装 [FFmpeg](https://ffmpeg.org/download.html)

#### 2. 安装Python依赖

```bash
cd 04_youtube_transcript
pip install -r requirements.txt
```

### 使用方法

#### 基本用法

下载视频并获取中文字幕：
```bash
python youtube_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

#### 高级用法

**仅获取字幕（不下载视频）：**
```bash
python youtube_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID" --no-video
```

**仅下载视频（不获取字幕）：**
```bash
python youtube_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID" --no-transcript
```

**指定视频质量：**
```bash
# 下载720p视频
python youtube_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID" --format 720p

# 下载1080p视频
python youtube_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID" --format 1080p

# 下载最佳质量
python youtube_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID" --format best
```

**仅下载音频：**
```bash
python youtube_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID" --format audio_only
```

**指定输出目录：**
```bash
python youtube_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID" -o /path/to/output
```

#### 完整参数说明

```
参数:
  url                   YouTube视频URL或视频ID（必需）

可选参数:
  -h, --help            显示帮助信息
  -o OUTPUT, --output OUTPUT
                        输出目录路径（默认: downloads）
  --no-video            不下载视频，仅获取字幕
  --no-transcript       不获取字幕，仅下载视频
  -f {best,720p,1080p,audio_only}, --format {best,720p,1080p,audio_only}
                        视频质量选项（默认: best）
```

### 输出文件

工具会在指定的输出目录（默认为 `downloads/`）中创建以下文件：

- **视频文件**: `视频标题.mp4` 或 `.webm`（根据格式）
- **音频文件**: `视频标题.mp3`（如果使用 `--format audio_only`）
- **字幕文件**: `VIDEO_ID_transcript_zh-CN.txt` 或 `VIDEO_ID_transcript_zh-TW.txt`

字幕文件格式示例：
```
[00:00:05] 欢迎观看本视频
[00:00:12] 今天我们将讨论...
[00:00:20] 首先，让我们看看...
```

### 代码示例

作为Python模块使用：

```python
from youtube_downloader import YouTubeDownloader

# 创建下载器实例
downloader = YouTubeDownloader(output_dir='my_videos')

# 下载视频并获取字幕
result = downloader.process(
    url='https://www.youtube.com/watch?v=VIDEO_ID',
    download_video=True,
    get_transcript=True,
    format_option='720p'
)

print(f"视频ID: {result['video_id']}")
print(f"视频文件: {result['video_file']}")
print(f"字幕内容: {result['transcript'][:100]}...")
```

### 常见问题

**Q: 如果视频没有中文字幕怎么办？**
A: 工具会自动尝试将其他语言的字幕翻译成中文。

**Q: 支持哪些YouTube URL格式？**
A: 支持以下格式：
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/embed/VIDEO_ID`
- 直接使用视频ID

**Q: 下载失败怎么办？**
A: 请确保：
1. 网络连接正常
2. 视频URL有效且可访问
3. FFmpeg已正确安装（用于视频处理）
4. 已安装最新版本的依赖包

**Q: 可以批量下载吗？**
A: 当前版本仅支持单个视频下载。如需批量下载，可以编写脚本循环调用。

### 注意事项

1. 请遵守YouTube服务条款
2. 仅用于个人学习和研究目的
3. 下载的视频可能受版权保护
4. 需要稳定的网络连接

---

## English Version

### Features

This is a powerful Python tool that can:

1. **Download YouTube Videos** - Support multiple resolutions and formats
2. **Get Chinese Transcripts** - Automatically fetch Simplified/Traditional Chinese subtitles
3. **Auto Translation** - Automatically translate from other languages if Chinese subtitles unavailable
4. **Flexible Configuration** - Download video only, get transcript only, or both

### Installation

#### 1. Install System Dependencies

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip ffmpeg
```

**macOS:**
```bash
brew install python3 ffmpeg
```

**Windows:**
- Install [Python 3.7+](https://www.python.org/downloads/)
- Install [FFmpeg](https://ffmpeg.org/download.html)

#### 2. Install Python Dependencies

```bash
cd 04_youtube_transcript
pip install -r requirements.txt
```

### Usage

#### Basic Usage

Download video and get Chinese transcript:
```bash
python youtube_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

#### Advanced Usage

**Get transcript only (no video download):**
```bash
python youtube_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID" --no-video
```

**Download video only (no transcript):**
```bash
python youtube_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID" --no-transcript
```

**Specify video quality:**
```bash
# Download 720p video
python youtube_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID" --format 720p

# Download 1080p video
python youtube_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID" --format 1080p

# Download best quality
python youtube_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID" --format best
```

**Download audio only:**
```bash
python youtube_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID" --format audio_only
```

**Specify output directory:**
```bash
python youtube_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID" -o /path/to/output
```

#### Complete Parameters

```
Arguments:
  url                   YouTube video URL or video ID (required)

Optional arguments:
  -h, --help            Show help message
  -o OUTPUT, --output OUTPUT
                        Output directory path (default: downloads)
  --no-video            Don't download video, get transcript only
  --no-transcript       Don't get transcript, download video only
  -f {best,720p,1080p,audio_only}, --format {best,720p,1080p,audio_only}
                        Video quality option (default: best)
```

### Output Files

The tool creates the following files in the specified output directory (default: `downloads/`):

- **Video file**: `Video_Title.mp4` or `.webm` (depending on format)
- **Audio file**: `Video_Title.mp3` (if using `--format audio_only`)
- **Transcript file**: `VIDEO_ID_transcript_zh-CN.txt` or `VIDEO_ID_transcript_zh-TW.txt`

Transcript file format example:
```
[00:00:05] Welcome to this video
[00:00:12] Today we will discuss...
[00:00:20] First, let's look at...
```

### Code Example

Use as a Python module:

```python
from youtube_downloader import YouTubeDownloader

# Create downloader instance
downloader = YouTubeDownloader(output_dir='my_videos')

# Download video and get transcript
result = downloader.process(
    url='https://www.youtube.com/watch?v=VIDEO_ID',
    download_video=True,
    get_transcript=True,
    format_option='720p'
)

print(f"Video ID: {result['video_id']}")
print(f"Video file: {result['video_file']}")
print(f"Transcript: {result['transcript'][:100]}...")
```

### FAQ

**Q: What if the video doesn't have Chinese subtitles?**
A: The tool will automatically try to translate subtitles from other languages to Chinese.

**Q: What YouTube URL formats are supported?**
A: The following formats are supported:
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/embed/VIDEO_ID`
- Direct video ID

**Q: What if the download fails?**
A: Please ensure:
1. Network connection is stable
2. Video URL is valid and accessible
3. FFmpeg is correctly installed (for video processing)
4. Latest version of dependencies installed

**Q: Can I batch download?**
A: Current version supports single video download only. For batch downloads, write a script to loop through calls.

### Important Notes

1. Please comply with YouTube Terms of Service
2. For personal learning and research purposes only
3. Downloaded videos may be protected by copyright
4. Stable internet connection required

### Dependencies

- `yt-dlp` - YouTube video downloader
- `youtube-transcript-api` - YouTube transcript/subtitle API
- `ffmpeg` - Video/audio processing (system dependency)

### License

This tool is for educational purposes only. Please respect copyright and YouTube's Terms of Service.
