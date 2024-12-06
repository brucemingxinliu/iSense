import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import subprocess
import os

def execute_gpm_script():
    """Execute gpm.py to generate the output image and get the confidence scores."""
    # Execute the gpm.py script
    try:
        subprocess.run(["python", "match.py"], check=True)  # Adjust the command if needed
        # After execution, display the GPM output image and update the table.
        display_gpm_image()
        update_confidence_table()  # Update the table with confidence results
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

def update_confidence_table():
    """Update the confidence table from the results returned by match.py."""
    # Clear existing rows in the table
    for row in tree.get_children():
        tree.delete(row)

    # Mock Data - Replace this with your actual data retrieval logic
    # Assuming 'match.py' writes scores to a file or can return scores directly
    confidence_scores = fetch_confidence_scores()  # Fetch the confidence scores

    for score in confidence_scores:
        tree.insert("", tk.END, values=(score['template'], score['confidence']))

def fetch_confidence_scores():
    """Fetch confidence scores. This is a mock function for demonstration."""
    # In an actual implementation, you would parse the output of match.py or read from a file.
    # Here's a mock implementation returning dummy values.
    return [
        {"template": "Template 1", "confidence": round(0.85, 2)},
    ]

# Create the main window
root = tk.Tk()
root.title("iSense V1.0")
root.configure(bg="#f0f0f0")

# Load the initial image
initial_image_path = "left.jpg"  # Path to your initial image
if os.path.exists(initial_image_path):
    initial_image = Image.open(initial_image_path)
    initial_image = initial_image.resize((600, 400), Image.LANCZOS)  # Resize image
    photo = ImageTk.PhotoImage(initial_image)

    # Create a label to display the initial image
    label = tk.Label(root, image=photo)
    label.pack(pady=10)
else:
    print(f"Initial image not found: {initial_image_path}")

# Create a button to run gpm.py and display the processed image
button = tk.Button(root, text="Run GPM Script", command=execute_gpm_script)
button.pack(pady=10)

# Create a table to display confidence scores
tree = ttk.Treeview(root, columns=("Template", "Confidence"), show="headings")
tree.heading("Template", text="Template")
tree.heading("Confidence", text="Confidence Score")
tree.column("Confidence", anchor=tk.CENTER)

# Use a scrollbar for the Treeview
scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
tree.pack(pady=10)

# Start the GUI loop
root.mainloop()