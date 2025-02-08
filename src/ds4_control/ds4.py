import time
from pyPS4Controller.controller import Controller


class MyController(Controller):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.running = False  # Flag to control the loop

    def send_signal(self):
        """Continuously sends signal while Up Arrow is pressed"""
        while self.running:
            print("🚀 Signal is being sent!")
            time.sleep(0.1)  # Adjust the frequency of the signal

    def on_up_arrow_press(self):
        print("Up Arrow Pressed: Sending Signal...")
        if not self.running:  # Prevent duplicate loops
            self.running = True
            self.send_signal()

    def on_up_arrow_release(self):
        print("Up Arrow Released: Stopping Signal...")
        self.running = False  # Stop sending the signal

    # Override other event handlers to do nothing
    def on_any_press(self, button_id=None):
        pass

    def on_any_release(self, button_id=None):
        pass


controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
controller.listen(timeout=60)
