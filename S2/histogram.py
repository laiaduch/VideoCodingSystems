import subprocess

def video_with_histogram(input_video, output_video):
    command = ['ffmpeg', '-i', input_video, '-vf',
               'split=2[a][b],[b]histogram, scale=500:500,format=yuv420p[hh], [a][hh]overlay',
                '-c:a', 'copy', output_video]

    subprocess.run(command)


