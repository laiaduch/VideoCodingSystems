import os
import subprocess
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

class VideoConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Converter")
        self.root.configure(bg="#f8f8f8")  # Background color
        self.root.geometry("500x200") # Window size

        # Variables
        self.input_file = None
        self.output_file = None
        self.resolution_var = tk.StringVar(root)
        self.resolution_var.set("Select Resolution")
        self.codec_var = tk.StringVar(root)
        self.codec_var.set("Select Codec")

        # Layout
        self.frame = tk.Frame(root)
        self.frame.pack(pady=10)

        self.select_button = tk.Button(self.frame, text="Select Video", command=self.select_video, bg="#333333", fg='white', borderwidth=2, relief="groove", width=15)
        self.select_button.grid(row=0, column=0)

        self.selected_file_label = tk.Label(self.frame, text="Selected File: None", bg="#f8f8f8")
        self.selected_file_label.grid(row=0, column=1, padx=10)

        self.resolution_menu = tk.OptionMenu(root, self.resolution_var, "1280x720", "854x480", "360x240", "160x120")
        self.resolution_menu.config(bg="#333333", fg='white')  # Button color
        self.resolution_menu.pack(pady=10)

        self.codec_menu = tk.OptionMenu(root, self.codec_var, "libvpx", "libvpx-vp9", "libx265", "libaom-av1")
        self.codec_menu.config(bg="#333333", fg='white')  # Button color
        self.codec_menu.pack(pady=10)

        self.convert_button = tk.Button(root, text="Convert", command=self.convert_video, bg="#8ae0db", fg="black", borderwidth=2, relief="groove", width=15)
        self.convert_button.pack(pady=10)

    def select_video(self):
        self.input_file = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.mkv;*.avi;*.mpeg")])
        self.selected_file_label.config(text=f"Selected File: {self.input_file}", bg="#f8f8f8")

    def convert_video(self):
        if not self.input_file:
            tk.messagebox.showerror("Error", "Please select a video first.")
            return

        resolution = self.resolution_var.get()
        codec = self.codec_var.get()

        if resolution == "Select Resolution" or codec == "Select Codec":
            tk.messagebox.showerror("Error", "Please select resolution and codec.")
            return

        output_file = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("Video Files", "*.mp4")])

        video_converter = VideoConverter(self.input_file)
        video_converter.convert(output_file, resolution, codec)
        tk.messagebox.showinfo("Conversion Complete", "Video converted successfully.")

class VideoConverter:
    def __init__(self, input_file):
        self.input_file = input_file

    def convert(self, output_file, resolution, codec):
        # Change the resolution of video
        cmd_resolution = ['ffmpeg', '-i', self.input_file, '-vf', f'scale={resolution}', '-c:a', 'copy', output_file]
        subprocess.run(cmd_resolution)

        # Change the codec
        if codec == 'libvpx':
            cmd_codec = ['ffmpeg', '-i', output_file, '-c:v', codec, '-c:a', 'libvorbis',
                         output_file.replace('.mp4', '_converted.webm')]
            subprocess.run(cmd_codec)
        else:
            cmd_codec = ['ffmpeg', '-i', output_file, '-c:v', codec, output_file.replace('.mp4', '_converted.mp4')]
            subprocess.run(cmd_codec)
        os.remove(output_file)

# Main
if __name__ == "__main__":
    root = tk.Tk()
    app = VideoConverterGUI(root)
    root.mainloop()

