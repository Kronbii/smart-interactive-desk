# serial_manager.py
import serial
import time
import atexit
import threading

arduino_serial = None

def init_serial(port="/dev/ttyACM0", baudrate=115200, timeout=1):
    global arduino_serial
    try:
        arduino_serial = serial.Serial(port, baudrate, timeout=1)
        time.sleep(2)
        print("✅ Arduino connected.")
    except serial.SerialException as e:
        print(f"❌ Serial error on {port}: {e}")
        if port == "/dev/ttyACM0":
            try:
                print("🔄 Trying /dev/ttyACM1...")
                arduino_serial = serial.Serial("/dev/ttyACM1", baudrate, timeout=1)
                time.sleep(2)
                print("✅ Arduino connected on /dev/ttyACM1.")
            except serial.SerialException as e2:
                print(f"❌ Serial error on /dev/ttyACM1: {e2}")

def send_command_async(command):
    global arduino_serial
    print(f"→ Sending: {command}")
    try:
        arduino_serial.reset_input_buffer()
        arduino_serial.reset_output_buffer()
    except Exception as e:
        print("[ERROR] Serial buffers unreachable, reconnecting...")
        arduino_serial.close()
        init_serial()
        time.sleep(2)
        
    if arduino_serial is None or not arduino_serial.is_open:
            print("[INFO] Reconnecting serial...")
            init_serial()
    if arduino_serial and arduino_serial.is_open:
        try:
            arduino_serial.write((command + "\n").encode())
            arduino_serial.flush()
        except serial.SerialException as e:
            print(f"❌ Write failed: {e}")
    else:
        print("❌ Serial not connected.")
        
        
def send_command(command):
    def task():
        send_command_async(command)  # or your comm.send_command(command)
    threading.Thread(target=task, daemon=True).start()

@atexit.register
def close_serial():
    global arduino_serial
    if arduino_serial and arduino_serial.is_open:
        arduino_serial.close()
        print("🔌 Serial connection closed.")
