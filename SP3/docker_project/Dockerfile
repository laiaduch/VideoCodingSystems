FROM python:3.8

# Install FFMPEG
RUN apt-get update && apt-get install -y ffmpeg

# Create a working directory
WORKDIR /app

# Copy the Python script into the container
COPY convert_to_grayscale.py .

# Install required Python packages
RUN pip install numpy opencv-python

# Command to run the script
CMD ["python", "convert_to_grayscale.py"]
