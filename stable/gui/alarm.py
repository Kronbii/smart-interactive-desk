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

def schedule_reminder(reminder_time_str, message):
    def alarm_loop():
        while True:
            now = datetime.now()
            current_time_str = now.strftime("%I:%M %p")  # Format: "HH:MM AM/PM"
            
            if current_time_str == reminder_time_str:
                messagebox.showinfo("⏰ Reminder", message if message else "Time's up!")
                break  # Stop loop after triggering
            time.sleep(1)  # Wait 1 sec before checking again

    threading.Thread(target=alarm_loop, daemon=True).start()

def create_alarm_content(parent):
    parent.configure(bg=config.theme.background_color)

    # Clear previous widgets
    for widget in parent.winfo_children():
        widget.destroy()

    # Header (normal weight)
    tk.Label(
        parent,
        text="⏰ Alarm / Reminder",
        font=(config.theme.font_family, 18),  # Removed "bold"
        bg=config.theme.background_color,
        fg=config.theme.accent_color
    ).pack(pady=20)

    # Time selector frame (centered)
    time_frame = tk.Frame(parent, bg=config.theme.background_color)
    time_frame.pack(pady=10)

    tk.Label(time_frame, text="Time:", font=(config.theme.font_family, 12), bg=config.theme.background_color, fg=config.theme.font_color).grid(row=0, column=0, columnspan=3, pady=(0, 5))

    hours = [f"{h:02}" for h in range(1, 13)]
    minutes = [f"{m:02}" for m in range(0, 60)]
    am_pm = ["AM", "PM"]

    hour_box = ttk.Combobox(time_frame, values=hours, width=7, state="readonly", font=(config.theme.font_family, 14))
    hour_box.current(0)
    hour_box.grid(row=1, column=0, padx=10, pady=5)

    minute_box = ttk.Combobox(time_frame, values=minutes, width=7, state="readonly", font=(config.theme.font_family, 14))
    minute_box.current(0)
    minute_box.grid(row=1, column=1, padx=10, pady=5)

    am_pm_box = ttk.Combobox(time_frame, values=am_pm, width=7, state="readonly", font=(config.theme.font_family, 14))
    am_pm_box.current(0)
    am_pm_box.grid(row=1, column=2, padx=10, pady=5)

    # Message input below time selectors
    msg_frame = tk.Frame(parent, bg=config.theme.background_color)
    msg_frame.pack(pady=(20, 10))

    tk.Label(msg_frame, text="Message:", font=(config.theme.font_family, 12), bg=config.theme.background_color, fg=config.theme.font_color).pack(anchor="w")
    message_entry = tk.Entry(msg_frame, font=(config.theme.font_family, 12), width=40)
    message_entry.pack(pady=5)

    # Set Reminder button
    def on_set_reminder():
        reminder_time = f"{hour_box.get()}:{minute_box.get()} {am_pm_box.get()}"
        message = message_entry.get()
        schedule_reminder(reminder_time, message)
        messagebox.showinfo("Reminder Set", f"Reminder set for {reminder_time}")

    tk.Button(
        parent,
        text="➕ Set Reminder",
        font=(config.theme.font_family, 12, "bold"),
        bg=config.theme.button_color,
        fg=config.theme.button_text_color,
        padx=20,
        pady=10,
        relief="groove",
        command=on_set_reminder
    ).pack(pady=20)
