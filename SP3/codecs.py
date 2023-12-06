import subprocess

class VideoConverter:
    def __init__(self, input_file):
        self.input_file = input_file

    # Function to change the resolution of the video
    def change_resolution(self, output_file, resolution):
        cmd = ['ffmpeg', '-i', self.input_file, '-vf', f'scale={resolution}', '-c:a', 'copy', output_file]
        subprocess.run(cmd)

    # Functions to run different codecs
    def _run_ffmpeg_command(self, output_file, codec):
        command = ['ffmpeg', '-i', self.input_file, '-c:v', codec, output_file]
        subprocess.run(command)
        print('Video converted successfully.')

    def convert_to_vp8(self, output_file):
        self._run_ffmpeg_command(output_file, 'libvpx')

    def convert_to_vp9(self, output_file):
        self._run_ffmpeg_command(output_file, 'libvpx-vp9')

    def convert_to_h265(self, output_file):
        self._run_ffmpeg_command(output_file, 'libx265')

    def convert_to_av1(self, output_file):
        self._run_ffmpeg_command(output_file, 'libaom-av1')


# Example Usage of the class
input_file = 'BBB.mpeg'
resolutions = ['1280x720', '854x480', '360x240', '160x120']

converter = VideoConverter(input_file)

for resolution in resolutions:
    output_file = f'output_{resolution}.mp4'
    converter.change_resolution(output_file, resolution)

print("Conversion completed.")
input_video = "output_854x480"
converter.convert_to_vp8('output_vp8.webm')
converter.convert_to_vp9('output_vp9.webm')
#converter.convert_to_h265('output_h265.mp4')
#converter.convert_to_av1('output_av1.webm')

