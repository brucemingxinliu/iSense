import cv2
import numpy as np
import os
import sys

def process_images(main_image_path, template_image_path, output_path):
    # Load the main image
    main_img = cv2.imread(main_image_path, 0)

    # Load the template image
    template = cv2.imread(template_image_path, 0)

    if main_img is None or template is None:
        raise FileNotFoundError("One or both of the image files could not be loaded.")

    # Initialize SIFT detector
    sift = cv2.SIFT_create()

    # Detect keypoints and compute descriptors for the main image
    keypoints_main, descriptors_main = sift.detectAndCompute(main_img, None)
    
    # Detect keypoints and compute descriptors for the template
    keypoints_t, descriptors_t = sift.detectAndCompute(template, None)

    # Initialize FLANN-based matcher
    index_params = dict(algorithm=1, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)

    # Match descriptors
    matches = flann.knnMatch(descriptors_t, descriptors_main, k=2)

    # Function to apply ratio test
    def ratio_test(matches):
        good_matches = []
        for m, n in matches:
            if m.distance < 0.7 * n.distance:
                good_matches.append(m)
        return good_matches

    # Filter good matches for the template
    good_matches_t = ratio_test(matches)

    def calculate_score(img_area, detected_area):
        area_score = (detected_area / img_area) if img_area > 0 else 0
        final_score = area_score * 2
        return final_score

    # Function to find homography and draw bounding box
    def draw_bounding_box(good_matches, keypoints_t, keypoints_main, img, template):
        if len(good_matches) >= 1:
            src_pts = np.float32([keypoints_t[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
            dst_pts = np.float32([keypoints_main[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
            h_img, w_img = img.shape
            h, w = template.shape
            pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)

            if M is not None:
                dst = cv2.perspectiveTransform(pts, M)
                img = cv2.polylines(img, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)
                detected_area = cv2.contourArea(np.int32(dst))
                img_area = h_img * w_img
                score = calculate_score(img_area, detected_area)
                print(score)
                if score > 0.6:
                    text = f'Target Image with Detected GPM Score: {score}'
                    cv2.putText(img, text,
                                (int(dst[0][0][0]), int(dst[0][0][1]) - 10),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.5,
                                (255, 255, 255),
                                1,
                                cv2.LINE_AA)
                    #return score
        else:
            print("Not enough matches to calculate homography")
            img = np.zeros((400, 200), dtype=np.uint8)
        # Save the result image
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        cv2.imwrite(output_path, img)
        return img

    result_img = draw_bounding_box(good_matches_t, keypoints_t, keypoints_main, main_img, template)
    #print(f"Result image saved to {output_path}")
    return result_img

if __name__ == "__main__":
    # Expecting arguments: main_image_path, template_image_path, output_path
    if len(sys.argv) != 4:
        print("Usage: python l_match.py <main_image_path> <template_image_path> <output_path>")
        sys.exit(1)

    main_image_path = sys.argv[1]
    template_image_path = sys.argv[2]
    output_path = sys.argv[3]

    try:
        process_images(main_image_path, template_image_path, output_path)
    except FileNotFoundError as e:
        print(e)