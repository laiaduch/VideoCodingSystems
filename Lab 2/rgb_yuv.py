import subprocess
import numpy as np


def rgb_to_yuv(red, green, blue):
    # RGB to YUV conversion formula
    y = 0.299 * red + 0.587 * green + 0.114 * blue
    u = 0.493 * (blue - y)
    v = 0.877 * (red - y)

    return [y, u, v]


def yuv_to_rgb(y, u, v):
    # YUV to RGB conversion formula
    r = y + 1.140 * v
    g = y - 0.396 * u - 0.581 * v
    b = y + 2.032 * u

    return [r, g, b]


def resize_with_quality(input_file, output_file, width, bitrate):
    command = ['ffmpeg', '-i', input_file, '-vf', f'scale={width}:-1', '-b:v', f'{bitrate}k', output_file]
    subprocess.run(command, check=True)


def serpentine(file_path):
    with open(file_path, 'rb') as file:
        # Read the bytes of the JPEG file
        jpeg_bytes = file.read()

        # Perform serpentine processing (zigzag pattern)
        serpentine_bytes = []
        width = 8  # Width of the zigzag pattern
        for i in range(0, len(jpeg_bytes), width):
            # Read bytes in forward order
            serpentine_bytes.extend(jpeg_bytes[i:i + width])
            # Read bytes in reverse order
            serpentine_bytes.extend(jpeg_bytes[i + width - 1:i - 1:-1])

        return serpentine_bytes


def convert_bw(input_path, output_path):
    comando_ffmpeg = ['ffmpeg', '-i', input_path, '-vf', 'format=gray', output_path]
    subprocess.run(comando_ffmpeg)


def run_length_encode(data):
    encoded_data = []
    count = 1
    for i in range(1, len(data)):
        if data[i] == data[i - 1]:
            count += 1
        else:
            encoded_data.append([data[i - 1], count])
            count = 1
    encoded_data.append([data[-1], count])  # Add the last element and its count

    return encoded_data


class DCTConverter:
    def __init__(self, size):
        self.size = size

    def dct(self, matrix):  # Compute the DCT
        return np.fft.fftn(matrix, norm='ortho')

    def idct(self, matrix):  # Compute the inverse
        return np.fft.ifftn(matrix, norm='ortho').real