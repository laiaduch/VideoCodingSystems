# Script to define all the necessary methods to download a video and integrate it the subtitles
import subprocess
import os

def download_video(video_url): # Download the video from the URL
    # Obtain the name of the file video without extension
    video_filename = os.path.join('video.mp4')

    subprocess.run(['yt-dlp', '-o', video_filename, video_url], check=True)
    print(f'The video is downloaded: {video_filename}')
    return video_filename


def download_subtitles(video_url): # Downlaod the subtitles of the video
    # Obtain the name of the subtitle file wihtout extension
    subtitle_filename = os.path.join('subtitles.vtt')

    subprocess.run(['yt-dlp', '--skip-download', '--write-sub', '--sub-lang', 'en', '--convert-subs', 'vtt', '-o',
                    subtitle_filename, video_url], check=True)
    print(f'The subtitles has been downloaded: {subtitle_filename}')
    return subtitle_filename

def integrate_subtitles(video_input, subtitles_input, video_output): # Create a new video with the subtitles integrate
    # Use ffmpeg to integrate subtitles into the video
    subprocess.run(['ffmpeg', '-i', video_input, '-vf', f'subtitles={subtitles_input}', '-c:a', 'libmp3lame', video_output], check=True)

    # Clean up temporary files
    os.remove(video_input)
