import time
from pyPS4Controller.controller import Controller


class MyController(Controller):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.running = False  # Flag to control the signal loop

    def on_x_press(self):
        print("X pressed: fet ya bassam")
        self.running = True

    def on_x_release(self):
        print("X released: dahar ya bassam")
        self.running = False  # Stop the loop when button is released

    # Override other event handlers to do nothing
    def on_any_press(self, button_id=None):
        pass

    def on_any_release(self, button_id=None):
        pass

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
while controller.running:
    print("Running")
    time.sleep(1)
    controller.listen(timeout=60)
