import time
from pyPS4Controller.controller import Controller


class MyController(Controller):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.running = False  # Flag to control the signal loop

    def on_x_press(self):
        print("X pressed: fet ya bassam")
        self.running = True

        # Run the continuous signal loop while button is pressed
        while self.running:
            print("Signal is being sent...")
            time.sleep(0.1)  # Adjust frequency of the signal

    def on_x_release(self):
        print("X released: dahar ya bassam")
        self.running = False  # Stop the loop when button is released

    # Override other event handlers to do nothing
    def on_any_press(self, button_id=None):
        pass

    def on_any_release(self, button_id=None):
        pass


controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
controller.listen(timeout=60)
