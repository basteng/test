@echo off
chcp 65001 >nul
echo ================================
echo YouTube视频下载及字幕获取工具
echo YouTube Video Downloader
echo ================================
echo.

set /p url="请输入YouTube视频URL (Enter YouTube URL): "

if "%url%"=="" (
    echo 错误: URL不能为空 / Error: URL cannot be empty
    pause
    exit /b 1
)

echo.
echo 请选择操作模式 / Select mode:
echo 1. 下载视频 + 获取字幕 (Download video + Get transcript)
echo 2. 仅获取字幕 (Transcript only)
echo 3. 仅下载视频 (Video only)
echo.
set /p mode="请选择 (1/2/3) / Select (1/2/3): "

if "%mode%"=="1" (
    python youtube_downloader.py "%url%"
) else if "%mode%"=="2" (
    python youtube_downloader.py "%url%" --no-video
) else if "%mode%"=="3" (
    python youtube_downloader.py "%url%" --no-transcript
) else (
    echo 无效选择，默认执行: 下载视频 + 获取字幕
    echo Invalid choice, default: Download video + Get transcript
    python youtube_downloader.py "%url%"
)

echo.
echo ================================
echo 处理完成 / Processing complete
echo ================================
pause
