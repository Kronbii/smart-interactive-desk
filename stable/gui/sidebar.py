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
from pages import show_page

CONFIG_PATH = os.path.join("/home/kronbii/github-repos/smart-interactive-desk/stable/gui/config.yaml")
# Load config.yaml
with open(CONFIG_PATH, "r") as file:
    config = Box(yaml.safe_load(file))

def setup_sidebar(menu_items, icons, pages, sidebar):
    for item, icon_key in menu_items:
        btn = tk.Button(
            sidebar, 
            text=f"  {item}",
            image=icons[icon_key],
            compound="left",
            anchor="w",
            bg=config.theme.bar_button_color,  # Apply button color from theme
            fg=config.theme.bar_button_text_color,  # Apply text color from theme
            relief="flat",
            padx=20,
            pady=17,
            font=(config.theme.font_family, 14, "bold"),  # Increased font size and made it bold
            bd=0,
            highlightthickness=0,
            command=lambda name=item: show_page(name, pages)
        )
        btn.pack(fill="x", pady=3, padx=5)
        btn.bind("<Enter>", lambda e, b=btn: b.config(bg=config.theme.button_hover_color))  # Hover effect from theme
        btn.bind("<Leave>", lambda e, b=btn: b.config(bg=config.theme.bar_button_color))  # Default color from theme