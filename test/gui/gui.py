import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# Set up the main application window
root = tk.Tk()
root.title("BEMO Smart Table")
root.geometry("1100x650")
root.configure(bg="#1a1f2c")  # Elegant dark navy background
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)

# Sidebar toggle state
sidebar_visible = True
sidebar_width = 220
sidebar_height = 650

# Sidebar frame
sidebar = tk.Frame(root, bg="#101623", width=sidebar_width, height=sidebar_height)
sidebar.grid(row=0, column=0, sticky="ns")
sidebar.grid_propagate(False)
root.grid_columnconfigure(0, weight=0, minsize=sidebar_width)

# Function to invert icon colors (black to white)
def invert_icon_colors(image):
    image = image.convert("RGBA")
    pixels = image.load()
    
    for i in range(image.width):
        for j in range(image.height):
            r, g, b, a = pixels[i, j]
            if r == 0 and g == 0 and b == 0:  # If it's black
                pixels[i, j] = (255, 255, 255, a)  # Change to white
    return image

# Load and process icons
icons = {}
icon_names = ["home", "control", "music", "stats", "list", "reminder", "alarm", "settings", "help"]
for name in icon_names:
    image = Image.open(f"/home/kronbii/github-repos/smart-interactive-desk/test/gui/icons/{name}.png").resize((18, 18))
    image = invert_icon_colors(image)  # Invert the icon colors to white
    icons[name] = ImageTk.PhotoImage(image)

# Sidebar menu items with associated icons
menu_items = [
    ("Home", "home"),
    ("Control", "control"),
    ("Music", "music"),
    ("Statistics", "stats"),
    ("Lists", "list"),
    ("Reminders", "reminder"),
    ("Alarms", "alarm"),
    ("Settings", "settings"),
    ("Help & Feedback", "help")
]

# Create a function to switch between pages
def show_page(page_name):
    for page in pages.values():
        page.grid_forget()  # Hide all pages
    pages[page_name].grid(row=0, column=1, sticky="nsew")  # Show the selected page

# Sidebar buttons
for item, icon_key in menu_items:
    btn = tk.Button(
        sidebar, text=f"  {item}", image=icons[icon_key], compound="left",
        anchor="w", bg="#101623", fg="white", relief="flat",
        padx=20, pady=12, font=("Segoe UI", 11), bd=0, highlightthickness=0,
        command=lambda name=item: show_page(name)  # Use lambda to pass the page name
    )
    btn.pack(fill="x", pady=3, padx=5)
    btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#1f2b3a"))
    btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#101623"))

# Main content frame
main_content = tk.Frame(root, bg="#1a1f2c")
main_content.grid(row=0, column=1, sticky="nsew")
main_content.columnconfigure(0, weight=1)
main_content.rowconfigure(1, weight=1)

# Title / header frame
header = tk.Frame(main_content, bg="#1a1f2c")
header.grid(row=0, column=0, sticky="ew", padx=30, pady=(30, 15))
header.columnconfigure(1, weight=1)

# Hamburger menu button
sidebar_animating = False

def toggle_sidebar():
    global sidebar_visible
    if sidebar_visible:
        animate_sidebar_hide()
    else:
        animate_sidebar_show()
    sidebar_visible = not sidebar_visible

def animate_sidebar_hide():
    def step():
        current_width = sidebar.winfo_width()
        if current_width > 0:
            new_width = max(current_width - 20, 0)
            sidebar.config(width=new_width)
            root.grid_columnconfigure(0, minsize=new_width)
            root.after(10, step)
        else:
            sidebar.grid_remove()
            root.grid_columnconfigure(0, minsize=0)
    step()

def animate_sidebar_show():
    sidebar.grid()
    sidebar.config(width=0)
    root.grid_columnconfigure(0, minsize=0)
    def step():
        current_width = sidebar.winfo_width()
        if current_width < sidebar_width:
            new_width = min(current_width + 20, sidebar_width)
            sidebar.config(width=new_width)
            root.grid_columnconfigure(0, minsize=new_width)
            root.after(10, step)
        else:
            root.grid_columnconfigure(0, minsize=sidebar_width)
    step()

