import tkinter as tk
from tkinter import ttk
from box import Box
import yaml
from gui import CONFIG_PATH

# Load config.yaml
with open(CONFIG_PATH, "r") as file:
    config = Box(yaml.safe_load(file))

def create_scrollable_page(page_frame):
    # Create Canvas with background color from theme
    canvas = tk.Canvas(page_frame, bg=config.theme.background_color, highlightthickness=0)
    
    # Create Vertical Scrollbar with customized appearance
    scroll_y = tk.Scrollbar(page_frame, orient="vertical", command=canvas.yview)
    canvas.config(yscrollcommand=scroll_y.set)
    scroll_y.pack(side="right", fill="y")

    # Pack Canvas
    canvas.pack(side="left", fill="both", expand=True)

    # Create Container Frame for the content inside the canvas
    page_container = tk.Frame(canvas, bg=config.theme.background_color)
    canvas.create_window((0, 0), window=page_container, anchor="nw")

    # Configure grid settings for page_container
    page_container.grid_rowconfigure(0, weight=1)
    page_container.grid_columnconfigure(0, weight=1)

    return page_container


def show_page(page_name, pages, header_title):
    for page in pages.values():
        page.grid_forget()
    pages[page_name].grid(row=1, column=0, columnspan=2, sticky="nsew")
    header_title.config(text=page_name)
    