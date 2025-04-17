import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import subprocess
import platform
import threading
from pygame import mixer
from tkinter import filedialog

mixer.init()

###################################Functions#####################################


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
    canvas = tk.Canvas(page_frame, bg="#1a1f2c")
    scroll_y = tk.Scrollbar(page_frame, orient="vertical", command=canvas.yview)
    canvas.config(yscrollcommand=scroll_y.set)
    scroll_y.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    page_container = tk.Frame(canvas, bg="#1a1f2c")
    canvas.create_window((0, 0), window=page_container, anchor="nw")
    page_container.grid_rowconfigure(0, weight=1)
    page_container.grid_columnconfigure(0, weight=1)
    return page_container

def show_page(page_name, pages):
    for page in pages.values():
        page.grid_forget()
    pages[page_name].grid(row=1, column=0, columnspan=2, sticky="nsew")
    header_title.config(text=page_name)

def setup_sidebar(menu_items, icons, pages, sidebar):
    for item, icon_key in menu_items:
        btn = tk.Button(
            sidebar, text=f"  {item}", image=icons[icon_key], compound="left",
            anchor="w", bg="#101623", fg="white", relief="flat",
            padx=20, pady=17, font=("Segoe UI", 11), bd=0, highlightthickness=0,
            command=lambda name=item: show_page(name, pages)
        )
        btn.pack(fill="x", pady=3, padx=5)
        btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#1f2b3a"))
        btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#101623"))

def setup_header(main_content):
    header = tk.Frame(main_content, bg="#1a1f2c", highlightbackground="green", highlightthickness=4)
    header.grid(row=0, column=0, sticky="new", padx=30, pady=(30, 15))
    header.columnconfigure(1, weight=1)
    title = tk.Label(header, text="", bg="#1a1f2c", fg="white", font=("Segoe UI", 20, "bold"), anchor="w")
    title.grid(row=0, column=1, sticky="w", padx=(10, 0))
    return title

###################################Create content#####################################


def create_music_content(parent):
    parent.configure(bg="#1a1f2c")

    # Header
    tk.Label(parent, text="🎶Music Player", font=("Segoe UI", 18), bg="#1a1f2c", fg="white").pack(pady=20)

    # Song Info Label
    global label_song
    label_song = tk.Label(parent, text="No song playing", font=("Segoe UI", 12, "italic"), bg="#1a1f2c", fg="white")
    label_song.pack(pady=10)

    # Buttons: Play, Pause, Stop
    button_frame = tk.Frame(parent, bg="#1a1f2c")
    button_frame.pack(pady=20)

    # Play Button
    play_button = tk.Button(button_frame, text="Play 🎧", command=play_music, bg="#2e3a59", fg="white", font=("Segoe UI", 14, "bold"), padx=15, pady=5)
    play_button.grid(row=0, column=0, padx=10)

    # Pause Button
    pause_button = tk.Button(button_frame, text="Pause ⏸️", command=pause_music, bg="#2e3a59", fg="white", font=("Segoe UI", 14, "bold"), padx=15, pady=5)
    pause_button.grid(row=0, column=1, padx=10)

    # Unpause Button
    unpause_button = tk.Button(button_frame, text="Unpause ▶️", command=unpause_music, bg="#2e3a59", fg="white", font=("Segoe UI", 14, "bold"), padx=15, pady=5)
    unpause_button.grid(row=0, column=2, padx=10)

    # Stop Button
    stop_button = tk.Button(button_frame, text="Stop 🛑", command=stop_music, bg="#2e3a59", fg="white", font=("Segoe UI", 14, "bold"), padx=15, pady=5)
    stop_button.grid(row=0, column=3, padx=10)

    # Volume Control Slider
    volume_label = tk.Label(parent, text="Volume 🎚️", font=("Segoe UI", 14), bg="#1a1f2c", fg="white")
    volume_label.pack(pady=10)

    volume_slider = tk.Scale(
        parent,
        from_=0,
        to=100,
        orient="horizontal",
        command=set_volume,
        bg="#1a1f2c",
        fg="white",
        sliderlength=20,
        length=300  # Wider slider here
    )
    volume_slider.set(50)  # Set default volume to 50%
    volume_slider.pack(pady=10)

    
def create_home_content(parent):
    parent.configure(bg="#1a1f2c")

    tk.Label(parent, text="📊 Statistics Overview", font=("Segoe UI", 18, "bold"), bg="#1a1f2c", fg="white").pack(pady=20)

    stats_frame = tk.Frame(parent, bg="#1a1f2c")
    stats_frame.pack(pady=10)

    stats = [
        ("🧍 Time Standing", "120", "min"),
        ("🪑 Time Sitting", "0", "min"),
        ("🖥️ Time on Table", "120", "min"),
    ]

    colors = ["#3a4a6d", "#2e3a59", "#4e5a7d"]

    for i, (label_text, value, unit) in enumerate(stats):
        stat_box = tk.Frame(stats_frame, bg=colors[i % len(colors)], padx=20, pady=10, highlightbackground="#5c6bc0", highlightthickness=2)
        stat_box.pack(pady=5, fill="x", padx=20)

        tk.Label(stat_box, text=label_text, font=("Segoe UI", 14, "bold"), bg=colors[i % len(colors)], fg="white").grid(row=0, column=0, sticky="w")
        tk.Label(stat_box, text=value, font=("Segoe UI", 14), bg=colors[i % len(colors)], fg="white").grid(row=0, column=1, padx=10)
        tk.Label(stat_box, text=unit, font=("Segoe UI", 14), bg=colors[i % len(colors)], fg="white").grid(row=0, column=2)



