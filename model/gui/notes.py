import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog
import os
import subprocess
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
    
def load_image():
    global displayed_image
    filepath = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if filepath:
        img = Image.open(filepath)
        img = img.resize((400, 300))  # Resize for aesthetics
        displayed_image = ImageTk.PhotoImage(img)
        current_image_label.configure(image=displayed_image)

def capture_image_from_webcam():
    subprocess.Popen(["gnome-terminal", "--", "python3", "segment.py"])

def remove_image():
    global displayed_image
    current_image_label.configure(image=None)
    displayed_image = None  # Important: release reference to the image

def create_notes_content(parent):
    global current_image_label

    parent.configure(bg=config.theme.background_color)

    # Expand image container to nearly full height
    image_frame = tk.Frame(parent, bg=config.theme.container_color, height=300)
    image_frame.pack(fill="both", expand=True, padx=20, pady=(20, 10))
    image_frame.pack_propagate(False)

    current_image_label = tk.Label(image_frame, bg=config.theme.container_color)
    current_image_label.pack(expand=True)

    # Button Container (horizontal alignment)
    button_frame = tk.Frame(parent, bg=config.theme.background_color)
    button_frame.pack(pady=10)

    tk.Button(
        button_frame,
        text="📁 Load Image",
        font=(config.theme.font_family, 10, "bold"),
        bg=config.theme.button_color,
        fg=config.theme.font_color,
        command=load_image
    ).grid(row=0, column=0, padx=5)

    tk.Button(
        button_frame,
        text="📷 Capture Image",
        font=(config.theme.font_family, 10, "bold"),
        bg=config.theme.button_color,
        fg=config.theme.font_color,
        command=capture_image_from_webcam
    ).grid(row=0, column=1, padx=5)

    tk.Button(
        button_frame,
        text="🗑️ Remove Image",
        font=(config.theme.font_family, 10, "bold"),
        bg=config.theme.button_color,
        fg=config.theme.font_color,
        command=remove_image
    ).grid(row=0, column=2, padx=5)

    return