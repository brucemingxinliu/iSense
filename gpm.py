import cv2
import numpy as np
import matplotlib.pyplot as plt

def locate_gpm(gpm_path, target_path):
    # Load images
    gpm_image = cv2.imread(gpm_path)
    target_image = cv2.imread(target_path)

    # Convert images to grayscale
    gpm_gray = cv2.cvtColor(gpm_image, cv2.COLOR_BGR2GRAY)
    target_gray = cv2.cvtColor(target_image, cv2.COLOR_BGR2GRAY)

    # Match template
    result = cv2.matchTemplate(target_gray, gpm_gray, cv2.TM_CCOEFF_NORMED)
    # Get the maximum confidence score and its position
    max_val = np.max(result)
    max_loc = np.unravel_index(np.argmax(result), result.shape)  # The top-left corner of the best match
    # Set a threshold for locating GPM in the target image
    threshold = 0.8
    yloc, xloc = np.where(result >= threshold)

    # Get the dimensions of the GPM
    h, w = gpm_gray.shape

    # Draw rectangles around the matched region
    for (x, y) in zip(xloc, yloc):
        cv2.rectangle(target_image, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Green rectangle

    # Convert BGR to RGB for display
    target_image_rgb = cv2.cvtColor(target_image, cv2.COLOR_BGR2RGB)

    # Display the images with a confidence score condition
    plt.figure(figsize=(10, 5))
    plt.imshow(target_image_rgb)
    
    # Prepare title with condition for confidence score
    title_text = f'Target Image with Detected GPM\nConfidence Score: {max_val:.2f}'
    if max_val < 0.6:
        title_text += ' (NG)'  # Append "NG" if the confidence score is below 0.7
    
    plt.title(title_text)
    plt.axis('off')
    plt.show()

# Example Usage:
gpm_image_path = 'ltemp.jpg'  # Provide the GPM image path
target_image_path = 'NG/2/5.png'  # Provide the target image path

locate_gpm(gpm_image_path, target_image_path)