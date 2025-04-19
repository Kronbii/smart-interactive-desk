# serial_manager.py
import serial
import time
import atexit

arduino_serial = None

def init_serial(port="/dev/ttyACM0", baudrate=115200, timeout=1):
    global arduino_serial
    try:
        arduino_serial = serial.Serial(port, baudrate, timeout=1)
        time.sleep(2)
        print("✅ Arduino connected.")
    except serial.SerialException as e:
        print(f"❌ Serial error: {e}")

def send_command(command):
    global arduino_serial
    print(f"→ Sending: {command}")
    if arduino_serial and arduino_serial.is_open:
        try:
            arduino_serial.write((command + "\n").encode())
        except serial.SerialException as e:
            print(f"❌ Write failed: {e}")
    else:
        print("❌ Serial not connected.")

@atexit.register
def close_serial():
    global arduino_serial
    if arduino_serial and arduino_serial.is_open:
        arduino_serial.close()
        print("🔌 Serial connection closed.")
