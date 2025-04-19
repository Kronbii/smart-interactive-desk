import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
from box import Box
import yaml
import os
from .control import create_control_content
from .web import open_qr_and_run_js

CONFIG_PATH = os.path.join("/home/kronbii/github-repos/smart-interactive-desk/stable/gui/config.yaml")
# Load config.yaml
with open(CONFIG_PATH, "r") as file:
    config = Box(yaml.safe_load(file))

def create_home_content(parent):
    parent.configure(bg=config.theme.background_color)

    # === Control Section Title ===
    tk.Label(
        parent, 
        text="🕹️ Control", 
        font=("Poppins", 16, "bold"), 
        bg=config.theme.background_color, 
        fg=config.theme.font_color
    ).pack(pady=(15, 5))

    # === Control Section ===
    control_frame = tk.Frame(parent, bg=config.theme.background_color)
    control_frame.pack()
    height_var, tilt_var = create_control_content(control_frame)

    # === Statistics Section Title ===
    tk.Label(
        parent, 
        text="📊 Statistics Overview", 
        font=("Poppins", 16, "bold"), 
        bg=config.theme.background_color, 
        fg=config.theme.font_color
    ).pack(pady=(20, 5))

    stats_frame = tk.Frame(parent, bg=config.theme.background_color)
    stats_frame.pack(pady=5)

    stats = [
        ("🧍 Time Standing", "120", "min"),
        ("🪑 Time Sitting", "0", "min"),
        ("🖥️ Time on Table", "120", "min"),
    ]
    colors = [config.theme.container_color, config.theme.container_color, config.theme.container_color]

    stat_frame = tk.Frame(stats_frame, bg=config.theme.background_color)
    stat_frame.pack(fill="x", padx=30, pady=5)

    for i, (label_text, value, unit) in enumerate(stats):
        stat_box = tk.Frame(
            stat_frame,
            bg=colors[i % len(colors)],
            padx=15,
            pady=8,
            highlightbackground=config.theme.container_color,
            highlightthickness=2
        )
        stat_box.pack(side="left", padx=8, expand=True)

        tk.Label(
            stat_box, 
            text=label_text, 
            font=("Poppins", 12, "bold"), 
            bg=colors[i], 
            fg=config.theme.accent_color  # Using accent color for text
        ).pack(side="left")
        tk.Label(
            stat_box, 
            text=value, 
            font=("Poppins", 12), 
            bg=colors[i], 
            fg=config.theme.font_color
        ).pack(side="left", padx=5)
        tk.Label(
            stat_box, 
            text=unit, 
            font=("Poppins", 12), 
            bg=colors[i], 
            fg=config.theme.font_color
        ).pack(side="left")

    # === Remote Control Button ===
    tk.Button(
        parent,
        text="🖼️ Remote Control",
        command=open_qr_and_run_js,
        font=("Poppins", 12, "bold"),
        bg=config.theme.button_color,
        fg=config.theme.button_text_color,
        relief="raised"
    ).pack(pady=15)

    return height_var, tilt_var