import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os
from pygame import mixer
from box import Box
import yaml
from .music import create_music_content
from .setting import create_settings_content
from .lists import create_list_content
from .pages import show_page
from .sidebar import setup_sidebar
from .header import setup_header
from .notes import create_notes_content
from .alarm import create_alarm_content
from .home import create_home_content
from .init_serial import init_serial
import threading
from gui import CONFIG_PATH


current_image_label = None  # global holder to access image widget
displayed_image = None      # to prevent image from being garbage collected

mixer.init()

# Load config.yaml
with open(CONFIG_PATH, "r") as file:
    config = Box(yaml.safe_load(file))

init_serial(config.serial.port1, config.serial.baudrate, config.serial.timeout)  # Initialize serial connection
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