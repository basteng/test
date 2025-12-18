#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YouTube Downloader 使用示例
Example usage of YouTube Downloader
"""

from youtube_downloader import YouTubeDownloader


def example_1_download_with_transcript():
    """
    示例1: 下载视频并获取中文字幕
    Example 1: Download video and get Chinese transcript
    """
    print("\n" + "="*60)
    print("示例1: 下载视频 + 获取字幕")
    print("Example 1: Download video + Get transcript")
    print("="*60)

    downloader = YouTubeDownloader(output_dir='downloads')

    # 替换为实际的YouTube URL
    # Replace with actual YouTube URL
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # 示例URL

    result = downloader.process(
        url=url,
        download_video=True,
        get_transcript=True,
        format_option='720p'
    )

    print(f"\n视频ID: {result['video_id']}")
    print(f"视频文件: {result['video_file']}")
    if result['transcript']:
        print(f"字幕获取成功，前100字符: {result['transcript'][:100]}...")


def example_2_transcript_only():
    """
    示例2: 仅获取字幕
    Example 2: Get transcript only
    """
    print("\n" + "="*60)
    print("示例2: 仅获取字幕")
    print("Example 2: Get transcript only")
    print("="*60)

    downloader = YouTubeDownloader(output_dir='downloads')

    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

    result = downloader.process(
        url=url,
        download_video=False,
        get_transcript=True
    )

    print(f"\n视频ID: {result['video_id']}")
    if result['transcript']:
        lines = result['transcript'].split('\n')
        print(f"字幕行数: {len(lines)}")
        print("\n前5行字幕:")
        for line in lines[:5]:
            print(line)


def example_3_video_only():
    """
    示例3: 仅下载视频
    Example 3: Download video only
    """
    print("\n" + "="*60)
    print("示例3: 仅下载视频")
    print("Example 3: Download video only")
    print("="*60)

    downloader = YouTubeDownloader(output_dir='downloads')

    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

    result = downloader.process(
        url=url,
        download_video=True,
        get_transcript=False,
        format_option='best'
    )

    print(f"\n视频ID: {result['video_id']}")
    print(f"视频文件: {result['video_file']}")


def example_4_audio_only():
    """
    示例4: 仅下载音频
    Example 4: Download audio only
    """
    print("\n" + "="*60)
    print("示例4: 仅下载音频")
    print("Example 4: Download audio only")
    print("="*60)

    downloader = YouTubeDownloader(output_dir='downloads')

    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

    result = downloader.process(
        url=url,
        download_video=True,
        get_transcript=False,
        format_option='audio_only'
    )

    print(f"\n视频ID: {result['video_id']}")
    print(f"音频文件: {result['video_file']}")


def example_5_batch_urls():
    """
    示例5: 批量下载多个视频
    Example 5: Batch download multiple videos
    """
    print("\n" + "="*60)
    print("示例5: 批量下载")
    print("Example 5: Batch download")
    print("="*60)

    downloader = YouTubeDownloader(output_dir='downloads')

    urls = [
        "https://www.youtube.com/watch?v=VIDEO_ID_1",
        "https://www.youtube.com/watch?v=VIDEO_ID_2",
        "https://www.youtube.com/watch?v=VIDEO_ID_3",
    ]

    results = []
    for i, url in enumerate(urls, 1):
        print(f"\n处理第 {i}/{len(urls)} 个视频...")
        try:
            result = downloader.process(
                url=url,
                download_video=True,
                get_transcript=True,
                format_option='720p'
            )
            results.append(result)
            print(f"✓ 完成: {result['video_id']}")
        except Exception as e:
            print(f"✗ 失败: {url} - {e}")

    print(f"\n总计完成: {len(results)}/{len(urls)}")


def main():
    """主函数 - 运行所有示例"""
    print("\n" + "="*60)
    print("YouTube Downloader 使用示例")
    print("YouTube Downloader Examples")
    print("="*60)

    print("\n注意: 这些是示例代码")
    print("Note: These are example codes")
    print("请将示例中的URL替换为实际的YouTube视频URL")
    print("Please replace URLs with actual YouTube video URLs")

    print("\n可用示例:")
    print("Available examples:")
    print("1. example_1_download_with_transcript() - 下载视频+字幕")
    print("2. example_2_transcript_only() - 仅字幕")
    print("3. example_3_video_only() - 仅视频")
    print("4. example_4_audio_only() - 仅音频")
    print("5. example_5_batch_urls() - 批量下载")

    print("\n要运行示例，请取消下面相应行的注释:")
    print("To run examples, uncomment the lines below:")
    print()

    # 取消注释以运行示例
    # Uncomment to run examples
    # example_1_download_with_transcript()
    # example_2_transcript_only()
    # example_3_video_only()
    # example_4_audio_only()
    # example_5_batch_urls()


if __name__ == '__main__':
    main()
