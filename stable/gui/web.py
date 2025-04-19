import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import subprocess
import os
from box import Box
import yaml

CONFIG_PATH = os.path.join("/home/kronbii/github-repos/smart-interactive-desk/stable/gui/config.yaml")
# Load config.yaml
with open(CONFIG_PATH, "r") as file:
    config = Box(yaml.safe_load(file))

def open_qr_and_run_js():
    # === Image and JS Paths ===
    base_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(base_dir, "assets", "QR.png")
    js_script_path = os.path.join(base_dir, "assets", "server.js")

    # === Open QR Image in Popup ===
    if not os.path.exists(image_path):
        print("QR image not found.")
        return

    img_win = tk.Toplevel()
    img_win.title("📷 Remote QR")
    img_win.configure(bg="#1a1f2c")

    img = Image.open(image_path)
    img = img.resize((500, 400))  # Adjust as needed
    tk_img = ImageTk.PhotoImage(img)

    tk.Label(img_win, image=tk_img, bg="#1a1f2c").pack(padx=10, pady=10)
    img_win.image = tk_img  # Keep reference

    # === Run JS Script in Background, Silently ===
    subprocess.Popen(["node", js_script_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)