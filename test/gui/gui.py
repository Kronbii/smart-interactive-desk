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

current_image_label = None  # global holder to access image widget
displayed_image = None      # to prevent image from being garbage collected

mixer.init()

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
CONFIG_PATH = os.path.join(ROOT_DIR, "config.yaml")

# Load config.yaml
with open(CONFIG_PATH, "r") as file:
    config = yaml.safe_load(file)
###################################Functions#####################################

def load_theme():
    with open("config.yaml", "r") as file:
        return yaml.safe_load(file)["theme"]

def set_background(parent):
    parent.configure(bg=theme.background_color)

# Function to create a themed label
def create_label(parent, text, font_size=12, font_weight="normal", bg_color=None, fg_color=None):
    bg_color = bg_color or theme.background_color
    fg_color = fg_color or theme.font_color
    return tk.Label(
        parent,
        text=text,
        font=(theme.font_family, font_size, font_weight),
        bg=bg_color,
        fg=fg_color
    )

# Function to create a themed button
def create_button(parent, text, command, font_size=12, bg_color=None, fg_color=None):
    bg_color = bg_color or theme.button_color
    fg_color = fg_color or theme.button_text_color
    return tk.Button(
        parent,
        text=text,
        font=(theme.font_family, font_size, "bold"),
        bg=bg_color,
        fg=fg_color,
        activebackground=theme.button_hover_color,
        activeforeground=theme.button_hover_text_color,
        command=command
    )



def open_qr_and_run_js():
    # === Image and JS Paths ===
    image_path = "/home/berjawi/Documents/smart-interactive-desk/test/gui/QR.png"
    js_script_path = "/home/berjawi/Documents/smart-interactive-desk/test/web/server.js"

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



def save_note(text):
    with open("note.txt", "w") as file:
        file.write(text)
    print("Note saved.")

def update_note(text):
    with open("note.txt", "w") as file:
        file.write(text)
    print("Note updated.")

def delete_note():
    with open("note.txt", "w") as file:
        file.write("")
    print("Note deleted.")

def play_music():
    song = filedialog.askopenfilename(title="Choose a song", filetypes=[("Audio Files", "*.mp3 *.wav")])
    if song:
        mixer.music.load(song)
        mixer.music.play()
        label_song.config(text=f"Now Playing: {song.split('/')[-1]}")  # Display song name

def pause_music():
    mixer.music.pause()
    label_song.config(text="Music Paused... 😴")

def unpause_music():
    mixer.music.unpause()
    label_song.config(text="Resumed 🎶")

def stop_music():
    mixer.music.stop()
    label_song.config(text="Music Stopped... 🎵")

def set_volume(val):
    mixer.music.set_volume(float(val) / 100)


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

def send_command(command):
    # Placeholder function for sending commands
    print(f"Command sent: {command}")

def invert_icon_colors(image):
    image = image.convert("RGBA")
    pixels = image.load()
    for i in range(image.width):
        for j in range(image.height):
            r, g, b, a = pixels[i, j]
            if r == 0 and g == 0 and b == 0:
                pixels[i, j] = (255, 255, 255, a)
    return image

def load_icons(icon_names):
    icons = {}
    for name in icon_names:
        image_path = os.path.join(os.path.dirname(__file__), "icons", f"{name}.png")
        image = Image.open(image_path).resize((24, 24))
        image = invert_icon_colors(image)
        icons[name] = ImageTk.PhotoImage(image)
    return icons

def create_scrollable_page(page_frame):
    theme = load_theme()  # Get the theme settings

    # Create Canvas with background color from theme
    canvas = tk.Canvas(page_frame, bg=theme["background_color"])
    
    # Create Vertical Scrollbar with customized appearance
    scroll_y = tk.Scrollbar(page_frame, orient="vertical", command=canvas.yview)
    canvas.config(yscrollcommand=scroll_y.set)
    scroll_y.pack(side="right", fill="y")

    # Pack Canvas
    canvas.pack(side="left", fill="both", expand=True)

    # Create Container Frame for the content inside the canvas
    page_container = tk.Frame(canvas, bg=theme["background_color"])
    canvas.create_window((0, 0), window=page_container, anchor="nw")

    # Configure grid settings for page_container
    page_container.grid_rowconfigure(0, weight=1)
    page_container.grid_columnconfigure(0, weight=1)

    return page_container


