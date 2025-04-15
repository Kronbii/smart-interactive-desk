import sys
import serial
import control
import serial
import time

SERIAL_PORT = "/dev/ttyACM0"
BAUD = 115200

def init_serial():
    try:
        ser = serial.Serial(
            SERIAL_PORT, BAUD, timeout=1
        )  # Serial connection
        return ser
    except serial.SerialException as e:
        print(f"Serial Error: {e}", flush=True)
        return None  # Avoid crash if serial port isn't available
        

def watch():
    print("Python process started, waiting for actions...", flush=True)
    # ser = init_serial()
    
    while True:
        state = control.get_control()
        if state.get("emergency_stop"):
            print("Emergency stop activated, stopping all actions.", flush=True)
            continue
        cmd = state['command']
        if cmd != "none":
            #if isinstance(cmd, dict) and cmd.get("type") == "manual":
            print(cmd, flush=True)
                #ser.write(f"{cmd}\n".encode())
        time.sleep(0.2)
       
    
if __name__ == "__main__":
    watch()

