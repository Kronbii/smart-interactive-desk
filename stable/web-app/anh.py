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
        ser = None  # Avoid crash if serial port isn't available
        return ser
    
def send_signal(command, last_command, ser):
    if ser:
        formatted_command = f"{command}\n"  # Add newline
        print(f"Sending: {formatted_command.strip()}")
        ser.write(formatted_command.encode())  # Send over serial

def main():
    # Read the action passed from Node.js via stdin
    ser = init_serial()
    action = sys.stdin.readline().strip()
    send_signal(action, None, ser)
    
    # Process the action (you can add more processing logic here)
    print(f"Python received action: {action}")
    
    """
    # Example: respond back with a processed message
    response = f"Processed action: {action}"
    
    # Output the response to stdout
    print(response)
    """

if __name__ == "__main__":
    main()
