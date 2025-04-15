import cv2
import numpy as np

def main(frame):
    # === Load and Resize Image ===
    frame_y, frame_x = frame.shape[:2]
    
    # === Create a blank canvas ===
    canvas = np.zeros((frame_y, frame_x, 3), dtype=np.uint8)
    
    # === Convert frame to Grayscale ===
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # === Apply Gaussian Blur to Reduce Noise ===
    blur_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0)
    
    # === Adaptive Thresholding (Better Than Fixed) ===
    bin_frame = cv2.adaptiveThreshold(
        blur_frame, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV, 15, 10
    )
    
    # === Morphological Cleaning (Open → Close) ===
    kernel = np.ones((3, 3), np.uint8)
    closed_frame = cv2.morphologyEx(bin_frame, cv2.MORPH_CLOSE, kernel, iterations=5)
    
    inv_frame = cv2.bitwise_not(closed_frame)
    
    # === Create RGBA Image with Transparency ===
    rgba_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)  # Convert to RGBA
    rgba_frame[:, :, :3] = 255  # Set RGB channels to 0
    rgba_frame[:, :, 3] = closed_frame  # Set alpha channel based on closed_frame
    
    frame = cv2.resize(frame, (int(frame_x / 3), int(frame_y / 3)))
    gray_frame = cv2.resize(gray_frame, (int(frame_x / 3), int(frame_y / 3)))
    bin_frame = cv2.resize(bin_frame, (int(frame_x / 3), int(frame_y / 3)))
    closed_frame = cv2.resize(closed_frame, (int(frame_x / 3), int(frame_y / 3)))
    inv_frame = cv2.resize(inv_frame, (int(frame_x / 3), int(frame_y / 3)))
    rgba_frame = cv2.resize(rgba_frame, (int(frame_x / 3), int(frame_y / 3)))
    
     # === Show Intermediate and Final Results ===
    cv2.imshow('Canvas', canvas)
    cv2.waitKey(0)
    cv2.imshow('Original Image', frame)
    cv2.waitKey(0)
    cv2.imshow('Grayscale', gray_frame)
    cv2.waitKey(0)
    cv2.imshow('Adaptive Threshold', bin_frame)
    cv2.waitKey(0)
    cv2.imshow('Morphology Cleaned', closed_frame)
    cv2.waitKey(0)
    cv2.imshow('inverted', inv_frame)
    cv2.waitKey(0)
    cv2.imshow('final', rgba_frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    save_flag = input("Save intermediate results? (y/n): ").strip().lower() == 'y'
    
    # === Save Intermediate Results ===
    if save_flag:
        cv2.imwrite('output_image.png', rgba_frame)  # Save the final image
        canvas[0:inv_frame.shape[0], 0:inv_frame.shape[1]] = cv2.cvtColor(inv_frame, cv2.COLOR_BGRA2BGR)
        cv2.imwrite('canvas.png', canvas)
    

if __name__ == "__main__":
    img = cv2.imread("/home/kronbii/github-repos/smart-interactive-desk/test/segmentation/test1.jpeg")  # Load your image here
    main(img)