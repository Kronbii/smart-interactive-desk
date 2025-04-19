import cv2
import numpy as np

def main(frame, i):
    # === Load and Resize Image Dimensions ===
    frame_y, frame_x = frame.shape[:2]
    
    # === Create or load a canvas ===
    try:
        canvas = cv2.imread('canvas.png')
    except:
        canvas = np.zeros((frame_y, frame_x, 3), dtype=np.uint8)
    
    # === Convert frame to grayscale ===
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # === Apply Gaussian Blur ===
    blur_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0)
    
    # === Adaptive Thresholding ===
    bin_frame = cv2.adaptiveThreshold(
        blur_frame, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV, 15, 10
    )
    
    # === Morphological Cleaning ===
    kernel = np.ones((3, 3), np.uint8)
    closed_frame = cv2.morphologyEx(bin_frame, cv2.MORPH_CLOSE, kernel, iterations=5)
    
    inv_frame = cv2.bitwise_not(closed_frame)
    
    # === Create transparent RGBA frame ===
    rgba_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
    rgba_frame[:, :, :3] = 255
    rgba_frame[:, :, 3] = closed_frame
    
    # === Resize all for display or tiling ===
    w, h = frame_x // 3, frame_y // 3
    frame      = cv2.resize(frame, (w, h))
    gray_frame = cv2.resize(gray_frame, (w, h))
    bin_frame  = cv2.resize(bin_frame, (w, h))
    closed_frame = cv2.resize(closed_frame, (w, h))
    inv_frame  = cv2.resize(inv_frame, (w, h))
    rgba_frame = cv2.resize(rgba_frame, (w, h))
    
    # === Optionally display or save frames here ===
    # cv2.imshow('Result', rgba_frame)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
    # === Ask to save and tile into canvas ===
    save_flag = input("Save intermediate results? (y/n): ").strip().lower() == 'y'
    if save_flag:
        cv2.imwrite('output_image.png', rgba_frame)
        row = i % 3
        col = i // 3
        canvas[row*h:row*h+h, col*w:col*w+w] = cv2.cvtColor(inv_frame, cv2.COLOR_BGRA2BGR)
        cv2.imwrite('canvas.png', canvas)

if __name__ == "__main__":
    # === Capture a single frame from the default webcam ===
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Cannot open webcam")
        exit(1)
    ret, frame = cap.read()
    cap.release()
    if not ret:
        print("Error: Failed to capture image from webcam")
        exit(1)
    # Pass the captured frame into main
    main(frame, 4)