def show_page(page_name, pages):
    for page in pages.values():
        page.grid_forget()
    pages[page_name].grid(row=1, column=0, columnspan=2, sticky="nsew")
    header_title.config(text=page_name)

def setup_sidebar(menu_items, icons, pages, sidebar):
    theme = load_theme()  # Get the theme settings
    for item, icon_key in menu_items:
        btn = tk.Button(
            sidebar, 
            text=f"  {item}",
            image=icons[icon_key],
            compound="left",
            anchor="w",
            bg=theme["button_color"],  # Apply button color from theme
            fg=theme["button_text_color"],  # Apply text color from theme
            relief="flat",
            padx=20,
            pady=17,
            font=("Segoe UI", 11),
            bd=0,
            highlightthickness=0,
            command=lambda name=item: show_page(name, pages)
        )
        btn.pack(fill="x", pady=3, padx=5)
        btn.bind("<Enter>", lambda e, b=btn: b.config(bg=theme["button_hover_color"]))  # Hover effect from theme
        btn.bind("<Leave>", lambda e, b=btn: b.config(bg=theme["button_color"]))  # Default color from theme

def setup_header(main_content):
    theme = load_theme()  # Get the theme settings
    header = tk.Frame(main_content, bg=theme["background_color"], highlightbackground="green", highlightthickness=4)
    header.grid(row=0, column=0, sticky="new", padx=30, pady=(30, 15))
    header.columnconfigure(1, weight=1)
    title = tk.Label(header, text="", bg=theme["background_color"], fg=theme["font_color"], font=("Segoe UI", 20, "bold"), anchor="w")
    title.grid(row=0, column=1, sticky="w", padx=(10, 0))
    return title


###################################Create content#####################################

def create_alarm_content(parent):
    theme = load_theme()  # Get the theme settings

    parent.configure(bg=theme['background_color'])

    # Clear previous widgets
    for widget in parent.winfo_children():
        widget.destroy()

    # Header (normal weight)
    tk.Label(
        parent,
        text="⏰ Alarm / Reminder",
        font=("Segoe UI", 18),  # Removed "bold"
        bg=theme['background_color'],
        fg=theme['accent_color']
    ).pack(pady=20)

    # Time selector frame (centered)
    time_frame = tk.Frame(parent, bg=theme['background_color'])
    time_frame.pack(pady=10)

    tk.Label(time_frame, text="Time:", font=("Segoe UI", 12), bg=theme['background_color'], fg=theme['font_color']).grid(row=0, column=0, columnspan=3, pady=(0, 5))

    hours = [f"{h:02}" for h in range(1, 13)]
    minutes = [f"{m:02}" for m in range(0, 60)]
    am_pm = ["AM", "PM"]

    hour_box = ttk.Combobox(time_frame, values=hours, width=7, state="readonly", font=("Segoe UI", 14))
    hour_box.current(0)
    hour_box.grid(row=1, column=0, padx=10, pady=5)

    minute_box = ttk.Combobox(time_frame, values=minutes, width=7, state="readonly", font=("Segoe UI", 14))
    minute_box.current(0)
    minute_box.grid(row=1, column=1, padx=10, pady=5)

    am_pm_box = ttk.Combobox(time_frame, values=am_pm, width=7, state="readonly", font=("Segoe UI", 14))
    am_pm_box.current(0)
    am_pm_box.grid(row=1, column=2, padx=10, pady=5)

    # Message input below time selectors
    msg_frame = tk.Frame(parent, bg=theme['background_color'])
    msg_frame.pack(pady=(20, 10))

    tk.Label(msg_frame, text="Message:", font=("Segoe UI", 12), bg=theme['background_color'], fg=theme['font_color']).pack(anchor="w")
    message_entry = tk.Entry(msg_frame, font=("Segoe UI", 12), width=40)
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
        font=("Segoe UI", 12, "bold"),
        bg=theme['button_color'],
        fg=theme['button_text_color'],
        padx=20,
        pady=10,
        relief="groove",
        command=on_set_reminder
    ).pack(pady=20)


