import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import threading

class CameraApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Camera Input")
        self.video_source = None
        self.is_running = False

        # Create UI elements
        self.label = tk.Label(master, text="Enter Camera IP Address:")
        self.label.pack(pady=10)

        self.ip_entry = tk.Entry(master)
        self.ip_entry.pack(pady=5)

        self.start_button = tk.Button(master, text="Start Camera", command=self.start_camera)
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(master, text="Stop Camera", command=self.stop_camera)
        self.stop_button.pack(pady=5)

        self.video_label = tk.Label(master)
        self.video_label.pack(pady=10)

        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)  # Handle window closing

    def start_camera(self):
        ip_address = self.ip_entry.get()
        self.video_source = f"rtsp://{ip_address}/..."  # Update with your camera's stream URL

        self.is_running = True
        self.capture_thread = threading.Thread(target=self.capture_video)
        self.capture_thread.start()

    def stop_camera(self):
        self.is_running = False

    def capture_video(self):
        cap = cv2.VideoCapture(self.video_source)

        while self.is_running:
            ret, frame = cap.read()
            if ret:
                # Convert OpenCV frame to PIL image
                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(cv2image)
                img = img.resize((640, 480), Image.LANCZOS)
                self.photo = ImageTk.PhotoImage(img)

                # Update the video label
                self.video_label.config(image=self.photo)
                self.video_label.image = self.photo

        cap.release()

    def on_closing(self):
        self.stop_camera()
        self.master.destroy()

# Create and run the GUI
root = tk.Tk()
app = CameraApp(root)
root.mainloop()