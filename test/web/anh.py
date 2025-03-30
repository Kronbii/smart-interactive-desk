import sys
import serial

esp32_port = "/dev/ttyUSB0"

def init_serial():
    try:
        ser = serial.Serial(
            esp32_port, 115200, timeout=1
        )  # Serial connection
        return ser
    except serial.SerialException as e:
        print(f"Serial Error: {e}", flush=True)
        return None  # Avoid crash if serial port isn't available

def send_signal(command, ser):
    if ser:
        formatted_command = f"{command}\n"  # Add newline
        print(f"{formatted_command.strip()}", flush=True)
        ser.write(formatted_command.encode())  # Send over serial

def main():
    print("Python process started, waiting for actions...", flush=True)
    ser = init_serial()

    while True:
        action = sys.stdin.readline().strip()  # Wait for input from Node.js
        if not action:
            continue  # Ignore empty input
        
        send_signal(action, ser)  # Send to ESP32

        # Respond back to Node.js
        # print(f"Python received action: {action}", flush=True)

if __name__ == "__main__":
    main()
