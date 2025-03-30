import sys
import serial
import json

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

def add_user(filepath, name, userID, pos1, pos2, pos3, pos4):
    #format new data
    new_data = {
        userID:{
        "name": name,
        "pos1": pos1,
        "pos2": pos2,
        "pos3": pos3,
        "pos4": pos4
        }
    }
    # Open the file in read mode to load existing data
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # If the file doesn't exist or is empty, start with an empty list or dict
        data = {}

    # Update the data with the new data (you can adjust this part based on the structure of your data)
    data.update(new_data)

    # Write the updated data back to the file
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)


def main():
    add_user('/home/bemo/smart-interactive-desk/user-database/users.json', 'df', 5, 45, 3455, 6, 7)
    '''
    print("Python process started, waiting for actions...", flush=True)
    ser = init_serial()

    while True:
        action = sys.stdin.readline().strip()  # Wait for input from Node.js
        if not action:
            continue  # Ignore empty input
        
        send_signal(action, ser)  # Send to ESP32

        # Respond back to Node.js
        # print(f"Python received action: {action}", flush=True)
'''
if __name__ == "__main__":
    main()
