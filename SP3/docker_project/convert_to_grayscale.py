import subprocess

def rgb_to_grayscale(input_video, output_video):
    # ffmpeg command to convert grayscale video
    command = [
        'ffmpeg',
        '-i', input_video,
        '-vf', 'format=gray',  # Filter to convert to grayscale
        '-c:a', 'copy',  # Copy the audio without modifications
        output_video
    ]

    try:
        # Execute ffmpeg command
        subprocess.run(command, check=True)
        print(f'Conversion completed. Grayscale video saved in  {output_video}')
    except subprocess.CalledProcessError as e:
        print(f'Error to convert the video: {e}')


input_video_path = 'BBB_cut.mp4'
output_video_path = 'BBB_grayscale.mp4'
rgb_to_grayscale(input_video_path, output_video_path)
