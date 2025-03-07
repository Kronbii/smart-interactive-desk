import time
import serial
import serial.tools.list_ports
import cv2
import numpy as np
import mediapipe as mp
import threading

# === Constants ===
BAUDRATE = 115200
offset = 70

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

# === Video Stream Class (Threaded) === #
class VideoStream:
    def __init__(self, src=0):
        self.cap = cv2.VideoCapture(src, cv2.CAP_V4L2)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        if not self.cap.isOpened():
            print("[ERROR] Could not open webcam.")
            raise RuntimeError("Camera could not be initialized")

        self.ret, self.frame = self.cap.read()
        self.lock = threading.Lock()
        self.running = True
        self.thread = threading.Thread(target=self.update, daemon=True)
        self.thread.start()

    def update(self):
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                print("[ERROR] Failed to capture frame.")
                break
            with self.lock:
                self.ret, self.frame = ret, frame

    def read(self):
        with self.lock:
            return self.frame.copy() if self.ret else None

    def stop(self):
        self.running = False
        self.thread.join()
        self.cap.release()

# === Posture Controller Class === #
class PostureController:
    def __init__(self, esp_port, baudrate=BAUDRATE):
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
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Reduce resolution
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 60)  # Set FPS
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Reduce buffer delay
    if not cap.isOpened():
        print("[ERROR] Could not open webcam. Exiting.")
        return
    
    with mp_holistic.Holistic(min_detection_confidence=0.6, min_tracking_confidence=0.5) as holistic:
        print("[INFO] MediaPipe Model Initialized!")

        while True:
            frame = video_stream.read()
            if frame is None:
                print("[ERROR] Frame is None, skipping...")
                continue

            frame = cv2.flip(frame, 1)  # Mirror the frame
            h, w, _ = frame.shape  # Get frame dimensions

            # Process frame with MediaPipe
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = holistic.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            up_threshold = h / 2 - offset
            down_threshold = h / 2 + offset

            # Extract shoulder position
            if results.pose_landmarks:
                left_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
                right_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]

                shoulder_mid_y = ((left_shoulder.y + right_shoulder.y) / 2) * h

                if up_threshold < shoulder_mid_y < down_threshold:
                    command = "s"
                elif shoulder_mid_y < up_threshold:
                    command = "u"
                else:
                    command = "d"

                controller.send_signal(command)  # Send to ESP
                print(f"[COMMAND] {command}")

            # Draw reference lines
            cv2.line(image, (0, h // 2), (w, h // 2), (0, 0, 255), 2)
            cv2.line(image, (0, int(up_threshold)), (w, int(up_threshold)), (0, 255, 255), 2)
            cv2.line(image, (0, int(down_threshold)), (w, int(down_threshold)), (255, 255, 255), 2)
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Display result
            cv2.imshow("Posture Detection", cv2.resize(image, (w, h)))
            if cv2.waitKey(10) & 0xFF == ord("q"):
                break

    print("[INFO] Stopping video stream...")
    video_stream.stop()
    cv2.destroyAllWindows()
    print("[INFO] Program Finished Successfully.")

# === Main Function === #
def main():
    esp_port = "/dev/ttyUSB0"
    if not esp_port:
        print("[ERROR] No ESP device found. Exiting.")
        return

    controller = PostureController(esp_port)
    video_stream = VideoStream(0)  # Start threaded video capture

    try:
        detect_posture(controller, video_stream)
    except KeyboardInterrupt:
        print("\n[INFO] Exiting...")
    finally:
        video_stream.stop()

if __name__ == "__main__":
    main()
