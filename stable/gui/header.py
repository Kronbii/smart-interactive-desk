import tkinter as tk
import os
from box import Box
import yaml

CONFIG_PATH = os.path.join("/home/kronbii/github-repos/smart-interactive-desk/stable/gui/config.yaml")
# Load config.yaml
with open(CONFIG_PATH, "r") as file:
    config = Box(yaml.safe_load(file))

def setup_header(main_content):
    header = tk.Frame(main_content, bg=config.theme.background_color)
    header.grid(row=0, column=0, sticky="new", padx=30, pady=(30, 15))
    header.columnconfigure(1, weight=1)
    title = tk.Label(header, text="", bg=config.theme.background_color, fg=config.theme.font_color, font=(config.theme.font_family, 20, "bold"), anchor="w")
    title.grid(row=0, column=1, sticky="w", padx=(10, 0))
    return title