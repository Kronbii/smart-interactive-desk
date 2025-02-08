import time
import serial
from pyPS4Controller.controller import Controller


class MyController(Controller):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ser = serial.Serial("/dev/ttyUSB1", 115200, timeout=1)  # Serial connection

    def send_signal(self, message):
        """Continuously sends signal while a button is pressed"""
        if self._stop:
            message = "s"
        elif self._up:
            message = "u"
        elif self._down:
            message = "d"
        print(f"Sending: {message}")
        self.ser.write(f"{message}\n".encode("utf-8"))  # Send over serial
        time.sleep(0.1)  # Adjust signal frequency

    def on_up_arrow_press(self):
        """Start sending 'u' when Up Arrow is pressed"""
        self._up = True
        self._down = False
        self._stop = False
        self.send_signal("u")

    def on_down_arrow_press(self):
        """Start sending 'd' when Down Arrow is pressed"""
        self._up = False
        self._down = True
        self._stop = False
        self.send_signal("d")

    def on_up_down_arrow_release(self):
        """Stop sending signals when button is released"""
        self._up = False
        self._down = False
        self._stop = True
        self.send_signal("s")

    # Override other event handlers to do nothing
    def on_any_press(self, button_id=None):
        pass

    def on_any_release(self, button_id=None):
        pass

    # Override other event handlers to do nothing
    def on_R3_y_at_rest(self):
        pass

    def on_R3_right(self, value):
        pass

    def on_L3_up(self, value):
        pass

    def on_L3_right(self, value):
        pass

    def on_L3_left(self, value):
        pass

    def on_R3_down(self, value):
        pass

    def on_R3_up(self, value):
        pass

    def on_L3_down(self, value):
        pass

    def on_R3_left(self, value):
        pass

    def on_R3_x_at_rest(self):
        pass

    def on_R3_y_at_rest(self):
        pass

    def on_L3_x_at_rest(self):
        pass

    def on_L3_y_at_rest(self):
        pass


controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)


def main():
    controller.listen(timeout=60)  # Keeps running until timeout


if __name__ == "__main__":
    main()
