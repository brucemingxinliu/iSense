from pypylon import pylon
import cv2
import numpy as np

def main():
    # Initialize the Pylon runtime
    #pylon.Initialize()

    # Create an instance of the camera object
    cam = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

    # Open the camera
    cam.Open()

    # Start grabbing images
    cam.StartGrabbing()

    # Set up a window for displaying the images
    cv2.namedWindow("Basler Camera Feed", cv2.WINDOW_NORMAL)

    while cam.IsGrabbing():
        grab_result = cam.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

        if grab_result.GrabSucceeded():
            # Convert the image to a NumPy array
            image_array = grab_result.Array

            # Display the image using OpenCV
            cv2.imshow("Basler Camera Feed", image_array)

        grab_result.Release()

        # Exit the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Stop grabbing and release the camera
    cam.StopGrabbing()
    cam.Close()

    # Destroy all OpenCV windows
    cv2.destroyAllWindows()

    # Terminate the Pylon runtime
    pylon.Terminate()

if __name__ == "__main__":
    main()