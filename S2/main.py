import subprocess
import os
import json

import subtitles
import histogram

class VideoProcessing(): # Create a class to perfom tasks 1, 2 and 3

    def __init__(self, input_file):
        self.input_file = input_file

    # Function to compute the macroblocks and motion vector of an input video
    def motion_vectors(self, output_motion):
        # Cut the video in 9 sec
        subprocess.run(['ffmpeg', '-i', self.input_file, '-ss', '00:00:00', '-t', '00:00:09', '-c', 'copy', 'temp_video.mp4'])

        # Compute macroblocks and motion vectors
        command = ['ffmpeg', '-flags2', '+export_mvs', '-i', 'temp_video.mp4', '-vf', 'codecview=mv=pf+bf+bb', output_motion]
        subprocess.run(command)

        # Clean up temporary files
        os.remove('temp_video.mp4')

    # Create a new container which has the video trac and three new audio tracks (package the container in a .mp4)
    def create_container(self, output_container_file):
        # Get absolute paths for input and output files
        input_file_absolute = os.path.abspath(self.input_file)
        output_container_absolute = os.path.abspath(output_container_file)

        # Cut the video in 50 sec
        subprocess.run(['ffmpeg', '-i', input_file_absolute, '-ss', '00:00:00', '-t', '00:00:50', '-c', 'copy', 'temp_video.mp4'])

        # Export the audio of BBB(50s) as MP3 mono, MP3 estéreo and AAC tracks
        subprocess.run(['ffmpeg', '-i', 'temp_video.mp4', '-vn', '-ac', '1', '-ab', '128k', '-ar', '44100', 'output_mono.mp3'])
        subprocess.run(['ffmpeg', '-i', 'temp_video.mp4', '-vn', '-ac', '2', '-ab', '96k', '-ar', '44100', 'output_stereo.mp3'])
        subprocess.run(['ffmpeg', '-i', 'temp_video.mp4', '-vn', '-ac', '2', '-ab', '128k', '-ar', '44100', '-strict',
                        'experimental',
                        'output_aac.aac'])

        # Combine the video and audio in a.mp4 file
        subprocess.run(['ffmpeg', '-i', 'temp_video.mp4', '-i', 'output_mono.mp3', '-i', 'output_stereo.mp3', '-i',
                        'output_aac.aac', '-c:v', 'copy', '-map', '0:v', '-map', '1:a:0', '-map', '2:a:0', '-map',
                        '3:a:0', '-y', output_container_absolute])

        # Clean up temporary files
        os.remove('output_mono.mp3')
        os.remove('output_stereo.mp3')
        os.remove('output_aac.aac')
        os.remove('temp_video.mp4')


    # This function counts how many tracks the input container has
    def count_tracks_in_mp4(self, input_container):
        # Counting audio tracks
        command_audio = ['ffprobe', '-v', 'error', '-select_streams', 'a', '-show_entries', 'stream=index', '-of',
                         'json', input_container]
        result_audio = subprocess.run(command_audio, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output_audio = result_audio.stdout
        data_audio = json.loads(output_audio)
        audio_tracks = len(data_audio['streams'])

        # Counting video tracks
        command_video = ['ffprobe', '-v', 'error', '-select_streams', 'v', '-show_entries', 'stream=index', '-of',
                         'json', input_container]
        result_video = subprocess.run(command_video, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output_video = result_video.stdout
        data_video = json.loads(output_video)
        video_tracks = len(data_video['streams'])

        return audio_tracks, video_tracks


# Input files:
input_file = 'BBB.mpeg'

# Constructor of the class
processing = VideoProcessing(input_file)

# Interactive part
try:
    option = int(input("What do you want to do?\n1- Create a video output that shows the macroblocks and motion vectors"
                       "\n2- Create BBB container" "\n3- How many tracks the mp4 container has? "
                       "\n4- Create a video with printed subtitles \n5- Create a new container with the YUV histogram "))

except:
    print("Incorrect option")
    option = 0

# Option 1: create a new video of 9 seconds with macroblocs and motion vectors
if option == 1:
    processing.motion_vectors('BBB_motionVectors.mpeg')

# Option 2: create BBB container which has 3 different audio tracks
if option == 2:
    processing.create_container('BBB_container.mp4')

# Option 3: Show on terminal how many tracks has the created container
if option == 3:
    audio_tracks, video_tracks = processing.count_tracks_in_mp4('BBB_container.mp4')
    print(f'Number of audio tracks: {audio_tracks}')
    print(f'Number of video tracks: {video_tracks}')


# Option 4 (inherits from subtitle.py): Create an output video with subtitles integrated
if option == 4:
    video_url = 'https://www.youtube.com/watch?v=YlUKcNNmywk'  # Replace with your desired video URL
    subtitles.download_video(video_url) # Download the video from youtube
    subtitles.download_subtitles(video_url) #Download the subtitles

    subtitles.integrate_subtitles('video.mp4.webm', 'subtitles.vtt.en.vtt', 'output_subtitles.mpeg')

# Option 5 (inherits from histogram.py): Create an output video with YUV histogram
if option == 5:
    histogram.video_with_histogram(input_file, 'BBB_histogram.mpeg')

