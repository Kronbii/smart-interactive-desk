# **Smart Desk Control Using DualShock 4**

This guide provides step-by-step instructions on how to use a DualShock 4 controller to operate the smart desk effectively.

## **Prerequisites**
Before proceeding, ensure that:
- You have **Python 3.x** installed on your Linux/macOS machine.
- Bluetooth is **enabled** on your system.
- The `pyPS4Controller` module is installed.

## **Installation & Setup**

### **1. Install the pyPS4Controller module**
Run the following command to install the required Python module:
```bash
pip install pyPS4Controller
```

### **2. Put the DualShock 4 into pairing mode**
- Press and hold the **PS button** and the **Share button** simultaneously.
- The light bar on the controller should start flashing rapidly, indicating it is in pairing mode.

### **3. Connect the DualShock 4 to Your Linux/macOS Machine**
#### **On Linux:**
Use Bluetooth settings or run the following commands:
```bash
bluetoothctl
scan on
pair <controller_address>
connect <controller_address>
trust <controller_address>
```
#### **On macOS:**
Open **System Preferences → Bluetooth**, find the controller, and connect.

### **4. Run the Python Script**
Ensure your script is correctly configured to read input from the DualShock 4. You can achieve this by using the `pyPS4Controller` library to define a custom controller class that handles button presses and joystick movements.

#### **Example Script:**
```python
from pyPS4Controller.controller import Controller

class MyController(Controller):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_x_press(self):
        print("X button pressed")

controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
controller.listen()
```
> **Note:** Replace `/dev/input/js0` with the appropriate device path for your system. Refer to the `pyPS4Controller` documentation for additional configuration options.

Run the script using:
```bash
python your_script.py
```

### **5. Read and Interpret Data from the Terminal**
- The script should display real-time input data from the controller.
- Ensure all joystick movements and button presses register correctly.

## **Troubleshooting**
- If the controller is not detected, ensure **Bluetooth is enabled** and try reconnecting.
- If the script doesn’t receive input, confirm that **pyPS4Controller is properly installed** and your Python script is correctly implemented.
- On Linux, you may need to run the script with `sudo` for proper permissions:
  ```bash
  sudo python your_script.py
  ```

This guide ensures a seamless setup for controlling the smart desk using a DualShock 4 controller. If any issues arise, refer to system logs or test with different Bluetooth adapters.

