# In this script we will find all the functions implemented for the lab 1
# In addition, we have a test part that the user can interact to test the created functions

import subprocess
import numpy as np

# TASK 1: convert values
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

# TASK 2: resize image to a low quality
def resize_with_quality(input_file, output_file, width, bitrate):
    command = [
        'ffmpeg',
        '-i', input_file,
        '-vf', f'scale={width}:-1',
        '-b:v', f'{bitrate}k',
        output_file
    ]
    subprocess.run(command, check=True)


# TASK 3: serpentine algorithm
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


# TASK 4: convert the image into bw
def convert_bw(input_path, output_path):
    comando_ffmpeg = [
        'ffmpeg',
        '-i', input_path,
        '-vf', 'format=gray',  # Filter to convert to bw
        output_path
    ]

    subprocess.run(comando_ffmpeg)

# TASK 5: run-length encoding
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

# TASK 6: DCT class
class DCTConverter:
    def __init__(self, size):
        self.size = size

    def dct(self, matrix): # Compute the DCT
        return np.fft.fftn(matrix, norm='ortho')

    def idct(self, matrix): # Compute the inverse
        return np.fft.ifftn(matrix, norm='ortho').real



################ TEST FUNCTIONS ##################
try:
    option = int(input("What do you wan to do? \n1- Convert RGB to YUV \n2- Convert YUV to RGB "
                       "\n3- Resize the image \n4- Read bytes in a serpentine way \n5- Convert the image into bw "
                       "\n6- Run-length encodinf for a given bits \n7-Class DCT: Compute the DCT and the inverse "))

except:
    print("Incorrect option")
    option = 0

# Option 1: converts from RGB to YUV
if option == 1:
    R = float(input("Choose the RED component: "))
    G = float(input("Choose the GREEN component: "))
    B = float(input("Choose the BLUE component: "))

    [Y, U, V] = rgb_to_yuv(R, G, B)
    print('The values in YUV are [%.2f, %.2f, %.2f]' % (Y, U, V))

# Option 2: converts from YUV to RGB
if option == 2:
    Y = float(input("Choose the Y component: "))
    U = float(input("Choose the U component: "))
    V = float(input("Choose the V component: "))

    [R, G, B] = yuv_to_rgb(Y, U, V)
    print('The values in RGB are [%.2f, %.2f, %.2f]' % (R, G, B))

# Option 3: resize the image (low quality)
if option == 3:
    input_file = "eddie.jpg"
    output_file = "eddie_resized.jpg"
    width = 510  # Desired width for resizing
    bitrate = 100  # Desired bitrate in kilobits per second (adjust as needed)

    resize_with_quality(input_file, output_file, width, bitrate)

# Option 4: read the bytes of an image in a serpentine way
if option == 4:
    input_file = "eddie.jpg"
    serpentine_bytes = serpentine(input_file)
    print('The bytes are:\n', serpentine_bytes)

# Option 5: convert the image into bw
if option == 5:
    input_file = "eddie.jpg"
    output_file = "eddie_bw.jpg"
    convert_bw(input_file, output_file)

# Option 6: Apply run-length encoding for a given sequence of bits
if option == 6:
    data = '00010010101000111100011'
    print(run_length_encode(data))

# Option 7: example usage of the class DCTConverter
if option == 7:
    dct_converter = DCTConverter(size=(8, 8)) # Instance of DCTConverter class

    input_matrix = np.random.random((8, 8)) # Fill the matrix with random numbers

    # Compute DCT
    dct_result = dct_converter.dct(input_matrix)
    print("DCT Result:")
    print(dct_result)

    # Compute inverse DCT
    inverse_dct_result = dct_converter.idct(dct_result)
    print("Inverse DCT Result:")
    print(inverse_dct_result)