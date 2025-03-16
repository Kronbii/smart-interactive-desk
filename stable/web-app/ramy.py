import sys
import time
import serial
import serial.tools.list_ports

esp32_port = "/dev/ttyUSB0"

def init_serial():
    try:
        ser = serial.Serial(
            esp32_port, 115200, timeout=1
        )  # Serial connection
        return ser
    except serial.SerialException as e:
        print(f"Serial Error: {e}")
        return None
    
def send_signal(command, last_command, ser):
    if ser:
        formatted_command = f"{command}\n"  # Add newline
        print(f"Sending: {formatted_command.strip()}")
        ser.write(formatted_command.encode())  # Send over serial

def receive_data(ser):
    if ser:
        try:
            if ser.in_waiting > 0:  # Check if data is available to read
                received_data = ser.readline().decode('utf-8').strip()
                if received_data:
                    print(f"{received_data}")
                    return received_data  # Return the data if needed
        except Exception as e:
            print(f"Error while reading: {e}")


def main():
    ser = init_serial()
    if not ser:
        print("Failed to connect to ESP32")
        return
    
    action = sys.stdin.readline().strip()
    send_signal(action, None, ser)  # last_command is back in place

    # Start receiving data after sending the command
    receive_data(ser)

if __name__ == "__main__":
    main()
