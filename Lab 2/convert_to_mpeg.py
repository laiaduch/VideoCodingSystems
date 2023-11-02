import subprocess

import rgb_yuv as lab1

# Function to convert video to MPEG format
def convert_to_mpeg(input_file, output_file):
    command = ['ffmpeg', '-i', input_file, '-c:v', 'mpeg2video', '-b:v', '5000k', output_file]
    subprocess.run(command)

# Function to parse video information using ffmpeg
def parse_video_info(video, info_file):
    # Run FFmpeg command to get video information
    ffprobe_command = f"ffprobe -i {video} -show_streams -show_format -print_format json"
    process = subprocess.Popen(ffprobe_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()

    # Save video information to a file
    with open(info_file, "w") as info_file:
        info_file.write(output.decode("utf-8"))
        info_file.write(error.decode("utf-8"))

    print("Video information parsing completed.")

# Function to modify video resolution using ffmpeg
def modify_resolution(input_file, output_file, width, height):
    command = ['ffmpeg', '-i', input_file, '-vf', f'scale={width}:{height}', output_file]
    subprocess.run(command)

# Function to change chroma subsampling using ffmpeg
def change_chroma_subsampling(input_file, output_file):
    command = ['ffmpeg', '-i', input_file, '-c:v', 'libx264', '-vf', 'format=yuv420p', output_file]
    subprocess.run(command)

# Function to read video information and print relevant data
def read_video_info(input_file):
    command = ['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height,codec_name,bit_rate,duration', '-of', 'default=noprint_wrappers=1:nokey=1', input_file]
    result = subprocess.run(command, capture_output=True, text=True)
    print("Video Information:")
    print("Width:", result.stdout.split('\n')[0])
    print("Height:", result.stdout.split('\n')[1])
    print("Codec Name:", result.stdout.split('\n')[2])
    print("Bit Rate:", result.stdout.split('\n')[3], "bps")
    print("Duration:", result.stdout.split('\n')[4], "seconds")


# Example of usage:
input_file = 'BigBuckBunny.mp4'
info_file = 'video_info.txt'  # File to save video information

# Task 1: Convert video to MPEG format
convert_to_mpeg(input_file, 'BBB.mpeg')
print(f"Video converted to 'BBB.mpeg'")

parse_video_info(input_file, info_file) # Parse and save video information

# Task 2: Modify video resolution
new_width = 640  
new_height = 480
modify_resolution(input_file, 'BBB_modified.mpeg', new_width, new_height)
print(f"Video resolution modified. New file saved as 'BBB_modified.mpeg'")

# Task 3: Chroma subsampling
input_file = 'BigBuckBunny.mp4'
change_chroma_subsampling(input_file, 'BBB_subsampling.mpeg')
print(f"Chroma subsampling changed. New file saved as 'BBB_subsampling.mp4'")


# Task 4: print relevant information
read_video_info(input_file)


# Task 5: inherits from lab 1
input_image = 'eddie.jpg'
lab1.convert_bw(input_image, 'new_eddie_bw.jpg')

