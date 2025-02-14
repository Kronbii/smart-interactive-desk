import cv2
import numpy as np
import mediapipe as mp

# Initialize MediaPipe models
mp_holistic = mp.solutions.holistic  # Full-body detection model
mp_drawing = mp.solutions.drawing_utils  # Utility to draw landmarks
mp_face_mesh = mp.solutions.face_mesh
mp_pose = mp.solutions.pose
mp_hands = mp.solutions.hands

print("[INFO] Initializing webcam...")

# Open webcam (0 = default camera)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print(
        "[ERROR] Could not open webcam. Check camera permissions or close other apps using the webcam."
    )
    exit()

print("[INFO] Webcam initialized successfully!")


# Function to detect and process the frame
def mediapipe_detection(image, model):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = model.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    return image, results


# Function to extract keypoints
def extract_keypoints(results):
    pose = (
        np.array(
            [
                [res.x, res.y, res.z, res.visibility]
                for res in results.pose_landmarks.landmark
            ]
        ).flatten()
        if results.pose_landmarks
        else np.zeros(33 * 4)
    )
    face = (
        np.array(
            [[res.x, res.y, res.z] for res in results.face_landmarks.landmark]
        ).flatten()
        if results.face_landmarks
        else np.zeros(468 * 3)
    )
    lh = (
        np.array(
            [[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]
        ).flatten()
        if results.left_hand_landmarks
        else np.zeros(21 * 3)
    )
    rh = (
        np.array(
            [[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]
        ).flatten()
        if results.right_hand_landmarks
        else np.zeros(21 * 3)
    )

    return np.concatenate([pose, face, lh, rh])


# Function to draw landmarks on frame
def draw_landmarks(image, results):
    """
    if results.face_landmarks:
        mp_drawing.draw_landmarks(
            image, results.face_landmarks, mp_face_mesh.FACEMESH_TESSELATION
        )
    """
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(
            image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS
        )
    if results.left_hand_landmarks:
        mp_drawing.draw_landmarks(
            image, results.left_hand_landmarks, mp_hands.HAND_CONNECTIONS
        )
    if results.right_hand_landmarks:
        mp_drawing.draw_landmarks(
            image, results.right_hand_landmarks, mp_hands.HAND_CONNECTIONS
        )


# Function to calculate the distance of the shoulder line to the bottom of the frame
def calculate_shoulder_distance(image, results):
    h, w, _ = image.shape  # Get frame dimensions

    if results.pose_landmarks:
        left_shoulder = results.pose_landmarks.landmark[
            mp_pose.PoseLandmark.LEFT_SHOULDER
        ]
        right_shoulder = results.pose_landmarks.landmark[
            mp_pose.PoseLandmark.RIGHT_SHOULDER
        ]

        # Convert normalized coordinates to pixel coordinates
        left_shoulder_y = int(left_shoulder.y * h)
        right_shoulder_y = int(right_shoulder.y * h)

        # Compute midpoint of the shoulder line
        shoulder_mid_y = (left_shoulder_y + right_shoulder_y) // 2

        # Calculate distance to the bottom of the frame
        distance = h - shoulder_mid_y  # Distance in pixels

        # Display the distance on the image
        cv2.putText(
            image,
            f"Shoulder Dist: {distance}px",
            (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2,
        )

        return distance

    return None  # Return None if pose landmarks are not detected


print("[INFO] Loading MediaPipe model...")

# Set the window size
cv2.namedWindow("Sign Language Detection", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Sign Language Detection", 1800, 1200)

try:
    with mp_holistic.Holistic(
        min_detection_confidence=0.8, min_tracking_confidence=0.5
    ) as holistic:
        print("[INFO] MediaPipe model initialized successfully!")

        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                print("[ERROR] Failed to capture frame.")
                break

            # Process frame with MediaPipe
            image, results = mediapipe_detection(frame, holistic)

            # Extract keypoints
            keypoints = extract_keypoints(results)

            # Calculate shoulder distance
            shoulder_distance = calculate_shoulder_distance(image, results)

            # Draw a reference line
            cv2.line(image, (0, 250), (650, 250), (0, 0, 255), 2)

            # Draw landmarks
            draw_landmarks(image, results)

            # Resize the image to 1800x1200 before displaying
            image_resized = cv2.resize(image, (1800, 1200))

            # Show output
            cv2.imshow("Sign Language Detection", image_resized)

            # Press 'q' to exit
            if cv2.waitKey(10) & 0xFF == ord("q"):
                print("[INFO] Exiting program...")
                break

except Exception as e:
    print(f"[ERROR] An exception occurred while running MediaPipe: {e}")

print("[INFO] Releasing resources...")
cap.release()
cv2.destroyAllWindows()
print("[INFO] Program finished successfully.")
