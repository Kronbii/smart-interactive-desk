import tkinter as tk
from tkinter import ttk
from box import Box
import yaml
from .init_serial import send_command
from gui import CONFIG_PATH

# Load config.yaml
with open(CONFIG_PATH, "r") as file:
    config = Box(yaml.safe_load(file))

def on_button_release(event=None):
    print("Command: s")
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

    height_val = 75
    tilt_val = 4
    up_pressed = tk.BooleanVar(value=False)
    down_pressed = tk.BooleanVar(value=False)
    tilt_up_pressed = tk.BooleanVar(value=False)
    tilt_down_pressed = tk.BooleanVar(value=False)

    height_var = tk.StringVar(value="75 cm")
    tilt_var = tk.StringVar(value="4°")

    def update_height_tilt():
        nonlocal height_val, tilt_val

        if up_pressed.get():
            height_val += 1.5
            height_var.set(f"{height_val} cm")
        elif down_pressed.get():
            height_val = max(0, height_val - 1)
            height_var.set(f"{height_val} cm")

        if tilt_up_pressed.get():
            tilt_val += 3
            tilt_var.set(f"{tilt_val}°")
        elif tilt_down_pressed.get():
            tilt_val = max(0, tilt_val - 1)
            tilt_var.set(f"{tilt_val}°")

        frame.after(1000, update_height_tilt)

    def create_control_button(parent, label, cmd, press_flag=None):
        btn = ttk.Button(parent, text=label, style="Rounded.TButton")
        if press_flag is not None:
            btn.bind("<ButtonPress-1>", lambda e: [press_flag.set(True), send_command(cmd)])
            btn.bind("<ButtonRelease-1>", lambda e: [press_flag.set(False), on_button_release()])
        else:
            btn.config(command=lambda: send_command(cmd))
        return btn

    up_btn = create_control_button(frame, "↑ Up", "u", up_pressed)
    down_btn = create_control_button(frame, "↓ Down", "d", down_pressed)
    tilt_up_btn = create_control_button(frame, "↥ Tilt Up", "tu", tilt_up_pressed)
    tilt_down_btn = create_control_button(frame, "↧ Tilt Down", "td", tilt_down_pressed)
    stop_btn = ttk.Button(frame, text="■ Stop", style="Rounded.TButton", command=lambda: send_command("s"))

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

    update_height_tilt()  # Start update loop

    return height_var, tilt_var
