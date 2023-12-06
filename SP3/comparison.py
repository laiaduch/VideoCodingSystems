import subprocess

def compare_videos_ffmpeg(input_video1, input_video2, output_video):
    # Use ffmpeg to concatenate videos side by side
    ffmpeg_command = ['ffmpeg', '-i',  input_video1, '-i', input_video2, '-filter_complex',
                      '[0:v][1:v]hstack=inputs=2[v];[0:a][1:a]amerge=inputs=2[a]', '-map', '[v]',
                      '-map', '[a]', output_video]

    # Run the ffmpeg command
    subprocess.run(ffmpeg_command)

# Example usage:
video1 = "output_vp8.webm"
video2 = "output_vp9.webm"

compare_videos_ffmpeg(video1, video2, "comparison_video.mp4")
