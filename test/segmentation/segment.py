import cv2
import numpy as np

# === Load and Resize Image ===
img = cv2.imread('test/segmentation/test1.jpeg')

img_y, img_x = img.shape[:2]

canvas = np.zeros((img_y, img_x, 3), dtype=np.uint8)

# === Convert to Grayscale ===
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# === Apply Gaussian Blur to Reduce Noise ===
blurred_img = cv2.GaussianBlur(gray_img, (5, 5), 0)

# === Adaptive Thresholding (Better Than Fixed) ===
adaptive_thresh = cv2.adaptiveThreshold(
    blurred_img, 255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY_INV, 15, 10
)

# === Morphological Cleaning (Open → Close) ===
kernel = np.ones((3, 3), np.uint8)
closed = cv2.morphologyEx(adaptive_thresh, cv2.MORPH_CLOSE, kernel, iterations=5)

inv_img = cv2.bitwise_not(closed)

# === Create RGBA Image with Transparency ===
rgba_img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)  # Convert to RGBA
rgba_img[:, :, :3] = 255  # Set RGB channels to 0
rgba_img[:, :, 3] = closed  # Set alpha channel based on closed
cv2.imwrite('output_image.png', rgba_img)  # Save the final image

img = cv2.resize(img, (int(img_x / 3), int(img_y / 3)))
gray_img = cv2.resize(gray_img, (int(img_x / 3), int(img_y / 3)))
adaptive_thresh = cv2.resize(adaptive_thresh, (int(img_x / 3), int(img_y / 3)))
closed = cv2.resize(closed, (int(img_x / 3), int(img_y / 3)))
inv_img = cv2.resize(inv_img, (int(img_x / 3), int(img_y / 3)))
rgba_img = cv2.resize(rgba_img, (int(img_x / 3), int(img_y / 3)))

canvas[0:rgba_img.shape[0], 0:rgba_img.shape[1]] = cv2.cvtColor(rgba_img, cv2.COLOR_BGRA2BGR)
cv2.imwrite('canvas.png', canvas)

# === Show Intermediate and Final Results ===
cv2.imshow('Canvas', canvas)
cv2.waitKey(0)
cv2.imshow('Original Image', img)
cv2.waitKey(0)
cv2.imshow('Grayscale', gray_img)
cv2.waitKey(0)
cv2.imshow('Adaptive Threshold', adaptive_thresh)
cv2.waitKey(0)
cv2.imshow('Morphology Cleaned', closed)
cv2.waitKey(0)
cv2.imshow('inverted', inv_img)
cv2.waitKey(0)
cv2.imshow('final', rgba_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

