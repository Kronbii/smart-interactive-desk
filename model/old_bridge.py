import sys
import serial
import control
import time

SERIAL_PORT = "/dev/ttyACM0"
BAUD = 115200
last_cmd = "none"
#TOOD: only send command or edit command if its different thaan last command

def init_serial():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD, timeout=0.2)
        ser.reset_input_buffer()
        return ser
    except Exception as e:
        print(f"Serial Error: {e}", flush=True)
        while True:
            print("ana")
        

def watch():
    print("Python process started, waiting for actions...", flush=True)
    last_cmd = "none"
    
    ser = init_serial()
    if not ser or not ser.is_open:
        print("Trying to reconnect to Arduino...", flash=True)
        ser = init_serial()
        return
    
    while True:
        state = control.get_control()
        cmd = state['command'].strip()
        
        if cmd != last_cmd:
            last_cmd = cmd
            print(cmd.strip(), flush=True)
            ser.write((cmd.strip() + "\n").encode("utf-8"))

        while ser.in_waiting == 0:  # Wait for Arduino to respond
            print("No response from Arduino", flush=True)
            break

        if ser.in_waiting >0:
            response = ser.readline().decode('utf-8').rstrip()  # Read response
            print(f"Response: {response}", flush=True)
            
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

