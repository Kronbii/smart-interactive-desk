import time
import serial
import serial.tools.list_ports
import cv2
import numpy as np
import mediapipe as mp

# === Initialize MediaPipe Models === #
mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# === Find ESP Port === #
def get_esp_port():
    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        if "USB" in port.device:
            return port.device  # Return first found USB port
    return None  # No port found

# === Posture Controller Class === #
class PostureController:
    def __init__(self, esp_port, baudrate=115200):
        try:
            self.ser = serial.Serial(esp_port, baudrate, timeout=1) 
            print(f"[INFO] Connected to ESP on {esp_port}")
        except serial.SerialException as e:
            print(f"[ERROR] Serial Connection Failed: {e}")
            self.ser = None
        self.last_command = None  # Track last command

    def send_signal(self, command):
        """Send a command only if it's different from the last one"""
        if self.last_command != command:
            self.last_command = command
            if self.ser:
                formatted_command = f"{command}\n"
                print(f"[SEND] {formatted_command.strip()}")
                self.ser.write(formatted_command.encode())

# === Posture Detection Function === #
def detect_posture(controller):
    print("[INFO] Initializing Webcam...")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[ERROR] Could not open webcam. Exiting.")
        return
    
    with mp_holistic.Holistic(min_detection_confidence=0.8, min_tracking_confidence=0.5) as holistic:
        print("[INFO] MediaPipe Model Initialized!")
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("[ERROR] Failed to capture frame. Exiting.")
                break

            frame = cv2.flip(frame, 1)  # Mirror the frame
            h, w, _ = frame.shape  # Get frame dimensions

            # Process frame with MediaPipe
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = holistic.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Extract shoulder position
            if results.pose_landmarks:
                left_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
                right_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]

                shoulder_mid_y = ((left_shoulder.y + right_shoulder.y) / 2) * h
                up_threshold = h / 2 + 70
                down_threshold = h / 2 - 70

                if shoulder_mid_y < up_threshold:
                    command = "u"
                elif shoulder_mid_y > down_threshold:
                    command = "d"
                else:
                    command = "s"

                controller.send_signal(command)  # Send to ESP
                print(command)

            # Draw reference line
            cv2.line(image, (0, h // 2), (w, h // 2), (0, 0, 255), 2)
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Display result
            cv2.imshow("Posture Detection", cv2.resize(image, (w, h)))
            if cv2.waitKey(10) & 0xFF == ord("q"):
                break

    cap.release()
    cv2.destroyAllWindows()
    print("[INFO] Program Finished Successfully.")

# === Main Function === #
def main():
    esp_port = "/dev/ttyUSB0"
    if not esp_port:
        print("[ERROR] No ESP device found. Exiting.")
        return
    
    controller = PostureController(esp_port)
    detect_posture(controller)

if __name__ == "__main__":
    main()
