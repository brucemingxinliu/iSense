import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import subprocess
import os

# Initialize confidence scores
confidence_score_gpm = 0
confidence_score_match = 0

def execute_gpm_script(ip_address):
    """Execute gpm.py to generate the output image and update the confidence score."""
    global confidence_score_gpm
    try:
        subprocess.run(["python", "gpm.py", ip_address], check=True)  # Pass IP address to gpm.py
        confidence_score_gpm = fetch_confidence_scores("gpm")
        update_combined_score()
    except subprocess.CalledProcessError as e:
        print(f"Error running gpm.py: {e}")

def execute_match_script(ip_address):
    """Execute match.py to update confidence score."""
    global confidence_score_match
    try:
        subprocess.run(["python", "match.py", ip_address], check=True)  # Pass IP address to match.py
        confidence_score_match = fetch_confidence_scores("match")
        update_combined_score()
    except subprocess.CalledProcessError as e:
        print(f"Error running match.py: {e}")

def fetch_confidence_scores(script_name):
    """Fetch confidence scores. Replace this with actual score fetching logic."""
    if script_name == "gpm":
        return round(0.85, 2)  # Replace with actual logic or return value from gpm.py
    elif script_name == "match":
        return round(0.90, 2)  # Replace with actual logic or return value from match.py
    return 0

def update_combined_score():
    """Update the combined score display."""
    combined_score = confidence_score_gpm + confidence_score_match
    combined_score_label.config(text=f"Combined Score: {combined_score:.2f}")

# Create the main window
root = tk.Tk()
root.title("iSense V1.0")
root.configure(bg="#f0f0f0")

# Section for gpm.py
gpm_frame = tk.Frame(root)
gpm_frame.pack(pady=10)

gpm_label = tk.Label(gpm_frame, text="GPM Confidence Score: 0", font=("Arial", 16))
gpm_label.pack()

gpm_ip_label = tk.Label(gpm_frame, text="Camera IP Address:")
gpm_ip_label.pack()

gpm_ip_entry = tk.Entry(gpm_frame)
gpm_ip_entry.pack()

gpm_button = tk.Button(gpm_frame, text="Run GPM Script", command=lambda: execute_gpm_script(gpm_ip_entry.get()))
gpm_button.pack(pady=5)

# Section for match.py
match_frame = tk.Frame(root)
match_frame.pack(pady=10)

match_label = tk.Label(match_frame, text="Match Confidence Score: 0", font=("Arial", 16))
match_label.pack()

match_ip_label = tk.Label(match_frame, text="Camera IP Address:")
match_ip_label.pack()

match_ip_entry = tk.Entry(match_frame)
match_ip_entry.pack()

match_button = tk.Button(match_frame, text="Run Match Script", command=lambda: execute_match_script(match_ip_entry.get()))
match_button.pack(pady=5)

# Combined score label
combined_score_label = tk.Label(root, text="Combined Score: 0.00", font=("Arial", 20))
combined_score_label.pack(pady=10)

# Start the GUI loop
root.mainloop()