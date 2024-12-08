import cv2
import numpy as np

def locate_gpm_in_frame(frame, gpm_gray):
    # Convert the frame to grayscale
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Match template
    result = cv2.matchTemplate(frame_gray, gpm_gray, cv2.TM_CCOEFF_NORMED)
    
    # Get the maximum confidence score and its position
    max_val = np.max(result)
    max_loc = np.unravel_index(np.argmax(result), result.shape)
    
    # Set a threshold for locating GPM in the frame
    threshold = 0.8
    yloc, xloc = np.where(result >= threshold)

    # Get the dimensions of the GPM template
    h, w = gpm_gray.shape

    # Draw rectangles around the matched region
    for (x, y) in zip(xloc, yloc):
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Green rectangle

    # Return the modified frame and the max confidence score
    return frame, max_val

def main():
    # Load the GPM image and convert it to grayscale
    gpm_image_path = 'templates/rtemp.jpg'  # Path to the GPM image
    gpm_image = cv2.imread(gpm_image_path)
    gpm_gray = cv2.cvtColor(gpm_image, cv2.COLOR_BGR2GRAY)

    # Open the USB webcam by specifying the correct index. Start with 1 for a secondary camera.
    cap = cv2.VideoCapture(0)  # Change index to 1 for USB webcam. Adjust if necessary.

    if not cap.isOpened():
        print("Error: Could not open video source.")
        return

    while True:
        # Capture a frame from the camera
        ret, frame = cap.read()

        if not ret:
            print("Error: Cannot read frame.")
            break

        # Detect GPM in the current frame
        processed_frame, max_val = locate_gpm_in_frame(frame, gpm_gray)

        # Display the frame with detection
        cv2.imshow('GPM Detection', processed_frame)

        # Print confidence score
        if max_val < 0.7:
            print("Low confidence: Detection might be NG")

        # Exit the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and destroy all windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()