def create_music_content(parent):
    theme = load_theme()  # Get the theme settings

    parent.configure(bg=theme["background_color"])

    # Header
    tk.Label(
        parent,
        text="🎶Music Player",
        font=("Segoe UI", 18),
        bg=theme["background_color"],
        fg=theme["font_color"]
    ).pack(pady=20)

    # Song Info Label
    global label_song
    label_song = tk.Label(
        parent,
        text="No song playing",
        font=("Segoe UI", 12, "italic"),
        bg=theme["background_color"],
        fg=theme["font_color"]
    )
    label_song.pack(pady=10)

    # Buttons: Play, Pause, Stop
    button_frame = tk.Frame(parent, bg=theme["background_color"])
    button_frame.pack(pady=20)

    # Play Button
    play_button = tk.Button(
        button_frame,
        text="Play 🎧",
        command=play_music,
        bg=theme["button_color"],
        fg=theme["button_text_color"],
        font=("Segoe UI", 14, "bold"),
        padx=15,
        pady=5
    )
    play_button.grid(row=0, column=0, padx=10)

    # Pause Button
    pause_button = tk.Button(
        button_frame,
        text="Pause ⏸️",
        command=pause_music,
        bg=theme["button_color"],
        fg=theme["button_text_color"],
        font=("Segoe UI", 14, "bold"),
        padx=15,
        pady=5
    )
    pause_button.grid(row=0, column=1, padx=10)

    # Unpause Button
    unpause_button = tk.Button(
        button_frame,
        text="Unpause ▶️",
        command=unpause_music,
        bg=theme["button_color"],
        fg=theme["button_text_color"],
        font=("Segoe UI", 14, "bold"),
        padx=15,
        pady=5
    )
    unpause_button.grid(row=0, column=2, padx=10)

    # Stop Button
    stop_button = tk.Button(
        button_frame,
        text="Stop 🛑",
        command=stop_music,
        bg=theme["button_color"],
        fg=theme["button_text_color"],
        font=("Segoe UI", 14, "bold"),
        padx=15,
        pady=5
    )
    stop_button.grid(row=0, column=3, padx=10)

    # Volume Control Label
    volume_label = tk.Label(
        parent,
        text="Volume 🎚️",
        font=("Segoe UI", 14),
        bg=theme["background_color"],
        fg=theme["font_color"]
    )
    volume_label.pack(pady=10)

    # Volume Control Slider
    volume_slider = tk.Scale(
        parent,
        from_=0,
        to=100,
        orient="horizontal",
        command=set_volume,
        bg=theme["background_color"],
        fg=theme["font_color"],
        sliderlength=20,
        length=300  # Wider slider here
    )
    volume_slider.set(50)  # Set default volume to 50%
    volume_slider.pack(pady=10)


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
    theme = load_theme()  # Get the theme settings

    parent.configure(bg=theme["background_color"])

    # === Control Section Title ===
    tk.Label(
        parent, 
        text="🕹️ Control", 
        font=("Poppins", 16, "bold"), 
        bg=theme["background_color"], 
        fg=theme["font_color"]
    ).pack(pady=(15, 5))

    # === Control Section ===
    control_frame = tk.Frame(parent, bg=theme["background_color"])
    control_frame.pack()
    height_var, tilt_var = create_control_content(control_frame)

    # === Statistics Section Title ===
    tk.Label(
        parent, 
        text="📊 Statistics Overview", 
        font=("Poppins", 16, "bold"), 
        bg=theme["background_color"], 
        fg=theme["font_color"]
    ).pack(pady=(20, 5))

    stats_frame = tk.Frame(parent, bg=theme["background_color"])
    stats_frame.pack(pady=5)

    stats = [
        ("🧍 Time Standing", "120", "min"),
        ("🪑 Time Sitting", "0", "min"),
        ("🖥️ Time on Table", "120", "min"),
    ]
    colors = [theme["container_color"], theme["container_color"], theme["container_color"]]

    stat_frame = tk.Frame(stats_frame, bg=theme["background_color"])
    stat_frame.pack(fill="x", padx=30, pady=5)

    for i, (label_text, value, unit) in enumerate(stats):
        stat_box = tk.Frame(
            stat_frame,
            bg=colors[i % len(colors)],
            padx=15,
            pady=8,
            highlightbackground=theme["container_color"],
            highlightthickness=2
        )
        stat_box.pack(side="left", padx=8, expand=True)

        tk.Label(
            stat_box, 
            text=label_text, 
            font=("Poppins", 12, "bold"), 
            bg=colors[i], 
            fg=theme["accent_color"]  # Using accent color for text
        ).pack(side="left")
        tk.Label(
            stat_box, 
            text=value, 
            font=("Poppins", 12), 
            bg=colors[i], 
            fg=theme["font_color"]
        ).pack(side="left", padx=5)
        tk.Label(
            stat_box, 
            text=unit, 
            font=("Poppins", 12), 
            bg=colors[i], 
            fg=theme["font_color"]
        ).pack(side="left")

    # === Remote Control Button ===
    tk.Button(
        parent,
        text="🖼️ Remote Control",
        command=open_qr_and_run_js,
        font=("Poppins", 12, "bold"),
        bg=theme["button_color"],
        fg=theme["button_text_color"],
        relief="raised"
    ).pack(pady=15)

    return height_var, tilt_var









