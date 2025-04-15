import cv2
import numpy as np
import segment

# Open a connection to the webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()
i=0
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture frame.")
        break

    # Display the resulting frame
    cv2.imshow('Webcam Feed', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    segment.main(frame, i)  # Call the segment function with the captured frame
    i += 1
    

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()