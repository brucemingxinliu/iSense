import cv2
import numpy as np
from pypylon import pylon

# Set up the camera
camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
camera.Open()

# The main loop where you continuously capture images from the camera
try:
    while True:
        # Grab a single frame
        camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
        converter = pylon.ImageFormatConverter()
        converter.OutputPixelFormat = pylon.PixelType_BGR8packed
        converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

        grab_result = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
        
        # Check if a frame was captured
        if grab_result.GrabSucceeded():
            # Access the image data
            image = converter.Convert(grab_result)
            main_img = image.GetArray()

            # Convert to grayscale
            main_img_gray = cv2.cvtColor(main_img, cv2.COLOR_BGR2GRAY)

            # Load template images for each area
            template1 = cv2.imread('templates/rtemp.jpg', 0)

            # Initialize SIFT detector
            sift = cv2.SIFT_create()

            # Detect keypoints and compute descriptors for the main image
            keypoints_main, descriptors_main = sift.detectAndCompute(main_img_gray, None)

            # Repeat for each template
            keypoints_t1, descriptors_t1 = sift.detectAndCompute(template1, None)

            # Initialize FLANN-based matcher
            index_params = dict(algorithm=1, trees=5)
            search_params = dict(checks=50)
            flann = cv2.FlannBasedMatcher(index_params, search_params)

            # Match descriptors
            matches_t1 = flann.knnMatch(descriptors_t1, descriptors_main, k=2)

            # Function to apply ratio test
            def ratio_test(matches):
                good_matches = []
                for m, n in matches:
                    if m.distance < 0.7 * n.distance:
                        good_matches.append(m)
                return good_matches

            # Filter good matches for each template
            good_matches_t1 = ratio_test(matches_t1)

            def calculate_score(img_area, detected_area):
                area_score = (detected_area / img_area) if img_area > 0 else 0
                final_score = area_score * 40 - 9
                return final_score

            # Function to find homography and draw bounding box
            def draw_bounding_box(good_matches, keypoints_t, keypoints_main, img, template):
                if len(good_matches) >= 1:
                    src_pts = np.float32([keypoints_t[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
                    dst_pts = np.float32([keypoints_main[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

                    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
                    h_img, w_img = img.shape[:2]
                    h, w = template.shape
                    pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)

                    if M is not None:
                        dst = cv2.perspectiveTransform(pts, M)
                        img = cv2.polylines(img, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)
                        detected_area = cv2.contourArea(np.int32(dst))
                        img_area = h_img * w_img
                        score = calculate_score(img_area, detected_area)
                        print(score)
                        if score > 0.5:
                            text = f'Target Image with Detected GPM Score: {score}'
                            cv2.putText(img, text, 
                                        (int(dst[0][0][0]), int(dst[0][0][1]) - 10),
                                        cv2.FONT_HERSHEY_SIMPLEX,
                                        0.5,
                                        (255, 255, 255),
                                        1,
                                        cv2.LINE_AA)
                else:
                    print(f"Not enough matches to calculate homography for this template (found: {len(good_matches)})")
                return img

            # Draw bounding boxes for each template
            main_img_result = draw_bounding_box(good_matches_t1, keypoints_t1, keypoints_main, main_img, template1)

            # Show the result
            desired_size = (1000, 800)
            resized_image = cv2.resize(main_img_result, desired_size)
            cv2.imshow('Detected Areas', resized_image)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        grab_result.Release()

finally:
    # Release the resources
    camera.StopGrabbing()
    camera.Close()
    cv2.destroyAllWindows()