hamburger_btn = tk.Button(header, text="☰", font=("Segoe UI", 16), bg="#1a1f2c", fg="white", bd=0, relief="flat", command=toggle_sidebar)
hamburger_btn.grid(row=0, column=0, sticky="w")

# Title label
title = tk.Label(header, text="Favorites", bg="#1a1f2c", fg="white",
                 font=("Segoe UI", 20, "bold"), anchor="w")
title.grid(row=0, column=1, sticky="w", padx=(10, 0))

# Page containers (each frame will represent a page)
home_page = tk.Frame(main_content, bg="#1a1f2c")
control_page = tk.Frame(main_content, bg="#1a1f2c")
music_page = tk.Frame(main_content, bg="#1a1f2c")
stats_page = tk.Frame(main_content, bg="#1a1f2c")
lists_page = tk.Frame(main_content, bg="#1a1f2c")
reminders_page = tk.Frame(main_content, bg="#1a1f2c")
alarms_page = tk.Frame(main_content, bg="#1a1f2c")
settings_page = tk.Frame(main_content, bg="#1a1f2c")
help_page = tk.Frame(main_content, bg="#1a1f2c")

# Create a canvas to make the page content scrollable
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

# Populate these pages with content (sample content here)
home_page_container = create_scrollable_page(home_page)
home_label = tk.Label(home_page_container, text="This is the Home page", fg="white", bg="#1a1f2c")
home_label.grid(row=0, column=0, pady=50, padx=20)

control_page_container = create_scrollable_page(control_page)
control_label = tk.Label(control_page_container, text="This is the Control page", fg="white", bg="#1a1f2c")
control_label.grid(row=0, column=0, pady=50, padx=20)

music_page_container = create_scrollable_page(music_page)
music_label = tk.Label(music_page_container, text="This is the Music page", fg="white", bg="#1a1f2c")
music_label.grid(row=0, column=0, pady=50, padx=20)

stats_page_container = create_scrollable_page(stats_page)
stats_label = tk.Label(stats_page_container, text="This is the Statistics page", fg="white", bg="#1a1f2c")
stats_label.grid(row=0, column=0, pady=50, padx=20)

lists_page_container = create_scrollable_page(lists_page)
lists_label = tk.Label(lists_page_container, text="This is the Lists page", fg="white", bg="#1a1f2c")
lists_label.grid(row=0, column=0, pady=50, padx=20)

reminders_page_container = create_scrollable_page(reminders_page)
reminders_label = tk.Label(reminders_page_container, text="This is the Reminders page", fg="white", bg="#1a1f2c")
reminders_label.grid(row=0, column=0, pady=50, padx=20)

alarms_page_container = create_scrollable_page(alarms_page)
alarms_label = tk.Label(alarms_page_container, text="This is the Alarms page", fg="white", bg="#1a1f2c")
alarms_label.grid(row=0, column=0, pady=50, padx=20)

settings_page_container = create_scrollable_page(settings_page)
settings_label = tk.Label(settings_page_container, text="This is the Settings page", fg="white", bg="#1a1f2c")
settings_label.grid(row=0, column=0, pady=50, padx=20)

help_page_container = create_scrollable_page(help_page)
help_label = tk.Label(help_page_container, text="This is the Help & Feedback page", fg="white", bg="#1a1f2c")
help_label.grid(row=0, column=0, pady=50, padx=20)

# Add pages to a dictionary for easy access
pages = {
    "Home": home_page,
    "Control": control_page,
    "Music": music_page,
    "Statistics": stats_page,
    "Lists": lists_page,
    "Reminders": reminders_page,
    "Alarms": alarms_page,
    "Settings": settings_page,
    "Help & Feedback": help_page,
}

# Set the default page to show
show_page("Home")

# Run the app
root.mainloop()
