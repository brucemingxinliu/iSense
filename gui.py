import tkinter as tk
from PIL import Image, ImageTk
import subprocess
import os

def execute_gpm_script():
    """Execute gpm.py to generate the output image."""
    # Execute the gpm.py script
    try:
        subprocess.run(["python", "gpm.py"], check=True)  # Adjust the command if needed
        # After execution, display the GPM output image
        display_gpm_image()
    except subprocess.CalledProcessError as e:
        print(f"Error running gpm.py: {e}")

def display_gpm_image():
    """Load and display the GPM processed image."""
    gpm_image_path = "gpm_output.jpg"  # Path to your GPM processed image

    if os.path.exists(gpm_image_path):
        gpm_image = Image.open(gpm_image_path)
        gpm_image = gpm_image.resize((600, 400), Image.LANCZOS)  # Resize the image
        photo = ImageTk.PhotoImage(gpm_image)

        # Update the label to show the new image
        label.config(image=photo)
        label.image = photo  # Keep a reference to avoid garbage collection
    else:
        print(f"GPM image not found: {gpm_image_path}")

# Create the main window
root = tk.Tk()
root.title("iSense V1.0")

# Load the initial image
initial_image_path = "failedleft.jpg"  # Path to your initial image
if os.path.exists(initial_image_path):
    initial_image = Image.open(initial_image_path)
    initial_image = initial_image.resize((600, 400), Image.LANCZOS)  # Resize image to fit the window
    photo = ImageTk.PhotoImage(initial_image)

    # Create a label to display the initial image
    label = tk.Label(root, image=photo)
    label.pack(pady=10)
else:
    print(f"Initial image not found: {initial_image_path}")

# Create a button to run gpm.py and display the processed image
button = tk.Button(root, text="Run GPM Script", command=execute_gpm_script)
button.pack(pady=10)

# Start the GUI loop
root.mainloop()