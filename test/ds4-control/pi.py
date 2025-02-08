import time
import serial
from pyPS4Controller.controller import Controller


class MyController(Controller):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            self.ser = serial.Serial(
                "/dev/ttyUSB0", 115200, timeout=1
            )  # Serial connection
        except serial.SerialException as e:
            print(f"Serial Error: {e}")
            self.ser = None  # Avoid crash if serial port isn't available

        self.current_command = None  # Track the current command

    def send_signal(self, command):
        """Send a command only if it's different from the last command"""
        if self.current_command != command:
            self.current_command = command
            if self.ser:
                print(f"Sending: {command}")
                self.ser.write(command.encode())  # Send over serial

    def on_up_arrow_press(self):
        """Start sending 'u' when Up Arrow is pressed"""
        self.send_signal("u")

    def on_down_arrow_press(self):
        """Start sending 'd' when Down Arrow is pressed"""
        self.send_signal("d")

    def on_up_down_arrow_release(self):
        """Stop sending signals when button is released"""
        self.send_signal("s")


controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)


def main():
    controller.listen(timeout=60)  # Keeps running until timeout


if __name__ == "__main__":
    main()