def create_settings_content(parent):
    theme = load_theme()  # Get the theme settings

    parent.configure(bg=theme["background_color"])

    title = tk.Label(
        parent,
        text="⚙️ Settings Page",
        font=("Segoe UI", 20, "bold"),
        bg=theme["background_color"],
        fg=theme["font_color"]
    )
    title.grid(row=0, column=0, columnspan=2, pady=(30, 20))

    # Bluetooth button
    bluetooth_btn = tk.Button(
        parent,
        text="🔵 Bluetooth Settings",
        command=open_bluetooth_settings,
        bg=theme["button_color"],
        fg=theme["button_text_color"],
        font=("Segoe UI", 12, "bold"),
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
        bg=theme["button_color"],
        fg=theme["button_text_color"],
        font=("Segoe UI", 12, "bold"),
        padx=20,
        pady=10,
        relief="groove"
    )
    wifi_btn.grid(row=1, column=1, padx=30, pady=10, sticky="ew")

    parent.grid_columnconfigure(0, weight=1)
    parent.grid_columnconfigure(1, weight=1)


def create_control_content(parent):
    theme = load_theme()  # Get the theme settings

    parent.configure(bg=theme["background_color"])

    frame = tk.Frame(parent, bg=theme["background_color"])
    frame.pack(pady=40)

    def on_button_release():
        send_command("stop")

    # Command buttons
    up_btn = ttk.Button(frame, text="↑ Up", style="Rounded.TButton", command=lambda: send_command("up"))
    down_btn = ttk.Button(frame, text="↓ Down", style="Rounded.TButton", command=lambda: send_command("down"))
    tilt_up_btn = ttk.Button(frame, text="↥ Tilt Up", style="Rounded.TButton", command=lambda: send_command("tilt up"))
    tilt_down_btn = ttk.Button(frame, text="↧ Tilt Down", style="Rounded.TButton", command=lambda: send_command("tilt down"))
    stop_btn = ttk.Button(frame, text="■ Stop", style="Rounded.TButton", command=lambda: send_command("stop"))

    # Dynamic variables
    height_var = tk.StringVar(value="0 cm")  # Starting value for height
    tilt_var = tk.StringVar(value="0°")     # Starting value for tilt

    # Static text labels with dynamic value next to them
    height_label = tk.Label(frame, text="Height:", bg=theme["container_color"], fg=theme["accent_color"],
                            font=("Segoe UI", 10, "bold"), width=15, height=2)
    height_value_label = tk.Label(frame, textvariable=height_var, bg=theme["container_color"], fg=theme["accent_color"],
                                  font=("Segoe UI", 10, "bold"), width=15, height=2)

    tilt_label = tk.Label(frame, text="Tilt:", bg=theme["container_color"], fg=theme["accent_color"],
                          font=("Segoe UI", 10, "bold"), width=15, height=2)
    tilt_value_label = tk.Label(frame, textvariable=tilt_var, bg=theme["container_color"], fg=theme["accent_color"],
                                 font=("Segoe UI", 10, "bold"), width=15, height=2)

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


