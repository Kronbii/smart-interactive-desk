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
from .music import create_music_content
from .setting import open_bluetooth_settings, open_wifi_settings
from .lists import create_list_content
from .pages import create_scrollable_page, show_page
from .sidebar import setup_sidebar
from .header import setup_header
from .notes import load_image, capture_image_from_webcam, remove_image, create_notes_content
from .alarm import schedule_reminder, create_alarm_content
from .control import create_control_content
from .web import open_qr_and_run_js

current_image_label = None  # global holder to access image widget
displayed_image = None      # to prevent image from being garbage collected

mixer.init()

CONFIG_PATH = os.path.join("/home/kronbii/github-repos/smart-interactive-desk/stable/gui/config.yaml")
print(f"Config path: {CONFIG_PATH}")

# Load config.yaml
with open(CONFIG_PATH, "r") as file:
    config = Box(yaml.safe_load(file))
    
###################################Functions#####################################

def set_background(parent):
    parent.configure(bg=config.theme.background_color)

# Function to create a themed label
def create_label(parent, text, font_size=12, font_weight="normal", bg_color=None, fg_color=None):
    bg_color = bg_color or config.theme.background_color
    fg_color = fg_color or config.theme.font_color
    return tk.Label(
        parent,
        text=text,
        font=(config.theme.font_family, font_size, font_weight),
        bg=bg_color,
        fg=fg_color
    )

# Function to create a themed button
def create_button(parent, text, command, font_size=12, bg_color=None, fg_color=None):
    bg_color = bg_color or config.theme.button_color
    fg_color = fg_color or config.theme.button_text_color
    return tk.Button(
        parent,
        text=text,
        font=(config.theme.font_family, font_size, "bold"),
        bg=bg_color,
        fg=fg_color,
        activebackground=config.theme.button_hover_color,
        activeforeground=config.theme.button_hover_text_color,
        command=command
    )

def invert_icon_colors(image, hex_color=config.theme.icon_color):
    image = image.convert("RGBA")
    pixels = image.load()
    # Convert hex color to RGB
    target_color = tuple(int(hex_color.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
    for i in range(image.width):
        for j in range(image.height):
            r, g, b, a = pixels[i, j]
            if r == 0 and g == 0 and b == 0:
                pixels[i, j] = (*target_color, a)
    return image

def load_icons(icon_names):
    icons = {}
    for name in icon_names:
        image_path = os.path.join(os.path.dirname(__file__), "icons", f"{name}.png")
        image = Image.open(image_path).resize((24, 24))
        image = invert_icon_colors(image)
        icons[name] = ImageTk.PhotoImage(image)
    return icons


###################################Create content#####################################

def open_remote_image():
    filepath = filedialog.askopenfilename(title="Select Remote Control Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
    if filepath:
        img_window = tk.Toplevel()
        img_window.title("Remote Control")
        img = Image.open(filepath)
        img = img.resize((500, 300))  # Resize as needed
        photo = ImageTk.PhotoImage(img)
        label = tk.Label(img_window, image=photo)
        label.image = photo
        label.pack()

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


###################################create pages#####################################
def create_placeholder_content(parent, title):
    tk.Label(parent, text=f"This is the {title} page", font=(config.theme.font_family, 18), bg=config.theme.background_color, fg="white").pack(pady=20)

def create_pages(main_content, page_titles):
    pages = {}
    main_content.grid_rowconfigure(1, weight=1)
    main_content.grid_columnconfigure(0, weight=1)
    for title in page_titles:
        page_frame = tk.Frame(main_content, bg=config.theme.page_color)
        page_frame.grid_rowconfigure(0, weight=1)
        page_frame.grid_columnconfigure(0, weight=1)
        content_wrapper = tk.Frame(page_frame, bg=config.theme.page_color)
        content_wrapper.grid(row=0, column=0, sticky="nsew")

        if title == "Home":
            create_home_content(content_wrapper)
        elif title == "Lists":
            create_list_content(content_wrapper)
        elif title == "Settings":
            create_settings_content(content_wrapper)
        elif title == "Music":
            create_music_content(content_wrapper)
        elif title == "Notes":
            create_notes_content(content_wrapper)
        elif title == "Alarm":
            create_alarm_content(content_wrapper)
        else:
            create_placeholder_content(content_wrapper, title)

        pages[title] = page_frame
    return pages


def main():
    global root, sidebar, main_content, sidebar_width, pages, header_title
    
    icon_names = ["home","notes", "music","list","alarm", "settings"]
    page_titles = ["Home","Notes", "Music","Lists", "Alarm", "Settings"]
    menu_items = [
    (page_titles[0], "home"),
    (page_titles[1], "notes"),
    (page_titles[2], "music"),
    (page_titles[3], "list"),
    (page_titles[4], "alarm"),
    (page_titles[5], "settings")
]
    
    root = tk.Tk()
    root.title("BEMO Smart Table")
    root.geometry("2560x1440")
    root.configure(bg=config.theme.root_color)
    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(0, weight=1)
    sidebar_width = config.theme.sidebar_width
    root.resizable(True, True)
    
    main_content = tk.Frame(root, bg=config.theme.root_color)
    main_content.grid(row=0, column=1, sticky="nsew")
    for row in range(2):
        for col in range(1):
            cell = tk.Frame(main_content, bg=config.theme.root_color)
            cell.grid(row=row, column=col, sticky="nsew")
            main_content.grid_rowconfigure(row, weight=(0 if row == 0 else 1))
            main_content.grid_columnconfigure(col, weight=1)

    sidebar = tk.Frame(root, bg=config.theme.background_color, width=sidebar_width, height=650)
    sidebar.grid(row=0, column=0, sticky="ns")
    sidebar.grid_propagate(False)
    root.grid_columnconfigure(0, weight=0, minsize=sidebar_width)

    icons = load_icons(icon_names)

    header_title = setup_header(main_content)
    pages = create_pages(main_content, page_titles)
    setup_sidebar(menu_items, icons, pages, sidebar, header_title)
    show_page("Home", pages, header_title)  # ← now opens Home first
    root.mainloop()


if __name__ == "__main__":
    main()