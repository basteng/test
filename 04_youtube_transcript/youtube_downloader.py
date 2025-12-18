#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YouTube视频下载及中文字幕获取工具
YouTube Video Downloader with Chinese Transcript Extractor
"""

import os
import sys
import argparse
from pathlib import Path
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
import yt_dlp

# 清除所有代理设置，确保可以直接访问YouTube
for proxy_var in ['http_proxy', 'https_proxy', 'HTTP_PROXY', 'HTTPS_PROXY',
                   'GLOBAL_AGENT_HTTP_PROXY', 'GLOBAL_AGENT_HTTPS_PROXY']:
    os.environ.pop(proxy_var, None)


class YouTubeDownloader:
    """YouTube视频下载和字幕提取器"""

    def __init__(self, output_dir='downloads'):
        """
        初始化下载器

        Args:
            output_dir: 输出目录路径
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def extract_video_id(self, url):
        """
        从YouTube URL中提取视频ID

        Args:
            url: YouTube视频URL

        Returns:
            视频ID字符串
        """
        if 'youtu.be/' in url:
            return url.split('youtu.be/')[-1].split('?')[0]
        elif 'youtube.com/watch?v=' in url:
            return url.split('v=')[-1].split('&')[0]
        elif 'youtube.com/embed/' in url:
            return url.split('embed/')[-1].split('?')[0]
        else:
            # 假设输入的就是视频ID
            return url

    def get_chinese_transcript(self, video_id, save_to_file=True):
        """
        获取中文字幕

        Args:
            video_id: YouTube视频ID
            save_to_file: 是否保存到文件

        Returns:
            字幕文本内容
        """
        print(f"\n正在获取视频 {video_id} 的中文字幕...")

        try:
            # 尝试获取中文字幕，优先简体中文，其次繁体中文
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

            transcript = None
            transcript_lang = None

            # 尝试获取简体中文
            try:
                transcript = transcript_list.find_transcript(['zh-CN', 'zh-Hans', 'zh'])
                transcript_lang = 'zh-CN'
                print("找到简体中文字幕")
            except NoTranscriptFound:
                pass

            # 如果没有简体中文，尝试繁体中文
            if transcript is None:
                try:
                    transcript = transcript_list.find_transcript(['zh-TW', 'zh-Hant'])
                    transcript_lang = 'zh-TW'
                    print("找到繁体中文字幕")
                except NoTranscriptFound:
                    pass

            # 如果还没有，尝试自动翻译成中文
            if transcript is None:
                print("未找到中文字幕，尝试自动翻译...")
                try:
                    # 获取任意可用的字幕并翻译成中文
                    available_transcripts = list(transcript_list)
                    if available_transcripts:
                        transcript = available_transcripts[0].translate('zh-CN')
                        transcript_lang = 'zh-CN (translated)'
                        print(f"已将 {available_transcripts[0].language} 字幕翻译成中文")
                except Exception as e:
                    print(f"翻译字幕失败: {e}")
                    return None

            if transcript is None:
                print("无法获取中文字幕")
                return None

            # 获取字幕内容
            transcript_data = transcript.fetch()

            # 格式化字幕文本
            transcript_text = self._format_transcript(transcript_data)

            # 保存到文件
            if save_to_file:
                transcript_file = self.output_dir / f"{video_id}_transcript_{transcript_lang.replace(' ', '_')}.txt"
                with open(transcript_file, 'w', encoding='utf-8') as f:
                    f.write(transcript_text)
                print(f"字幕已保存到: {transcript_file}")

            return transcript_text

        except TranscriptsDisabled:
            print(f"视频 {video_id} 的字幕已被禁用")
            return None
        except NoTranscriptFound:
            print(f"视频 {video_id} 没有可用的字幕")
            return None
        except Exception as e:
            print(f"获取字幕时出错: {e}")
            return None

    def _format_transcript(self, transcript_data):
        """
        格式化字幕数据

        Args:
            transcript_data: 字幕数据列表

        Returns:
            格式化的字幕文本
        """
        lines = []
        for entry in transcript_data:
            start_time = self._format_time(entry['start'])
            text = entry['text']
            lines.append(f"[{start_time}] {text}")

        return '\n'.join(lines)

    def _format_time(self, seconds):
        """
        将秒数转换为时间格式 HH:MM:SS

        Args:
            seconds: 秒数

        Returns:
            格式化的时间字符串
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"

    def download_video(self, url, format_option='best'):
        """
        下载YouTube视频

        Args:
            url: YouTube视频URL
            format_option: 视频质量选项 ('best', '720p', '1080p', 'audio_only')

        Returns:
            下载的文件路径
        """
        print(f"\n正在下载视频: {url}")

        # 配置下载选项
        ydl_opts = {
            'outtmpl': str(self.output_dir / '%(title)s.%(ext)s'),
            'quiet': False,
            'no_warnings': False,
            'proxy': '',  # 禁用代理
        }

        # 根据格式选项设置
        if format_option == 'audio_only':
            ydl_opts['format'] = 'bestaudio/best'
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        elif format_option == '720p':
            ydl_opts['format'] = 'bestvideo[height<=720]+bestaudio/best[height<=720]'
        elif format_option == '1080p':
            ydl_opts['format'] = 'bestvideo[height<=1080]+bestaudio/best[height<=1080]'
        else:  # 'best'
            ydl_opts['format'] = 'bestvideo+bestaudio/best'

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                print(f"\n视频下载完成: {filename}")
                return filename
        except Exception as e:
            print(f"下载视频时出错: {e}")
            return None

    def process(self, url, download_video=True, get_transcript=True, format_option='best'):
        """
        处理YouTube视频：下载视频和获取字幕

        Args:
            url: YouTube视频URL
            download_video: 是否下载视频
            get_transcript: 是否获取字幕
            format_option: 视频质量选项

        Returns:
            包含视频文件路径和字幕文本的字典
        """
        video_id = self.extract_video_id(url)
        print(f"视频ID: {video_id}")

        result = {
            'video_id': video_id,
            'video_file': None,
            'transcript': None
        }

        # 获取字幕
        if get_transcript:
            transcript = self.get_chinese_transcript(video_id)
            result['transcript'] = transcript

        # 下载视频
        if download_video:
            video_file = self.download_video(url, format_option)
            result['video_file'] = video_file

        return result


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='YouTube视频下载及中文字幕获取工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  # 下载视频并获取中文字幕
  python youtube_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID"

  # 仅获取字幕，不下载视频
  python youtube_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID" --no-video

  # 仅下载视频，不获取字幕
  python youtube_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID" --no-transcript

  # 指定下载质量
  python youtube_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID" --format 720p

  # 仅下载音频
  python youtube_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID" --format audio_only
        """
    )

    parser.add_argument('url', help='YouTube视频URL或视频ID')
    parser.add_argument('-o', '--output', default='downloads',
                        help='输出目录路径 (默认: downloads)')
    parser.add_argument('--no-video', action='store_true',
                        help='不下载视频，仅获取字幕')
    parser.add_argument('--no-transcript', action='store_true',
                        help='不获取字幕，仅下载视频')
    parser.add_argument('-f', '--format', default='best',
                        choices=['best', '720p', '1080p', 'audio_only'],
                        help='视频质量选项 (默认: best)')

    args = parser.parse_args()

    # 创建下载器实例
    downloader = YouTubeDownloader(output_dir=args.output)

    # 处理视频
    result = downloader.process(
        url=args.url,
        download_video=not args.no_video,
        get_transcript=not args.no_transcript,
        format_option=args.format
    )

    # 打印结果
    print("\n" + "="*60)
    print("处理完成！")
    print("="*60)
    if result['video_file']:
        print(f"视频文件: {result['video_file']}")
    if result['transcript']:
        print(f"字幕已获取 (共 {len(result['transcript'].split(chr(10)))} 行)")
    print("="*60)


if __name__ == '__main__':
    main()
