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

CONFIG_PATH = os.path.join("/home/kronbii/github-repos/smart-interactive-desk/stable/gui/config.yaml")
# Load config.yaml
with open(CONFIG_PATH, "r") as file:
    config = Box(yaml.safe_load(file))

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

def create_settings_content(parent):
    parent.configure(bg=config.theme.background_color)

    title = tk.Label(
        parent,
        text="⚙️ Settings Page",
        font=(config.theme.font_family, 20, "bold"),
        bg=config.theme.background_color,
        fg=config.theme.font_color
    )
    title.grid(row=0, column=0, columnspan=2, pady=(30, 20))

    # Bluetooth button
    bluetooth_btn = tk.Button(
        parent,
        text="🔵 Bluetooth Settings",
        command=open_bluetooth_settings,
        bg=config.theme.button_color,
        fg=config.theme.button_text_color,
        font=(config.theme.font_family, 12, "bold"),
        padx=20,
        pady=10,
        relief="groove"
    )
    bluetooth_btn.grid(row=1, column=0, padx=30, pady=10, sticky="ew")

    # Wi-Fi button
    wifi_btn = tk.Button(
        parent,
        text="📶 Wi-Fi Settings",
        command=open_wifi_settings,
        bg=config.theme.button_color,
        fg=config.theme.button_text_color,
        font=(config.theme.font_family, 12, "bold"),
        padx=20,
        pady=10,
        relief="groove"
    )
    wifi_btn.grid(row=1, column=1, padx=30, pady=10, sticky="ew")

    parent.grid_columnconfigure(0, weight=1)
    parent.grid_columnconfigure(1, weight=1)
