import time
from pyPS4Controller.controller import Controller


class MyController(Controller):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._up = False  # Flag to control the loop
        self._down = False  # Flag to control the loop
        self._stop = False  # Flag to control the loop

    def send_signal(self):
        """Continuously sends signal while Up Arrow is pressed"""
        if self._up:
            print("send up")
            time.sleep(0.1)
        elif self._down:
            print("send down")
            time.sleep(0.1)
        elif self._stop:
            print("stop")
            time.sleep(0.1)

    def on_up_arrow_press(self):
        self._up = True
        self.send_signal()

    def on_down_arrow_press(self):
        self._down = True
        self.send_signal()

    def on_up_down_arrow_release(self):
        self._stop = False  # Stop sending the signal
        self.send_signal()

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
controller.listen(timeout=60)
