import tkinter as tk
from tkinter import ttk
import os
from box import Box
import yaml
from .command import get_control, set_control

CONFIG_PATH = os.path.join("/home/kronbii/github-repos/smart-interactive-desk/stable/gui/config.yaml")
# Load config.yaml
with open(CONFIG_PATH, "r") as file:
    config = Box(yaml.safe_load(file))
    
def send_command(command):
    # Placeholder function for sending commands
    print(f"Command: {command}")
    data = get_control()
    data['command'] = command
    set_control(data)
    
def on_button_release():
    print(f"Command: s")
    send_command("s")

def create_control_content(parent):
    parent.configure(bg=config.theme.background_color)

    frame = tk.Frame(parent, bg=config.theme.background_color)
    frame.pack(pady=40)

    # Add custom style for Rounded.TButton
    style = ttk.Style()
    style.configure("Rounded.TButton", font=(config.theme.font_family, 10, "bold"), padding=10, relief="flat")
    style.map("Rounded.TButton",
              background=[("active", config.theme.button_hover_color), ("!disabled", config.theme.button_color)],
              foreground=[("active", config.theme.button_hover_text_color), ("!disabled", config.theme.button_text_color)])

    # Command buttons
    up_btn = ttk.Button(frame, text="↑ Up", style="Rounded.TButton", command=lambda: send_command("u"))
    down_btn = ttk.Button(frame, text="↓ Down", style="Rounded.TButton", command=lambda: send_command("d"))
    tilt_up_btn = ttk.Button(frame, text="↥ Tilt Up", style="Rounded.TButton", command=lambda: send_command("tu"))
    tilt_down_btn = ttk.Button(frame, text="↧ Tilt Down", style="Rounded.TButton", command=lambda: send_command("td"))
    stop_btn = ttk.Button(frame, text="■ Stop", style="Rounded.TButton", command=lambda: send_command("s"))

    # Dynamic variables
    height_var = tk.StringVar(value="0 cm")  # Starting value for height
    tilt_var = tk.StringVar(value="0°")     # Starting value for tilt

    # Static text labels with dynamic value next to them
    height_label = tk.Label(frame, text="Height:", bg=config.theme.container_color, fg=config.theme.accent_color,
                            font=(config.theme.font_family, 10, "bold"), width=15, height=2)
    height_value_label = tk.Label(frame, textvariable=height_var, bg=config.theme.container_color, fg=config.theme.accent_color,
                                  font=(config.theme.font_family, 10, "bold"), width=15, height=2)

    tilt_label = tk.Label(frame, text="Tilt:", bg=config.theme.container_color, fg=config.theme.accent_color,
                          font=(config.theme.font_family, 10, "bold"), width=15, height=2)
    tilt_value_label = tk.Label(frame, textvariable=tilt_var, bg=config.theme.container_color, fg=config.theme.accent_color,
                                 font=(config.theme.font_family, 10, "bold"), width=15, height=2)

    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)

    # Layout
    up_btn.grid(row=0, column=0, padx=10, pady=(20, 5), sticky="ew")
    down_btn.grid(row=0, column=1, padx=10, pady=(20, 5), sticky="ew")
    height_label.grid(row=1, column=0, padx=10, pady=(10, 5), sticky="ew")
    height_value_label.grid(row=1, column=1, padx=10, pady=(10, 5), sticky="ew")

    tilt_up_btn.grid(row=2, column=0, padx=10, pady=(10, 5), sticky="ew")
    tilt_down_btn.grid(row=2, column=1, padx=10, pady=(10, 5), sticky="ew")
    tilt_label.grid(row=3, column=0, padx=10, pady=(10, 5), sticky="ew")
    tilt_value_label.grid(row=3, column=1, padx=10, pady=(10, 5), sticky="ew")

    stop_btn.grid(row=4, column=0, columnspan=2, padx=10, pady=20, sticky="ew")

    # Return label variables so you can update them externally
    return height_var, tilt_var