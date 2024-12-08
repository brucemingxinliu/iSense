import cv2
import numpy as np
import os
# Load the main image
main_img = cv2.imread('templates/left.jpg', 0)

# Load template images for each area
template1 = cv2.imread('templates/ltemp.jpg', 0)

# Initialize SIFT detector
sift = cv2.SIFT_create()

# Detect keypoints and compute descriptors for the main image
keypoints_main, descriptors_main = sift.detectAndCompute(main_img, None)

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
   # match_score = len(good_matches)  # Number of good matches
    area_score = (detected_area / img_area) if img_area > 0 else 0  # Ratio of the detected area to the template area

    # Combine scores; you may choose a method to combine (here we just sum them)
    final_score = area_score*2 # Multiplying the area ratio helps to scale it
    return final_score


# Function to find homography and draw bounding box
def draw_bounding_box(good_matches, keypoints_t, keypoints_main, img, template):
    if len(good_matches) >= 1:  # Require at least 4 good matches for homography
        src_pts = np.float32([keypoints_t[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([keypoints_main[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        h_img, w_img = img.shape
        h, w = template.shape
        pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
        
        if M is not None:
            dst = cv2.perspectiveTransform(pts, M)
            img = cv2.polylines(img, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)
            # Calculate detected area
            detected_area = cv2.contourArea(np.int32(dst))  # Area of the detected bounding box
            img_area = h_img*w_img
            # Calculate score
            score = calculate_score(img_area, detected_area)
            print (score)
             # Add score text on the image
            if score>0.5:
                text = f'Target Image with Detected GPM Score: {score}'
                cv2.putText(img, text, 
                            (int(dst[0][0][0]), int(dst[0][0][1]) - 10),  # Position slightly above the first point of the bounding box
                            cv2.FONT_HERSHEY_SIMPLEX,  # Font type
                            0.5,  # Font scale
                            (255, 255, 255),  # Font color (white in BGR)
                            1,  # Thickness of the text
                            cv2.LINE_AA)  # Line type
    else:
        print(f"Not enough matches to calculate homography for this template (found: {len(good_matches)})")
    # Save the result image
    output_path = 'result/left_result.jpg'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)  # Create the directory if it doesn't exist
    cv2.imwrite(output_path, main_img)
    return img

# Draw bounding boxes for each template
main_img = draw_bounding_box(good_matches_t1, keypoints_t1, keypoints_main, main_img, template1)


#print(f"Result image saved to {output_path}")
# Show the result
#desired_size = (1000,800)
#resized_image = cv2.resize(main_img, desired_size)
#cv2.imshow('Detected Areas', resized_image)
#cv2.waitKey(0)
#cv2.destroyAllWindows()