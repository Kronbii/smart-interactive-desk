import time
import serial
from pyPS4Controller.controller import Controller
import serial.tools.list_ports
import posture

def get_esp_port():
    ports = list(serial.tools.list_ports.comports())  # outputs all the ports connected
    found_port = list()  # list of all the ports connected
    
    for i in range(len(ports)):
        print(ports[i])  # to print all the available ports connected
        if "USB" in ports[i].device:
            found_port.append(ports[i].device)  # append all the ports which have serial word in them
    return found_port


class PostureController():
    def __init__(self, esp_port, baudrate):
        try:
            self.ser = serial.Serial(esp_port, baudrate, timeout=1) 
        except serial.SerialException as e:
            print(f"Serial Error: {e}")
            self.ser = None
        self.last_command = None  # Track the last sent command

    def send_signal(self, command):
        """Send a command only if it's different from the last one"""
        if self.last_command != command:
            self.last_command = command
            if self.ser:
                formatted_command = f"{command}\n"  # Add newline
                print(f"Sending: {formatted_command.strip()}")
                self.ser.write(formatted_command.encode())  # Send over serial
        
    def get_command(self):
        command, flag= posture.main()
        return command, flag
                
    def el3ab(self):
        while True:
            command , flag= posture.main()
            if not flag:
                print("error")
            if command == "up":
                self.send_signal("u")
            elif command == "down":
                self.send_signal("d")
            elif command == "stop":
                self.send_signal("s")
            else:
                self.send_signal("s")
        

def main():
    esp_port = get_esp_port()
    baudrate = 115200
    controller = PostureController(esp_port, baudrate)
    controller.el3ab()

if __name__ == "__main__":
    main()
