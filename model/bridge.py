import sys
import serial
import control
import time

SERIAL_PORT = "/dev/ttyACM0"
BAUD = 115200

def init_serial():
    try:
        ser = serial.Serial(
            SERIAL_PORT, BAUD, timeout=1
        )  # Serial connection
        return ser
    except Exception as e:
        print(f"Serial Error: {e}", flush=True)
        while True:
            print("ana")
        

def watch():
    print("Python process started, waiting for actions...", flush=True)
    ser = init_serial()
    
    while True:
        state = control.get_control()
        cmd = state['command']
        cmd = f"{cmd}\n"
        print(cmd.strip(), flush=True)
        ser.write(cmd.encode())
        ser.flush()
        time.sleep(0.9)

        """
        if ser.in_waiting:
            try:
                line = ser.readline().decode(errors="ignore").strip()
                if line.startswith("POS:"):
                    parts = line[4:].split(",")
                    if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                        height = int(parts[0])
                        tilt = int(parts[1])
                        control.update_sensor_feedback(height, tilt)
            except Exception:
                print("Error reading from serial port", flush=True)
                pass
       """
    
if __name__ == "__main__":
    watch()

