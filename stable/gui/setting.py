import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import filedialog
import os
import subprocess
import platform
import threading
import time
from datetime import datetime
from pygame import mixer
from tkinter import filedialog
from tkinter import messagebox
from tkinter import filedialog
import cv2
import os
from box import Box
import yaml

def open_bluetooth_settings():
    system = platform.system()
    try:
        if system == "Windows":
            subprocess.run(["start", "ms-settings:bluetooth"], shell=True)
        elif system == "Darwin":  # macOS
            subprocess.run(["open", "/System/Library/PreferencePanes/Bluetooth.prefPane"])
        elif system == "Linux":
            subprocess.run(["blueman-manager"])  # works if Blueman is installed
        else:
            print("Unsupported OS")
    except Exception as e:
        print(f"Error opening Bluetooth settings: {e}")

def open_wifi_settings():
    system = platform.system()
    try:
        if system == "Windows":
            subprocess.run(["start", "ms-settings:network-wifi"], shell=True)
        elif system == "Darwin":  # macOS
            subprocess.run(["open", "/System/Library/PreferencePanes/Network.prefPane"])
        elif system == "Linux":
            # GNOME-based desktops (Ubuntu, Pop!_OS, etc.)
            subprocess.run(["nm-connection-editor"])
        else:
            print("Unsupported OS")
    except Exception as e:
        print(f"Error opening Wi-Fi settings: {e}")