def create_notes_content(parent):
    global current_image_label

    theme = load_theme()  # Get the theme settings

    parent.configure(bg=theme["background_color"])

    # Expand image container to nearly full height
    image_frame = tk.Frame(parent, bg=theme["container_color"], height=300)
    image_frame.pack(fill="both", expand=True, padx=20, pady=(20, 10))
    image_frame.pack_propagate(False)

    current_image_label = tk.Label(image_frame, bg=theme["container_color"])
    current_image_label.pack(expand=True)

    # Button Container (horizontal alignment)
    button_frame = tk.Frame(parent, bg=theme["background_color"])
    button_frame.pack(pady=10)

    tk.Button(
        button_frame,
        text="📁 Load Image",
        font=("Segoe UI", 10, "bold"),
        bg=theme["button_color"],
        fg=theme["font_color"],
        command=load_image
    ).grid(row=0, column=0, padx=5)

    tk.Button(
        button_frame,
        text="📷 Capture Image",
        font=("Segoe UI", 10, "bold"),
        bg=theme["button_color"],
        fg=theme["font_color"],
        command=capture_image_from_webcam
    ).grid(row=0, column=1, padx=5)

    tk.Button(
        button_frame,
        text="🗑️ Remove Image",
        font=("Segoe UI", 10, "bold"),
        bg=theme["button_color"],
        fg=theme["font_color"],
        command=remove_image
    ).grid(row=0, column=2, padx=5)

    return