def create_settings_content(parent):
    for widget in parent.winfo_children():
        widget.destroy()

    parent.configure(bg="#1a1f2c")

    title = tk.Label(
        parent,
        text="⚙️ Settings Page",
        font=("Segoe UI", 20, "bold"),  # Match button font style
        bg="#1a1f2c",
        fg="white"  # Match button text color
    )
    title.grid(row=0, column=0, columnspan=2, pady=(30, 20))

    # Bluetooth button
    bluetooth_btn = tk.Button(
        parent,
        text="🔵 Bluetooth Settings",
        command=open_bluetooth_settings,
        bg="#3a506b",
        fg="white",
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
        bg="#3a506b",
        fg="white",
        font=("Segoe UI", 12, "bold"),
        padx=20,
        pady=10,
        relief="groove"
    )
    wifi_btn.grid(row=1, column=1, padx=30, pady=10, sticky="ew")

    # Make columns expand evenly
    parent.grid_columnconfigure(0, weight=1)
    parent.grid_columnconfigure(1, weight=1)


def create_control_content(parent):
    style = ttk.Style()
    style.theme_use("clam")

    style.configure(
        "Base.TButton",
        font=("Segoe UI", 12, "bold"),
        padding=(25, 15),
        foreground="#ffffff",
        background="#2e3a59",
        borderwidth=0,
        relief="flat",
        focuscolor="none"
    )
    style.map("Base.TButton", background=[("active", "#3e4a6d")], foreground=[("active", "#ffffff")])

    style.layout("Rounded.TButton", [
        ("Button.border", {"children": [("Button.padding", {"children": [("Button.label", {"sticky": "nswe"})]})], "sticky": "nswe"})
    ])
    style.configure("Rounded.TButton", borderwidth=5, relief="flat", background="#2e3a59", padding=(25, 15), foreground="white", font=("Segoe UI", 12, "bold"))
    style.map("Rounded.TButton", background=[("active", "#3e4a6d")])

    frame = tk.Frame(parent, bg="#1a1f2c")
    frame.pack(pady=40)

    def on_button_release():
        send_command("stop")

    # Command buttons
    up_btn = ttk.Button(frame, text="↑ Up", style="Rounded.TButton")
    down_btn = ttk.Button(frame, text="↓ Down", style="Rounded.TButton")
    tilt_up_btn = ttk.Button(frame, text="↥ Tilt Up", style="Rounded.TButton")
    tilt_down_btn = ttk.Button(frame, text="↧ Tilt Down", style="Rounded.TButton")
    stop_btn = ttk.Button(frame, text="■ Stop", style="Rounded.TButton", command=lambda: send_command("stop"))

    up_btn.bind("<ButtonPress-1>", lambda e: send_command("up"))
    up_btn.bind("<ButtonRelease-1>", lambda e: on_button_release())

    down_btn.bind("<ButtonPress-1>", lambda e: send_command("down"))
    down_btn.bind("<ButtonRelease-1>", lambda e: on_button_release())

    tilt_up_btn.bind("<ButtonPress-1>", lambda e: send_command("tilt up"))
    tilt_up_btn.bind("<ButtonRelease-1>", lambda e: on_button_release())

    tilt_down_btn.bind("<ButtonPress-1>", lambda e: send_command("tilt down"))
    tilt_down_btn.bind("<ButtonRelease-1>", lambda e: on_button_release())

    # Dynamic variables
    height_var = tk.StringVar(value="0 cm")  # Starting value for height
    tilt_var = tk.StringVar(value="0°")     # Starting value for tilt

    # Static text labels with dynamic value next to them
    height_label = tk.Label(frame, text="Height:", bg="white", fg="black",
                            
                            font=("Segoe UI", 10, "bold"), width=15, height=2)
    height_value_label = tk.Label(frame, textvariable=height_var, bg="white", fg="black",
                                  font=("Segoe UI", 10, "bold"), width=15, height=2)

    tilt_label = tk.Label(frame, text="Tilt:", bg="white", fg="black",
                          font=("Segoe UI", 10, "bold"), width=15, height=2)
    tilt_value_label = tk.Label(frame, textvariable=tilt_var, bg="white", fg="black",
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
    parent.configure(bg="#1a1f2c")
    parent.grid_rowconfigure(1, weight=1)  # Let the notes area expand vertically
    parent.grid_columnconfigure(0, weight=1)  # Let the notes area expand horizontally

    # Header
    tk.Label(
        parent,
        text="📝 Notes Page",
        font=("Segoe UI", 18, "bold"),
        bg="#1a1f2c",
        fg="#ffcc00"
    ).grid(row=0, column=0, pady=20)

    # Notes Text Box inside a Frame with padding
    text_frame = tk.Frame(parent, bg="#1a1f2c", padx=20, pady=10)
    text_frame.grid(row=1, column=0, sticky="nsew")
    text_frame.grid_rowconfigure(0, weight=1)
    text_frame.grid_columnconfigure(0, weight=1)

    notes_text = tk.Text(
        text_frame,
        wrap="word",
        font=("Segoe UI", 12),
        bg="#2e3a59",
        fg="white",
        insertbackground="white",
        relief="flat"
    )
    notes_text.grid(row=0, column=0, sticky="nsew")

    # Buttons Frame
    buttons_frame = tk.Frame(parent, bg="#1a1f2c")
    buttons_frame.grid(row=2, column=0, pady=10)

    # Save Note Button
    tk.Button(
        buttons_frame,
        text="💾 Save Note",
        font=("Segoe UI", 12, "bold"),
        bg="#3a506b",
        fg="white",
        padx=10,
        pady=5,
        relief="groove",
        command=lambda: save_note(notes_text.get("1.0", "end-1c"))
    ).grid(row=0, column=0, padx=5)

    # Update Note Button
    tk.Button(
        buttons_frame,
        text="🔄 Update Note",
        font=("Segoe UI", 12, "bold"),
        bg="#3a506b",
        fg="white",
        padx=10,
        pady=5,
        relief="groove",
        command=lambda: update_note(notes_text.get("1.0", "end-1c"))
    ).grid(row=0, column=1, padx=5)

    # Delete Note Button
    tk.Button(
        buttons_frame,
        text="❌ Delete Note",
        font=("Segoe UI", 12, "bold"),
        bg="#3a506b",
        fg="white",
        padx=10,
        pady=5,
        relief="groove",
        command=delete_note
    ).grid(row=0, column=2, padx=5)

def create_list_content(parent):
    # Main container frame
    task_frame = tk.Frame(parent, bg="#1a1f2c")
    task_frame.pack(pady=20, fill="both", expand=True)

    # Input for new task — Entry + Button (TOP)
    task_entry_frame = tk.Frame(task_frame, bg="#1a1f2c")
    task_entry_frame.pack(fill="x", pady=(0, 10))

    task_entry = tk.Entry(task_entry_frame, font=("Segoe UI", 12), bg="#3e4a6d", fg="white", insertbackground="white")
    task_entry.pack(side="left", padx=(10, 5), fill="x", expand=True)

    add_task_btn = tk.Button(task_entry_frame, text="Add Task", font=("Segoe UI", 12, "bold"),
                             bg="#2e3a59", fg="white", command=lambda: add_task())
    add_task_btn.pack(side="right", padx=(5, 10))

    # Scrollable canvas for tasks
    canvas_frame = tk.Frame(task_frame, bg="#1a1f2c")
    canvas_frame.pack(fill="both", expand=True)

    canvas = tk.Canvas(canvas_frame, bg="#1a1f2c", highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    # Frame inside canvas to hold all tasks
    task_list_frame = tk.Frame(canvas, bg="#1a1f2c")
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
        elif title == "Control Panel":
            create_control_content(content_wrapper)
        elif title == "Lists":
            create_list_content(content_wrapper)
        elif title == "Settings":
            create_settings_content(content_wrapper)
        elif title == "Music":
            create_music_content(content_wrapper)
        elif title == "Notes":
            create_notes_content(content_wrapper)
        else:
            create_placeholder_content(content_wrapper, title)

        pages[title] = page_frame
    return pages


###################################Add page icon and name#####################################


def main():
    global root, sidebar, main_content, sidebar_width, pages, header_title
    
    icon_names = ["home", "control","notes", "music","list","alarm", "settings", "help"]
    page_titles = ["Home", "Control Panel","Notes", "Music","Lists", "Reminders and Alarms", "Settings", "Help & Feedback"]
    menu_items = [
    (page_titles[0], "home"),
    (page_titles[1], "control"),
    (page_titles[2], "notes"),
    (page_titles[3], "music"),
    (page_titles[4], "list"),
    (page_titles[5], "alarm"),
    (page_titles[6], "settings"),
    (page_titles[7], "help")
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

    sidebar = tk.Frame(root, bg="#101623", width=sidebar_width, height=650)
    sidebar.grid(row=0, column=0, sticky="ns")
    sidebar.grid_propagate(False)
    root.grid_columnconfigure(0, weight=0, minsize=sidebar_width)

    icons = load_icons(icon_names)

    header_title = setup_header(main_content)
    pages = create_pages(main_content, page_titles)
    setup_sidebar(menu_items, icons, pages, sidebar)
    show_page("Control Panel", pages)
    root.mainloop()

if __name__ == "__main__":
    main()