def create_list_content(parent):
    theme = load_theme()  # Get the theme settings

    # Main container frame
    task_frame = tk.Frame(parent, bg=theme["background_color"])
    task_frame.pack(pady=20, fill="both", expand=True)

    # Input for new task — Entry + Button (TOP)
    task_entry_frame = tk.Frame(task_frame, bg=theme["background_color"])
    task_entry_frame.pack(fill="x", pady=(0, 10))

    task_entry = tk.Entry(task_entry_frame, font=("Segoe UI", 12), bg="#3e4a6d", fg="white", insertbackground="white")
    task_entry.pack(side="left", padx=(10, 5), fill="x", expand=True)

    add_task_btn = tk.Button(task_entry_frame, text="Add Task", font=("Segoe UI", 12, "bold"),
                             bg="#2e3a59", fg="white", command=lambda: add_task())
    add_task_btn.pack(side="right", padx=(5, 10))

    # Scrollable canvas for tasks
    canvas_frame = tk.Frame(task_frame, bg=theme["background_color"])
    canvas_frame.pack(fill="both", expand=True)

    canvas = tk.Canvas(canvas_frame, bg=theme["background_color"], highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    # Frame inside canvas to hold all tasks
    task_list_frame = tk.Frame(canvas, bg=theme["background_color"])
    task_window = canvas.create_window((0, 0), window=task_list_frame, anchor="nw")

    # Allow resizing and scrolling
    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def on_canvas_configure(event):
        canvas.itemconfig(task_window, width=event.width)

    def on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    task_list_frame.bind("<Configure>", on_frame_configure)
    canvas.bind("<Configure>", on_canvas_configure)
    canvas.bind_all("<MouseWheel>", on_mousewheel)  # enable scrolling with mousewheel

    tasks = []

    def on_checkbox_toggle(task_name, var, task_box):
        if var.get():
            tasks.remove(task_name)
            task_box.destroy()
            refresh_task_list()

    def add_task():
        new_task = task_entry.get()
        if new_task.strip():
            tasks.append(new_task.strip())
            task_entry.delete(0, tk.END)
            refresh_task_list()

    def refresh_task_list():
        for widget in task_list_frame.winfo_children():
            widget.destroy()
        create_task_list()
        canvas.configure(scrollregion=canvas.bbox("all"))

    def create_task_list():
        for task in tasks:
            task_box = tk.Frame(task_list_frame, bg="#2e3a59", pady=10, padx=15, relief="solid", borderwidth=1)
            task_box.pack(fill="x", pady=5, padx=10)

            var = tk.BooleanVar()
            checkbox = tk.Checkbutton(
                task_box, variable=var, bg="#2e3a59", fg="white",
                selectcolor="#3e4a6d", activebackground="#2e4a69",
                command=lambda t=task, v=var, box=task_box: on_checkbox_toggle(t, v, box),
                font=("Segoe UI", 12), width=2
            )
            checkbox.pack(side="left", padx=10)

            label = tk.Label(task_box, text=task, bg="#2e3a59", fg="white", font=("Segoe UI", 12))
            label.pack(side="left", padx=10)

    # Optional: preload example tasks
    tasks.extend(["Example Task 1", "Example Task 2"])
    refresh_task_list()

    # 👉 Allow pressing Enter to add tasks
    task_entry.bind("<Return>", lambda event: add_task())

###################################create pages#####################################


def create_placeholder_content(parent, title):
    tk.Label(parent, text=f"This is the {title} page", font=("Segoe UI", 18), bg="#1a1f2c", fg="white").pack(pady=20)

def create_pages(main_content, page_titles):
    pages = {}
    main_content.grid_rowconfigure(1, weight=1)
    main_content.grid_columnconfigure(0, weight=1)
    for title in page_titles:
        page_frame = tk.Frame(main_content, bg="#1a1f2c", highlightbackground="pink", highlightthickness=6)
        page_frame.grid_rowconfigure(0, weight=1)
        page_frame.grid_columnconfigure(0, weight=1)
        content_wrapper = tk.Frame(page_frame, bg="#1a1f2c")
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


###################################Add page icon and name#####################################


def main():
    global root, sidebar, main_content, sidebar_width, pages, header_title
    
    icon_names = ["home","notes", "music","list","alarm", "settings", "help"]
    page_titles = ["Home","Notes", "Music","Lists", "Alarm", "Settings", "Help & Feedback"]
    menu_items = [
    (page_titles[0], "home"),
    (page_titles[1], "notes"),
    (page_titles[2], "music"),
    (page_titles[3], "list"),
    (page_titles[4], "alarm"),
    (page_titles[5], "settings"),
    (page_titles[6], "help")
]
    
    root = tk.Tk()
    root.title("BEMO Smart Table")
    root.geometry("2560x1440")
    root.configure(bg="#1a1f2c")
    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(0, weight=1)
    sidebar_width = 220

    main_content = tk.Frame(root, bg="#1a1f2c", highlightbackground="red", highlightthickness=6)
    main_content.grid(row=0, column=1, sticky="nsew")
    for row in range(2):
        for col in range(1):
            cell = tk.Frame(main_content, bg="#1a1f2c", highlightbackground="white", highlightthickness=1)
            cell.grid(row=row, column=col, sticky="nsew")
            main_content.grid_rowconfigure(row, weight=(0 if row == 0 else 1))
            main_content.grid_columnconfigure(col, weight=1)

    sidebar = tk.Frame(root, bg=theme["background_color"], width=sidebar_width, height=650)
    sidebar.grid(row=0, column=0, sticky="ns")
    sidebar.grid_propagate(False)
    root.grid_columnconfigure(0, weight=0, minsize=sidebar_width)

    icons = load_icons(icon_names)

    header_title = setup_header(main_content)
    pages = create_pages(main_content, page_titles)
    setup_sidebar(menu_items, icons, pages, sidebar)
    show_page("Home", pages)  # ← now opens Home first
    root.mainloop()


if __name__ == "__main__":
    main()